#!/usr/bin/env python3

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import sys
import warnings
import math
from macros import colors


def algorithm_font(algorithm):
    if algorithm == 'liquid':
        return r'\textsf{LIQUID}'
    else:
        return r'\textsf{{qTorch-{}}}'.format(algorithm)


def runtime(treewidth_time, simulation_time):
    if math.isnan(treewidth_time):
        return simulation_time
    else:
        return treewidth_time + simulation_time


def plot_liquid_comparison(data_filename, plot_filename, verbose):
        # Use latex font
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')

        # sns.set_context("paper", rc={"font.size": 80,
        #                              "axes.titlesize": 80,
        #                              "axes.labelsize": 50})

        # Set up Seaborn style
        sns.set(style="darkgrid")

        # Import the dataframe
        dataframe = pd.read_csv(data_filename, header=0)

        # Keep the data we want
        dataframe = dataframe.loc[(dataframe['algorithm'] != 'quickbb')]
        dataframe = dataframe.loc[dataframe['vertices'].isin([10, 14, 18,
                                                              22, 26, 30])]

        dataframe['algorithm'] =\
            np.vectorize(algorithm_font)(dataframe['algorithm'])
        dataframe['runtime'] =\
            np.vectorize(runtime)(dataframe['tree-decomp-time'],
                                  dataframe['simulation-time'])
        if verbose:
            print(dataframe)

        # Compute the plot
        facet_kws = dict()
        warnings.simplefilter(action='ignore', category=FutureWarning)
        plot = sns.factorplot(data=dataframe,
                              row="regularity",
                              x="vertices",
                              y="runtime",
                              hue="algorithm",
                              palette=[colors[x] for x in ['freetdi', 'meiji', 'liquid']],
                              facet_kws=facet_kws,
                              kind="strip",
                              dodge=True,
                              jitter=True,
                              alpha=0.7,
                              linewidth=0.1,
                              aspect=1.7,
                              size=2.5,
                              hue_order=['\\textsf{qTorch-freetdi}',
                                         '\\textsf{qTorch-meiji-e}',
                                         '\\textsf{LIQUID}'],
                              legend=False)

        # Manually add dashed lines to facets
        for axis in plot.fig.get_axes():
            for i in range(len(dataframe["vertices"]) - 1):
                axis.axvline(x=i+.5, c="white", dashes=(2, 1))
                axis.axhline(y=600, c='black', dashes=(3, 3))

        # Set axis lengths and format
        plot.set(ylim=(.01, 1000000), yscale='log')

        # Set axis labels
        plot.fig.get_axes()[-1].set(xlabel="Vertices")
        for axis in plot.fig.get_axes():
            axis.set(ylabel="Total Simulation Time (sec)")

        # Set axis labels
        plot.set_titles(row_template="{row_name}-Regular")

        # Add legend
        plot.fig.get_axes()[0].legend(loc="upper left")

        # Save figure
        for extension in ['.pdf', '.png']:
            plot.savefig(plot_filename + extension)


if __name__ == '__main__':
    data_filename = sys.argv[1]
    plot_filename = sys.argv[2]
    plot_liquid_comparison(data_filename, plot_filename, False)
