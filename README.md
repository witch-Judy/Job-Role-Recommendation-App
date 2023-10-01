# Job-Role-Recommendation-App
This is a web application that analysis job holder profiles and provides profile-based recommendation of job roles in the Data Science and Machine Learning (DSML) sector.

## Development Framework
This project use Streamlit to develop the web app.
## Dataset
This project use combined datasets from Kaggle's Annual Machine Learning and Data Science Survey from the past three years (2020-2022).
## Project Task
### 1. Exploratory data analysis
Build the first version of your app that allows users to visualize and explore the data to derive insights.
#### 1.1 Trend over time
By selected the "Trends" tab, we can observe multiple different topic of trends during 2020 to 2022.
We provide these trends in the drop-down menu to choose from:
 - Popular Job Title
 - Popular Machine Learning Framework
 - Popular Programming Language
#### 1.2 Statistical tendencies
By selected the "Statistics" tab, we can observe several different data statistics over selected years.
We provide these statistics in the drop-down menu to choose from:
 - Income by Country
 - Industry Distribution of Different Age Range
 - Experience vs Salary
 - Gender Distribution

## How to run the Streamlit Web Page?
1. First, Python is required in the local environment
2. Dependency Python Library
   - Data Analytics & Graphing: pandas, matplotlib, seaborn, plotly
   - Front-End: streamlit
   - Other: re, difflib, sys, os, warnings
3. Open the terminal and go to the project directory
4. Enter the following command and press enter
   ```
    python -m streamlit run app/visualize.py
    ```
5. The web page will pop up in your web browser