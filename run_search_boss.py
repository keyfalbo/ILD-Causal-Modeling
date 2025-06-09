import jpype.imports
import tools.TetradSearch as ts
import pandas as pd
import os
import sys
import tools.translate as tr
import tools.translate as ptt
import tools.visualize as ptv
import semopy as sem
from semopy import Model

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

# Load the knowledge file that was created
search.load_knowledge(fr"R:\RECOVER\SecureStudyData\1726269 Phantom Limb Pain F31\Ecological Momentary Assessment\Survey Responses\{participant_id}\{participant_id}_knowledge.txt")

# Specify parameters for degenerate gaussian score
search.use_degenerate_gaussian_score(penalty_discount=1, structure_prior=0)
search.use_degenerate_gaussian_test()

# Set parameters and run the search
search.run_boss(num_starts=2, use_bes=True, time_lag=0, use_data_order=False)

# Write CPDAG to text file
f = open(fr"R:\RECOVER\SecureStudyData\1726269 Phantom Limb Pain F31\Ecological Momentary Assessment\Survey Responses\{participant_id}\{participant_id}_cpdag.txt",'w')
f.write(str(search.get_string()))

# Write DAG to text file
f = open(fr"R:\RECOVER\SecureStudyData\1726269 Phantom Limb Pain F31\Ecological Momentary Assessment\Survey Responses\{participant_id}\{participant_id}_dag.txt",'w')
f.write(str(search.get_dag_string()))

# Change to lavaan format and write to text file
lavaan_model = search.get_lavaan()
filewrite = open(fr"R:\RECOVER\SecureStudyData\1726269 Phantom Limb Pain F31\Ecological Momentary Assessment\Survey Responses\{participant_id}\{participant_id}_lavaan.txt",'w')
filewrite.write(str(lavaan_model))

# Read the saved lavaan file
with open (fr"R:\RECOVER\SecureStudyData\1726269 Phantom Limb Pain F31\Ecological Momentary Assessment\Survey Responses\{participant_id}\{participant_id}_lavaan.txt",'r') as file:
    lines = file.readlines()
    file_content = ''.join(lines)
components = file_content.split('\n\n')
edges = components[1]

mod = edges
model = Model(mod)
model.fit(df)
stats = sem.calc_stats(model)
stats.to_csv(os.path.join(fr"R:\RECOVER\SecureStudyData\1726269 Phantom Limb Pain F31\Ecological Momentary Assessment\Survey Responses\{participant_id}\{participant_id}_fitstats.csv"), index=False, header=True)

estimates = model.inspect()
estimates.to_csv(os.path.join(fr"R:\RECOVER\SecureStudyData\1726269 Phantom Limb Pain F31\Ecological Momentary Assessment\Survey Responses\{participant_id}\{participant_id}_estimates.csv"), index=False, header=True)

# Visualize only the edges and estimates where one of the outcome variables is the child
df_estimates = pd.read_csv(os.path.join(fr"R:\RECOVER\SecureStudyData\1726269 Phantom Limb Pain F31\Ecological Momentary Assessment\Survey Responses\{participant_id}\{participant_id}_estimates.csv"))   
outcomes_to_keep = ['plp_intensity','plp_intensity_before_next_survey']
df_estimates_outcome = df_estimates[df_estimates['lval'].isin(outcomes_to_keep)]
df_estimates_outcome = df_estimates_outcome.sort_values(by='Estimate', key=abs, ascending=False)
df_estimates_outcome.to_csv(os.path.join(fr"R:\RECOVER\SecureStudyData\1726269 Phantom Limb Pain F31\Ecological Momentary Assessment\Survey Responses\{participant_id}\{participant_id}_estimates_outcomeonly.csv"), index=False, header=True)