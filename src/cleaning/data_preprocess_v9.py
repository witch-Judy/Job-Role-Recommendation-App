import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, MultiLabelBinarizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import os
import numpy as np
import joblib

# ---------------------summary ---------------------

# from V8 

# 1. drop the columns that have 'Choose not to answer' more than 50% (more than 50% empty)
# 2. drop the rows(repondants) that did not answer to more than 30% of the questions'

# ---------------------------------------------------


# Get the absolute path of the current script
path = "../../data/processed/Data_Preprocess_v8_simplified.csv"
data = pd.read_csv(path, low_memory=False)
data.shape

# count the percentage of 'Choose not to answer' in each column
for col in data.columns:
    count = data[col].value_counts(normalize=True).get('Choose not to answer', 0)
    percentage = count * 100
    print(f"{col}: {percentage:.2f}%")

# list the columns that have 'Choose not to answer' more than 50%
# Initialize an empty list to store column names to be dropped
columns_to_drop = []

# Iterate over each column to calculate the percentage
for col in data.columns:
    count = data[col].value_counts(normalize=True).get('Choose not to answer', 0)
    percentage = count * 100
    if percentage > 50:
        columns_to_drop.append(col)

# Drop the identified columns
reduced_data = data.drop(columns=columns_to_drop)

# Print the names of the columns dropped
print(f"Columns dropped: {columns_to_drop}")

# Initialize a list to store the indices of rows to be flagged
rows_to_flag = []

# Iterate over the rows
for index, row in reduced_data.iterrows():
    # Count the occurrences of 'Choose not to answer'
    count = (row == 'Choose not to answer').sum()
    # Calculate the percentage
    percentage = (count / len(row)) * 100
    # Check if the percentage exceeds 50%
    if percentage > 30:
        rows_to_flag.append(index)

# Print the indices of the rows
print(f"Row indices where more than 30% of data is 'Choose not to answer': {rows_to_flag}")
print(len(rows_to_flag))

reduced_data = reduced_data.drop(rows_to_flag, axis=0)

reduced_data.to_csv('../../data/processed/Data_Preprocess_v9_reduced.csv', index=False)
