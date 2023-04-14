#hent GPS data
import pandas as pd
import streamlit as st
import seaborn as sns
import os
import glob
import matplotlib.pyplot as plt
import openpyxl as xlsxwriter
from pandas import DataFrame
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
df1.to_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\U19 eventdata.csv')
print('U19 Data hentet')

    
import gspread
import pandas as pd
import streamlit as st


gc = gspread.service_account()
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1aKhqUERGEZ9et5hBFFxHrlANsXrLSWWDkriMgBBJjAA/edit?resourcekey#gid=575235197')
ws = sh.worksheet('Samlet')
df0 = pd.DataFrame(ws.get_all_records())
df0['Tidsstempel'] = df0['Tidsstempel'].str[:-9]
df0['Tidsstempel'] = pd.to_datetime(df0['Tidsstempel'], dayfirst=True)
df0['Tidsstempel'] = df0['Tidsstempel'].dt.isocalendar().week
df0.columns = df0.columns.str.replace('Tidsstempel', 'Ugenummer')


df0['Hvor udmattet er du?'] = df0['Hvor udmattet er du?'].replace('Ingen udmattelse',1)
df0['Hvor udmattet er du?'] = df0['Hvor udmattet er du?'].replace('Minimal udmattelse',2)
df0['Hvor udmattet er du?'] = df0['Hvor udmattet er du?'].replace('Bedre end normalt',3)
df0['Hvor udmattet er du?'] = df0['Hvor udmattet er du?'].replace('Normalt',4)
df0['Hvor udmattet er du?'] = df0['Hvor udmattet er du?'].replace('Værre end normalt',5)
df0['Hvor udmattet er du?'] = df0['Hvor udmattet er du?'].replace('Meget udmattet',6)
df0['Hvor udmattet er du?'] = df0['Hvor udmattet er du?'].replace('Udmattet - stor træthed',7)

df0['Hvordan var din søvn i den seneste uge?'] = df0['Hvordan var din søvn i den seneste uge?'].replace('Fremragende',1)
df0['Hvordan var din søvn i den seneste uge?'] = df0['Hvordan var din søvn i den seneste uge?'].replace('Meget god',2)
df0['Hvordan var din søvn i den seneste uge?'] = df0['Hvordan var din søvn i den seneste uge?'].replace('Bedre end normalt',3)
df0['Hvordan var din søvn i den seneste uge?'] = df0['Hvordan var din søvn i den seneste uge?'].replace('Normalt',4)
df0['Hvordan var din søvn i den seneste uge?'] = df0['Hvordan var din søvn i den seneste uge?'].replace('Værre end normalt',5)
df0['Hvordan var din søvn i den seneste uge?'] = df0['Hvordan var din søvn i den seneste uge?'].replace('Afbrudt',6)
df0['Hvordan var din søvn i den seneste uge?'] = df0['Hvordan var din søvn i den seneste uge?'].replace('Forfærdelig - ingen søvn',7)

df0['Hvor mange timer sov du i gennemsnit pr. nat i den seneste uge?'] = df0['Hvor mange timer sov du i gennemsnit pr. nat i den seneste uge?'].replace('10+',1)
df0['Hvor mange timer sov du i gennemsnit pr. nat i den seneste uge?'] = df0['Hvor mange timer sov du i gennemsnit pr. nat i den seneste uge?'].replace('9-10',2)
df0['Hvor mange timer sov du i gennemsnit pr. nat i den seneste uge?'] = df0['Hvor mange timer sov du i gennemsnit pr. nat i den seneste uge?'].replace('8-9',3)
df0['Hvor mange timer sov du i gennemsnit pr. nat i den seneste uge?'] = df0['Hvor mange timer sov du i gennemsnit pr. nat i den seneste uge?'].replace(8,4)
df0['Hvor mange timer sov du i gennemsnit pr. nat i den seneste uge?'] = df0['Hvor mange timer sov du i gennemsnit pr. nat i den seneste uge?'].replace('7-8',5)
df0['Hvor mange timer sov du i gennemsnit pr. nat i den seneste uge?'] = df0['Hvor mange timer sov du i gennemsnit pr. nat i den seneste uge?'].replace('5-7',6)
df0['Hvor mange timer sov du i gennemsnit pr. nat i den seneste uge?'] = df0['Hvor mange timer sov du i gennemsnit pr. nat i den seneste uge?'].replace('5 eller mindre',7)

