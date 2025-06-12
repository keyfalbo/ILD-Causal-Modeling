import pandas as pd
import sys
from itertools import groupby
import os

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

# Read the appropriate csv file
df = pd.read_csv(os.path.join(input_dir, f"{participant_id}_combineddata1.csv"))   

# Delete columns
df = df.drop(['ExternalReference', 'plp_fallasleep', 'plp_stayasleep', 'plp_yn', 'other_pain_yn', 'activity_yn', 'prosthesis_yn', 'feels_like_k', 'plp_duration',  'plp_interference', 'plp_interference_before_next_survey'], axis = 1)

# Create a list of variables for this participant
variables_list = df.columns.tolist()

# Create variables for survey date, day before survey, and 2 days before survey
df['DateTime'] = df['DateTime'].astype(str)
df['survey_date'] = df['DateTime'].str.split(' ').str[0]
df['survey_date'] = pd.to_datetime(df['survey_date'])
df['survey_yesterday'] = df['survey_date'] - pd.Timedelta(1, unit = 'D')
df['survey_yesterday'] = pd.to_datetime(df['survey_yesterday'])
df['survey_2daysago'] = df['survey_date'] - pd.Timedelta(2, unit = 'D')
df['survey_2daysago'] = pd.to_datetime(df['survey_2daysago'])

# Create new variables. Group each variable by survey_yesterday and find the maximum value.
df['max_activity_duration_today'] = df.groupby('survey_yesterday')['activity_duration'].transform('max')
df['max_activity_intensity_today'] = df.groupby('survey_yesterday')['activity_intensity'].transform('max')
df['max_prosthesis_duration_today'] = df.groupby('survey_yesterday')['prosthesis_duration'].transform('max')
if 'socket_comfort' in variables_list:
    df['avg_socket_comfort_today'] = df.groupby('survey_yesterday')['socket_comfort'].transform('mean')
else:
    pass

# Create variable for maximum yesterday by shifting values from current survey date
df['max_activity_duration_yesterday'] = df['max_activity_duration_today'].shift().where(df.survey_yesterday.eq(df.survey_date.shift()))
df['max_activity_intensity_yesterday'] = df['max_activity_intensity_today'].shift().where(df.survey_yesterday.eq(df.survey_date.shift()))
df['max_prosthesis_duration_yesterday'] = df['max_prosthesis_duration_today'].shift().where(df.survey_yesterday.eq(df.survey_date.shift()))
if 'socket_comfort' in variables_list:
    df['avg_socket_comfort_yesterday'] = df['avg_socket_comfort_today'].shift().where(df.survey_yesterday.eq(df.survey_date.shift()))
else:
    pass

#Carry values forward through the day
df['max_activity_duration_yesterday'] = df.groupby('survey_yesterday')['max_activity_duration_yesterday'].ffill()
df['max_activity_duration_yesterday'] = df.groupby('survey_yesterday')['max_activity_duration_yesterday'].bfill()
df['max_activity_intensity_yesterday'] = df.groupby('survey_yesterday')['max_activity_intensity_yesterday'].ffill()
df['max_activity_intensity_yesterday'] = df.groupby('survey_yesterday')['max_activity_intensity_yesterday'].bfill()
df['max_prosthesis_duration_yesterday'] = df.groupby('survey_yesterday')['max_prosthesis_duration_yesterday'].ffill()
df['max_prosthesis_duration_yesterday'] = df.groupby('survey_yesterday')['max_prosthesis_duration_yesterday'].bfill()
if 'socket_comfort' in variables_list:
    df['avg_socket_comfort_yesterday'] = df.groupby('survey_yesterday')['avg_socket_comfort_yesterday'].ffill()
    df['avg_socket_comfort_yesterday'] = df.groupby('survey_yesterday')['avg_socket_comfort_yesterday'].bfill()
else:
    pass

