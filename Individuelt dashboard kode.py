import pandas as pd
import streamlit as st
import json
from pandas import json_normalize
import ast
df = pd.read_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Individuelt dashboard U15.csv')
df.rename(columns={'playerId': 'Player id'}, inplace=True)
df = df.astype(str)
dfevents = pd.read_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\U15 eventdata alle.csv',low_memory=False)
dfevents = dfevents[['Player id','Player name','team_name','label','date','matchId']]
dfspillernavn = df[['Player id','matchId','positions','average','percent']]
dfspillernavn = dfspillernavn.astype(str)
dfevents['Player id'] = dfevents['Player id'].astype(str)
dfevents['matchId'] = dfevents['matchId'].astype(str)
df = dfspillernavn.merge(dfevents)
df['Player&matchId'] = df['Player id'] + df['matchId']
df['Player&matchId'] = df['Player&matchId'].drop_duplicates(keep='first')
df = df.dropna()
df = df[['Player id','Player name','team_name','matchId','label','date','positions','average','percent']]
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
df = df[['Player name','team_name','matchId','label','date','position_names','position_codes','average','percent']]
df = df.rename(columns={'team_name':'Team name'})
df['percent'] = df['percent'].apply(lambda x: ast.literal_eval(x))

# Create a new dataframe with the columns as the dictionary keys and the values as a list
new_df = pd.DataFrame(df['percent'].to_list(), index=df.index).add_prefix('percent_')

# Concatenate the new dataframe with the original dataframe
df = pd.concat([df, new_df], axis=1)

# Drop the original 'percent' column
df = df.drop('percent', axis=1)

df['average'] = df['average'].apply(lambda x: ast.literal_eval(x))

# Create a new dataframe with the columns as the dictionary keys and the values as a list
new_df = pd.DataFrame(df['average'].to_list(), index=df.index).add_prefix('average_')

# Concatenate the new dataframe with the original dataframe
df = pd.concat([df, new_df], axis=1)

# Drop the original 'percent' column
df = df.drop('average', axis=1)
df['position_codes'] = df['position_codes'].astype(str)
st.dataframe(df)