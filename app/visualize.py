from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def vis_income():
    list_of_top10 = ['India', 'United States of America', 'Japan', 'Brazil', 'Russia', 'United Kingdom of Great Britain and Northern Ireland', 'Nigeria', 'Spain', 'China', 'Germany']
    
    country = st.multiselect('Select countries to display their median income distribution:', list_of_top10, default='United States of America')
    start, end = st.slider("Select the time frame", 2020, 2022, (2020,2022))
    
    # read country_income data from analyzed folder
    income = pd.read_csv('./data/analyzed/country_income.csv', low_memory=False)

    # filter the data as per the user input
    income = income[income['Year'].isin(range(start, end+1))]
    income = income[income['Country'].isin(country)]

    # sort the country by the name of the country to maintain order in the graph
    income = income.sort_values(by=['Country'])
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



st.header("Data Science and Machine Learning")
st.header("Industry Survey 2020-2022")

tab1, tab2 = st.tabs(["Trends", "Statistics"])

with tab1:
    st.header("Trends")
    labelx = ['Popular Job Titles', 'Popular Machine Learning Frameworks']
    x = st.selectbox("Which trend do you want to see?",labelx,0)

    if x == 'Popular Machine Learning Frameworks':
        vis_ML()

    if x == 'Popular Job Titles':
        vis_Jobtitle()

with tab2:
    st.header("Statistics")
    labely = ['Income by Country']
    y = st.selectbox("Which Statistics do you want to see?", labely, 0)

    if y == 'Income by Country':
        vis_income()
            

        
