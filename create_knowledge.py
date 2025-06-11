import pandas as pd
import sys
import os

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

# Read the appropriate csv file
df = pd.read_csv(os.path.join(input_dir, f"{participant_id}_combineddata2.csv"))

# Create a list of variables for this participant
variables_list = df.columns.tolist()

# Create knowledge tiers
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
        
# Create list of weather variables and non-weather variables
weather_list = ['temp_k', 'humidity_pct', 'pressure_hPa', 'rain_lasthr_mm', 'snow_lasthr_mm', 'lag1_temp_k', 'lag1_humidity_pct', 'lag1_pressure_hPa', 'lag1_rain_lasthr_mm', 'lag1_snow_lasthr_mm',
                'lag2_temp_k', 'lag2_humidity_pct', 'lag2_pressure_hPa', 'lag2_rain_lasthr_mm', 'lag2_snow_lasthr_mm', 'temp_k_before_next_survey', 'humidity_pct_before_next_survey', 
                'pressure_hPa_before_next_survey', 'rain_lasthr_mm_before_next_survey', 'snow_lasthr_mm_before_next_survey', 'lag1_temp_k_before_next_survey', 'lag1_humidity_pct_before_next_survey',
                'lag1_pressure_hPa_before_next_survey', 'lag1_rain_lasthr_mm_before_next_survey', 'lag1_snow_lasthr_mm_before_next_survey', 'lag2_temp_k_before_next_survey', 'lag2_humidity_pct_before_next_survey', 
                'lag2_pressure_hPa_before_next_survey', 'lag2_rain_lasthr_mm_before_next_survey', 'lag2_snow_lasthr_mm_before_next_survey', 'max_1hr_temp_k_diff_today', 'max_1hr_temp_k_diff_yesterday', 
                'max_1hr_temp_k_diff_2daysago', 'max_1hr_humidity_pct_diff_today', 'max_1hr_humidity_pct_diff_yesterday', 'max_1hr_humidity_pct_diff_2daysago',
                'max_1hr_pressure_hPa_diff_today', 'max_1hr_pressure_hPa_diff_yesterday','max_1hr_pressure_hPa_diff_2daysago', 'morning', 'evening', 'morning_before_next_survey', 'evening_before_next_survey']   
nonweather_list = []
currentparticipant_weather_list = []

for item in variables_list:
    if item not in weather_list:
        nonweather_list.append(item)

for item in weather_list:
    if item in variables_list:
        currentparticipant_weather_list.append(item)


# Write text file
f = open(os.path.join(input_dir, f"{participant_id}_knowledge.txt"),'w')

f.write('/knowledge')
f.write('\n')
f.write('addtemporal')
f.write('\n')
f.write('\n')

while True:
    if tier0_list:
        f.write('0  ')
        f.write(' '.join(tier0_list))
        f.write('\n')
        f.write('1  ')
        f.write(' '.join(tier1_list))
        f.write('\n')
        f.write('2  ')
        f.write(' '.join(tier2_list))
        f.write('\n')
        f.write('3  ')
        f.write(' '.join(tier3_list))
        f.write('\n')
        f.write('4  ')
        f.write(' '.join(tier4_list))
        f.write('\n')
        f.write('5  ')
        f.write(' '.join(tier5_list))
        f.write('\n')
        f.write('6  ')
        f.write(' '.join(tier6_list))
        f.write('\n')
        f.write('7  ')
        f.write(' '.join(tier7_list))
    elif tier1_list:
        f.write('0  ')
        f.write(' '.join(tier1_list))
        f.write('\n')
        f.write('1  ')
        f.write(' '.join(tier2_list))
        f.write('\n')
        f.write('2  ')
        f.write(' '.join(tier3_list))
        f.write('\n')
        f.write('3  ')
        f.write(' '.join(tier4_list))
        f.write('\n')
        f.write('4  ')
        f.write(' '.join(tier5_list))
        f.write('\n')
        f.write('5  ')
        f.write(' '.join(tier6_list))
        f.write('\n')
        f.write('6  ')
        f.write(' '.join(tier7_list))
    elif tier2_list:
        f.write('0  ')
        f.write(' '.join(tier2_list))
        f.write('\n')
        f.write('1  ')
        f.write(' '.join(tier3_list))
        f.write('\n')
        f.write('2  ')
        f.write(' '.join(tier4_list))
        f.write('\n')
        f.write('3  ')
        f.write(' '.join(tier5_list))
        f.write('\n')
        f.write('4  ')
        f.write(' '.join(tier6_list))
        f.write('\n')
        f.write('5  ')
        f.write(' '.join(tier7_list))
    elif tier3_list:
        f.write('0  ')
        f.write(' '.join(tier3_list))
        f.write('\n')
        f.write('1  ')
        f.write(' '.join(tier4_list))
        f.write('\n')
        f.write('2  ')
        f.write(' '.join(tier5_list))
        f.write('\n')
        f.write('3  ')
        f.write(' '.join(tier6_list))
    elif tier4_list:
        f.write('0  ')
        f.write(' '.join(tier4_list))
        f.write('\n')
        f.write('1  ')
        f.write(' '.join(tier5_list))
        f.write('\n')
        f.write('2  ')
        f.write(' '.join(tier6_list))
        f.write('\n')
        f.write('3  ')
        f.write(' '.join(tier7_list))
    elif tier5_list:
        f.write('0  ')
        f.write(' '.join(tier5_list))
        f.write('\n')
        f.write('1  ')
        f.write(' '.join(tier6_list))
        f.write('\n')
        f.write('2  ')
        f.write(' '.join(tier7_list))
    else:
        f.write('0  ')
        f.write(' '.join(tier6_list))
        f.write('\n')
        f.write('1  ')
        f.write(' '.join(tier7_list))
        break

    break

f.write('\n')
f.write('\n')
f.write('forbiddirect')
f.write('\n')
for i in nonweather_list:
    for j in currentparticipant_weather_list:
        f.write(i)
        f.write(' ')
        f.write(j)
        f.write('\n')

f.write('\n')
f.write('requiredirect')