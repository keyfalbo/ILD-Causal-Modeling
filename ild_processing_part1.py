import pandas as pd
import sys
from itertools import groupby
import os
from statistics import mean
from datetime import datetime
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


# Get participant time zone
time_zone = input("What time zone does the participant live in? ")

if time_zone == 'EST':
       pass
elif time_zone =='CST':
       pass
elif time_zone == 'MST':
       pass
elif time_zone == 'PST':
    pass
else:
    print("That is not a valid time zone!")
    sys.exit()



########### MORNING SURVEY PROCESSING ###########
df_morning = pd.read_csv(os.path.join(input_dir,"Morning.csv")) # Read the appropriate csv file

# Clean dataframe and keep only data from specific participant
df_morning = df_morning.drop([0,1], axis=0)
df_morning = df_morning[df_morning['ExternalReference'].str.contains(participant_id) == True]
df_morning['ExternalReference'] = df_morning['ExternalReference'].str.rsplit('M', n=1).str[0]
df_morning = df_morning.drop(['EndDate', 'Status', 'IPAddress', 'Progress', 'Duration (in seconds)', 'Finished', 'RecordedDate', 'ResponseId', 'RecipientLastName', 
                              'RecipientFirstName', 'RecipientEmail', 'LocationLatitude', 'LocationLongitude','DistributionChannel',
                              'UserLanguage', 'Q27'], axis = 1)

# Select columns for unreported pain and create new dataframe with only these columns
df_morning2 = df_morning[['StartDate','Q22', 'Q28_1', 'Q28_2', 'Q28_3', 'Q30', 'Q31_1', 'Q31_2', 'Q32']] 
df_morning = df_morning.drop(['Q22', 'Q28_1', 'Q28_2', 'Q28_3', 'Q30', 'Q31_1', 'Q31_2', 'Q32'], axis = 1)

# Rename columns to variable names
df_morning = df_morning.rename(columns = {'StartDate':'DateTime', 'Q1_1':'sleep_time1','Q1_2':'sleep_time2', 'Q9_1':'wake_time1', 'Q9_2':'wake_time2', 'Q38':'last_sleep_quality', 'Q10':'plp_fallasleep', 
                                          'Q21':'plp_stayasleep', 'Q6_1':'shrinker_hrs', 'Q6_2':'shrinker_mins', 'Q7':'plp_yn', 'Q8':'plp_intensity', 'Q12_1':'plp_hrs', 
                                          'Q12_2':'plp_mins','Q39':'plp_interference', 'Q13':'other_pain_yn', 'Q14':'other_pain_intensity', 'Q33':'restroom', 'Q34':'health', 
                                          'Q37':'happy', 'Q47':'sad', 'Q48':'relaxed', 'Q49':'nervous', 'Q50':'irritable', 'Q51':'distressed', 'Q52':'excited', 'Q53':'lonely'})

# Change DateTime to reflect participant time zone
df_morning['DateTime'] = pd.to_datetime(df_morning['DateTime'])
if time_zone == 'EST':
        df_morning['DateTime'] = df_morning['DateTime'] + pd.Timedelta(1, unit = 'h')
elif time_zone =='CST':
        df_morning['DateTime'] = df_morning['DateTime']
elif time_zone == 'MST':
        df_morning['DateTime'] = df_morning['DateTime'] - pd.Timedelta(1, unit = 'h')
elif time_zone =='PST':
        df_morning['DateTime'] = df_morning['DateTime'] - pd.Timedelta(2, unit = 'h')

df_morning['DateTime'] = df_morning['DateTime'].astype(str)

# Replace missing values of specified columns with zeros
df_morning['shrinker_hrs'] = df_morning['shrinker_hrs'].fillna(0)
df_morning['shrinker_mins'] = df_morning['shrinker_mins'].fillna(0)
df_morning['plp_intensity'] = df_morning['plp_intensity'].fillna(0)
df_morning['plp_hrs'] = df_morning['plp_hrs'].fillna(0)
df_morning['plp_mins'] = df_morning['plp_mins'].fillna(0)
df_morning['plp_interference'] = df_morning['plp_interference'].fillna(0)
df_morning['other_pain_intensity'] = df_morning['other_pain_intensity'].fillna(0)

# Calculate last nights sleep
df_morning['survey_date'] = df_morning['DateTime'].str.split(' ').str[0]
df_morning['survey_date'] = pd.to_datetime(df_morning['survey_date'])
df_morning['survey_yesterday'] = df_morning['survey_date'] - pd.Timedelta(1, unit = 'D')
df_morning['survey_yesterday'] = pd.to_datetime(df_morning['survey_yesterday'])

df_morning['sleep_time1'] = df_morning['sleep_time1'].str.split(':').str[0]
df_morning['sleep_time1'] = df_morning['sleep_time1'].str.replace('Earlier than 7', '7')
df_morning['sleep_time1'] = df_morning['sleep_time1'].str.replace('Later than 3', '4')
df_morning['sleep_time1'] = df_morning['sleep_time1'].str.replace('12', '0')
df_morning['sleep_time1'] = df_morning['sleep_time1'].astype(int)
df_morning['sleep_time3'] = df_morning['sleep_time1'].where(df_morning['sleep_time1'] < 6, other = (df_morning['sleep_time1'] + 12))
df_morning['sleep_time2'] = df_morning['sleep_time2'].fillna(':00')
df_morning['sleep_time'] = df_morning['sleep_time3'].astype(str) + df_morning['sleep_time2']
df_morning['sleep_datetime'] = (df_morning['survey_yesterday'].astype(str) + ' ' + df_morning['sleep_time']).where(df_morning['sleep_time3'] > 18, 
                                                                                                                   other = (df_morning['survey_date'].astype(str) + ' ' + df_morning['sleep_time']))
df_morning['sleep_datetime'] = pd.to_datetime(df_morning['sleep_datetime'])     # Convert to datetime format

df_morning['wake_time1'] = df_morning['wake_time1'].str.split(':').str[0]
df_morning['wake_time1'] = df_morning['wake_time1'].str.replace('Earlier than 3', '3')
df_morning['wake_time1'] = df_morning['wake_time1'].str.replace('Later than 12', '13')
df_morning['wake_time2'] = df_morning['wake_time2'].fillna(':00')
df_morning['wake_time'] = df_morning['wake_time1'].astype(str) + df_morning['wake_time2']
df_morning['wake_datetime'] = df_morning['survey_date'].astype(str) + ' ' + df_morning['wake_time']
df_morning['wake_datetime'] = pd.to_datetime(df_morning['wake_datetime'])

df_morning['last_nights_sleep'] = (df_morning['wake_datetime'] - df_morning['sleep_datetime']) / pd.Timedelta(hours = 1)

df_morning = df_morning.drop(['sleep_time1', 'sleep_time2', 'sleep_time3', 'sleep_time', 'sleep_datetime', 'wake_time1', 'wake_time2', 'wake_time', 'wake_datetime' ,'survey_date', 'survey_yesterday'], axis=1)

# Calculate duration of wearing shrinker last night
df_morning['shrinker_hrs'] = df_morning['shrinker_hrs'].str.replace('13 hours or more', '13')
df_morning['shrinker_hrs'] = df_morning['shrinker_hrs'].astype(int)
df_morning['shrinker_mins'] = df_morning['shrinker_mins'].astype(int)
df_morning['shrinker_hrs'] = df_morning['shrinker_hrs']*60
df_morning['shrinker_duration_last_night'] = df_morning['shrinker_hrs'] + df_morning['shrinker_mins']
df_morning = df_morning.drop(['shrinker_hrs', 'shrinker_mins'], axis=1)

# Calculate duration of PLP
df_morning = df_morning.replace(['13 hours or more'], ['13'])
df_morning = df_morning.replace(['1 minute or less'], ['1'])
df_morning['plp_hrs'] = df_morning['plp_hrs'].astype(int)
df_morning['plp_mins'] = df_morning['plp_mins'].astype(int)
df_morning['plp_hrs'] = df_morning['plp_hrs']*60
df_morning['plp_duration'] = df_morning['plp_hrs'] + df_morning['plp_mins']
df_morning = df_morning.drop(['plp_hrs', 'plp_mins'], axis=1)

# Replace descriptors with number values
df_morning = df_morning.replace(['(1) Very poor', '(2) Poor', '(3) Fair', '(4) Good', '(5) Very good'], ['1', '2', '3', '4', '5'])
df_morning = df_morning.replace(['(1) Not at all', '(2) A little bit', '(3) Somewhat', '(4) Quite a bit', '(5) Very much'], ['1', '2', '3', '4', '5'])
df_morning = df_morning.replace(['(1) Poor', '(2) Fair', '(3) Good', '(4) Very good', '(5) Excellent'], ['1', '2', '3', '4', '5'])
df_morning = df_morning.replace(['(1) Very slightly or not at all', '(2) A little', '(3) Moderately', '(4) Quite a bit', '(5) Extremely'], ['1', '2', '3', '4', '5'])
df_morning = df_morning.replace(['0 (no pain)', '10 (worst pain imaginable)'], ['0', '10'])
df_morning = df_morning.replace(['No', 'Yes'], ['0', '1'])

