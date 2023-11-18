from collections import namedtuple
import altair as alt
import math

import numpy as np
import pandas as pd
import streamlit as st
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
import warnings
import joblib

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
    st.markdown("<h3 style='text-align: center; color: #78798F;'>Input your chioces and click 'Recommend' button below</h3>", unsafe_allow_html=True) 

    # Get the absolute path of the current script
    current_path = os.path.abspath(__file__)
    # Go up three levels to get the root directory of the project
    project_root_path = os.path.dirname(os.path.dirname(os.path.dirname(current_path)))
    # Verify if we have reached the correct root path
    expected_root = "Job-Role-Recommendation-App"
    if expected_root not in project_root_path:
        # Adjust the path accordingly if the expected root is not found
        project_root_path = os.path.join(project_root_path, expected_root)

    loc = os.path.join(project_root_path, "src", "modelling")

    # Define file paths
    model_path = os.path.join(loc, "model_and_encoders.joblib")

    # Load models
    try:
        model_package = joblib.load(model_path)

    except FileNotFoundError as e:
        print("File not found error:", e)

    st.sidebar.title("Input your details")

    coding_languages = st.sidebar.multiselect(
        'Select your coding languages',
        ['Bash', 'C', 'C#', 'C++', 'Go', 'Java', 'Javascript', 'Julia', 'MATLAB', 'PHP', 'Python', 'R', 'SQL', 'Swift', 'Other', 'Choose not to answer'])
    ide = st.sidebar.multiselect(
        'Select your IDEs',
        ['Notepad++',
        'Spyder',
        'Sublime Text',
        'Vim / Emacs',
        'Jupyter Notebook',
        'MATLAB',
        'PyCharm',
        'RStudio',
        'Visual Studio',
        'Visual Studio Code (VSCode)',
        'Choose not to answer',
        'IntelliJ',
        'Jupyter (JupyterLab, Jupyter Notebooks, etc)',
        'JupyterLab',
        'Other'])
    data_viz_libs = st.sidebar.multiselect(
        'Select your data visualization libraries',
        ['Altair',
        'Bokeh',
        'D3 js',
        'Dygraphs',
        'Geoplotlib',
        'Ggplot / ggplot2',
        'Highcharter',
        'Leaflet / Folium',
        'Plotly / Plotly Express',
        'Pygal',
        'Seaborn',
        'Shiny',
        'Choose not to answer',
        'Matplotlib',
        'Other'])
    
    ml_algos = st.sidebar.multiselect(
        'Select Machine Learning algorithms you use',
        ['Autoencoder Networks (DAE, VAE, etc)',
        'Bayesian Approaches',
        'Choose not to answer',
        'Convolutional Neural Networks',
        'Decision Trees or Random Forests',
        'Dense Neural Networks (MLPs, etc)',
        'Evolutionary Approaches',
        'Generative Adversarial Networks',
        'Gradient Boosting Machines (xgboost, lightgbm, etc)',
        'Graph Neural Networks',
        'Linear or Logistic Regression',
        'Other',
        'Recurrent Neural Networks',
        'Transformer Networks (BERT, gpt-3, etc)'])

    coding_years = st.sidebar.selectbox(
        'Select your coding years',
        ['< 1 years', '1-2 years', '1-3 years','3-5 years', '5-10 years', '10-20 years', '20+ years'],
        )
    ml_years = st.sidebar.selectbox(
        'Select your Machine Learning years',
        ['Under 1 year', '1-2 years', '2-3 years','3-4 years', '4-5 years', '5-10 years', '10-20 years',  '20 or more years',  'I do not use machine learning methods'])
    age = st.sidebar.selectbox(
        'Select your age group',
        ['18-21', '22-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-69', '70+'])
    gender = st.sidebar.selectbox(
        'Select your gender',
        ['Man', 'Woman', 'Nonbinary', 'Prefer not to say', 'Choose not to answer'])
    country = st.sidebar.selectbox(
        'Select your country',
        ['Algeria', 'Argentina', 'Australia', 'Austria', 'Bangladesh', 'Belarus', 'Belgium', 'Brazil', 'Cameroon', 'Canada', 'Chile', 'China', 'Colombia', 'Czech Republic', 'Denmark', 'Ecuador', 'Egypt', 'Ethiopia', 'France', 'Germany', 'Ghana', 'Greece', 'Hong Kong (S.A.R.)', 'India', 'Indonesia', 'Iran, Islamic Republic of...', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Japan', 'Kazakhstan', 'Kenya', 'Malaysia', 'Mexico', 'Morocco', 'Nepal', 'Netherlands', 'Nigeria', 'Norway', 'Other', 'Pakistan', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Republic of Korea', 'Romania', 'Russia', 'Saudi Arabia', 'Singapore', 'South Africa', 'South Korea', 'Spain', 'Sri Lanka', 'Sweden', 'Switzerland', 'Taiwan', 'Thailand', 'Tunisia', 'Turkey', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom of Great Britain and Northern Ireland', 'United States of America', 'Viet Nam', 'Zimbabwe'],
        index=50)
    tpu_use_freq = st.sidebar.selectbox(
        'Select your TPU usage frequency',
        [ 'Never', 'Once', '2-5 times', '6-25 times', 'More than 25 times'])
    academic_degree = st.sidebar.selectbox(
        'Select your highest academic degree',
        ['Bachelor’s degree', 'Doctoral degree', 'Master’s degree', 'No formal education past high school', 'Professional degree', 'Professional doctorate', 'Some college/university study without earning a bachelor’s degree'])

    # if st.sidebar.button('Recommend'):
    if st.sidebar.button('Recommend'):
 
        ans = {
            "Q11_coding years": [coding_years],
            "Q12_coding language": [':'.join(coding_languages)],
            "Q13_IDE": [':'.join(ide)],
            "Q15_data visualization lib": [':'.join(data_viz_libs)],
            "Q16_ML years": [ml_years],
            "Q18_ML algo": [':'.join(ml_algos)],
            "Q2_age": [age],
            "Q3_gender": [gender],
            "Q4_country": [country],
            "Q43_TPU use freq": [tpu_use_freq],
            "Q8_academic dgree": [academic_degree]
        }
        multi_select_columns = [
            'Q12_coding language',
            'Q13_IDE',
            'Q15_data visualization lib',
            'Q18_ML algo'
            ]

        single_select_columns = [
            'Q11_coding years',
            'Q16_ML years',  
            'Q2_age',
            'Q3_gender', 
            'Q4_country', 
            'Q43_TPU use freq',
            'Q8_academic dgree'
            ]

        user_data = pd.DataFrame(ans)
        rf = model_package['model']
        mlb_encoders = model_package['mlb_encoders']
        ohe_encoders = model_package['ohe_encoders']

        # Assuming new_data is your new data for prediction
        # Preprocess new_data using the saved encoders
        multi_encoded = [pd.DataFrame(mlb_encoders[col].transform(user_data[col].str.split(':')),
                                    columns=mlb_encoders[col].classes_,
                                    index=user_data.index) for col in multi_select_columns]

        single_encoded = [pd.DataFrame(ohe_encoders[col].transform(user_data[[col]]),
                                    columns=ohe_encoders[col].get_feature_names_out([col]),
                                    index=user_data.index) for col in single_select_columns]

        
        # Combine encoded features
        new_data_encoded = pd.concat(multi_encoded + single_encoded, axis=1)

        # Make predictions
        predictions = rf.predict_proba(new_data_encoded)

        class_labels = rf.classes_

        # Extract the probabilities for the single instance
        probs = predictions[0]

        # Get indices of the top 3 probabilities in descending order
        top_3_indices = np.argsort(probs)[::-1][:3]
        the_rest = np.argsort(probs)[::-1][3:]

        # Get corresponding class labels and probabilities
        top_3_labels_and_probs = [(class_labels[idx], probs[idx]) for idx in top_3_indices]
        the_rest_labels_and_probs = [(class_labels[idx], probs[idx]) for idx in the_rest]
        
        st.markdown("<h1 style='text-align: center; color: 78798F;'>Recommended Job Roles</h1>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("<br><br>", unsafe_allow_html=True)
        for idx, (label, prob) in enumerate(top_3_labels_and_probs, start=1):
            st.markdown(f"<h3 style='text-align: left; color: #4E9948; font-family: Arial, sans-serif; margin-left: 10px;'>{idx}. {label}: {prob * 100:.2f}%</h3>", unsafe_allow_html=True)

        for idx, (label, prob) in enumerate(the_rest_labels_and_probs, start=4):
            st.markdown(f"<h6 style='text-align: left; color: #A3C4B6; font-family: Arial, sans-serif; margin-left: 10px;'>{idx}. {label}: {prob * 100:.2f}%</h6>", unsafe_allow_html=True)
            
        st.markdown("<br><br>", unsafe_allow_html=True) 
        st.markdown("---")
        st.markdown(f"<h6 style='text-align: left; color: #E89086; font-family: Arial, sans-serif; margin-left: 10px;'>*Note: This model is trained on data from 2020-2022. The predictions are based on 11 popular job roles in the industry.</h6>", unsafe_allow_html=True)


