import streamlit as st

def Wellness_data():
    import pandas as pd
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
     
def GPS_Data():
    import pandas as pd
    import streamlit as st
    import seaborn as sns
    import matplotlib.pyplot as plt
    import openpyxl as xlsxwriter
    from pandas import DataFrame
    
    
    dforiginal = pd.read_csv('samlet gps data.csv')
    dforiginal = dforiginal.loc[dforiginal['Split Name'] =='all']
    
    Højintens_løb = dforiginal['Distance in Speed Zone 4  (km)']
    Sprint = dforiginal['Distance in Speed Zone 5  (km)']
    Hårde_accelerationer = dforiginal['Accelerations Zone Count: 3 - 4 m/s/s'] + dforiginal['Accelerations Zone Count: > 4 m/s/s']
    Hårde_deccelerationer = dforiginal['Deceleration Zone Count: 3 - 4 m/s/s'] + dforiginal['Deceleration Zone Count: > 4 m/s/s']
    Tid_med_høj_puls = (dforiginal['Time in HR Load Zone 85% - 96% Max HR (secs)'] + dforiginal['Time in HR Load Zone 96% - 100% Max HR (secs)'])/60
    dforiginal.insert(loc = 42, column = 'Højintens løb', value= Højintens_løb)
    dforiginal.insert(loc = 43, column = 'Sprint', value= Sprint)
    dforiginal.insert(loc = 44, column = 'Hårde Accelerationer', value = Hårde_accelerationer)
    dforiginal.insert(loc = 45, column = 'Hårde deccelerationer', value=Hårde_deccelerationer)
    dforiginal.insert(loc = 46, column = 'Tid med høj puls', value=Tid_med_høj_puls)
    dforiginal['Date'] = dforiginal['Date'].astype(str)
    df_GPS = dforiginal[['Date','Player Name','Ugenummer','Distance (km)','Top Speed (km/h)','Højintens løb','Sprint','Hårde Accelerationer','Hårde deccelerationer','Tid med høj puls','Trup']]
    Trup = ['U17','U19']
    option0 = st.selectbox('Vælg trup',Trup)
    df_GPS = df_GPS.loc[df_GPS.loc[df_GPS['Trup'] == option0,'Trup'].index.values]
    df_GPSgennemsnit = df_GPS[['Ugenummer','Player Name','Date','Distance (km)', 'Top Speed (km/h)', 'Højintens løb', 'Sprint', 'Hårde Accelerationer', 'Hårde deccelerationer','Tid med høj puls']]
    df_GPSgennemsnit = df_GPSgennemsnit.groupby(['Date']).mean(numeric_only=True)
    df_GPSgennemsnit['Ugenummer'] = df_GPSgennemsnit['Ugenummer'].astype(int)
    st.write('Trupgennemsnit pr. dag')
    st.line_chart(df_GPSgennemsnit,y=['Sprint','Distance (km)','Top Speed (km/h)','Højintens løb','Hårde Accelerationer','Hårde deccelerationer','Tid med høj puls'],)
    st.dataframe(df_GPSgennemsnit)
    spillere = df_GPS.drop_duplicates(subset=['Player Name'])
    option = st.selectbox('Vælg spiller',spillere['Player Name'])
    Ugenumre_sorteret = dforiginal.drop_duplicates(subset=['Ugenummer'])
    Ugenumre_sorteret = sorted(Ugenumre_sorteret['Ugenummer'])
    filtreret_GPSspiller = df_GPS.loc[df_GPS.loc[df_GPS['Player Name'] == option, 'Player Name'].index.values]

    df = filtreret_GPSspiller
    Ugenummer = df_GPS['Ugenummer']
    df_Ugenummer = []
    for i in Ugenummer:
        if i not in df_Ugenummer:
            if i !=None:
                df_Ugenummer.append(i)
    df_Ugenummer = sorted(df_Ugenummer)
    option2 = st.multiselect('Vælg ugenummer',df_Ugenummer)

    filtreret_dfugenummer = df_GPS.loc[df.loc[df_GPS.Ugenummer.isin(option2),'Ugenummer'].index.values]
    df = filtreret_dfugenummer
    df = df[df['Distance (km)'] !=0]
    df['Date'] = df['Date'].astype(str)
    df = df.rename(columns={'Date':'index'}).set_index('index')
    df = df[~df.index.duplicated()]
    afvigelser = pd.DataFrame(df)
    afvigelser['Distance (km)'] = df['Distance (km)'] / df_GPSgennemsnit['Distance (km)']
    afvigelser['Top Speed (km/h)'] = df['Top Speed (km/h)'] / df_GPSgennemsnit['Top Speed (km/h)']
    afvigelser['Højintens løb'] = df['Højintens løb'] / df_GPSgennemsnit['Højintens løb']
    afvigelser['Sprint'] = df['Sprint'] / df_GPSgennemsnit['Sprint']
    afvigelser['Hårde Accelerationer'] = df['Hårde Accelerationer'] / df_GPSgennemsnit['Hårde Accelerationer']
    afvigelser['Hårde deccelerationer'] = df['Hårde deccelerationer'] / df_GPSgennemsnit['Hårde deccelerationer']
    afvigelser['Tid med høj puls'] = df['Tid med høj puls'] / df_GPSgennemsnit['Tid med høj puls']
    st.write('Afvigelser for den valgte spiller i forhold til truppens gennemsnit (1 = trupgennemsnittet for dagen)')
    st.line_chart(afvigelser,y=['Sprint','Distance (km)','Top Speed (km/h)','Højintens løb','Hårde Accelerationer','Hårde deccelerationer','Tid med høj puls'],)
    st.write('Tabel for afvigelser (1 = trupgennemsnittet for dagen)')
    st.dataframe(afvigelser)
    st.write('Absolutte tal for den valgte spiller')
    st.dataframe(df)
    print('GPS data')

def Teamsheet():
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    import os
    dfbenchmark = pd.read_excel('Benchmarks.xlsx')
    dfårgange = dfbenchmark['Årgang'].drop_duplicates(keep='last')
    option2 = st.selectbox('Vælg årgang',dfårgange)
    df = pd.read_excel('Team Stats Horsens U15.xlsx')
    df = df.iloc[2:]
    df2 = pd.read_excel('Team Stats Horsens U17.xlsx')
    df2 = df2.iloc[2:]
    df3 = pd.read_excel('Team Stats Horsens U19.xlsx')
    df3 = df3.iloc[2:]
    df = df.append(df2).append(df3)
    df = pd.DataFrame(df)
    df = df[df['Team'].str.contains(option2)]

    df.columns = df.columns.astype(str)
    df.columns = df.columns.str.replace('Unnamed: 80','Forward pass accuracy')
    df.columns = df.columns.str.replace('Unnamed: 9','Shots on target')
    dfbenchmark = dfbenchmark.loc[dfbenchmark.loc[dfbenchmark.Årgang ==(option2),'Årgang'].index.values]
    df['Deep completions'] = df['Deep completed crosses'] + df['Deep completed passes']
    df['xG/shot'] = df['xG']/df['Shots / on target']
    df['Forward pass score'] = ((df['Forward passes / accurate']/df['Passes / accurate'])+(df['Forward pass accuracy']/100))/2
    df['Touches in box'] = df['Touches in penalty area']
    df['Shots against'] = df['Shots / on target'].shift(-1)
    df['xG against'] = df['xG'].shift(-1)
    df['Deep completions against'] = df['Deep completions'].shift(-1)
    df['Touches in box against'] = df['Touches in box'].shift(-1)
    df['Smart passes against'] = df['Smart passes / accurate'].shift(-1)
    df.columns = df.columns.str.replace('Shots / on target','Shots')
    df2 = df[['Date','Match','Team','Scheme','Goals','Possession, %','Unnamed: 13', 'Duels / won','Unnamed: 25','xG','PPDA','Deep completions','Smart passes / accurate','Touches in box','Shots','Shots on target','Forward pass score','Shots against','xG against','Deep completions against','Touches in box against','Interceptions','Unnamed: 66','Smart passes against','xG/shot']]
    df2.columns = df2.columns.str.replace('Unnamed: 13','Accurate passes, %')
    df2.columns = df2.columns.str.replace('Unnamed: 25','Duels won, %')
    df2.columns = df2.columns.str.replace('Unnamed: 66','Defensive duels won, %')
    df2.columns = df2.columns.str.replace('Duels / won','Duels')
    df2.columns = df2.columns.str.replace('Smart passes / accurate','Smart passes')
    df3 = df2[df2['Team'].str.contains('Horsens')]
    df2overordnet = df2[['Date','Match','Team','Scheme','Goals','Possession, %','Duels','Duels won, %','xG','PPDA']]
    dfmålbare = df3[['Match','Team','Forward pass score','Touches in box','xG','xG/shot','Shots','Shots on target','Deep completions','Smart passes','xG against','PPDA','Shots against','Interceptions','Defensive duels won, %','Deep completions against','Touches in box against','Smart passes against']]
    dfkampe = df2['Match'].drop_duplicates(keep='last')

    option = st.multiselect('Vælg kamp (Hvis ingen kamp er valgt, vises gennemsnit for alle)',dfkampe)
    if len(option) > 0:
        temp_select = option
    else:
        temp_select = dfkampe
    
    filtreretdfoverordnet = df2overordnet.loc[df2overordnet.loc[df2overordnet.Match.isin(temp_select),'Match'].index.values]
    filtreretdfoverordnet = filtreretdfoverordnet.groupby(['Team']).mean(numeric_only=True)
    filtreret_dfkamp = dfmålbare.loc[dfmålbare.loc[dfmålbare.Match.isin(temp_select),'Match'].index.values]
    filtreret_dfkamp = filtreret_dfkamp.drop(['Match'],axis=1)
    #filtreret_dfkamp = filtreret_dfkamp.groupby(['Team']).mean(numeric_only=True)

    dfsammenligning = filtreret_dfkamp.append(dfbenchmark)
    dfsammenligning = dfsammenligning.groupby(['Team']).mean(numeric_only=True)
    #dfsammenligning['Team'] = dfsammenligning['Team'].astype(str)
    #dfsammenligning = dfsammenligning.rename(columns={'index':'Team'}).set_index('Team')
    st.write('Generelle stats')
    st.dataframe(filtreretdfoverordnet)
    st.write('Grænseværdier')
    st.dataframe(dfsammenligning)
    
    import plotly.graph_objs as go
    import numpy as np
    from plotly.subplots import make_subplots

    trace1 = go.Indicator(mode="gauge+number",    value=dfsammenligning['Forward pass score'][1],domain={'row' : 1, 'column' : 1},title={'text': "Forward pass score"},gauge={'axis':{'range':[dfsammenligning['Forward pass score'][2],dfsammenligning['Forward pass score'][0]]},})
    trace2 = go.Indicator(mode="gauge+number",    value=dfsammenligning['Touches in box'][1],domain={'row' : 1, 'column' : 2},title={'text': "Touches in box"},gauge={'axis':{'range':[dfsammenligning['Touches in box'][2],dfsammenligning['Touches in box'][0]]},})
    trace3 = go.Indicator(mode="gauge+number",    value=dfsammenligning['xG'][1],domain={'row' : 1, 'column' : 3},title={'text': "xG"},gauge={'axis':{'range':[dfsammenligning['xG'][2],dfsammenligning['xG'][0]]},})
    trace4 = go.Indicator(mode="gauge+number",    value=dfsammenligning['xG/shot'][1],domain={'row' : 1, 'column' : 4},title={'text': "xG/shot"},gauge={'axis':{'range':[dfsammenligning['xG/shot'][2],dfsammenligning['xG/shot'][0]]},'steps':[{'range':[0,dfsammenligning['xG/shot'][2]],'color':'red'}]})
    trace5 = go.Indicator(mode="gauge+number",    value=dfsammenligning['Shots'][1],domain={'row' : 2, 'column' : 1},title={'text': "Shots"},gauge={'axis':{'range':[dfsammenligning['Shots'][2],dfsammenligning['Shots'][0]]},})
    trace6 = go.Indicator(mode="gauge+number",    value=dfsammenligning['Shots on target'][1],domain={'row' : 2, 'column' : 2},title={'text': "Shots on target"},gauge={'axis':{'range':[dfsammenligning['Shots on target'][2],dfsammenligning['Shots on target'][0]]},})
    trace7 = go.Indicator(mode="gauge+number",    value=dfsammenligning['Deep completions'][1],domain={'row' : 2, 'column' : 3},title={'text': "Deep completions"},gauge={'axis':{'range':[dfsammenligning['Deep completions'][2],dfsammenligning['Deep completions'][0]]},})
    trace8 = go.Indicator(mode="gauge+number",    value=dfsammenligning['Smart passes'][1],domain={'row' : 2, 'column' : 4},title={'text': "Smart passes"},gauge={'axis':{'range':[dfsammenligning['Smart passes'][2],dfsammenligning['Smart passes'][0]]},})
    
    fig = make_subplots(
    rows=2,
    cols=4,
    specs=[[{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'}],[{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'}]],
    )

    fig.append_trace(trace1, row=1, col=1)
    fig.append_trace(trace2, row=1, col=2)
    fig.append_trace(trace3, row=1, col=3)
    fig.append_trace(trace4, row=1, col=4)
    fig.append_trace(trace5, row=2, col=1)
    fig.append_trace(trace6, row=2, col=2)
    fig.append_trace(trace7, row=2, col=3)
    fig.append_trace(trace8, row=2, col=4)
    
    st.title('Offensive parametre')
    st.write('Skalaen går fra sidste års gennemsnit til sidste års ligagennemsnit, ved ingen udfyldning er den rød, delvis udfyldning er gul, helt fyldt er grøn')
    st.plotly_chart(fig,use_container_width=True)
    
    trace9 = go.Indicator(mode="gauge+number",    value=dfsammenligning['xG against'][1],domain={'row' : 1, 'column' : 1},title={'text': "xG against"},gauge={'axis':{'range':[dfsammenligning['xG against'][2],dfsammenligning['xG against'][0]]}})
    trace10 = go.Indicator(mode="gauge+number",    value=dfsammenligning['PPDA'][1],domain={'row' : 1, 'column' : 2},title={'text': "PPDA"},gauge={'axis':{'range':[dfsammenligning['PPDA'][2],dfsammenligning['PPDA'][0]]}})
    trace11 = go.Indicator(mode="gauge+number",    value=dfsammenligning['Shots against'][1],domain={'row' : 1, 'column' : 3},title={'text': "Shots against"},gauge={'axis':{'range':[dfsammenligning['Shots against'][2],dfsammenligning['Shots against'][0]]}})
    trace12 = go.Indicator(mode="gauge+number",    value=dfsammenligning['Interceptions'][1],domain={'row' : 1, 'column' : 4},title={'text': "Interceptions"},gauge={'axis':{'range':[dfsammenligning['Interceptions'][2],dfsammenligning['Interceptions'][0]]}})
    trace13 = go.Indicator(mode="gauge+number",    value=dfsammenligning['Defensive duels won, %'][1],domain={'row' : 2, 'column' : 1},title={'text': "Defensive duels won"},gauge={'axis':{'range':[dfsammenligning['Defensive duels won, %'][2],dfsammenligning['Defensive duels won, %'][0]]}})
    trace14 = go.Indicator(mode="gauge+number",    value=dfsammenligning['Deep completions against'][1],domain={'row' : 2, 'column' : 2},title={'text': "Deep completions against"},gauge={'axis':{'range':[dfsammenligning['Deep completions against'][2],dfsammenligning['Deep completions against'][0]]}})
    trace15 = go.Indicator(mode="gauge+number",    value=dfsammenligning['Touches in box against'][1],domain={'row' : 2, 'column' : 3},title={'text': "Touches in box against"},gauge={'axis':{'range':[dfsammenligning['Touches in box against'][2],dfsammenligning['Touches in box against'][0]]}})
    trace16 = go.Indicator(mode="gauge+number",    value=dfsammenligning['Smart passes against'][1],domain={'row' : 2, 'column' : 4},title={'text': "Smart passes against"},gauge={'axis':{'range':[dfsammenligning['Smart passes against'][2],dfsammenligning['Smart passes against'][0]]}})
    fig1 = make_subplots(
    rows=2,
    cols=4,
    specs=[[{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'}],[{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'},{'type' : 'indicator'}]],
    )

    fig1.append_trace(trace9, row=1, col=1)
    fig1.append_trace(trace10, row=1, col=2)
    fig1.append_trace(trace11, row=1, col=3)
    fig1.append_trace(trace12, row=1, col=4)
    fig1.append_trace(trace13, row=2, col=1)
    fig1.append_trace(trace14, row=2, col=2)
    fig1.append_trace(trace15, row=2, col=3)
    fig1.append_trace(trace16, row=2, col=4)
    st.title('Defensive parametre')
    st.write('Skalaen går fra sidste års gennemsnit til sidste års ligagennemsnit, ved ingen udfyldning er den rød, delvis udfyldning er gul, helt fyldt er grøn')
    st.plotly_chart(fig1,use_container_width=True)
    print('teamsheet')
