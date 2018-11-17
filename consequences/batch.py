"""
This file deconstructs a configuration file and sends its arguments to the
proper functions to execute the entire pipeline.
"""

import sys
import subprocess
import os
import argparse


def call_functions(output_dir, num_threads, algo_seed, timeout, verbose,
                   docker_verbose, algorithms, csv_filename):
    """
    Constructs a string to make a subprocess call to generate the datasets,
    compute tree decompositions and create a csv of results.

    Keyword arguments:
    output_dir -- desired output directory of related files
    num_threads -- number of threads to run on
    algo_seed -- random seed for a PACE algorithm
    timeout -- maximum time for each algorithm in seconds
    verbose -- option to print more pipeline info to console
    docker_verbose -- option to print more docker info to console
    algorithms -- list of algorithms to compute
    csv_filename -- desired filename of .csv file
    """

    # generate graphs
    callString = "python dataset-generator.py {}".format(args.config_filename)
    subprocess.call(callString, shell=True)

    # construct compute_td call
    input_string = " -i {}".format(output_dir)
    num_threads_string = " -n {}".format(num_threads)
    if num_threads == "default":
        num_threads_string = ""
    seed_string = " -s {}".format(algo_seed)
    if algo_seed == "default":
        seed_string = ""
    timeout_string = " -t {}".format(timeout)
    if timeout == "default":
        timeout_string = ""
    output_string = " -o {}".format(output_dir)
    verbose_string = " -v"
    if verbose == "false":
        verbose_string = ""
    docker_verbose_string = " --docker_verbose"
    if docker_verbose == "false":
        docker_verbose_string = ""
    algorithms_string = " -a " + ' '.join(algorithms)
    if(csv_filename == 'default'):
        base = os.path.basename(args.config_filename)
        csv_filename = ("{}/{}".format(output_dir,
                        base.replace(".cfg", ".csv")))

    # call compute_td
    td_call = "python compute_td.py"
    call_td = "{}{}{}{}{}{}{}{}{}".format(td_call, input_string,
                                          num_threads_string, seed_string,
                                          timeout_string, output_string,
                                          verbose_string,
                                          docker_verbose_string,
                                          algorithms_string)

    call_csv = "python generate_csv.py {} {}".format(output_dir, csv_filename)
    subprocess.call(call_td, shell=True)
    subprocess.call(call_csv, shell=True)


def construct_argparser():
    """
    Controls the retrieval of command line arguments using the argparse module.
    """

    parser = argparse.ArgumentParser(description="Master script")
    parser.add_argument("config_filename", type=str,
                        help="input filename for config file")
    return parser


def parse_config():
    """
    Checks the config file for the correct format and directs params to main
    """

    checklist = ["n", "r", "graph_seeds", "output_dir", "num_threads",
                 "algo_seed", "timeout", "verbose", "docker_verbose",
                 "algorithms", "csv_filename"]
    expected = len(checklist)
    with open(args.config_filename, 'r') as infile:
        for count, line in enumerate(infile.readlines()):

            try:
                header, body = line.split(":")
                # if header == "n":
                if header in checklist:
                        checklist.remove(header)

                if header == "output_dir":
                    output_dir = body.strip()
                elif header == "num_threads":
                    num_threads = body.strip()
                elif header == "algo_seed":
                    algo_seed = body.strip()
                elif header == "timeout":
                    timeout = body.strip()
                elif header == "verbose":
                    verbose = body.strip()
                elif header == "docker_verbose":
                    docker_verbose = body.strip()
                elif header == "algorithms":
                    algorithms = body.split()
                elif header == "csv_filename":
                    csv_filename = body.strip()
            except ValueError:
                print ("Invalid configuration format: parsing error.  "
                       "Exiting Program.")
                sys.exit()

    if (len(checklist) is not 0):
        print ("Invalid configuration format: not all fields present.")
        print ("Exiting program.")
        sys.exit()
    elif (count + 1 is not expected):
        print ("Invalid configuration format: extra fields present.")
        print ("Exiting program.")
        sys.exit()

    return (output_dir, num_threads, algo_seed, timeout, verbose,
            docker_verbose, algorithms, csv_filename)


if __name__ == "__main__":
    """
    Main CLI for converting a .peo file to a PACE tree decomposition (.td).
    """

    args = construct_argparser().parse_args()
    (output_dir, num_threads, algo_seed, timeout, verbose, docker_verbose,
     algorithms, csv_filename) = parse_config()

    from pathlib import Path
    home = str(Path.home())
    if('~/' in output_dir):
        output_dir = output_dir.replace('~/', "{}/".format(home))

    import pathlib
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    call_functions(output_dir, num_threads, algo_seed, timeout, verbose,
                   docker_verbose, algorithms, csv_filename)

    print ("Experiment complete")
