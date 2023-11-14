"""
Author:     Liao Yueh-Fan
Data:       2023/9/21
Course:     NUS IT5006 Fundamentals of Data Analytics
Project:    Job Role Recommendation App
Function:   Functions for Data Cleaning and Preprocessing
"""
import pandas as pd
import numpy as np
import re
import difflib
import data_preprocess_constant as constant

def data_preprocess():
    # route of the data location
    loc = "../../data/raw/"
    # load data: read question part and answer part separately
    question2020, question2021, question2022, data2020, data2021, data2022 = \
        load_data(loc)
    # try to match questions in different year, output 2021 and 2020 question map
    question2020Mul, question2021Mul, question2022Mul, questionMap2021, questionMap2020 = \
        match_question(question2020, question2021, question2022)
    # rename each data column name to specific format (ex. "Q2_age", "Q13_IDE_Jupyter")
    data2022, data2021, data2020 = \
        col_format(data2020, data2021, data2022, question2020Mul, question2021Mul, question2022Mul,
                   questionMap2021, questionMap2020, constant.dataColNameMap)
    # merge three years data
    data = merge_data(data2020, data2021, data2022)
    # add min and max column for columns' value is a range of number
    number_col_addMinMax(data)
    # filter abnormal high educational degree
    filter_abnormal_degree(data)
    # filter abnormal experience (condition: max age - min experience years <= 10)
    filter_abnormal_experience(data)

    # filter student or unemployed answer (only use professional data)
    # filter_unprofessional(data)
    # todo: duration time (Get rid of those who take too long or too short time to complete the questionnaire)

    # classify each column of different type and merge multiple choices question column into one column
    GetColType_MergeQuestion(data)
    # mapping 2020/2021 column value to 2022 since the values are inclusion relationship
    col_value_mapping(data)
    # reorder dataframe columns in alphabetical order
    data = data.reindex(sorted(data.columns), axis=1)

    return data

def load_data(loc):
    # read kaggle csv data from 2020-2022 (question part)
    question2020 = pd.read_csv(loc + "kaggle_survey_2020_responses.csv", nrows=1)
    question2021 = pd.read_csv(loc + "kaggle_survey_2021_responses.csv", nrows=1)
    question2022 = pd.read_csv(loc + "kaggle_survey_2022_responses.csv", nrows=1)
    # label data with year in the first column
    question2020.insert(0, "year", "2020")
    question2021.insert(0, "year", "2021")
    question2022.insert(0, "year", "2022")
    # rename duration time column name
    question2020.rename(columns={"Time from Start to Finish (seconds)": "Q0"}, inplace=True)
    question2021.rename(columns={"Time from Start to Finish (seconds)": "Q0"}, inplace=True)
    question2022.rename(columns={"Duration (in seconds)": "Q1"}, inplace=True)

    # read kaggle csv data from 2020-2022 (answer part)
    data2020 = pd.read_csv(loc + "kaggle_survey_2020_responses.csv", skiprows=[1])
    data2021 = pd.read_csv(loc + "kaggle_survey_2021_responses.csv", skiprows=[1])
    data2022 = pd.read_csv(loc + "kaggle_survey_2022_responses.csv", skiprows=[1])
    # label data with year in the first column
    data2020.insert(0, "year", "2020")
    data2021.insert(0, "year", "2021")
    data2022.insert(0, "year", "2022")
    # rename duration time column name
    data2020.rename(columns={"Time from Start to Finish (seconds)": "Q0"}, inplace=True)
    data2021.rename(columns={"Time from Start to Finish (seconds)": "Q0"}, inplace=True)
    data2022.rename(columns={"Duration (in seconds)": "Q1"}, inplace=True)

    return question2020, question2021, question2022, data2020, data2021, data2022
