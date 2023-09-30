import pandas as pd

def framework(data):

    # filter the data for the columns needed
    filter_col = [col for col in data if col.startswith('Q17')]
    filter_col.append('year')
    data= data[filter_col]

    # find the column names that start with 'Q17'
    q17_columns = [col for col in data.columns if col.startswith('Q17')]

    # Rename columns based on the portion after the last '_'
    for col in q17_columns:
        new_name = col.rsplit('_', 1)[-1]
        data.rename(columns={col: new_name}, inplace=True)

    # gouping by year and count the number of each framework, sort by counts
    data = data.groupby('year').count().transpose().reset_index().rename(columns={'index': 'Framework', 2020:'2020', 2021:'2021', 2022:'2022'}).sort_values(by='2022', ascending=False)

    # create a summary of the major frameworks and combine others
    summary = data.iloc[:6]
    summary.loc['Others'] = data[6:].sum()

    # rename the last row as Others
    summary['Framework'].iloc[-1] = 'Others'

    # return the summary
    return summary


