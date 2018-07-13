#!/usr/bin/env python3

import pandas as pd
import seaborn as sns
import sys
import matplotlib.pyplot as plt
import numpy as np
from macros import colors


def algorithm_font(algorithm):
    return r'\textsf{{{}}}'.format(algorithm)


def combined(algorithm, regularity):
    return '{}-{}'.format(algorithm, regularity)


def plot_tw_vs_simtime(data_filename, plot_filename, verbose):

    # Use latex font
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    # Set up Seaborn style
    sns.set(style="darkgrid")

    # Import the dataframe
    dataframe = pd.read_csv(data_filename)
    dataframe = dataframe.sort_values(by=['algorithm'])

    # Keep the data we want for the large facet
    dataframe = dataframe.dropna(subset=['tree-decomp-width'])
    dataframe = dataframe.loc[(dataframe['algorithm'] != 'quickbb')]
    dataframe = dataframe.loc[dataframe['vertices'].isin([10, 14, 18,
                                                          22, 26, 30])]

    dataframe['tree-decomp-width'] =\
        pd.to_numeric(dataframe['tree-decomp-width'], downcast='integer')
    dataframe['algorithm'] =\
        np.vectorize(algorithm_font)(dataframe['algorithm'])
    # If we want to have a different color for algorithm + regularity
    # dataframe['combined'] =\
    #     np.vectorize(combined)(dataframe['algorithm'], dataframe['regularity'])

    plot = sns.stripplot(x="tree-decomp-width",
                         y="simulation-time",
                         hue="algorithm",
                         data=dataframe,
                         dodge=True,
                         size=4,
                         jitter=True,
                         alpha=0.7,
                         linewidth=0.1,
                         palette=[colors[x] for x in ['freetdi', 'meiji']],
                         hue_order=['\\textsf{freetdi}', '\\textsf{meiji-e}'])
    for i in range(len(dataframe["tree-decomp-width"].unique()) - 1):
        plot.axvline(x=i+.5, c="white", dashes=(2, 1))

    plot.set(ylim=(.01, 10000), yscale="log")

    plot.set(xlabel="Contraction Complexity",
             ylabel="Simulation Time (sec)")

    # Add legend
    plot.legend(loc="upper right")

    # Save figure
    for extension in ['.pdf', '.png']:
        plt.savefig(plot_filename + extension)


if __name__ == '__main__':
    data_filename = sys.argv[1]
    plot_filename = sys.argv[2]
    plot_tw_vs_simtime(data_filename, plot_filename, False)
