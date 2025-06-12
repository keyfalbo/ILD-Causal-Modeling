import pandas as pd
import os
import sys
import numpy as np

input_dir = "Sample-Data"

# Read each saved jackknifing text file. Convert each to csv file.
for i in range(50):
    node_1_list = []
    interaction_list = []
    node_2_list = []
    edge_list = []
    no_edge_list = []
    interaction_1_list = []
    interaction_2_list = []
    interaction_3_list = []
    with open(os.path.join(input_dir, fr"group_jk{i}.txt"), 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line[0].isdigit():
                element_node_1 = line.split(" ", 2)
                node_1 = element_node_1[1]
                element_interaction = line.split(" ", 3)
                interaction = element_interaction[2]
                element_node_2 = line.split(" ", 4)
                node_2 = element_node_2[3]

                node_1_list.append(node_1)
                interaction_list.append(interaction)
                node_2_list.append(node_2)

    df_bootstrap = pd.DataFrame()
    df_bootstrap = pd.DataFrame(columns = ['Node_1', 'Interaction', 'Node_2'])
    df_bootstrap['Node_1'] = node_1_list
    df_bootstrap['Interaction'] = interaction_list
    df_bootstrap['Node_2'] = node_2_list

    df_bootstrap.to_csv(os.path.join(input_dir,fr"group_jk{i}.csv"), index=False, header=True)


# Merge all csv files into a single dataframe
file_path = (fr"CSV graphs")
file_list = os.listdir(file_path)

# Create a dictionary of dataframes. For each file in the file_list, read the csv with that file name, save it to a dataframe, and name the dataframe df_0, df_1, etc.
# Dictionary will contain the names of the dataframes and the data themselves.
# Save the dataframes to a list df_list for merging later.
df_dict = {}
df_list = []
for i, file in enumerate(file_list):
    df = pd.read_csv(os.path.join(fr"CSV graphs\{file}"))
    df_name = f"df_{i}"
    df_dict[df_name] = df
    df_list.append(df)

merged_df = pd.concat(df_list, ignore_index=True)

merged_df.to_csv(os.path.join(input_dir, fr"group_jackknifing_alledges.csv"), index = False, header=True)


### THE FOLLOWING CODE WORKS FOR ALL DIRECTED EDGES. UNDIRECTED EDGES MUST BE DEALT WITH MANUALLY FROM CSV SAVED AFTER RUNNING THIS CODE. ###
merged_df = pd.read_csv(os.path.join(input_dir, fr"group_jackknifing_alledges.csv"))
merged_df['Node_2'] = merged_df['Node_2'].str.replace('\n', '', regex=False)

specific_edges_df = merged_df.groupby(merged_df.columns.tolist(),as_index=False).size()
specific_edges_df['Percent'] = specific_edges_df['size'] / 50
specific_edges_df = specific_edges_df.drop(['size'], axis=1)
specific_edges_df['Node_2'] = specific_edges_df['Node_2'].str.replace('\n', '', regex=False)
specific_edges_df['Combined_Nodes'] = specific_edges_df['Node_1'] + " " + specific_edges_df['Node_2']
specific_edges_df['Reversed_Combined_Nodes'] = specific_edges_df['Node_2'] + " " + specific_edges_df['Node_1']

# For each row, check if the exact string in 'Reversed_Combined_Nodes' is in 'Combined_Nodes' for all rows in dataframe. If it is, return 'True' in 'Match' column.
def find_string_in_any_row(df):
    def check_any_row(row):
        search_string = str(row['Reversed_Combined_Nodes'])
        for other_row in df['Combined_Nodes']:
            if search_string == str(other_row):
                return True
        return False
    df['Match'] = df.apply(check_any_row, axis=1)
    return df
specific_edges_df = find_string_in_any_row(specific_edges_df)

# For each row, check if the exact string in 'Reversed_Combined_Nodes' is in 'Combined_Nodes' for all rows in dataframe. If it is, return the value from 'Percent' column in that other row.
def find_and_sum_percent(df):
    def find_and_sum_percent_helper(row):
        search_string = str(row['Reversed_Combined_Nodes'])
        matching_rows = df[df['Combined_Nodes'] == search_string]
        if not matching_rows.empty:
            return matching_rows['Percent'].sum()
        else:
            return 0
    df['Percent2'] = df.apply(find_and_sum_percent_helper, axis=1)
    return df
specific_edges_df = find_and_sum_percent(specific_edges_df)


specific_edges_df['Edge'] = specific_edges_df['Percent'] + specific_edges_df['Percent2']
specific_edges_df['No_edge'] = 1 - specific_edges_df['Edge']
specific_edges_df['---'] = specific_edges_df['Percent'].where(specific_edges_df['Interaction'] == '---', other = 0) 
specific_edges_df['-->'] = np.where(specific_edges_df['---'] == 0, specific_edges_df['Percent'], '')
specific_edges_df['<--'] = np.where(specific_edges_df['---'] == 0, specific_edges_df['Percent2'], '')

# Find an exact string match between 'Reversed_Combined_Nodes' and 'Combined_Nodes' across all rows.
# Create pairs of matching rows and delete the second row in each pair.
def find_match_remove_second(df):
    rows_to_drop = []
    matched_indices = set()
    for index1, row1 in df.iterrows():
        search_string = str(row1['Reversed_Combined_Nodes'])
        for index2, row2 in df.iterrows():
            if index1 != index2 and search_string == str(row2['Combined_Nodes']):
                if index1 not in matched_indices and index2 not in matched_indices:
                    rows_to_drop.append(index2)
                    matched_indices.add(index1)
                    matched_indices.add(index2)
                    break

    df = df.drop(rows_to_drop)
    df = df.reset_index(drop = True)
    return df
specific_edges_df_dropped = find_match_remove_second(specific_edges_df)

# Save csv file. Manually check for undirected edges and update percentages of corresponding edges accordingly.
specific_edges_df_dropped.to_csv(os.path.join(input_dir, fr"group_jackknifing_merged.csv"), index = False, header=True)