df_morning['activity_yn'] = 0
df_morning['activity_duration'] = 0
df_morning['activity_intensity'] = 0
df_morning['prosthesis_yn'] = 0
df_morning['prosthesis_duration'] = 0
df_morning['remove_prosthesis'] = 0
df_morning['morning'] = 1       # Add indicator for time of day
df_morning['evening'] = 0



########### AFTERNOON SURVEY PROCESSING ###########
df_afternoon = pd.read_csv(os.path.join(input_dir,"Afternoon.csv")) # Read the appropriate csv file

# Clean dataframe and keep only data from specific participant
df_afternoon = df_afternoon.drop([0,1], axis=0)
df_afternoon = df_afternoon[df_afternoon['ExternalReference'].str.contains(participant_id) == True]
df_afternoon['ExternalReference'] = df_afternoon['ExternalReference'].str.rsplit('A', n=1).str[0]
df_afternoon = df_afternoon.drop(['EndDate', 'Status', 'IPAddress', 'Progress', 'Duration (in seconds)', 'Finished', 'RecordedDate', 'ResponseId', 'RecipientLastName', 
                                      'RecipientFirstName', 'RecipientEmail', 'LocationLatitude', 'LocationLongitude','DistributionChannel',
                                     'UserLanguage', 'Q26'], 
                                      axis = 1)

# Select columns for unreported pain and create new dataframe with only these columns
df_afternoon2 = df_afternoon[['StartDate','Q21', 'Q27_1', 'Q27_2', 'Q27_3', 'Q28', 'Q29_1', 'Q29_2', 'Q30']] 
df_afternoon = df_afternoon.drop(['Q21', 'Q27_1', 'Q27_2', 'Q27_3', 'Q28', 'Q29_1', 'Q29_2', 'Q30'], axis = 1)

# Rename columns to variable names
df_afternoon = df_afternoon.rename(columns = {'StartDate':'DateTime', 'Q7':'plp_yn', 'Q8':'plp_intensity', 'Q12_1':'plp_hrs', 'Q12_2':'plp_mins', 'Q20':'plp_interference', 'Q13':'other_pain_yn', 
                                              'Q14':'other_pain_intensity', 'Q20.1':'activity_yn', 'Q6':'activity_duration', 'Q36':'activity_intensity', 'Q21.1':'prosthesis_yn', 
                                              'Q22':'prosthesis_duration', 'Q33':'socket_comfort', 'Q31':'remove_prosthesis', 'Q32':'restroom', 'Q34':'health', 'Q37':'happy', 
                                              'Q47':'sad', 'Q48':'relaxed', 'Q49':'nervous', 'Q50':'irritable', 'Q51':'distressed', 'Q52':'excited', 'Q53':'lonely'})

# Change DateTime to reflect participant time zone
df_afternoon['DateTime'] = pd.to_datetime(df_afternoon['DateTime'])
if time_zone == 'EST':
        df_afternoon['DateTime'] = df_afternoon['DateTime'] + pd.Timedelta(1, unit = 'h')
elif time_zone =='CST':
        df_afternoon['DateTime'] = df_afternoon['DateTime']
elif time_zone == 'MST':
        df_afternoon['DateTime'] = df_afternoon['DateTime'] - pd.Timedelta(1, unit = 'h')
elif time_zone =='PST':
        df_afternoon['DateTime'] = df_afternoon['DateTime'] - pd.Timedelta(2, unit = 'h')

# Replace missing values of specified columns with zeros
df_afternoon['plp_intensity'] = df_afternoon['plp_intensity'].fillna(0)
df_afternoon['plp_hrs'] = df_afternoon['plp_hrs'].fillna(0)
df_afternoon['plp_mins'] = df_afternoon['plp_mins'].fillna(0)
df_afternoon['plp_interference'] = df_afternoon['plp_interference'].fillna(0)
df_afternoon['other_pain_intensity'] = df_afternoon['other_pain_intensity'].fillna(0)
df_afternoon['activity_duration'] = df_afternoon['activity_duration'].fillna(0)
df_afternoon['activity_intensity'] = df_afternoon['activity_intensity'].fillna(0)
df_afternoon['prosthesis_duration'] = df_afternoon['prosthesis_duration'].fillna(0)
df_afternoon['remove_prosthesis'] = df_afternoon['remove_prosthesis'].fillna(0)

# Calculate duration of PLP
df_afternoon = df_afternoon.replace(['13 hours or more'], ['13'])
df_afternoon = df_afternoon.replace(['1 minute or less'], ['1'])
df_afternoon['plp_hrs'] = df_afternoon['plp_hrs'].astype(int)
df_afternoon['plp_mins'] = df_afternoon['plp_mins'].astype(int)
df_afternoon['plp_hrs'] = df_afternoon['plp_hrs']*60
df_afternoon['plp_duration'] = df_afternoon['plp_hrs'] + df_afternoon['plp_mins']
df_afternoon = df_afternoon.drop(['plp_hrs', 'plp_mins'], axis=1)

# Replace descriptors with number values
df_afternoon = df_afternoon.replace(['(1) Not at all', '(2) A little bit', '(3) Somewhat', '(4) Quite a bit', '(5) Very much'], ['1', '2', '3', '4', '5'])
df_afternoon = df_afternoon.replace(['(1) Poor', '(2) Fair', '(3) Good', '(4) Very good', '(5) Excellent'], ['1', '2', '3', '4', '5'])
df_afternoon = df_afternoon.replace(['(1) Very slightly or not at all', '(2) A little', '(3) Moderately', '(4) Quite a bit', '(5) Extremely'], ['1', '2', '3', '4', '5'])
df_afternoon = df_afternoon.replace(['0 (no pain)', '10 (worst pain imaginable)'], ['0', '10'])
df_afternoon = df_afternoon.replace(['15 minutes or less', '16 - 30 minutes', '31 - 45 minutes', '46 - 60 minutes', '1 hour 1 minute - 1 hour 15 minutes', 
                                     '1 hour 16 minutes - 1 hour 30 minutes', '1 hour 31 minutes - 1 hour 45 minutes', '1 hour 46 minutes - 2 hours', 
                                     'I have been active for over 2 hours', 'I have had my prosthesis on for over 2 hours'], ['1', '2', '3', '4', '5', '6', '7', '8', '9', '9'])
df_afternoon = df_afternoon.replace(['(1) Very light activity', '(2) Light activity', '(3) Moderate activity', '(4) Vigorous activity', '(5) Very hard activity',
                                     '(6) Max effort activity'], ['1', '2', '3', '4', '5', '6'])
df_afternoon = df_afternoon.replace(['Not applicable (I do not use a prosthesis)', 'No', 'Yes'], ['0', '0', '1'])
df_afternoon = df_afternoon.replace(['0 (most uncomfortable socket fit you can imagine)', '10 (most comfortable socket fit you can imagine)'], ['0', '10'])

df_afternoon['morning'] = 0       # Add indicator for time of day
df_afternoon['evening'] = 0



########### EVENING SURVEY ###########
df_evening = pd.read_csv(os.path.join(input_dir,"Evening.csv")) # Read the appropriate csv file

# Clean dataframe and keep only data from specific participant
df_evening = df_evening.drop([0,1], axis=0)
df_evening = df_evening[df_evening['ExternalReference'].str.contains(participant_id) == True]
df_evening['ExternalReference'] = df_evening['ExternalReference'].str.rsplit('E', n=1).str[0]
df_evening = df_evening.drop(['EndDate', 'Status', 'IPAddress', 'Progress', 'Duration (in seconds)', 'Finished', 'RecordedDate', 'ResponseId', 'RecipientLastName', 
                                      'RecipientFirstName', 'RecipientEmail', 'LocationLatitude', 'LocationLongitude','DistributionChannel',
                                     'UserLanguage', 'Q45'], 
                                      axis = 1)
df_evening = df_evening.drop(['Q21.1', 'Q33', 'Q34', 'Q38', 'Q45.1', 'Q44', 'Q51.1', 'Q43', 'Q42', 'Q41', 'Q40', 'Q39.1', 'Q37.2', 'Q38.1', 'Q58', 'Q36.1', 'Q72'], 
                                      axis = 1)

# Select columns for unreported pain and create new dataframe with only these columns
df_evening2 = df_evening[['StartDate','Q39', 'Q46_1', 'Q46_2', 'Q46_3', 'Q47', 'Q48_1', 'Q48_2', 'Q49']] 
df_evening = df_evening.drop(['Q39', 'Q46_1', 'Q46_2', 'Q46_3', 'Q47', 'Q48_1', 'Q48_2', 'Q49'], axis = 1)

