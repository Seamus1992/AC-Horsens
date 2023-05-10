import pandas as pd
import streamlit as st
import json
from pandas import json_normalize
import ast
from dateutil import parser
df = pd.read_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Individuelt dashboard U15.csv')
df.rename(columns={'playerId': 'Player id'}, inplace=True)
df = df.astype(str)
dfevents = pd.read_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\U15 eventdata alle.csv',low_memory=False)
dfevents = dfevents[['Player id','Player name','team_name','label','date','matchId']]
dfspillernavn = df[['Player id','matchId','positions','average','percent','total']]
dfspillernavn = dfspillernavn.astype(str)
dfevents['Player id'] = dfevents['Player id'].astype(str)
dfevents['matchId'] = dfevents['matchId'].astype(str)
df = dfspillernavn.merge(dfevents)

df['Player&matchId'] = df['Player id'] + df['matchId']
df['Player&matchId'] = df['Player&matchId'].drop_duplicates(keep='first')
df = df.dropna()
df = df[['Player id','Player name','team_name','matchId','label','date','positions','average','percent','total']]

#df = df.set_index('Player id')

data = df['positions']
df1 = pd.DataFrame(data)
# Funktion, der ekstraherer navne og koder fra strengdata og opretter en ny kolonne med disse værdier
def extract_positions(data):
    positions_list = ast.literal_eval(data) # Konverterer strengen til en liste af ordbøger
    names = [pos['position']['name'] for pos in positions_list]
    codes = [pos['position']['code'] for pos in positions_list]
    return pd.Series({'position_names': names, 'position_codes': codes})

# Anvender funktionen på kolonnen og tilføjer resultaterne som nye kolonner til dataframe
df1[['position_names', 'position_codes']] = df1['positions'].apply(extract_positions)

df = pd.merge(df,df1,left_index=True, right_index=True)
df = df.set_index('Player id')
df = df.drop(columns=['positions_x'])
df = df.drop(columns=['positions_y'])
df = df[['Player name','team_name','matchId','label','date','position_names','position_codes','average','percent','total']]
df = df.rename(columns={'team_name':'Team name'})
df['percent'] = df['percent'].apply(lambda x: ast.literal_eval(x))

# Create a new dataframe with the columns as the dictionary keys and the values as a list
new_df = pd.DataFrame(df['percent'].to_list(), index=df.index).add_prefix('percent_')

# Concatenate the new dataframe with the original dataframe
df = pd.concat([df, new_df], axis=1)

# Drop the original 'percent' column
df = df.drop('percent', axis=1)

df['total'] = df['total'].apply(lambda x: ast.literal_eval(x))

# Create a new dataframe with the columns as the dictionary keys and the values as a list
new_df = pd.DataFrame(df['total'].to_list(), index=df.index).add_prefix('total_')

# Concatenate the new dataframe with the original dataframe
df = pd.concat([df, new_df], axis=1)

# Drop the original 'percent' column
df = df.drop('total', axis=1)

df['average'] = df['average'].apply(lambda x: ast.literal_eval(x))

# Create a new dataframe with the columns as the dictionary keys and the values as a list
new_df = pd.DataFrame(df['average'].to_list(), index=df.index).add_prefix('average_')

# Concatenate the new dataframe with the original dataframe
df = pd.concat([df, new_df], axis=1)


# Drop the original 'percent' column
df = df.drop('average', axis=1)
df['position_codes'] = df['position_codes'].astype(str)
df['date'] = df['date'].astype(str)
df['date'] = df['date'].apply(lambda x: parser.parse(x))

# Sort the dataframe by the 'date' column
df = df.sort_values(by='date',ascending=False)

# Format the 'date' column to day-month-year format
df['date'] = df['date'].apply(lambda x: x.strftime('%d-%m-%Y'))

df_backs = df[df['position_codes'].str.contains('|'.join(['lb', 'rb']))]
df_Stoppere = df[df['position_codes'].str.contains('|'.join(['cb']))]
df_Centrale_midt = df[df['position_codes'].str.contains('|'.join(['cm','amf','dmf']))]
df_Kanter = df[df['position_codes'].str.contains('|'.join(['rw','lw','ramf','lamf']))]
df_Angribere = df[df['position_codes'].str.contains('|'.join(['cf']))]
st.dataframe(df)


df_Angribere['xG per 90 score'] = pd.qcut(df_Angribere['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
df_Angribere['Goals per 90 score'] = pd.qcut(df_Angribere['average_goals'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)  
df_Angribere['Shots on target, % score'] = pd.qcut(df_Angribere['percent_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)   
df_Angribere['Offensive duels won, % score'] = pd.qcut(df_Angribere['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
df_Angribere['Duels won, % score'] = pd.qcut(df_Angribere['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
df_Angribere['Accurate passes, % score'] = pd.qcut(df_Angribere['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
df_Angribere['Successful dribbles, % score'] = pd.qcut(df_Angribere['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
df_Angribere['xA per 90 score'] = pd.qcut(df_Angribere['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
df_Angribere['Touches in box per 90 score'] = pd.qcut(df_Angribere['average_touchInBox'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
df_Angribere['Progressive passes per 90 score'] = pd.qcut(df_Angribere['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
df_Angribere['Successful attacking actions per 90 score'] = pd.qcut(df_Angribere['average_successfulAttackingActions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
df_Angribere = df_Angribere[['Player name','Team name','label','date','position_names','total_minutesOnField','xG per 90 score','Goals per 90 score','Shots on target, % score','Offensive duels won, % score','Duels won, % score','Accurate passes, % score','Successful dribbles, % score','xA per 90 score','Touches in box per 90 score','Progressive passes per 90 score','Successful attacking actions per 90 score']]
st.dataframe(df_Angribere)