import gspread
import pandas as pd
import streamlit as st
import numpy as np

gc = gspread.service_account()
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1haWEtNQdhthKaSQjb2BRHlq2FLexicUOAHbjNFRAUAk/edit#gid=1984878556')
ws = sh.worksheet('Samlet')
df = pd.DataFrame(ws.get_all_records())
df.to_csv('ny wellness.csv',index=False)
df = pd.read_csv('ny wellness.csv')
df['Tidsstempel'] = pd.to_datetime(df['Tidsstempel'], format='%d/%m/%Y %H.%M.%S')
df['Hvilken årgang er du?'] = df['Hvilken årgang er du?'].astype(str)
df['Hvor frisk er du?'] = df['Hvor frisk er du?'].astype(str)
df['Hvor frisk er du?'] = df['Hvor frisk er du?'].str.extract(r'(\d+)').astype(float)
df['Hvordan har du det mentalt'] = df['Hvordan har du det mentalt'].astype(str)
df['Hvordan har du det mentalt'] = df['Hvordan har du det mentalt'].str.extract(r'(\d+)').astype(float)
df['Hvordan har din søvn været?'] = df['Hvordan har din søvn været?'].astype(str)
df['Hvordan har din søvn været?'] = df['Hvordan har din søvn været?'].str.extract(r'(\d+)').astype(float)
df['Hvor hård var træning/kamp? (10 er hårdest)'] = df['Hvor hård var træning/kamp? (10 er hårdest)'].astype(str)
df['Hvor hård var træning/kamp? (10 er hårdest)'] = df['Hvor hård var træning/kamp? (10 er hårdest)'].str.extract(r'(\d+)').astype(float)
df['Hvor udmattet er du?'] = df['Hvor udmattet er du?'].astype(str)
df['Hvor udmattet er du?'] = df['Hvor udmattet er du?'].str.extract(r'(\d+)').astype(float)
df['Bedøm din muskelømhed'] = df['Bedøm din muskelømhed'].astype(str)
df['Bedøm din muskelømhed'] = df['Bedøm din muskelømhed'].str.extract(r'(\d+)').astype(float)
df['Jeg følte mig tilpas udfordret under træning/kamp'] = df['Jeg følte mig tilpas udfordret under træning/kamp'].astype(str)
df['Jeg følte mig tilpas udfordret under træning/kamp'] = df['Jeg følte mig tilpas udfordret under træning/kamp'].str.extract(r'(\d+)').astype(float)
df['Min tidsfornemmelse forsvandt under træning/kamp'] = df['Min tidsfornemmelse forsvandt under træning/kamp'].astype(str)
df['Min tidsfornemmelse forsvandt under træning/kamp'] = df['Min tidsfornemmelse forsvandt under træning/kamp'].str.extract(r'(\d+)').astype(float)
df['Jeg oplevede at tanker og handlinger var rettet mod træning/kamp'] = df['Jeg oplevede at tanker og handlinger var rettet mod træning/kamp'].astype(str)
df['Jeg oplevede at tanker og handlinger var rettet mod træning/kamp'] = df['Jeg oplevede at tanker og handlinger var rettet mod træning/kamp'].str.extract(r'(\d+)').astype(float)
df['Hvordan har du det mentalt?'] = df['Hvordan har du det mentalt?'].astype(str)
df['Hvordan har du det mentalt?'] = df['Hvordan har du det mentalt?'].str.extract(r'(\d+)').astype(float)

df.rename(columns={'Hvor mange timer sov i du i nat?':'Hvor mange timer sov du i nat?'},inplace=True)
df = pd.melt(df,id_vars=['Tidsstempel','Spørgsmål før eller efter træning','Hvor frisk er du?','Hvordan har du det mentalt','Har du fået nok at spise inden træning/kamp?','Hvordan har din søvn været?','Hvor mange timer sov du i nat?','Træning/kamp - tid i minutter?','Hvor hård var træning/kamp? (10 er hårdest)','Hvor udmattet er du?','Bedøm din muskelømhed','Hvordan har du det mentalt?','Jeg følte mig tilpas udfordret under træning/kamp','Min tidsfornemmelse forsvandt under træning/kamp','Jeg oplevede at tanker og handlinger var rettet mod træning/kamp','Hvilken årgang er du?'],value_vars=['Spillere U13','Spillere U14','Spillere U15','Spillere U16','Spillere U17','Spillere U18','Spillere U19','Spillere U20','Spillere U21'],value_name='Spiller')
df = df[df['Spiller'] != '']
kampe = df['Hvilken årgang er du?'].drop_duplicates(keep='first')
kampe = sorted(kampe)
option4 = st.multiselect('Vælg årgang (Hvis ingen årgang er valgt, vises alle)',kampe)
if len(option4) > 0:
    filtreretdfkamp = option4
