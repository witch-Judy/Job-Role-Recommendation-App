"""
Author:     Chen Bihan
Data:       2023/9/26
Course:     NUS IT5006 Fundamentals of Data Analytics
Project:    Job Role Recommendation App
Function:   Functions for app
"""

import pandas as pd
import streamlit as st
import sys
import os

current_path = os.path.abspath(__file__)
parent_path = os.path.dirname(current_path)
project_root_path = os.path.dirname(parent_path)
sys.path.append(project_root_path)
dataV3_path = os.path.join(project_root_path, "data/processed/Data_Preprocess_v3.csv")
final_data = pd.read_csv(dataV3_path)


from src.analysis.coding_language_country import plot_language_trend
from src.analysis.age_industry import plot_industry_distribution


# to delete the warning message of the front page
st.set_option('deprecation.showPyplotGlobalUse', False)

# Sidebar title
st.sidebar.title("Job Role Recommendation")

# Main categories: Data Analysis and Recommendation
main_selection = st.sidebar.selectbox("Choose a category", ["Data Analysis", "Recommendation system"])

# If Data Analysis is selected
if main_selection == "Data Analysis":
    st.write("## Data Analysis")

    # Sub-categories for Data Analysis: x class and y class
    analysis_selection = st.sidebar.selectbox("Choose a class", ["<x>：Trend over time", "<y>：Statistical tendencies"])

    # If x class is selected under Data Analysis
    if analysis_selection == "<x>：Trend over time":
        st.write("### <x> Trend over time")

        # Add sub-titles for x class
        x_sub_title = st.sidebar.selectbox("Choose a sub-title for x class", ["country_income", "Machine learning framework", "coding_language"])
        st.write(f"You chose {x_sub_title} under {analysis_selection}")

        # If 'coding_language' is selected, add a country selector and display the plot based on the selected country
        if x_sub_title == "coding_language":
            st.write("you have to choose a country and then we will give you a barchart form 2020 to 2022")
            # Add a country selector
            country = st.sidebar.selectbox("Choose a country", ["United States of America", "Japan", "India", "China", "Germany", "France", "Brazil", "Russia", "United Kingdom", "Indonesia"])
            # Display the plot based on the selected country

            plot_language_trend(final_data, country)

            #TODO
            # this place is for Young Ho to place his <x>plots




    # If y class is selected under Data Analysis
    elif analysis_selection == "<y>：Statistical tendencies":
        st.write("### <y> Statistical tendencies")

        # Add sub-titles for y class
        y_sub_title = st.sidebar.selectbox("Choose a sub-title for y class", ["Programming experience vs Salary", "income_country", "the composition of industry based on age","job_title","the gender ratio"])
        st.write(f"You chose {y_sub_title} under {analysis_selection}")
        # Display content or analysis for the chosen sub-title
        if y_sub_title == "the composition of industry based on age":
            st.write("you have to choose an age range and the years  and then we will give you a barchart. We do not have data on 2020 so you can not selet this year")
            # Add a age range selector
            age_range = st.sidebar.selectbox("Choose an age_range", ["25-29", "30-34", "35-39", "22-24", "40-44 ", "45-49 ", "50-54", "18-21  ", "55-59 ", "60-69 ","70+"])
            # Add a year range selector
            year_range_str = st.sidebar.selectbox("choose a year_range",["[2021, 2022]","[2021]","[2022]"])
            year_range = eval(year_range_str)
            # Display the plot based on the selected bottoms
            plot_industry_distribution(age_range, year_range )








# If Recommendation is selected
elif main_selection == "Recommendation":
    st.write("## Recommendation")

# Remember to run the app with: streamlit run your_script_name.py
