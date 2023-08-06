import numpy as np
from Bio import SeqIO

from bokeh.plotting import figure
from bokeh.models.tools import BoxZoomTool
from bokeh.models import HoverTool, NumeralTickFormatter, LabelSet
from bokeh.models.glyphs import Patches

import gffpandas.gffpandas as gffpd
from bokeh.models import (
    CustomJS,
    Range1d,
    ColumnDataSource,
)

from bokeh.io import output_notebook
output_notebook()

init_pos = 10000
init_win = 20000


def browser(genome_path: str, gff_path: str, 
             genome_format="fasta", 
             init_pos=init_pos, 
             init_win=init_win, 
             **kwargs):
    
    genome=next(SeqIO.parse(genome_path,genome_format))
    annotation = get_genome_annotations(gff_path)
    annotation.gene=annotation.gene.fillna("")
    annotation.gene=annotation[['gene','locus_tag']].apply(lambda x: f"{x[0]} {x[1]}",axis=1) #create names with both locus tag and gene name
    genes = get_genes_from_annotation(annotation)

    semi_win = init_win / 2
    init_left = init_pos - semi_win
    init_right = init_pos + semi_win
    x_range = Range1d(
            init_left, init_right, bounds=(init_left, init_right), 
            max_interval = 100000,
            min_interval = 50,
        )
    glyphSource = ColumnDataSource(get_gene_patches(genes, init_left, init_right))
    p=create_genome_browser_plot(glyphSource,x_range,**kwargs)


    sequence = {'base': list(str(genome.seq[int(init_left):int(init_right)]).upper()),
                                'x': list(range(int(init_left),int(init_right)))}

    seqSource = ColumnDataSource({'base': [" "],
                                'x': [0]})
    seqLabel = LabelSet(x='x', y=-1.98, text='base',
                      text_font_size='8pt', 
                      text_font_style='bold',
                      source=seqSource)
    p.add_layout(seqLabel)

    xcb= CustomJS(args={"x_range":p.x_range,"seqSource":seqSource,"sequence":sequence}, code="""
        let x_size = x_range.end - x_range.start;
        const seqdata = seqSource.data;
        const x = seqSource.data['x'];
        if (x_size<300){
            seqSource.data['base']=sequence['base'].slice(x_range.start-sequence['x'][0], x_range.end-sequence['x'][0]);
            seqSource.data['x']=sequence['x'].slice(x_range.start-sequence['x'][0], x_range.end-sequence['x'][0]);
        } else {
            seqSource.data['base']=[" "];
            seqSource.data['x']=[0]
        }
        seqSource.change.emit()
    """)

    p.x_range.js_on_change('start', xcb)
    p.x_range.js_on_change('end', xcb)
    return p

def create_genome_browser_plot(glyphSource, x_range, **kwargs):
    plot_height = kwargs.get("plot_height", 150)
    label_angle = kwargs.get("label_angle", 45)
    text_font_size = kwargs.get("text_font_size", "10pt")
    output_backend = kwargs.get("output_backend", "webgl")
    
    y_min, y_max = get_y_range()
    p_annot = figure(
        tools = "xwheel_zoom,xpan,save",
        active_scroll = "xwheel_zoom",
        height = plot_height,
        x_range = x_range,
        y_range = Range1d(y_min, y_max),
        output_backend=output_backend,
    )
    # Add tool
    p_annot.add_tools(BoxZoomTool(dimensions="width"))

    #p_annot.sizing_mode = "stretch_both"

    # Format x axis values
    p_annot.xaxis[0].formatter = NumeralTickFormatter(format="0,0")
    # Hide grid
    p_annot.xgrid.visible = False
    p_annot.ygrid.visible = False
    # Hide axis
    p_annot.yaxis.visible = False
    glyph = p_annot.add_glyph(
        glyphSource, Patches(xs="xs", ys="ys", fill_color="color")
    )
    # gene labels in the annotation track
    # This seems to be necessary to show the labels
    p_annot.scatter(x="pos", y=0, size=0, source=glyphSource)
    labels = LabelSet(
        x="pos",
        y=-0.9,
        text="names",
        level="glyph",
        angle=label_angle,
        text_font_size=text_font_size,
        x_offset=-5,
        y_offset=0,
        source=glyphSource,
        text_align='left',
    )

    p_annot.add_layout(labels)
    p_annot.add_tools(
        HoverTool(
            renderers=[glyph],
            tooltips=[("name", "@hover_names"), ("product", "@product")],
        )
    )
    return p_annot