# Create variable for maximum 2 days ago by shifting values from yesterday
df['max_activity_duration_2daysago'] = df['max_activity_duration_yesterday'].shift().where(df.survey_2daysago.eq(df.survey_yesterday.shift()))
df['max_activity_intensity_2daysago'] = df['max_activity_intensity_yesterday'].shift().where(df.survey_2daysago.eq(df.survey_yesterday.shift()))
df['max_prosthesis_duration_2daysago'] = df['max_prosthesis_duration_yesterday'].shift().where(df.survey_2daysago.eq(df.survey_yesterday.shift()))
if 'socket_comfort' in variables_list:
    df['avg_socket_comfort_2daysago'] = df['avg_socket_comfort_yesterday'].shift().where(df.survey_2daysago.eq(df.survey_yesterday.shift()))
else:
    pass

# Carry values forward through the day
df['max_activity_duration_2daysago'] = df.groupby('survey_2daysago')['max_activity_duration_2daysago'].ffill()
df['max_activity_duration_2daysago'] = df.groupby('survey_2daysago')['max_activity_duration_2daysago'].bfill()
df['max_activity_intensity_2daysago'] = df.groupby('survey_2daysago')['max_activity_intensity_2daysago'].ffill()
df['max_activity_intensity_2daysago'] = df.groupby('survey_2daysago')['max_activity_intensity_2daysago'].bfill()
df['max_prosthesis_duration_2daysago'] = df.groupby('survey_2daysago')['max_prosthesis_duration_2daysago'].ffill()
df['max_prosthesis_duration_2daysago'] = df.groupby('survey_2daysago')['max_prosthesis_duration_2daysago'].bfill()
if 'socket_comfort' in variables_list:
    df['avg_socket_comfort_2daysago'] = df.groupby('survey_2daysago')['avg_socket_comfort_2daysago'].ffill()
    df['avg_socket_comfort_2daysago'] = df.groupby('survey_2daysago')['avg_socket_comfort_2daysago'].bfill()
else:
    pass

# Combine activity duration and activity intensity variables
df['activity_intensity_duration_mult'] = df['activity_intensity'] * df['activity_duration']
df.drop(['activity_intensity', 'activity_duration'], axis=1, inplace=True)
df['max_activity_intensity_duration_today_mult'] = df['max_activity_intensity_today'] * df['max_activity_duration_today']
df.drop(['max_activity_duration_today', 'max_activity_intensity_today'], axis=1, inplace=True)
df['max_activity_intensity_duration_yesterday_mult'] = df['max_activity_intensity_yesterday'] * df['max_activity_duration_yesterday']
df.drop(['max_activity_intensity_yesterday', 'max_activity_duration_yesterday'], axis=1, inplace=True)
df['max_activity_intensity_duration_2daysago_mult'] = df['max_activity_intensity_2daysago'] * df['max_activity_duration_2daysago']
df.drop(['max_activity_intensity_2daysago', 'max_activity_duration_2daysago'], axis=1, inplace=True)

# Create weather variables maximum and minimum yesterday by shifting values from current survey date
df['max_1hr_temp_k_diff_yesterday'] = df['max_1hr_temp_k_diff_today'].shift().where(df.survey_yesterday.eq(df.survey_date.shift()))
df['max_1hr_humidity_pct_diff_yesterday'] = df['max_1hr_humidity_pct_diff_today'].shift().where(df.survey_yesterday.eq(df.survey_date.shift()))
df['max_1hr_pressure_hPa_diff_yesterday'] = df['max_1hr_pressure_hPa_diff_today'].shift().where(df.survey_yesterday.eq(df.survey_date.shift()))

# Carry values forward through the day
df['max_1hr_temp_k_diff_yesterday'] = df.groupby('survey_yesterday')['max_1hr_temp_k_diff_yesterday'].ffill()
df['max_1hr_temp_k_diff_yesterday'] = df.groupby('survey_yesterday')['max_1hr_temp_k_diff_yesterday'].bfill()
df['max_1hr_humidity_pct_diff_yesterday'] = df.groupby('survey_yesterday')['max_1hr_humidity_pct_diff_yesterday'].ffill()
df['max_1hr_humidity_pct_diff_yesterday'] = df.groupby('survey_yesterday')['max_1hr_humidity_pct_diff_yesterday'].bfill()
df['max_1hr_pressure_hPa_diff_yesterday'] = df.groupby('survey_yesterday')['max_1hr_pressure_hPa_diff_yesterday'].ffill()
df['max_1hr_pressure_hPa_diff_yesterday'] = df.groupby('survey_yesterday')['max_1hr_pressure_hPa_diff_yesterday'].bfill()

