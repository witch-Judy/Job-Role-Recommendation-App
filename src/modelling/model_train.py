import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, MultiLabelBinarizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import os
import numpy as np
import joblib

# Get the absolute path of the current script
path = "data/processed/Data_Preprocess_v9_reduced.csv"
reduced_data = pd.read_csv(path, low_memory=False)

multi_select_columns = [
    'Q12_coding language',
    'Q13_IDE',
    'Q15_data visualization lib',
    'Q18_ML algo'
    ]

single_select_columns = [
    'Q11_coding years',
    'Q16_ML years',  
    'Q2_age',
    'Q3_gender', 
    'Q4_country', 
    'Q43_TPU use freq',
    'Q8_academic dgree'
    ]

def create_model(reduced_data, multi_select_columns, single_select_columns):
    # Separate features and target variable
    X = reduced_data.drop('Q23_role title', axis=1)  # Assuming 'Q23_role title' is the target variable
    y = reduced_data['Q23_role title']

    # Processing multi-select features
    mlb_encoders = {}
    multi_encoded = []
    for col in multi_select_columns:
        mlb = MultiLabelBinarizer()
        encoded = pd.DataFrame(mlb.fit_transform(X[col].str.split(':')),
                               columns=mlb.classes_,
                               index=X.index)
        multi_encoded.append(encoded)
        mlb_encoders[col] = mlb

    # Processing single-select features
    ohe_encoders = {}
    single_encoded = []
    for col in single_select_columns:
        ohe = OneHotEncoder(sparse=False)
        encoded = pd.DataFrame(ohe.fit_transform(X[[col]]),
                               columns=ohe.get_feature_names_out([col]),
                               index=X.index)
        single_encoded.append(encoded)
        ohe_encoders[col] = ohe

    # Combine all encoded features
    X_encoded = pd.concat(multi_encoded + single_encoded, axis=1)

    # Splitting into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

    # Training the Random Forest model
    rf = RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=42)
    rf.fit(X_train, y_train)

    # Bundle the model and encoders
    model_package = {
        'model': rf,
        'mlb_encoders': mlb_encoders,
        'ohe_encoders': ohe_encoders
    }

    # Save the model and encoders
    joblib.dump(model_package, 'src/modelling/model_and_encoders.joblib')

    # Prediction and evaluation
    y_pred = rf.predict(X_test)
    report = classification_report(y_test, y_pred)
    print('model created')

    return report

report = create_model(reduced_data, multi_select_columns, single_select_columns)

print(report)

