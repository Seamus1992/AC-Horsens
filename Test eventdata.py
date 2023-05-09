import streamlit as st
import pandas as pd
import ast
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

st.dataframe(df)