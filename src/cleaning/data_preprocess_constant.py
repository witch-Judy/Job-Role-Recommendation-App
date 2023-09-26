"""
Author:     Liao Yueh-Fan
Data:       2023/9/21
Course:     NUS IT5006 Fundamentals of Data Analytics
Project:    Job Role Recommendation App
Function:   Constant for Data Cleaning and Preprocessing
"""
dataColNameMap = {
    "Q1":"time",
    "Q2":"age",
    "Q3":"gender",
    "Q4":"country",
    "Q5":"student or not",
    "Q6":"DS course platform",
    "Q7":"DS helpful platform",
    "Q8":"academic dgree",
    "Q9":"academic publish",
    "Q10":"ML research",
    "Q11":"coding years",
    "Q12":"coding language",
    "Q13":"IDE",
    "Q14":"notebook",
    "Q15":"data visualization lib",
    "Q16":"ML years",
    "Q17":"ML framework",
    "Q18":"ML algo",
    "Q19":"computer vision method",
    "Q20":"NLP method",
    "Q21":"pre-trained model",
    "Q22":"ML model hub",
    "Q23":"role title",
    "Q24":"industry",
    "Q25":"company size",
    "Q26":"DS number",
    "Q27":"ML used in company",
    "Q28":"activities at work",
    "Q29":"yearly compensation",
    "Q30":"ML/CC service spent",
    "Q31":"CC platform",
    "Q32":"best cloud platform",
    "Q33":"CC product",
    "Q34":"data storage product",
    "Q35":"big data product",
    "Q36":"business intelligence tool",
    "Q37":"managed ML product",
    "Q38":"automated ML tool",
    "Q39":"ML model serving product",
    "Q40":"ML model monitoring tool",
    "Q41":"ethical AI product",
    "Q42":"ML model hardware",
    "Q43":"TPU use freq",
    "Q44":"DS media"
}

manualQuestionMap2021 = {
    "Q10": "Q14",
    "Q14": "Q15",
    "Q26": "Q30",
    "Q27": "Q31",
    "Q29": "Q33",
    "Q30": "Q34",
    "Q32": "Q35",
    "Q34": "Q36",
    "Q37": "Q38",
    "Q38": "Q39",
    "Q38": "Q40",
    "Q12": "Q42"
}

manualQuestionMap2020 = {
    "Q10": "Q14",
    "Q14": "Q15",
    "Q25": "Q30",
    "Q26": "Q31",
    "Q27": "Q33",
    "Q29": "Q35",
    "Q31": "Q36",
    "Q33": "Q38",
    "Q35": "Q39",
    "Q35": "Q40",
    "Q12": "Q42"
}

number_col = ["Q29_yearly compensation", "Q30_ML/CC service spent"]
money_col = ["Q29_yearly compensation", "Q30_ML/CC service spent"]
Q29_max_option = ["> 500000", ">1000000"]
Q30_min_option = ["0 (USD)"]
Q30_max_option = ["100000 or more (USD)"]