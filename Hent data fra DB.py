#hent GPS data
import pandas as pd
import streamlit as st
import seaborn as sns
import os
import glob
import matplotlib.pyplot as plt
import openpyxl as xlsxwriter
from pandas import DataFrame
from dateutil import parser
os.chdir(r'C:\Users\SéamusPeareBartholdy\OneDrive - AC Horsens A S\Akademi\Excel Organisering og indhold af træning framework\GPS udtræk')
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
df = pd.DataFrame(combined_csv)
df = df.dropna()
print ('GPS csv filer kombineret')
df2 = pd.read_excel(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\GPS spillere.xlsx')
dforiginal = df.merge(df2)
os.chdir(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens')
dforiginal.to_excel(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\samlet gps data.xlsx', index=False)
dforiginal = pd.read_excel(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\samlet gps data.xlsx')
writer = pd.ExcelWriter(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\samlet gps data.xlsx', engine='xlsxwriter')
dforiginal.to_excel(writer,sheet_name='Sheet1', index=None, header=True)


workbook  = writer.book
worksheet = writer.sheets['Sheet1']

formatdict = {'num_format':'dd-mm-yyyy'}
fmt = workbook.add_format(formatdict)
worksheet.set_column('A:A', None, fmt)

formatdict = {'num_format':'hh:mm:ss'}
fmt = workbook.add_format(formatdict)
worksheet.set_column('F:G', None, fmt)

writer.close()
dforiginal = pd.read_excel(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\samlet gps data.xlsx',decimal=',')
Ugenummer = dforiginal['Date'].apply(lambda x: x.isocalendar()[1])
dforiginal.insert(loc = 48, column = 'Ugenummer', value= Ugenummer)
dforiginal.to_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\samlet gps data.csv', index=False)
os.remove(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\samlet gps data.xlsx')
print('GPS færdig')

#Hent eventdata
from azure.storage.fileshare import ShareServiceClient
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
import os
connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 22-23/U15 Ligaen/'


service_client = ShareServiceClient.from_connection_string(connection_string)
share_client = service_client.get_share_client(share_name)
directory_client = share_client.get_directory_client(dir_path)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchEvents' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))

find_json_files(directory_client)

# Create an empty list to store the events data
events_list = []

# Iterate over each item in the json_files list and append its 'events' data to the events_list
for item in json_files:
    events_list.extend(item['events'])

# Convert the events_list to a DataFrame
df = pd.DataFrame(events_list)
print('U15 data hentet fra database')
type_cols = pd.json_normalize(df['type'])
type_cols.columns = ['type_primary','type_secondary']
df = pd.concat([df.drop('type', axis=1), type_cols], axis=1)
df = df.rename(columns= {'id':'Action id'})
type_cols = pd.json_normalize(df['location'])
type_cols.columns = ['x','y']
df = pd.concat([df.drop('location', axis=1), type_cols], axis=1)
df = df.rename(columns={'x' : 'Action location start x', 'y' : 'Action location start y'})
type_cols = pd.json_normalize(df['team'])
type_cols.columns = ['id','name','formation']
df = pd.concat([df.drop('team', axis=1), type_cols], axis=1)
df = df.rename(columns={'id' : 'Team id', 'name' : 'Team name','formation':'Team formation'})
type_cols = pd.json_normalize(df['opponentTeam'])
type_cols.columns = ['id','name','formation']
df = pd.concat([df.drop('opponentTeam', axis=1), type_cols], axis=1)
df = df.rename(columns={'id' : 'Opponent team id', 'name' : 'Opponent team name','formation':'Opponent team formation'})
type_cols = pd.json_normalize(df['player'])
type_cols.columns = ['id','name','position']
df = pd.concat([df.drop('player', axis=1), type_cols], axis=1)
df = df.rename(columns={'id' : 'Player id', 'name' : 'Player name','position':'Player position'})
type_cols = pd.json_normalize(df['pass'])
type_cols.columns = ['accurate','angle','height','length','recipient','id','name','position','endLocation']
df = pd.concat([df.drop('pass', axis=1), type_cols], axis=1)
df = df.rename(columns={'accurate' : 'Pass accurate', 'angle' : 'Pass angle','height':'Pass height','length':'Pass length','recipient':'Pass recipient id','id':'Pass recipient name','name':'Pass recipient position','position':'Pass end x','endLocation':'Pass end y'})
type_cols = pd.json_normalize(df['shot'])
type_cols.columns = ['bodypart','isGoal','onTarget','goalZone','xg','postShotXg','goalkeeperActionId','goalkeeper','id','name']
df = pd.concat([df.drop('shot', axis=1), type_cols], axis=1)
df = df.rename(columns={'bodypart' : 'Shot bodypart', 'isGoal' : 'Shot is goal','onTarget':'Shot on target','goalZone':'Shot goalzone','xg':'Shot xg','postShotxg':'Shot post shot xg','goalkeeperActionId':'Shot goalkeeper action id','goalkeeper':'Shot goalkeeper','id':'Shot goalkeeper id','name':'Shot goalkeeper name'})
type_cols = pd.json_normalize(df['possession'])
type_cols.columns = ['id','duration','types','eventsNumber','eventIndex','location','x','y','x','y','id','name','formation','withShot','withShotOnGoal','withGoal','flank','xg',]
df = pd.concat([df.drop('possession', axis=1), type_cols], axis=1)
df = df.rename(columns={'id' : 'Possession id', 'duration' : 'Possession duration','types':'Possession type','eventsnumber':'Possession eventsnumber','eventIndex':'Possession event index','location':'Possession location'})
# create unique names for duplicate columns
dup_cols = [col for col in df.columns if df.columns.tolist().count(col) > 1]
unique_cols = [f'{col}_{i}' if col in dup_cols else col for i, col in enumerate(df.columns)]

# rename the dataframe columns with the unique names
df.columns = unique_cols

df = df.rename(columns={'Possession id_44':'Possession id','x_50':'Possession start location x','y_51':'Possession start location y','x_52':'Possession end location x','y_53':'Possession end location y','Possession id_54':'Possession team id','name':'Possession team name','formation':'Possession team formation','withShot':'Possession with shot','withShotOnGoal':'Possession with shot on goal','withGoal':'Possession with goal','flank':'Possession flank','xg':'Possession xg'})
type_cols = pd.json_normalize(df['groundDuel'])
type_cols.columns = ['opponent','id','name','position','duelType','keptPossession','progressedWithBall','stoppedProgress','recoveredPossession','takeOn','side','relatedDuelId']
df = pd.concat([df.drop('groundDuel', axis=1), type_cols], axis=1)
df = df.rename(columns={'opponent':'Ground duel type','id':'Ground duel kept possession','name':'Ground duel progressed with ball','position':'Ground duel stopped progress','duelType':'Ground duel recovered possession','keptPosession':'Ground duel takeon','progressedWithBall':'Ground duel side','stoppedProgress':'Ground duel related duel id','recoveredPossession':'Ground duel opponent id','takeOn':'Ground duel opponent name','side':'Ground duel opponent position','relatedDuelId':'slettes'})
#df = df.rename(columns={'bodypart' : 'Shot bodypart', 'isGoal' : 'Shot is goal','onTarget':'Shot on target','goalZone':'Shot goalzone','xg':'Shot xg','postShotxg':'Shot post shot xg','goalkeeperActionId':'Shot goalkeeper action id','goalkeeper':'Shot goalkeeper','id':'Shot goalkeeper id','name':'Shot goalkeeper name'})
type_cols = pd.json_normalize(df['aerialDuel'])
type_cols.columns = ['opponent','id','name','position','height','firstTouch','height','relatedDuelId']
df = pd.concat([df.drop('aerialDuel', axis=1), type_cols], axis=1)
df = df.rename(columns={'opponent':'Aerial duelfirstTouch','id':'Aerial duel height','name':'Aerial duel related duel id','position':'Aerial duel opponent id','height':'Aerial duel opponent name','firstTouch':'Aerial duel opponent position','relatedDuelId':'slettes'})
dup_cols = [col for col in df.columns if df.columns.tolist().count(col) > 1]
unique_cols = [f'{col}_{i}' if col in dup_cols else col for i, col in enumerate(df.columns)]
# rename the dataframe columns with the unique names
df.columns = unique_cols
df = df.rename(columns={'Aerial duel opponent name_78':'Aerial duel opponent height','Aerial duel opponent name_76':'Aerial duel opponent name'})
type_cols = pd.json_normalize(df['infraction'])
type_cols.columns = ['yellowCard','redCard','type','opponent','id','name','position']
df = pd.concat([df.drop('infraction', axis=1), type_cols], axis=1)
df = df.rename(columns={'yellowCard':'Infraction yellow card','redCard':'Infraction red card','type':'Infraction type','opponent':'Infraction opponent id','id':'Infraction opponent name','name':'Infraction opponent position','position':'slettes'})
type_cols = pd.json_normalize(df['carry'])
type_cols.columns = ['progression','x','y']
df = pd.concat([df.drop('carry', axis=1), type_cols], axis=1)
df = df.rename(columns={'progression':'Carry progression','x':'Carry end location x','y':'Carry end location y'})
df = df[df['Team name'].str.contains('Horsens')|df['Opponent team name'].str.contains('Horsens')]
print('U15 data sorteret til kun at indeholde egne kampe')

df['type_secondary'] = df['type_secondary'].astype(str)
df['type_secondary'] = df['type_secondary'].str.replace('[','',regex=True)
df['type_secondary'] = df['type_secondary'].str.replace(']','',regex=True)
df['type_secondary'] = df['type_secondary'].str.replace('"','',regex=True)
df['type_secondary'] = df['type_secondary'].str.replace(',','',regex=True)
df['type_secondary'] = df['type_secondary'].str.replace("'",'',regex=True)

df['Pass'] = df['type_secondary'].map(lambda x: 1 if 'pass' in x else 0)
df['Pass to penalty area'] = df['type_secondary'].map(lambda x: 1 if 'pass_to_penalty_area' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('pass_to_penalty_area','',regex=True)
df['Back pass'] = df['type_secondary'].map(lambda x: 1 if 'back_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('back_pass','',regex=True)
df['Short or medium pass'] = df['type_secondary'].map(lambda x: 1 if 'short_or_medium_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('short_or_medium_pass','',regex=True)
df['Aerial duel'] = df['type_secondary'].map(lambda x: 1 if 'aerial_duel' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('aerial_duel','',regex=True)
df['Shot assist'] = df['type_secondary'].map(lambda x: 1 if 'shot_assist' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('shot_assist','',regex=True)
df['Shot block'] = df['type_secondary'].map(lambda x: 1 if 'shot_block' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('shot_block','',regex=True)
df['Shot'] = df['type_secondary'].map(lambda x: 1 if 'shot' in x else 0)
df['Second assist'] = df['type_secondary'].map(lambda x: 1 if 'second_assist' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('second_assist','',regex=True)
df['Third assist'] = df['type_secondary'].map(lambda x: 1 if 'third_assist' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('third_assist','',regex=True)
df['Assist'] = df['type_secondary'].map(lambda x: 1 if 'assist' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('assist','',regex=True)
df['Ball out'] = df['type_secondary'].map(lambda x: 1 if 'ball_out' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('ball_out','',regex=True)
df['Carry'] = df['type_secondary'].map(lambda x: 1 if 'carry' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('carry','',regex=True)
df['Conceded goal'] = df['type_secondary'].map(lambda x: 1 if 'conceded_goal' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('conceded_goal','',regex=True)
df['Counterpressing recovery'] = df['type_secondary'].map(lambda x: 1 if 'counterpressing_recovery' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('counterpressing_recovery','',regex=True)
df['Cross blocked'] = df['type_secondary'].map(lambda x: 1 if 'cross_blocked' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('cross_blocked','',regex=True)
df['Deep completed cross'] = df['type_secondary'].map(lambda x: 1 if 'deep_completed_cross' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('deep_completed_cross','',regex=True)
df['Free kick cross'] = df['type_secondary'].map(lambda x: 1 if 'free_kick_cross' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('free_kick_cross','',regex=True)
df['Cross'] = df['type_secondary'].map(lambda x: 1 if 'cross' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('cross','',regex=True)
df['Deep completion'] = df['type_secondary'].map(lambda x: 1 if 'deep_completion' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('deep_completion','',regex=True)
df['Defensive duel'] = df['type_secondary'].map(lambda x: 1 if 'defensive_duel' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('defensive_duel','',regex=True)
df['Dribble'] = df['type_secondary'].map(lambda x: 1 if 'dribble' in x else 0)
df['Dribbled past attempt'] = df['type_secondary'].map(lambda x: 1 if 'dribbled_past_attempt' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('dribbled_past_attempt','',regex=True)
df['type_secondary'] = df['type_secondary'].str.replace('dribble','',regex=True)
df['Forward pass'] = df['type_secondary'].map(lambda x: 1 if 'forward_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('forward_pass','',regex=True)
df['Foul suffered'] = df['type_secondary'].map(lambda x: 1 if 'foul_suffered' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('foul_suffered','',regex=True)
df['Free kick shot'] = df['type_secondary'].map(lambda x: 1 if 'free_kick_shot' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('free_kick_shot','',regex=True)
df['Ground duel'] = df['type_secondary'].map(lambda x: 1 if 'ground_duel' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('ground_duel','',regex=True)
df['Hand pass'] = df['type_secondary'].map(lambda x: 1 if 'hand_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('hand_pass','',regex=True)
df['Head pass'] = df['type_secondary'].map(lambda x: 1 if 'head_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('head_pass','',regex=True)
df['Head shot'] = df['type_secondary'].map(lambda x: 1 if 'head_shot' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('head_shot','',regex=True)
df['Key pass'] = df['type_secondary'].map(lambda x: 1 if 'key_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('key_pass','',regex=True)
df['Lateral pass'] = df['type_secondary'].map(lambda x: 1 if 'lateral_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('lateral_pass','',regex=True)
df['Linkup play'] = df['type_secondary'].map(lambda x: 1 if 'linkup_play' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('linkup_play','',regex=True)
df['Long pass'] = df['type_secondary'].map(lambda x: 1 if 'long_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('long_pass','',regex=True)
df['Loose ball duel'] = df['type_secondary'].map(lambda x: 1 if 'loose_ball_duel' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('loose_ball_duel','',regex=True)
df['Loss'] = df['type_secondary'].map(lambda x: 1 if 'loss' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('loss','',regex=True)
df['Offensive duel'] = df['type_secondary'].map(lambda x: 1 if 'offensive_duel' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('offensive_duel','',regex=True)
df['Opportunity'] = df['type_secondary'].map(lambda x: 1 if 'opportunity' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('opportunity','',regex=True)
df['Pass into final third'] = df['type_secondary'].map(lambda x: 1 if 'pass_to_final_third' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('pass_to_final_third','',regex=True)
df['Penalty conceded goal'] = df['type_secondary'].map(lambda x: 1 if 'penalty_conceded_goal' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('penalty_conceded_goal','',regex=True)
df['Penalty foul'] = df['type_secondary'].map(lambda x: 1 if 'penalty_foul' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('penalty_foul','',regex=True)
df['Goal'] = df['type_secondary'].map(lambda x: 1 if 'goal' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('goal','',regex=True)
df['Penalty goal'] = df['type_secondary'].map(lambda x: 1 if 'penalty_goal' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('penalty_goal','',regex=True)
df['Penalty save'] = df['type_secondary'].map(lambda x: 1 if 'penalty_save' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('penalty_save','',regex=True)
df['Progressive pass'] = df['type_secondary'].map(lambda x: 1 if 'progressive_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('progressive_pass','',regex=True)
df['Progressive run'] = df['type_secondary'].map(lambda x: 1 if 'progressive_run' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('progressive_run','',regex=True)
df['Recovery'] = df['type_secondary'].map(lambda x: 1 if 'recovery' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('recovery','',regex=True)
df['Red card'] = df['type_secondary'].map(lambda x: 1 if 'red_card' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('red_card','',regex=True)
df['Save with reflex'] = df['type_secondary'].map(lambda x: 1 if 'save_with_reflex' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('save_with_reflex','',regex=True)
df['Shot after corner'] = df['type_secondary'].map(lambda x: 1 if 'shot_after_corner' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('shot_after_corner','',regex=True)
df['Shot after free kick'] = df['type_secondary'].map(lambda x: 1 if 'shot_after_free_kick' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('shot_after_free_kick','',regex=True)
df['Shot after throw in'] = df['type_secondary'].map(lambda x: 1 if 'shot_after_throw_in' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('shot_after_throw_in','',regex=True)
df['Sliding tackle'] = df['type_secondary'].map(lambda x: 1 if 'sliding_tackle' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('sliding_tackle','',regex=True)
df['Smart pass'] = df['type_secondary'].map(lambda x: 1 if 'smart_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('smart_pass','',regex=True)
df['Through pass'] = df['type_secondary'].map(lambda x: 1 if 'through_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('through_pass','',regex=True)
df['Touch in box'] = df['type_secondary'].map(lambda x: 1 if 'touch_in_box' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('touch_in_box','',regex=True)
df['Under pressure'] = df['type_secondary'].map(lambda x: 1 if 'under_pressure' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('under_pressure','',regex=True)
df['Whistle'] = df['type_secondary'].map(lambda x: 1 if 'whistle' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('whistle','',regex=True)
df['Yellow card'] = df['type_secondary'].map(lambda x: 1 if 'yellow_card' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('yellow_card','',regex=True)
df['type_secondary'] = df['type_secondary'].str.replace('pass','',regex=True)
df['Save'] = df['type_secondary'].map(lambda x: 1 if 'save' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('save','',regex=True)
df['Foul'] = df['type_secondary'].map(lambda x: 1 if 'foul' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('foul','',regex=True)
df['Interception'] = df['type_secondary'].map(lambda x: 1 if 'interception' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('interception','',regex=True)
df['Acceleration'] = df['type_secondary'].map(lambda x: 1 if 'acceleration' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('acceleration','',regex=True)
print('U15 data talt for aktioner')
df = pd.melt(df, id_vars = ['Action id','matchId','matchPeriod','minute','second','matchTimestamp','videoTimestamp','relatedEventId','type_primary','Action location start x','Action location start y','Team id','Team name','Team formation','Opponent team id','Opponent team name','Opponent team formation','Player id','Player name','Player position','Pass accurate','Pass angle','Pass height','Pass length','Pass recipient id','Pass recipient name','Pass recipient position','Pass end x','Pass end y','Shot bodypart','Shot is goal','Shot on target','Shot goalzone','Shot xg','postShotXg','Shot goalkeeper','Shot goalkeeper id','Shot goalkeeper name','Possession id','Possession duration','Possession type','eventsNumber','Possession event index','Possession start location x','Possession start location y','Possession end location x','Possession end location y','Possession team id','Possession team name','Possession team formation','Possession with shot','Possession with shot on goal','Possession with goal','Possession flank','Possession xg','Ground duel type','Ground duel kept possession','Ground duel progressed with ball','Ground duel stopped progress','Ground duel recovered possession','keptPossession','Ground duel side','Ground duel related duel id','Ground duel opponent id','Ground duel opponent name','Ground duel opponent position','Aerial duelfirstTouch','Aerial duel height','Aerial duel related duel id','Aerial duel opponent id','Aerial duel opponent name','Aerial duel opponent position','Aerial duel opponent height','Infraction yellow card','Infraction red card','Infraction type','Infraction opponent id','Infraction opponent name','Infraction opponent position','Carry progression','Carry end location x','Carry end location y'],value_vars=['Pass to penalty area','Back pass','Short or medium pass','Aerial duel','Shot assist','Shot block','Shot','Second assist','Third assist','Assist','Ball out','Carry','Conceded goal','Counterpressing recovery','Cross blocked','Deep completed cross','Free kick cross','Cross','Deep completion','Defensive duel','Dribbled past attempt','Dribble','Forward pass','Foul suffered','Free kick shot','Ground duel','Hand pass','Head pass','Head shot','Key pass','Lateral pass','Linkup play','Long pass','Loose ball duel','Loss','Offensive duel','Opportunity','Pass into final third','Penalty conceded goal','Penalty foul','Penalty goal','Penalty save','Progressive pass','Progressive run','Recovery','Red card','Save with reflex','Shot after corner','Shot after free kick','Shot after throw in','Sliding tackle','Smart pass','Through pass','Touch in box','Under pressure','Whistle','Yellow card','Pass','Save','Foul','Interception','Goal','Acceleration']) 
df = df.drop(df[df.value == 0].index)
print('U15 data tilpasset til app')

connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 22-23/U15 Ligaen/'


service_client = ShareServiceClient.from_connection_string(connection_string)
share_client = service_client.get_share_client(share_name)
directory_client = share_client.get_directory_client(dir_path)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
print('U15 kampdetaljer hentet fra database')
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})
df1 = kampdetaljer.merge(df)

df1['date'] = df1['date'].astype(str)
df1['date'] = df1['date'].apply(lambda x: parser.parse(x))

# Sort the dataframe by the 'date' column
df1 = df1.sort_values(by='date',ascending=False)

# Format the 'date' column to day-month-year format
df1['date'] = df1['date'].apply(lambda x: x.strftime('%d-%m-%Y'))
        
df1.to_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\U15 eventdata.csv')
print('U15 Data hentet')

from azure.storage.fileshare import ShareServiceClient
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
import os
connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 22-23/U17 Ligaen/'


service_client = ShareServiceClient.from_connection_string(connection_string)
share_client = service_client.get_share_client(share_name)
directory_client = share_client.get_directory_client(dir_path)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchEvents' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))

find_json_files(directory_client)

# Create an empty list to store the events data
events_list = []

# Iterate over each item in the json_files list and append its 'events' data to the events_list
for item in json_files:
    events_list.extend(item['events'])

# Convert the events_list to a DataFrame
df = pd.DataFrame(events_list)
print('U17 data hentet fra database')
type_cols = pd.json_normalize(df['type'])
type_cols.columns = ['type_primary','type_secondary']
df = pd.concat([df.drop('type', axis=1), type_cols], axis=1)
df = df.rename(columns= {'id':'Action id'})
type_cols = pd.json_normalize(df['location'])
type_cols.columns = ['x','y']
df = pd.concat([df.drop('location', axis=1), type_cols], axis=1)
df = df.rename(columns={'x' : 'Action location start x', 'y' : 'Action location start y'})
type_cols = pd.json_normalize(df['team'])
type_cols.columns = ['id','name','formation']
df = pd.concat([df.drop('team', axis=1), type_cols], axis=1)
df = df.rename(columns={'id' : 'Team id', 'name' : 'Team name','formation':'Team formation'})
type_cols = pd.json_normalize(df['opponentTeam'])
type_cols.columns = ['id','name','formation']
df = pd.concat([df.drop('opponentTeam', axis=1), type_cols], axis=1)
df = df.rename(columns={'id' : 'Opponent team id', 'name' : 'Opponent team name','formation':'Opponent team formation'})
type_cols = pd.json_normalize(df['player'])
type_cols.columns = ['id','name','position']
df = pd.concat([df.drop('player', axis=1), type_cols], axis=1)
df = df.rename(columns={'id' : 'Player id', 'name' : 'Player name','position':'Player position'})
type_cols = pd.json_normalize(df['pass'])
type_cols.columns = ['accurate','angle','height','length','recipient','id','name','position','endLocation']
df = pd.concat([df.drop('pass', axis=1), type_cols], axis=1)
df = df.rename(columns={'accurate' : 'Pass accurate', 'angle' : 'Pass angle','height':'Pass height','length':'Pass length','recipient':'Pass recipient id','id':'Pass recipient name','name':'Pass recipient position','position':'Pass end x','endLocation':'Pass end y'})
type_cols = pd.json_normalize(df['shot'])
type_cols.columns = ['bodypart','isGoal','onTarget','goalZone','xg','postShotXg','goalkeeperActionId','goalkeeper','id','name']
df = pd.concat([df.drop('shot', axis=1), type_cols], axis=1)
df = df.rename(columns={'bodypart' : 'Shot bodypart', 'isGoal' : 'Shot is goal','onTarget':'Shot on target','goalZone':'Shot goalzone','xg':'Shot xg','postShotxg':'Shot post shot xg','goalkeeperActionId':'Shot goalkeeper action id','goalkeeper':'Shot goalkeeper','id':'Shot goalkeeper id','name':'Shot goalkeeper name'})
type_cols = pd.json_normalize(df['possession'])
type_cols.columns = ['id','duration','types','eventsNumber','eventIndex','location','x','y','x','y','id','name','formation','withShot','withShotOnGoal','withGoal','flank','xg',]
df = pd.concat([df.drop('possession', axis=1), type_cols], axis=1)
df = df.rename(columns={'id' : 'Possession id', 'duration' : 'Possession duration','types':'Possession type','eventsnumber':'Possession eventsnumber','eventIndex':'Possession event index','location':'Possession location'})
# create unique names for duplicate columns
dup_cols = [col for col in df.columns if df.columns.tolist().count(col) > 1]
unique_cols = [f'{col}_{i}' if col in dup_cols else col for i, col in enumerate(df.columns)]

# rename the dataframe columns with the unique names
df.columns = unique_cols

df = df.rename(columns={'Possession id_44':'Possession id','x_50':'Possession start location x','y_51':'Possession start location y','x_52':'Possession end location x','y_53':'Possession end location y','Possession id_54':'Possession team id','name':'Possession team name','formation':'Possession team formation','withShot':'Possession with shot','withShotOnGoal':'Possession with shot on goal','withGoal':'Possession with goal','flank':'Possession flank','xg':'Possession xg'})
type_cols = pd.json_normalize(df['groundDuel'])
type_cols.columns = ['opponent','id','name','position','duelType','keptPossession','progressedWithBall','stoppedProgress','recoveredPossession','takeOn','side','relatedDuelId']
df = pd.concat([df.drop('groundDuel', axis=1), type_cols], axis=1)
df = df.rename(columns={'opponent':'Ground duel type','id':'Ground duel kept possession','name':'Ground duel progressed with ball','position':'Ground duel stopped progress','duelType':'Ground duel recovered possession','keptPosession':'Ground duel takeon','progressedWithBall':'Ground duel side','stoppedProgress':'Ground duel related duel id','recoveredPossession':'Ground duel opponent id','takeOn':'Ground duel opponent name','side':'Ground duel opponent position','relatedDuelId':'slettes'})
#df = df.rename(columns={'bodypart' : 'Shot bodypart', 'isGoal' : 'Shot is goal','onTarget':'Shot on target','goalZone':'Shot goalzone','xg':'Shot xg','postShotxg':'Shot post shot xg','goalkeeperActionId':'Shot goalkeeper action id','goalkeeper':'Shot goalkeeper','id':'Shot goalkeeper id','name':'Shot goalkeeper name'})
type_cols = pd.json_normalize(df['aerialDuel'])
type_cols.columns = ['opponent','id','name','position','height','firstTouch','height','relatedDuelId']
df = pd.concat([df.drop('aerialDuel', axis=1), type_cols], axis=1)
df = df.rename(columns={'opponent':'Aerial duelfirstTouch','id':'Aerial duel height','name':'Aerial duel related duel id','position':'Aerial duel opponent id','height':'Aerial duel opponent name','firstTouch':'Aerial duel opponent position','relatedDuelId':'slettes'})
dup_cols = [col for col in df.columns if df.columns.tolist().count(col) > 1]
unique_cols = [f'{col}_{i}' if col in dup_cols else col for i, col in enumerate(df.columns)]
# rename the dataframe columns with the unique names
df.columns = unique_cols
df = df.rename(columns={'Aerial duel opponent name_78':'Aerial duel opponent height','Aerial duel opponent name_76':'Aerial duel opponent name'})
type_cols = pd.json_normalize(df['infraction'])
type_cols.columns = ['yellowCard','redCard','type','opponent','id','name','position']
df = pd.concat([df.drop('infraction', axis=1), type_cols], axis=1)
df = df.rename(columns={'yellowCard':'Infraction yellow card','redCard':'Infraction red card','type':'Infraction type','opponent':'Infraction opponent id','id':'Infraction opponent name','name':'Infraction opponent position','position':'slettes'})
type_cols = pd.json_normalize(df['carry'])
type_cols.columns = ['progression','x','y']
df = pd.concat([df.drop('carry', axis=1), type_cols], axis=1)
df = df.rename(columns={'progression':'Carry progression','x':'Carry end location x','y':'Carry end location y'})
df = df[df['Team name'].str.contains('Horsens')|df['Opponent team name'].str.contains('Horsens')]
print('U17 data sorteret til kun at indeholde egne kampe')

df['type_secondary'] = df['type_secondary'].astype(str)
df['type_secondary'] = df['type_secondary'].str.replace('[','',regex=True)
df['type_secondary'] = df['type_secondary'].str.replace(']','',regex=True)
df['type_secondary'] = df['type_secondary'].str.replace('"','',regex=True)
df['type_secondary'] = df['type_secondary'].str.replace(',','',regex=True)
df['type_secondary'] = df['type_secondary'].str.replace("'",'',regex=True)

df['Pass'] = df['type_secondary'].map(lambda x: 1 if 'pass' in x else 0)
df['Pass to penalty area'] = df['type_secondary'].map(lambda x: 1 if 'pass_to_penalty_area' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('pass_to_penalty_area','',regex=True)
df['Back pass'] = df['type_secondary'].map(lambda x: 1 if 'back_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('back_pass','',regex=True)
df['Short or medium pass'] = df['type_secondary'].map(lambda x: 1 if 'short_or_medium_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('short_or_medium_pass','',regex=True)
df['Aerial duel'] = df['type_secondary'].map(lambda x: 1 if 'aerial_duel' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('aerial_duel','',regex=True)
df['Shot assist'] = df['type_secondary'].map(lambda x: 1 if 'shot_assist' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('shot_assist','',regex=True)
df['Shot block'] = df['type_secondary'].map(lambda x: 1 if 'shot_block' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('shot_block','',regex=True)
df['Shot'] = df['type_secondary'].map(lambda x: 1 if 'shot' in x else 0)
df['Second assist'] = df['type_secondary'].map(lambda x: 1 if 'second_assist' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('second_assist','',regex=True)
df['Third assist'] = df['type_secondary'].map(lambda x: 1 if 'third_assist' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('third_assist','',regex=True)
df['Assist'] = df['type_secondary'].map(lambda x: 1 if 'assist' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('assist','',regex=True)
df['Ball out'] = df['type_secondary'].map(lambda x: 1 if 'ball_out' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('ball_out','',regex=True)
df['Carry'] = df['type_secondary'].map(lambda x: 1 if 'carry' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('carry','',regex=True)
df['Conceded goal'] = df['type_secondary'].map(lambda x: 1 if 'conceded_goal' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('conceded_goal','',regex=True)
df['Counterpressing recovery'] = df['type_secondary'].map(lambda x: 1 if 'counterpressing_recovery' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('counterpressing_recovery','',regex=True)
df['Cross blocked'] = df['type_secondary'].map(lambda x: 1 if 'cross_blocked' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('cross_blocked','',regex=True)
df['Deep completed cross'] = df['type_secondary'].map(lambda x: 1 if 'deep_completed_cross' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('deep_completed_cross','',regex=True)
df['Free kick cross'] = df['type_secondary'].map(lambda x: 1 if 'free_kick_cross' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('free_kick_cross','',regex=True)
df['Cross'] = df['type_secondary'].map(lambda x: 1 if 'cross' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('cross','',regex=True)
df['Deep completion'] = df['type_secondary'].map(lambda x: 1 if 'deep_completion' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('deep_completion','',regex=True)
df['Defensive duel'] = df['type_secondary'].map(lambda x: 1 if 'defensive_duel' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('defensive_duel','',regex=True)
df['Dribble'] = df['type_secondary'].map(lambda x: 1 if 'dribble' in x else 0)
df['Dribbled past attempt'] = df['type_secondary'].map(lambda x: 1 if 'dribbled_past_attempt' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('dribbled_past_attempt','',regex=True)
df['type_secondary'] = df['type_secondary'].str.replace('dribble','',regex=True)
df['Forward pass'] = df['type_secondary'].map(lambda x: 1 if 'forward_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('forward_pass','',regex=True)
df['Foul suffered'] = df['type_secondary'].map(lambda x: 1 if 'foul_suffered' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('foul_suffered','',regex=True)
df['Free kick shot'] = df['type_secondary'].map(lambda x: 1 if 'free_kick_shot' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('free_kick_shot','',regex=True)
df['Ground duel'] = df['type_secondary'].map(lambda x: 1 if 'ground_duel' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('ground_duel','',regex=True)
df['Hand pass'] = df['type_secondary'].map(lambda x: 1 if 'hand_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('hand_pass','',regex=True)
df['Head pass'] = df['type_secondary'].map(lambda x: 1 if 'head_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('head_pass','',regex=True)
df['Head shot'] = df['type_secondary'].map(lambda x: 1 if 'head_shot' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('head_shot','',regex=True)
df['Key pass'] = df['type_secondary'].map(lambda x: 1 if 'key_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('key_pass','',regex=True)
df['Lateral pass'] = df['type_secondary'].map(lambda x: 1 if 'lateral_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('lateral_pass','',regex=True)
df['Linkup play'] = df['type_secondary'].map(lambda x: 1 if 'linkup_play' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('linkup_play','',regex=True)
df['Long pass'] = df['type_secondary'].map(lambda x: 1 if 'long_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('long_pass','',regex=True)
df['Loose ball duel'] = df['type_secondary'].map(lambda x: 1 if 'loose_ball_duel' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('loose_ball_duel','',regex=True)
df['Loss'] = df['type_secondary'].map(lambda x: 1 if 'loss' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('loss','',regex=True)
df['Offensive duel'] = df['type_secondary'].map(lambda x: 1 if 'offensive_duel' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('offensive_duel','',regex=True)
df['Opportunity'] = df['type_secondary'].map(lambda x: 1 if 'opportunity' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('opportunity','',regex=True)
df['Pass into final third'] = df['type_secondary'].map(lambda x: 1 if 'pass_to_final_third' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('pass_to_final_third','',regex=True)
df['Penalty conceded goal'] = df['type_secondary'].map(lambda x: 1 if 'penalty_conceded_goal' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('penalty_conceded_goal','',regex=True)
df['Penalty foul'] = df['type_secondary'].map(lambda x: 1 if 'penalty_foul' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('penalty_foul','',regex=True)
df['Goal'] = df['type_secondary'].map(lambda x: 1 if 'goal' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('goal','',regex=True)
df['Penalty goal'] = df['type_secondary'].map(lambda x: 1 if 'penalty_goal' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('penalty_goal','',regex=True)
df['Penalty save'] = df['type_secondary'].map(lambda x: 1 if 'penalty_save' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('penalty_save','',regex=True)
df['Progressive pass'] = df['type_secondary'].map(lambda x: 1 if 'progressive_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('progressive_pass','',regex=True)
df['Progressive run'] = df['type_secondary'].map(lambda x: 1 if 'progressive_run' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('progressive_run','',regex=True)
df['Recovery'] = df['type_secondary'].map(lambda x: 1 if 'recovery' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('recovery','',regex=True)
df['Red card'] = df['type_secondary'].map(lambda x: 1 if 'red_card' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('red_card','',regex=True)
df['Save with reflex'] = df['type_secondary'].map(lambda x: 1 if 'save_with_reflex' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('save_with_reflex','',regex=True)
df['Shot after corner'] = df['type_secondary'].map(lambda x: 1 if 'shot_after_corner' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('shot_after_corner','',regex=True)
df['Shot after free kick'] = df['type_secondary'].map(lambda x: 1 if 'shot_after_free_kick' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('shot_after_free_kick','',regex=True)
df['Shot after throw in'] = df['type_secondary'].map(lambda x: 1 if 'shot_after_throw_in' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('shot_after_throw_in','',regex=True)
df['Sliding tackle'] = df['type_secondary'].map(lambda x: 1 if 'sliding_tackle' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('sliding_tackle','',regex=True)
df['Smart pass'] = df['type_secondary'].map(lambda x: 1 if 'smart_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('smart_pass','',regex=True)
df['Through pass'] = df['type_secondary'].map(lambda x: 1 if 'through_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('through_pass','',regex=True)
df['Touch in box'] = df['type_secondary'].map(lambda x: 1 if 'touch_in_box' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('touch_in_box','',regex=True)
df['Under pressure'] = df['type_secondary'].map(lambda x: 1 if 'under_pressure' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('under_pressure','',regex=True)
df['Whistle'] = df['type_secondary'].map(lambda x: 1 if 'whistle' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('whistle','',regex=True)
df['Yellow card'] = df['type_secondary'].map(lambda x: 1 if 'yellow_card' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('yellow_card','',regex=True)
df['type_secondary'] = df['type_secondary'].str.replace('pass','',regex=True)
df['Save'] = df['type_secondary'].map(lambda x: 1 if 'save' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('save','',regex=True)
df['Foul'] = df['type_secondary'].map(lambda x: 1 if 'foul' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('foul','',regex=True)
df['Interception'] = df['type_secondary'].map(lambda x: 1 if 'interception' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('interception','',regex=True)
df['Acceleration'] = df['type_secondary'].map(lambda x: 1 if 'acceleration' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('acceleration','',regex=True)
print('U17 data talt for aktioner')
df = pd.melt(df, id_vars = ['Action id','matchId','matchPeriod','minute','second','matchTimestamp','videoTimestamp','relatedEventId','type_primary','Action location start x','Action location start y','Team id','Team name','Team formation','Opponent team id','Opponent team name','Opponent team formation','Player id','Player name','Player position','Pass accurate','Pass angle','Pass height','Pass length','Pass recipient id','Pass recipient name','Pass recipient position','Pass end x','Pass end y','Shot bodypart','Shot is goal','Shot on target','Shot goalzone','Shot xg','postShotXg','Shot goalkeeper','Shot goalkeeper id','Shot goalkeeper name','Possession id','Possession duration','Possession type','eventsNumber','Possession event index','Possession start location x','Possession start location y','Possession end location x','Possession end location y','Possession team id','Possession team name','Possession team formation','Possession with shot','Possession with shot on goal','Possession with goal','Possession flank','Possession xg','Ground duel type','Ground duel kept possession','Ground duel progressed with ball','Ground duel stopped progress','Ground duel recovered possession','keptPossession','Ground duel side','Ground duel related duel id','Ground duel opponent id','Ground duel opponent name','Ground duel opponent position','Aerial duelfirstTouch','Aerial duel height','Aerial duel related duel id','Aerial duel opponent id','Aerial duel opponent name','Aerial duel opponent position','Aerial duel opponent height','Infraction yellow card','Infraction red card','Infraction type','Infraction opponent id','Infraction opponent name','Infraction opponent position','Carry progression','Carry end location x','Carry end location y'],value_vars=['Pass to penalty area','Back pass','Short or medium pass','Aerial duel','Shot assist','Shot block','Shot','Second assist','Third assist','Assist','Ball out','Carry','Conceded goal','Counterpressing recovery','Cross blocked','Deep completed cross','Free kick cross','Cross','Deep completion','Defensive duel','Dribbled past attempt','Dribble','Forward pass','Foul suffered','Free kick shot','Ground duel','Hand pass','Head pass','Head shot','Key pass','Lateral pass','Linkup play','Long pass','Loose ball duel','Loss','Offensive duel','Opportunity','Pass into final third','Penalty conceded goal','Penalty foul','Penalty goal','Penalty save','Progressive pass','Progressive run','Recovery','Red card','Save with reflex','Shot after corner','Shot after free kick','Shot after throw in','Sliding tackle','Smart pass','Through pass','Touch in box','Under pressure','Whistle','Yellow card','Pass','Save','Foul','Interception','Goal','Acceleration']) 
df = df.drop(df[df.value == 0].index)
print('U17 data tilpasset til app')

connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 22-23/U17 Ligaen/'


service_client = ShareServiceClient.from_connection_string(connection_string)
share_client = service_client.get_share_client(share_name)
directory_client = share_client.get_directory_client(dir_path)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
print('U17 kampdetaljer hentet fra database')
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})
df1 = kampdetaljer.merge(df)

df1['date'] = df1['date'].astype(str)
df1['date'] = df1['date'].apply(lambda x: parser.parse(x))

# Sort the dataframe by the 'date' column
df1 = df1.sort_values(by='date',ascending=False)

# Format the 'date' column to day-month-year format
df1['date'] = df1['date'].apply(lambda x: x.strftime('%d-%m-%Y'))
        
df1.to_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\U17 eventdata.csv')
print(' U17 Data hentet')

from azure.storage.fileshare import ShareServiceClient
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
import os
connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 22-23/U19 Ligaen/'


service_client = ShareServiceClient.from_connection_string(connection_string)
share_client = service_client.get_share_client(share_name)
directory_client = share_client.get_directory_client(dir_path)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchEvents' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))

find_json_files(directory_client)

# Create an empty list to store the events data
events_list = []

# Iterate over each item in the json_files list and append its 'events' data to the events_list
for item in json_files:
    events_list.extend(item['events'])

# Convert the events_list to a DataFrame
df = pd.DataFrame(events_list)
print('U19 data hentet fra database')
type_cols = pd.json_normalize(df['type'])
type_cols.columns = ['type_primary','type_secondary']
df = pd.concat([df.drop('type', axis=1), type_cols], axis=1)
df = df.rename(columns= {'id':'Action id'})
type_cols = pd.json_normalize(df['location'])
type_cols.columns = ['x','y']
df = pd.concat([df.drop('location', axis=1), type_cols], axis=1)
df = df.rename(columns={'x' : 'Action location start x', 'y' : 'Action location start y'})
type_cols = pd.json_normalize(df['team'])
type_cols.columns = ['id','name','formation']
df = pd.concat([df.drop('team', axis=1), type_cols], axis=1)
df = df.rename(columns={'id' : 'Team id', 'name' : 'Team name','formation':'Team formation'})
type_cols = pd.json_normalize(df['opponentTeam'])
type_cols.columns = ['id','name','formation']
df = pd.concat([df.drop('opponentTeam', axis=1), type_cols], axis=1)
df = df.rename(columns={'id' : 'Opponent team id', 'name' : 'Opponent team name','formation':'Opponent team formation'})
type_cols = pd.json_normalize(df['player'])
type_cols.columns = ['id','name','position']
df = pd.concat([df.drop('player', axis=1), type_cols], axis=1)
df = df.rename(columns={'id' : 'Player id', 'name' : 'Player name','position':'Player position'})
type_cols = pd.json_normalize(df['pass'])
type_cols.columns = ['accurate','angle','height','length','recipient','id','name','position','endLocation']
df = pd.concat([df.drop('pass', axis=1), type_cols], axis=1)
df = df.rename(columns={'accurate' : 'Pass accurate', 'angle' : 'Pass angle','height':'Pass height','length':'Pass length','recipient':'Pass recipient id','id':'Pass recipient name','name':'Pass recipient position','position':'Pass end x','endLocation':'Pass end y'})
type_cols = pd.json_normalize(df['shot'])
type_cols.columns = ['bodypart','isGoal','onTarget','goalZone','xg','postShotXg','goalkeeperActionId','goalkeeper','id','name']
df = pd.concat([df.drop('shot', axis=1), type_cols], axis=1)
df = df.rename(columns={'bodypart' : 'Shot bodypart', 'isGoal' : 'Shot is goal','onTarget':'Shot on target','goalZone':'Shot goalzone','xg':'Shot xg','postShotxg':'Shot post shot xg','goalkeeperActionId':'Shot goalkeeper action id','goalkeeper':'Shot goalkeeper','id':'Shot goalkeeper id','name':'Shot goalkeeper name'})
type_cols = pd.json_normalize(df['possession'])
type_cols.columns = ['id','duration','types','eventsNumber','eventIndex','location','x','y','x','y','id','name','formation','withShot','withShotOnGoal','withGoal','flank','xg',]
df = pd.concat([df.drop('possession', axis=1), type_cols], axis=1)
df = df.rename(columns={'id' : 'Possession id', 'duration' : 'Possession duration','types':'Possession type','eventsnumber':'Possession eventsnumber','eventIndex':'Possession event index','location':'Possession location'})
# create unique names for duplicate columns
dup_cols = [col for col in df.columns if df.columns.tolist().count(col) > 1]
unique_cols = [f'{col}_{i}' if col in dup_cols else col for i, col in enumerate(df.columns)]

# rename the dataframe columns with the unique names
df.columns = unique_cols

df = df.rename(columns={'Possession id_44':'Possession id','x_50':'Possession start location x','y_51':'Possession start location y','x_52':'Possession end location x','y_53':'Possession end location y','Possession id_54':'Possession team id','name':'Possession team name','formation':'Possession team formation','withShot':'Possession with shot','withShotOnGoal':'Possession with shot on goal','withGoal':'Possession with goal','flank':'Possession flank','xg':'Possession xg'})
type_cols = pd.json_normalize(df['groundDuel'])
type_cols.columns = ['opponent','id','name','position','duelType','keptPossession','progressedWithBall','stoppedProgress','recoveredPossession','takeOn','side','relatedDuelId']
df = pd.concat([df.drop('groundDuel', axis=1), type_cols], axis=1)
df = df.rename(columns={'opponent':'Ground duel type','id':'Ground duel kept possession','name':'Ground duel progressed with ball','position':'Ground duel stopped progress','duelType':'Ground duel recovered possession','keptPosession':'Ground duel takeon','progressedWithBall':'Ground duel side','stoppedProgress':'Ground duel related duel id','recoveredPossession':'Ground duel opponent id','takeOn':'Ground duel opponent name','side':'Ground duel opponent position','relatedDuelId':'slettes'})
#df = df.rename(columns={'bodypart' : 'Shot bodypart', 'isGoal' : 'Shot is goal','onTarget':'Shot on target','goalZone':'Shot goalzone','xg':'Shot xg','postShotxg':'Shot post shot xg','goalkeeperActionId':'Shot goalkeeper action id','goalkeeper':'Shot goalkeeper','id':'Shot goalkeeper id','name':'Shot goalkeeper name'})
type_cols = pd.json_normalize(df['aerialDuel'])
type_cols.columns = ['opponent','id','name','position','height','firstTouch','height','relatedDuelId']
df = pd.concat([df.drop('aerialDuel', axis=1), type_cols], axis=1)
df = df.rename(columns={'opponent':'Aerial duelfirstTouch','id':'Aerial duel height','name':'Aerial duel related duel id','position':'Aerial duel opponent id','height':'Aerial duel opponent name','firstTouch':'Aerial duel opponent position','relatedDuelId':'slettes'})
dup_cols = [col for col in df.columns if df.columns.tolist().count(col) > 1]
unique_cols = [f'{col}_{i}' if col in dup_cols else col for i, col in enumerate(df.columns)]
# rename the dataframe columns with the unique names
df.columns = unique_cols
df = df.rename(columns={'Aerial duel opponent name_78':'Aerial duel opponent height','Aerial duel opponent name_76':'Aerial duel opponent name'})
type_cols = pd.json_normalize(df['infraction'])
type_cols.columns = ['yellowCard','redCard','type','opponent','id','name','position']
df = pd.concat([df.drop('infraction', axis=1), type_cols], axis=1)
df = df.rename(columns={'yellowCard':'Infraction yellow card','redCard':'Infraction red card','type':'Infraction type','opponent':'Infraction opponent id','id':'Infraction opponent name','name':'Infraction opponent position','position':'slettes'})
type_cols = pd.json_normalize(df['carry'])
type_cols.columns = ['progression','x','y']
df = pd.concat([df.drop('carry', axis=1), type_cols], axis=1)
df = df.rename(columns={'progression':'Carry progression','x':'Carry end location x','y':'Carry end location y'})
df = df[df['Team name'].str.contains('Horsens')|df['Opponent team name'].str.contains('Horsens')]
print('U19 data sorteret til kun at indeholde egne kampe')

df['type_secondary'] = df['type_secondary'].astype(str)
df['type_secondary'] = df['type_secondary'].str.replace('[','',regex=True)
df['type_secondary'] = df['type_secondary'].str.replace(']','',regex=True)
df['type_secondary'] = df['type_secondary'].str.replace('"','',regex=True)
df['type_secondary'] = df['type_secondary'].str.replace(',','',regex=True)
df['type_secondary'] = df['type_secondary'].str.replace("'",'',regex=True)

df['Pass'] = df['type_secondary'].map(lambda x: 1 if 'pass' in x else 0)
df['Pass to penalty area'] = df['type_secondary'].map(lambda x: 1 if 'pass_to_penalty_area' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('pass_to_penalty_area','',regex=True)
df['Back pass'] = df['type_secondary'].map(lambda x: 1 if 'back_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('back_pass','',regex=True)
df['Short or medium pass'] = df['type_secondary'].map(lambda x: 1 if 'short_or_medium_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('short_or_medium_pass','',regex=True)
df['Aerial duel'] = df['type_secondary'].map(lambda x: 1 if 'aerial_duel' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('aerial_duel','',regex=True)
df['Shot assist'] = df['type_secondary'].map(lambda x: 1 if 'shot_assist' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('shot_assist','',regex=True)
df['Shot block'] = df['type_secondary'].map(lambda x: 1 if 'shot_block' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('shot_block','',regex=True)
df['Shot'] = df['type_secondary'].map(lambda x: 1 if 'shot' in x else 0)
df['Second assist'] = df['type_secondary'].map(lambda x: 1 if 'second_assist' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('second_assist','',regex=True)
df['Third assist'] = df['type_secondary'].map(lambda x: 1 if 'third_assist' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('third_assist','',regex=True)
df['Assist'] = df['type_secondary'].map(lambda x: 1 if 'assist' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('assist','',regex=True)
df['Ball out'] = df['type_secondary'].map(lambda x: 1 if 'ball_out' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('ball_out','',regex=True)
df['Carry'] = df['type_secondary'].map(lambda x: 1 if 'carry' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('carry','',regex=True)
df['Conceded goal'] = df['type_secondary'].map(lambda x: 1 if 'conceded_goal' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('conceded_goal','',regex=True)
df['Counterpressing recovery'] = df['type_secondary'].map(lambda x: 1 if 'counterpressing_recovery' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('counterpressing_recovery','',regex=True)
df['Cross blocked'] = df['type_secondary'].map(lambda x: 1 if 'cross_blocked' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('cross_blocked','',regex=True)
df['Deep completed cross'] = df['type_secondary'].map(lambda x: 1 if 'deep_completed_cross' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('deep_completed_cross','',regex=True)
df['Free kick cross'] = df['type_secondary'].map(lambda x: 1 if 'free_kick_cross' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('free_kick_cross','',regex=True)
df['Cross'] = df['type_secondary'].map(lambda x: 1 if 'cross' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('cross','',regex=True)
df['Deep completion'] = df['type_secondary'].map(lambda x: 1 if 'deep_completion' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('deep_completion','',regex=True)
df['Defensive duel'] = df['type_secondary'].map(lambda x: 1 if 'defensive_duel' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('defensive_duel','',regex=True)
df['Dribble'] = df['type_secondary'].map(lambda x: 1 if 'dribble' in x else 0)
df['Dribbled past attempt'] = df['type_secondary'].map(lambda x: 1 if 'dribbled_past_attempt' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('dribbled_past_attempt','',regex=True)
df['type_secondary'] = df['type_secondary'].str.replace('dribble','',regex=True)
df['Forward pass'] = df['type_secondary'].map(lambda x: 1 if 'forward_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('forward_pass','',regex=True)
df['Foul suffered'] = df['type_secondary'].map(lambda x: 1 if 'foul_suffered' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('foul_suffered','',regex=True)
df['Free kick shot'] = df['type_secondary'].map(lambda x: 1 if 'free_kick_shot' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('free_kick_shot','',regex=True)
df['Ground duel'] = df['type_secondary'].map(lambda x: 1 if 'ground_duel' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('ground_duel','',regex=True)
df['Hand pass'] = df['type_secondary'].map(lambda x: 1 if 'hand_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('hand_pass','',regex=True)
df['Head pass'] = df['type_secondary'].map(lambda x: 1 if 'head_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('head_pass','',regex=True)
df['Head shot'] = df['type_secondary'].map(lambda x: 1 if 'head_shot' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('head_shot','',regex=True)
df['Key pass'] = df['type_secondary'].map(lambda x: 1 if 'key_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('key_pass','',regex=True)
df['Lateral pass'] = df['type_secondary'].map(lambda x: 1 if 'lateral_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('lateral_pass','',regex=True)
df['Linkup play'] = df['type_secondary'].map(lambda x: 1 if 'linkup_play' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('linkup_play','',regex=True)
df['Long pass'] = df['type_secondary'].map(lambda x: 1 if 'long_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('long_pass','',regex=True)
df['Loose ball duel'] = df['type_secondary'].map(lambda x: 1 if 'loose_ball_duel' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('loose_ball_duel','',regex=True)
df['Loss'] = df['type_secondary'].map(lambda x: 1 if 'loss' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('loss','',regex=True)
df['Offensive duel'] = df['type_secondary'].map(lambda x: 1 if 'offensive_duel' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('offensive_duel','',regex=True)
df['Opportunity'] = df['type_secondary'].map(lambda x: 1 if 'opportunity' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('opportunity','',regex=True)
df['Pass into final third'] = df['type_secondary'].map(lambda x: 1 if 'pass_to_final_third' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('pass_to_final_third','',regex=True)
df['Penalty conceded goal'] = df['type_secondary'].map(lambda x: 1 if 'penalty_conceded_goal' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('penalty_conceded_goal','',regex=True)
df['Penalty foul'] = df['type_secondary'].map(lambda x: 1 if 'penalty_foul' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('penalty_foul','',regex=True)
df['Goal'] = df['type_secondary'].map(lambda x: 1 if 'goal' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('goal','',regex=True)
df['Penalty goal'] = df['type_secondary'].map(lambda x: 1 if 'penalty_goal' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('penalty_goal','',regex=True)
df['Penalty save'] = df['type_secondary'].map(lambda x: 1 if 'penalty_save' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('penalty_save','',regex=True)
df['Progressive pass'] = df['type_secondary'].map(lambda x: 1 if 'progressive_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('progressive_pass','',regex=True)
df['Progressive run'] = df['type_secondary'].map(lambda x: 1 if 'progressive_run' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('progressive_run','',regex=True)
df['Recovery'] = df['type_secondary'].map(lambda x: 1 if 'recovery' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('recovery','',regex=True)
df['Red card'] = df['type_secondary'].map(lambda x: 1 if 'red_card' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('red_card','',regex=True)
df['Save with reflex'] = df['type_secondary'].map(lambda x: 1 if 'save_with_reflex' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('save_with_reflex','',regex=True)
df['Shot after corner'] = df['type_secondary'].map(lambda x: 1 if 'shot_after_corner' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('shot_after_corner','',regex=True)
df['Shot after free kick'] = df['type_secondary'].map(lambda x: 1 if 'shot_after_free_kick' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('shot_after_free_kick','',regex=True)
df['Shot after throw in'] = df['type_secondary'].map(lambda x: 1 if 'shot_after_throw_in' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('shot_after_throw_in','',regex=True)
df['Sliding tackle'] = df['type_secondary'].map(lambda x: 1 if 'sliding_tackle' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('sliding_tackle','',regex=True)
df['Smart pass'] = df['type_secondary'].map(lambda x: 1 if 'smart_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('smart_pass','',regex=True)
df['Through pass'] = df['type_secondary'].map(lambda x: 1 if 'through_pass' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('through_pass','',regex=True)
df['Touch in box'] = df['type_secondary'].map(lambda x: 1 if 'touch_in_box' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('touch_in_box','',regex=True)
df['Under pressure'] = df['type_secondary'].map(lambda x: 1 if 'under_pressure' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('under_pressure','',regex=True)
df['Whistle'] = df['type_secondary'].map(lambda x: 1 if 'whistle' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('whistle','',regex=True)
df['Yellow card'] = df['type_secondary'].map(lambda x: 1 if 'yellow_card' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('yellow_card','',regex=True)
df['type_secondary'] = df['type_secondary'].str.replace('pass','',regex=True)
df['Save'] = df['type_secondary'].map(lambda x: 1 if 'save' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('save','',regex=True)
df['Foul'] = df['type_secondary'].map(lambda x: 1 if 'foul' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('foul','',regex=True)
df['Interception'] = df['type_secondary'].map(lambda x: 1 if 'interception' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('interception','',regex=True)
df['Acceleration'] = df['type_secondary'].map(lambda x: 1 if 'acceleration' in x else 0)
df['type_secondary'] = df['type_secondary'].str.replace('acceleration','',regex=True)
print('U19 data talt for aktioner')
df = pd.melt(df, id_vars = ['Action id','matchId','matchPeriod','minute','second','matchTimestamp','videoTimestamp','relatedEventId','type_primary','Action location start x','Action location start y','Team id','Team name','Team formation','Opponent team id','Opponent team name','Opponent team formation','Player id','Player name','Player position','Pass accurate','Pass angle','Pass height','Pass length','Pass recipient id','Pass recipient name','Pass recipient position','Pass end x','Pass end y','Shot bodypart','Shot is goal','Shot on target','Shot goalzone','Shot xg','postShotXg','Shot goalkeeper','Shot goalkeeper id','Shot goalkeeper name','Possession id','Possession duration','Possession type','eventsNumber','Possession event index','Possession start location x','Possession start location y','Possession end location x','Possession end location y','Possession team id','Possession team name','Possession team formation','Possession with shot','Possession with shot on goal','Possession with goal','Possession flank','Possession xg','Ground duel type','Ground duel kept possession','Ground duel progressed with ball','Ground duel stopped progress','Ground duel recovered possession','keptPossession','Ground duel side','Ground duel related duel id','Ground duel opponent id','Ground duel opponent name','Ground duel opponent position','Aerial duelfirstTouch','Aerial duel height','Aerial duel related duel id','Aerial duel opponent id','Aerial duel opponent name','Aerial duel opponent position','Aerial duel opponent height','Infraction yellow card','Infraction red card','Infraction type','Infraction opponent id','Infraction opponent name','Infraction opponent position','Carry progression','Carry end location x','Carry end location y'],value_vars=['Pass to penalty area','Back pass','Short or medium pass','Aerial duel','Shot assist','Shot block','Shot','Second assist','Third assist','Assist','Ball out','Carry','Conceded goal','Counterpressing recovery','Cross blocked','Deep completed cross','Free kick cross','Cross','Deep completion','Defensive duel','Dribbled past attempt','Dribble','Forward pass','Foul suffered','Free kick shot','Ground duel','Hand pass','Head pass','Head shot','Key pass','Lateral pass','Linkup play','Long pass','Loose ball duel','Loss','Offensive duel','Opportunity','Pass into final third','Penalty conceded goal','Penalty foul','Penalty goal','Penalty save','Progressive pass','Progressive run','Recovery','Red card','Save with reflex','Shot after corner','Shot after free kick','Shot after throw in','Sliding tackle','Smart pass','Through pass','Touch in box','Under pressure','Whistle','Yellow card','Pass','Save','Foul','Interception','Goal','Acceleration']) 
df = df.drop(df[df.value == 0].index)
print('U19 data tilpasset til app')

connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 22-23/U19 Ligaen/'


service_client = ShareServiceClient.from_connection_string(connection_string)
share_client = service_client.get_share_client(share_name)
directory_client = share_client.get_directory_client(dir_path)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
print('U19 kampdetaljer hentet fra database')
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})
df1 = kampdetaljer.merge(df)

df1['date'] = df1['date'].astype(str)
df1['date'] = df1['date'].apply(lambda x: parser.parse(x))

# Sort the dataframe by the 'date' column
df1 = df1.sort_values(by='date',ascending=False)

# Format the 'date' column to day-month-year format
df1['date'] = df1['date'].apply(lambda x: x.strftime('%d-%m-%Y'))
        
df1.to_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\U19 eventdata.csv')
print('U19 Data hentet')

    
import gspread
import pandas as pd
import streamlit as st
import numpy as np

gc = gspread.service_account()
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1haWEtNQdhthKaSQjb2BRHlq2FLexicUOAHbjNFRAUAk/edit#gid=1984878556')
ws = sh.worksheet('Samlet')
df = pd.DataFrame(ws.get_all_records())
df.to_csv('ny wellness.csv',index=False)
print('Wellness data hentet')

from azure.storage.fileshare import ShareServiceClient
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
import os
import streamlit as st
connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 21-22/U15 Ligaen/'


service_client = ShareServiceClient.from_connection_string(connection_string)
share_client = service_client.get_share_client(share_name)
directory_client = share_client.get_directory_client(dir_path)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchAdvanceStats' in item.name:
            # If the item is a JSON file with 'MatchAdvanceStats' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
df = pd.json_normalize(json_files)
df = pd.DataFrame(df)
df.columns = df.columns.str.replace('66870','Horsens U15 sidste sæson')
df.columns = df.columns.str.replace('65133','Esbjerg U15')
df.columns = df.columns.str.replace('65132','København U15')
df.columns = df.columns.str.replace('65130','Silkeborg U15')
df.columns = df.columns.str.replace('65129','SønderjyskE U15')
df.columns = df.columns.str.replace('65128','AAB U15')
df.columns = df.columns.str.replace('65127','OB U15')
df.columns = df.columns.str.replace('65126','Vejle U15')
df.columns = df.columns.str.replace('65125','Randers U15')
df.columns = df.columns.str.replace('65124','FC Nordsjælland U15')
df.columns = df.columns.str.replace('65122','Midtjylland U15')
df.columns = df.columns.str.replace('65121','AGF U15')
df.columns = df.columns.str.replace('64359','Lyngby U15')
df.columns = df.columns.str.replace('22392','Brøndby IF U15')
#df.columns = df.columns.str.replace('general.','')
#possession_cols = [col for col in df.columns if col.startswith('possession')]
#df.columns = df.columns.where(~df.columns.str.startswith('possession.'), df.columns.str.replace('possession.', ''))
#df.columns = df.columns.str.replace('openplay.','')
#df.columns = df.columns.str.replace('attacks.','')
#df.columns = df.columns.str.replace('transitions.','')
#df.columns = df.columns.str.replace('passes.','')
#df.columns = df.columns.str.replace('defence.','')
#df.columns = df.columns.str.replace('duels.','')
#df.columns = df.columns.str.replace('flanks.','')


json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})

dfegnekampe = kampdetaljer.merge(df)
dfegnekampe['label'] = dfegnekampe['label'].astype(str)
dfegnekampe = dfegnekampe[dfegnekampe['label'].str.contains('Horsens')]
dfegnekampe.to_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Teamsheet alle kampe U15 sidste sæson.csv',index=False)

from azure.storage.fileshare import ShareServiceClient
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
import os
import streamlit as st
connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 22-23/U15 Ligaen/'


service_client = ShareServiceClient.from_connection_string(connection_string)
share_client = service_client.get_share_client(share_name)
directory_client = share_client.get_directory_client(dir_path)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchAdvanceStats' in item.name:
            # If the item is a JSON file with 'MatchAdvanceStats' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
df = pd.json_normalize(json_files)
df = pd.DataFrame(df)
df.columns = df.columns.str.replace('66870','Horsens U15')
df.columns = df.columns.str.replace('65133','Esbjerg U15')
df.columns = df.columns.str.replace('65132','København U15')
df.columns = df.columns.str.replace('65130','Silkeborg U15')
df.columns = df.columns.str.replace('65129','SønderjyskE U15')
df.columns = df.columns.str.replace('65128','AAB U15')
df.columns = df.columns.str.replace('65127','OB U15')
df.columns = df.columns.str.replace('65126','Vejle U15')
df.columns = df.columns.str.replace('65125','Randers U15')
df.columns = df.columns.str.replace('65124','FC Nordsjælland U15')
df.columns = df.columns.str.replace('65122','Midtjylland U15')
df.columns = df.columns.str.replace('65121','AGF U15')
df.columns = df.columns.str.replace('64359','Lyngby U15')
df.columns = df.columns.str.replace('22392','Brøndby IF U15')
#df.columns = df.columns.str.replace('general.','')
#possession_cols = [col for col in df.columns if col.startswith('possession')]
#df.columns = df.columns.where(~df.columns.str.startswith('possession.'), df.columns.str.replace('possession.', ''))
#df.columns = df.columns.str.replace('openplay.','')
#df.columns = df.columns.str.replace('attacks.','')
#df.columns = df.columns.str.replace('transitions.','')
#df.columns = df.columns.str.replace('passes.','')
#df.columns = df.columns.str.replace('defence.','')
#df.columns = df.columns.str.replace('duels.','')
#df.columns = df.columns.str.replace('flanks.','')


json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})

dfegnekampe = kampdetaljer.merge(df)
dfegnekampe['label'] = dfegnekampe['label'].astype(str)
#dfegnekampe = dfegnekampe[dfegnekampe['label'].str.contains('Horsens')]
dfegnekampe.to_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Teamsheet alle kampe U15.csv',index=False)

from azure.storage.fileshare import ShareServiceClient
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
import os
import streamlit as st
connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 22-23/U15 Ligaen/'
print('U15 ligaen')

service_client = ShareServiceClient.from_connection_string(connection_string)
share_client = service_client.get_share_client(share_name)
directory_client = share_client.get_directory_client(dir_path)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchAdvanceStats' in item.name:
            # If the item is a JSON file with 'MatchAdvanceStats' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
df = pd.json_normalize(json_files)
df = pd.DataFrame(df)
df.columns = df.columns.str.replace('66870','Horsens U15')
df.columns = df.columns.str.replace('65133','Esbjerg U15')
df.columns = df.columns.str.replace('65132','København U15')
df.columns = df.columns.str.replace('65130','Silkeborg U15')
df.columns = df.columns.str.replace('65129','SønderjyskE U15')
df.columns = df.columns.str.replace('65128','AAB U15')
df.columns = df.columns.str.replace('65127','OB U15')
df.columns = df.columns.str.replace('65126','Vejle U15')
df.columns = df.columns.str.replace('65125','Randers U15')
df.columns = df.columns.str.replace('65124','FC Nordsjælland U15')
df.columns = df.columns.str.replace('65122','Midtjylland U15')
df.columns = df.columns.str.replace('65121','AGF U15')
df.columns = df.columns.str.replace('64359','Lyngby U15')
df.columns = df.columns.str.replace('22392','Brøndby IF U15')
#df.columns = df.columns.str.replace('general.','')
#possession_cols = [col for col in df.columns if col.startswith('possession')]
#df.columns = df.columns.where(~df.columns.str.startswith('possession.'), df.columns.str.replace('possession.', ''))
#df.columns = df.columns.str.replace('openplay.','')
#df.columns = df.columns.str.replace('attacks.','')
#df.columns = df.columns.str.replace('transitions.','')
#df.columns = df.columns.str.replace('passes.','')
#df.columns = df.columns.str.replace('defence.','')
#df.columns = df.columns.str.replace('duels.','')
#df.columns = df.columns.str.replace('flanks.','')


json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})

dfegnekampe = kampdetaljer.merge(df)
dfegnekampe['label'] = dfegnekampe['label'].astype(str)
dfegnekampe = dfegnekampe[dfegnekampe['label'].str.contains('Horsens')]
dfegnekampe.to_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Teamsheet egne kampe U15.csv',index=False)


#Start på U17
connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 21-22/U17 Ligaen/'


service_client = ShareServiceClient.from_connection_string(connection_string)
share_client = service_client.get_share_client(share_name)
directory_client = share_client.get_directory_client(dir_path)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchAdvanceStats' in item.name:
            # If the item is a JSON file with 'MatchAdvanceStats' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
df = pd.json_normalize(json_files)
df = pd.DataFrame(df)
df.columns = df.columns.str.replace('30685','Horsens U17 sidste sæson')
df.columns = df.columns.str.replace('27148','Esbjerg U17')
df.columns = df.columns.str.replace('27144','København U17')
df.columns = df.columns.str.replace('27147','Silkeborg U17')
df.columns = df.columns.str.replace('62977','SønderjyskE U17')
df.columns = df.columns.str.replace('27142','AAB U17')
df.columns = df.columns.str.replace('27143','OB U17')
df.columns = df.columns.str.replace('27141','Vejle U17')
df.columns = df.columns.str.replace('27140','Randers U17')
df.columns = df.columns.str.replace('27149','FC Nordsjælland U17')
df.columns = df.columns.str.replace('27139','Midtjylland U17')
df.columns = df.columns.str.replace('27145','AGF U17')
df.columns = df.columns.str.replace('27152','Lyngby U17')
df.columns = df.columns.str.replace('27146','Brøndby IF U17')
#df.columns = df.columns.str.replace('general.','')
#possession_cols = [col for col in df.columns if col.startswith('possession')]
#df.columns = df.columns.where(~df.columns.str.startswith('possession.'), df.columns.str.replace('possession.', ''))
#df.columns = df.columns.str.replace('openplay.','')
#df.columns = df.columns.str.replace('attacks.','')
#df.columns = df.columns.str.replace('transitions.','')
#df.columns = df.columns.str.replace('passes.','')
#df.columns = df.columns.str.replace('defence.','')
#df.columns = df.columns.str.replace('duels.','')
#df.columns = df.columns.str.replace('flanks.','')


json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})

dfegnekampe = kampdetaljer.merge(df)
dfegnekampe['label'] = dfegnekampe['label'].astype(str)
dfegnekampe = dfegnekampe[dfegnekampe['label'].str.contains('Horsens')]
dfegnekampe.to_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Teamsheet alle kampe U17 sidste sæson.csv',index=False)

from azure.storage.fileshare import ShareServiceClient
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
import os
import streamlit as st
connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 22-23/U17 Ligaen/'


service_client = ShareServiceClient.from_connection_string(connection_string)
share_client = service_client.get_share_client(share_name)
directory_client = share_client.get_directory_client(dir_path)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchAdvanceStats' in item.name:
            # If the item is a JSON file with 'MatchAdvanceStats' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
df = pd.json_normalize(json_files)
df = pd.DataFrame(df)
df.columns = df.columns.str.replace('30685','Horsens U17')
df.columns = df.columns.str.replace('27148','Esbjerg U17')
df.columns = df.columns.str.replace('27144','København U17')
df.columns = df.columns.str.replace('27147','Silkeborg U17')
df.columns = df.columns.str.replace('62977','SønderjyskE U17')
df.columns = df.columns.str.replace('27142','AAB U17')
df.columns = df.columns.str.replace('27143','OB U17')
df.columns = df.columns.str.replace('27141','Vejle U17')
df.columns = df.columns.str.replace('27140','Randers U17')
df.columns = df.columns.str.replace('27149','FC Nordsjælland U17')
df.columns = df.columns.str.replace('27139','Midtjylland U17')
df.columns = df.columns.str.replace('27145','AGF U17')
df.columns = df.columns.str.replace('27152','Lyngby U17')
df.columns = df.columns.str.replace('27146','Brøndby IF U17')
#df.columns = df.columns.str.replace('general.','')
#possession_cols = [col for col in df.columns if col.startswith('possession')]
#df.columns = df.columns.where(~df.columns.str.startswith('possession.'), df.columns.str.replace('possession.', ''))
#df.columns = df.columns.str.replace('openplay.','')
#df.columns = df.columns.str.replace('attacks.','')
#df.columns = df.columns.str.replace('transitions.','')
#df.columns = df.columns.str.replace('passes.','')
#df.columns = df.columns.str.replace('defence.','')
#df.columns = df.columns.str.replace('duels.','')
#df.columns = df.columns.str.replace('flanks.','')


json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})

dfegnekampe = kampdetaljer.merge(df)
dfegnekampe['label'] = dfegnekampe['label'].astype(str)
#dfegnekampe = dfegnekampe[dfegnekampe['label'].str.contains('Horsens')]
dfegnekampe.to_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Teamsheet alle kampe U17.csv',index=False)

from azure.storage.fileshare import ShareServiceClient
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
import os
import streamlit as st
connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 22-23/U17 Ligaen/'

print('U17 data hentet')
service_client = ShareServiceClient.from_connection_string(connection_string)
share_client = service_client.get_share_client(share_name)
directory_client = share_client.get_directory_client(dir_path)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchAdvanceStats' in item.name:
            # If the item is a JSON file with 'MatchAdvanceStats' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
df = pd.json_normalize(json_files)
df = pd.DataFrame(df)
df.columns = df.columns.str.replace('30685','Horsens U17')
df.columns = df.columns.str.replace('27148','Esbjerg U17')
df.columns = df.columns.str.replace('27144','København U17')
df.columns = df.columns.str.replace('27147','Silkeborg U17')
df.columns = df.columns.str.replace('62977','SønderjyskE U17')
df.columns = df.columns.str.replace('27142','AAB U17')
df.columns = df.columns.str.replace('27143','OB U17')
df.columns = df.columns.str.replace('27141','Vejle U17')
df.columns = df.columns.str.replace('27140','Randers U17')
df.columns = df.columns.str.replace('27149','FC Nordsjælland U17')
df.columns = df.columns.str.replace('27139','Midtjylland U17')
df.columns = df.columns.str.replace('27145','AGF U17')
df.columns = df.columns.str.replace('27152','Lyngby U17')
df.columns = df.columns.str.replace('27146','Brøndby IF U17')
#df.columns = df.columns.str.replace('general.','')
#possession_cols = [col for col in df.columns if col.startswith('possession')]
#df.columns = df.columns.where(~df.columns.str.startswith('possession.'), df.columns.str.replace('possession.', ''))
#df.columns = df.columns.str.replace('openplay.','')
#df.columns = df.columns.str.replace('attacks.','')
#df.columns = df.columns.str.replace('transitions.','')
#df.columns = df.columns.str.replace('passes.','')
#df.columns = df.columns.str.replace('defence.','')
#df.columns = df.columns.str.replace('duels.','')
#df.columns = df.columns.str.replace('flanks.','')


json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})

dfegnekampe = kampdetaljer.merge(df)
dfegnekampe['label'] = dfegnekampe['label'].astype(str)
dfegnekampe = dfegnekampe[dfegnekampe['label'].str.contains('Horsens')]
dfegnekampe.to_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Teamsheet egne kampe U17.csv',index=False)


#Start på U19
connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 21-22/U19 Ligaen/'


service_client = ShareServiceClient.from_connection_string(connection_string)
share_client = service_client.get_share_client(share_name)
directory_client = share_client.get_directory_client(dir_path)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchAdvanceStats' in item.name:
            # If the item is a JSON file with 'MatchAdvanceStats' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
df = pd.json_normalize(json_files)
df = pd.DataFrame(df)
df.columns = df.columns.str.replace('38324','Horsens U19 sidste sæson')
df.columns = df.columns.str.replace('23735','Esbjerg U19')
df.columns = df.columns.str.replace('23732','København U19')
df.columns = df.columns.str.replace('23736','Silkeborg U19')
df.columns = df.columns.str.replace('23738','SønderjyskE U19')
df.columns = df.columns.str.replace('23730','AAB U19')
df.columns = df.columns.str.replace('23726','OB U19')
df.columns = df.columns.str.replace('23733','Vejle U19')
df.columns = df.columns.str.replace('23737','Randers U19')
df.columns = df.columns.str.replace('23727','FC Nordsjælland U19')
df.columns = df.columns.str.replace('23729','Midtjylland U19')
df.columns = df.columns.str.replace('25612','AGF U19')
df.columns = df.columns.str.replace('23731','Lyngby U19')
df.columns = df.columns.str.replace('23734','Brøndby IF U19')
#df.columns = df.columns.str.replace('general.','')
#possession_cols = [col for col in df.columns if col.startswith('possession')]
#df.columns = df.columns.where(~df.columns.str.startswith('possession.'), df.columns.str.replace('possession.', ''))
#df.columns = df.columns.str.replace('openplay.','')
#df.columns = df.columns.str.replace('attacks.','')
#df.columns = df.columns.str.replace('transitions.','')
#df.columns = df.columns.str.replace('passes.','')
#df.columns = df.columns.str.replace('defence.','')
#df.columns = df.columns.str.replace('duels.','')
#df.columns = df.columns.str.replace('flanks.','')


json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})

dfegnekampe = kampdetaljer.merge(df)
dfegnekampe['label'] = dfegnekampe['label'].astype(str)
dfegnekampe = dfegnekampe[dfegnekampe['label'].str.contains('Horsens')]
dfegnekampe.to_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Teamsheet alle kampe U19 sidste sæson.csv',index=False)

from azure.storage.fileshare import ShareServiceClient
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
import os
import streamlit as st
connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 22-23/U19 Ligaen/'


service_client = ShareServiceClient.from_connection_string(connection_string)
share_client = service_client.get_share_client(share_name)
directory_client = share_client.get_directory_client(dir_path)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchAdvanceStats' in item.name:
            # If the item is a JSON file with 'MatchAdvanceStats' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
df = pd.json_normalize(json_files)
df = pd.DataFrame(df)
df.columns = df.columns.str.replace('38324','Horsens U19')
df.columns = df.columns.str.replace('23735','Esbjerg U19')
df.columns = df.columns.str.replace('23732','København U19')
df.columns = df.columns.str.replace('23736','Silkeborg U19')
df.columns = df.columns.str.replace('23738','SønderjyskE U19')
df.columns = df.columns.str.replace('23730','AAB U19')
df.columns = df.columns.str.replace('23726','OB U19')
df.columns = df.columns.str.replace('23733','Vejle U19')
df.columns = df.columns.str.replace('23737','Randers U19')
df.columns = df.columns.str.replace('23727','FC Nordsjælland U19')
df.columns = df.columns.str.replace('23729','Midtjylland U19')
df.columns = df.columns.str.replace('25612','AGF U19')
df.columns = df.columns.str.replace('23731','Lyngby U19')
df.columns = df.columns.str.replace('23734','Brøndby IF U19')
#df.columns = df.columns.str.replace('general.','')
#possession_cols = [col for col in df.columns if col.startswith('possession')]
#df.columns = df.columns.where(~df.columns.str.startswith('possession.'), df.columns.str.replace('possession.', ''))
#df.columns = df.columns.str.replace('openplay.','')
#df.columns = df.columns.str.replace('attacks.','')
#df.columns = df.columns.str.replace('transitions.','')
#df.columns = df.columns.str.replace('passes.','')
#df.columns = df.columns.str.replace('defence.','')
#df.columns = df.columns.str.replace('duels.','')
#df.columns = df.columns.str.replace('flanks.','')


json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})

dfegnekampe = kampdetaljer.merge(df)
dfegnekampe['label'] = dfegnekampe['label'].astype(str)
#dfegnekampe = dfegnekampe[dfegnekampe['label'].str.contains('Horsens')]
dfegnekampe.to_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Teamsheet alle kampe U19.csv',index=False)

from azure.storage.fileshare import ShareServiceClient
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
import os
import streamlit as st
connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 22-23/U19 Ligaen/'

print('U19 holddata hentet')
service_client = ShareServiceClient.from_connection_string(connection_string)
share_client = service_client.get_share_client(share_name)
directory_client = share_client.get_directory_client(dir_path)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchAdvanceStats' in item.name:
            # If the item is a JSON file with 'MatchAdvanceStats' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
df = pd.json_normalize(json_files)
df = pd.DataFrame(df)
df.columns = df.columns.str.replace('38324','Horsens U19')
df.columns = df.columns.str.replace('23735','Esbjerg U19')
df.columns = df.columns.str.replace('23732','København U19')
df.columns = df.columns.str.replace('23736','Silkeborg U19')
df.columns = df.columns.str.replace('23738','SønderjyskE U19')
df.columns = df.columns.str.replace('23730','AAB U19')
df.columns = df.columns.str.replace('23726','OB U19')
df.columns = df.columns.str.replace('23733','Vejle U19')
df.columns = df.columns.str.replace('23737','Randers U19')
df.columns = df.columns.str.replace('23727','FC Nordsjælland U19')
df.columns = df.columns.str.replace('23729','Midtjylland U19')
df.columns = df.columns.str.replace('25612','AGF U19')
df.columns = df.columns.str.replace('23731','Lyngby U19')
df.columns = df.columns.str.replace('23734','Brøndby IF U19')
#df.columns = df.columns.str.replace('general.','')
#possession_cols = [col for col in df.columns if col.startswith('possession')]
#df.columns = df.columns.where(~df.columns.str.startswith('possession.'), df.columns.str.replace('possession.', ''))
#df.columns = df.columns.str.replace('openplay.','')
#df.columns = df.columns.str.replace('attacks.','')
#df.columns = df.columns.str.replace('transitions.','')
#df.columns = df.columns.str.replace('passes.','')
#df.columns = df.columns.str.replace('defence.','')
#df.columns = df.columns.str.replace('duels.','')
#df.columns = df.columns.str.replace('flanks.','')


json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})

dfegnekampe = kampdetaljer.merge(df)
dfegnekampe['label'] = dfegnekampe['label'].astype(str)
dfegnekampe = dfegnekampe[dfegnekampe['label'].str.contains('Horsens')]
dfegnekampe.to_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Teamsheet egne kampe U19.csv',index=False)

from azure.storage.fileshare import ShareServiceClient
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
import ast

connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 22-23/U15 Ligaen/'


service_client = ShareServiceClient.from_connection_string(connection_string)
share_client = service_client.get_share_client(share_name)
directory_client = share_client.get_directory_client(dir_path)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchAdvancePlayerStats' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))

find_json_files(directory_client)

# Create an empty list to store the events data
players_list = []
# Iterate over each item in the json_files list and append its 'events' data to the events_list
for item in json_files:
    players_list.extend(item['players'])


# Convert the events_list to a DataFrame
df = pd.DataFrame(players_list)
df.to_csv('Individuelt dashboard U15.csv',index=False)
print('Matchstats hentet')
json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchEvents' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))

find_json_files(directory_client)

# Create an empty list to store the events data
events_list = []

# Iterate over each item in the json_files list and append its 'events' data to the events_list
for item in json_files:
    events_list.extend(item['events'])

# Convert the events_list to a DataFrame
df = pd.DataFrame(events_list)
df = df[['matchId','team','opponentTeam','player']]
print('eventdata hentet')
json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
            
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})
df1 = kampdetaljer.merge(df)

df1.to_csv('U15 eventdata alle.csv',index=False)

df = pd.read_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\U15 eventdata alle.csv')
df['team'] = df['team'].apply(lambda x: ast.literal_eval(x))

# Create a new dataframe with the columns as the dictionary keys and the values as a list
new_df = pd.DataFrame(df['team'].to_list(), index=df.index).add_prefix('team_')

# Concatenate the new dataframe with the original dataframe
df = pd.concat([df, new_df], axis=1)

# Drop the original 'percent' column
df = df.drop('team', axis=1)

df['opponentTeam'] = df['opponentTeam'].apply(lambda x: ast.literal_eval(x))

# Create a new dataframe with the columns as the dictionary keys and the values as a list
new_df = pd.DataFrame(df['opponentTeam'].to_list(), index=df.index).add_prefix('opponentTeam_')

# Concatenate the new dataframe with the original dataframe
df = pd.concat([df, new_df], axis=1)

# Drop the original 'percent' column
df = df.drop('opponentTeam', axis=1)

df['player'] = df['player'].apply(lambda x: ast.literal_eval(x))

# Create a new dataframe with the columns as the dictionary keys and the values as a list
new_df = pd.DataFrame(df['player'].to_list(), index=df.index).add_prefix('Player ')

# Concatenate the new dataframe with the original dataframe
df = pd.concat([df, new_df], axis=1)

# Drop the original 'percent' column
df = df.drop('player', axis=1)
df['matchId'] = df['matchId'].astype(str)
df['Player id'] = df['Player id'].astype(str)
df.to_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\U15 eventdata alle.csv')

print('Matchdetails hentet')

print('Alt data hentet')