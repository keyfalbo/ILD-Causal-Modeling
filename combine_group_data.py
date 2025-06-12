import pandas as pd
import sys
import os

# Read individual participant data files before standardization
file_path = 'Sample-Data'
file_list = os.listdir(file_path)




# Standardize variables within participant and combine data for the group
df_dict = {}
df_list = []
std_df_dict = {}
std_df_list = []
for i, file in enumerate(file_list):
    if file.endswith("combineddata2.csv"):
        df = pd.read_csv(os.path.join(file_path, file))
        std_df = (df - df.mean()) / df.std()
        std_df_name = f"std_df_{i}"
        std_df_dict[std_df_name] = std_df
        std_df_list.append(std_df_name)

std_group_df_all = pd.concat(std_df_dict)
missing_values_all = std_group_df_all.isna().sum()
df_missing_all = pd.DataFrame(missing_values_all)

# Record missing values in a csv file
df_missing_all.to_csv(os.path.join(file_path, "group_missingdata.csv"), index=True, header=False)

# Save combined data for the group
std_group_df_all.to_csv(os.path.join(file_path, "group_data.csv"), index=False, header=True)