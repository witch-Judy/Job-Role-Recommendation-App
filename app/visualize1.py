from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
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
    st.header("Estimated Income Distribution in selected countries within the chosen timeframe")

    col1, col2 = st.columns([3, 2])
    country = col1.multiselect('Select countries to display their median income distribution:', list_of_top10,
                             default='United States of America')
    start, end = col1.slider("Select the time frame", 2020, 2022, (2020, 2022))

    # read country_income data from analyzed folder
    income = pd.read_csv('./data/analyzed/country_income.csv', low_memory=False)

    # filter the data as per the user input
    income = income[income['Year'].isin(range(start, end + 1))]
    income = income[income['Country'].isin(country)]

    # sort the country by the name of the country to maintain order in the graph
    income = income.sort_values(by=['Country'])
    income.rename(columns={'Median': 'Median Income'}, inplace=True)

    plt.figure(figsize=(10, 6))
    sns.set(style="whitegrid")
    ax = sns.boxplot(x='Country', y='Median Income', data=income)
    plt.title("Income Distribution by Country")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=10)
    col1.pyplot(plt)

    # observation and disclaimer
    show_description(col2, "Income by Country")

    
def vis_ML():
    # read framework data from analyzed folder
    pop_framework = pd.read_csv('./data/analyzed/framework.csv', low_memory=False)
    print(pop_framework)

    st.header("Change in the Composition of Popular Machine Learning Frameworks over the three years")

    # Convert absolute numbers to percentages
    for year in ['2020', '2021', '2022']:
        total = pop_framework[year].sum()
        pop_framework[f'{year}_pct'] = (pop_framework[year] / total) * 100

    # Function to create a bar chart using Matplotlib
    def create_percentage_bar_chart(data):
        fig, ax = plt.subplots()
        x = range(len(data))
        ax.bar(x, data['2020_pct'], width=0.2, label='2020')
        ax.bar([p + 0.2 for p in x], data['2021_pct'], width=0.2, label='2021')
        ax.bar([p + 0.4 for p in x], data['2022_pct'], width=0.2, label='2022')
        ax.set_xticks([p + 0.2 for p in x])
        ax.set_xticklabels(data['Framework'])
        plt.xticks(rotation=45)
        plt.legend()
        plt.title('Percentage Composition of Machine Learning Frameworks 2020-2022')
        plt.ylabel('Percentage')
        plt.xlabel('Frameworks')
        return fig

    col1, col2 = st.columns([3, 2])
    # Create a percentage bar chart
    col1.pyplot(create_percentage_bar_chart(pop_framework))

    # observation and disclaimer
    show_description(col2, "Popular Machine Learning Frameworks")



def vis_Jobtitle():
    # read job title data from analyzed folder
    title_of_top5 = pd.read_csv('./data/analyzed/job_title.csv', low_memory=False)
    st.header("Top Five Job Titles of the respondants")

    col1, col2 = st.columns([3, 2])
    # Create a multiselect widget with the top 5 job titles
    selected_titles = col1.multiselect('Select job titles to display their trends:', title_of_top5['Title'], 'Student')

    if selected_titles == []:
        col1.markdown(''':red[Please select at least one job title]''')

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
        col1.pyplot(fig)

    # observation and disclaimer
    show_description(col2, "Popular Job Titles")

def program_lan():
    st.header("The Trend of Programming Language used by Specific Country")
    label_country = ['United States of America', 'Japan', 'United Kingdom of Great Britain and Northern Ireland',
                     'France', 'Germany', 'India', 'Brazil', 'China', 'Russia', 'Indonesia']

    col1, col2 = st.columns([3, 2])
    country = col1.selectbox("Which country do you want to see?", label_country, 0)
    plot_language_trend(col1, country)

    # observation and disclaimer
    show_description(col2, "Popular Programming Languages")

def age_dist():
    st.header("Industry Distribution for Age Range")

    col1, col2 = st.columns([3, 2])
    label_ages = ["18-21", "22-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-69", "70+"]
    ages = col1.selectbox("which age range do you want to see? ", label_ages, 0)
    label_years = [2021, 2022, (2021, 2022)]
    years = col1.selectbox("Which years range do you want to see?", label_years, 0)
    if isinstance(years, int):
        years = [years]
    plot_industry_distribution(col1, ages, years)

    # observation and disclaimer
    show_description(col2, "Industry Distribution on Different Age Ranges")


def salary_exper():
    st.header("Relationship Between Coding Experience and Yearly Compensation.")

    col1, col2 = st.columns([3, 2])
    selected_years_range = col1.slider('Select a range of years', 2020, 2022, (2020, 2022))
    if selected_years_range[0] == selected_years_range[1]:
        years_list = [selected_years_range[0]]
    else:
        years_list = list(selected_years_range)
    years2 = list(years_list)
    plot_experience_vs_compensation(col1, years2)
    # observation and disclaimer
    show_description(col2, "Experience vs Salary")


def gen_dist():
    st.header("Gender Percentage of Different Countries")
    # label_years3 = [(2020, 2021, 2022), 2020, 2021, 2022, (2020, 2021), (2020, 2022), (2021, 2022)]
    # years3 = st.selectbox("Which years range do you want to see?", label_years3, 0)
    # if isinstance(years3, int):
    #     years3 = [years3]

    col1, col2 = st.columns([3, 2])
    selected_years_range2 = col1.slider('Select a range of years', 2020, 2022, (2020, 2022))
    if selected_years_range2[0] == selected_years_range2[1]:
        years_list2 = [selected_years_range2[0]]
    else:
        years_list2 = list(selected_years_range2)
    years3 = list(years_list2)
    plot_gender_distribution(col1, years3)# observation and disclaimer
    show_description(col2, "Gender Distribution")

def show_description(col, title):
    col.empty()
    df_observation = pd.read_csv("./docs/Exploratory data analysis observations.csv")
    df_disclaimer = pd.read_csv("./docs/Exploratory data analysis disclaimer.csv")
    doc_list = [df_observation, df_disclaimer]
    doc_header = ["Observation", "Disclaimer"]
    # loop all the content(observation/disclaimer) in that column
    for idx in range(len(doc_header)):
        row = 0
        col.subheader(doc_header[idx])
        while True:
            if row == doc_list[idx].shape[0]:
                break
            elif pd.notna(doc_list[idx].loc[row, title]):
                # print observation
                obs_str = str(row+1) + ". " + doc_list[idx].loc[row, title]
                col.write(obs_str)
            else:
                break
            row += 1

import streamlit as st
st.set_page_config(layout="wide")

st.sidebar.title("Job-Role-Recommendation-App")

main_selection = st.sidebar.selectbox("Choose a function:", ["analysis", "recommendation"])

if main_selection == "analysis":
    analysis_selection = st.sidebar.selectbox("Choose an analysis:", ["Trends", "Statistics"])

    if analysis_selection == "Trends":
        labelx = ['Popular Job Titles', 'Popular Machine Learning Frameworks', 'Popular Programming Languages']
        x = st.sidebar.selectbox("Which trend do you want to see?", labelx, 0)

        if x == 'Popular Machine Learning Frameworks':
            vis_ML()
        elif x == 'Popular Job Titles':
            vis_Jobtitle()
        elif x == 'Popular Programming Languages':
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