else:
    filtreretdfkamp = kampe

filtreretdfkamp = df.loc[df.loc[df['Hvilken årgang er du?'].isin(filtreretdfkamp),'Hvilken årgang er du?'].index.values]
førtræning = filtreretdfkamp[['Tidsstempel','Spiller','Hvilken årgang er du?','Hvor frisk er du?','Hvordan har du det mentalt','Har du fået nok at spise inden træning/kamp?','Hvordan har din søvn været?','Hvor mange timer sov du i nat?']]
eftertræning = filtreretdfkamp[['Tidsstempel','Spiller','Hvilken årgang er du?','Træning/kamp - tid i minutter?','Hvor hård var træning/kamp? (10 er hårdest)','Hvor udmattet er du?','Bedøm din muskelømhed','Hvordan har du det mentalt?','Jeg følte mig tilpas udfordret under træning/kamp','Min tidsfornemmelse forsvandt under træning/kamp','Jeg oplevede at tanker og handlinger var rettet mod træning/kamp']]
førtræning.dropna(inplace=True)
eftertræning.dropna(inplace=True)


def color_row(row):
    color = ''
    if 'Hvor frisk er du?' in row and row['Hvor frisk er du?'] >= 6 or 'Hvordan har du det mentalt' in row and row['Hvordan har du det mentalt'] >= 6 or 'Hvordan har din søvn været?' in row and row['Hvordan har din søvn været?'] >= 6 or ('Har du fået nok at spise inden træning/kamp?' in row and row['Har du fået nok at spise inden træning/kamp?'] =='Nej') or ('Hvor mange timer sov du i nat?' in row and row['Hvor mange timer sov du i nat?'] == 'Under 7 timer'):
        color = 'red'
    elif 'Hvor frisk er du?' in row and row['Hvor frisk er du?'] == 5 or 'Hvordan har du det mentalt' in row and row['Hvordan har du det mentalt'] == 5 or 'Hvordan har din søvn været?' in row and row['Hvordan har din søvn været?'] == 5 or ('Har du fået nok at spise inden træning/kamp?' in row and row['Har du fået nok at spise inden træning/kamp?'] =='Ved ikke') or ('Hvor mange timer sov du i nat?' in row and row['Hvor mange timer sov du i nat?'] == '7-8 timer'):
        color = 'yellow'
    return ['background-color: %s' % color] * row.size
førtræning.set_index('Tidsstempel', inplace=True)
førtræning.sort_index(ascending=False, inplace=True)

førtræning = førtræning.style.apply(color_row, axis=1, subset=pd.IndexSlice[:])

def color_row(row):
    color = ''
    if 'Hvor udmattet er du?' in row and row['Hvor udmattet er du?'] >= 6 or 'Bedøm din muskelømhed' in row and row['Bedøm din muskelømhed'] >= 6 or 'Hvordan har du det mentalt?' in row and row['Hvordan har du det mentalt?'] >= 6 or ('Jeg følte mig tilpas udfordret under træning/kamp' in row and row['Jeg følte mig tilpas udfordret under træning/kamp'] >= 6) or ('Min tidsfornemmelse forsvandt under træning/kamp' in row and row['Min tidsfornemmelse forsvandt under træning/kamp'] >= 6 or 'Jeg oplevede at tanker og handlinger var rettet mod træning/kamp' in row and row['Jeg oplevede at tanker og handlinger var rettet mod træning/kamp'] >= 6):
        color = 'red'
    elif 'Hvor udmattet er du?' in row and row['Hvor udmattet er du?'] == 5 or 'Bedøm din muskelømhed' in row and row['Bedøm din muskelømhed'] == 5 or 'Hvordan har du det mentalt?' in row and row['Hvordan har du det mentalt?'] == 5 or ('Jeg følte mig tilpas udfordret under træning/kamp' in row and row['Jeg følte mig tilpas udfordret under træning/kamp'] == 5) or ('Min tidsfornemmelse forsvandt under træning/kamp' in row and row['Min tidsfornemmelse forsvandt under træning/kamp'] == 5 or 'Jeg oplevede at tanker og handlinger var rettet mod træning/kamp' in row and row['Jeg oplevede at tanker og handlinger var rettet mod træning/kamp'] == 5):
        color = 'yellow'
    return ['background-color: %s' % color] * row.size
eftertræning.set_index('Tidsstempel', inplace=True)
eftertræning.sort_index(ascending=False, inplace=True)

eftertræning = eftertræning.style.apply(color_row, axis=1, subset=pd.IndexSlice[:])

# Display the styled dataframe

st.write('Før træning')
st.dataframe(førtræning)
st.write('Efter træning')
st.dataframe(eftertræning)