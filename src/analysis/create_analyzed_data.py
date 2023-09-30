import pandas as pd

from src.analysis.framework import framework
from src.analysis.job_title import title
from src.analysis.country_income import country_income


data_preprocessed = pd.read_csv('./data/processed/Data_Preprocess_v6.csv', low_memory=False)

data_framework = framework(data_preprocessed)
data_framework.to_csv('./data/analyzed/framework.csv',
            index=False, header=True, mode='w')

data_title = title(data_preprocessed)
data_title.to_csv('./data/analyzed/job_title.csv',
            index=False, header=True, mode='w')

data_income = country_income(data_preprocessed)
data_income.to_csv('./data/analyzed/country_income.csv',
            index=False, header=True, mode='w')






