import pandas as pd
import streamlit as st
df = pd.read_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Individuelt dashboard test.csv')
df.rename(columns={'playerId': 'Player id'}, inplace=True)
dfevents = pd.read_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\U15 eventdata.csv')
dfevents = dfevents[['Player id','Player name']]
df = df.astype(str)
df = pd.concat([df,dfevents])
df = df[['Player id','Player name','matchId','positions','total','average','percent']]
st.dataframe(df)
print(df)