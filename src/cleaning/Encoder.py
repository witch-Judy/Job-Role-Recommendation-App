import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, MultiLabelBinarizer

# change the path to suit your environment
path = "../../data/processed/Data_Preprocess_v7.csv"
df = pd.read_csv(path, low_memory=False)


mulSelQuestionTitle = ["Q6_DS course platform", "Q12_coding language", "Q13_IDE", "Q14_notebook",
                       "Q15_data visualization lib", "Q17_ML framework", "Q18_ML algo", "Q19_computer vision method", "Q20_NLP method",
                       "Q28_activities at work", "Q31_CC platform", "Q33_CC product", "Q35_big data product", "Q36_business intelligence tool",
                       "Q37_managed ML product", "Q38_automated ML tool", "Q42_ML model hardware", "Q44_DS media"]

sinSelQuestionTitle = ["Q3_gender", "Q8_academic dgree", 'Q4_country', 'Q11_coding years', 'Q23_role title', 'Q27_ML used in company']

numericQuestionTitle = ["Q1_time", 'Q16_ML years_min', 'Q25_company size_min', 'Q26_DS number_min', "Q29_yearly compensation_min", 
                        "Q2_age_min", "Q30_ML/CC service spent_min", "Q43_TPU use freq_min"]


# Custom transformer for multilabel columns
class mulselTransformer():    
    def fit(self, X, y=None):
        self.mlb = MultiLabelBinarizer()
        # Replace NaN with 'None' and split by comma
        encode = [el.split(':') if el == el else ['None'] for el in X]
        self.mlb.fit(encode)
        return self

    def transform(self, X):
        # Replace NaN with 'None' and split by comma
        encode = [el.split(':') if el == el else ['None'] for el in X]
        return self.mlb.transform(encode)
    
    def get_params(self, deep=True):
        return {}

# Define the transformers for each column type
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

# Create a ColumnTransformer with the transformers
preprocessor = ColumnTransformer([
    ('num', 'passthrough', numericQuestionTitle),
    ('cat', categorical_transformer, sinSelQuestionTitle),
    ('Q6', mulselTransformer(), mulSelQuestionTitle[0]),
    ('Q12', mulselTransformer(), mulSelQuestionTitle[1]),
    ('Q13', mulselTransformer(), mulSelQuestionTitle[2]),
    ('Q14', mulselTransformer(), mulSelQuestionTitle[3]),
    ('Q15', mulselTransformer(), mulSelQuestionTitle[4]),
    ('Q17', mulselTransformer(), mulSelQuestionTitle[5]),
    ('Q18', mulselTransformer(), mulSelQuestionTitle[6]),
    ('Q19', mulselTransformer(), mulSelQuestionTitle[7]),
    ('Q20', mulselTransformer(), mulSelQuestionTitle[8]),
    ('Q28', mulselTransformer(), mulSelQuestionTitle[9]),
    ('Q31', mulselTransformer(), mulSelQuestionTitle[10]),
    ('Q33', mulselTransformer(), mulSelQuestionTitle[11]),
    ('Q35', mulselTransformer(), mulSelQuestionTitle[12]),
    ('Q36', mulselTransformer(), mulSelQuestionTitle[13]),
    ('Q37', mulselTransformer(), mulSelQuestionTitle[14]),
    ('Q38', mulselTransformer(), mulSelQuestionTitle[15]),
    ('Q42', mulselTransformer(), mulSelQuestionTitle[16]),
    ('Q44', mulselTransformer(), mulSelQuestionTitle[17]),
])

# Fit and transform the data
preprocessor.fit(df)
X = preprocessor.transform(df)

# change the save paths to suit your environment
save_path = "../../data/processed/Data_Encoded_v1.csv"
encoded = pd.DataFrame(X)
encoded.to_csv(save_path, index=False)