def match_question(question2020, question2021, question2022):
    # collect question number contains "_B" (for now we just take _A)
    question2020colB = getColWithStr(question2020, "_B")
    question2021colB = getColWithStr(question2021, "_B")

    # delete question number contains "_B"
    delColWithColName(question2020, question2020colB)
    delColWithColName(question2021, question2021colB)

    # collect question number contains "_" (filter multiple choices questions)
    question2020colMul = getColWithStr(question2020, "_")
    question2021colMul = getColWithStr(question2021, "_")
    question2022colMul = getColWithStr(question2022, "_")
    question2020Mul = pd.DataFrame()
    question2021Mul = pd.DataFrame()
    question2022Mul = pd.DataFrame()

    # pop multiple choices question column to another DataFrame, and rewrite the origin question number/statement
    question2020, question2020Mul = popMulChoiceQuestion(question2020, question2020colMul, question2020Mul)
    question2021, question2021Mul = popMulChoiceQuestion(question2021, question2021colMul, question2021Mul)
    question2022, question2022Mul = popMulChoiceQuestion(question2022, question2022colMul, question2022Mul)

    # match question map for 2021 and 2020 {key=QTitle_2021, value=QTitle_2022}
    questionMap2021 = {}
    questionMap2020 = {}

    # loop all the question in 2022 data and find the most similar question in 2021 data (save in questionMap2021)
    for i in question2022:
        maxRatio = 0
        for j in question2021:
            diffRatio = difflib.SequenceMatcher(a=question2022[i][0].lower(), b=question2021[j][0].lower()).ratio()
            if (maxRatio <= diffRatio and diffRatio > 0.9):
                maxRatio = diffRatio
                questionMap2021[j] = i
    # loop all the question in 2022 data and find the most similar question in 2020 data (save in questionMap2020)
    for i in question2022:
        maxRatio = 0
        for j in question2020:
            diffRatio = difflib.SequenceMatcher(a=question2022[i][0].lower(), b=question2020[j][0].lower()).ratio()
            if (maxRatio <= diffRatio and diffRatio > 0.9):
                maxRatio = diffRatio
                questionMap2020[j] = i

    # manually match the question that can not be automatically match through string comparison method (2021 <->2022)
    for key in constant.manualQuestionMap2021:
        questionMap2021[key] = constant.manualQuestionMap2021[key]

    # manually match the question that can not be automatically match through string comparison method (2020 <->2022)
    for key in constant.manualQuestionMap2020:
        questionMap2020[key] = constant.manualQuestionMap2020[key]

    return question2020Mul, question2021Mul, question2022Mul, questionMap2021, questionMap2020

def delColWithColName(df, colArr):
    # drop specific column name in dataframe (colArr is column name array)
    for col in range(len(colArr)):
        del df[colArr[col]]

def getColWithStr(df, str):
    # go through all the column in dataframe and find column name with 'str' (reutrn columns' name array)
    dfColArr = []
    for col in range(len(df.columns)):
        if str in df.columns.values[col]:
            dfColArr.append(df.columns.values[col])
    return dfColArr

def popMulChoiceQuestion(df, colArr, df_mul):
    # find all the multiple choices question in dataframe and pop to another dataframe(df_mul)
    for col in range(len(colArr)):
        if re.search("_1$", colArr[col]):
            df_mul[colArr[col]] = df[colArr[col]]
            df.update(pd.DataFrame({colArr[col]: [df[colArr[col]][0].split("-", 1)[0].strip()]}))
            df.rename(columns={colArr[col]: colArr[col].split("_", 1)[0]}, inplace=True)
        else:
            df_mul[colArr[col]] = df.pop(colArr[col])
    return df, df_mul
