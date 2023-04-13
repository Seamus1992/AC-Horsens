import pandas as pd
import csv
import streamlit as st
import numpy as np
from datetime import datetime

df = pd.read_csv('Teamsheet egne kampe.csv')
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
dfsorteredekampe['gennemsnit'] = dfsorteredekampe.mean(axis=1)
dfsorteredekampe = pd.concat([dfoverskrifter,dfsorteredekampe])
dfsorteredekampe = dfsorteredekampe.dropna(how='all')
dfsorteredekampe = dfsorteredekampe.rename_axis('Parameter')
dfsorteredekampe = dfsorteredekampe[~dfsorteredekampe.index.str.contains('Horsens', case=False)]

st.dataframe(dfsorteredekampe)
