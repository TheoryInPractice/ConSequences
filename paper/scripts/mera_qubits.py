import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sys
import numpy as np
import warnings
from macros import colors, markers


def operators(dim, operator_location):
    # Given 1, 2, or 4 coordinates like x-y-z-w, depending on dim and operators
    num_operators = len(operator_location.split('-')) / dim
    if num_operators == 1:
        return 'One Operator'
    elif num_operators == 2:
        return 'Two Operators'


def qubits(kary, level):
    return kary**(level)


def fabric(dim, kary):
    return '{}D {}:1'.format(dim, kary)


def algorithm_font(algorithm):
    return r'\textsf{{{}}}'.format(algorithm)


def subject(dim, kary, level, operator_position):
    return '{}-{}-{}-{}'.format(dim, kary, level, operator_position)


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
    dataframe['Qubits Available'] =\
        np.vectorize(qubits)(dataframe['kary'], dataframe['level'])
    dataframe['subject'] =\
        np.vectorize(subject)(dataframe['dim'],
                              dataframe['kary'],
                              dataframe['level'],
                              dataframe['operator_position'])

    dataframe = dataframe.rename(
        columns={'time': 'Run Time (sec)',
                 'treewidth': 'Contraction Complexity'})
    if verbose:
        print(dataframe)

    # Compute the plot
    facet_kws = dict()
    warnings.simplefilter(action='ignore', category=FutureWarning)
    plot = sns.factorplot(data=dataframe,
                          col='operators',
                          row='fabric',
                          x="Qubits Available",
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


    # # Make facet grid of scatter plots
    # grid = sns.FacetGrid(dataframe,
    #                      col="operators",
    #                      row="fabric",
    #                      hue="algorithm",
    #                      palette=[colors[x] for x in ['freetdi', 'meiji', 'netcon']],
    #                      margin_titles=True,
    #                      hue_order=['\\textsf{freetdi}',
    #                                 '\\textsf{meiji-e}',
    #                                 '\\textsf{netcon}'])
    # plot = grid.map_dataframe(plt.scatter,
    #                           'Qubits Available',
    #                           'Run Time (sec)',
    #                           linewidth=0.1)

    # Make facet grid of timeseries plots
    # print(dataframe)
    # grid = sns.FacetGrid(dataframe,
    #                      col="operators",
    #                      row="fabric",
    #                      margin_titles=True)
    # warnings.simplefilter(action='ignore', category=UserWarning)
    # plot = grid.map_dataframe(sns.tsplot,
    #                           time='Qubits Available',
    #                           value='Run Time (sec)',
    #                           condition='algorithm',
    #                           unit='operator_position',
    #                           color='deep')

    # Manually add dashed lines to facets
    for axis in plot.fig.get_axes():
        axis.axhline(y=1200, color='black', dashes=[3, 3])
        for i in range(len(dataframe["Qubits Available"]) - 1):
            axis.axvline(x=i+.5, c="white", dashes=(2, 1))

    # Set axis lengths and format
    plot.set(ylim=(.001, 10000), yscale='log')

    #xticks=range(0, 31, 5)

    # Set axis labels
    plot.set_titles(col_template="{col_name}", row_template="{row_name} MERA")

    # Add legend
    plot.fig.get_axes()[3].legend(loc="lower right")

    # Save figure
    for extension in ['.pdf', '.png']:
        plot.savefig(plot_filename + extension)


if __name__ == '__main__':
    data_filename = sys.argv[1]
    plot_filename = sys.argv[2]
    plot_mera_treewidth_comparison(data_filename, plot_filename, False)
