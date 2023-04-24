import pandas as pd
import streamlit as st
df = pd.read_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Individuelt dashboard test.csv')
df.rename(columns={'playerId': 'Player id'}, inplace=True)
df = df.astype(str)
dfevents = pd.read_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\U15 eventdata.csv')
dfevents = dfevents[['Player id','Player name','label','date','matchId']]
dfspillernavn = df[['Player id','matchId','positions','total','average','percent']]
dfspillernavn = dfspillernavn.astype(str)
dfevents['Player id'] = dfevents['Player id'].astype(str)
dfevents['matchId'] = dfevents['matchId'].astype(str)
df = dfspillernavn.merge(dfevents)
df['Player&matchId'] = df['Player id'] + df['matchId']
df['Player&matchId'] = df['Player&matchId'].drop_duplicates(keep='first')
df = df.dropna()
df = df[['Player id','Player name','matchId','label','date','positions','total','average','percent']]
df = df.set_index('Player id')
st.dataframe(df)
print(df)