def col_format(data2020, data2021, data2022, question2020Mul, question2021Mul, question2022Mul,
               questionMap2021, questionMap2020, dataColNameMap):
    # get all the questions' column name that can be found in 3 dataset
    renameColArr2022 = []
    for ele in dataColNameMap.keys():
        if ele in questionMap2021.values() and ele in questionMap2020.values():
            renameColArr2022.append(ele)

    # rename data 2022 column name to specific format
    for col in data2022:
        if col in dataColNameMap and col in renameColArr2022:
            # rename columns name to "Q1_time"
            data2022.rename(columns={col: col + "_" + dataColNameMap[col]}, inplace=True)
        elif "_" in col:
            questionNum = col.split("_", 1)[0]
            if questionNum in renameColArr2022:
                shortStatement = dataColNameMap[questionNum]
                if " - Selected Choice - " in question2022Mul[col][0]:
                    choice = question2022Mul[col][0].split("- Selected Choice -")[-1].strip()
                else:
                    choice = question2022Mul[col][0].split("-")[-1].strip()
                # if choice statement contains "(xxxx)" we delete it
                if "(" in choice:
                    choice = choice.split("(")[0].strip()
                # update multiple choices question not empty cell value to 1
                # data2022[col] = data2022[col].replace(pd.unique(data2022[data2022[col].notnull()][col]), 1)
                # rename columns name to "Q12_coding language_Python"
                data2022.rename(columns={col: questionNum + "_" + shortStatement + "_" + choice}, inplace=True)

    # rename data 2021 column name to specific format
    for col in data2021:
        if "_B" in col:
            # remove not useful column
            del data2021[col]
            continue
        # question find a match (2022 <-> 2021)
        if col in questionMap2021:
            col2022 = questionMap2021[col]
            if col2022 in dataColNameMap and col2022 in renameColArr2022:
                # rename columns name to "Q1_time"
                data2021.rename(columns={col: col2022 + "_" + dataColNameMap[col2022]}, inplace=True)
        if "_" in col:
            questionNum = col.split("_", 1)[0]
            if questionNum in questionMap2021:
                questionNum2022 = questionMap2021[questionNum]
                if questionNum2022 in renameColArr2022:
                    shortStatement = dataColNameMap[questionNum2022]
                    choice = question2021Mul[col][0].split("- Selected Choice -")[-1].strip()
                    if "(" in choice:
                        # if choice statement contains "(xxxx)" we delete it
                        choice = choice.split("(")[0].strip()

                    # update multiple choices question not empty cell value to 1
                    # data2021[col] = data2021[col].replace(pd.unique(data2021[data2021[col].notnull()][col]), 1)
                    # rename columns name to "Q12_coding language_Python"
                    data2021.rename(columns={col: questionNum2022 + "_" + shortStatement + "_" + choice}, inplace=True)

    # rename data 2020 column name to specific format
    for col in data2020:
        if "_B" in col:
            # remove not useful column
            del data2020[col]
            continue
        # question find a match (2022 <-> 2020)
        if col in questionMap2020:
            col2022 = questionMap2020[col]
            if col2022 in dataColNameMap and col2022 in renameColArr2022:
                data2020.rename(columns={col: col2022 + "_" + dataColNameMap[col2022]}, inplace=True)
        if "_" in col:
            questionNum = col.split("_", 1)[0]
            if questionNum in questionMap2020:
                questionNum2022 = questionMap2020[questionNum]
                if questionNum2022 in renameColArr2022:
                    shortStatement = dataColNameMap[questionNum2022]
                    choice = question2020Mul[col][0].split("- Selected Choice -")[-1].strip()
                    if "(" in choice:
                        choice = choice.split("(")[0].strip()

                    # update multiple choices question not empty cell value to 1
                    # data2020[col] = data2020[col].replace(pd.unique(data2020[data2020[col].notnull()][col]), 1)
                    # rename columns name to "Q12_coding language_Python"
                    data2020.rename(columns={col: questionNum2022 + "_" + shortStatement + "_" + choice}, inplace=True)

    return data2022, data2021, data2020

def merge_data(data2020, data2021, data2022):
    # merge three years dataset together
    data = pd.concat([data2020, data2021, data2022], ignore_index=True)
    return data

