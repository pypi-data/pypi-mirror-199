# genomeNotebook

**A genome browser for the jupyter notebook .**

genomeNotebook is a genome browser built on the bokeh plotting library. It can be used to create interactive genome plots that can be easily overlayed and combined with any plots you can build using bokeh.

## Getting Started

### Installation

For the moment, you can install this package only via PyPI

#### PyPI

```console
$ pip install genomenotebook
```

#### Usage

In a Jupyter notebook running with python
```
import genomenotebook as gn
from bokeh.plotting import show

p=gn.browser(genome_path="path_to_fasta_file",
          genome_format="fasta",
          gff_path="path_to_gff_file",
          init_pos=3725353,
          init_win=10000,
         )

show(p)
```

See the example folder for more details.