# Create weather variables maximum and minimum 2 days ago by shifting values from yesterday
df['max_1hr_temp_k_diff_2daysago'] = df['max_1hr_temp_k_diff_yesterday'].shift().where(df.survey_2daysago.eq(df.survey_yesterday.shift()))
df['max_1hr_humidity_pct_diff_2daysago'] = df['max_1hr_humidity_pct_diff_yesterday'].shift().where(df.survey_2daysago.eq(df.survey_yesterday.shift()))
df['max_1hr_pressure_hPa_diff_2daysago'] = df['max_1hr_pressure_hPa_diff_yesterday'].shift().where(df.survey_2daysago.eq(df.survey_yesterday.shift()))

# Carry values forward through the day
df['max_1hr_temp_k_diff_2daysago'] = df.groupby('survey_yesterday')['max_1hr_temp_k_diff_2daysago'].ffill()
df['max_1hr_temp_k_diff_2daysago'] = df.groupby('survey_yesterday')['max_1hr_temp_k_diff_2daysago'].bfill()
df['max_1hr_humidity_pct_diff_2daysago'] = df.groupby('survey_yesterday')['max_1hr_humidity_pct_diff_2daysago'].ffill()
df['max_1hr_humidity_pct_diff_2daysago'] = df.groupby('survey_yesterday')['max_1hr_humidity_pct_diff_2daysago'].bfill()
df['max_1hr_pressure_hPa_diff_2daysago'] = df.groupby('survey_yesterday')['max_1hr_pressure_hPa_diff_2daysago'].ffill()
df['max_1hr_pressure_hPa_diff_2daysago'] = df.groupby('survey_yesterday')['max_1hr_pressure_hPa_diff_2daysago'].bfill()

# Create a list of variables for creation of standard time lags
lag_list = ['plp_intensity', 'other_pain_intensity', 'health', 'happy', 'sad', 'relaxed', 'nervous', 'irritable', 'distressed', 'excited', 'lonely', 
            'temp_k', 'humidity_pct', 'pressure_hPa', 'rain_lasthr_mm', 'snow_lasthr_mm', 
            'plp_intensity_before_next_survey', 'temp_k_before_next_survey', 'humidity_pct_before_next_survey', 'pressure_hPa_before_next_survey',
            'rain_lasthr_mm_before_next_survey', 'snow_lasthr_mm_before_next_survey']

# Create standard time lags for specified variables
for item in lag_list:
    df['lag1_' + item] = df[item].shift(1, axis=0)
    df['lag2_' + item] = df[item].shift(2, axis=0)

df = df.drop(['DateTime', 'survey_date', 'survey_yesterday', 'survey_2daysago'], axis = 1)
df = df.dropna(subset=['max_prosthesis_duration_2daysago'])     

# Find columns with little to no variance (mode of column makes up 95% or more of entire column) and delete (even if the variable is an outcome)
for column in df:
    counts = df[column].value_counts()
    max_count = counts.max()
    count_row = df.shape[0]
    max_pct = max_count/count_row
    if max_pct > 0.95:
        df = df.drop([column], axis=1)
    else:
        pass

# Find columns with little to no variance (mode of column makes up 70% or more of entire column) and delete (unless the variable is an outcome)
outcome_list = ['plp_intensity','plp_intensity_before_next_survey']
for column in df:
    if column not in outcome_list:
        counts = df[column].value_counts()
        max_count = counts.max()
        count_row = df.shape[0]
        max_pct = max_count/count_row
        if max_pct > 0.70:
            df = df.drop([column], axis=1)
        else:
            pass

# Save csv file before standardiaing
df.to_csv(os.path.join(input_dir, f"{participant_id}_combineddata2_before_standardization.csv"), index=False, header=True)

# Standardize all variables
df_std = (df - df.mean()) / df.std()

# Save csv file after standardizing
df_std.to_csv(os.path.join(input_dir, f"{participant_id}_combineddata2.csv"), index=False, header=True)
