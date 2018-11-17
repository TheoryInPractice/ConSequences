# Dockerized Treewidth Solvers
To abstract-away dependency issues with running treewidth solvers from various literature, we wrap all solvers in individual Docker containers.
This README is for users interested in running these treewidth solvers outside of the tensor network framework.

# Using our images on Dockerhub
The easiest way to use our existing images is install Docker and run
```
docker run -it --rm -v $PWD:/data tdgoodrich/[solver] ./run.sh [input.gr] [timeout] [output.td]
```
where
* `[solver]` is a supported treewidth solver (currently `freetdi`, `meiji`, and `quickbb`)
* `[input.gr]` is a graph in PACE `.gr` format
* `[timeout]` is a timeout in seconds
* `[output.td]` is where the algorithm will write the tree decomposition in PACE `.td` format

These images are hosted on Dockerhub ('GitHub of Docker') and does not require even downloading the ConSequences repository.

Standard error will be piped to the console, although from our experience this text is not directly useful.
If a solver fails then it will typically produce a `.td` file with only comments.  

# Extending our images
If you would like to rebuild these images with additional functionality or would like to wrap your own treewidth solver in a similar interface, see our Docker images in the `consequences/solver/algorithms` folder.
Each solver has a
* `dockerfile` which specifies how to construct the Docker container,
* a `run.sh` that provides a command-line interface to the solver,
* and a `build.sh` for building the dockerfile into an image.

The interface to our solvers can be changed by modifying `run.sh` then rebuilding with `build.sh`, for example.
Users with questions or concerns about these Docker images are encouraged to create a GitHub issue to initiate a dialog.