# Rename columns to variable names
df_evening = df_evening.rename(columns = {'StartDate':'DateTime', 'Q7':'plp_yn', 'Q8':'plp_intensity', 'Q12_1':'plp_hrs', 'Q12_2':'plp_mins', 'Q37':'plp_interference', 'Q13':'other_pain_yn', 
                                              'Q14':'other_pain_intensity', 'Q20':'activity_yn', 'Q6':'activity_duration', 'Q36':'activity_intensity', 'Q21':'prosthesis_yn', 
                                              'Q22':'prosthesis_duration', 'Q55':'socket_comfort', 'Q53':'remove_prosthesis', 'Q54':'restroom', 'Q56':'health', 'Q37.1':'happy', 
                                              'Q47.1':'sad', 'Q48':'relaxed', 'Q49.1':'nervous', 'Q50':'irritable', 'Q51':'distressed', 'Q52':'excited', 'Q53.1':'lonely'})

# Change DateTime to reflect participant time zone
df_evening['DateTime'] = pd.to_datetime(df_evening['DateTime'])
if time_zone == 'EST':
        df_evening['DateTime'] = df_evening['DateTime'] + pd.Timedelta(1, unit = 'h')
elif time_zone =='CST':
        df_evening['DateTime'] = df_evening['DateTime']
elif time_zone == 'MST':
        df_evening['DateTime'] = df_evening['DateTime'] - pd.Timedelta(1, unit = 'h')
elif time_zone =='PST':
        df_evening['DateTime'] = df_evening['DateTime'] - pd.Timedelta(2, unit = 'h')

# Replace missing values of specified columns with zeros
df_evening['plp_intensity'] = df_evening['plp_intensity'].fillna(0)
df_evening['plp_hrs'] = df_evening['plp_hrs'].fillna(0)
df_evening['plp_mins'] = df_evening['plp_mins'].fillna(0)
df_evening['plp_interference'] = df_evening['plp_interference'].fillna(0)
df_evening['other_pain_intensity'] = df_evening['other_pain_intensity'].fillna(0)
df_evening['activity_duration'] = df_evening['activity_duration'].fillna(0)
df_evening['activity_intensity'] = df_evening['activity_intensity'].fillna(0)
df_evening['prosthesis_duration'] = df_evening['prosthesis_duration'].fillna(0)
df_evening['remove_prosthesis'] = df_evening['remove_prosthesis'].fillna(0)

# Calculate duration of PLP
df_evening = df_evening.replace(['13 hours or more'], ['13'])
df_evening = df_evening.replace(['1 minute or less'], ['1'])
df_evening['plp_hrs'] = df_evening['plp_hrs'].astype(int)
df_evening['plp_mins'] = df_evening['plp_mins'].astype(int)
df_evening['plp_hrs'] = df_evening['plp_hrs']*60
df_evening['plp_duration'] = df_evening['plp_hrs'] + df_evening['plp_mins']
df_evening = df_evening.drop(['plp_hrs', 'plp_mins'], axis=1)

# Replace descriptors with number values
df_evening = df_evening.replace(['(1) Not at all', '(2) A little bit', '(3) Somewhat', '(4) Quite a bit', '(5) Very much'], ['1', '2', '3', '4', '5'])
df_evening = df_evening.replace(['(1) Poor', '(2) Fair', '(3) Good', '(4) Very good', '(5) Excellent'], ['1', '2', '3', '4', '5'])
df_evening = df_evening.replace(['(1) Very slightly or not at all', '(2) A little', '(3) Moderately', '(4) Quite a bit', '(5) Extremely'], ['1', '2', '3', '4', '5'])
df_evening = df_evening.replace(['0 (no pain)', '10 (worst pain imaginable)'], ['0', '10'])
df_evening = df_evening.replace(['15 minutes or less', '16 - 30 minutes', '31 - 45 minutes', '46 - 60 minutes', '1 hour 1 minute - 1 hour 15 minutes', 
                                     '1 hour 16 minutes - 1 hour 30 minutes', '1 hour 31 minutes - 1 hour 45 minutes', '1 hour 46 minutes - 2 hours', 
                                     'I have been active for over 2 hours', 'I have had my prosthesis on for over 2 hours'], ['1', '2', '3', '4', '5', '6', '7', '8', '9', '9'])
df_evening = df_evening.replace(['16 minutes - 30 minutes', '31 minutes - 45 minutes', '46 minutes - 60 minutes'],['2', '3', '4'])
df_evening = df_evening.replace(['(1) Very light activity', '(2) Light activity', '(3) Moderate activity', '(4) Vigorous activity', '(5) Very hard activity',
                                     '(6) Max effort activity'], ['1', '2', '3', '4', '5', '6'])
df_evening = df_evening.replace(['Not applicable (I do not use a prosthesis)', 'No', 'Yes'], ['0', '0', '1'])
df_evening = df_evening.replace(['0 (most uncomfortable socket fit you can imagine)', '10 (most comfortable socket fit you can imagine)'], ['0', '10'])

df_evening['morning'] = 0       # Add indicator for time of day
df_evening['evening'] = 1



########### PAIN SURVEY PROCESSING ###########
df_pain = pd.read_csv(os.path.join(input_dir, "Pain.csv")) # Read the appropriate csv file

# Clean dataframe and keep only data from specific participant
df_pain = df_pain.drop([0,1], axis=0)
df_pain = df_pain[df_pain['ExternalReference'].str.contains(participant_id) == True]
df_pain['ExternalReference'] = df_pain['ExternalReference'].str.rsplit('M', n=1).str[0]
df_pain = df_pain.drop(['EndDate', 'Status', 'IPAddress', 'Progress', 'Duration (in seconds)', 'Finished', 'RecordedDate', 'ResponseId', 'RecipientLastName', 
                                      'RecipientFirstName', 'RecipientEmail', 'LocationLatitude', 'LocationLongitude','DistributionChannel',
                                     'UserLanguage','Q22'], 
                                      axis = 1)

# Rename columns to variable names
df_pain = df_pain.rename(columns = {'StartDate':'DateTime', 'Q8':'plp_intensity', 'Q12_1':'plp_hrs', 'Q12_2':'plp_mins', 'Q21':'plp_interference'})

# Change DateTime to reflect participant time zone
df_pain['DateTime'] = pd.to_datetime(df_pain['DateTime'])
if time_zone == 'EST':
        df_pain['DateTime'] = df_pain['DateTime'] + pd.Timedelta(1, unit = 'h')
elif time_zone =='CST':
        df_pain['DateTime'] = df_pain['DateTime']     # Keep survey time to reflect CST
elif time_zone == 'MST':
        df_pain['DateTime'] = df_pain['DateTime'] - pd.Timedelta(1, unit = 'h')
elif time_zone =='PST':
        df_pain['DateTime'] = df_pain['DateTime'] - pd.Timedelta(2, unit = 'h')

# Format time of reported phantom limb pain (PLP)
df_pain['DateTime'] = df_pain['DateTime'].astype(str)
df_pain['plp_timehr'] = df_pain['DateTime'].str.rsplit(' ').str[1]
df_pain['plp_timehr'] = df_pain['plp_timehr'].str.split(':').str[0]
df_pain['plp_timehr'] = df_pain['plp_timehr'].astype(int)

# Create indicator variable for time of day
df_pain['morning'] = df_pain['plp_timehr'] < 12
df_pain['evening'] = df_pain['plp_timehr'] > 16
df_pain['morning'] = df_pain['morning'].astype(int)
df_pain['evening'] = df_pain['evening'].astype(int)

df_pain = df_pain.drop(['plp_timehr'], axis=1)

# Replace missing values of specified columns with zeros
df_pain['plp_hrs'] = df_pain['plp_hrs'].fillna(0)
df_pain['plp_mins'] = df_pain['plp_mins'].fillna(0)

# Calculate duration of PLP
df_pain = df_pain.replace(['13 hours or more'], ['13'])
df_pain = df_pain.replace(['1 minute or less'], ['1'])
df_pain['plp_hrs'] = df_pain['plp_hrs'].astype(int)
df_pain['plp_mins'] = df_pain['plp_mins'].astype(int)
df_pain['plp_hrs'] = df_pain['plp_hrs']*60
df_pain['plp_duration'] = df_pain['plp_hrs'] + df_pain['plp_mins']
df_pain = df_pain.drop(['plp_hrs', 'plp_mins'], axis=1)

# Replace descriptors with number values
df_pain = df_pain.replace(['(1) Not at all', '(2) A little bit', '(3) Somewhat', '(4) Quite a bit', '(5) Very much'], ['1', '2', '3', '4', '5'])
df_pain = df_pain.replace(['0 (no pain)', '10 (worst pain imaginable)'], ['0', '10'])

df_pain['plp_yn'] = 1



########### UNREPORTED PAIN PROCESSING ###########

########### MORNING ###########
# Rename columns to variable names
df_morning2 = df_morning2.rename(columns = {'Q22':'plp_yn','Q28_1':'unrep_plp_timehr', 'Q28_2':'unrep_plp_timemin', 'Q28_3':'unrep_plp_timeampm', 'Q30':'plp_intensity',
                                          'Q31_1':'plp_hrs', 'Q31_2':'plp_mins', 'Q32':'plp_interference'})

df_morning2 = df_morning2[df_morning2['plp_yn'].str.contains('No') == False]
df_morning2 = df_morning2[df_morning2['plp_yn'].notna()]

