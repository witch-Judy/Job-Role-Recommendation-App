"""
Author:     Chen Bihan
Data:       2023/9/26
Course:     NUS IT5006 Fundamentals of Data Analytics
Project:    Job Role Recommendation App
Function:   Functions for Analysis of coding experience vs compensation
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import streamlit as st

# Get the absolute path of the current script
current_path = os.path.abspath(__file__)
# Get the root directory of the project
project_root_path = os.path.dirname(os.path.dirname(os.path.dirname(current_path)))
loc = os.path.join(project_root_path, "data", "analyzed")
final_data_path = os.path.join(loc, "experience_vs_salary.csv")
final_data = pd.read_csv(final_data_path)

# Functions for plotting experience vs compensation

def compute_salary_midpoint(salary_range):
    """
    Compute the midpoint of the salary range for plotting purposes.
    Updated to handle non-string values.

    Parameters:
    - salary_range: String representing the salary range or NaN

    Returns:
    - Midpoint of the salary range as a float, or None for non-string values
    """
    # Check if the salary_range is a string
    if not isinstance(salary_range, str):
        return None

    # Remove any non-numeric characters
    numbers = [int(s.replace(',', '').replace('>', '').replace('<', '').replace('$', '').strip())
               for s in salary_range.split('-')]

    # Compute the midpoint
    if len(numbers) == 2:
        return sum(numbers) / 2
    elif len(numbers) == 1:
        return numbers[0]
    else:
        return None


def plot_experience_vs_compensation(years):
    """
    Updated function to use the new compute_salary_midpoint_v2 function.
    """
    # Filter data based on the specified years and exclude students
    filtered_data = final_data[(final_data['year'].astype(int).isin(years)) & (final_data['Q5_student or not'] != 'Student')]

    # Convert the salary range to its midpoint
    filtered_data['Q29_midpoint'] = filtered_data['Q29_yearly compensation'].apply(compute_salary_midpoint)

    # Setting the order of the experience categories
    experience_order = [
        'I have never written code', '< 1 years', '1-2 years', '3-5 years',
        '5-10 years', '10-20 years', '20+ years'
    ]

    plt.figure(figsize=(15, 9))
    sns.boxplot(
        x='Q11_coding years', y='Q29_midpoint',
        data=filtered_data, order=experience_order,palette="Blues"
    )
    plt.title(f"Relationship Between Coding Experience and Yearly Compensation Midpoint ({', '.join(map(str, years))})",
              fontsize=16)
    plt.xlabel("Coding Experience", fontsize=14)
    plt.ylabel("Yearly Compensation Midpoint", fontsize=14)
    plt.ylim(0, 250000)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt.gcf())


# # For demonstration, plot the relationship for the year 2020
# plot_experience_vs_compensation([2020])
# plot_experience_vs_compensation([2020, 2021])
# plot_experience_vs_compensation([2020, 2021, 2022])