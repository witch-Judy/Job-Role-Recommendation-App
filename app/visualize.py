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
    list_of_top10 = ['India', 'United States of America', 'Japan', 'Brazil', 'Russia', 'United Kingdom of Great Britain and Northern Ireland', 'Nigeria', 'Spain', 'China', 'Germany']
    
    country = st.multiselect('Select countries to display their median income distribution:', list_of_top10, default='United States of America')
    start, end = st.slider("Select the time frame", 2020, 2022, (2020,2022))
    
    # read country_income data from analyzed folde
    income = pd.read_csv('./data/analyzed/country_income.csv', low_memory=False)

    income = income[income['Year'].isin(range(start, end+1))]
    income = income[income['Country'].isin(country)]
    income.rename(columns={'Median': 'Median Income'}, inplace=True)

    st.markdown("### Estimated Income Distribution in selected countries within the chosen timeframe ###")

    plt.figure(figsize=(10, 6))
    sns.set(style="whitegrid")
    ax=sns.boxplot(x='Country', y='Median Income', data=income)
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

    st.plotly_chart(px.pie(pop_framework, values='2020', names='Framework', title='Popular Machine Learning Frameworks in 2020', ))
    st.plotly_chart(px.pie(pop_framework, values='2021', names='Framework', title='Popular Machine Learning Frameworks in 2021', ))
    st.plotly_chart(px.pie(pop_framework, values='2022', names='Framework', title='Popular Machine Learning Frameworks in 2022', ))


    # disclaimer
    st.write('Disclaimer')
    st.write('1. Top 6 most used Machine Learning frameworks are shown and the rest are combined as Others')



def vis_Jobtitle():
    # read job title data from analyzed folder
    title_of_top5 = pd.read_csv('./data/analyzed/job_title.csv', low_memory=False)


    st.markdown("### Top Five Job Titles of the respondants ###")

    # Create a multiselect widget with the top 5 job titles
    selected_titles = st.multiselect('Select job titles to display their trends:', title_of_top5['Title'], 'Student')

    # Filter the DataFrame for the selected title
    title_data = title_of_top5[title_of_top5['Title'].isin(selected_titles)]
    # Create a line plot for the selected title
    st.line_chart(title_data.set_index('Title').T)

    # disclaimer
    st.write('Disclaimer')
    st.write('1. Top five job titles of the respondants are selected')
    st.write('2. The job titles of the same role are synchronized')
def program_lan():
    st.markdown("### the trend of Programming Language used by specific country ###")
    label_country = ['United States of America','Japan','United Kingdom of Great Britain and Northern Ireland','France','Germany','India','Brazil','China','Russia','Indonesia']

    country = st.selectbox("Which country do you want to see?", label_country, 0)
    plot_language_trend(country)
    # disclaimer
    st.write('Disclaimer')
    st.write('1.Top 10 countries are selected, based on the number of responders in the dataset, we give you the top five developed and developing countries with the highest respective numbers.')
    st.write(
        "2.It is interesting to see that the largest number of people use Python, because the data set comes from the questionnaire sent to users by Kaggle, and most people who use Kaggle do machine learning and data analysis. Python is usually used to handle this kind of problem. ")



def age_dist():
    st.markdown("### Industry Distribution for Age Range ###")
    label_ages = ["25-29", "30-34", "35-39", "22-24", "40-44 ", "45-49 ", "50-54", "18-21  ", "55-59 ", "60-69 ", "70+"]
    ages = st.selectbox("which age range do you want to see? ", label_ages, 0)
    label_years = [2021,2022,(2021,2022)]
    years = st.selectbox("Which years range do you want to see?", label_years, 0)
    if isinstance(years, int):
        years = [years]
    plot_industry_distribution(ages, years)
    st.write('Disclaimer')
    st.write("There is no industry data in 2020, so we don't give you this option.")
def salary_exper():
    st.markdown("### Relationship Between Coding Experience and Yearly Compensation. ###")
    label_years2 = [(2020,2021,2022),2020,2021,2022,(2020,2021),(2020,2022),(2021,2022)]
    years2 = st.selectbox("Which years range do you want to see?",label_years2,0)
    if isinstance(years2, int):
        years2 = [years2]
    plot_experience_vs_compensation(years2)
    st.write('Disclaimer')
    st.write("In the questionnaire survey data set, there are no 1-2 year options for 2021 and 2022, so they are empty. ")
def gen_dist():
    st.markdown("### the gender percentage of different countries. ###")
    label_years3 = [(2020, 2021, 2022), 2020, 2021, 2022, (2020, 2021), (2020, 2022), (2021, 2022)]
    years3 = st.selectbox("Which years range do you want to see?", label_years3, 0)
    if isinstance(years3, int):
        years3 = [years3]
    plot_gender_distribution(years3)
    st.write('Disclaimer')
    st.write("Top 10 countries are selected, based on the number of responders in the dataset, we give you the top five developed and developing countries with the highest respective numbers.")

st.header("Data Science and Machine Learning")
st.header("Industry Survey 2020-2022")

tab1, tab2 = st.tabs(["Trends", "Statistics"])

with tab1:
    st.header("Trends")
    labelx = ['Popular Job Titles', 'Popular ML Framework','Popular Programming Language']
    x = st.selectbox("Which trend do you want to see?",labelx,0)

    if x == 'Popular ML Framework':
        vis_ML()

    elif x == 'Popular Job Titles':
        vis_Jobtitle()
    elif x == 'Popular Programming Language':
        program_lan()

with tab2:
    st.header("Statistics")
    labely = ['Income by Country','industry distribution of different age_range','experience vs salary','gender distribution']
    y = st.selectbox("Which Statistics do you want to see?", labely, 0)

    options = {
        'Income by Country': vis_income,
        'industry distribution of different age_range': age_dist,
        'experience vs salary': salary_exper,
        'gender distribution': gen_dist
    }

    if y in options:
        options[y]()
    else:
        print("Invalid option: ", y)

            

        