# Replace missing values of specified columns with zeros
df_morning2['plp_hrs'] = df_morning2['plp_hrs'].fillna(0)
df_morning2['plp_mins'] = df_morning2['plp_mins'].fillna(0)

# Change StartDate to reflect participant time zone
df_morning2['StartDate'] = pd.to_datetime(df_morning2['StartDate'])
if time_zone == 'EST':
        df_morning2['StartDate'] = df_morning2['StartDate'] + pd.Timedelta(1, unit = 'h')
elif time_zone =='CST':
        df_morning2['StartDate'] = df_morning2['StartDate']
elif time_zone == 'MST':
        df_morning2['StartDate'] = df_morning2['StartDate'] - pd.Timedelta(1, unit = 'h')
elif time_zone =='PST':
        df_morning2['StartDate'] = df_morning2['StartDate'] - pd.Timedelta(2, unit = 'h')

df_morning2['StartDate'] = df_morning2['StartDate'].astype(str)

# Format time of unreported PLP
df_morning2['unrep_plp_timehr'] = df_morning2['unrep_plp_timehr'].str.rsplit(':').str[0]
df_morning2['unrep_plp_timemin'] = df_morning2['unrep_plp_timemin'].fillna(':00')
df_morning2['unrep_plp_timehr'] = df_morning2['unrep_plp_timehr'].astype(int)
df_morning2['unrep_plp_timehr_mil'] = df_morning2['unrep_plp_timehr'].where(df_morning2['unrep_plp_timeampm'] == 'AM', other = (df_morning2['unrep_plp_timehr'] + 12))
df_morning2['unrep_plp_timehr_mil'] = df_morning2['unrep_plp_timehr_mil'].astype(str)
df_morning2['unrep_plp_timehr_mil'] = df_morning2['unrep_plp_timehr_mil'].str.replace('12', '0')
df_morning2['unrep_plp_timehr_mil'] = df_morning2['unrep_plp_timehr_mil'].str.replace('24', '12')
df_morning2['unrep_plp_time'] = df_morning2['unrep_plp_timehr_mil'].astype(str) + df_morning2['unrep_plp_timemin']
df_morning2['survey_date'] = df_morning2['StartDate'].str.split(' ').str[0]
df_morning2['survey_date'] = pd.to_datetime(df_morning2['survey_date'])
df_morning2['survey_yesterday'] = df_morning2['survey_date'] - pd.Timedelta(1, unit = 'D')
df_morning2['survey_yesterday'] = pd.to_datetime(df_morning2['survey_yesterday'])
df_morning2['survey_hour'] = df_morning2['StartDate'].str.split(' ').str[1]
df_morning2['survey_hour'] = df_morning2['survey_hour'].str.split(':').str[0]
df_morning2['unrep_plp_timehr_mil'] = df_morning2['unrep_plp_timehr_mil'].astype(int)
df_morning2['survey_hour'] = df_morning2['survey_hour'].astype(int)
df_morning2['unrep_plp_time'] = (df_morning2['survey_yesterday'].astype(str) + ' ' + df_morning2['unrep_plp_time']).where(df_morning2['unrep_plp_timehr_mil'] >= df_morning2['survey_hour'], 
                                                                                                                   other = (df_morning2['survey_date'].astype(str) + ' ' + df_morning2['unrep_plp_time']))

# Create indicator variable for time of day
df_morning2['morning'] = df_morning2['unrep_plp_timehr_mil'] < 12
df_morning2['evening'] = df_morning2['unrep_plp_timehr_mil'] > 16
df_morning2['morning'] = df_morning2['morning'].astype(int)
df_morning2['evening'] = df_morning2['evening'].astype(int)

df_morning2['unrep_plp_time'] = pd.to_datetime(df_morning2['unrep_plp_time'])

df_morning2 = df_morning2.drop(['unrep_plp_timehr', 'unrep_plp_timemin', 'unrep_plp_timeampm', 'unrep_plp_timehr_mil', 'survey_date', 'survey_yesterday', 'survey_hour', 'StartDate'], axis=1)

# Rename columns to variable names
df_morning2 = df_morning2.rename(columns = {'unrep_plp_time':'DateTime'})

# Calculate duration of PLP
df_morning2 = df_morning2.replace(['13 hours or more'], ['13'])
df_morning2 = df_morning2.replace(['1 minute or less'], ['1'])
df_morning2['plp_hrs'] = df_morning2['plp_hrs'].astype(int)
df_morning2['plp_mins'] = df_morning2['plp_mins'].astype(int)
df_morning2['plp_hrs'] = df_morning2['plp_hrs']*60
df_morning2['plp_duration'] = df_morning2['plp_hrs'] + df_morning2['plp_mins']
df_morning2 = df_morning2.drop(['plp_hrs', 'plp_mins'], axis=1)

# Replace descriptors with number values
df_morning2 = df_morning2.replace(['(1) Not at all', '(2) A little bit', '(3) Somewhat', '(4) Quite a bit', '(5) Very much'], ['1', '2', '3', '4', '5'])
df_morning2 = df_morning2.replace(['0 (no pain)', '10 (worst pain imaginable)'], ['0', '10'])
df_morning2 = df_morning2.replace(['No', 'Yes'], ['0', '1'])


########### AFTERNOON ###########
# Rename columns to variable names
df_afternoon2 = df_afternoon2.rename(columns = {'Q21':'plp_yn','Q27_1':'unrep_plp_timehr', 'Q27_2':'unrep_plp_timemin', 'Q27_3':'unrep_plp_timeampm', 'Q28':'plp_intensity',
                                          'Q29_1':'plp_hrs', 'Q29_2':'plp_mins', 'Q30':'plp_interference'})

df_afternoon2 = df_afternoon2[df_afternoon2['plp_yn'].str.contains('No') == False]
df_afternoon2 = df_afternoon2[df_afternoon2['plp_yn'].notna()]

# Replace missing values of specified columns with zeros
df_afternoon2['plp_hrs'] = df_afternoon2['plp_hrs'].fillna(0)
df_afternoon2['plp_mins'] = df_afternoon2['plp_mins'].fillna(0)

# Change DateTime to reflect participant time zone
df_afternoon2['StartDate'] = pd.to_datetime(df_afternoon2['StartDate'])
if time_zone == 'EST':
        df_afternoon2['StartDate'] = df_afternoon2['StartDate'] + pd.Timedelta(1, unit = 'h')
elif time_zone =='CST':
        df_afternoon2['StartDate'] = df_afternoon2['StartDate']
elif time_zone == 'MST':
        df_afternoon2['StartDate'] = df_afternoon2['StartDate'] - pd.Timedelta(1, unit = 'h')
elif time_zone =='PST':
        df_afternoon2['StartDate'] = df_afternoon2['StartDate'] - pd.Timedelta(2, unit = 'h')

df_afternoon2['StartDate'] = df_afternoon2['StartDate'].astype(str)

# Format time of unreported PLP
df_afternoon2['unrep_plp_timehr'] = df_afternoon2['unrep_plp_timehr'].str.split(':').str[0]
df_afternoon2['unrep_plp_timemin'] = df_afternoon2['unrep_plp_timemin'].fillna(':00')
df_afternoon2['unrep_plp_timehr'] = df_afternoon2['unrep_plp_timehr'].astype(int)
df_afternoon2['unrep_plp_timehr_mil'] = df_afternoon2['unrep_plp_timehr'].where(df_afternoon2['unrep_plp_timeampm'] == 'AM', other = (df_afternoon2['unrep_plp_timehr'] + 12))
df_afternoon2['unrep_plp_timehr_mil'] = df_afternoon2['unrep_plp_timehr_mil'].astype(str)
df_afternoon2['unrep_plp_timehr_mil'] = df_afternoon2['unrep_plp_timehr_mil'].str.replace('12', '0')
df_afternoon2['unrep_plp_timehr_mil'] = df_afternoon2['unrep_plp_timehr_mil'].str.replace('24', '12')
df_afternoon2['unrep_plp_time'] = df_afternoon2['unrep_plp_timehr_mil'].astype(str) + df_afternoon2['unrep_plp_timemin']
df_afternoon2['survey_date'] = df_afternoon2['StartDate'].str.split(' ').str[0]
df_afternoon2['survey_date'] = pd.to_datetime(df_afternoon2['survey_date'])
df_afternoon2['survey_yesterday'] = df_afternoon2['survey_date'] - pd.Timedelta(1, unit = 'D')
df_afternoon2['survey_yesterday'] = pd.to_datetime(df_afternoon2['survey_yesterday'])
df_afternoon2['survey_hour'] = df_afternoon2['StartDate'].str.split(' ').str[1]
df_afternoon2['survey_hour'] = df_afternoon2['survey_hour'].str.split(':').str[0]
df_afternoon2['unrep_plp_timehr_mil'] = df_afternoon2['unrep_plp_timehr_mil'].astype(int)
df_afternoon2['survey_hour'] = df_afternoon2['survey_hour'].astype(int)
df_afternoon2['unrep_plp_time'] = (df_afternoon2['survey_yesterday'].astype(str) + ' ' + df_afternoon2['unrep_plp_time']).where(df_afternoon2['unrep_plp_timehr_mil'] >= df_afternoon2['survey_hour'], 
                                                                                                                   other = (df_afternoon2['survey_date'].astype(str) + ' ' + df_afternoon2['unrep_plp_time']))