def Individuelt_dashboard():
    import pandas as pd
    import openpyxl
    import numpy as np
    import matplotlib.pyplot as plt
    import plotly.express as px 
    import time
    import plotly.graph_objects as go

    def U19():
        U19navne = pd.read_excel('Navne.xlsx')
        dfU19 = pd.read_excel('U19 spillere sæson.xlsx')
        dfU19 = dfU19[dfU19['Minutes played'] >= 300]
        dfU19['Position'] = dfU19['Position'].astype(str)
        dfU19['Team'] = dfU19['Team'].astype(str)
        
        #Dele spillerne i ligaen ud på positioner
        df_backsU19 = dfU19[dfU19['Position'].str.contains('|'.join(['LB', 'RB']))]
        df_StoppereU19 = dfU19[dfU19['Position'].str.contains('|'.join(['CB']))]
        df_Centrale_midtU19 = dfU19[dfU19['Position'].str.contains('|'.join(['CM','AMF','DMF']))]
        df_KanterU19 = dfU19[dfU19['Position'].str.contains('|'.join(['RW','LW','RAMF','LAMF']))]
        df_AngribereU19 = dfU19[dfU19['Position'].str.contains('|'.join(['CF']))]
        
        #Rangere stoppere i ligaen og give dem 1-5 i rating på forskellige parametre
        df_StoppereU19['Def duels won score'] = pd.qcut(df_StoppereU19['Defensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate passes, % score'] = pd.qcut(df_StoppereU19['Accurate passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate long passes, % score'] = pd.qcut(df_StoppereU19['Accurate long passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Forward passes per 90 score'] = pd.qcut(df_StoppereU19['Forward passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate forward passes score'] = pd.qcut(df_StoppereU19['Accurate forward passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate short/medium passes, % score'] = pd.qcut(df_StoppereU19['Accurate short / medium passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Interceptions per 90 score'] = pd.qcut(df_StoppereU19['Interceptions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['PAdj Interceptions score'] = pd.qcut(df_StoppereU19['PAdj Interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Successful defensive actions per 90 score'] = pd.qcut(df_StoppereU19['Successful defensive actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Shots blocked per 90 score'] = pd.qcut(df_StoppereU19['Shots blocked per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate forward passes, %'] = pd.qcut(df_StoppereU19['Accurate forward passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate passes to finale third, % score'] = pd.qcut(df_StoppereU19['Accurate passes to final third, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate progressive passes, % score'] = pd.qcut(df_StoppereU19['Accurate progressive passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Deep completions per 90 score'] = pd.qcut(df_StoppereU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Offensive duels won, % score'] = pd.qcut(df_StoppereU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Progressive runs per 90 score'] = pd.qcut(df_StoppereU19['Progressive runs per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Successful dribbles, % score'] = pd.qcut(df_StoppereU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Aerial duels won, % score'] = pd.qcut(df_StoppereU19['Aerial duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate through passes, % score'] = pd.qcut(df_StoppereU19['Accurate through passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19 = df_StoppereU19[df_StoppereU19['Team'].str.contains('Horsens')]
        df_StoppereU19 = U19navne.merge(df_StoppereU19)
        
        #Oprette forskellige parametre ud fra talent-id for stoppere
        df_StoppereU19['Pasningssikker Stopper'] = (df_StoppereU19['Accurate passes, % score'] + df_StoppereU19['Accurate long passes, % score'] + df_StoppereU19['Forward passes per 90 score'] + df_StoppereU19['Accurate forward passes score'] + df_StoppereU19['Accurate forward passes score'] + df_StoppereU19['Accurate short/medium passes, % score'] + df_StoppereU19['Forward passes per 90 score'] + df_StoppereU19['Accurate forward passes score'])/8
        df_StoppereU19['Spilintelligens defensivt Stopper'] = (df_StoppereU19['Interceptions per 90 score'] + df_StoppereU19['Successful defensive actions per 90 score']+df_StoppereU19['Shots blocked per 90 score'] + df_StoppereU19['PAdj Interceptions score'] + df_StoppereU19['PAdj Interceptions score'] + df_StoppereU19['Interceptions per 90 score'])/6
        df_StoppereU19['Spilintelligens offensivt Stopper'] = (df_StoppereU19['Accurate forward passes score'] + df_StoppereU19['Accurate passes to finale third, % score'] + df_StoppereU19['Accurate progressive passes, % score'] + df_StoppereU19['Accurate through passes, % score'] + df_StoppereU19['Deep completions per 90 score'] + df_StoppereU19['Offensive duels won, % score'] + df_StoppereU19['Progressive runs per 90 score'] + df_StoppereU19['Successful dribbles, % score'] + df_StoppereU19['Accurate forward passes score'])/9
        df_StoppereU19['Nærkamps- og duelstærk Stopper'] = (df_StoppereU19['Def duels won score'] + df_StoppereU19['Aerial duels won, % score'] + df_StoppereU19['Def duels won score'] + df_StoppereU19['Def duels won score'])/4
        df_StoppereU19 = df_StoppereU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Pasningssikker Stopper','Spilintelligens defensivt Stopper','Spilintelligens offensivt Stopper','Nærkamps- og duelstærk Stopper']]
        
        #Samme proces med backs
        df_backsU19['Accurate crosses, % score'] = pd.qcut(df_backsU19['Accurate crosses, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['xA per 90 score'] = pd.qcut(df_backsU19['xA per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Deep completions per 90 score'] = pd.qcut(df_backsU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Deep completed crosses per 90 score'] = pd.qcut(df_backsU19['Deep completed crosses per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Successful dribbles, % score'] = pd.qcut(df_backsU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Defensive duels won, % score'] = pd.qcut(df_backsU19['Defensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Progressive runs per 90 score'] = pd.qcut(df_backsU19['Progressive runs per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Offensive duels won, % score'] = pd.qcut(df_backsU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Accelerations per 90 score'] = pd.qcut(df_backsU19['Accelerations per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Duels won, % score'] = pd.qcut(df_backsU19['Duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Interceptions per 90 score'] = pd.qcut(df_backsU19['Interceptions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Successful defensive actions per 90 score'] = pd.qcut(df_backsU19['Successful defensive actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19 = df_backsU19[df_backsU19['Team'].str.contains('Horsens')]
        df_backsU19 = U19navne.merge(df_backsU19)
        
        df_backsU19['Indlægsstærk Back'] = (df_backsU19['Accurate crosses, % score'] + df_backsU19['xA per 90 score'] + df_backsU19['Deep completed crosses per 90 score'] + df_backsU19['Deep completed crosses per 90 score'])/4
        df_backsU19['1v1 færdigheder Back'] = (df_backsU19['Successful dribbles, % score'] + df_backsU19['Defensive duels won, % score'] + df_backsU19['Progressive runs per 90 score'] + df_backsU19['Offensive duels won, % score'] + df_backsU19['Accelerations per 90 score'] + df_backsU19['Duels won, % score'])/6
        df_backsU19['Spilintelligens defensivt Back'] = (df_backsU19['Interceptions per 90 score'] + df_backsU19['Successful defensive actions per 90 score'] + df_backsU19['Duels won, % score'] + df_backsU19['Defensive duels won, % score'])/4
        df_backsU19 = df_backsU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Indlægsstærk Back','1v1 færdigheder Back','Spilintelligens defensivt Back']]
        
        #Samme proces med centrale midt
        df_Centrale_midtU19['Accurate passes, % score'] = pd.qcut(df_Centrale_midtU19['Accurate passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Accurate forward passes, % score'] = pd.qcut(df_Centrale_midtU19['Accurate forward passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Accurate long passes, % score'] = pd.qcut(df_Centrale_midtU19['Accurate long passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Key passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Key passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Smart passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Smart passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Deep completions per 90 score'] = pd.qcut(df_Centrale_midtU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Through passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Through passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Progressive passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Progressive passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Offensive duels won, % score'] = pd.qcut(df_Centrale_midtU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Received passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Received passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Successful dribbles, % score'] = pd.qcut(df_Centrale_midtU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Successful defensive actions per 90 score'] = pd.qcut(df_Centrale_midtU19['Successful defensive actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Interceptions per 90 score'] = pd.qcut(df_Centrale_midtU19['Interceptions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Duels won, % score'] = pd.qcut(df_Centrale_midtU19['Duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Defensive duels won, % score'] = pd.qcut(df_Centrale_midtU19['Defensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['PAdj Interceptions score'] = pd.qcut(df_Centrale_midtU19['PAdj Interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19 = df_Centrale_midtU19[df_Centrale_midtU19['Team'].str.contains('Horsens')]
        df_Centrale_midtU19 = U19navne.merge(df_Centrale_midtU19)
        df_Centrale_midtU19['Pasningssikker/spilvendinger Central midt'] = (df_Centrale_midtU19['Accurate passes, % score'] + df_Centrale_midtU19['Accurate forward passes, % score'] + df_Centrale_midtU19['Accurate long passes, % score'] + df_Centrale_midtU19['Accurate passes, % score'] + df_Centrale_midtU19['Key passes per 90 score'] + df_Centrale_midtU19['Accurate forward passes, % score'] + df_Centrale_midtU19['Smart passes per 90 score'] + df_Centrale_midtU19['Deep completions per 90 score'] + df_Centrale_midtU19['Through passes per 90 score'] + df_Centrale_midtU19['Progressive passes per 90 score'])/10
        df_Centrale_midtU19['Boldfast Central midt'] = (df_Centrale_midtU19['Offensive duels won, % score'] + df_Centrale_midtU19['Received passes per 90 score'] + df_Centrale_midtU19['Accurate passes, % score'] + df_Centrale_midtU19['Successful dribbles, % score'] + df_Centrale_midtU19['Accurate passes, % score'])/5
        df_Centrale_midtU19['Spilintelligens defensivt Central midt'] = (df_Centrale_midtU19['Interceptions per 90 score'] + df_Centrale_midtU19['Successful defensive actions per 90 score'] + df_Centrale_midtU19['Duels won, % score'] + df_Centrale_midtU19['Defensive duels won, % score'] + df_Centrale_midtU19['PAdj Interceptions score'] + df_Centrale_midtU19['PAdj Interceptions score'])/6
        df_Centrale_midtU19 = df_Centrale_midtU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Pasningssikker/spilvendinger Central midt','Boldfast Central midt', 'Spilintelligens defensivt Central midt']]
        
        df_KanterU19['xG per 90 score'] = pd.qcut(df_KanterU19['xG per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Goals per 90 score'] = pd.qcut(df_KanterU19['Goals per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Shots on target, % score'] = pd.qcut(df_KanterU19['Shots on target, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Successful dribbles, % score'] = pd.qcut(df_KanterU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate passes, % score'] = pd.qcut(df_KanterU19['Accurate passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate forward passes, % score'] = pd.qcut(df_KanterU19['Accurate forward passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Deep completions per 90 score'] = pd.qcut(df_KanterU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate through passes, % score'] = pd.qcut(df_KanterU19['Accurate through passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate progressive passes, % score'] = pd.qcut(df_KanterU19['Accurate progressive passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Successful attacking actions per 90 score'] = pd.qcut(df_KanterU19['Successful attacking actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate passes to final third, % score'] = pd.qcut(df_KanterU19['Accurate passes to final third, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Offensive duels won, % score'] = pd.qcut(df_KanterU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['xA per 90 score'] = pd.qcut(df_KanterU19['xA per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate smart passes, % score'] = pd.qcut(df_KanterU19['Accurate smart passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate crosses, % score'] = pd.qcut(df_KanterU19['Accurate crosses, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Successful attacking actions per 90 score'] = pd.qcut(df_KanterU19['Successful attacking actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Smart passes per 90 score'] = pd.qcut(df_KanterU19['Smart passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Key passes per 90 score'] = pd.qcut(df_KanterU19['Key passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19 = df_KanterU19[df_KanterU19['Team'].str.contains('Horsens')]
        df_KanterU19 = U19navne.merge(df_KanterU19)
        
        df_KanterU19['Sparkefærdigheder Kant'] = (df_KanterU19['xG per 90 score'] + df_KanterU19['Goals per 90 score'] + df_KanterU19['Shots on target, % score'])/3
        df_KanterU19['1v1 Offensivt Kant'] = (df_KanterU19['Successful dribbles, % score'] + df_KanterU19['Successful dribbles, % score'] + df_KanterU19['Offensive duels won, % score'])/3
        df_KanterU19['Kombinationsstærk Kant'] = (df_KanterU19['Accurate passes, % score'] + df_KanterU19['Accurate forward passes, % score'] + df_KanterU19['Deep completions per 90 score'] + df_KanterU19['Accurate through passes, % score'] + df_KanterU19['Accurate progressive passes, % score'] + df_KanterU19['Successful attacking actions per 90 score'] + df_KanterU19['Accurate passes to final third, % score'])/7
        df_KanterU19['Spilintelligens offensivt/indlægsstærk Kant'] = (df_KanterU19['xA per 90 score'] + df_KanterU19['xG per 90 score'] + df_KanterU19['xA per 90 score'] + df_KanterU19['xG per 90 score'] + df_KanterU19['Accurate through passes, % score'] + df_KanterU19['Accurate smart passes, % score'] + df_KanterU19['Accurate forward passes, % score'] + df_KanterU19['Accurate progressive passes, % score'] + df_KanterU19['Accurate passes to final third, % score'] + df_KanterU19['Accurate crosses, % score'] + df_KanterU19['Successful attacking actions per 90 score'] + df_KanterU19['Smart passes per 90 score'] + df_KanterU19['Key passes per 90 score'])/13
        df_KanterU19 = df_KanterU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Sparkefærdigheder Kant','1v1 Offensivt Kant','Kombinationsstærk Kant','Spilintelligens offensivt/indlægsstærk Kant']]

        df_AngribereU19['xG per 90 score'] = pd.qcut(df_AngribereU19['xG per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Goals per 90 score'] = pd.qcut(df_AngribereU19['Goals per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)  
        df_AngribereU19['Shots on target, % score'] = pd.qcut(df_AngribereU19['Shots on target, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)   
        df_AngribereU19['Offensive duels won, % score'] = pd.qcut(df_AngribereU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Duels won, % score'] = pd.qcut(df_AngribereU19['Duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Accurate passes, % score'] = pd.qcut(df_AngribereU19['Accurate passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Successful dribbles, % score'] = pd.qcut(df_AngribereU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['xA per 90 score'] = pd.qcut(df_AngribereU19['xA per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Touches in box per 90 score'] = pd.qcut(df_AngribereU19['Touches in box per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Deep completions per 90 score'] = pd.qcut(df_AngribereU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Successful attacking actions per 90 score'] = pd.qcut(df_AngribereU19['Successful attacking actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    
        df_AngribereU19 = df_AngribereU19[df_AngribereU19['Team'].str.contains('Horsens')]
        df_AngribereU19 = U19navne.merge(df_AngribereU19)
        
        df_AngribereU19['Sparkefærdigheder Angriber'] = (df_AngribereU19['xG per 90 score'] + df_AngribereU19['xG per 90 score'] + df_AngribereU19['Goals per 90 score'] + df_AngribereU19['Shots on target, % score'])/4
        df_AngribereU19['Boldfast Angriber'] = (df_AngribereU19['Offensive duels won, % score'] + df_AngribereU19['Offensive duels won, % score'] + df_AngribereU19['Duels won, % score'] + df_AngribereU19['Accurate passes, % score'] + df_AngribereU19['Successful dribbles, % score'])/5
        df_AngribereU19['Spilintelligens offensivt Angriber'] = (df_AngribereU19['xA per 90 score'] + df_AngribereU19['xG per 90 score'] + df_AngribereU19['Touches in box per 90 score'] + df_AngribereU19['Deep completions per 90 score'] + df_AngribereU19['Successful attacking actions per 90 score'] + df_AngribereU19['Touches in box per 90 score'] + df_AngribereU19['xG per 90 score'])/7
        
        df_AngribereU19 = df_AngribereU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Sparkefærdigheder Angriber','Boldfast Angriber','Spilintelligens offensivt Angriber']]
        
        
        df_samlet = df_StoppereU19.append(df_backsU19).append(df_Centrale_midtU19).append(df_KanterU19).append(df_AngribereU19)
        dfspillere = df_samlet['Spillere'].drop_duplicates(keep='last')
        dfspillere = dfspillere.astype(str)
        dfspillere = sorted(dfspillere)
        option2 = st.selectbox('Vælg spiller',dfspillere)
        df_samlet = df_samlet[df_samlet['Spillere'].str.contains(option2)]
        df_samlet = df_samlet.groupby(['Spillere']).mean(numeric_only=True)

        #Start på seneste 5 kampe
        dfU19s5 = pd.read_excel('U19 spillere seneste 5.xlsx')
        dfU19s5 = dfU19s5[dfU19s5['Minutes played'] >= 200]
        dfU19s5['Position'] = dfU19s5['Position'].astype(str)
        dfU19s5['Team'] = dfU19s5['Team'].astype(str)
        
        #Dele spillerne i ligaen ud på positioner
        df_backsU19 = dfU19s5[dfU19s5['Position'].str.contains('|'.join(['LB', 'RB']))]
        df_StoppereU19 = dfU19s5[dfU19s5['Position'].str.contains('|'.join(['CB']))]
        df_Centrale_midtU19 = dfU19s5[dfU19s5['Position'].str.contains('|'.join(['CM','AMF','DMF']))]
        df_KanterU19 = dfU19s5[dfU19s5['Position'].str.contains('|'.join(['RW','LW','RAMF','LAMF']))]
        df_AngribereU19 = dfU19s5[dfU19s5['Position'].str.contains('|'.join(['CF']))]
        
        #Rangere stoppere i ligaen og give dem 1-5 i rating på forskellige parametre
        df_StoppereU19['Def duels won score'] = pd.qcut(df_StoppereU19['Defensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate passes, % score'] = pd.qcut(df_StoppereU19['Accurate passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate long passes, % score'] = pd.qcut(df_StoppereU19['Accurate long passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Forward passes per 90 score'] = pd.qcut(df_StoppereU19['Forward passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate forward passes score'] = pd.qcut(df_StoppereU19['Accurate forward passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate short/medium passes, % score'] = pd.qcut(df_StoppereU19['Accurate short / medium passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Interceptions per 90 score'] = pd.qcut(df_StoppereU19['Interceptions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['PAdj Interceptions score'] = pd.qcut(df_StoppereU19['PAdj Interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Successful defensive actions per 90 score'] = pd.qcut(df_StoppereU19['Successful defensive actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Shots blocked per 90 score'] = pd.qcut(df_StoppereU19['Shots blocked per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate forward passes, %'] = pd.qcut(df_StoppereU19['Accurate forward passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate passes to finale third, % score'] = pd.qcut(df_StoppereU19['Accurate passes to final third, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate progressive passes, % score'] = pd.qcut(df_StoppereU19['Accurate progressive passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Deep completions per 90 score'] = pd.qcut(df_StoppereU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Offensive duels won, % score'] = pd.qcut(df_StoppereU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Progressive runs per 90 score'] = pd.qcut(df_StoppereU19['Progressive runs per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Successful dribbles, % score'] = pd.qcut(df_StoppereU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Aerial duels won, % score'] = pd.qcut(df_StoppereU19['Aerial duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate through passes, % score'] = pd.qcut(df_StoppereU19['Accurate through passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19 = df_StoppereU19[df_StoppereU19['Team'].str.contains('Horsens')]
        df_StoppereU19 = U19navne.merge(df_StoppereU19)
        
        #Oprette forskellige parametre ud fra talent-id for stoppere
        df_StoppereU19['Pasningssikker Stopper'] = (df_StoppereU19['Accurate passes, % score'] + df_StoppereU19['Accurate long passes, % score'] + df_StoppereU19['Forward passes per 90 score'] + df_StoppereU19['Accurate forward passes score'] + df_StoppereU19['Accurate forward passes score'] + df_StoppereU19['Accurate short/medium passes, % score'] + df_StoppereU19['Forward passes per 90 score'] + df_StoppereU19['Accurate forward passes score'])/8
        df_StoppereU19['Spilintelligens defensivt Stopper'] = (df_StoppereU19['Interceptions per 90 score'] + df_StoppereU19['Successful defensive actions per 90 score']+df_StoppereU19['Shots blocked per 90 score'] + df_StoppereU19['PAdj Interceptions score'] + df_StoppereU19['PAdj Interceptions score'] + df_StoppereU19['Interceptions per 90 score'])/6
        df_StoppereU19['Spilintelligens offensivt Stopper'] = (df_StoppereU19['Accurate forward passes score'] + df_StoppereU19['Accurate passes to finale third, % score'] + df_StoppereU19['Accurate progressive passes, % score'] + df_StoppereU19['Accurate through passes, % score'] + df_StoppereU19['Deep completions per 90 score'] + df_StoppereU19['Offensive duels won, % score'] + df_StoppereU19['Progressive runs per 90 score'] + df_StoppereU19['Successful dribbles, % score'] + df_StoppereU19['Accurate forward passes score'])/9
        df_StoppereU19['Nærkamps- og duelstærk Stopper'] = (df_StoppereU19['Def duels won score'] + df_StoppereU19['Aerial duels won, % score'] + df_StoppereU19['Def duels won score'] + df_StoppereU19['Def duels won score'])/4
        df_StoppereU19 = df_StoppereU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Pasningssikker Stopper','Spilintelligens defensivt Stopper','Spilintelligens offensivt Stopper','Nærkamps- og duelstærk Stopper']]
        
        #Samme proces med backs
        df_backsU19['Accurate crosses, % score'] = pd.qcut(df_backsU19['Accurate crosses, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['xA per 90 score'] = pd.qcut(df_backsU19['xA per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Deep completions per 90 score'] = pd.qcut(df_backsU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Deep completed crosses per 90 score'] = pd.qcut(df_backsU19['Deep completed crosses per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Successful dribbles, % score'] = pd.qcut(df_backsU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Defensive duels won, % score'] = pd.qcut(df_backsU19['Defensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Progressive runs per 90 score'] = pd.qcut(df_backsU19['Progressive runs per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Offensive duels won, % score'] = pd.qcut(df_backsU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Accelerations per 90 score'] = pd.qcut(df_backsU19['Accelerations per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Duels won, % score'] = pd.qcut(df_backsU19['Duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Interceptions per 90 score'] = pd.qcut(df_backsU19['Interceptions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Successful defensive actions per 90 score'] = pd.qcut(df_backsU19['Successful defensive actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19 = df_backsU19[df_backsU19['Team'].str.contains('Horsens')]
        df_backsU19 = U19navne.merge(df_backsU19)
        
        df_backsU19['Indlægsstærk Back'] = (df_backsU19['Accurate crosses, % score'] + df_backsU19['xA per 90 score'] + df_backsU19['Deep completed crosses per 90 score'] + df_backsU19['Deep completed crosses per 90 score'])/4
        df_backsU19['1v1 færdigheder Back'] = (df_backsU19['Successful dribbles, % score'] + df_backsU19['Defensive duels won, % score'] + df_backsU19['Progressive runs per 90 score'] + df_backsU19['Offensive duels won, % score'] + df_backsU19['Accelerations per 90 score'] + df_backsU19['Duels won, % score'])/6
        df_backsU19['Spilintelligens defensivt Back'] = (df_backsU19['Interceptions per 90 score'] + df_backsU19['Successful defensive actions per 90 score'] + df_backsU19['Duels won, % score'] + df_backsU19['Defensive duels won, % score'])/4
        df_backsU19 = df_backsU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Indlægsstærk Back','1v1 færdigheder Back','Spilintelligens defensivt Back']]
        
        #Samme proces med centrale midt
        df_Centrale_midtU19['Accurate passes, % score'] = pd.qcut(df_Centrale_midtU19['Accurate passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Accurate forward passes, % score'] = pd.qcut(df_Centrale_midtU19['Accurate forward passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Accurate long passes, % score'] = pd.qcut(df_Centrale_midtU19['Accurate long passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Key passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Key passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Smart passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Smart passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Deep completions per 90 score'] = pd.qcut(df_Centrale_midtU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Through passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Through passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Progressive passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Progressive passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Offensive duels won, % score'] = pd.qcut(df_Centrale_midtU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Received passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Received passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Successful dribbles, % score'] = pd.qcut(df_Centrale_midtU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Successful defensive actions per 90 score'] = pd.qcut(df_Centrale_midtU19['Successful defensive actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Interceptions per 90 score'] = pd.qcut(df_Centrale_midtU19['Interceptions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Duels won, % score'] = pd.qcut(df_Centrale_midtU19['Duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Defensive duels won, % score'] = pd.qcut(df_Centrale_midtU19['Defensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['PAdj Interceptions score'] = pd.qcut(df_Centrale_midtU19['PAdj Interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19 = df_Centrale_midtU19[df_Centrale_midtU19['Team'].str.contains('Horsens')]
        df_Centrale_midtU19 = U19navne.merge(df_Centrale_midtU19)
        df_Centrale_midtU19['Pasningssikker/spilvendinger Central midt'] = (df_Centrale_midtU19['Accurate passes, % score'] + df_Centrale_midtU19['Accurate forward passes, % score'] + df_Centrale_midtU19['Accurate long passes, % score'] + df_Centrale_midtU19['Accurate passes, % score'] + df_Centrale_midtU19['Key passes per 90 score'] + df_Centrale_midtU19['Accurate forward passes, % score'] + df_Centrale_midtU19['Smart passes per 90 score'] + df_Centrale_midtU19['Deep completions per 90 score'] + df_Centrale_midtU19['Through passes per 90 score'] + df_Centrale_midtU19['Progressive passes per 90 score'])/10
        df_Centrale_midtU19['Boldfast Central midt'] = (df_Centrale_midtU19['Offensive duels won, % score'] + df_Centrale_midtU19['Received passes per 90 score'] + df_Centrale_midtU19['Accurate passes, % score'] + df_Centrale_midtU19['Successful dribbles, % score'] + df_Centrale_midtU19['Accurate passes, % score'])/5
        df_Centrale_midtU19['Spilintelligens defensivt Central midt'] = (df_Centrale_midtU19['Interceptions per 90 score'] + df_Centrale_midtU19['Successful defensive actions per 90 score'] + df_Centrale_midtU19['Duels won, % score'] + df_Centrale_midtU19['Defensive duels won, % score'] + df_Centrale_midtU19['PAdj Interceptions score'] + df_Centrale_midtU19['PAdj Interceptions score'])/6
        df_Centrale_midtU19 = df_Centrale_midtU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Pasningssikker/spilvendinger Central midt','Boldfast Central midt', 'Spilintelligens defensivt Central midt']]
        
        df_KanterU19['xG per 90 score'] = pd.qcut(df_KanterU19['xG per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Goals per 90 score'] = pd.qcut(df_KanterU19['Goals per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Shots on target, % score'] = pd.qcut(df_KanterU19['Shots on target, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Successful dribbles, % score'] = pd.qcut(df_KanterU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate passes, % score'] = pd.qcut(df_KanterU19['Accurate passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate forward passes, % score'] = pd.qcut(df_KanterU19['Accurate forward passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Deep completions per 90 score'] = pd.qcut(df_KanterU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate through passes, % score'] = pd.qcut(df_KanterU19['Accurate through passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate progressive passes, % score'] = pd.qcut(df_KanterU19['Accurate progressive passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Successful attacking actions per 90 score'] = pd.qcut(df_KanterU19['Successful attacking actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate passes to final third, % score'] = pd.qcut(df_KanterU19['Accurate passes to final third, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Offensive duels won, % score'] = pd.qcut(df_KanterU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['xA per 90 score'] = pd.qcut(df_KanterU19['xA per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate smart passes, % score'] = pd.qcut(df_KanterU19['Accurate smart passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate crosses, % score'] = pd.qcut(df_KanterU19['Accurate crosses, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Successful attacking actions per 90 score'] = pd.qcut(df_KanterU19['Successful attacking actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Smart passes per 90 score'] = pd.qcut(df_KanterU19['Smart passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Key passes per 90 score'] = pd.qcut(df_KanterU19['Key passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19 = df_KanterU19[df_KanterU19['Team'].str.contains('Horsens')]
        df_KanterU19 = U19navne.merge(df_KanterU19)
        
        df_KanterU19['Sparkefærdigheder Kant'] = (df_KanterU19['xG per 90 score'] + df_KanterU19['Goals per 90 score'] + df_KanterU19['Shots on target, % score'])/3
        df_KanterU19['1v1 Offensivt Kant'] = (df_KanterU19['Successful dribbles, % score'] + df_KanterU19['Successful dribbles, % score'] + df_KanterU19['Offensive duels won, % score'])/3
        df_KanterU19['Kombinationsstærk Kant'] = (df_KanterU19['Accurate passes, % score'] + df_KanterU19['Accurate forward passes, % score'] + df_KanterU19['Deep completions per 90 score'] + df_KanterU19['Accurate through passes, % score'] + df_KanterU19['Accurate progressive passes, % score'] + df_KanterU19['Successful attacking actions per 90 score'] + df_KanterU19['Accurate passes to final third, % score'])/7
        df_KanterU19['Spilintelligens offensivt/indlægsstærk Kant'] = (df_KanterU19['xA per 90 score'] + df_KanterU19['xG per 90 score'] + df_KanterU19['xA per 90 score'] + df_KanterU19['xG per 90 score'] + df_KanterU19['Accurate through passes, % score'] + df_KanterU19['Accurate smart passes, % score'] + df_KanterU19['Accurate forward passes, % score'] + df_KanterU19['Accurate progressive passes, % score'] + df_KanterU19['Accurate passes to final third, % score'] + df_KanterU19['Accurate crosses, % score'] + df_KanterU19['Successful attacking actions per 90 score'] + df_KanterU19['Smart passes per 90 score'] + df_KanterU19['Key passes per 90 score'])/13
        df_KanterU19 = df_KanterU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Sparkefærdigheder Kant','1v1 Offensivt Kant','Kombinationsstærk Kant','Spilintelligens offensivt/indlægsstærk Kant']]

        df_AngribereU19['xG per 90 score'] = pd.qcut(df_AngribereU19['xG per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Goals per 90 score'] = pd.qcut(df_AngribereU19['Goals per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)  
        df_AngribereU19['Shots on target, % score'] = pd.qcut(df_AngribereU19['Shots on target, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)   
        df_AngribereU19['Offensive duels won, % score'] = pd.qcut(df_AngribereU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Duels won, % score'] = pd.qcut(df_AngribereU19['Duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Accurate passes, % score'] = pd.qcut(df_AngribereU19['Accurate passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Successful dribbles, % score'] = pd.qcut(df_AngribereU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['xA per 90 score'] = pd.qcut(df_AngribereU19['xA per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Touches in box per 90 score'] = pd.qcut(df_AngribereU19['Touches in box per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Deep completions per 90 score'] = pd.qcut(df_AngribereU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Successful attacking actions per 90 score'] = pd.qcut(df_AngribereU19['Successful attacking actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    
        df_AngribereU19 = df_AngribereU19[df_AngribereU19['Team'].str.contains('Horsens')]
        df_AngribereU19 = U19navne.merge(df_AngribereU19)
        
        df_AngribereU19['Sparkefærdigheder Angriber'] = (df_AngribereU19['xG per 90 score'] + df_AngribereU19['xG per 90 score'] + df_AngribereU19['Goals per 90 score'] + df_AngribereU19['Shots on target, % score'])/4
        df_AngribereU19['Boldfast Angriber'] = (df_AngribereU19['Offensive duels won, % score'] + df_AngribereU19['Offensive duels won, % score'] + df_AngribereU19['Duels won, % score'] + df_AngribereU19['Accurate passes, % score'] + df_AngribereU19['Successful dribbles, % score'])/5
        df_AngribereU19['Spilintelligens offensivt Angriber'] = (df_AngribereU19['xA per 90 score'] + df_AngribereU19['xG per 90 score'] + df_AngribereU19['Touches in box per 90 score'] + df_AngribereU19['Deep completions per 90 score'] + df_AngribereU19['Successful attacking actions per 90 score'] + df_AngribereU19['Touches in box per 90 score'] + df_AngribereU19['xG per 90 score'])/7
        
        df_AngribereU19 = df_AngribereU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Sparkefærdigheder Angriber','Boldfast Angriber','Spilintelligens offensivt Angriber']]
        
        
        df_samlets5 = df_StoppereU19.append(df_backsU19).append(df_Centrale_midtU19).append(df_KanterU19).append(df_AngribereU19)
        df_samlets5 = df_samlets5[df_samlets5['Spillere'].str.contains(option2)]
        df_samlets5 = df_samlets5.groupby(['Spillere']).mean(numeric_only=True)


        df_samlet = df_samlet.append(df_samlets5)

        option3 = st.selectbox('Vælg position',('Stopper','Back','Central midt','Kant','Angriber'))

        df_samlet = df_samlet.filter(regex=option3)
        df_samlet['Datasæt'] = 'Seneste 5 kampe'
        df_samlet['Datasæt'][0] = 'Hele sæsonen'
        df_samlet = df_samlet.rename(columns = lambda x: x.replace(option3, ''))
        df_samletvendtom = df_samlet.reset_index()
        df_samletvendtom['Unique'] = df_samletvendtom['Spillere'] + df_samletvendtom['Datasæt']
        df_samletvendtom = pd.DataFrame.drop(df_samletvendtom,axis=1,columns='Spillere')
        df_samletvendtom = df_samletvendtom.transpose()
        df_samletvendtom = df_samletvendtom.reset_index()
        df_samletvendtom = df_samletvendtom.query("index != 'Unique'")
        df_samletvendtom = df_samletvendtom.query("index != 'Datasæt'")
        df_samletvendtom = pd.DataFrame(df_samletvendtom,index=None)
        df_samletvendtom = df_samletvendtom.rename(columns={'index':'index'}).set_index('index')
        df_samletvendtom = df_samletvendtom.rename(columns={0:'Hele sæsonen'})
        df_samletvendtom = df_samletvendtom.rename(columns={1:'Seneste 5 kampe'})

        
        categories = df_samletvendtom.index
        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r= df_samletvendtom['Hele sæsonen'],
            theta=categories,
            fill='toself',
            name='Hele sæsonen'
        ))
        fig.add_trace(go.Scatterpolar(
            r= df_samletvendtom['Seneste 5 kampe'],
            theta=categories,
            fill='toself',
            name='Seneste 5 kampe',
        ))

        fig.update_layout(
            polar=dict(
            radialaxis=dict(
            visible=True,
            range=[0, 5],
            )),
        showlegend=True,
        )
        fig.update_layout(polar=dict(bgcolor = '#1e2130'))
        st.title(option2+' fodbold')
        st.write('Rating efter talent-id på position, skalaen er 1-5, 5 er hvis spilleren er blandt de 20% bedste i ligaen på den pågældende stat')
        st.plotly_chart(fig,use_container_width=True)
        st.dataframe(df_samletvendtom,use_container_width=True)

    def U17():
        import pandas as pd
        import openpyxl
        import numpy as np
        import matplotlib.pyplot as plt
        import plotly.express as px 
        import time
        import plotly.graph_objects as go
        U19navne = pd.read_excel('Navne.xlsx')
        dfU19 = pd.read_excel('U17 spillere sæson.xlsx')
        dfU19 = dfU19[dfU19['Minutes played'] >= 300]
        dfU19['Position'] = dfU19['Position'].astype(str)
        dfU19['Team'] = dfU19['Team'].astype(str)
        
        #Dele spillerne i ligaen ud på positioner
        df_backsU19 = dfU19[dfU19['Position'].str.contains('|'.join(['LB', 'RB']))]
        df_StoppereU19 = dfU19[dfU19['Position'].str.contains('|'.join(['CB']))]
        df_Centrale_midtU19 = dfU19[dfU19['Position'].str.contains('|'.join(['CM','AMF','DMF']))]
        df_KanterU19 = dfU19[dfU19['Position'].str.contains('|'.join(['RW','LW','RAMF','LAMF']))]
        df_AngribereU19 = dfU19[dfU19['Position'].str.contains('|'.join(['CF']))]
        
        #Rangere stoppere i ligaen og give dem 1-5 i rating på forskellige parametre
        df_StoppereU19['Def duels won score'] = pd.qcut(df_StoppereU19['Defensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate passes, % score'] = pd.qcut(df_StoppereU19['Accurate passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate long passes, % score'] = pd.qcut(df_StoppereU19['Accurate long passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Forward passes per 90 score'] = pd.qcut(df_StoppereU19['Forward passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate forward passes score'] = pd.qcut(df_StoppereU19['Accurate forward passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate short/medium passes, % score'] = pd.qcut(df_StoppereU19['Accurate short / medium passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Interceptions per 90 score'] = pd.qcut(df_StoppereU19['Interceptions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['PAdj Interceptions score'] = pd.qcut(df_StoppereU19['PAdj Interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Successful defensive actions per 90 score'] = pd.qcut(df_StoppereU19['Successful defensive actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Shots blocked per 90 score'] = pd.qcut(df_StoppereU19['Shots blocked per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate forward passes, %'] = pd.qcut(df_StoppereU19['Accurate forward passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate passes to finale third, % score'] = pd.qcut(df_StoppereU19['Accurate passes to final third, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate progressive passes, % score'] = pd.qcut(df_StoppereU19['Accurate progressive passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Deep completions per 90 score'] = pd.qcut(df_StoppereU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Offensive duels won, % score'] = pd.qcut(df_StoppereU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Progressive runs per 90 score'] = pd.qcut(df_StoppereU19['Progressive runs per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Successful dribbles, % score'] = pd.qcut(df_StoppereU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Aerial duels won, % score'] = pd.qcut(df_StoppereU19['Aerial duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate through passes, % score'] = pd.qcut(df_StoppereU19['Accurate through passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19 = df_StoppereU19[df_StoppereU19['Team'].str.contains('Horsens')]
        df_StoppereU19 = U19navne.merge(df_StoppereU19)
        
        #Oprette forskellige parametre ud fra talent-id for stoppere
        df_StoppereU19['Pasningssikker Stopper'] = (df_StoppereU19['Accurate passes, % score'] + df_StoppereU19['Accurate long passes, % score'] + df_StoppereU19['Forward passes per 90 score'] + df_StoppereU19['Accurate forward passes score'] + df_StoppereU19['Accurate forward passes score'] + df_StoppereU19['Accurate short/medium passes, % score'] + df_StoppereU19['Forward passes per 90 score'] + df_StoppereU19['Accurate forward passes score'])/8
        df_StoppereU19['Spilintelligens defensivt Stopper'] = (df_StoppereU19['Interceptions per 90 score'] + df_StoppereU19['Successful defensive actions per 90 score']+df_StoppereU19['Shots blocked per 90 score'] + df_StoppereU19['PAdj Interceptions score'] + df_StoppereU19['PAdj Interceptions score'] + df_StoppereU19['Interceptions per 90 score'])/6
        df_StoppereU19['Spilintelligens offensivt Stopper'] = (df_StoppereU19['Accurate forward passes score'] + df_StoppereU19['Accurate passes to finale third, % score'] + df_StoppereU19['Accurate progressive passes, % score'] + df_StoppereU19['Accurate through passes, % score'] + df_StoppereU19['Deep completions per 90 score'] + df_StoppereU19['Offensive duels won, % score'] + df_StoppereU19['Progressive runs per 90 score'] + df_StoppereU19['Successful dribbles, % score'] + df_StoppereU19['Accurate forward passes score'])/9
        df_StoppereU19['Nærkamps- og duelstærk Stopper'] = (df_StoppereU19['Def duels won score'] + df_StoppereU19['Aerial duels won, % score'] + df_StoppereU19['Def duels won score'] + df_StoppereU19['Def duels won score'])/4
        df_StoppereU19 = df_StoppereU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Pasningssikker Stopper','Spilintelligens defensivt Stopper','Spilintelligens offensivt Stopper','Nærkamps- og duelstærk Stopper']]
        
        #Samme proces med backs
        df_backsU19['Accurate crosses, % score'] = pd.qcut(df_backsU19['Accurate crosses, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['xA per 90 score'] = pd.qcut(df_backsU19['xA per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Deep completions per 90 score'] = pd.qcut(df_backsU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Deep completed crosses per 90 score'] = pd.qcut(df_backsU19['Deep completed crosses per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Successful dribbles, % score'] = pd.qcut(df_backsU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Defensive duels won, % score'] = pd.qcut(df_backsU19['Defensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Progressive runs per 90 score'] = pd.qcut(df_backsU19['Progressive runs per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Offensive duels won, % score'] = pd.qcut(df_backsU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Accelerations per 90 score'] = pd.qcut(df_backsU19['Accelerations per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Duels won, % score'] = pd.qcut(df_backsU19['Duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Interceptions per 90 score'] = pd.qcut(df_backsU19['Interceptions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Successful defensive actions per 90 score'] = pd.qcut(df_backsU19['Successful defensive actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19 = df_backsU19[df_backsU19['Team'].str.contains('Horsens')]
        df_backsU19 = U19navne.merge(df_backsU19)
        
        df_backsU19['Indlægsstærk Back'] = (df_backsU19['Accurate crosses, % score'] + df_backsU19['xA per 90 score'] + df_backsU19['Deep completed crosses per 90 score'] + df_backsU19['Deep completed crosses per 90 score'])/4
        df_backsU19['1v1 færdigheder Back'] = (df_backsU19['Successful dribbles, % score'] + df_backsU19['Defensive duels won, % score'] + df_backsU19['Progressive runs per 90 score'] + df_backsU19['Offensive duels won, % score'] + df_backsU19['Accelerations per 90 score'] + df_backsU19['Duels won, % score'])/6
        df_backsU19['Spilintelligens defensivt Back'] = (df_backsU19['Interceptions per 90 score'] + df_backsU19['Successful defensive actions per 90 score'] + df_backsU19['Duels won, % score'] + df_backsU19['Defensive duels won, % score'])/4
        df_backsU19 = df_backsU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Indlægsstærk Back','1v1 færdigheder Back','Spilintelligens defensivt Back']]
        
        #Samme proces med centrale midt
        df_Centrale_midtU19['Accurate passes, % score'] = pd.qcut(df_Centrale_midtU19['Accurate passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Accurate forward passes, % score'] = pd.qcut(df_Centrale_midtU19['Accurate forward passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Accurate long passes, % score'] = pd.qcut(df_Centrale_midtU19['Accurate long passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Key passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Key passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Smart passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Smart passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Deep completions per 90 score'] = pd.qcut(df_Centrale_midtU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Through passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Through passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Progressive passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Progressive passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Offensive duels won, % score'] = pd.qcut(df_Centrale_midtU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Received passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Received passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Successful dribbles, % score'] = pd.qcut(df_Centrale_midtU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Successful defensive actions per 90 score'] = pd.qcut(df_Centrale_midtU19['Successful defensive actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Interceptions per 90 score'] = pd.qcut(df_Centrale_midtU19['Interceptions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Duels won, % score'] = pd.qcut(df_Centrale_midtU19['Duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Defensive duels won, % score'] = pd.qcut(df_Centrale_midtU19['Defensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['PAdj Interceptions score'] = pd.qcut(df_Centrale_midtU19['PAdj Interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19 = df_Centrale_midtU19[df_Centrale_midtU19['Team'].str.contains('Horsens')]
        df_Centrale_midtU19 = U19navne.merge(df_Centrale_midtU19)
        df_Centrale_midtU19['Pasningssikker/spilvendinger Central midt'] = (df_Centrale_midtU19['Accurate passes, % score'] + df_Centrale_midtU19['Accurate forward passes, % score'] + df_Centrale_midtU19['Accurate long passes, % score'] + df_Centrale_midtU19['Accurate passes, % score'] + df_Centrale_midtU19['Key passes per 90 score'] + df_Centrale_midtU19['Accurate forward passes, % score'] + df_Centrale_midtU19['Smart passes per 90 score'] + df_Centrale_midtU19['Deep completions per 90 score'] + df_Centrale_midtU19['Through passes per 90 score'] + df_Centrale_midtU19['Progressive passes per 90 score'])/10
        df_Centrale_midtU19['Boldfast Central midt'] = (df_Centrale_midtU19['Offensive duels won, % score'] + df_Centrale_midtU19['Received passes per 90 score'] + df_Centrale_midtU19['Accurate passes, % score'] + df_Centrale_midtU19['Successful dribbles, % score'] + df_Centrale_midtU19['Accurate passes, % score'])/5
        df_Centrale_midtU19['Spilintelligens defensivt Central midt'] = (df_Centrale_midtU19['Interceptions per 90 score'] + df_Centrale_midtU19['Successful defensive actions per 90 score'] + df_Centrale_midtU19['Duels won, % score'] + df_Centrale_midtU19['Defensive duels won, % score'] + df_Centrale_midtU19['PAdj Interceptions score'] + df_Centrale_midtU19['PAdj Interceptions score'])/6
        df_Centrale_midtU19 = df_Centrale_midtU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Pasningssikker/spilvendinger Central midt','Boldfast Central midt', 'Spilintelligens defensivt Central midt']]
        
        df_KanterU19['xG per 90 score'] = pd.qcut(df_KanterU19['xG per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Goals per 90 score'] = pd.qcut(df_KanterU19['Goals per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Shots on target, % score'] = pd.qcut(df_KanterU19['Shots on target, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Successful dribbles, % score'] = pd.qcut(df_KanterU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate passes, % score'] = pd.qcut(df_KanterU19['Accurate passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate forward passes, % score'] = pd.qcut(df_KanterU19['Accurate forward passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Deep completions per 90 score'] = pd.qcut(df_KanterU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate through passes, % score'] = pd.qcut(df_KanterU19['Accurate through passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate progressive passes, % score'] = pd.qcut(df_KanterU19['Accurate progressive passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Successful attacking actions per 90 score'] = pd.qcut(df_KanterU19['Successful attacking actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate passes to final third, % score'] = pd.qcut(df_KanterU19['Accurate passes to final third, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Offensive duels won, % score'] = pd.qcut(df_KanterU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['xA per 90 score'] = pd.qcut(df_KanterU19['xA per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate smart passes, % score'] = pd.qcut(df_KanterU19['Accurate smart passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate crosses, % score'] = pd.qcut(df_KanterU19['Accurate crosses, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Successful attacking actions per 90 score'] = pd.qcut(df_KanterU19['Successful attacking actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Smart passes per 90 score'] = pd.qcut(df_KanterU19['Smart passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Key passes per 90 score'] = pd.qcut(df_KanterU19['Key passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19 = df_KanterU19[df_KanterU19['Team'].str.contains('Horsens')]
        df_KanterU19 = U19navne.merge(df_KanterU19)
        
        df_KanterU19['Sparkefærdigheder Kant'] = (df_KanterU19['xG per 90 score'] + df_KanterU19['Goals per 90 score'] + df_KanterU19['Shots on target, % score'])/3
        df_KanterU19['1v1 Offensivt Kant'] = (df_KanterU19['Successful dribbles, % score'] + df_KanterU19['Successful dribbles, % score'] + df_KanterU19['Offensive duels won, % score'])/3
        df_KanterU19['Kombinationsstærk Kant'] = (df_KanterU19['Accurate passes, % score'] + df_KanterU19['Accurate forward passes, % score'] + df_KanterU19['Deep completions per 90 score'] + df_KanterU19['Accurate through passes, % score'] + df_KanterU19['Accurate progressive passes, % score'] + df_KanterU19['Successful attacking actions per 90 score'] + df_KanterU19['Accurate passes to final third, % score'])/7
        df_KanterU19['Spilintelligens offensivt/indlægsstærk Kant'] = (df_KanterU19['xA per 90 score'] + df_KanterU19['xG per 90 score'] + df_KanterU19['xA per 90 score'] + df_KanterU19['xG per 90 score'] + df_KanterU19['Accurate through passes, % score'] + df_KanterU19['Accurate smart passes, % score'] + df_KanterU19['Accurate forward passes, % score'] + df_KanterU19['Accurate progressive passes, % score'] + df_KanterU19['Accurate passes to final third, % score'] + df_KanterU19['Accurate crosses, % score'] + df_KanterU19['Successful attacking actions per 90 score'] + df_KanterU19['Smart passes per 90 score'] + df_KanterU19['Key passes per 90 score'])/13
        df_KanterU19 = df_KanterU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Sparkefærdigheder Kant','1v1 Offensivt Kant','Kombinationsstærk Kant','Spilintelligens offensivt/indlægsstærk Kant']]

        df_AngribereU19['xG per 90 score'] = pd.qcut(df_AngribereU19['xG per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Goals per 90 score'] = pd.qcut(df_AngribereU19['Goals per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)  
        df_AngribereU19['Shots on target, % score'] = pd.qcut(df_AngribereU19['Shots on target, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)   
        df_AngribereU19['Offensive duels won, % score'] = pd.qcut(df_AngribereU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Duels won, % score'] = pd.qcut(df_AngribereU19['Duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Accurate passes, % score'] = pd.qcut(df_AngribereU19['Accurate passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Successful dribbles, % score'] = pd.qcut(df_AngribereU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['xA per 90 score'] = pd.qcut(df_AngribereU19['xA per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Touches in box per 90 score'] = pd.qcut(df_AngribereU19['Touches in box per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Deep completions per 90 score'] = pd.qcut(df_AngribereU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Successful attacking actions per 90 score'] = pd.qcut(df_AngribereU19['Successful attacking actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    
        df_AngribereU19 = df_AngribereU19[df_AngribereU19['Team'].str.contains('Horsens')]
        df_AngribereU19 = U19navne.merge(df_AngribereU19)
        
        df_AngribereU19['Sparkefærdigheder Angriber'] = (df_AngribereU19['xG per 90 score'] + df_AngribereU19['xG per 90 score'] + df_AngribereU19['Goals per 90 score'] + df_AngribereU19['Shots on target, % score'])/4
        df_AngribereU19['Boldfast Angriber'] = (df_AngribereU19['Offensive duels won, % score'] + df_AngribereU19['Offensive duels won, % score'] + df_AngribereU19['Duels won, % score'] + df_AngribereU19['Accurate passes, % score'] + df_AngribereU19['Successful dribbles, % score'])/5
        df_AngribereU19['Spilintelligens offensivt Angriber'] = (df_AngribereU19['xA per 90 score'] + df_AngribereU19['xG per 90 score'] + df_AngribereU19['Touches in box per 90 score'] + df_AngribereU19['Deep completions per 90 score'] + df_AngribereU19['Successful attacking actions per 90 score'] + df_AngribereU19['Touches in box per 90 score'] + df_AngribereU19['xG per 90 score'])/7
        
        df_AngribereU19 = df_AngribereU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Sparkefærdigheder Angriber','Boldfast Angriber','Spilintelligens offensivt Angriber']]
        
        
        df_samlet = df_StoppereU19.append(df_backsU19).append(df_Centrale_midtU19).append(df_KanterU19).append(df_AngribereU19)
        dfspillere = df_samlet['Spillere'].drop_duplicates(keep='last')
        dfspillere = dfspillere.astype(str)
        dfspillere = sorted(dfspillere)
        option2 = st.selectbox('Vælg spiller',dfspillere)
        df_samlet = df_samlet[df_samlet['Spillere'].str.contains(option2)]
        df_samlet = df_samlet.groupby(['Spillere']).mean(numeric_only=True)

        #Start på seneste 5 kampe
        dfU19s5 = pd.read_excel('U17 spillere seneste 5.xlsx')
        dfU19s5 = dfU19s5[dfU19s5['Minutes played'] >= 200]
        dfU19s5['Position'] = dfU19s5['Position'].astype(str)
        dfU19s5['Team'] = dfU19s5['Team'].astype(str)
        
        #Dele spillerne i ligaen ud på positioner
        df_backsU19 = dfU19s5[dfU19s5['Position'].str.contains('|'.join(['LB', 'RB']))]
        df_StoppereU19 = dfU19s5[dfU19s5['Position'].str.contains('|'.join(['CB']))]
        df_Centrale_midtU19 = dfU19s5[dfU19s5['Position'].str.contains('|'.join(['CM','AMF','DMF']))]
        df_KanterU19 = dfU19s5[dfU19s5['Position'].str.contains('|'.join(['RW','LW','RAMF','LAMF']))]
        df_AngribereU19 = dfU19s5[dfU19s5['Position'].str.contains('|'.join(['CF']))]
        
        #Rangere stoppere i ligaen og give dem 1-5 i rating på forskellige parametre
        df_StoppereU19['Def duels won score'] = pd.qcut(df_StoppereU19['Defensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate passes, % score'] = pd.qcut(df_StoppereU19['Accurate passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate long passes, % score'] = pd.qcut(df_StoppereU19['Accurate long passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Forward passes per 90 score'] = pd.qcut(df_StoppereU19['Forward passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate forward passes score'] = pd.qcut(df_StoppereU19['Accurate forward passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate short/medium passes, % score'] = pd.qcut(df_StoppereU19['Accurate short / medium passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Interceptions per 90 score'] = pd.qcut(df_StoppereU19['Interceptions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['PAdj Interceptions score'] = pd.qcut(df_StoppereU19['PAdj Interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Successful defensive actions per 90 score'] = pd.qcut(df_StoppereU19['Successful defensive actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Shots blocked per 90 score'] = pd.qcut(df_StoppereU19['Shots blocked per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate forward passes, %'] = pd.qcut(df_StoppereU19['Accurate forward passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate passes to finale third, % score'] = pd.qcut(df_StoppereU19['Accurate passes to final third, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate progressive passes, % score'] = pd.qcut(df_StoppereU19['Accurate progressive passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Deep completions per 90 score'] = pd.qcut(df_StoppereU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Offensive duels won, % score'] = pd.qcut(df_StoppereU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Progressive runs per 90 score'] = pd.qcut(df_StoppereU19['Progressive runs per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Successful dribbles, % score'] = pd.qcut(df_StoppereU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Aerial duels won, % score'] = pd.qcut(df_StoppereU19['Aerial duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate through passes, % score'] = pd.qcut(df_StoppereU19['Accurate through passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19 = df_StoppereU19[df_StoppereU19['Team'].str.contains('Horsens')]
        df_StoppereU19 = U19navne.merge(df_StoppereU19)
        
        #Oprette forskellige parametre ud fra talent-id for stoppere
        df_StoppereU19['Pasningssikker Stopper'] = (df_StoppereU19['Accurate passes, % score'] + df_StoppereU19['Accurate long passes, % score'] + df_StoppereU19['Forward passes per 90 score'] + df_StoppereU19['Accurate forward passes score'] + df_StoppereU19['Accurate forward passes score'] + df_StoppereU19['Accurate short/medium passes, % score'] + df_StoppereU19['Forward passes per 90 score'] + df_StoppereU19['Accurate forward passes score'])/8
        df_StoppereU19['Spilintelligens defensivt Stopper'] = (df_StoppereU19['Interceptions per 90 score'] + df_StoppereU19['Successful defensive actions per 90 score']+df_StoppereU19['Shots blocked per 90 score'] + df_StoppereU19['PAdj Interceptions score'] + df_StoppereU19['PAdj Interceptions score'] + df_StoppereU19['Interceptions per 90 score'])/6
        df_StoppereU19['Spilintelligens offensivt Stopper'] = (df_StoppereU19['Accurate forward passes score'] + df_StoppereU19['Accurate passes to finale third, % score'] + df_StoppereU19['Accurate progressive passes, % score'] + df_StoppereU19['Accurate through passes, % score'] + df_StoppereU19['Deep completions per 90 score'] + df_StoppereU19['Offensive duels won, % score'] + df_StoppereU19['Progressive runs per 90 score'] + df_StoppereU19['Successful dribbles, % score'] + df_StoppereU19['Accurate forward passes score'])/9
        df_StoppereU19['Nærkamps- og duelstærk Stopper'] = (df_StoppereU19['Def duels won score'] + df_StoppereU19['Aerial duels won, % score'] + df_StoppereU19['Def duels won score'] + df_StoppereU19['Def duels won score'])/4
        df_StoppereU19 = df_StoppereU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Pasningssikker Stopper','Spilintelligens defensivt Stopper','Spilintelligens offensivt Stopper','Nærkamps- og duelstærk Stopper']]
        
        #Samme proces med backs
        df_backsU19['Accurate crosses, % score'] = pd.qcut(df_backsU19['Accurate crosses, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['xA per 90 score'] = pd.qcut(df_backsU19['xA per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Deep completions per 90 score'] = pd.qcut(df_backsU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Deep completed crosses per 90 score'] = pd.qcut(df_backsU19['Deep completed crosses per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Successful dribbles, % score'] = pd.qcut(df_backsU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Defensive duels won, % score'] = pd.qcut(df_backsU19['Defensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Progressive runs per 90 score'] = pd.qcut(df_backsU19['Progressive runs per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Offensive duels won, % score'] = pd.qcut(df_backsU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Accelerations per 90 score'] = pd.qcut(df_backsU19['Accelerations per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Duels won, % score'] = pd.qcut(df_backsU19['Duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Interceptions per 90 score'] = pd.qcut(df_backsU19['Interceptions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Successful defensive actions per 90 score'] = pd.qcut(df_backsU19['Successful defensive actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19 = df_backsU19[df_backsU19['Team'].str.contains('Horsens')]
        df_backsU19 = U19navne.merge(df_backsU19)
        
        df_backsU19['Indlægsstærk Back'] = (df_backsU19['Accurate crosses, % score'] + df_backsU19['xA per 90 score'] + df_backsU19['Deep completed crosses per 90 score'] + df_backsU19['Deep completed crosses per 90 score'])/4
        df_backsU19['1v1 færdigheder Back'] = (df_backsU19['Successful dribbles, % score'] + df_backsU19['Defensive duels won, % score'] + df_backsU19['Progressive runs per 90 score'] + df_backsU19['Offensive duels won, % score'] + df_backsU19['Accelerations per 90 score'] + df_backsU19['Duels won, % score'])/6
        df_backsU19['Spilintelligens defensivt Back'] = (df_backsU19['Interceptions per 90 score'] + df_backsU19['Successful defensive actions per 90 score'] + df_backsU19['Duels won, % score'] + df_backsU19['Defensive duels won, % score'])/4
        df_backsU19 = df_backsU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Indlægsstærk Back','1v1 færdigheder Back','Spilintelligens defensivt Back']]
        
        #Samme proces med centrale midt
        df_Centrale_midtU19['Accurate passes, % score'] = pd.qcut(df_Centrale_midtU19['Accurate passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Accurate forward passes, % score'] = pd.qcut(df_Centrale_midtU19['Accurate forward passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Accurate long passes, % score'] = pd.qcut(df_Centrale_midtU19['Accurate long passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Key passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Key passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Smart passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Smart passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Deep completions per 90 score'] = pd.qcut(df_Centrale_midtU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Through passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Through passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Progressive passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Progressive passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Offensive duels won, % score'] = pd.qcut(df_Centrale_midtU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Received passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Received passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Successful dribbles, % score'] = pd.qcut(df_Centrale_midtU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Successful defensive actions per 90 score'] = pd.qcut(df_Centrale_midtU19['Successful defensive actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Interceptions per 90 score'] = pd.qcut(df_Centrale_midtU19['Interceptions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Duels won, % score'] = pd.qcut(df_Centrale_midtU19['Duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Defensive duels won, % score'] = pd.qcut(df_Centrale_midtU19['Defensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['PAdj Interceptions score'] = pd.qcut(df_Centrale_midtU19['PAdj Interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19 = df_Centrale_midtU19[df_Centrale_midtU19['Team'].str.contains('Horsens')]
        df_Centrale_midtU19 = U19navne.merge(df_Centrale_midtU19)
        df_Centrale_midtU19['Pasningssikker/spilvendinger Central midt'] = (df_Centrale_midtU19['Accurate passes, % score'] + df_Centrale_midtU19['Accurate forward passes, % score'] + df_Centrale_midtU19['Accurate long passes, % score'] + df_Centrale_midtU19['Accurate passes, % score'] + df_Centrale_midtU19['Key passes per 90 score'] + df_Centrale_midtU19['Accurate forward passes, % score'] + df_Centrale_midtU19['Smart passes per 90 score'] + df_Centrale_midtU19['Deep completions per 90 score'] + df_Centrale_midtU19['Through passes per 90 score'] + df_Centrale_midtU19['Progressive passes per 90 score'])/10
        df_Centrale_midtU19['Boldfast Central midt'] = (df_Centrale_midtU19['Offensive duels won, % score'] + df_Centrale_midtU19['Received passes per 90 score'] + df_Centrale_midtU19['Accurate passes, % score'] + df_Centrale_midtU19['Successful dribbles, % score'] + df_Centrale_midtU19['Accurate passes, % score'])/5
        df_Centrale_midtU19['Spilintelligens defensivt Central midt'] = (df_Centrale_midtU19['Interceptions per 90 score'] + df_Centrale_midtU19['Successful defensive actions per 90 score'] + df_Centrale_midtU19['Duels won, % score'] + df_Centrale_midtU19['Defensive duels won, % score'] + df_Centrale_midtU19['PAdj Interceptions score'] + df_Centrale_midtU19['PAdj Interceptions score'])/6
        df_Centrale_midtU19 = df_Centrale_midtU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Pasningssikker/spilvendinger Central midt','Boldfast Central midt', 'Spilintelligens defensivt Central midt']]
        
        df_KanterU19['xG per 90 score'] = pd.qcut(df_KanterU19['xG per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Goals per 90 score'] = pd.qcut(df_KanterU19['Goals per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Shots on target, % score'] = pd.qcut(df_KanterU19['Shots on target, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Successful dribbles, % score'] = pd.qcut(df_KanterU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate passes, % score'] = pd.qcut(df_KanterU19['Accurate passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate forward passes, % score'] = pd.qcut(df_KanterU19['Accurate forward passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Deep completions per 90 score'] = pd.qcut(df_KanterU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate through passes, % score'] = pd.qcut(df_KanterU19['Accurate through passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate progressive passes, % score'] = pd.qcut(df_KanterU19['Accurate progressive passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Successful attacking actions per 90 score'] = pd.qcut(df_KanterU19['Successful attacking actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate passes to final third, % score'] = pd.qcut(df_KanterU19['Accurate passes to final third, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Offensive duels won, % score'] = pd.qcut(df_KanterU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['xA per 90 score'] = pd.qcut(df_KanterU19['xA per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate smart passes, % score'] = pd.qcut(df_KanterU19['Accurate smart passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate crosses, % score'] = pd.qcut(df_KanterU19['Accurate crosses, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Successful attacking actions per 90 score'] = pd.qcut(df_KanterU19['Successful attacking actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Smart passes per 90 score'] = pd.qcut(df_KanterU19['Smart passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Key passes per 90 score'] = pd.qcut(df_KanterU19['Key passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19 = df_KanterU19[df_KanterU19['Team'].str.contains('Horsens')]
        df_KanterU19 = U19navne.merge(df_KanterU19)
        
        df_KanterU19['Sparkefærdigheder Kant'] = (df_KanterU19['xG per 90 score'] + df_KanterU19['Goals per 90 score'] + df_KanterU19['Shots on target, % score'])/3
        df_KanterU19['1v1 Offensivt Kant'] = (df_KanterU19['Successful dribbles, % score'] + df_KanterU19['Successful dribbles, % score'] + df_KanterU19['Offensive duels won, % score'])/3
        df_KanterU19['Kombinationsstærk Kant'] = (df_KanterU19['Accurate passes, % score'] + df_KanterU19['Accurate forward passes, % score'] + df_KanterU19['Deep completions per 90 score'] + df_KanterU19['Accurate through passes, % score'] + df_KanterU19['Accurate progressive passes, % score'] + df_KanterU19['Successful attacking actions per 90 score'] + df_KanterU19['Accurate passes to final third, % score'])/7
        df_KanterU19['Spilintelligens offensivt/indlægsstærk Kant'] = (df_KanterU19['xA per 90 score'] + df_KanterU19['xG per 90 score'] + df_KanterU19['xA per 90 score'] + df_KanterU19['xG per 90 score'] + df_KanterU19['Accurate through passes, % score'] + df_KanterU19['Accurate smart passes, % score'] + df_KanterU19['Accurate forward passes, % score'] + df_KanterU19['Accurate progressive passes, % score'] + df_KanterU19['Accurate passes to final third, % score'] + df_KanterU19['Accurate crosses, % score'] + df_KanterU19['Successful attacking actions per 90 score'] + df_KanterU19['Smart passes per 90 score'] + df_KanterU19['Key passes per 90 score'])/13
        df_KanterU19 = df_KanterU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Sparkefærdigheder Kant','1v1 Offensivt Kant','Kombinationsstærk Kant','Spilintelligens offensivt/indlægsstærk Kant']]

        df_AngribereU19['xG per 90 score'] = pd.qcut(df_AngribereU19['xG per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Goals per 90 score'] = pd.qcut(df_AngribereU19['Goals per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)  
        df_AngribereU19['Shots on target, % score'] = pd.qcut(df_AngribereU19['Shots on target, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)   
        df_AngribereU19['Offensive duels won, % score'] = pd.qcut(df_AngribereU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Duels won, % score'] = pd.qcut(df_AngribereU19['Duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Accurate passes, % score'] = pd.qcut(df_AngribereU19['Accurate passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Successful dribbles, % score'] = pd.qcut(df_AngribereU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['xA per 90 score'] = pd.qcut(df_AngribereU19['xA per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Touches in box per 90 score'] = pd.qcut(df_AngribereU19['Touches in box per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Deep completions per 90 score'] = pd.qcut(df_AngribereU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Successful attacking actions per 90 score'] = pd.qcut(df_AngribereU19['Successful attacking actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    
        df_AngribereU19 = df_AngribereU19[df_AngribereU19['Team'].str.contains('Horsens')]
        df_AngribereU19 = U19navne.merge(df_AngribereU19)
        
        df_AngribereU19['Sparkefærdigheder Angriber'] = (df_AngribereU19['xG per 90 score'] + df_AngribereU19['xG per 90 score'] + df_AngribereU19['Goals per 90 score'] + df_AngribereU19['Shots on target, % score'])/4
        df_AngribereU19['Boldfast Angriber'] = (df_AngribereU19['Offensive duels won, % score'] + df_AngribereU19['Offensive duels won, % score'] + df_AngribereU19['Duels won, % score'] + df_AngribereU19['Accurate passes, % score'] + df_AngribereU19['Successful dribbles, % score'])/5
        df_AngribereU19['Spilintelligens offensivt Angriber'] = (df_AngribereU19['xA per 90 score'] + df_AngribereU19['xG per 90 score'] + df_AngribereU19['Touches in box per 90 score'] + df_AngribereU19['Deep completions per 90 score'] + df_AngribereU19['Successful attacking actions per 90 score'] + df_AngribereU19['Touches in box per 90 score'] + df_AngribereU19['xG per 90 score'])/7
        
        df_AngribereU19 = df_AngribereU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Sparkefærdigheder Angriber','Boldfast Angriber','Spilintelligens offensivt Angriber']]
        
        
        df_samlets5 = df_StoppereU19.append(df_backsU19).append(df_Centrale_midtU19).append(df_KanterU19).append(df_AngribereU19)
        df_samlets5 = df_samlets5[df_samlets5['Spillere'].str.contains(option2)]
        df_samlets5 = df_samlets5.groupby(['Spillere']).mean(numeric_only=True)


        df_samlet = df_samlet.append(df_samlets5)

        option3 = st.selectbox('Vælg position',('Stopper','Back','Central midt','Kant','Angriber'))

        df_samlet = df_samlet.filter(regex=option3)
        df_samlet['Datasæt'] = 'Seneste 5 kampe'
        df_samlet['Datasæt'][0] = 'Hele sæsonen'
        df_samlet = df_samlet.rename(columns = lambda x: x.replace(option3, ''))
        df_samletvendtom = df_samlet.reset_index()
        df_samletvendtom['Unique'] = df_samletvendtom['Spillere'] + df_samletvendtom['Datasæt']
        df_samletvendtom = pd.DataFrame.drop(df_samletvendtom,axis=1,columns='Spillere')
        df_samletvendtom = df_samletvendtom.transpose()
        df_samletvendtom = df_samletvendtom.reset_index()
        df_samletvendtom = df_samletvendtom.query("index != 'Unique'")
        df_samletvendtom = df_samletvendtom.query("index != 'Datasæt'")
        df_samletvendtom = pd.DataFrame(df_samletvendtom,index=None)
        df_samletvendtom = df_samletvendtom.rename(columns={'index':'index'}).set_index('index')
        df_samletvendtom = df_samletvendtom.rename(columns={0:'Hele sæsonen'})
        df_samletvendtom = df_samletvendtom.rename(columns={1:'Seneste 5 kampe'})

        
        categories = df_samletvendtom.index
        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r= df_samletvendtom['Hele sæsonen'],
            theta=categories,
            fill='toself',
            name='Hele sæsonen'
        ))
        fig.add_trace(go.Scatterpolar(
            r= df_samletvendtom['Seneste 5 kampe'],
            theta=categories,
            fill='toself',
            name='Seneste 5 kampe',
        ))

        fig.update_layout(
            polar=dict(
            radialaxis=dict(
            visible=True,
            range=[0, 5],
            )),
        showlegend=True,
        )
        fig.update_layout(polar=dict(bgcolor = '#1e2130'))
        st.title(option2+' fodbold')
        st.write('Rating efter talent-id på position, skalaen er 1-5, 5 er hvis spilleren er blandt de 20% bedste i ligaen på den pågældende stat')        
        st.plotly_chart(fig,use_container_width=True)
        st.dataframe(df_samletvendtom,use_container_width=True)
    
    def U15():
        import pandas as pd
        import openpyxl
        import numpy as np
        import matplotlib.pyplot as plt
        import plotly.express as px 
        import time
        import plotly.graph_objects as go
        U19navne = pd.read_excel('Navne.xlsx')
        dfU19 = pd.read_excel('U15 spillere sæson.xlsx')
        dfU19 = dfU19[dfU19['Minutes played'] >= 300]
        dfU19['Position'] = dfU19['Position'].astype(str)
        dfU19['Team'] = dfU19['Team'].astype(str)
        
        #Dele spillerne i ligaen ud på positioner
        df_backsU19 = dfU19[dfU19['Position'].str.contains('|'.join(['LB', 'RB']))]
        df_StoppereU19 = dfU19[dfU19['Position'].str.contains('|'.join(['CB']))]
        df_Centrale_midtU19 = dfU19[dfU19['Position'].str.contains('|'.join(['CM','AMF','DMF']))]
        df_KanterU19 = dfU19[dfU19['Position'].str.contains('|'.join(['RW','LW','RAMF','LAMF']))]
        df_AngribereU19 = dfU19[dfU19['Position'].str.contains('|'.join(['CF']))]
        
        #Rangere stoppere i ligaen og give dem 1-5 i rating på forskellige parametre
        df_StoppereU19['Def duels won score'] = pd.qcut(df_StoppereU19['Defensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate passes, % score'] = pd.qcut(df_StoppereU19['Accurate passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate long passes, % score'] = pd.qcut(df_StoppereU19['Accurate long passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Forward passes per 90 score'] = pd.qcut(df_StoppereU19['Forward passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate forward passes score'] = pd.qcut(df_StoppereU19['Accurate forward passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate short/medium passes, % score'] = pd.qcut(df_StoppereU19['Accurate short / medium passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Interceptions per 90 score'] = pd.qcut(df_StoppereU19['Interceptions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['PAdj Interceptions score'] = pd.qcut(df_StoppereU19['PAdj Interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Successful defensive actions per 90 score'] = pd.qcut(df_StoppereU19['Successful defensive actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Shots blocked per 90 score'] = pd.qcut(df_StoppereU19['Shots blocked per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate forward passes, %'] = pd.qcut(df_StoppereU19['Accurate forward passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate passes to finale third, % score'] = pd.qcut(df_StoppereU19['Accurate passes to final third, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate progressive passes, % score'] = pd.qcut(df_StoppereU19['Accurate progressive passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Deep completions per 90 score'] = pd.qcut(df_StoppereU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Offensive duels won, % score'] = pd.qcut(df_StoppereU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Progressive runs per 90 score'] = pd.qcut(df_StoppereU19['Progressive runs per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Successful dribbles, % score'] = pd.qcut(df_StoppereU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Aerial duels won, % score'] = pd.qcut(df_StoppereU19['Aerial duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate through passes, % score'] = pd.qcut(df_StoppereU19['Accurate through passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19 = df_StoppereU19[df_StoppereU19['Team'].str.contains('Horsens')]
        df_StoppereU19 = U19navne.merge(df_StoppereU19)
        
        #Oprette forskellige parametre ud fra talent-id for stoppere
        df_StoppereU19['Pasningssikker Stopper'] = (df_StoppereU19['Accurate passes, % score'] + df_StoppereU19['Accurate long passes, % score'] + df_StoppereU19['Forward passes per 90 score'] + df_StoppereU19['Accurate forward passes score'] + df_StoppereU19['Accurate forward passes score'] + df_StoppereU19['Accurate short/medium passes, % score'] + df_StoppereU19['Forward passes per 90 score'] + df_StoppereU19['Accurate forward passes score'])/8
        df_StoppereU19['Spilintelligens defensivt Stopper'] = (df_StoppereU19['Interceptions per 90 score'] + df_StoppereU19['Successful defensive actions per 90 score']+df_StoppereU19['Shots blocked per 90 score'] + df_StoppereU19['PAdj Interceptions score'] + df_StoppereU19['PAdj Interceptions score'] + df_StoppereU19['Interceptions per 90 score'])/6
        df_StoppereU19['Spilintelligens offensivt Stopper'] = (df_StoppereU19['Accurate forward passes score'] + df_StoppereU19['Accurate passes to finale third, % score'] + df_StoppereU19['Accurate progressive passes, % score'] + df_StoppereU19['Accurate through passes, % score'] + df_StoppereU19['Deep completions per 90 score'] + df_StoppereU19['Offensive duels won, % score'] + df_StoppereU19['Progressive runs per 90 score'] + df_StoppereU19['Successful dribbles, % score'] + df_StoppereU19['Accurate forward passes score'])/9
        df_StoppereU19['Nærkamps- og duelstærk Stopper'] = (df_StoppereU19['Def duels won score'] + df_StoppereU19['Aerial duels won, % score'] + df_StoppereU19['Def duels won score'] + df_StoppereU19['Def duels won score'])/4
        df_StoppereU19 = df_StoppereU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Pasningssikker Stopper','Spilintelligens defensivt Stopper','Spilintelligens offensivt Stopper','Nærkamps- og duelstærk Stopper']]
        
        #Samme proces med backs
        df_backsU19['Accurate crosses, % score'] = pd.qcut(df_backsU19['Accurate crosses, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['xA per 90 score'] = pd.qcut(df_backsU19['xA per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Deep completions per 90 score'] = pd.qcut(df_backsU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Deep completed crosses per 90 score'] = pd.qcut(df_backsU19['Deep completed crosses per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Successful dribbles, % score'] = pd.qcut(df_backsU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Defensive duels won, % score'] = pd.qcut(df_backsU19['Defensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Progressive runs per 90 score'] = pd.qcut(df_backsU19['Progressive runs per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Offensive duels won, % score'] = pd.qcut(df_backsU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Accelerations per 90 score'] = pd.qcut(df_backsU19['Accelerations per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Duels won, % score'] = pd.qcut(df_backsU19['Duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Interceptions per 90 score'] = pd.qcut(df_backsU19['Interceptions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Successful defensive actions per 90 score'] = pd.qcut(df_backsU19['Successful defensive actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19 = df_backsU19[df_backsU19['Team'].str.contains('Horsens')]
        df_backsU19 = U19navne.merge(df_backsU19)
        
        df_backsU19['Indlægsstærk Back'] = (df_backsU19['Accurate crosses, % score'] + df_backsU19['xA per 90 score'] + df_backsU19['Deep completed crosses per 90 score'] + df_backsU19['Deep completed crosses per 90 score'])/4
        df_backsU19['1v1 færdigheder Back'] = (df_backsU19['Successful dribbles, % score'] + df_backsU19['Defensive duels won, % score'] + df_backsU19['Progressive runs per 90 score'] + df_backsU19['Offensive duels won, % score'] + df_backsU19['Accelerations per 90 score'] + df_backsU19['Duels won, % score'])/6
        df_backsU19['Spilintelligens defensivt Back'] = (df_backsU19['Interceptions per 90 score'] + df_backsU19['Successful defensive actions per 90 score'] + df_backsU19['Duels won, % score'] + df_backsU19['Defensive duels won, % score'])/4
        df_backsU19 = df_backsU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Indlægsstærk Back','1v1 færdigheder Back','Spilintelligens defensivt Back']]
        
        #Samme proces med centrale midt
        df_Centrale_midtU19['Accurate passes, % score'] = pd.qcut(df_Centrale_midtU19['Accurate passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Accurate forward passes, % score'] = pd.qcut(df_Centrale_midtU19['Accurate forward passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Accurate long passes, % score'] = pd.qcut(df_Centrale_midtU19['Accurate long passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Key passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Key passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Smart passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Smart passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Deep completions per 90 score'] = pd.qcut(df_Centrale_midtU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Through passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Through passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Progressive passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Progressive passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Offensive duels won, % score'] = pd.qcut(df_Centrale_midtU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Received passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Received passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Successful dribbles, % score'] = pd.qcut(df_Centrale_midtU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Successful defensive actions per 90 score'] = pd.qcut(df_Centrale_midtU19['Successful defensive actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Interceptions per 90 score'] = pd.qcut(df_Centrale_midtU19['Interceptions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Duels won, % score'] = pd.qcut(df_Centrale_midtU19['Duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Defensive duels won, % score'] = pd.qcut(df_Centrale_midtU19['Defensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['PAdj Interceptions score'] = pd.qcut(df_Centrale_midtU19['PAdj Interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19 = df_Centrale_midtU19[df_Centrale_midtU19['Team'].str.contains('Horsens')]
        df_Centrale_midtU19 = U19navne.merge(df_Centrale_midtU19)
        df_Centrale_midtU19['Pasningssikker/spilvendinger Central midt'] = (df_Centrale_midtU19['Accurate passes, % score'] + df_Centrale_midtU19['Accurate forward passes, % score'] + df_Centrale_midtU19['Accurate long passes, % score'] + df_Centrale_midtU19['Accurate passes, % score'] + df_Centrale_midtU19['Key passes per 90 score'] + df_Centrale_midtU19['Accurate forward passes, % score'] + df_Centrale_midtU19['Smart passes per 90 score'] + df_Centrale_midtU19['Deep completions per 90 score'] + df_Centrale_midtU19['Through passes per 90 score'] + df_Centrale_midtU19['Progressive passes per 90 score'])/10
        df_Centrale_midtU19['Boldfast Central midt'] = (df_Centrale_midtU19['Offensive duels won, % score'] + df_Centrale_midtU19['Received passes per 90 score'] + df_Centrale_midtU19['Accurate passes, % score'] + df_Centrale_midtU19['Successful dribbles, % score'] + df_Centrale_midtU19['Accurate passes, % score'])/5
        df_Centrale_midtU19['Spilintelligens defensivt Central midt'] = (df_Centrale_midtU19['Interceptions per 90 score'] + df_Centrale_midtU19['Successful defensive actions per 90 score'] + df_Centrale_midtU19['Duels won, % score'] + df_Centrale_midtU19['Defensive duels won, % score'] + df_Centrale_midtU19['PAdj Interceptions score'] + df_Centrale_midtU19['PAdj Interceptions score'])/6
        df_Centrale_midtU19 = df_Centrale_midtU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Pasningssikker/spilvendinger Central midt','Boldfast Central midt', 'Spilintelligens defensivt Central midt']]
        
        df_KanterU19['xG per 90 score'] = pd.qcut(df_KanterU19['xG per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Goals per 90 score'] = pd.qcut(df_KanterU19['Goals per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Shots on target, % score'] = pd.qcut(df_KanterU19['Shots on target, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Successful dribbles, % score'] = pd.qcut(df_KanterU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate passes, % score'] = pd.qcut(df_KanterU19['Accurate passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate forward passes, % score'] = pd.qcut(df_KanterU19['Accurate forward passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Deep completions per 90 score'] = pd.qcut(df_KanterU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate through passes, % score'] = pd.qcut(df_KanterU19['Accurate through passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate progressive passes, % score'] = pd.qcut(df_KanterU19['Accurate progressive passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Successful attacking actions per 90 score'] = pd.qcut(df_KanterU19['Successful attacking actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate passes to final third, % score'] = pd.qcut(df_KanterU19['Accurate passes to final third, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Offensive duels won, % score'] = pd.qcut(df_KanterU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['xA per 90 score'] = pd.qcut(df_KanterU19['xA per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate smart passes, % score'] = pd.qcut(df_KanterU19['Accurate smart passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate crosses, % score'] = pd.qcut(df_KanterU19['Accurate crosses, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Successful attacking actions per 90 score'] = pd.qcut(df_KanterU19['Successful attacking actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Smart passes per 90 score'] = pd.qcut(df_KanterU19['Smart passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Key passes per 90 score'] = pd.qcut(df_KanterU19['Key passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19 = df_KanterU19[df_KanterU19['Team'].str.contains('Horsens')]
        df_KanterU19 = U19navne.merge(df_KanterU19)
        
        df_KanterU19['Sparkefærdigheder Kant'] = (df_KanterU19['xG per 90 score'] + df_KanterU19['Goals per 90 score'] + df_KanterU19['Shots on target, % score'])/3
        df_KanterU19['1v1 Offensivt Kant'] = (df_KanterU19['Successful dribbles, % score'] + df_KanterU19['Successful dribbles, % score'] + df_KanterU19['Offensive duels won, % score'])/3
        df_KanterU19['Kombinationsstærk Kant'] = (df_KanterU19['Accurate passes, % score'] + df_KanterU19['Accurate forward passes, % score'] + df_KanterU19['Deep completions per 90 score'] + df_KanterU19['Accurate through passes, % score'] + df_KanterU19['Accurate progressive passes, % score'] + df_KanterU19['Successful attacking actions per 90 score'] + df_KanterU19['Accurate passes to final third, % score'])/7
        df_KanterU19['Spilintelligens offensivt/indlægsstærk Kant'] = (df_KanterU19['xA per 90 score'] + df_KanterU19['xG per 90 score'] + df_KanterU19['xA per 90 score'] + df_KanterU19['xG per 90 score'] + df_KanterU19['Accurate through passes, % score'] + df_KanterU19['Accurate smart passes, % score'] + df_KanterU19['Accurate forward passes, % score'] + df_KanterU19['Accurate progressive passes, % score'] + df_KanterU19['Accurate passes to final third, % score'] + df_KanterU19['Accurate crosses, % score'] + df_KanterU19['Successful attacking actions per 90 score'] + df_KanterU19['Smart passes per 90 score'] + df_KanterU19['Key passes per 90 score'])/13
        df_KanterU19 = df_KanterU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Sparkefærdigheder Kant','1v1 Offensivt Kant','Kombinationsstærk Kant','Spilintelligens offensivt/indlægsstærk Kant']]

        df_AngribereU19['xG per 90 score'] = pd.qcut(df_AngribereU19['xG per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Goals per 90 score'] = pd.qcut(df_AngribereU19['Goals per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)  
        df_AngribereU19['Shots on target, % score'] = pd.qcut(df_AngribereU19['Shots on target, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)   
        df_AngribereU19['Offensive duels won, % score'] = pd.qcut(df_AngribereU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Duels won, % score'] = pd.qcut(df_AngribereU19['Duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Accurate passes, % score'] = pd.qcut(df_AngribereU19['Accurate passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Successful dribbles, % score'] = pd.qcut(df_AngribereU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['xA per 90 score'] = pd.qcut(df_AngribereU19['xA per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Touches in box per 90 score'] = pd.qcut(df_AngribereU19['Touches in box per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Deep completions per 90 score'] = pd.qcut(df_AngribereU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Successful attacking actions per 90 score'] = pd.qcut(df_AngribereU19['Successful attacking actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    
        df_AngribereU19 = df_AngribereU19[df_AngribereU19['Team'].str.contains('Horsens')]
        df_AngribereU19 = U19navne.merge(df_AngribereU19)
        
        df_AngribereU19['Sparkefærdigheder Angriber'] = (df_AngribereU19['xG per 90 score'] + df_AngribereU19['xG per 90 score'] + df_AngribereU19['Goals per 90 score'] + df_AngribereU19['Shots on target, % score'])/4
        df_AngribereU19['Boldfast Angriber'] = (df_AngribereU19['Offensive duels won, % score'] + df_AngribereU19['Offensive duels won, % score'] + df_AngribereU19['Duels won, % score'] + df_AngribereU19['Accurate passes, % score'] + df_AngribereU19['Successful dribbles, % score'])/5
        df_AngribereU19['Spilintelligens offensivt Angriber'] = (df_AngribereU19['xA per 90 score'] + df_AngribereU19['xG per 90 score'] + df_AngribereU19['Touches in box per 90 score'] + df_AngribereU19['Deep completions per 90 score'] + df_AngribereU19['Successful attacking actions per 90 score'] + df_AngribereU19['Touches in box per 90 score'] + df_AngribereU19['xG per 90 score'])/7
        
        df_AngribereU19 = df_AngribereU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Sparkefærdigheder Angriber','Boldfast Angriber','Spilintelligens offensivt Angriber']]
        
        
        df_samlet = df_StoppereU19.append(df_backsU19).append(df_Centrale_midtU19).append(df_KanterU19).append(df_AngribereU19)
        dfspillere = df_samlet['Spillere'].drop_duplicates(keep='last')
        dfspillere = dfspillere.astype(str)
        dfspillere = sorted(dfspillere)
        option2 = st.selectbox('Vælg spiller',dfspillere)
        df_samlet = df_samlet[df_samlet['Spillere'].str.contains(option2)]
        df_samlet = df_samlet.groupby(['Spillere']).mean(numeric_only=True)

        #Start på seneste 5 kampe
        dfU19s5 = pd.read_excel('U15 spillere seneste 5.xlsx')
        dfU19s5 = dfU19s5[dfU19s5['Minutes played'] >= 200]
        dfU19s5['Position'] = dfU19s5['Position'].astype(str)
        dfU19s5['Team'] = dfU19s5['Team'].astype(str)
        
        #Dele spillerne i ligaen ud på positioner
        df_backsU19 = dfU19s5[dfU19s5['Position'].str.contains('|'.join(['LB', 'RB']))]
        df_StoppereU19 = dfU19s5[dfU19s5['Position'].str.contains('|'.join(['CB']))]
        df_Centrale_midtU19 = dfU19s5[dfU19s5['Position'].str.contains('|'.join(['CM','AMF','DMF']))]
        df_KanterU19 = dfU19s5[dfU19s5['Position'].str.contains('|'.join(['RW','LW','RAMF','LAMF']))]
        df_AngribereU19 = dfU19s5[dfU19s5['Position'].str.contains('|'.join(['CF']))]
        
        #Rangere stoppere i ligaen og give dem 1-5 i rating på forskellige parametre
        df_StoppereU19['Def duels won score'] = pd.qcut(df_StoppereU19['Defensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate passes, % score'] = pd.qcut(df_StoppereU19['Accurate passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate long passes, % score'] = pd.qcut(df_StoppereU19['Accurate long passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Forward passes per 90 score'] = pd.qcut(df_StoppereU19['Forward passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate forward passes score'] = pd.qcut(df_StoppereU19['Accurate forward passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate short/medium passes, % score'] = pd.qcut(df_StoppereU19['Accurate short / medium passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Interceptions per 90 score'] = pd.qcut(df_StoppereU19['Interceptions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['PAdj Interceptions score'] = pd.qcut(df_StoppereU19['PAdj Interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Successful defensive actions per 90 score'] = pd.qcut(df_StoppereU19['Successful defensive actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Shots blocked per 90 score'] = pd.qcut(df_StoppereU19['Shots blocked per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate forward passes, %'] = pd.qcut(df_StoppereU19['Accurate forward passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate passes to finale third, % score'] = pd.qcut(df_StoppereU19['Accurate passes to final third, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate progressive passes, % score'] = pd.qcut(df_StoppereU19['Accurate progressive passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Deep completions per 90 score'] = pd.qcut(df_StoppereU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Offensive duels won, % score'] = pd.qcut(df_StoppereU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Progressive runs per 90 score'] = pd.qcut(df_StoppereU19['Progressive runs per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Successful dribbles, % score'] = pd.qcut(df_StoppereU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Aerial duels won, % score'] = pd.qcut(df_StoppereU19['Aerial duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19['Accurate through passes, % score'] = pd.qcut(df_StoppereU19['Accurate through passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_StoppereU19 = df_StoppereU19[df_StoppereU19['Team'].str.contains('Horsens')]
        df_StoppereU19 = U19navne.merge(df_StoppereU19)
        
        #Oprette forskellige parametre ud fra talent-id for stoppere
        df_StoppereU19['Pasningssikker Stopper'] = (df_StoppereU19['Accurate passes, % score'] + df_StoppereU19['Accurate long passes, % score'] + df_StoppereU19['Forward passes per 90 score'] + df_StoppereU19['Accurate forward passes score'] + df_StoppereU19['Accurate forward passes score'] + df_StoppereU19['Accurate short/medium passes, % score'] + df_StoppereU19['Forward passes per 90 score'] + df_StoppereU19['Accurate forward passes score'])/8
        df_StoppereU19['Spilintelligens defensivt Stopper'] = (df_StoppereU19['Interceptions per 90 score'] + df_StoppereU19['Successful defensive actions per 90 score']+df_StoppereU19['Shots blocked per 90 score'] + df_StoppereU19['PAdj Interceptions score'] + df_StoppereU19['PAdj Interceptions score'] + df_StoppereU19['Interceptions per 90 score'])/6
        df_StoppereU19['Spilintelligens offensivt Stopper'] = (df_StoppereU19['Accurate forward passes score'] + df_StoppereU19['Accurate passes to finale third, % score'] + df_StoppereU19['Accurate progressive passes, % score'] + df_StoppereU19['Accurate through passes, % score'] + df_StoppereU19['Deep completions per 90 score'] + df_StoppereU19['Offensive duels won, % score'] + df_StoppereU19['Progressive runs per 90 score'] + df_StoppereU19['Successful dribbles, % score'] + df_StoppereU19['Accurate forward passes score'])/9
        df_StoppereU19['Nærkamps- og duelstærk Stopper'] = (df_StoppereU19['Def duels won score'] + df_StoppereU19['Aerial duels won, % score'] + df_StoppereU19['Def duels won score'] + df_StoppereU19['Def duels won score'])/4
        df_StoppereU19 = df_StoppereU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Pasningssikker Stopper','Spilintelligens defensivt Stopper','Spilintelligens offensivt Stopper','Nærkamps- og duelstærk Stopper']]
        
        #Samme proces med backs
        df_backsU19['Accurate crosses, % score'] = pd.qcut(df_backsU19['Accurate crosses, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['xA per 90 score'] = pd.qcut(df_backsU19['xA per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Deep completions per 90 score'] = pd.qcut(df_backsU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Deep completed crosses per 90 score'] = pd.qcut(df_backsU19['Deep completed crosses per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Successful dribbles, % score'] = pd.qcut(df_backsU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Defensive duels won, % score'] = pd.qcut(df_backsU19['Defensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Progressive runs per 90 score'] = pd.qcut(df_backsU19['Progressive runs per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Offensive duels won, % score'] = pd.qcut(df_backsU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Accelerations per 90 score'] = pd.qcut(df_backsU19['Accelerations per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Duels won, % score'] = pd.qcut(df_backsU19['Duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Interceptions per 90 score'] = pd.qcut(df_backsU19['Interceptions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19['Successful defensive actions per 90 score'] = pd.qcut(df_backsU19['Successful defensive actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backsU19 = df_backsU19[df_backsU19['Team'].str.contains('Horsens')]
        df_backsU19 = U19navne.merge(df_backsU19)
        
        df_backsU19['Indlægsstærk Back'] = (df_backsU19['Accurate crosses, % score'] + df_backsU19['xA per 90 score'] + df_backsU19['Deep completed crosses per 90 score'] + df_backsU19['Deep completed crosses per 90 score'])/4
        df_backsU19['1v1 færdigheder Back'] = (df_backsU19['Successful dribbles, % score'] + df_backsU19['Defensive duels won, % score'] + df_backsU19['Progressive runs per 90 score'] + df_backsU19['Offensive duels won, % score'] + df_backsU19['Accelerations per 90 score'] + df_backsU19['Duels won, % score'])/6
        df_backsU19['Spilintelligens defensivt Back'] = (df_backsU19['Interceptions per 90 score'] + df_backsU19['Successful defensive actions per 90 score'] + df_backsU19['Duels won, % score'] + df_backsU19['Defensive duels won, % score'])/4
        df_backsU19 = df_backsU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Indlægsstærk Back','1v1 færdigheder Back','Spilintelligens defensivt Back']]
        
        #Samme proces med centrale midt
        df_Centrale_midtU19['Accurate passes, % score'] = pd.qcut(df_Centrale_midtU19['Accurate passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Accurate forward passes, % score'] = pd.qcut(df_Centrale_midtU19['Accurate forward passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Accurate long passes, % score'] = pd.qcut(df_Centrale_midtU19['Accurate long passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Key passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Key passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Smart passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Smart passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Deep completions per 90 score'] = pd.qcut(df_Centrale_midtU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Through passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Through passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Progressive passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Progressive passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Offensive duels won, % score'] = pd.qcut(df_Centrale_midtU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Received passes per 90 score'] = pd.qcut(df_Centrale_midtU19['Received passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Successful dribbles, % score'] = pd.qcut(df_Centrale_midtU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Successful defensive actions per 90 score'] = pd.qcut(df_Centrale_midtU19['Successful defensive actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Interceptions per 90 score'] = pd.qcut(df_Centrale_midtU19['Interceptions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Duels won, % score'] = pd.qcut(df_Centrale_midtU19['Duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['Defensive duels won, % score'] = pd.qcut(df_Centrale_midtU19['Defensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19['PAdj Interceptions score'] = pd.qcut(df_Centrale_midtU19['PAdj Interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midtU19 = df_Centrale_midtU19[df_Centrale_midtU19['Team'].str.contains('Horsens')]
        df_Centrale_midtU19 = U19navne.merge(df_Centrale_midtU19)
        df_Centrale_midtU19['Pasningssikker/spilvendinger Central midt'] = (df_Centrale_midtU19['Accurate passes, % score'] + df_Centrale_midtU19['Accurate forward passes, % score'] + df_Centrale_midtU19['Accurate long passes, % score'] + df_Centrale_midtU19['Accurate passes, % score'] + df_Centrale_midtU19['Key passes per 90 score'] + df_Centrale_midtU19['Accurate forward passes, % score'] + df_Centrale_midtU19['Smart passes per 90 score'] + df_Centrale_midtU19['Deep completions per 90 score'] + df_Centrale_midtU19['Through passes per 90 score'] + df_Centrale_midtU19['Progressive passes per 90 score'])/10
        df_Centrale_midtU19['Boldfast Central midt'] = (df_Centrale_midtU19['Offensive duels won, % score'] + df_Centrale_midtU19['Received passes per 90 score'] + df_Centrale_midtU19['Accurate passes, % score'] + df_Centrale_midtU19['Successful dribbles, % score'] + df_Centrale_midtU19['Accurate passes, % score'])/5
        df_Centrale_midtU19['Spilintelligens defensivt Central midt'] = (df_Centrale_midtU19['Interceptions per 90 score'] + df_Centrale_midtU19['Successful defensive actions per 90 score'] + df_Centrale_midtU19['Duels won, % score'] + df_Centrale_midtU19['Defensive duels won, % score'] + df_Centrale_midtU19['PAdj Interceptions score'] + df_Centrale_midtU19['PAdj Interceptions score'])/6
        df_Centrale_midtU19 = df_Centrale_midtU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Pasningssikker/spilvendinger Central midt','Boldfast Central midt', 'Spilintelligens defensivt Central midt']]
        
        df_KanterU19['xG per 90 score'] = pd.qcut(df_KanterU19['xG per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Goals per 90 score'] = pd.qcut(df_KanterU19['Goals per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Shots on target, % score'] = pd.qcut(df_KanterU19['Shots on target, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Successful dribbles, % score'] = pd.qcut(df_KanterU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate passes, % score'] = pd.qcut(df_KanterU19['Accurate passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate forward passes, % score'] = pd.qcut(df_KanterU19['Accurate forward passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Deep completions per 90 score'] = pd.qcut(df_KanterU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate through passes, % score'] = pd.qcut(df_KanterU19['Accurate through passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate progressive passes, % score'] = pd.qcut(df_KanterU19['Accurate progressive passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Successful attacking actions per 90 score'] = pd.qcut(df_KanterU19['Successful attacking actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate passes to final third, % score'] = pd.qcut(df_KanterU19['Accurate passes to final third, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Offensive duels won, % score'] = pd.qcut(df_KanterU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['xA per 90 score'] = pd.qcut(df_KanterU19['xA per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate smart passes, % score'] = pd.qcut(df_KanterU19['Accurate smart passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Accurate crosses, % score'] = pd.qcut(df_KanterU19['Accurate crosses, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Successful attacking actions per 90 score'] = pd.qcut(df_KanterU19['Successful attacking actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Smart passes per 90 score'] = pd.qcut(df_KanterU19['Smart passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19['Key passes per 90 score'] = pd.qcut(df_KanterU19['Key passes per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_KanterU19 = df_KanterU19[df_KanterU19['Team'].str.contains('Horsens')]
        df_KanterU19 = U19navne.merge(df_KanterU19)
        
        df_KanterU19['Sparkefærdigheder Kant'] = (df_KanterU19['xG per 90 score'] + df_KanterU19['Goals per 90 score'] + df_KanterU19['Shots on target, % score'])/3
        df_KanterU19['1v1 Offensivt Kant'] = (df_KanterU19['Successful dribbles, % score'] + df_KanterU19['Successful dribbles, % score'] + df_KanterU19['Offensive duels won, % score'])/3
        df_KanterU19['Kombinationsstærk Kant'] = (df_KanterU19['Accurate passes, % score'] + df_KanterU19['Accurate forward passes, % score'] + df_KanterU19['Deep completions per 90 score'] + df_KanterU19['Accurate through passes, % score'] + df_KanterU19['Accurate progressive passes, % score'] + df_KanterU19['Successful attacking actions per 90 score'] + df_KanterU19['Accurate passes to final third, % score'])/7
        df_KanterU19['Spilintelligens offensivt/indlægsstærk Kant'] = (df_KanterU19['xA per 90 score'] + df_KanterU19['xG per 90 score'] + df_KanterU19['xA per 90 score'] + df_KanterU19['xG per 90 score'] + df_KanterU19['Accurate through passes, % score'] + df_KanterU19['Accurate smart passes, % score'] + df_KanterU19['Accurate forward passes, % score'] + df_KanterU19['Accurate progressive passes, % score'] + df_KanterU19['Accurate passes to final third, % score'] + df_KanterU19['Accurate crosses, % score'] + df_KanterU19['Successful attacking actions per 90 score'] + df_KanterU19['Smart passes per 90 score'] + df_KanterU19['Key passes per 90 score'])/13
        df_KanterU19 = df_KanterU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Sparkefærdigheder Kant','1v1 Offensivt Kant','Kombinationsstærk Kant','Spilintelligens offensivt/indlægsstærk Kant']]

        df_AngribereU19['xG per 90 score'] = pd.qcut(df_AngribereU19['xG per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Goals per 90 score'] = pd.qcut(df_AngribereU19['Goals per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)  
        df_AngribereU19['Shots on target, % score'] = pd.qcut(df_AngribereU19['Shots on target, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)   
        df_AngribereU19['Offensive duels won, % score'] = pd.qcut(df_AngribereU19['Offensive duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Duels won, % score'] = pd.qcut(df_AngribereU19['Duels won, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Accurate passes, % score'] = pd.qcut(df_AngribereU19['Accurate passes, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Successful dribbles, % score'] = pd.qcut(df_AngribereU19['Successful dribbles, %'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['xA per 90 score'] = pd.qcut(df_AngribereU19['xA per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Touches in box per 90 score'] = pd.qcut(df_AngribereU19['Touches in box per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Deep completions per 90 score'] = pd.qcut(df_AngribereU19['Deep completions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_AngribereU19['Successful attacking actions per 90 score'] = pd.qcut(df_AngribereU19['Successful attacking actions per 90'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
    
        df_AngribereU19 = df_AngribereU19[df_AngribereU19['Team'].str.contains('Horsens')]
        df_AngribereU19 = U19navne.merge(df_AngribereU19)
        
        df_AngribereU19['Sparkefærdigheder Angriber'] = (df_AngribereU19['xG per 90 score'] + df_AngribereU19['xG per 90 score'] + df_AngribereU19['Goals per 90 score'] + df_AngribereU19['Shots on target, % score'])/4
        df_AngribereU19['Boldfast Angriber'] = (df_AngribereU19['Offensive duels won, % score'] + df_AngribereU19['Offensive duels won, % score'] + df_AngribereU19['Duels won, % score'] + df_AngribereU19['Accurate passes, % score'] + df_AngribereU19['Successful dribbles, % score'])/5
        df_AngribereU19['Spilintelligens offensivt Angriber'] = (df_AngribereU19['xA per 90 score'] + df_AngribereU19['xG per 90 score'] + df_AngribereU19['Touches in box per 90 score'] + df_AngribereU19['Deep completions per 90 score'] + df_AngribereU19['Successful attacking actions per 90 score'] + df_AngribereU19['Touches in box per 90 score'] + df_AngribereU19['xG per 90 score'])/7
        
        df_AngribereU19 = df_AngribereU19[['Spillere','Team','Position','Age','Matches played','Minutes played','Sparkefærdigheder Angriber','Boldfast Angriber','Spilintelligens offensivt Angriber']]
        
        
        df_samlets5 = df_StoppereU19.append(df_backsU19).append(df_Centrale_midtU19).append(df_KanterU19).append(df_AngribereU19)
        df_samlets5 = df_samlets5[df_samlets5['Spillere'].str.contains(option2)]
        df_samlets5 = df_samlets5.groupby(['Spillere']).mean(numeric_only=True)


        df_samlet = df_samlet.append(df_samlets5)

        option3 = st.selectbox('Vælg position',('Stopper','Back','Central midt','Kant','Angriber'))

        df_samlet = df_samlet.filter(regex=option3)
        df_samlet['Datasæt'] = 'Seneste 5 kampe'
        df_samlet['Datasæt'][0] = 'Hele sæsonen'
        df_samlet = df_samlet.rename(columns = lambda x: x.replace(option3, ''))
        df_samletvendtom = df_samlet.reset_index()
        df_samletvendtom['Unique'] = df_samletvendtom['Spillere'] + df_samletvendtom['Datasæt']
        df_samletvendtom = pd.DataFrame.drop(df_samletvendtom,axis=1,columns='Spillere')
        df_samletvendtom = df_samletvendtom.transpose()
        df_samletvendtom = df_samletvendtom.reset_index()
        df_samletvendtom = df_samletvendtom.query("index != 'Unique'")
        df_samletvendtom = df_samletvendtom.query("index != 'Datasæt'")
        df_samletvendtom = pd.DataFrame(df_samletvendtom,index=None)
        df_samletvendtom = df_samletvendtom.rename(columns={'index':'index'}).set_index('index')
        df_samletvendtom = df_samletvendtom.rename(columns={0:'Hele sæsonen'})
        df_samletvendtom = df_samletvendtom.rename(columns={1:'Seneste 5 kampe'})


        
        categories = df_samletvendtom.index
        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r= df_samletvendtom['Hele sæsonen'],
            theta=categories,
            fill='toself',
            name='Hele sæsonen'
        ))
        fig.add_trace(go.Scatterpolar(
            r= df_samletvendtom['Seneste 5 kampe'],
            theta=categories,
            fill='toself',
            name='Seneste 5 kampe',
        ))

        fig.update_layout(
            polar=dict(
            radialaxis=dict(
            visible=True,
            range=[0, 5],
            )),
        showlegend=True,
        )
        fig.update_layout(polar=dict(bgcolor = '#1e2130'))
        st.title(option2+' fodbold')
        st.write('Rating efter talent-id på position, skalaen er 1-5, 5 er hvis spilleren er blandt de 20% bedste i ligaen på den pågældende stat')        
        st.plotly_chart(fig,use_container_width=True)
        st.dataframe(df_samletvendtom,use_container_width=True)
        print('Individuelt dashboard')    
    
    
    Årgange = {'U15':U15,'U17':U17,
               'U19':U19,}
    rullemenu = st.selectbox('Vælg årgang',Årgange.keys())
    Årgange[rullemenu]()


def event_data():
    def U15():
        import pandas as pd
        import streamlit as st
        from mplsoccer.pitch import Pitch
        import matplotlib.pyplot as plt
        import plotly.express as px

        df = pd.read_csv('U15 eventdata.csv',low_memory=False)

        kampe = df['label'].drop_duplicates(keep='first')
        option4 = st.multiselect('Vælg kamp (Hvis ingen kamp er valgt, vises alle)',kampe)
        if len(option4) > 0:
            filtreretdfkamp = option4
        else:
            filtreretdfkamp = kampe

        filtreretdfkamp = df.loc[df.loc[df.label.isin(filtreretdfkamp),'label'].index.values]

        filtreretdfhold = filtreretdfkamp.loc[filtreretdfkamp.loc[filtreretdfkamp['Team name'] == 'Horsens U15', 'Team name'].index.values]

        spillere = filtreretdfhold['Player name'].drop_duplicates(keep='first').astype(str)
        spillere = sorted(spillere)
        option = st.multiselect('Vælg spillere',spillere)
        if len(option) > 0:
            filtreretdfspiller = option
        else:
            filtreretdfspiller = spillere
        filtreretdfspiller = filtreretdfhold.loc[filtreretdfhold.loc[filtreretdfhold['Player name'].isin(filtreretdfspiller),'Player name'].index.values]

        aktioner = filtreretdfspiller['variable'].drop_duplicates(keep='first')
        aktioner = sorted(aktioner)
        option3 = st.multiselect('Vælg aktion',aktioner)
        if len(option3) > 0:
            filtreretdfaktion = option3
        else:
            filtreretdfaktion = aktioner
        filtreretdfaktion = filtreretdfspiller.loc[filtreretdfspiller.loc[filtreretdfspiller['variable'].isin(filtreretdfaktion),'variable'].index.values]

        x = filtreretdfaktion['Action location start x']
        y = filtreretdfaktion['Action location start y']


        pitch = Pitch(pitch_type = 'wyscout',pitch_color='grass', line_color='white', stripe=True)
        fig, ax = pitch.draw()
        sc = pitch.scatter(x,y,ax=ax)
        st.pyplot(plt.gcf())
    def U17():
        import pandas as pd
        import streamlit as st
        from mplsoccer.pitch import Pitch
        import matplotlib.pyplot as plt
        import plotly.express as px

        df = pd.read_csv('U17 eventdata.csv',low_memory=False)

        kampe = df['label'].drop_duplicates(keep='first')
        option4 = st.multiselect('Vælg kamp (Hvis ingen kamp er valgt, vises alle)',kampe)
        if len(option4) > 0:
            filtreretdfkamp = option4
        else:
            filtreretdfkamp = kampe

        filtreretdfkamp = df.loc[df.loc[df.label.isin(filtreretdfkamp),'label'].index.values]

        filtreretdfhold = filtreretdfkamp.loc[filtreretdfkamp.loc[filtreretdfkamp['Team name'] == 'Horsens U17', 'Team name'].index.values]

        spillere = filtreretdfhold['Player name'].drop_duplicates(keep='first').astype(str)
        spillere = sorted(spillere)
        option = st.multiselect('Vælg spillere',spillere)
        if len(option) > 0:
            filtreretdfspiller = option
        else:
            filtreretdfspiller = spillere
        filtreretdfspiller = filtreretdfhold.loc[filtreretdfhold.loc[filtreretdfhold['Player name'].isin(filtreretdfspiller),'Player name'].index.values]

        aktioner = filtreretdfspiller['variable'].drop_duplicates(keep='first')
        aktioner = sorted(aktioner)
        option2 = st.multiselect('Vælg aktion',aktioner)
        if len(option2) > 0:
            filtreretdfaktion = option2
        else:
            filtreretdfaktion = aktioner
        filtreretdfaktion = filtreretdfspiller.loc[filtreretdfspiller.loc[filtreretdfspiller['variable'].isin(filtreretdfaktion),'variable'].index.values]

        x = filtreretdfaktion['Action location start x']
        y = filtreretdfaktion['Action location start y']


        pitch = Pitch(pitch_type = 'wyscout',pitch_color='grass', line_color='white', stripe=True)
        fig, ax = pitch.draw()
        sc = pitch.scatter(x,y,ax=ax)
        st.pyplot(plt.gcf())        
    def U19():
        import pandas as pd
        import streamlit as st
        from mplsoccer.pitch import Pitch
        import matplotlib.pyplot as plt
        import plotly.express as px

        df = pd.read_csv('U19 eventdata.csv',low_memory=False)

        kampe = df['label'].drop_duplicates(keep='first')
        option4 = st.multiselect('Vælg kamp (Hvis ingen kamp er valgt, vises alle)',kampe)
        if len(option4) > 0:
            filtreretdfkamp = option4
        else:
            filtreretdfkamp = kampe

        filtreretdfkamp = df.loc[df.loc[df.label.isin(filtreretdfkamp),'label'].index.values]

        filtreretdfhold = filtreretdfkamp.loc[filtreretdfkamp.loc[filtreretdfkamp['Team name'] == 'Horsens U19', 'Team name'].index.values]

        spillere = filtreretdfhold['Player name'].drop_duplicates(keep='first').astype(str)
        spillere = sorted(spillere)
        option = st.multiselect('Vælg spillere',spillere)
        if len(option) > 0:
            filtreretdfspiller = option
        else:
            filtreretdfspiller = spillere
        filtreretdfspiller = filtreretdfhold.loc[filtreretdfhold.loc[filtreretdfhold['Player name'].isin(filtreretdfspiller),'Player name'].index.values]

        aktioner = filtreretdfspiller['variable'].drop_duplicates(keep='first')
        aktioner = sorted(aktioner)
        option2 = st.multiselect('Vælg aktion',aktioner)
        if len(option2) > 0:
            filtreretdfaktion = option2
        else:
            filtreretdfaktion = aktioner
        filtreretdfaktion = filtreretdfspiller.loc[filtreretdfspiller.loc[filtreretdfspiller['variable'].isin(filtreretdfaktion),'variable'].index.values]

        x = filtreretdfaktion['Action location start x']
        y = filtreretdfaktion['Action location start y']


        pitch = Pitch(pitch_type = 'wyscout',pitch_color='grass', line_color='white', stripe=True)
        fig, ax = pitch.draw()
        sc = pitch.scatter(x,y,ax=ax)
        st.pyplot(plt.gcf())
    Årgange = {'U15':U15,
               'U17':U17,
               'U19':U19}
    rullemenu = st.selectbox('Vælg årgang',Årgange.keys())
    Årgange[rullemenu]()


overskrifter_til_menu = {
    'Wellness Data':Wellness_data,
    'GPS Data': GPS_Data,
    'Teamsheet': Teamsheet,
    'Individuelt dashboard': Individuelt_dashboard,
    'Event data' : event_data
}
demo_navn = st.sidebar.selectbox('Vælg dataform',overskrifter_til_menu.keys())
overskrifter_til_menu[demo_navn]()
from PIL import Image

image = Image.open('Logo.png')
st.sidebar.image(image)
