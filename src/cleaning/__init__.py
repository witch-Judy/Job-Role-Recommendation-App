"""
Author:     Liao Yueh-Fan
Data:       2023/9/21
Course:     NUS IT5006 Fundamentals of Data Analytics
Project:    Job Role Recommendation App
Function:   Init fot Data Cleaning and Preprocessing
"""

from data_preprecess import data_preprocess

data = data_preprocess()
data.to_csv(r'..\..\data\processed\Data_Preprocess_v3.csv',
            index=False, header=True, mode='w')