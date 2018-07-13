import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sys
import warnings
import numpy as np
from macros import colors, markers


def operators(dim, operator_location):
    # Given 1, 2, or 4 coordinates like x-y-z-w, depending on dim and operators
    num_operators = len(operator_location.split('-')) / dim
    if num_operators == 1:
        return 'One Operator'
    elif num_operators == 2:
        return 'Two Operators'


def fabric(dim, kary):
    return '{}D {}:1'.format(dim, kary)


def algorithm_font(algorithm):
    return r'\textsf{{{}}}'.format(algorithm)


def plot_mera_treewidth_comparison(data_filename, plot_filename, verbose):
    # Use latex font
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    # Set up Seaborn style
    sns.set(style="darkgrid")

    # Import the dataframe
    dataframe = pd.read_csv(data_filename)
    dataframe['operators'] =\
        np.vectorize(operators)(dataframe['dim'],
                                dataframe['operator_position'])
    dataframe['fabric'] =\
        np.vectorize(fabric)(dataframe['dim'], dataframe['kary'])
    dataframe['algorithm'] =\
        np.vectorize(algorithm_font)(dataframe['algorithm'])

    dataframe = dataframe.rename(
        columns={'time': 'Run Time (sec)',
                 'treewidth': 'Contraction Complexity'})
    if verbose:
        print(dataframe)

    # # Make facet grid of scatter plots
    # grid = sns.FacetGrid(dataframe,
    #                      col="operators",
    #                      row="fabric",
    #                      hue="algorithm",
    #                      palette=[colors[x] for x in ['freetdi', 'meiji', 'netcon']],
    #                      hue_kws=dict(marker=[markers[x] for x in ['freetdi', 'meiji', 'netcon']]),
    #                      margin_titles=True,
    #                      hue_order=['\\textsf{freetdi}',
    #                                 '\\textsf{meiji-e}',
    #                                 '\\textsf{netcon}'])
    # plot = grid.map(plt.scatter,
    #                 "Contraction Complexity",
    #                 "Run Time (sec)",
    #                 alpha=0.7,
    #                 linewidth=0.1,
    #                 edgecolor='black')


    facet_kws = dict()
    warnings.simplefilter(action='ignore', category=FutureWarning)
    plot = sns.factorplot(data=dataframe,
                          col='operators',
                          row='fabric',
                          x="Contraction Complexity",
                          y="Run Time (sec)",
                          hue="algorithm",
                          palette=[colors[x] for x in ['freetdi',
                                                       'meiji',
                                                       'netcon']],
                          facet_kws=facet_kws,
                          kind="strip",
                          dodge=True,
                          jitter=True,
                          alpha=0.7,
                          linewidth=0.1,
                          aspect=1.7,
                          size=2.5,
                          hue_order=['\\textsf{freetdi}',
                                     '\\textsf{meiji-e}',
                                     '\\textsf{netcon}'],
                          legend=False)



    # Manually add dashed lines to facets
    for axis in plot.fig.get_axes():
        axis.axhline(y=1200, color='black', dashes=[3, 3])
        for i in range(len(dataframe["Contraction Complexity"]) - 1):
            axis.axvline(x=i+.5, c="white", dashes=(2, 1))

    # Set axis lengths and format
    plot.set(ylim=(.001, 10000), yscale='log')

    # Set axis labels
    plot.set_titles(col_template="{col_name}", row_template="{row_name} MERA")

    # Add legend
    plot.fig.get_axes()[0].legend(loc="lower right")

    # Save figure
    for extension in ['.pdf', '.png']:
        plot.savefig(plot_filename + extension)


if __name__ == '__main__':
    data_filename = sys.argv[1]
    plot_filename = sys.argv[2]
    plot_mera_treewidth_comparison(data_filename, plot_filename, False)