# Create indicator variable for time of day
df_afternoon2['morning'] = df_afternoon2['unrep_plp_timehr_mil'] < 12
df_afternoon2['evening'] = df_afternoon2['unrep_plp_timehr_mil'] > 16
df_afternoon2['morning'] = df_afternoon2['morning'].astype(int)
df_afternoon2['evening'] = df_afternoon2['evening'].astype(int)

df_afternoon2['unrep_plp_time'] = pd.to_datetime(df_afternoon2['unrep_plp_time'])

df_afternoon2 = df_afternoon2.drop(['unrep_plp_timehr', 'unrep_plp_timemin', 'unrep_plp_timeampm', 'unrep_plp_timehr_mil', 'survey_date', 'survey_yesterday', 'survey_hour', 'StartDate'], axis=1)

# Rename columns to variable names
df_afternoon2 = df_afternoon2.rename(columns = {'unrep_plp_time':'DateTime'})

# Calculate duration of PLP
df_afternoon2 = df_afternoon2.replace(['13 hours or more'], ['13'])
df_afternoon2 = df_afternoon2.replace(['1 minute or less'], ['1'])
df_afternoon2['plp_hrs'] = df_afternoon2['plp_hrs'].astype(int)
df_afternoon2['plp_mins'] = df_afternoon2['plp_mins'].astype(int)
df_afternoon2['plp_hrs'] = df_afternoon2['plp_hrs']*60
df_afternoon2['plp_duration'] = df_afternoon2['plp_hrs'] + df_afternoon2['plp_mins']
df_afternoon2 = df_afternoon2.drop(['plp_hrs', 'plp_mins'], axis=1)

# Replace descriptors with number values
df_afternoon2 = df_afternoon2.replace(['(1) Not at all', '(2) A little bit', '(3) Somewhat', '(4) Quite a bit', '(5) Very much'], ['1', '2', '3', '4', '5'])
df_afternoon2 = df_afternoon2.replace(['0 (no pain)', '10 (worst pain imaginable)'], ['0', '10'])
df_afternoon2 = df_afternoon2.replace(['No', 'Yes'], ['0', '1'])


########### EVENING ###########
# Rename columns to variable names
df_evening2 = df_evening2.rename(columns = {'Q39':'plp_yn','Q46_1':'unrep_plp_timehr', 'Q46_2':'unrep_plp_timemin', 'Q46_3':'unrep_plp_timeampm', 'Q47':'plp_intensity',
                                          'Q48_1':'plp_hrs', 'Q48_2':'plp_mins', 'Q49':'plp_interference'})

df_evening2 = df_evening2[df_evening2['plp_yn'].str.contains('No') == False]
df_evening2 = df_evening2[df_evening2['plp_yn'].notna()]

# Replace missing values of specified columns with zeros
df_evening2['plp_hrs'] = df_evening2['plp_hrs'].fillna(0)
df_evening2['plp_mins'] = df_evening2['plp_mins'].fillna(0)

# Change DateTime to reflect participant time zone
df_evening2['StartDate'] = pd.to_datetime(df_evening2['StartDate'])
if time_zone == 'EST':
        df_evening2['StartDate'] = df_evening2['StartDate'] + pd.Timedelta(1, unit = 'h')
elif time_zone =='CST':
        df_evening2['StartDate'] = df_evening2['StartDate']
elif time_zone == 'MST':
        df_evening2['StartDate'] = df_evening2['StartDate'] - pd.Timedelta(1, unit = 'h')
elif time_zone =='PST':
        df_evening2['StartDate'] = df_evening2['StartDate'] - pd.Timedelta(2, unit = 'h')

df_evening2['StartDate'] = df_evening2['StartDate'].astype(str)

# Format time of unreported PLP
df_evening2['unrep_plp_timehr'] = df_evening2['unrep_plp_timehr'].str.split(':').str[0]
df_evening2['unrep_plp_timemin'] = df_evening2['unrep_plp_timemin'].fillna(':00')
df_evening2['unrep_plp_timehr'] = df_evening2['unrep_plp_timehr'].astype(int)
df_evening2['unrep_plp_timehr_mil'] = df_evening2['unrep_plp_timehr'].where(df_evening2['unrep_plp_timeampm'] == 'AM', other = (df_evening2['unrep_plp_timehr'] + 12))
df_evening2['unrep_plp_timehr_mil'] = df_evening2['unrep_plp_timehr_mil'].astype(str)
df_evening2['unrep_plp_timehr_mil'] = df_evening2['unrep_plp_timehr_mil'].str.replace('12', '0')
df_evening2['unrep_plp_timehr_mil'] = df_evening2['unrep_plp_timehr_mil'].str.replace('24', '12')
df_evening2['unrep_plp_time'] = df_evening2['unrep_plp_timehr_mil'].astype(str) + df_evening2['unrep_plp_timemin']
df_evening2['survey_date'] = df_evening2['StartDate'].str.split(' ').str[0]
df_evening2['survey_date'] = pd.to_datetime(df_evening2['survey_date'])
df_evening2['survey_yesterday'] = df_evening2['survey_date'] - pd.Timedelta(1, unit = 'D')
df_evening2['survey_yesterday'] = pd.to_datetime(df_evening2['survey_yesterday'])
df_evening2['survey_hour'] = df_evening2['StartDate'].str.split(' ').str[1]
df_evening2['survey_hour'] = df_evening2['survey_hour'].str.split(':').str[0]
df_evening2['unrep_plp_timehr_mil'] = df_evening2['unrep_plp_timehr_mil'].astype(int)
df_evening2['survey_hour'] = df_evening2['survey_hour'].astype(int)
df_evening2['unrep_plp_time'] = (df_evening2['survey_yesterday'].astype(str) + ' ' + df_evening2['unrep_plp_time']).where(df_evening2['unrep_plp_timehr_mil'] >= df_evening2['survey_hour'], 
                                                                                                                   other = (df_evening2['survey_date'].astype(str) + ' ' + df_evening2['unrep_plp_time']))

# Create indicator variable for morning or evening
df_evening2['morning'] = df_evening2['unrep_plp_timehr_mil'] < 12
df_evening2['evening'] = df_evening2['unrep_plp_timehr_mil'] > 16
df_evening2['morning'] = df_evening2['morning'].astype(int)
df_evening2['evening'] = df_evening2['evening'].astype(int)

df_evening2['unrep_plp_time'] = pd.to_datetime(df_evening2['unrep_plp_time'])

#   Delete unneeded columns
df_evening2 = df_evening2.drop(['unrep_plp_timehr', 'unrep_plp_timemin', 'unrep_plp_timeampm', 'unrep_plp_timehr_mil', 'survey_date', 'survey_yesterday', 'survey_hour', 'StartDate'], axis=1)

# Rename columns to variable names
df_evening2 = df_evening2.rename(columns = {'unrep_plp_time':'DateTime'})

# Calculate duration of PLP
df_evening2 = df_evening2.replace(['13 hours or more'], ['13'])
df_evening2 = df_evening2.replace(['1 minute or less'], ['1'])
df_evening2['plp_hrs'] = df_evening2['plp_hrs'].astype(int)
df_evening2['plp_mins'] = df_evening2['plp_mins'].astype(int)
df_evening2['plp_hrs'] = df_evening2['plp_hrs']*60
df_evening2['plp_duration'] = df_evening2['plp_hrs'] + df_evening2['plp_mins']
df_evening2 = df_evening2.drop(['plp_hrs', 'plp_mins'], axis=1)

# Replace descriptors with number values
df_evening2 = df_evening2.replace(['(1) Not at all', '(2) A little bit', '(3) Somewhat', '(4) Quite a bit', '(5) Very much'], ['1', '2', '3', '4', '5'])
df_evening2 = df_evening2.replace(['0 (no pain)', '10 (worst pain imaginable)'], ['0', '10'])
df_evening2 = df_evening2.replace(['No', 'Yes'], ['0', '1'])


# Combine unreported pain from morning, afternoon, and evening surveys into one dataframe
df_unreportedpain_combined = pd.concat([df_morning2, df_afternoon2, df_evening2], axis = 0, ignore_index=True)
df_unreportedpain_combined['DateTime'] = pd.to_datetime(df_unreportedpain_combined['DateTime'])
df_unreportedpain_combined.sort_values(by = ['DateTime'], inplace=True)



### ACCOUNT FOR TRAVEL TO DIFFERENT TIME ZONES FOR UNREPORTED PAIN EPISODES ###
# Check if timestamp input is valid
def is_timestamp_valid(timestamp_str, format):
    try:
        datetime.strptime(timestamp_str, format)
        return True
    except ValueError:
        return False

# Set format for timestamp to be checked
timestamp_format = '%Y-%m-%d %H:%M'

