# DAB

  The DAB (Dockerized Algorithm Batch processor) project currently is a set of shell scripts used in conjunction with a
set of docker containers containing entries to the [PACE challenge](https://pacechallenge.wordpress.com/). On a high
level, a call to the `dab.sh` script will search the docker path for PACE
challenge containers and execute a set of graph instances on each of the
containers.

# Installation and Basic Usage

1. Install Docker. Instructions can be found [here](https://docs.docker.com/engine/installation/).

2. Start the Docker daemon. Instructions can be found
   [here](https://docs.docker.com/engine/admin/#start-the-daemon-using-operating-system-utilities).

  * To ensure the Docker daemon is running, in a terminal run `docker images`.
    If the daemon is running, the output should look like
    ```
    REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
    ```
    If the output looks like
    ```
    Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
    ```
    , check that you are properly starting the Docker daemon.


3. Build Images. The DAB repository includes a small set of dockerized
   algorithms to get you started, but they need to be built first. To make this
   as painless as possible, a `build.sh` script has been included for each
   algorithm. You can read more about creating dockerfiles and building images
   [here](https://docs.docker.com/engine/reference/commandline/build/#parent-command). There are
   currently just 2 algorithms that come included with DAB, Meiji and QuickBB.
   To build these, simply navigate to their respective directories and run
   `./build.sh`. You may need to give the script executable permissions, which
   can be done by running `chmod +x build.sh`. Once you've built both images,
   we can check if we did everything properly by running `docker images -f
   "label=pace"`. You should see something like
   ```
   REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
   meiji               0.1                 5e8cac00c144        6 days ago          9.05MB
   quickbb             0.1                 6d14845e876f        6 days ago          94.3MB
   ```
   The important part is that you have two images, one in the `meiji`
   , the other in the `quickbb` repository.

4. Now let's make sure we've installed everything correctly by running the
   algorithms on a small test set of graphs, conveniently located in the
   `/test` directory. The `dab.sh` script currently includes 3 flags. The only
   required flag is `-s [source directory]`, which points to a source directory
   containing the graph files to run on. The other two are `-t [timeout]` for a
   timeout in seconds, and `-e [extension]` to look for graph files using a file
   extension other than the default `.gr`.








