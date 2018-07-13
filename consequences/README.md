# `ConSequences` Codebase
## Overview

| ![ConSequences Code Pipeline](code.png "ConSequences Code Pipeline")  |
|---|
| **Figure**: ConSequences Code Pipeline. Code is represented with rounded corners and data with sharp corners. Code blocks are further split into Docker (blue) and Python (gray).|

ConSequences is primarily a pipeline of Python code used to pre- and post-process data, along with a dispatcher for calling contraction sequence algorithms wrapped in Docker images.
In this README we overview how to install the software, and how to run it with various use cases.

## Installation (General)

This codebase requires Python 3 and Docker.

In general, we recommend wrangling Python dependencies using an environment like `virtualenv`; see below for example instructions for installing on Ubuntu 18.04, and refer to the [virtualenv docs](https://virtualenv.pypa.io/en/stable/) page for more information.
Regardless of whether a virtual environment is used or not, the Python requirements are included in `requirements.txt` and may be installed with `pip install -r requirements.txt`.

For stability, we recommend installing Docker Community Edition (CE) on the stable channel.
Detailed instructions for installing Docker CE can be found in the [docker docs](https://docs.docker.com/install/).

## Installation (Ubuntu 18.04)
_Detailed installation guide for Ubuntu 18.04 LTS coming soon._

## How to run

### Provided algorithms

_Description of provided algorithms coming soon_

### Supported data formats

_Description of provided data formats coming soon_

### Running the command-line interface

_Description of CLI commands coming soon_

### Running a batch experiment

_config file format coming soon_

## Templates for extension

_Python template for adding new input data types coming soon_

_Docker image template for adding new algorithms coming soon_