# Check for travel outside time zone
travel_timezone_yn = input("Did the participant travel outside their time zone? ")
if travel_timezone_yn == 'yes':
    travel_number_of_times = int(input("How many times did the participant travel outside their time zone? "))
    if travel_number_of_times > 3:
        print("Only the first three instances of travel will be captured! Update code if more instances are needed.")
    travel_number_of_timestamps = travel_number_of_times*2
    travel_timestamps_list = []
    for i in range(travel_number_of_timestamps):
        travel_timestamp = input(f"Enter travel timestamp #{i} (YYYY-MM-DD 00:00): ")
        if is_timestamp_valid(travel_timestamp, timestamp_format):
            pass
        else:
            print('Invalid input')
            sys.exit()
        travel_timestamps_list.append(travel_timestamp)

    # Create a new dataframe for only unreported pain during travel times
    df_travel = df_unreportedpain_combined[(df_unreportedpain_combined['DateTime'] >= travel_timestamps_list[0]) & (df_unreportedpain_combined['DateTime'] <= travel_timestamps_list[1])]

    # Drop the rows of unreported pain during travel times
    df_unreportedpain_droppedtravel = df_unreportedpain_combined[~df_unreportedpain_combined['DateTime'].between(travel_timestamps_list[0], travel_timestamps_list[1])]

    # Get time zone of travel
    travel_time_zone = input("What time zone did the participant travel to? ")
    if travel_time_zone == 'EST':
        pass
    elif travel_time_zone =='CST':
        pass
    elif travel_time_zone == 'MST':
        pass
    elif travel_time_zone == 'PST':
        pass
    else:
        print("That is not a valid time zone!")
        sys.exit()

    # Change DateTime of unreported pain during travel to reflect participant time zone
    df_travel['DateTime'] = pd.to_datetime(df_travel['DateTime'])
    if travel_time_zone == 'EST':
        if time_zone == 'CST':
            df_travel['DateTime'] = df_travel['DateTime'] - pd.Timedelta(1, unit = 'h')
        elif time_zone == 'MST':
            df_travel['DateTime'] = df_travel['DateTime'] - pd.Timedelta(2, unit = 'h')
        elif time_zone == 'PST':
            df_travel['DateTime'] = df_travel['DateTime'] - pd.Timedelta(3, unit = 'h')
    elif travel_time_zone == 'CST':
        if time_zone == 'EST':
            df_travel['DateTime'] = df_travel['DateTime'] + pd.Timedelta(1, unit = 'h')
        elif time_zone == 'MST':
            df_travel['DateTime'] = df_travel['DateTime'] - pd.Timedelta(1, unit = 'h')
        elif time_zone == 'PST':
            df_travel['DateTime'] = df_travel['DateTime'] - pd.Timedelta(2, unit = 'h')
    elif travel_time_zone == 'MST':
        if time_zone == 'EST':
            df_travel['DateTime'] = df_travel['DateTime'] + pd.Timedelta(2, unit = 'h')
        elif time_zone == 'CST':
            df_travel['DateTime'] = df_travel['DateTime'] + pd.Timedelta(1, unit = 'h')
        elif time_zone == 'PST':
            df_travel['DateTime'] = df_travel['DateTime'] - pd.Timedelta(1, unit = 'h')
    elif travel_time_zone == 'PST':
        if time_zone == 'EST':
            df_travel['DateTime'] = df_travel['DateTime'] + pd.Timedelta(3, unit = 'h')
        elif time_zone == 'CST':
            df_travel['DateTime'] = df_travel['DateTime'] + pd.Timedelta(2, unit = 'h')
        elif time_zone == 'MST':
            df_travel['DateTime'] = df_travel['DateTime'] + pd.Timedelta(1, unit = 'h')

    df_travel['DateTime'] = df_travel['DateTime'].astype(str)

    # Combine dataframe with nontravel unreported PLP (after dropping travel rows) and travel unreported PLP (converted to participant's usual time zone)
    df_unreportedpain_updatedtimes = pd.concat([df_travel, df_unreportedpain_droppedtravel], axis = 0, ignore_index=True)
    df_unreportedpain_updatedtimes['DateTime'] = pd.to_datetime(df_unreportedpain_updatedtimes['DateTime'])
    df_unreportedpain_updatedtimes.sort_values(by = ['DateTime'], inplace=True)

    # This runs if participant took more than one trip to a different time zone
    if travel_number_of_times > 1:
        # Create a new dataframe for only unreported pain during travel times
        df_travel2 = df_unreportedpain_updatedtimes[(df_unreportedpain_updatedtimes['DateTime'] >= travel_timestamps_list[2]) & (df_unreportedpain_updatedtimes['DateTime'] <= travel_timestamps_list[3])]
        # print(df_travel.head())

        # Drop the rows of unreported pain during travel times
        df_unreportedpain_updatedtimes = df_unreportedpain_updatedtimes[~df_unreportedpain_updatedtimes['DateTime'].between(travel_timestamps_list[2], travel_timestamps_list[3])]
        # print(df_unreportedpain_droppedtravel)

        # Get time zone of travel
        travel_time_zone2 = input("What time zone did the participant travel to second? ")
        if travel_time_zone2 == 'EST':
            pass
        elif travel_time_zone2 =='CST':
            pass
        elif travel_time_zone2 == 'MST':
            pass
        elif travel_time_zone2 == 'PST':
            pass
        else:
            print("That is not a valid time zone!")
            sys.exit()

        # Change DateTime of unreported pain during travel to reflect participant time zone
        df_travel2['DateTime'] = pd.to_datetime(df_travel2['DateTime'])   # Convert DateTime to datetime format
        if travel_time_zone2 == 'EST':
            if time_zone == 'CST':
                df_travel2['DateTime'] = df_travel2['DateTime'] - pd.Timedelta(1, unit = 'h')
            elif time_zone == 'MST':
                df_travel2['DateTime'] = df_travel2['DateTime'] - pd.Timedelta(2, unit = 'h')
            elif time_zone == 'PST':
                df_travel2['DateTime'] = df_travel2['DateTime'] - pd.Timedelta(3, unit = 'h')
        elif travel_time_zone2 == 'CST':
            if time_zone == 'EST':
                df_travel2['DateTime'] = df_travel2['DateTime'] + pd.Timedelta(1, unit = 'h')
            elif time_zone == 'MST':
                df_travel2['DateTime'] = df_travel2['DateTime'] - pd.Timedelta(1, unit = 'h')
            elif time_zone == 'PST':
                df_travel2['DateTime'] = df_travel2['DateTime'] - pd.Timedelta(2, unit = 'h')
        elif travel_time_zone2 == 'MST':
            if time_zone == 'EST':
                df_travel2['DateTime'] = df_travel2['DateTime'] + pd.Timedelta(2, unit = 'h')
            elif time_zone == 'CST':
                df_travel2['DateTime'] = df_travel2['DateTime'] + pd.Timedelta(1, unit = 'h')
            elif time_zone == 'PST':
                df_travel2['DateTime'] = df_travel2['DateTime'] - pd.Timedelta(1, unit = 'h')
        elif travel_time_zone2 == 'PST':
            if time_zone == 'EST':
                df_travel2['DateTime'] = df_travel2['DateTime'] + pd.Timedelta(3, unit = 'h')
            elif time_zone == 'CST':
                df_travel2['DateTime'] = df_travel2['DateTime'] + pd.Timedelta(2, unit = 'h')
            elif time_zone == 'MST':
                df_travel2['DateTime'] = df_travel2['DateTime'] + pd.Timedelta(1, unit = 'h')

        df_travel2['DateTime'] = df_travel2['DateTime'].astype(str)

        # Combine dataframe with nontravel unreported PLP (dropped travel rows) and travel unreported PLP (converted to participant's usual time zone)
        df_unreportedpain_updatedtimes2 = pd.concat([df_travel2, df_unreportedpain_updatedtimes], axis = 0, ignore_index=True)
        df_unreportedpain_updatedtimes2['DateTime'] = pd.to_datetime(df_unreportedpain_updatedtimes2['DateTime'])
        df_unreportedpain_updatedtimes2.sort_values(by = ['DateTime'], inplace=True)
        df_unreportedpain_updatedtimes = df_unreportedpain_updatedtimes2
    else:
        pass
        
    # This runs if participant took more than two trips to a different time zone
    if travel_number_of_times > 2:
        # Create a new dataframe for only unreported pain during travel times
        df_travel3 = df_unreportedpain_updatedtimes[(df_unreportedpain_updatedtimes['DateTime'] >= travel_timestamps_list[4]) & (df_unreportedpain_updatedtimes['DateTime'] <= travel_timestamps_list[5])]
        # print(df_travel.head())

        # Drop the rows of unreported pain during travel times
        df_unreportedpain_updatedtimes = df_unreportedpain_updatedtimes[~df_unreportedpain_updatedtimes['DateTime'].between(travel_timestamps_list[4], travel_timestamps_list[5])]
        # print(df_unreportedpain_droppedtravel)

        # Get time zone of travel
        travel_time_zone3 = input("What time zone did the participant travel to third? ")
        if travel_time_zone2 == 'EST':
            pass
        elif travel_time_zone2 =='CST':
            pass
        elif travel_time_zone2 == 'MST':
            pass
        elif travel_time_zone2 == 'PST':
            pass
        else:
            print("That is not a valid time zone!")
            sys.exit()

        # Change DateTime of unreported pain during travel to reflect participant time zone
        df_travel3['DateTime'] = pd.to_datetime(df_travel3['DateTime'])
        if travel_time_zone3 == 'EST':
            if time_zone == 'CST':
                df_travel3['DateTime'] = df_travel3['DateTime'] - pd.Timedelta(1, unit = 'h')
            elif time_zone == 'MST':
                df_travel3['DateTime'] = df_travel3['DateTime'] - pd.Timedelta(2, unit = 'h')
            elif time_zone == 'PST':
                df_travel3['DateTime'] = df_travel3['DateTime'] - pd.Timedelta(3, unit = 'h')
        elif travel_time_zone3 == 'CST':
            if time_zone == 'EST':
                df_travel3['DateTime'] = df_travel3['DateTime'] + pd.Timedelta(1, unit = 'h')
            elif time_zone == 'MST':
                df_travel3['DateTime'] = df_travel3['DateTime'] - pd.Timedelta(1, unit = 'h')
            elif time_zone == 'PST':
                df_travel3['DateTime'] = df_travel3['DateTime'] - pd.Timedelta(2, unit = 'h')
        elif travel_time_zone3 == 'MST':
            if time_zone == 'EST':
                df_travel3['DateTime'] = df_travel3['DateTime'] + pd.Timedelta(2, unit = 'h')
            elif time_zone == 'CST':
                df_travel3['DateTime'] = df_travel3['DateTime'] + pd.Timedelta(1, unit = 'h')
            elif time_zone == 'PST':
                df_travel3['DateTime'] = df_travel3['DateTime'] - pd.Timedelta(1, unit = 'h')
        elif travel_time_zone3 == 'PST':
            if time_zone == 'EST':
                df_travel3['DateTime'] = df_travel3['DateTime'] + pd.Timedelta(3, unit = 'h')
            elif time_zone == 'CST':
                df_travel3['DateTime'] = df_travel3['DateTime'] + pd.Timedelta(2, unit = 'h')
            elif time_zone == 'MST':
                df_travel3['DateTime'] = df_travel3['DateTime'] + pd.Timedelta(1, unit = 'h')

        df_travel3['DateTime'] = df_travel3['DateTime'].astype(str)

        # Combine dataframe with nontravel unreported PLP (dropped travel rows) and travel unreported PLP (converted to participant's usual time zone)
        df_unreportedpain_updatedtimes3 = pd.concat([df_travel3, df_unreportedpain_updatedtimes], axis = 0, ignore_index=True)
        df_unreportedpain_updatedtimes3['DateTime'] = pd.to_datetime(df_unreportedpain_updatedtimes3['DateTime'])
        df_unreportedpain_updatedtimes3.sort_values(by = ['DateTime'], inplace=True)
        df_unreportedpain_updatedtimes = df_unreportedpain_updatedtimes3
    else:
        pass
