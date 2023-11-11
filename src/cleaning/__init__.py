"""
Author:     Liao Yueh-Fan
Data:       2023/9/21
Course:     NUS IT5006 Fundamentals of Data Analytics
Project:    Job Role Recommendation App
Function:   Init fot Data Cleaning and Preprocessing
"""

from data_preprecess import data_preprocess
from data_encoding import data_encoding

data = data_preprocess()
data.to_csv(r'D:\personal\Master Program\Course Learning\Sem1\IT5006_Fundamentals of Data Analytics\Project\data\processed\Data_Preprocess_v7.csv',
            index=False, header=True, mode='w')

# data = data_encoding(data)
# data.to_csv(r'D:\personal\Master Program\Course Learning\Sem1\IT5006_Fundamentals of Data Analytics\Project\data\processed\Data_Preprocess_Encode_v1.csv',
#             index=False, header=True, mode='w')
