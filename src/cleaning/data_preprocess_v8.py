import pandas as pd

# ---------------summary ---------------------
# 1. drop job roles that are less than 100
# 2. drop 'Other' job roles


path = "../../data/processed/Data_Preprocess_v7_cleaned.csv"
df = pd.read_csv(path, low_memory=False)

rm = df['Q23_role title'].value_counts()
rm.reset_index()

rmlist = rm[rm < 100].index.tolist()
rmlist.append('Other')
rmlist

# remove the rows with the role title in the rmlist
simplifed_df = df[~df['Q23_role title'].isin(rmlist)]
simplifed_df['Q23_role title'].value_counts()

save_path = "../../data/Data_Preprocess_v8_simplified.csv"

simplifed_df.to_csv(save_path, index=False)