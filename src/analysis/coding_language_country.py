"""
Author:     Chen Bihan
Data:       2023/9/26
Course:     NUS IT5006 Fundamentals of Data Analytics
Project:    Job Role Recommendation App
Function:   Functions for Analysis of coding language trend
"""


from matplotlib import pyplot as plt
import numpy as np
import streamlit as st
import pandas as pd
import os


def plot_language_trend(st_col, country):
    """
    Plot the trend of programming languages used in a specific country across 2020-2022.

    Parameters:
    - country: String specifying the country to be analyzed

    Returns:
    - A bar chart showing the trend of programming languages for the specified country
    """
    # Get the absolute path of the current script
    current_path = os.path.abspath(__file__)
    # Get the root directory of the project
    project_root_path = os.path.dirname(os.path.dirname(os.path.dirname(current_path)))
    loc = os.path.join(project_root_path, "data", "analyzed")
    final_data_path = os.path.join(loc, "coding_language_country.csv")
    final_data = pd.read_csv(final_data_path)

    # Updated list of top languages based on column names in the dataset
    top_languages = ['Q12_coding language_Python', 'Q12_coding language_R', 'Q12_coding language_SQL',
                     'Q12_coding language_C', 'Q12_coding language_C++', 'Q12_coding language_Java',
                     'Q12_coding language_Javascript', 'Q12_coding language_Bash',
                     'Q12_coding language_MATLAB', 'Q12_coding language_Julia']

    # Filter data for the specified country
    country_data = final_data[final_data['Q4_country'] == country]

    # Convert the year column to integer type
    country_data['year'] = country_data['year'].astype(int)
    # to find columns which represent programming languages
    q12_columns = [col for col in final_data.columns if col.startswith('Q12_coding')]

    # Convert the language columns to binary format
    for col in q12_columns:
        country_data.loc[:, col] = country_data[col].apply(lambda x: 1 if pd.notnull(x) else 0)
    # Group by year and sum the values for each programming language
    country_language_usage = country_data.groupby('year')[q12_columns].sum()

    # Convert the counts to percentages
    total_respondents = country_data.groupby('year').size()
    country_language_usage_percentage = country_language_usage.divide(total_respondents, axis=0) * 100

    # Subset the data based on the updated top languages
    country_language_usage_percentage = country_language_usage_percentage[top_languages]

    # Custom colors
    colors = ['#aec7e8','#1f77b4','#08306b']

    # Plotting
    plt.figure(figsize=(15, 9))
    bar_width = 0.3
    years = [int(year) for year in sorted(final_data['year'].unique())]  # Ensure years are of integer type
    for index, year in enumerate(years):
        plt.bar(
            np.arange(len(top_languages)) + index * bar_width,
            country_language_usage_percentage.loc[year],
            width=bar_width,
            label=str(year),
            color=colors[index]
        )

    plt.title(f"Trend of Top 10 Programming Languages Used in {country} (2020-2022)", fontsize=16)
    plt.xlabel("Programming Language", fontsize=14)
    plt.ylabel("Percentage of Users (%)", fontsize=14)
    plt.xticks(np.arange(len(top_languages)) + bar_width, [lang.split("_")[-1] for lang in top_languages], rotation=45)
    plt.legend()
    plt.tight_layout()
    st_col.pyplot(plt.gcf())


# Test the final  function with updated top languages for USA
# plot_language_trend("United States of America")







