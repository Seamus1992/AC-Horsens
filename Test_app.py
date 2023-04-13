import streamlit as st

def Wellness_data():
    import pandas as pd
    df0 = pd.read_csv('samlet wellness.csv')
    df_wellness = df0[['Navn','Ugenummer','Årgang','Hvor udmattet er du?','Hvordan var din søvn i den seneste uge?','Hvor mange timer sov du i gennemsnit pr. nat i den seneste uge?','Bedøm din muskeltræthed','Hvordan har du det psykologisk (mentalt)?', 'Hvordan har din kost(mad) set ud den seneste uge?','Hvordan har dit humør været efter fodboldtræning den seneste uge?']]

    Årgang = df_wellness['Årgang']
    df_Årgang = []
    for i in Årgang:
        if i not in df_Årgang:
            if i !=None:
                df_Årgang.append(i)
    df_Årgang = sorted(df_Årgang)
    option = st.selectbox('Vælg årgang',df_Årgang)
    filtreret_dfårgang = df_wellness.loc[df_wellness.loc[df_wellness['Årgang'] == option, 'Årgang'].index.values]

    df = filtreret_dfårgang
    Ugenummer = df_wellness['Ugenummer']
    df_Ugenummer = []
    for i in Ugenummer:
        if i not in df_Ugenummer:
            if i !=None:
                df_Ugenummer.append(i)
    df_Ugenummer = sorted(df_Ugenummer)
    option2 = st.selectbox('Vælg ugenummer',df_Ugenummer)

    filtreret_dfugenummer = df_wellness.loc[df.loc[df_wellness.Ugenummer ==option2,'Ugenummer'].index.values]
    df = filtreret_dfugenummer
    #df['Jeg oplevede at jeg havde kontrol'].astype(int)
    df = df.drop_duplicates(subset='Navn', keep='last')
    #df = df.groupby(['Navn']).mean
    df = df.set_index('Navn')
    df = df.apply(pd.to_numeric)
    df['Gennemsnit'] = df.iloc[:,2:11].mean(axis=1,skipna=True)
    
    # Subset your original dataframe with condition
    df_ = df[df['Gennemsnit'].gt(4)]
    # Pass the subset dataframe index and column to pd.IndexSlice
    slice_ = pd.IndexSlice[df_.index, df_.columns]

    df1 = df.style.set_properties(**{'background-color': 'red'}, subset=slice_)
    st.write('Wellness Data')
    st.dataframe(df1)
    #with pd.ExcelWriter('Wellness udtræk.xlsx', engine="openpyxl", mode="a",if_sheet_exists='replace') as writer:
        #df.to_excel(writer,'Rådata', index=True)

    st.write('Flow Data')

    df_flow = df0[['Navn','Ugenummer','Årgang','Jeg følte mig tilpas udfordret under træning i den seneste uge','Jeg oplevede at tanker (og handlinger) var rettet mod aktiviteten i den seneste uge','Min tidsfornemmelse forsvandt','Jeg havde ingen problemer med at koncentrere mig','Jeg var helt klar i hovedet','Jeg var helt optaget af aktiviteten','Mine tanker blev af sig selv knyttet til aktiviteten','Jeg var ikke i tvivl om hvad jeg skulle gøre','Jeg oplevede at jeg havde kontrol']]

    filtreret_dfårgang = df_flow.loc[df_flow.loc[df_flow['Årgang'] == option, 'Årgang'].index.values]

    df = filtreret_dfårgang

    filtreret_dfugenummer = df_flow.loc[df.loc[df_flow.Ugenummer ==option2,'Ugenummer'].index.values]
    df = filtreret_dfugenummer
    df = df.drop_duplicates(subset='Navn', keep='last')
    df = df.set_index('Navn')

    df = df.apply(pd.to_numeric)
    df['Gennemsnit'] = df.iloc[:,2:10].mean(axis=1,skipna=True)

    # Subset your original dataframe with condition
    df_ = df[df['Gennemsnit'].gt(4)]

    # Pass the subset dataframe index and column to pd.IndexSlice
    slice_ = pd.IndexSlice[df_.index, df_.columns]

    df1 = df.style.set_properties(**{'background-color': 'red'}, subset=slice_)

    st.dataframe(df1)
    print('wellness')
     
def GPS_Data():
    import pandas as pd
    import streamlit as st
    import seaborn as sns
    import matplotlib.pyplot as plt
    import openpyxl as xlsxwriter
    from pandas import DataFrame
    
    
    dforiginal = pd.read_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\samlet gps data.csv')
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
    st.write('Afvigelser for den valgte spiller i forhold til truppens gennemsnit')
    st.line_chart(afvigelser,y=['Sprint','Distance (km)','Top Speed (km/h)','Højintens løb','Hårde Accelerationer','Hårde deccelerationer','Tid med høj puls'],)
    st.write('Tabel for afvigelser')
    st.dataframe(afvigelser)
    st.write('Absolutte tal for den valgte spiller')
    st.dataframe(df)
    print('GPS data')

def Teamsheet():
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    import os
    dfbenchmark = pd.read_excel(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Benchmarks.xlsx')
    dfårgange = dfbenchmark['Årgang'].drop_duplicates(keep='last')
    option2 = st.selectbox('Vælg årgang',dfårgange)
    df = pd.read_excel(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Team Stats Horsens U15.xlsx')
    df = df.iloc[2:]
    df2 = pd.read_excel(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Team Stats Horsens U17.xlsx')
    df2 = df2.iloc[2:]
    df3 = pd.read_excel(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Team Stats Horsens U19.xlsx')
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
    st.title('Defensive parametre',)
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
        U19navne = pd.read_excel(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Navne.xlsx')
        dfU19 = pd.read_excel(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\U19 spillere sæson.xlsx')
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
        dfU19s5 = pd.read_excel(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\U19 spillere seneste 5.xlsx')
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
        st.write('Rating efter talent-id på position')
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
        U19navne = pd.read_excel(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Navne.xlsx')
        dfU19 = pd.read_excel(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\U17 spillere sæson.xlsx')
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
        dfU19s5 = pd.read_excel(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\U17 spillere seneste 5.xlsx')
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
        st.write('Rating efter talent-id på position')
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
        U19navne = pd.read_excel(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Navne.xlsx')
        dfU19 = pd.read_excel(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\U15 spillere sæson.xlsx')
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
        dfU19s5 = pd.read_excel(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\U15 spillere seneste 5.xlsx')
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
        st.write('Rating efter talent-id på position')
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

        df = pd.read_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\U15 eventdata.csv',low_memory=False)

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

        df = pd.read_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\U17 eventdata.csv',low_memory=False)

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

        df = pd.read_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\U19 eventdata.csv',low_memory=False)

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

image = Image.open(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Logo.png')
st.sidebar.image(image)
