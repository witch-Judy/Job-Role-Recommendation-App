from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import sys
import os
import warnings

warnings.filterwarnings("ignore")

current_path = os.path.abspath(__file__)
parent_path = os.path.dirname(current_path)
project_root_path = os.path.dirname(parent_path)
sys.path.append(project_root_path)

from src.analysis.coding_language_country import plot_language_trend
from src.analysis.age_industry import plot_industry_distribution
from src.analysis.experience_vs_salary import plot_experience_vs_compensation
from src.analysis.gender_distribution import plot_gender_distribution


def vis_income():
    list_of_top10 = ['India', 'United States of America', 'Japan', 'Brazil', 'Russia',
                     'United Kingdom of Great Britain and Northern Ireland', 'Nigeria', 'Spain', 'China', 'Germany']

    country = st.multiselect('Select countries to display their median income distribution:', list_of_top10,
                             default='United States of America')
    start, end = st.slider("Select the time frame", 2020, 2022, (2020, 2022))

    # read country_income data from analyzed folder
    income = pd.read_csv('./data/analyzed/country_income.csv', low_memory=False)

    # filter the data as per the user input
    income = income[income['Year'].isin(range(start, end + 1))]
    income = income[income['Country'].isin(country)]

    # sort the country by the name of the country to maintain order in the graph
    income = income.sort_values(by=['Country'])
    income.rename(columns={'Median': 'Median Income'}, inplace=True)

    st.markdown("### Estimated Income Distribution in selected countries within the chosen timeframe ###")

    plt.figure(figsize=(10, 6))
    sns.set(style="whitegrid")
    ax = sns.boxplot(x='Country', y='Median Income', data=income)
    plt.title("Income Distribution by Country")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=10)
    st.pyplot(plt)

    # disclaimer
    st.empty()
    st.write('Disclaimer')
    st.write('1. Top ten countries with the most respondants are selected.')
    st.write('2. The income of each respondant is estimated as the average of the min and max of the chosen range.')
    st.write('3. The outliers who earn more than $500,000 is filtered out.')


def vis_ML():
    # read framework data from analyzed folder
    pop_framework = pd.read_csv('./data/analyzed/framework.csv', low_memory=False)
    print(pop_framework)

    st.markdown("### Change in the Composition of Popular Machine Learning Frameworks over the three years ###")

    # Create pie charts for the three years
    st.plotly_chart(
        px.pie(pop_framework, values='2020', names='Framework', title='Popular Machine Learning Frameworks in 2020', ))
    st.plotly_chart(
        px.pie(pop_framework, values='2021', names='Framework', title='Popular Machine Learning Frameworks in 2021', ))
    st.plotly_chart(
        px.pie(pop_framework, values='2022', names='Framework', title='Popular Machine Learning Frameworks in 2022', ))

    # disclaimer
    st.write('Disclaimer')
    st.write('1. Top 6 most used Machine Learning frameworks are shown and the rest are combined as Others')


def vis_Jobtitle():
    # read job title data from analyzed folder
    title_of_top5 = pd.read_csv('./data/analyzed/job_title.csv', low_memory=False)

    st.markdown("### Top Five Job Titles of the respondants ###")

    # Create a multiselect widget with the top 5 job titles
    selected_titles = st.multiselect('Select job titles to display their trends:', title_of_top5['Title'], 'Student')

    if selected_titles == []:
        st.markdown(''':red[Please select at least one job title]''')

    else:
        # Filter the DataFrame for the selected title
        title_data = title_of_top5[title_of_top5['Title'].isin(selected_titles)]

        # Create a line plot for the selected title
        title_data.set_index('Title', inplace=True)

        # Plot the line chart using Matplotlib
        fig, ax = plt.subplots()
        title_data.T.plot(kind='line', ax=ax, marker='o')

        # Set plot details
        ax.set(xlabel='Year', ylabel='Counts', title='Job Titles Over Years')
        ax.grid(False)
        ax.legend(title='Job Title')

        # Display the Matplotlib plot in Streamlit
        st.pyplot(fig)

    # disclaimer
    st.write('Disclaimer')
    st.write('1. Top five job titles of the respondants are selected')
    st.write('2. The job titles of the same role are synchronized')


