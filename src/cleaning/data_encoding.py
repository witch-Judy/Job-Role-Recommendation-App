"""
Author:     Liao Yueh-Fan
Data:       2023/11/8
Course:     NUS IT5006 Fundamentals of Data Analytics
Project:    Job Role Recommendation App
Function:   Functions for Data Encoding
"""
import pandas as pd
import data_encoding_constant as constant

def data_encoding(data):
    # multiple selections question (one question have several columns): change each column's value into 0 and 1
    for df_col in data.columns.values:
        if any(substring in df_col for substring in constant.mulSelQuestionTitle):
            mulSelQuestionEncode(data, df_col)

    # single selection question (one question have one column): remove the column and add one-hot encoding columns
    data = onehotEncoder(data, constant.sinSelQuestionTitle)

    return data

def mulSelQuestionEncode(df, col_name):
    # change the column value that is not blank and null to 1 (ex. Q12: R -> Q12: 1)
    df[col_name].replace(pd.unique(df[df[col_name].notnull()][col_name]), 1, inplace=True)
    # change the column value that is NaN to 0 (ex. Q12: Nan -> Q12: 0)
    df[col_name].replace(pd.unique(df[df[col_name].isnull()][col_name]), 0, inplace=True)


def onehotEncoder(df, columns_to_encode):    
    # Apply one-hot encoding to each column in the list
    for column in columns_to_encode:
        # Check if the column exists in the dataframe
        if column in df.columns:
            # Get one-hot encoding for the column
            encoded_columns = pd.get_dummies(df[column], prefix=column, dtype=int)
            # Drop the original column from the dataframe
            df = df.drop(column, axis=1)
            # Concatenate the new encoded columns to the original dataframe
            df = pd.concat([df, encoded_columns], axis=1)
        else:
            print(f"Column {column} not found in the dataframe.")
    
    return df