df0['Bedøm din muskeltræthed'] = df0['Bedøm din muskeltræthed'].replace('Ingen ømhed',1)
df0['Bedøm din muskeltræthed'] = df0['Bedøm din muskeltræthed'].replace('Meget lidt ømhed',2)
df0['Bedøm din muskeltræthed'] = df0['Bedøm din muskeltræthed'].replace('Bedre end normalt',3)
df0['Bedøm din muskeltræthed'] = df0['Bedøm din muskeltræthed'].replace('Normalt',4)
df0['Bedøm din muskeltræthed'] = df0['Bedøm din muskeltræthed'].replace('Værre end normalt',5)
df0['Bedøm din muskeltræthed'] = df0['Bedøm din muskeltræthed'].replace('Meget øm/stram',6)
df0['Bedøm din muskeltræthed'] = df0['Bedøm din muskeltræthed'].replace('Ekstremt øm/stram',7)

df0['Hvordan har du det psykologisk (mentalt)?'] = df0['Hvordan har du det psykologisk (mentalt)?'].replace('Har det storartet - meget afslappet',1)
df0['Hvordan har du det psykologisk (mentalt)?'] = df0['Hvordan har du det psykologisk (mentalt)?'].replace('Har det godt - afslappet',2)
df0['Hvordan har du det psykologisk (mentalt)?'] = df0['Hvordan har du det psykologisk (mentalt)?'].replace('Bedre end normalt',3)
df0['Hvordan har du det psykologisk (mentalt)?'] = df0['Hvordan har du det psykologisk (mentalt)?'].replace('Normalt',4)
df0['Hvordan har du det psykologisk (mentalt)?'] = df0['Hvordan har du det psykologisk (mentalt)?'].replace('Værre end normalt',5)
df0['Hvordan har du det psykologisk (mentalt)?'] = df0['Hvordan har du det psykologisk (mentalt)?'].replace('Stresset',6)
df0['Hvordan har du det psykologisk (mentalt)?'] = df0['Hvordan har du det psykologisk (mentalt)?'].replace('Meget stresset',7)

df0['Hvordan har din kost(mad) set ud den seneste uge?'] = df0['Hvordan har din kost(mad) set ud den seneste uge?'].replace('Meget sund - meget varieret',1)
df0['Hvordan har din kost(mad) set ud den seneste uge?'] = df0['Hvordan har din kost(mad) set ud den seneste uge?'].replace('Sund - varieret',2)
df0['Hvordan har din kost(mad) set ud den seneste uge?'] = df0['Hvordan har din kost(mad) set ud den seneste uge?'].replace('Mest sund - nogenlunde varieret',3)
df0['Hvordan har din kost(mad) set ud den seneste uge?'] = df0['Hvordan har din kost(mad) set ud den seneste uge?'].replace('Varieret',4)
df0['Hvordan har din kost(mad) set ud den seneste uge?'] = df0['Hvordan har din kost(mad) set ud den seneste uge?'].replace('Varieret, men lidt usund',5)
df0['Hvordan har din kost(mad) set ud den seneste uge?'] = df0['Hvordan har din kost(mad) set ud den seneste uge?'].replace('Usund - ikke varieret',6)
df0['Hvordan har din kost(mad) set ud den seneste uge?'] = df0['Hvordan har din kost(mad) set ud den seneste uge?'].replace('Meget usund - slet ikke varieret',7)

df0['Hvordan har dit humør været efter fodboldtræning den seneste uge?'] = df0['Hvordan har dit humør været efter fodboldtræning den seneste uge?'].replace('Fremragende',1)
df0['Hvordan har dit humør været efter fodboldtræning den seneste uge?'] = df0['Hvordan har dit humør været efter fodboldtræning den seneste uge?'].replace('Meget godt',2)
df0['Hvordan har dit humør været efter fodboldtræning den seneste uge?'] = df0['Hvordan har dit humør været efter fodboldtræning den seneste uge?'].replace('Bedre end normalt',3)
df0['Hvordan har dit humør været efter fodboldtræning den seneste uge?'] = df0['Hvordan har dit humør været efter fodboldtræning den seneste uge?'].replace('Normalt',4)
df0['Hvordan har dit humør været efter fodboldtræning den seneste uge?'] = df0['Hvordan har dit humør været efter fodboldtræning den seneste uge?'].replace('Værre end normalt',5)
df0['Hvordan har dit humør været efter fodboldtræning den seneste uge?'] = df0['Hvordan har dit humør været efter fodboldtræning den seneste uge?'].replace('Meget dårligt',6)
df0['Hvordan har dit humør været efter fodboldtræning den seneste uge?'] = df0['Hvordan har dit humør været efter fodboldtræning den seneste uge?'].replace('Ekstremt dårligt',7)

df0['Ugenummer'] = pd.to_numeric(df0['Ugenummer'], errors="coerce").fillna(0).astype('int64')
df0.to_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\samlet wellness.csv')