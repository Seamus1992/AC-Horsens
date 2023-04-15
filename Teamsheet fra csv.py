import pandas as pd
import csv
import streamlit as st
import numpy as np
from datetime import datetime

df = pd.read_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Teamsheet egne kampe.csv')
kampe = df['label']
option = st.multiselect('Vælg kamp (Hvis ingen kamp er valgt, vises gennemsnit for alle)',kampe)
if len(option) > 0:
    temp_select = option
else:
    temp_select = kampe

dfsorteredekampe = df.loc[df.loc[df.label.isin(temp_select),'label'].index.values]
dfsorteredekampe = dfsorteredekampe.iloc[: , 1:]
dfsorteredekampe['date'] = dfsorteredekampe['date'].astype(str)
dfsorteredekampe['date'] = dfsorteredekampe['date'].str.replace(r'\sGMT.*$', '', regex=True)
dfsorteredekampe['date'] = pd.to_datetime(dfsorteredekampe['date'], format="%B %d, %Y at %I:%M:%S %p")
dfsorteredekampe['date'] = dfsorteredekampe['date'].dt.strftime('%d-%m-%Y')
dfsorteredekampe = dfsorteredekampe.transpose()
dfoverskrifter = dfsorteredekampe[:2]
dfsorteredekampe = dfsorteredekampe[2:].apply(pd.to_numeric, errors='coerce')
dfsorteredekampe = pd.concat([dfoverskrifter,dfsorteredekampe])
dfsorteredekampe = dfsorteredekampe.dropna(how='all')
dfsorteredekampe = dfsorteredekampe.rename_axis('Parameter').astype(str)
dfsorteredekampe = dfsorteredekampe.transpose()
# select the columns that end with "shots", "xg", or "dribbles" and group by "AC Horsens"
# Extract columns that end with 'shots', 'xg', or 'dribbles'
goals_cols = [col for col in dfsorteredekampe.columns if col.endswith('.goals')]
shots_cols = [col for col in dfsorteredekampe.columns if col.endswith('.shots')]
xg_cols = [col for col in dfsorteredekampe.columns if col.endswith('.xg')]
duels_cols = [col for col in dfsorteredekampe.columns if col.endswith('.duels')]
duelswon_cols = [col for col in dfsorteredekampe.columns if col.endswith('.duelsSuccessful')]
possession_cols = [col for col in dfsorteredekampe.columns if col.endswith('.possessionPercent')]
ppda_cols = [col for col in dfsorteredekampe.columns if col.endswith('.ppda')]

# Create a new dataframe with the average values for each team
team_data = {}
for team in set([col.split('.')[1] for col in shots_cols]):
    team_goals = dfsorteredekampe[[col for col in goals_cols if(team) in col]].mean(axis=1)    
    team_shots = dfsorteredekampe[[col for col in shots_cols if(team) in col]].mean(axis=1)
    team_xg = dfsorteredekampe[[col for col in xg_cols if (team) in col]].mean(axis=1)
    team_duels = dfsorteredekampe[[col for col in duels_cols if (team) in col]].mean(axis=1)
    team_duelswon = dfsorteredekampe[[col for col in duelswon_cols if (team) in col]].mean(axis=1)
    team_possession = dfsorteredekampe[[col for col in possession_cols if (team) in col]].mean(axis=1)
    team_ppda = dfsorteredekampe[[col for col in ppda_cols if (team) in col]].mean(axis=1)

    team_data[team] = pd.concat([team_goals,team_shots, team_xg, team_duels,team_duelswon,team_possession,team_ppda], axis=1)
    
team_df = pd.concat(team_data, axis=0, keys=team_data.keys())
team_df.columns = ['Goals','Shots', 'Xg', 'Duels','Duels won','Possession %','PPDA']
team_df = team_df.groupby(level=0).mean()
st.write('Generelle stats')
st.dataframe(team_df)
st.dataframe(dfsorteredekampe)