gene_y_range = (-1.5, -1)

def get_arrow_patch(genes_region, ori="+"):
    y_min, y_max = gene_y_range
    y_min = y_min 
    if ori == "+":
        xs = list(
            zip(
                genes_region.start.values,
                genes_region.start.values,
                np.maximum(genes_region.start.values, genes_region.end.values - 100),
                genes_region.end.values,
                np.maximum(genes_region.start.values, genes_region.end.values - 100),
            )
        )
        color = ["orange"] * genes_region.shape[0]
    elif ori == "-":
        xs = list(
            zip(
                genes_region.start.values,
                genes_region.start.values,
                np.minimum(genes_region.start.values, genes_region.end.values + 100),
                genes_region.end.values,
                np.minimum(genes_region.start.values, genes_region.end.values + 100),
            )
        )
        color = ["purple"] * genes_region.shape[0]

    ys = [
        np.array([y_min, y_max, y_max, (y_max + y_min) / 2, y_min])
        for i in range(genes_region.shape[0])
    ]
    genes_mid = genes_region.left + (genes_region.right - genes_region.left) / 2
    pos = list(genes_mid.values)
    names = list(genes_region.gene.values)
    product = list(genes_region["product"].values)
    return dict(
        xs=xs,
        ys=ys,
        pos=pos,
        names=names,
        hover_names=names,
        product=product,
        color=color,
    )

def arrow_patch(genes_region):
    arr_plus = get_arrow_patch(genes_region[genes_region["strand"] == "+"], "+")
    arr_minus = get_arrow_patch(genes_region[genes_region["strand"] == "-"], "-")
    return dict([(k, arr_plus[k] + arr_minus[k]) for k in arr_plus.keys()])


def rect_patch(genes_region):
    y_min, y_max = gene_y_range
    xs = list(
        zip(
            genes_region.start.values,
            genes_region.start.values,
            genes_region.end.values,
            genes_region.end.values,
        )
    )
    xs = [np.array(x) for x in xs]
    ys = [np.array([y_min, y_max, y_max, y_min]) for i in range(genes_region.shape[0])]
    genes_mid = genes_region.left + (genes_region.right - genes_region.left) / 2
    pos = list(genes_mid.values)
    names = list(genes_region.gene.values)
    product = list(genes_region["product"].values)
    color = ["grey"] * genes_region.shape[0]
    return dict(
        xs=xs,
        ys=ys,
        pos=pos,
        names=[""] * genes_region.shape[0],
        hover_names=names,
        product=product,
        color=color,
    )


def get_gene_patches(genes, left, right):
    genes_region = genes[
        (genes["right"] > left)
        & (genes["left"] < right)
        & (genes["type"] != "repeat_region")
    ]
    arr = arrow_patch(genes_region)
    # repeat_region
    rep_region = genes[
        (genes["right"] > left)
        & (genes["left"] < right)
        & (genes["type"] == "repeat_region")
    ]
    rect = rect_patch(rep_region)

    # concatenate patches
    res = dict([(k, arr[k] + rect[k]) for k in arr.keys()])
    return res


Y_RANGE = (-2, 2)
def get_y_range():
    """Accessor that returns the Y range for the genome browser plot

    :return: [description]
    :rtype: [type]
    """
    return Y_RANGE


def get_genome_annotations(genome_path: str):
    annotation = gffpd.read_gff3(genome_path)
    annotation = annotation.attributes_to_columns()
    annotation.loc[:, "left"] = annotation[["start"]].values
    annotation.loc[:, "right"] = annotation[["end"]].values
    return annotation

def get_genes_from_annotation(annotation):

    genes = annotation[
        annotation.type.isin(["CDS", "repeat_region", "ncRNA", "rRNA", "tRNA"])
    ].copy()

    genes.loc[genes["strand"] == "+", "start"] = genes.loc[
        genes["strand"] == "+", "left"
    ].values

    genes.loc[genes["strand"] == "+", "end"] = genes.loc[
        genes["strand"] == "+", "right"
    ].values

    genes.loc[genes["strand"] == "-", "start"] = genes.loc[
        genes["strand"] == "-", "right"
    ].values

    genes.loc[genes["strand"] == "-", "end"] = genes.loc[
        genes["strand"] == "-", "left"
    ].values

    genes.loc[genes["type"] == "repeat_region", "gene"] = "REP"
    return genes