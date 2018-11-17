# `ConSequences`: A code framework for contraction sequence algorithms

This repository hosts an (BSD 3-clause) open source framework for running contraction sequence algorithms for tensor network simulations.
These algorithms come from two primary sources: The tensor network literature and the structural graph theory and algorithms literature.
In this framework we provide pre- and post-processing routines for wrangling data, an algorithm dispatcher for easily running batch experiments, a command-line interface for computing a contraction sequence on a given network with a given algorithm, and a containerized method for running individual algorithms.

For notes on running our Dockerized treewidth solvers, see [TREEWIDTH.md](TREEWIDTH.md).

For detailed notes on installing and using `ConSequences`, see the [README](consequences/README.md) in the `consequences` subfolder.

For the experimental supplement to **"Benchmarking treewidth as a practical component of tensor-network--based simulation"**, see the [README](paper/README.md) in the `paper` subfolder.

## Citing this repository

_A Zenodo DOI will be provided once all code is finalized. In the mean time, please cite the corresponding paper on arXiv:_

```
@article{dumitrescu2018benchmarking,
      author         = "Dumitrescu, Eugene F. and Fisher, Allison L. and
                        Goodrich, Timothy D. and Humble, Travis S. and Sullivan,
                        Blair D. and Wright, Andrew L.",
      title          = "{Benchmarking treewidth as a practical component of
                        tensor-network--based quantum simulation}",
      year           = "2018",
      eprint         = "1807.04599",
      archivePrefix  = "arXiv",
      primaryClass   = "cs.DS",
      SLACcitation   = "%%CITATION = ARXIV:1807.04599;%%"
}
```

## Contact information

Having problems installing or running code? Want to discuss codebase extensions or additional use cases? Contact us by creating a GitHub issue or by emailing Timothy at <tdgoodri@ncsu.edu>.
