import pandas as pd

def country_income(data):

    # filter the data for the columns needed
    filter_col = ['Q29_yearly compensation_min','Q29_yearly compensation_max', 'year', 'Q4_country']
    data = data[filter_col]

    # drop the rows with missing values and calculate the median income by averaging the min and max
    data.dropna(inplace=True)
    data['Median'] = (data['Q29_yearly compensation_min'] + data['Q29_yearly compensation_max'])/2

    # outliers who earn more than 500000 is filtered out
    median = data[data['Q29_yearly compensation_min']<500000][['Median', 'year', 'Q4_country']]
    median.rename(columns={'Q4_country': 'Country', 'year': 'Year'}, inplace=True)

    # find the top ten countries with the most respondants
    list_of_top10 = median.value_counts('Country')[:11].reset_index()
    list_of_top10 = list_of_top10['Country'].tolist()
    list_of_top10.remove('Other')

    # from the top ten countries, filter the data for the selected countries and years
    median = median[median['Country'].isin(list_of_top10)]
    
    # median = median[median['Year'].isin(range(start, end+1))]
    # median = median[median['Country'].isin(country)]
    # median.rename(columns={'Median': 'Median Income'}, inplace=True)

    return median