def number_col_addMinMax(data):
    # add new column for columns about "number": _min and _max (category: money)
    for i in range(len(constant.number_col)):
        data[constant.number_col[i]+"_min"] = data.loc[:, constant.number_col[i]]
        data[constant.number_col[i]+"_max"] = data.loc[:, constant.number_col[i]]

    # delete dollar sign and thousandths (ex. $1,000 => 1000)
    for i in range(len(constant.money_col)):
        data[constant.money_col[i]+"_min"].replace(["\$", ","], "", inplace=True, regex=True)
        data[constant.money_col[i]+"_max"].replace(["\$", ","], "", inplace=True, regex=True)

    # delete "year" and "years" (ex. 2-5 years => 2-5)
    for i in range(len(constant.year_col)):
        data[constant.year_col[i]+"_min"].replace([" (year.|year)"], "", inplace=True, regex=True)
        data[constant.year_col[i]+"_max"].replace([" (year.|year)"], "", inplace=True, regex=True)

    # delete "employees" and thousandths
    for i in range(len(constant.employee_col)):
        data[constant.employee_col[i]+"_min"].replace([" employees", ","], "", inplace=True, regex=True)
        data[constant.employee_col[i]+"_max"].replace([" employees", ","], "", inplace=True, regex=True)

    # delete "times"
    for i in range(len(constant.freq_col)):
        data[constant.freq_col[i]+"_min"].replace([" times"], "", inplace=True, regex=True)
        data[constant.freq_col[i]+"_max"].replace([" times"], "", inplace=True, regex=True)

    # use dash sign to find the min value and max value of the range (ex. 0-999 => min=0;max=999;)
    for i in range(len(constant.number_col)):
        data[constant.number_col[i]+"_min"].replace("-[0-9]+", "", inplace=True, regex=True)
        data[constant.number_col[i]+"_max"].replace("[0-9]+-", "", inplace=True, regex=True)

    # handle irregular edgy case for Q2
    data["Q2_age_min"].replace("\+", "", inplace=True, regex=True)
    data["Q2_age_max"].replace(constant.Q2_max_option, "inf", inplace=True)

    # handle irregular edgy case for Q29
    data["Q29_yearly compensation_min"].replace(">", "", inplace=True, regex=True)
    data["Q29_yearly compensation_min"] = data["Q29_yearly compensation_min"].str.strip()
    data["Q29_yearly compensation_max"].replace(constant.Q29_max_option, "inf", inplace=True)

    # handle irregular edgy case for Q30
    data["Q30_ML/CC service spent_min"].replace(constant.Q30_min_option, "0", inplace=True)
    data["Q30_ML/CC service spent_min"].replace(constant.Q30_max_option, "100000", inplace=True)
    data["Q30_ML/CC service spent_max"].replace(constant.Q30_min_option, "0", inplace=True)
    data["Q30_ML/CC service spent_max"].replace(constant.Q30_max_option, "inf", inplace=True)

    # handle irregular edgy case for Q11
    data["Q11_coding years_min"].replace("\+", "", inplace=True, regex=True)
    data["Q11_coding years_min"].replace(constant.Q11_min_option, "0", inplace=True)
    data["Q11_coding years_min"].replace(constant.Q11_none_option, "0", inplace=True)
    data["Q11_coding years_max"].replace("< ", "", inplace=True, regex=True)
    data["Q11_coding years_max"].replace(constant.Q11_max_option, "inf", inplace=True)
    data["Q11_coding years_max"].replace(constant.Q11_none_option, "0", inplace=True)

    # handle irregular edgy case for Q16
    data["Q16_ML years_min"].replace(" or more", "", inplace=True, regex=True)
    data["Q16_ML years_min"].replace(constant.Q16_min_option, "0", inplace=True)
    data["Q16_ML years_min"].replace(constant.Q16_none_option, "0", inplace=True)
    data["Q16_ML years_max"].replace("Under ", "", inplace=True, regex=True)
    data["Q16_ML years_max"].replace(constant.Q16_max_option, "inf", inplace=True)
    data["Q16_ML years_max"].replace(constant.Q16_none_option, "0", inplace=True)

    # handle irregular edgy case for Q25
    data["Q25_company size_min"].replace(" or more", "", inplace=True, regex=True)
    data["Q25_company size_max"].replace(constant.Q25_max_option, "inf", inplace=True)

    # handle irregular edgy case for Q26
    data["Q26_DS number_min"].replace("\+", "", inplace=True, regex=True)
    data["Q26_DS number_max"].replace(constant.Q26_max_option, "inf", inplace=True)

    # handle irregular edgy case for Q43
    data["Q43_TPU use freq_min"].replace("More than ", "", inplace=True, regex=True)
    data["Q43_TPU use freq_min"].replace(constant.Q43_min_option, "1", inplace=True)
    data["Q43_TPU use freq_min"].replace(constant.Q43_none_option, "0", inplace=True)
    data["Q43_TPU use freq_max"].replace(constant.Q43_min_option, "1", inplace=True)
    data["Q43_TPU use freq_max"].replace(constant.Q43_max_option, "inf", inplace=True)
    data["Q43_TPU use freq_max"].replace(constant.Q43_none_option, "0", inplace=True)

