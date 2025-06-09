import jpype.imports
import tools.TetradSearch as ts
import pandas as pd
import os
import sys
import tools.translate as tr
import tools.translate as ptt
import tools.visualize as ptv


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

try:
    jpype.startJVM(classpath=[f"resources/tetrad-current.jar"])
except OSError:
    pass

# Read the appropriate csv file
df = pd.read_csv(os.path.join(fr"R:\RECOVER\SecureStudyData\1726269 Phantom Limb Pain F31\Ecological Momentary Assessment\Survey Responses\{participant_id}\{participant_id}_combineddata2.csv"))

df = df.astype({col: "float64" for col in df.columns})

search = ts.TetradSearch(df)

# Load the knowledge text file that was created
search.load_knowledge(fr"R:\RECOVER\SecureStudyData\1726269 Phantom Limb Pain F31\Ecological Momentary Assessment\Survey Responses\{participant_id}\{participant_id}_knowledge.txt")

# Specify parameters for degenerate gaussian score
search.use_degenerate_gaussian_score(penalty_discount=1, structure_prior=0)
search.use_degenerate_gaussian_test()

search.set_bootstrapping(numberResampling=50, percent_resample_size=90, with_replacement=False,
                         add_original=False, resampling_ensemble=1, seed=413021)

search.run_boss(num_starts=2, use_bes=True, time_lag=0, use_data_order=False)
for i in range(50):
    f = open(fr"R:\RECOVER\SecureStudyData\1726269 Phantom Limb Pain F31\Ecological Momentary Assessment\Survey Responses\{participant_id}\Jackknifing Graphs\{participant_id}_jk{i}.txt",'w')
    f.write(str(search.bootstrap_graph(i)))
    
# Write results to text file
f = open(fr"R:\RECOVER\SecureStudyData\1726269 Phantom Limb Pain F31\Ecological Momentary Assessment\Survey Responses\{participant_id}\{participant_id}_jackknifing.txt",'w')
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

with open(fr"R:\RECOVER\SecureStudyData\1726269 Phantom Limb Pain F31\Ecological Momentary Assessment\Survey Responses\{participant_id}\Test Weather\{participant_id}_jackknifing.txt", 'r') as file:
    lines = file.readlines()
    for line in lines:
        if line[0].isdigit():
            element_node_1 = line.split(" ", 2)
            node_1 = element_node_1[1]
            element_interaction = line.split(" ", 3)
            interaction = element_interaction[2]
            element_node_2 = line.split(" ", 4)
            node_2 = element_node_2[3]
            if '[edge]' in line:
                element_edge = line.split("[edge]:", 1)
                edge = element_edge[1]
                edge_list.append(edge)
            if '[no edge]' in line:
                element_no_edge = line.split("[no edge]:", 1)
                no_edge = element_no_edge[1]
                no_edge_list.append(no_edge)
            else:
                no_edge_list.append(0)
            if '-->' in line:
                element_interaction_1 = line.rsplit('-->', 1)
                interaction_1 = element_interaction_1[1]
                interaction_1_list.append(interaction_1)
            else:
                interaction_1_list.append('N/A')
            if '<--' in line:
                element_interaction_2 = line.split('<--', 1)
                interaction_2 = element_interaction_2[1]
                interaction_2_list.append(interaction_2)
            else:
                interaction_2_list.append('N/A')
            if '---' in line:
                element_interaction_3 = line.rsplit('---', 1)
                interaction_3 = element_interaction_3[1]
                interaction_3_list.append(interaction_3)
            else:
                interaction_3_list.append('N/A')


            node_1_list.append(node_1)
            interaction_list.append(interaction)
            node_2_list.append(node_2)

df_bootstrap = pd.DataFrame()
df_bootstrap = pd.DataFrame(columns = ['Node_1', 'Interaction', 'Node_2','Edge','No_edge','-->','<--','---'])
df_bootstrap['Node_1'] = node_1_list
df_bootstrap['Interaction'] = interaction_list
df_bootstrap['Node_2'] = node_2_list
df_bootstrap['Edge'] = edge_list
df_bootstrap['Edge'] = df_bootstrap['Edge'].str.split('\n').str[0]
df_bootstrap['No_edge'] = no_edge_list
df_bootstrap['No_edge'] = df_bootstrap['No_edge'].str.split(';').str[0]
df_bootstrap['-->'] = interaction_1_list
df_bootstrap['-->'] = df_bootstrap['-->'].str.split(']:').str[1]
df_bootstrap['-->'] = df_bootstrap['-->'].str.split(';').str[0]
df_bootstrap['<--'] = interaction_2_list
df_bootstrap['<--'] = df_bootstrap['<--'].str.split('l]:').str[1]   #???
df_bootstrap['<--'] = df_bootstrap['<--'].str.split(';').str[0]
df_bootstrap['---'] = interaction_3_list
df_bootstrap['---'] = df_bootstrap['---'].str.split(']:').str[1]
df_bootstrap['---'] = df_bootstrap['---'].str.split(';').str[0]

df_bootstrap = df_bootstrap.fillna(0)

df_bootstrap.to_csv(fr"R:\RECOVER\SecureStudyData\1726269 Phantom Limb Pain F31\Ecological Momentary Assessment\Survey Responses\{participant_id}\{participant_id}_jackknifing.csv", index=False, header=True)

# Visualize only the edges where one of the outcome variables is the child
df_bootstrap = pd.read_csv(os.path.join(fr"R:\RECOVER\SecureStudyData\1726269 Phantom Limb Pain F31\Ecological Momentary Assessment\Survey Responses\{participant_id}\{participant_id}_jackknifing.csv"))   
outcomes_to_keep = ['plp_intensity','plp_intensity_before_next_survey']
df_bootstrap_outcome = df_bootstrap[df_bootstrap['Node_2'].isin(outcomes_to_keep)]
df_bootstrap_outcome.to_csv(os.path.join(fr"R:\RECOVER\SecureStudyData\1726269 Phantom Limb Pain F31\Ecological Momentary Assessment\Survey Responses\{participant_id}\{participant_id}_jackknifing_outcomeonly.csv"), index=False, header=True)