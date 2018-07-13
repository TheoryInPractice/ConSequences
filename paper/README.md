# Paper Supplement

In this README we detail how to replicate experiments found in "Benchmarking treewidth as a practical component of tensor-network--based quantum simulation" ([arXiv link](https://arxiv.org/abs/1807.04599])).
We provide two levels of granularity: First, given the results we computed, we provide scripts to regenerate the plots.
Second, we provide convenience scripts for recomputing entire experiments.
(Note that these run times may be on the order of weeks, depending on hardware specs.)

## Recomputing plots
_Before recomputing plots, make sure Python 3 has been installed per this repository's [ConSequences README](../consequences/README.md)._

Data computed on our hardware is provided in the `data` subfolder, and split per experiment into `provided_mera.csv` and `provided_qtorch.csv`.
This data was computed on workstations with a single Xeon
E5-2623 v3 processor (8 threads with a 3.0GHz base clock and 10MB cache) and 64GB system memory

To make all figures, run `make provided_figures`.
To reproduce individual plots based on our data, run `make provided_[figure/table]`. For example, `make provided_figure3` will regenerate Figure 3.

## Recomputing experiments

_Convenience scripts coming soon_