elif travel_timezone_yn =='no':
    df_unreportedpain_updatedtimes = df_unreportedpain_combined
else:
    print("Invalid input")
    sys.exit()



########### COMBINE DATAFRAMES ###########
df_combined = pd.concat([df_morning, df_afternoon, df_evening, df_pain, df_unreportedpain_updatedtimes], axis = 0, ignore_index=True)
df_combined['DateTime'] = pd.to_datetime(df_combined['DateTime'])
df_combined.sort_values(by = ['DateTime'], inplace=True)

# Find datetime to search for in weather spreadsheet
df_combined['DateTime'] = df_combined['DateTime'].astype(str)
df_combined['datetime_weather_search'] = df_combined['DateTime'].str.split(':').str[0] 
df_combined['datetime_weather_search'] = df_combined['datetime_weather_search'] + ':00'
df_combined['DateTime'] = pd.to_datetime(df_combined['DateTime'])



########### WEATHER ###########
df_weather = pd.read_csv(os.path.join(input_dir, f"{participant_id}_Weather.csv")) # Read the appropriate csv file

# Format columns and data
df_weather = df_weather[['time', 'temperature_2m (°C)', 'relative_humidity_2m (%)', 'apparent_temperature (°C)', 'rain (mm)', 'snowfall (cm)', 'pressure_msl (hPa)']]
df_weather = df_weather.rename(columns = {'temperature_2m (°C)':'temp_C', 'relative_humidity_2m (%)':'humidity_pct', 'apparent_temperature (°C)':'feels_like_C', 
                                          'pressure_msl (hPa)':'pressure_hPa', 'rain (mm)':'rain_lasthr_mm', 'snowfall (cm)':'snow_lasthr_cm'})
df_weather['temp_k'] = df_weather['temp_C'] + 273.15
df_weather['feels_like_k'] = df_weather['feels_like_C'] + 273.15
df_weather['snow_lasthr_mm'] = df_weather['snow_lasthr_cm'] * 10
df_weather['datetime_weather_search'] = pd.to_datetime(df_weather['time'],unit='s')
df_weather['datetime_weather_search'] = df_weather['datetime_weather_search'] - pd.Timedelta(6, unit = 'h')
df_weather = df_weather.drop(['temp_C', 'feels_like_C', 'snow_lasthr_cm', 'time'], axis=1)

# Convert to participant time zone. Weather data from API is collected in CST.
df_weather['datetime_weather_search'] = pd.to_datetime(df_weather['datetime_weather_search'])
if time_zone == 'EST':
        df_weather['datetime_weather_search'] = df_weather['datetime_weather_search'] + pd.Timedelta(1, unit = 'h')
elif time_zone =='CST':
        df_weather['datetime_weather_search'] = df_weather['datetime_weather_search']
elif time_zone == 'MST':
        df_weather['datetime_weather_search'] = df_weather['datetime_weather_search'] - pd.Timedelta(1, unit = 'h')
elif time_zone =='PST':
        df_weather['datetime_weather_search'] = df_weather['datetime_weather_search'] - pd.Timedelta(2, unit = 'h')

df_weather['datetime_weather_search'] = df_weather['datetime_weather_search'].dt.round('60min')

df_weather['datetime_weather_search'] = df_weather['datetime_weather_search'].astype(str)

df_weather['datetime_weather_search'] = df_weather['datetime_weather_search'].str.rsplit(':', n=1).str[0]

df_weather['datetime_weather_search'] = df_weather['datetime_weather_search'].astype(str)
df_weather['survey_date'] = df_weather['datetime_weather_search'].str.split(' ').str[0]
df_weather['survey_date'] = pd.to_datetime(df_weather['survey_date'])
df_weather['survey_yesterday'] = df_weather['survey_date'] - pd.Timedelta(1, unit = 'D')
df_weather['survey_yesterday'] = pd.to_datetime(df_weather['survey_yesterday'])

# Calculate differences for each hour, take absolute value, then find max for the day
df_weather['temp_k_diff'] = df_weather['temp_k'].diff().abs()
df_weather['max_1hr_temp_k_diff_today'] = df_weather.groupby('survey_yesterday')['temp_k_diff'].transform('max')
df_weather['humidity_pct_diff'] = df_weather['humidity_pct'].diff().abs()
df_weather['max_1hr_humidity_pct_diff_today'] = df_weather.groupby('survey_yesterday')['humidity_pct_diff'].transform('max')
df_weather['pressure_hPa_diff'] = df_weather['pressure_hPa'].diff().abs()
df_weather['max_1hr_pressure_hPa_diff_today'] = df_weather.groupby('survey_yesterday')['pressure_hPa_diff'].transform('max')

# Shift temperature, humidity, pressure, rain, and snow back two rows to create placeholders if needed for before_next_survey (when plp_intensity_before_next_survey is 0)
df_weather['temp_k_before_next_survey_placeholder'] = df_weather['temp_k'].shift(-2)
df_weather['humidity_pct_before_next_survey_placeholder'] = df_weather['humidity_pct'].shift(-2)
df_weather['pressure_hPa_before_next_survey_placeholder'] = df_weather['pressure_hPa'].shift(-2)
df_weather['rain_lasthr_mm_before_next_survey_placeholder'] = df_weather['rain_lasthr_mm'].shift(-2)
df_weather['snow_lasthr_mm_before_next_survey_placeholder'] = df_weather['snow_lasthr_mm'].shift(-2)

df_weather = df_weather.drop(['temp_k_diff', 'humidity_pct_diff', 'pressure_hPa_diff'], axis=1)

# Combine df_combined with weather data
df_combined2 = pd.merge(df_combined,df_weather,how='outer',on='datetime_weather_search')
df_combined2 = df_combined2[df_combined2['plp_yn'].notna()]      # Drop any rows where plp_yn is 'NaN' to eliminate extra weather data

df_combined2.reset_index(drop=True, inplace = True)     # Reset the row index to begin at 0


