import pandas as pd
import numpy as np
import os

import jpype
import jpype.imports

jpype.startJVM("-Xmx4g", classpath=[f"resources/tetrad-current.jar"])

from testwise_deletion import DG

import edu.cmu.tetrad.data as td
import edu.cmu.tetrad.graph as tg
import edu.cmu.tetrad.search as ts

# Set parameters for BOSS
boss_bes = False
boss_starts = 2
boss_threads = 3

df = pd.read_csv(os.path.join(fr"R:\RECOVER\SecureStudyData\1726269 Phantom Limb Pain F31\Ecological Momentary Assessment\Survey Responses\Group Analysis\group_data.csv"))

# Create knowledge
knowledge = td.Knowledge()

variables_list = df.columns.tolist() 

tier0_list = []
tier1_list = []
tier2_list = []
tier3_potential = ['lag2_plp_intensity_before_next_survey', 'lag2_temp_k_before_next_survey','lag2_humidity_pct_before_next_survey','lag2_pressure_hPa_before_next_survey','lag2_rain_lasthr_mm_before_next_survey']
tier3_list = []
tier4_list = []
tier5_potential = ['lag1_plp_intensity_before_next_survey', 'lag1_temp_k_before_next_survey','lag1_humidity_pct_before_next_survey','lag1_pressure_hPa_before_next_survey','lag1_rain_lasthr_mm_before_next_survey']
tier5_list = []
tier6_list = []
tier7_potential = ['plp_intensity_before_next_survey', 'temp_k_before_next_survey','humidity_pct_before_next_survey','pressure_hPa_before_next_survey','rain_lasthr_mm_before_next_survey', 'morning_before_next_survey', 'evening_before_next_survey']
tier7_list = []
for item in tier3_potential:
    if item in variables_list:
        tier3_list.append(item)
for item in tier5_potential:
    if item in variables_list:
        tier5_list.append(item)
for item in tier7_potential:
    if item in variables_list:
        tier7_list.append(item)

# Add variables to appropriate tiers
for item in variables_list:
    if 'before_next_survey' not in item:
        if '2daysago' in item:
            tier0_list.append(item)
        elif 'last_last' in item:
            tier0_list.append(item)
        elif 'yesterday' in item:
            tier1_list.append(item)
        elif 'last_night' in item:
            tier2_list.append(item)
        elif 'last_sleep_quality' in item:
            tier2_list.append(item)
        elif 'lag2_' in item:
            tier2_list.append(item)
        elif 'lag1_' in item:
            tier4_list.append(item)
        else:
            tier6_list.append(item)
for col in df.columns:
    if col in tier0_list: 
        knowledge.addToTier(0, col)
    elif col in tier1_list:
        knowledge.addToTier(1, col)
    elif col in tier2_list:
        knowledge.addToTier(2, col)
    elif col in tier3_list:
        knowledge.addToTier(3, col)
    elif col in tier4_list:
        knowledge.addToTier(4, col)
    elif col in tier5_list:
        knowledge.addToTier(5, col)
    elif col in tier6_list:
        knowledge.addToTier(6, col)
    else: 
        knowledge.addToTier(7, col)

# Set forbidden edges
weather_list = ['temp_k', 'humidity_pct', 'pressure_hPa', 'rain_lasthr_mm', 'snow_lasthr_mm', 'lag1_temp_k', 'lag1_humidity_pct', 'lag1_pressure_hPa', 'lag1_rain_lasthr_mm', 'lag1_snow_lasthr_mm',
                'lag2_temp_k', 'lag2_humidity_pct', 'lag2_pressure_hPa', 'lag2_rain_lasthr_mm', 'lag2_snow_lasthr_mm', 'temp_k_before_next_survey', 'humidity_pct_before_next_survey', 
                'pressure_hPa_before_next_survey', 'rain_lasthr_mm_before_next_survey', 'snow_lasthr_mm_before_next_survey', 'lag1_temp_k_before_next_survey', 'lag1_humidity_pct_before_next_survey',
                'lag1_pressure_hPa_before_next_survey', 'lag1_rain_lasthr_mm_before_next_survey', 'lag1_snow_lasthr_mm_before_next_survey', 'lag2_temp_k_before_next_survey', 'lag2_humidity_pct_before_next_survey', 
                'lag2_pressure_hPa_before_next_survey', 'lag2_rain_lasthr_mm_before_next_survey', 'lag2_snow_lasthr_mm_before_next_survey', 'max_1hr_temp_k_diff_today', 'max_1hr_temp_k_diff_yesterday', 
                'max_1hr_temp_k_diff_2daysago', 'max_1hr_humidity_pct_diff_today', 'max_1hr_humidity_pct_diff_yesterday', 'max_1hr_humidity_pct_diff_2daysago',
                'max_1hr_pressure_hPa_diff_today', 'max_1hr_pressure_hPa_diff_yesterday','max_1hr_pressure_hPa_diff_2daysago', 'morning', 'evening', 'morning_before_next_survey', 'evening_before_next_survey']   
nonweather_list = []
current_weather_list = []
for item in variables_list:
    if item not in weather_list:
        nonweather_list.append(item)
for item in weather_list:
    if item in variables_list:
        current_weather_list.append(item)
for node1 in nonweather_list:
    for node2 in weather_list:
        knowledge.setForbidden(node1,node2)


reps = 50
freqs = {}

for rep in range(reps):

    resampled = df.sample(frac=0.9, replace=False)
    score = DG(resampled, 1)

    boss = ts.Boss(score)
    boss.setUseBes(boss_bes)
    boss.setNumStarts(boss_starts)
    boss.setNumThreads(boss_threads)
    boss.setUseDataOrder(False)
    boss.setResetAfterBM(False)
    boss.setResetAfterRS(False)
    boss.setVerbose(False)
    boss = ts.PermutationSearch(boss)
    boss.setKnowledge(knowledge)

    graph = boss.search()
    f = open(fr"R:\RECOVER\SecureStudyData\1726269 Phantom Limb Pain F31\Ecological Momentary Assessment\Survey Responses\Group Analysis\Jackknifing Graphs\group_jk{rep}.txt",'w')
    f.write(str(graph.toString()))