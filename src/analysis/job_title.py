import pandas as pd

def title(data):

    # find the number of students in 2022
    filter_col = [col for col in data if col.startswith('Q5')]
    no_of_stu = data[filter_col].value_counts().iloc[1]
    no_of_stu

    # filter the data for job titles and years
    data = data[["year", "Q23_role title"]]

    # synchronize the job titles of the same role
    by_year = data.groupby(['year', 'Q23_role title']).size().reset_index(name='count')
    by_year.rename({"Q23_role title": "Title"}, axis=1, inplace=True)
    mask = by_year['Title'].str.startswith('Data Analyst')
    by_year.loc[mask, 'Title'] = 'Data Analyst'
    mask = by_year['Title'].str.startswith('Machine Learning')
    by_year.loc[mask, 'Title'] = 'Machine Learning Engineer'

    # create a pivot table with job titles as rows and years as columns
    pivot_df = by_year.pivot(index='Title', columns='year', values='count')

    # assign the total number of students in 2022 due to the different format of the 2022 survey
    pivot_df[2022].loc['Student'] = no_of_stu
    pivot_df.sort_values(by=2022, ascending=False, inplace=True)

    # for top 5 titles, change the column names to strings and values to integers
    top_5 = pivot_df.iloc[:5].rename({2020:'2020', 2021:'2021', 2022: '2022'}, axis=1).reset_index()
    top_5 = top_5.astype(int, errors='ignore')
    return top_5
