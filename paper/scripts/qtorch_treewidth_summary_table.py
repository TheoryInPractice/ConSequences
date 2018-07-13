#!/bin/python

import pandas
import sys


def latex_table(data_filename, table_filename):
    # Read in the dataset
    dataframe = pandas.read_csv(data_filename)

    # Keep the data we want
    dataframe = dataframe.loc[(dataframe['algorithm'] != 'quickbb') &
                              (dataframe['algorithm'] != 'liquid')]
    dataframe = dataframe.loc[dataframe['vertices'].isin([10, 14, 18,
                                                          22, 26, 30])]
    # First 25 seeds
    dataframe = dataframe.loc[dataframe['seed'].isin(range(0, 25))]

    print(dataframe)

    with open('foo.csv', 'w') as outfile:
        outfile.write(dataframe.to_csv(index=False))

    # Describe our dataframe
    describe = dataframe.groupby(
        ['regularity', 'vertices']).describe().round(decimals=1)
    describe = describe['tree-decomp-width']

    # Drop thje 25% and 75% levels
    describe = describe.drop(columns=['25%', '75%'])

    describe = describe.loc[(describe['count'] != 0)]

    # Make min, 50%, max, and count ints
    int_headers = ['min', '50%', 'max', 'count']
    describe[int_headers] = describe[int_headers].astype('int')

    with open(table_filename, 'w') as outfile:
        outfile.write(describe.to_latex())


if __name__ == '__main__':
    data_filename = sys.argv[1]
    table_filename = sys.argv[2]
    latex_table(data_filename, table_filename)
