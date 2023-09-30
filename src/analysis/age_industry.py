"""
Author:     Chen Bihan
Data:       2023/9/26
Course:     NUS IT5006 Fundamentals of Data Analytics
Project:    Job Role Recommendation App
Function:   Functions for Analysis of age vs industry
"""

import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd
import os

# Get the absolute path of the current script
current_path = os.path.abspath(__file__)
# Get the root directory of the project
project_root_path = os.path.dirname(os.path.dirname(os.path.dirname(current_path)))
loc = os.path.join(project_root_path, "data", "processed")
final_data_path = os.path.join(loc, "Data_Preprocess_v3.csv")
final_data = pd.read_csv(final_data_path)

def plot_industry_distribution(age_range, years):
    """
    Use Seaborn to plot a histogram of the distribution of different industries based on a given age group and year.

    Parameters:
    - age_range: selected Age Range like: '30-34'
    - years: selected years like: [2021], [2022] or [2021, 2022](no data on 2020)
    Returns:
    the bar chart of the Industry Distribution for selected Age Range and selected years
    """

    # to filter the data according to age range and years
    filtered_data = final_data[(final_data['Q2_age'] == age_range) & (final_data['year'].isin(years))]

    # to get the industry distribution
    industry_counts = filtered_data['Q24_industry'].value_counts()

    if industry_counts.empty:
        print(f"No industry data available for age range {age_range} in years {years}.")
        return

    # to plot bar chart
    plt.figure(figsize=(12, 8))
    sns.barplot(x=industry_counts.index, y=industry_counts.values, color="#273c75")
    plt.title(f'Industry Distribution for Age Range {age_range} in Years {years}')
    plt.xlabel('Industry')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# to use this function
plot_industry_distribution('30-34', [2021])



