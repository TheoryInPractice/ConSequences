# Paper Supplement

The publication "Benchmarking treewidth as a practical component of tensor network simulations" (To appear in PLOS ONE, [arXiv link](https://arxiv.org/abs/1807.04599)) contains experiments generated with ConSequences.
In this README we detail the data, how it was generated, and how to reuse our plotting routines.

# Data
Data computed on our hardware is provided in the `data` subfolder, and generated on workstations with a single Xeon
E5-2623 v3 processor (8 threads with a 3.0GHz base clock and 10MB cache) and 64GB system memory.

The data used in the MERA experiment is provided in `paper/data/mera.csv`. The headers of this CSV are as follows:
* `dim`: The dimension of the MERA
* `kary`: The k used for the k-ary isometries
* `level`: The number of levels (plys) from the top of the MERA to the operators
* `vertices`: The number of vertices in the tensor network (after computing causal cone)
* `edges`: The number of edges in the tensor network (after computing causal cone)
* `operator_position`: Two operators are place, one at 0 (0-0) and one at `operator_position` for 1D (2D), respectively
* `algorithm`: The algorithm used to compute the contraction sequence
* `treewidth`: The treewidth (or contraction complexity) computed by the `algorithm` on this MERA network
* `time`: The run time to optimal treewidth

The data used in the QAOA experiment is provided in `paper/data/qtorch.csv`. The headers of this CSV are as follows:
* `regularity`: The regularity of the graph generated to cut with MaxCut using a QAOA circuit
* `vertices`: The number of vertices in the regular graph
* `seed`: The seed used to generate this graph in NetworkX with our data generator
* `tree-decomp-width`: The width of the tree decomposition found (not necessarily optimal)
* `algorithm`: The algorithm used to compute the tree decomposition / contraction sequence
* `tree-decomp-time`: Run time to find the contraction sequence
* `simulation-time`: Run time to finish the simulation with the used contraction sequence

## Recomputing plots
_Before recomputing plots, make sure Python 3 has been installed per this repository's [ConSequences README](../consequences/README.md)._

To make all figures, run `make figures`.
To reproduce individual plots based on our data, run `make [figure/table]`. For example, `make figure3` will regenerate Figure 3.
These plots are saved to the `plots` subfolder.
