"""
Author:     Chen Bihan
Data:       2023/9/26
Course:     NUS IT5006 Fundamentals of Data Analytics
Project:    Job Role Recommendation App
Function:   to filter the data to get better Corresponding speed
"""

import pandas as pd
import os
# Get the absolute path of the current script
current_path = os.path.abspath(__file__)
# Get the root directory of the project
project_root_path = os.path.dirname(os.path.dirname(os.path.dirname(current_path)))
loc = os.path.join(project_root_path, "data", "processed")
final_data_path = os.path.join(loc, "Data_Preprocess_v6.csv")
final_data = pd.read_csv(final_data_path)
# the data of chen functions
# for age_industry
selected_columns1 = final_data[['year', 'Q2_age', 'Q24_industry']]
new_data1 = pd.DataFrame(selected_columns1)
condition1 = new_data1['year'] != 2020
filtered_data1 = new_data1[condition1]
file_path1 = os.path.join(project_root_path, "data", "analyzed", "age_industry.csv")
filtered_data1.to_csv(file_path1, index=False, header=True, mode='w')

# for coding language country
top_languages = ['Q12_coding language_Python', 'Q12_coding language_R', 'Q12_coding language_SQL',
                 'Q12_coding language_C', 'Q12_coding language_C++', 'Q12_coding language_Java',
                 'Q12_coding language_Javascript', 'Q12_coding language_Bash',
                 'Q12_coding language_MATLAB', 'Q12_coding language_Julia']
selected_columns2 = ['year', 'Q4_country'] + top_languages
filtered_data2 = final_data[selected_columns2]
file_path2 = os.path.join(project_root_path, "data", "analyzed", "coding_language_country.csv")
filtered_data2.to_csv(file_path2, index=False, header=True, mode='w')


# for experience_vs_salary
selected_columns3 = ['year', 'Q5_student or not', 'Q29_yearly compensation', 'Q11_coding years']
filtered_data3 = final_data[selected_columns3]
file_path3 = os.path.join(project_root_path, "data", "analyzed", "experience_vs_salary.csv")
filtered_data3.to_csv(file_path3, index=False, header=True, mode='w')

# for gender_distribution
selected_columns4 = ['year','Q4_country','Q3_gender']
filtered_data4 = final_data[selected_columns4]
file_path4 = os.path.join(project_root_path, "data", "analyzed", "gender_distribution.csv")
filtered_data4.to_csv(file_path4,index=False, header=True, mode='w')