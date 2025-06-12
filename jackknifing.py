from jvm_debug import start_jvm
import pandas as pd
import os
import sys
# needed to include pytetrad
sys.path.insert(1, os.path.join(os.path.dirname(__file__), "py-tetrad/pytetrad/"))
sys.path.insert(1, os.path.join(os.path.dirname(__file__), "py-tetrad/"))
import tools.TetradSearch as ts
import tools.translate as tr
import tools.translate as ptt
import tools.visualize as ptv
import numpy as np

#Input Directory
input_dir = r"Sample-Data"

# Get participant ID
participant_id = input("What is the participant ID? ")

if participant_id == 'EMA01':
       pass
elif participant_id =='EMA02':
       pass
elif participant_id == 'EMA03':
       pass
elif participant_id == 'EMA04':
    pass
elif participant_id == 'EMA05':
    pass
elif participant_id == 'EMA06':
    pass
elif participant_id == 'EMA07':
    pass
elif participant_id == 'EMA08':
    pass
elif participant_id == 'EMA09':
    pass
elif participant_id == 'EMA10':
    pass
elif participant_id == 'EMA11':
    pass
elif participant_id == 'EMA12':
    pass
elif participant_id == 'EMA13':
    pass
elif participant_id == 'EMA14':
    pass
elif participant_id == 'EMA15':
    pass
elif participant_id == 'EMA16':
    pass
elif participant_id == 'EMA17':
    pass
elif participant_id == 'EMA18':
    pass
elif participant_id == 'EMA19':
    pass
elif participant_id == 'EMA20':
    pass
else:
    print("That is not a valid ID!")
    sys.exit()

def clean_data_for_causal_discovery(df):
    """
    Clean data to avoid comparison method violations in BOSS algorithm
    """
    print("Cleaning data for causal discovery...")
    print(f"Original data shape: {df.shape}")
    
    # Convert to float64 consistently
    df = df.astype({col: "float64" for col in df.columns})
    
    # Handle infinite values
    df = df.replace([np.inf, -np.inf], np.nan)
    
    # Check for problematic values
    nan_counts = df.isna().sum()
    if nan_counts.any():
        print(f"Found NaN values: {nan_counts[nan_counts > 0].to_dict()}")
        # Fill NaN with column medians (more robust than means)
        df = df.fillna(df.median())

    print("Data cleaning complete.")
    return df

# Read and clean the data
try:
    df = pd.read_csv(os.path.join(input_dir, f"{participant_id}_combineddata2.csv"))
    df = clean_data_for_causal_discovery(df)
except Exception as e:
    print(f"Error reading/cleaning data: {e}")
    sys.exit(1)

search = ts.TetradSearch(df)

# Load the knowledge text file that was created
search.load_knowledge(os.path.join(input_dir, f"{participant_id}_knowledge.txt"))

# Specify parameters for degenerate gaussian score
search.use_degenerate_gaussian_score(penalty_discount=1, structure_prior=0)
search.use_degenerate_gaussian_test()

search.set_bootstrapping(numberResampling=50, percent_resample_size=90, with_replacement=False,
                         add_original=False, resampling_ensemble=1, seed=413021)

pc_success = False
while not pc_success:
    try:
        # Try BOSS algorithm first
        search.run_boss(num_starts=2, use_bes=True, time_lag=0, use_data_order=False)
        print("✓ BOSS succeeded!")
        pc_success = True
    except Exception as e:
        print(f"✗ BOSS failed: {e}")
        try:
            # If BOSS fails, try PC
            search.run_pc()
            print("✓ RUN_PC succeeded!")
            pc_success = True
        except Exception as e2:
            print(f"✗ RUN_PC failed: {e2}")
            raise Exception("All causal discovery strategies failed!")

# Create directory if it doesn't exist
jackknife_dir = os.path.join(input_dir, "Jackknifing Graphs")
os.makedirs(jackknife_dir, exist_ok=True)

# Write jackknife files with proper file handling
for i in range(50):
    filepath = os.path.join(jackknife_dir, f"{participant_id}_jk{i}.txt")
    with open(filepath, 'w') as f:
        f.write(str(search.bootstrap_graph(i)))

# Write results to text file with proper file handling
results_filepath = os.path.join(input_dir, f"{participant_id}_jackknifing.txt")
with open(results_filepath, 'w') as f:
    f.write(str(search.get_java()))
# Use text file to create a dataframe and output csv file
node_1_list = []
interaction_list = []
node_2_list = []
edge_list = []
no_edge_list = []
interaction_1_list = []
interaction_2_list = []
interaction_3_list = []
with open(results_filepath, 'r') as file:
    for line in file:
        if line and line[0].isdigit():
            parts = line.split()
            node_1 = parts[1] if len(parts) > 1 else 'N/A'
            interaction = parts[2] if len(parts) > 2 else 'N/A'
            node_2 = parts[3] if len(parts) > 3 else 'N/A'
            node_1_list.append(node_1)
            interaction_list.append(interaction)
            node_2_list.append(node_2)

            edge = line.split("[edge]:", 1)[-1].strip() if '[edge]' in line else '0'
            no_edge = line.split("[no edge]:", 1)[-1].strip() if '[no edge]' in line else '0'
            interaction_1 = line.rsplit('-->', 1)[-1].strip() if '-->' in line else 'N/A'
            interaction_2 = line.split('<--', 1)[-1].strip() if '<--' in line else 'N/A'
            interaction_3 = line.rsplit('---', 1)[-1].strip() if '---' in line else 'N/A'

            edge_list.append(edge)
            no_edge_list.append(no_edge)
            interaction_1_list.append(interaction_1)
            interaction_2_list.append(interaction_2)
            interaction_3_list.append(interaction_3)

# Create DataFrame
df_bootstrap = pd.DataFrame({
    'Node_1': node_1_list,
    'Interaction': interaction_list,
    'Node_2': node_2_list,
    'Edge': edge_list,
    'No_edge': no_edge_list,
    '-->': interaction_1_list,
    '<--': interaction_2_list,
    '---': interaction_3_list,
})

# Safely clean and format the fields
def extract_split(val, split_str, index):
    try:
        return val.split(split_str)[index]
    except Exception:
        return '0'

for col, split_strs in {
    'Edge': ['\n'],
    'No_edge': [';'],
    '-->': [']:',';'],
    '<--': ['l]:',';'],
    '---': [']:',';'],
}.items():
    df_bootstrap[col] = df_bootstrap[col].astype(str)
    for s in split_strs:
        df_bootstrap[col] = df_bootstrap[col].apply(lambda x: extract_split(x, s, 0 if s == ';' else 1))

# Replace missing or failed values
df_bootstrap = df_bootstrap.fillna('0')

# Write full and filtered CSVs
df_bootstrap.to_csv(os.path.join(input_dir, f"{participant_id}_jackknifing.csv"), index=False, header=True)

# Filter for outcome variables
outcomes_to_keep = ['plp_intensity', 'plp_intensity_before_next_survey']
df_bootstrap_outcome = df_bootstrap[df_bootstrap['Node_2'].isin(outcomes_to_keep)]
df_bootstrap_outcome.to_csv(os.path.join(input_dir, f"{participant_id}_jackknifing_outcomeonly.csv"), index=False, header=True)