# Add pain events to previous Daily Survey
missing_data = df_combined2['other_pain_intensity'].isnull()
consecutive_missing = []
for k, g in groupby(enumerate(missing_data), lambda x: x[1]):
    if k:
        consecutive_missing.append(list(map(lambda x: x[0], list(g))))

for i in consecutive_missing:
    intensity_data = []
    interference_data = []
    temp_data = []
    humidity_data = []
    pressure_data = []
    rain_data = []
    snow_data = []
    morning_data = []
    evening_data = []
    for j in i:
        plp_intensity = df_combined2.iloc[j]['plp_intensity']
        plp_interference = df_combined2.iloc[j]['plp_interference']
        temp = df_combined2.iloc[j]['temp_k']
        humidity = df_combined2.iloc[j]['humidity_pct']
        pressure = df_combined2.iloc[j]['pressure_hPa']
        rain = df_combined2.iloc[j]['rain_lasthr_mm']
        snow = df_combined2.iloc[j]['snow_lasthr_mm']
        morning = df_combined2.iloc[j]['morning']
        evening = df_combined2.iloc[j]['evening']
        intensity_data.append(plp_intensity)
        interference_data.append(plp_interference)
        temp_data.append(temp)
        humidity_data.append(humidity)
        pressure_data.append(pressure)
        rain_data.append(rain)
        snow_data.append(snow)
        morning_data.append(morning)
        evening_data.append(evening)

    max_intensity = max(intensity_data)
    max_interference = max(interference_data)
    avg_temp = mean(temp_data)
    avg_humidity = mean(humidity_data)
    avg_pressure = mean(pressure_data)
    max_rain = max(rain_data)
    max_snow = max(snow_data)
    max_morning = max(morning_data)
    max_evening = max(evening_data)

    previous_row = i[0]-1
    df_combined2.loc[previous_row, 'plp_intensity_before_next_survey'] = max_intensity
    df_combined2.loc[previous_row, 'plp_interference_before_next_survey'] = max_interference
    df_combined2.loc[previous_row, 'temp_k_before_next_survey'] = avg_temp
    df_combined2.loc[previous_row, 'humidity_pct_before_next_survey'] = avg_humidity
    df_combined2.loc[previous_row, 'pressure_hPa_before_next_survey'] = avg_pressure
    df_combined2.loc[previous_row, 'rain_lasthr_mm_before_next_survey'] = max_rain
    df_combined2.loc[previous_row, 'snow_lasthr_mm_before_next_survey'] = max_snow
    df_combined2.loc[previous_row, 'morning_before_next_survey'] = max_morning
    df_combined2.loc[previous_row, 'evening_before_next_survey'] = max_evening

df_combined2['plp_intensity_before_next_survey'] = df_combined2['plp_intensity_before_next_survey'].fillna(df_combined2['plp_intensity'].mode()[0])
df_combined2['plp_interference_before_next_survey'] = df_combined2['plp_interference_before_next_survey'].fillna(df_combined2['plp_interference'].mode()[0])
df_combined2['temp_k_before_next_survey'] = df_combined2['temp_k_before_next_survey'].fillna(df_combined2['temp_k_before_next_survey_placeholder'])
df_combined2['humidity_pct_before_next_survey'] = df_combined2['humidity_pct_before_next_survey'].fillna(df_combined2['humidity_pct_before_next_survey_placeholder'])
df_combined2['pressure_hPa_before_next_survey'] = df_combined2['pressure_hPa_before_next_survey'].fillna(df_combined2['pressure_hPa_before_next_survey_placeholder'])
df_combined2['rain_lasthr_mm_before_next_survey'] = df_combined2['rain_lasthr_mm_before_next_survey'].fillna(df_combined2['rain_lasthr_mm_before_next_survey_placeholder'])
df_combined2['snow_lasthr_mm_before_next_survey'] = df_combined2['snow_lasthr_mm_before_next_survey'].fillna(df_combined2['snow_lasthr_mm_before_next_survey_placeholder'])
df_combined2['morning_before_next_survey'] = df_combined2['morning_before_next_survey'].fillna(0)
df_combined2['evening_before_next_survey'] = df_combined2['evening_before_next_survey'].fillna(0)

df_combined2['DateTime'] = df_combined2['DateTime'].astype(str)
df_combined2['survey_date'] = df_combined2['DateTime'].str.split(' ').str[0]
df_combined2['survey_date'] = pd.to_datetime(df_combined2['survey_date'])

# Carry forward night data through next day
df_combined2['last_nights_sleep'] = df_combined2.groupby('survey_date')['last_nights_sleep'].ffill()
df_combined2['last_nights_sleep'] = df_combined2.groupby('survey_date')['last_nights_sleep'].bfill()
df_combined2['last_sleep_quality'] = df_combined2.groupby('survey_date')['last_sleep_quality'].ffill()
df_combined2['last_sleep_quality'] = df_combined2.groupby('survey_date')['last_sleep_quality'].bfill()
df_combined2['plp_fallasleep'] = df_combined2.groupby('survey_date')['plp_fallasleep'].ffill()
df_combined2['plp_fallasleep'] = df_combined2.groupby('survey_date')['plp_fallasleep'].bfill()
df_combined2['plp_stayasleep'] = df_combined2.groupby('survey_date')['plp_stayasleep'].ffill()
df_combined2['plp_stayasleep'] = df_combined2.groupby('survey_date')['plp_stayasleep'].bfill()
df_combined2['shrinker_duration_last_night'] = df_combined2.groupby('survey_date')['shrinker_duration_last_night'].ffill()
df_combined2['shrinker_duration_last_night'] = df_combined2.groupby('survey_date')['shrinker_duration_last_night'].bfill()


# Create variable for night before last (for variables: last_last_nights_sleep, last_last_sleep_quality, shrinker_duration_last_last_night)
df_combined2['last_last_nights_sleep'] = df_combined2['last_nights_sleep'].shift().where(df_combined2.survey_yesterday.eq(df_combined2.survey_date.shift()))
df_combined2['last_last_sleep_quality'] = df_combined2['last_sleep_quality'].shift().where(df_combined2.survey_yesterday.eq(df_combined2.survey_date.shift()))
df_combined2['shrinker_duration_last_last_night'] = df_combined2['shrinker_duration_last_night'].shift().where(df_combined2.survey_yesterday.eq(df_combined2.survey_date.shift()))

# Carry forward data through next day
df_combined2['last_last_nights_sleep'] = df_combined2.groupby('survey_date')['last_last_nights_sleep'].ffill()
df_combined2['last_last_nights_sleep'] = df_combined2.groupby('survey_date')['last_last_nights_sleep'].bfill()
df_combined2['last_last_sleep_quality'] = df_combined2.groupby('survey_date')['last_last_sleep_quality'].ffill()
df_combined2['last_last_sleep_quality'] = df_combined2.groupby('survey_date')['last_last_sleep_quality'].bfill()
df_combined2['shrinker_duration_last_last_night'] = df_combined2.groupby('survey_date')['shrinker_duration_last_last_night'].ffill()
df_combined2['shrinker_duration_last_last_night'] = df_combined2.groupby('survey_date')['shrinker_duration_last_last_night'].bfill()

df_combined2 = df_combined2.drop(['survey_date', 'datetime_weather_search', 'survey_yesterday', 'temp_k_before_next_survey_placeholder', 'humidity_pct_before_next_survey_placeholder',
                                  'pressure_hPa_before_next_survey_placeholder', 'rain_lasthr_mm_before_next_survey_placeholder', 'snow_lasthr_mm_before_next_survey_placeholder'], axis=1)
df_combined2 = df_combined2.dropna(subset=['other_pain_intensity'])

missing_values = df_combined2.isna().sum()
df_missing = pd.DataFrame(missing_values)

# Record missing values for each column for this participant in a csv file
df_missing.to_csv(os.path.join(input_dir, f"{participant_id}_missingdata.csv"), index=True, header=False)

# Use median imputation for missing values in each column except socket_comfort
variables_with_missing = df_combined2.columns[df_combined2.isnull().any()]
# print(variables_with_missing)
donotfill = ['socket_comfort']
for item in variables_with_missing:
        if item not in donotfill:
                df_combined2[item] = df_combined2[item].apply(pd.to_numeric)
                df_combined2[item] = df_combined2[item].fillna(df_combined2[item].median())
else:
      pass

# If greater than 50% of samples are missing a value for socket_comfort, delete the column. If less than 50% of samples are missing a value, retain the column and manually impute the missing values after running this code.
missing_socket_comfort = df_combined2['socket_comfort'].isna().sum()
count_row = df_combined2.shape[0]
percent_missing_socket_comfort = missing_socket_comfort/count_row
if percent_missing_socket_comfort > 0.5:
      df_combined2 = df_combined2.drop(['socket_comfort'], axis=1)
else:
      pass

# Save csv file
for id, group in df_combined2.groupby(['ExternalReference']):

    group.to_csv(os.path.join(input_dir, f"{participant_id}_combineddata1.csv"), index=False, header=True)