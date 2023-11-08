"""
Author:     Liao Yueh-Fan
Data:       2023/9/21
Course:     NUS IT5006 Fundamentals of Data Analytics
Project:    Job Role Recommendation App
Function:   Init fot Data Cleaning and Preprocessing
"""

from data_preprecess import data_preprocess
from data_encoding import data_encoding
import pandas as pd

# data = data_preprocess()
# data.to_csv(r'..\..\data\processed\Data_Preprocess_v6.csv',
#             index=False, header=True, mode='w')

# data = data_encoding(data)
# data.to_csv(r'..\..\data\processed\Data_Preprocess_Encode_v1.csv',
#             index=False, header=True, mode='w')


data = pd.read_csv('./data/processed/Data_Preprocess_v6.csv', low_memory=False)

data = data_encoding(data)
data.to_csv('./data/processed/Data_Preprocess_Encode_v1.csv',
            index=False, header=True, mode='w')