def filter_unprofessional(data):
    # remove students
    data = data[data["Q5_student or not"] != 'No']
    # remove students and currently not employed
    data = data[data["Q23_role title"] != 'Currently not employed']
    data = data[data["Q23_role title"] != 'Student']

def filter_abnormal_experience(data):
    # first we get the row index of age and experience years that cells value are not inf
    non_inf_data = data[["Q2_age_max", "Q11_coding years_min"]].ne('inf').all(axis=1)
    # subtract age and years
    age_sub_year = data.loc[non_inf_data, ["Q2_age_max"]].astype(float)["Q2_age_max"] - \
                   data.loc[non_inf_data, ["Q11_coding years_min"]].astype(float)["Q11_coding years_min"]
    # drop the row with abnormal experience (max age - min coding years <= 10)
    data.drop(data.loc[age_sub_year[age_sub_year <= 10].index].index, inplace=True)

    # first we get the row index of age and experience years that cells value are not inf
    non_inf_data = data[["Q2_age_max", "Q16_ML years_min"]].ne('inf').all(axis=1)
    # subtract age and years
    age_sub_year = data.loc[non_inf_data, ["Q2_age_max"]].astype(float)["Q2_age_max"] - \
                   data.loc[non_inf_data, ["Q16_ML years_min"]].astype(float)["Q16_ML years_min"]
    # drop the row with abnormal experience (max age - min ML years <= 10)
    data.drop(data.loc[age_sub_year[age_sub_year <= 10].index].index, inplace=True)

def filter_abnormal_degree(data):
    doctor_data = data[["Q8_academic dgree"]].isin(["Professional doctorate", "Doctoral degree"]).all(axis=1)
    doctor_age = data.loc[doctor_data, ["Q2_age_min"]].astype(float)
    data.drop(data.loc[doctor_age[doctor_age["Q2_age_min"]<=20].index].index, inplace=True)

def GetColType_MergeQuestion(data):
    """
    This function is used to get the type of each column and merge the same question columns' value into one column
    """
    # loop all the columns
    for col in data.columns.values:
        if len([x for x in constant.dataColNameMap.values() if x in col]) == 0 and col != "year":
            del data[col]
            continue
        # if the column name contains no "_" or 1 "_", then it is a categorical variable or a numerical variable
        if len([ch for ch in col if ch=="_"]) <= 1:
            # determine the type of variable by checking the column type
            if (data[col].dtypes == "float64" or data[col].dtypes == "int64"):
                constant.num_col.add(col)
            if (data[col].dtypes == "object"):
                constant.single_choice_col.add(col)
        # if the column name contains 2 "_" and no "min/max", then it is a categorical variable with multiple values
        if len([ch for ch in col if ch=="_"]) == 2:
            if "min" not in col and "max" not in col:
                new_col = col.split("_")[0]+"_"+col.split("_")[1]
                constant.multi_choice_col.add(new_col)
                # merge the same question columns' value into one column "value1:value2:value3"
                if new_col not in data.columns.values:
                    # if the question name is not in the dataframe, create a new column
                    data[new_col] = np.where(data[col].isnull(), "", data[col].astype(str).apply(lambda x: x.strip()))
                else:
                    # if the question name is already in the dataframe, merge the value
                    data[new_col] = data[new_col].astype(str) + np.where(data[col].isnull(), "", np.where(data[new_col]=="", data[col], ":"+data[col].astype(str).apply(lambda x: x.strip()))).astype(str)
                # delete the original column
                del data[col]
            # if the column name contains 2 "_" and "min/max", then it is a numerical variable
            elif "min" in col and "max" in col:
                constant.num_col.add(col)
    return data

def col_value_mapping(data):
    # map 2020/2021 job role title to 2022 dataset
    data["Q23_role title"].replace(constant.Q23_role_title_map, inplace=True)