def program_lan():
    st.markdown("### The Trend of Programming Language used by Specific Country ###")
    label_country = ['United States of America', 'Japan', 'United Kingdom of Great Britain and Northern Ireland',
                     'France', 'Germany', 'India', 'Brazil', 'China', 'Russia', 'Indonesia']

    country = st.selectbox("Which country do you want to see?", label_country, 0)
    plot_language_trend(country)
    # disclaimer
    st.write('Disclaimer')
    st.write(
        '1.Top 10 countries are selected, based on the number of responders in the dataset, we give you the top five developed and developing countries with the highest respective numbers.')
    st.write(
        "2.It is interesting to see that the largest number of people use Python, because the data set comes from the questionnaire sent to users by Kaggle, and most people who use Kaggle do machine learning and data analysis. Python is usually used to handle this kind of problem. ")


def age_dist():
    st.markdown("### Industry Distribution for Age Range ###")
    label_ages = ["18-21", "22-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-69", "70+"]
    ages = st.selectbox("which age range do you want to see? ", label_ages, 0)
    label_years = [2021, 2022, (2021, 2022)]
    years = st.selectbox("Which years range do you want to see?", label_years, 0)
    if isinstance(years, int):
        years = [years]
    plot_industry_distribution(ages, years)
    st.write('Disclaimer')
    st.write("There is no industry data in 2020, so we don't give you this option.")


def salary_exper():
    st.markdown("### Relationship Between Coding Experience and Yearly Compensation. ###")
    selected_years_range = st.slider('Select a range of years', 2020, 2022, (2020, 2022))
    if selected_years_range[0] == selected_years_range[1]:
        years_list = [selected_years_range[0]]
    else:
        years_list = list(selected_years_range)
    years2 = list(years_list)
    plot_experience_vs_compensation(years2)
    st.write('Disclaimer')
    st.write(
        "In the questionnaire survey data set, there are no 1-2 year options for 2021 and 2022, so they are empty. ")


def gen_dist():
    st.markdown("### the gender percentage of different countries. ###")
    # label_years3 = [(2020, 2021, 2022), 2020, 2021, 2022, (2020, 2021), (2020, 2022), (2021, 2022)]
    # years3 = st.selectbox("Which years range do you want to see?", label_years3, 0)
    # if isinstance(years3, int):
    #     years3 = [years3]

    selected_years_range2 = st.slider('Select a range of years', 2020, 2022, (2020, 2022))
    if selected_years_range2[0] == selected_years_range2[1]:
        years_list2 = [selected_years_range2[0]]
    else:
        years_list2 = list(selected_years_range2)
    years3 = list(years_list2)
    plot_gender_distribution(years3)
    st.write('Disclaimer')
    st.write(
        "Top 10 countries are selected, based on the number of responders in the dataset, we give you the top five developed and developing countries with the highest respective numbers.")


import streamlit as st

st.sidebar.title("Job-Role-Recommendation-App")

main_selection = st.sidebar.selectbox("Choose a function:", ["analysis", "recommendation"])

if main_selection == "analysis":
    analysis_selection = st.sidebar.selectbox("Choose an analysis:", ["Trends", "Statistics"])

    if analysis_selection == "Trends":
        labelx = ['Popular Job Titles', 'Popular Machine Learning Frameworks', 'Popular Programming Language']
        x = st.sidebar.selectbox("Which trend do you want to see?", labelx, 0)

        if x == 'Popular Machine Learning Frameworks':
            vis_ML()
        elif x == 'Popular Job Titles':
            vis_Jobtitle()
        elif x == 'Popular Programming Language':
            program_lan()

    elif analysis_selection == "Statistics":
        labely = ['Income by Country', 'Industry Distribution of Different Age Range', 'Experience vs Salary',
                  'Gender Distribution']
        y = st.sidebar.selectbox("Which Statistics do you want to see?", labely, 0)

        options = {
            'Income by Country': vis_income,
            'Industry Distribution of Different Age Range': age_dist,
            'Experience vs Salary': salary_exper,
            'Gender Distribution': gen_dist
        }

        if y in options:
            options[y]()
        else:
            print("Invalid option: ", y)

elif main_selection == "recommendation":
    st.write("Recommendation content will be added here.")
