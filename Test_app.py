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
    førtræning = førtræning.loc[~førtræning.index.duplicated(keep='first')]
    førtræning = førtræning.astype(int,errors='ignore')
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
    eftertræning = eftertræning.loc[~eftertræning.index.duplicated(keep='first')]
    eftertræning = eftertræning.astype(int,errors='ignore')
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
    import streamlit as st
    def U15():
        import pandas as pd
        import csv
        import streamlit as st
        import numpy as np
        from datetime import datetime
        df = pd.read_csv('Teamsheet egne kampe U15.csv')
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
        team_df= team_df.round(decimals=2)
        st.dataframe(team_df)

        forward_passes_cols = [col for col in dfsorteredekampe.columns if col.endswith('.forwardPasses')]
        forward_passes_successful_cols = [col for col in dfsorteredekampe.columns if col.endswith('.forwardPassesSuccessful')]
        passes_cols = [col for col in dfsorteredekampe.columns if col.endswith('.passes')]
        touches_in_box_cols = [col for col in dfsorteredekampe.columns if col.endswith('.touchesInBox')]
        xg_cols = [col for col in dfsorteredekampe.columns if col.endswith('.xg')]
        xgpershot_cols = [col for col in dfsorteredekampe.columns if col.endswith('.xgPerShot')]
        dzshots_cols = [col for col in dfsorteredekampe.columns if col.endswith('.shotsFromDangerZone')]
        possessionantal_cols = [col for col in dfsorteredekampe.columns if col.endswith('.possessionNumber')]
        possessionanmodstandershalvdel_cols = [col for col in dfsorteredekampe.columns if col.endswith('.reachingOpponentHalf')]
        possessionanmodstandersfelt_cols = [col for col in dfsorteredekampe.columns if col.endswith('.reachingOpponentBox')]
        challenge_intensity_cols = [col for col in dfsorteredekampe.columns if col.endswith('.challengeIntensity')]
        recoveries_cols = [col for col in dfsorteredekampe.columns if col.endswith('.recoveriesTotal')]
        opponenthalfrecoveries_cols = [col for col in dfsorteredekampe.columns if col.endswith('.opponentHalfRecoveries')]
        ppda_cols = [col for col in dfsorteredekampe.columns if col.endswith('.ppda')]

        # Create a new dataframe with the average values for each team
        team_data_målbare = {}
        for team in set([col.split('.')[1] for col in shots_cols]):
            team_forward_passes = dfsorteredekampe[[col for col in forward_passes_cols if(team) in col]].mean(axis=1)    
            team_forward_passes_successful = dfsorteredekampe[[col for col in forward_passes_successful_cols if(team) in col]].mean(axis=1)
            team_passes = dfsorteredekampe[[col for col in passes_cols if (team) in col]].mean(axis=1)
            team_touches_in_box = dfsorteredekampe[[col for col in touches_in_box_cols if (team) in col]].mean(axis=1)
            team_xg = dfsorteredekampe[[col for col in xg_cols if (team) in col]].mean(axis=1)
            team_xgpershot = dfsorteredekampe[[col for col in xgpershot_cols if (team) in col]].mean(axis=1)
            team_dzshots = dfsorteredekampe[[col for col in dzshots_cols if (team) in col]].mean(axis=1)
            team_possessionantal = dfsorteredekampe[[col for col in possessionantal_cols if (team) in col]].mean(axis=1)
            team_possessionmodstandershalvdel = dfsorteredekampe[[col for col in possessionanmodstandershalvdel_cols if (team) in col]].mean(axis=1)
            team_possessionmodstandersfelt = dfsorteredekampe[[col for col in possessionanmodstandersfelt_cols if (team) in col]].mean(axis=1)
            team_challenge_intensity = dfsorteredekampe[[col for col in challenge_intensity_cols if (team) in col]].mean(axis=1)
            team_recoveries = dfsorteredekampe[[col for col in recoveries_cols if (team) in col]].mean(axis=1)
            team_opponenthalfrecoveries = dfsorteredekampe[[col for col in opponenthalfrecoveries_cols if (team) in col]].mean(axis=1)

            team_ppda = dfsorteredekampe[[col for col in ppda_cols if (team) in col]].mean(axis=1)

            team_data_målbare[team] = pd.concat([team_forward_passes,team_forward_passes_successful, team_passes, team_touches_in_box,team_xg,team_xgpershot,team_dzshots,team_possessionantal,team_possessionmodstandershalvdel,team_possessionmodstandersfelt,team_challenge_intensity,team_recoveries,team_opponenthalfrecoveries,team_ppda], axis=1)
            
        team_df_målbare = pd.concat(team_data_målbare, axis=0, keys=team_data_målbare.keys())
        team_df_målbare.columns = ['Forward passes','Forward passes successful', 'Passes', 'Touches in box','xG','xG/shot','Dangerzone shots','Antal possessions','Antal possessions der når modstanders halvdel','Antal possessions der når modstanders felt','Challenge intensity','Recoveries','Opp half recoveries','PPDA']
        team_df_målbare = team_df_målbare.groupby(level=0).mean()
        team_df_målbare['Forward pass %'] = (team_df_målbare['Forward passes successful']/team_df_målbare['Forward passes'])*100
        team_df_målbare['Forward pass share'] = (team_df_målbare['Forward passes']/team_df_målbare['Passes'])*100
        team_df_målbare['Forward pass score'] = team_df_målbare[['Forward pass share','Forward pass %']].mean(axis=1)
        team_df_målbare['Possession to opp box'] = team_df_målbare['Antal possessions der når modstanders felt']
        team_df_målbare['Possession to opp half %'] = (team_df_målbare['Antal possessions der når modstanders halvdel']/team_df_målbare['Antal possessions'])*100
        team_df_målbare['Possession to opp box %'] = (team_df_målbare['Antal possessions der når modstanders felt']/team_df_målbare['Antal possessions'])*100
        team_df_målbare = team_df_målbare[['Forward pass score','Touches in box','xG','xG/shot','Dangerzone shots','Possession to opp box','Possession to opp half %','Possession to opp box %','Challenge intensity','Recoveries','Opp half recoveries','PPDA']]
        team_df_målbare = team_df_målbare.round(decimals=3)
        hold = 'Horsens U15'
        team_df_målbare_andre_hold = team_df_målbare.drop(hold)
        team_df_målbare['xG against'] = team_df_målbare_andre_hold['xG'].mean()
        team_df_målbare['Danger zone shots against'] = team_df_målbare_andre_hold['Dangerzone shots'].mean()
        team_df_målbare['Touches in box against'] = team_df_målbare_andre_hold['Touches in box'].mean()
        team_df_målbare['Duels won %'] = (team_df['Duels won']/team_df['Duels'])*100
        mask = team_df_målbare.index.str.contains('Horsens')
        team_df_målbare = team_df_målbare[mask]
        team_df_målbare = team_df_målbare.round(decimals=2)

        import pandas as pd
        import csv
        import streamlit as st
        import numpy as np
        from datetime import datetime

        df = pd.read_csv('Teamsheet alle kampe U15.csv')

        dfsorteredeallekampe = df.iloc[: , 1:]
        dfsorteredeallekampe['date'] = dfsorteredeallekampe['date'].astype(str)
        dfsorteredeallekampe['date'] = dfsorteredeallekampe['date'].str.replace(r'\sGMT.*$', '', regex=True)
        dfsorteredeallekampe['date'] = pd.to_datetime(dfsorteredeallekampe['date'], format="%B %d, %Y at %I:%M:%S %p")
        dfsorteredeallekampe['date'] = dfsorteredeallekampe['date'].dt.strftime('%d-%m-%Y')
        dfsorteredeallekampe = dfsorteredeallekampe.transpose()
        dfoverskrifter = dfsorteredeallekampe[:2]
        dfsorteredeallekampe = dfsorteredeallekampe[2:].apply(pd.to_numeric, errors='coerce')
        dfsorteredeallekampe = pd.concat([dfoverskrifter,dfsorteredeallekampe])
        dfsorteredeallekampe = dfsorteredeallekampe.dropna(how='all')
        dfsorteredeallekampe = dfsorteredeallekampe.rename_axis('Parameter').astype(str)
        dfsorteredeallekampe = dfsorteredeallekampe.transpose()


        goals_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.goals')]
        shots_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.shots')]
        xg_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.xg')]
        duels_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.duels')]
        duelswon_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.duelsSuccessful')]
        possession_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.possessionPercent')]
        ppda_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.ppda')]

        # Create a new dataframe with the average values for each team
        team_data = {}
        for team in set([col.split('.')[1] for col in shots_cols]):
            team_goals = dfsorteredeallekampe[[col for col in goals_cols if(team) in col]].mean(axis=1)    
            team_shots = dfsorteredeallekampe[[col for col in shots_cols if(team) in col]].mean(axis=1)
            team_xg = dfsorteredeallekampe[[col for col in xg_cols if (team) in col]].mean(axis=1)
            team_duels = dfsorteredeallekampe[[col for col in duels_cols if (team) in col]].mean(axis=1)
            team_duelswon = dfsorteredeallekampe[[col for col in duelswon_cols if (team) in col]].mean(axis=1)
            team_possession = dfsorteredeallekampe[[col for col in possession_cols if (team) in col]].mean(axis=1)
            team_ppda = dfsorteredeallekampe[[col for col in ppda_cols if (team) in col]].mean(axis=1)

            team_data[team] = pd.concat([team_goals,team_shots, team_xg, team_duels,team_duelswon,team_possession,team_ppda], axis=1)
            
        team_df = pd.concat(team_data, axis=0, keys=team_data.keys())
        team_df.columns = ['Goals','Shots', 'Xg', 'Duels','Duels won','Possession %','PPDA']
        team_df = team_df.groupby(level=0).mean()
        team_df= team_df.round(decimals=2)


        forward_passes_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.forwardPasses')]
        forward_passes_successful_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.forwardPassesSuccessful')]
        passes_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.passes')]
        touches_in_box_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.touchesInBox')]
        xg_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.xg')]
        xgpershot_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.xgPerShot')]
        dzshots_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.shotsFromDangerZone')]
        possessionantal_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.possessionNumber')]
        possessionanmodstandershalvdel_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.reachingOpponentHalf')]
        possessionanmodstandersfelt_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.reachingOpponentBox')]
        challenge_intensity_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.challengeIntensity')]
        recoveries_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.recoveriesTotal')]
        opponenthalfrecoveries_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.opponentHalfRecoveries')]
        ppda_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.ppda')]

        # Create a new dataframe with the average values for each team
        team_data_målbare_alle = {}
        for team in set([col.split('.')[1] for col in shots_cols]):
            team_forward_passes = dfsorteredeallekampe[[col for col in forward_passes_cols if(team) in col]].mean(axis=1)    
            team_forward_passes_successful = dfsorteredeallekampe[[col for col in forward_passes_successful_cols if(team) in col]].mean(axis=1)
            team_passes = dfsorteredeallekampe[[col for col in passes_cols if (team) in col]].mean(axis=1)
            team_touches_in_box = dfsorteredeallekampe[[col for col in touches_in_box_cols if (team) in col]].mean(axis=1)
            team_xg = dfsorteredeallekampe[[col for col in xg_cols if (team) in col]].mean(axis=1)
            team_xgpershot = dfsorteredeallekampe[[col for col in xgpershot_cols if (team) in col]].mean(axis=1)
            team_dzshots = dfsorteredeallekampe[[col for col in dzshots_cols if (team) in col]].mean(axis=1)
            team_possessionantal = dfsorteredeallekampe[[col for col in possessionantal_cols if (team) in col]].mean(axis=1)
            team_possessionmodstandershalvdel = dfsorteredeallekampe[[col for col in possessionanmodstandershalvdel_cols if (team) in col]].mean(axis=1)
            team_possessionmodstandersfelt = dfsorteredeallekampe[[col for col in possessionanmodstandersfelt_cols if (team) in col]].mean(axis=1)
            team_challenge_intensity = dfsorteredeallekampe[[col for col in challenge_intensity_cols if (team) in col]].mean(axis=1)
            team_recoveries = dfsorteredeallekampe[[col for col in recoveries_cols if (team) in col]].mean(axis=1)
            team_opponenthalfrecoveries = dfsorteredeallekampe[[col for col in opponenthalfrecoveries_cols if (team) in col]].mean(axis=1)

            team_ppda = dfsorteredeallekampe[[col for col in ppda_cols if (team) in col]].mean(axis=1)

            team_data_målbare_alle[team] = pd.concat([team_forward_passes,team_forward_passes_successful, team_passes, team_touches_in_box,team_xg,team_xgpershot,team_dzshots,team_possessionantal,team_possessionmodstandershalvdel,team_possessionmodstandersfelt,team_challenge_intensity,team_recoveries,team_opponenthalfrecoveries,team_ppda], axis=1)
            
        team_df_målbare_alle = pd.concat(team_data_målbare_alle, axis=0, keys=team_data_målbare_alle.keys())
        team_df_målbare_alle.columns = ['Forward passes','Forward passes successful', 'Passes', 'Touches in box','xG','xG/shot','Dangerzone shots','Antal possessions','Antal possessions der når modstanders halvdel','Antal possessions der når modstanders felt','Challenge intensity','Recoveries','Opp half recoveries','PPDA']
        team_df_målbare_alle = team_df_målbare_alle.groupby(level=0).mean()
        team_df_målbare_alle['Forward pass %'] = (team_df_målbare_alle['Forward passes successful']/team_df_målbare_alle['Forward passes'])*100
        team_df_målbare_alle['Forward pass share'] = (team_df_målbare_alle['Forward passes']/team_df_målbare_alle['Passes'])*100
        team_df_målbare_alle['Forward pass score'] = team_df_målbare_alle[['Forward pass share','Forward pass %']].mean(axis=1)
        team_df_målbare_alle['Possession to opp box'] = team_df_målbare_alle['Antal possessions der når modstanders felt']
        team_df_målbare_alle['Possession to opp half %'] = (team_df_målbare_alle['Antal possessions der når modstanders halvdel']/team_df_målbare_alle['Antal possessions'])*100
        team_df_målbare_alle['Possession to opp box %'] = (team_df_målbare_alle['Antal possessions der når modstanders felt']/team_df_målbare_alle['Antal possessions'])*100
        team_df_målbare_alle = team_df_målbare_alle[['Forward pass score','Touches in box','xG','xG/shot','Dangerzone shots','Possession to opp box','Possession to opp half %','Possession to opp box %','Challenge intensity','Recoveries','Opp half recoveries','PPDA']]
        team_df_målbare_alle = team_df_målbare_alle.round(decimals=3)
        #hold = 'Horsens U15'
        #team_df_målbare_andre_hold = team_df_målbare.drop(hold)
        team_df_målbare_alle['xG against'] = team_df_målbare_alle['xG'].mean()
        team_df_målbare_alle['Danger zone shots against'] = team_df_målbare_alle['Dangerzone shots'].mean()
        team_df_målbare_alle['Touches in box against'] = team_df_målbare_alle['Touches in box'].mean()
        team_df_målbare_alle['Duels won %'] = (team_df['Duels won']/team_df['Duels'])*100
        team_df_målbare_alle = team_df_målbare_alle.round(decimals=2)
        Benchmark = team_df_målbare_alle.mean(axis=0)
        team_df_målbare_alle.loc['Liga Gennemsnit'] = Benchmark
        mask = team_df_målbare_alle.index.str.contains('Liga Gennemsnit')
        team_df_målbare_alle = team_df_målbare_alle[mask]


        df = pd.read_csv('Teamsheet alle kampe U15 sidste sæson.csv')

        dfsorteredekampesidstesæson = df.iloc[: , 1:]
        dfsorteredekampesidstesæson['date'] = dfsorteredekampesidstesæson['date'].astype(str)
        dfsorteredekampesidstesæson['date'] = dfsorteredekampesidstesæson['date'].str.replace(r'\sGMT.*$', '', regex=True)
        dfsorteredekampesidstesæson['date'] = pd.to_datetime(dfsorteredekampesidstesæson['date'], format="%B %d, %Y at %I:%M:%S %p")
        dfsorteredekampesidstesæson['date'] = dfsorteredekampesidstesæson['date'].dt.strftime('%d-%m-%Y')
        dfsorteredekampesidstesæson = dfsorteredekampesidstesæson.transpose()
        dfoverskrifter = dfsorteredekampesidstesæson[:2]
        dfsorteredekampesidstesæson = dfsorteredekampesidstesæson[2:].apply(pd.to_numeric, errors='coerce')
        dfsorteredekampesidstesæson = pd.concat([dfoverskrifter,dfsorteredekampesidstesæson])
        dfsorteredekampesidstesæson = dfsorteredekampesidstesæson.dropna(how='all')
        dfsorteredekampesidstesæson = dfsorteredekampesidstesæson.rename_axis('Parameter').astype(str)
        dfsorteredekampesidstesæson = dfsorteredekampesidstesæson.transpose()


        goals_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.goals')]
        shots_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.shots')]
        xg_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.xg')]
        duels_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.duels')]
        duelswon_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.duelsSuccessful')]
        possession_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.possessionPercent')]
        ppda_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.ppda')]

        # Create a new dataframe with the average values for each team
        team_data_sidstesæson = {}
        for team in set([col.split('.')[1] for col in shots_cols]):
            team_goals = dfsorteredekampesidstesæson[[col for col in goals_cols if(team) in col]].mean(axis=1)    
            team_shots = dfsorteredekampesidstesæson[[col for col in shots_cols if(team) in col]].mean(axis=1)
            team_xg = dfsorteredekampesidstesæson[[col for col in xg_cols if (team) in col]].mean(axis=1)
            team_duels = dfsorteredekampesidstesæson[[col for col in duels_cols if (team) in col]].mean(axis=1)
            team_duelswon = dfsorteredekampesidstesæson[[col for col in duelswon_cols if (team) in col]].mean(axis=1)
            team_possession = dfsorteredekampesidstesæson[[col for col in possession_cols if (team) in col]].mean(axis=1)
            team_ppda = dfsorteredekampesidstesæson[[col for col in ppda_cols if (team) in col]].mean(axis=1)

            team_data_sidstesæson[team] = pd.concat([team_goals,team_shots, team_xg, team_duels,team_duelswon,team_possession,team_ppda], axis=1)
            
        team_df_sidstesæson = pd.concat(team_data_sidstesæson, axis=0, keys=team_data_sidstesæson.keys())
        team_df_sidstesæson.columns = ['Goals','Shots', 'Xg', 'Duels','Duels won','Possession %','PPDA']
        team_df_sidstesæson = team_df_sidstesæson.groupby(level=0).mean()


        team_df_sidstesæson= team_df_sidstesæson.round(decimals=2)


        forward_passes_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.forwardPasses')]
        forward_passes_successful_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.forwardPassesSuccessful')]
        passes_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.passes')]
        touches_in_box_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.touchesInBox')]
        xg_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.xg')]
        xgpershot_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.xgPerShot')]
        dzshots_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.shotsFromDangerZone')]
        possessionantal_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.possessionNumber')]
        possessionanmodstandershalvdel_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.reachingOpponentHalf')]
        possessionanmodstandersfelt_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.reachingOpponentBox')]
        challenge_intensity_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.challengeIntensity')]
        recoveries_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.recoveriesTotal')]
        opponenthalfrecoveries_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.opponentHalfRecoveries')]
        ppda_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.ppda')]

        # Create a new dataframe with the average values for each team
        team_data_målbare_sidstesæson = {}
        for team in set([col.split('.')[1] for col in shots_cols]):
            team_forward_passes = dfsorteredekampesidstesæson[[col for col in forward_passes_cols if(team) in col]].mean(axis=1)    
            team_forward_passes_successful = dfsorteredekampesidstesæson[[col for col in forward_passes_successful_cols if(team) in col]].mean(axis=1)
            team_passes = dfsorteredekampesidstesæson[[col for col in passes_cols if (team) in col]].mean(axis=1)
            team_touches_in_box = dfsorteredekampesidstesæson[[col for col in touches_in_box_cols if (team) in col]].mean(axis=1)
            team_xg = dfsorteredekampesidstesæson[[col for col in xg_cols if (team) in col]].mean(axis=1)
            team_xgpershot = dfsorteredekampesidstesæson[[col for col in xgpershot_cols if (team) in col]].mean(axis=1)
            team_dzshots = dfsorteredekampesidstesæson[[col for col in dzshots_cols if (team) in col]].mean(axis=1)
            team_possessionantal = dfsorteredekampesidstesæson[[col for col in possessionantal_cols if (team) in col]].mean(axis=1)
            team_possessionmodstandershalvdel = dfsorteredekampesidstesæson[[col for col in possessionanmodstandershalvdel_cols if (team) in col]].mean(axis=1)
            team_possessionmodstandersfelt = dfsorteredekampesidstesæson[[col for col in possessionanmodstandersfelt_cols if (team) in col]].mean(axis=1)
            team_challenge_intensity = dfsorteredekampesidstesæson[[col for col in challenge_intensity_cols if (team) in col]].mean(axis=1)
            team_recoveries = dfsorteredekampesidstesæson[[col for col in recoveries_cols if (team) in col]].mean(axis=1)
            team_opponenthalfrecoveries = dfsorteredekampesidstesæson[[col for col in opponenthalfrecoveries_cols if (team) in col]].mean(axis=1)

            team_ppda = dfsorteredekampesidstesæson[[col for col in ppda_cols if (team) in col]].mean(axis=1)

            team_data_målbare_sidstesæson[team] = pd.concat([team_forward_passes,team_forward_passes_successful, team_passes, team_touches_in_box,team_xg,team_xgpershot,team_dzshots,team_possessionantal,team_possessionmodstandershalvdel,team_possessionmodstandersfelt,team_challenge_intensity,team_recoveries,team_opponenthalfrecoveries,team_ppda], axis=1)
            
        team_df_målbaresidstesæson = pd.concat(team_data_målbare_sidstesæson, axis=0, keys=team_data_målbare_sidstesæson.keys())
        team_df_målbaresidstesæson.columns = ['Forward passes','Forward passes successful', 'Passes', 'Touches in box','xG','xG/shot','Dangerzone shots','Antal possessions','Antal possessions der når modstanders halvdel','Antal possessions der når modstanders felt','Challenge intensity','Recoveries','Opp half recoveries','PPDA']
        team_df_målbaresidstesæson = team_df_målbaresidstesæson.groupby(level=0).mean()
        team_df_målbaresidstesæson['Forward pass %'] = (team_df_målbaresidstesæson['Forward passes successful']/team_df_målbaresidstesæson['Forward passes'])*100
        team_df_målbaresidstesæson['Forward pass share'] = (team_df_målbaresidstesæson['Forward passes']/team_df_målbaresidstesæson['Passes'])*100
        team_df_målbaresidstesæson['Forward pass score'] = team_df_målbaresidstesæson[['Forward pass share','Forward pass %']].mean(axis=1)
        team_df_målbaresidstesæson['Possession to opp box'] = team_df_målbaresidstesæson['Antal possessions der når modstanders felt']
        team_df_målbaresidstesæson['Possession to opp half %'] = (team_df_målbaresidstesæson['Antal possessions der når modstanders halvdel']/team_df_målbaresidstesæson['Antal possessions'])*100
        team_df_målbaresidstesæson['Possession to opp box %'] = (team_df_målbaresidstesæson['Antal possessions der når modstanders felt']/team_df_målbaresidstesæson['Antal possessions'])*100
        team_df_målbaresidstesæson = team_df_målbaresidstesæson[['Forward pass score','Touches in box','xG','xG/shot','Dangerzone shots','Possession to opp box','Possession to opp half %','Possession to opp box %','Challenge intensity','Recoveries','Opp half recoveries','PPDA']]
        team_df_målbaresidstesæson = team_df_målbaresidstesæson.round(decimals=3)

        team_df_målbaresidstesæson['xG against'] = team_df_målbaresidstesæson['xG'].mean()
        team_df_målbaresidstesæson['Danger zone shots against'] = team_df_målbaresidstesæson['Dangerzone shots'].mean()
        team_df_målbaresidstesæson['Touches in box against'] = team_df_målbaresidstesæson['Touches in box'].mean()
        team_df_målbaresidstesæson['Duels won %'] = (team_df_sidstesæson['Duels won']/team_df_sidstesæson['Duels'])*100
        mask = team_df_målbaresidstesæson.index.str.contains('Horsens')
        team_df_målbaresidstesæson = team_df_målbaresidstesæson[mask]
        team_df_målbaresidstesæson = team_df_målbaresidstesæson.round(decimals=2)
        frames = [team_df_målbare_alle,team_df_målbare,team_df_målbaresidstesæson]
        Benchmark = pd.concat(frames)
        st.dataframe(Benchmark)
        import plotly.graph_objs as go
        import numpy as np
        from plotly.subplots import make_subplots

        trace1 = go.Indicator(mode="gauge+number",    value=Benchmark['Forward pass score'][1],domain={'row' : 1, 'column' : 1},title={'text': "Forward pass score"},gauge={'axis':{'range':[Benchmark['Forward pass score'][2],Benchmark['Forward pass score'][0]]},})
        trace2 = go.Indicator(mode="gauge+number",    value=Benchmark['Touches in box'][1],domain={'row' : 1, 'column' : 2},title={'text': "Touches in box"},gauge={'axis':{'range':[Benchmark['Touches in box'][2],Benchmark['Touches in box'][0]]},})
        trace3 = go.Indicator(mode="gauge+number",    value=Benchmark['xG'][1],domain={'row' : 1, 'column' : 3},title={'text': "xG"},gauge={'axis':{'range':[Benchmark['xG'][2],Benchmark['xG'][0]]},})
        trace4 = go.Indicator(mode="gauge+number",    value=Benchmark['xG/shot'][1],domain={'row' : 1, 'column' : 4},title={'text': "xG/shot"},gauge={'axis':{'range':[Benchmark['xG/shot'][2],Benchmark['xG/shot'][0]]},'steps':[{'range':[0,Benchmark['xG/shot'][2]],'color':'red'}]})
        trace5 = go.Indicator(mode="gauge+number",    value=Benchmark['Dangerzone shots'][1],domain={'row' : 2, 'column' : 1},title={'text': "Dangerzone shots"},gauge={'axis':{'range':[Benchmark['Dangerzone shots'][2],Benchmark['Dangerzone shots'][0]]},})
        trace6 = go.Indicator(mode="gauge+number",    value=Benchmark['Possession to opp box'][1],domain={'row' : 2, 'column' : 2},title={'text': "Possession to opp box"},gauge={'axis':{'range':[Benchmark['Possession to opp box'][2],Benchmark['Possession to opp box'][0]]},})
        trace7 = go.Indicator(mode="gauge+number",    value=Benchmark['Possession to opp half %'][1],domain={'row' : 2, 'column' : 3},title={'text': "Possession to opp half %"},gauge={'axis':{'range':[Benchmark['Possession to opp half %'][2],Benchmark['Possession to opp half %'][0]]},})
        trace8 = go.Indicator(mode="gauge+number",    value=Benchmark['Possession to opp box %'][1],domain={'row' : 2, 'column' : 4},title={'text': "Possession to opp box %"},gauge={'axis':{'range':[Benchmark['Possession to opp box %'][2],Benchmark['Possession to opp box %'][0]]},})
        
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
        
        trace9 = go.Indicator(mode="gauge+number",    value=Benchmark['xG against'][1],domain={'row' : 1, 'column' : 1},title={'text': "xG against"},gauge={'axis':{'range':[Benchmark['xG against'][2],Benchmark['xG against'][0]]}})
        trace10 = go.Indicator(mode="gauge+number",    value=Benchmark['PPDA'][1],domain={'row' : 1, 'column' : 2},title={'text': "PPDA"},gauge={'axis':{'range':[Benchmark['PPDA'][2],Benchmark['PPDA'][0]]}})
        trace11 = go.Indicator(mode="gauge+number",    value=Benchmark['Danger zone shots against'][1],domain={'row' : 1, 'column' : 3},title={'text': "Danger zone shots against"},gauge={'axis':{'range':[Benchmark['Danger zone shots against'][2],Benchmark['Danger zone shots against'][0]]}})
        trace12 = go.Indicator(mode="gauge+number",    value=Benchmark['Challenge intensity'][1],domain={'row' : 1, 'column' : 4},title={'text': "Challenge intensity"},gauge={'axis':{'range':[Benchmark['Challenge intensity'][2],Benchmark['Challenge intensity'][0]]}})
        trace13 = go.Indicator(mode="gauge+number",    value=Benchmark['Recoveries'][1],domain={'row' : 2, 'column' : 1},title={'text': "Recoveries"},gauge={'axis':{'range':[Benchmark['Recoveries'][2],Benchmark['Recoveries'][0]]}})
        trace14 = go.Indicator(mode="gauge+number",    value=Benchmark['Opp half recoveries'][1],domain={'row' : 2, 'column' : 2},title={'text': "Opp half recoveries"},gauge={'axis':{'range':[Benchmark['Opp half recoveries'][2],Benchmark['Opp half recoveries'][0]]}})
        trace15 = go.Indicator(mode="gauge+number",    value=Benchmark['Touches in box against'][1],domain={'row' : 2, 'column' : 3},title={'text': "Touches in box against"},gauge={'axis':{'range':[Benchmark['Touches in box against'][2],Benchmark['Touches in box against'][0]]}})
        trace16 = go.Indicator(mode="gauge+number",    value=Benchmark['Duels won %'][1],domain={'row' : 2, 'column' : 4},title={'text': "Duels won %"},gauge={'axis':{'range':[Benchmark['Duels won %'][2],Benchmark['Duels won %'][0]]}})
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
        
        
    def U17():
        import pandas as pd
        import csv
        import streamlit as st
        import numpy as np
        from datetime import datetime
        df = pd.read_csv('Teamsheet egne kampe U17.csv')
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
        team_df= team_df.round(decimals=2)
        st.dataframe(team_df)

        forward_passes_cols = [col for col in dfsorteredekampe.columns if col.endswith('.forwardPasses')]
        forward_passes_successful_cols = [col for col in dfsorteredekampe.columns if col.endswith('.forwardPassesSuccessful')]
        passes_cols = [col for col in dfsorteredekampe.columns if col.endswith('.passes')]
        touches_in_box_cols = [col for col in dfsorteredekampe.columns if col.endswith('.touchesInBox')]
        xg_cols = [col for col in dfsorteredekampe.columns if col.endswith('.xg')]
        xgpershot_cols = [col for col in dfsorteredekampe.columns if col.endswith('.xgPerShot')]
        dzshots_cols = [col for col in dfsorteredekampe.columns if col.endswith('.shotsFromDangerZone')]
        possessionantal_cols = [col for col in dfsorteredekampe.columns if col.endswith('.possessionNumber')]
        possessionanmodstandershalvdel_cols = [col for col in dfsorteredekampe.columns if col.endswith('.reachingOpponentHalf')]
        possessionanmodstandersfelt_cols = [col for col in dfsorteredekampe.columns if col.endswith('.reachingOpponentBox')]
        challenge_intensity_cols = [col for col in dfsorteredekampe.columns if col.endswith('.challengeIntensity')]
        recoveries_cols = [col for col in dfsorteredekampe.columns if col.endswith('.recoveriesTotal')]
        opponenthalfrecoveries_cols = [col for col in dfsorteredekampe.columns if col.endswith('.opponentHalfRecoveries')]
        ppda_cols = [col for col in dfsorteredekampe.columns if col.endswith('.ppda')]

        # Create a new dataframe with the average values for each team
        team_data_målbare = {}
        for team in set([col.split('.')[1] for col in shots_cols]):
            team_forward_passes = dfsorteredekampe[[col for col in forward_passes_cols if(team) in col]].mean(axis=1)    
            team_forward_passes_successful = dfsorteredekampe[[col for col in forward_passes_successful_cols if(team) in col]].mean(axis=1)
            team_passes = dfsorteredekampe[[col for col in passes_cols if (team) in col]].mean(axis=1)
            team_touches_in_box = dfsorteredekampe[[col for col in touches_in_box_cols if (team) in col]].mean(axis=1)
            team_xg = dfsorteredekampe[[col for col in xg_cols if (team) in col]].mean(axis=1)
            team_xgpershot = dfsorteredekampe[[col for col in xgpershot_cols if (team) in col]].mean(axis=1)
            team_dzshots = dfsorteredekampe[[col for col in dzshots_cols if (team) in col]].mean(axis=1)
            team_possessionantal = dfsorteredekampe[[col for col in possessionantal_cols if (team) in col]].mean(axis=1)
            team_possessionmodstandershalvdel = dfsorteredekampe[[col for col in possessionanmodstandershalvdel_cols if (team) in col]].mean(axis=1)
            team_possessionmodstandersfelt = dfsorteredekampe[[col for col in possessionanmodstandersfelt_cols if (team) in col]].mean(axis=1)
            team_challenge_intensity = dfsorteredekampe[[col for col in challenge_intensity_cols if (team) in col]].mean(axis=1)
            team_recoveries = dfsorteredekampe[[col for col in recoveries_cols if (team) in col]].mean(axis=1)
            team_opponenthalfrecoveries = dfsorteredekampe[[col for col in opponenthalfrecoveries_cols if (team) in col]].mean(axis=1)

            team_ppda = dfsorteredekampe[[col for col in ppda_cols if (team) in col]].mean(axis=1)

            team_data_målbare[team] = pd.concat([team_forward_passes,team_forward_passes_successful, team_passes, team_touches_in_box,team_xg,team_xgpershot,team_dzshots,team_possessionantal,team_possessionmodstandershalvdel,team_possessionmodstandersfelt,team_challenge_intensity,team_recoveries,team_opponenthalfrecoveries,team_ppda], axis=1)
            
        team_df_målbare = pd.concat(team_data_målbare, axis=0, keys=team_data_målbare.keys())
        team_df_målbare.columns = ['Forward passes','Forward passes successful', 'Passes', 'Touches in box','xG','xG/shot','Dangerzone shots','Antal possessions','Antal possessions der når modstanders halvdel','Antal possessions der når modstanders felt','Challenge intensity','Recoveries','Opp half recoveries','PPDA']
        team_df_målbare = team_df_målbare.groupby(level=0).mean()
        team_df_målbare['Forward pass %'] = (team_df_målbare['Forward passes successful']/team_df_målbare['Forward passes'])*100
        team_df_målbare['Forward pass share'] = (team_df_målbare['Forward passes']/team_df_målbare['Passes'])*100
        team_df_målbare['Forward pass score'] = team_df_målbare[['Forward pass share','Forward pass %']].mean(axis=1)
        team_df_målbare['Possession to opp box'] = team_df_målbare['Antal possessions der når modstanders felt']
        team_df_målbare['Possession to opp half %'] = (team_df_målbare['Antal possessions der når modstanders halvdel']/team_df_målbare['Antal possessions'])*100
        team_df_målbare['Possession to opp box %'] = (team_df_målbare['Antal possessions der når modstanders felt']/team_df_målbare['Antal possessions'])*100
        team_df_målbare = team_df_målbare[['Forward pass score','Touches in box','xG','xG/shot','Dangerzone shots','Possession to opp box','Possession to opp half %','Possession to opp box %','Challenge intensity','Recoveries','Opp half recoveries','PPDA']]
        team_df_målbare = team_df_målbare.round(decimals=3)
        hold = 'Horsens U17'
        team_df_målbare_andre_hold = team_df_målbare.drop(hold)
        team_df_målbare['xG against'] = team_df_målbare_andre_hold['xG'].mean()
        team_df_målbare['Danger zone shots against'] = team_df_målbare_andre_hold['Dangerzone shots'].mean()
        team_df_målbare['Touches in box against'] = team_df_målbare_andre_hold['Touches in box'].mean()
        team_df_målbare['Duels won %'] = (team_df['Duels won']/team_df['Duels'])*100
        mask = team_df_målbare.index.str.contains('Horsens')
        team_df_målbare = team_df_målbare[mask]
        team_df_målbare = team_df_målbare.round(decimals=2)

        import pandas as pd
        import csv
        import streamlit as st
        import numpy as np
        from datetime import datetime

        df = pd.read_csv('Teamsheet alle kampe U17.csv')

        dfsorteredeallekampe = df.iloc[: , 1:]
        dfsorteredeallekampe['date'] = dfsorteredeallekampe['date'].astype(str)
        dfsorteredeallekampe['date'] = dfsorteredeallekampe['date'].str.replace(r'\sGMT.*$', '', regex=True)
        dfsorteredeallekampe['date'] = pd.to_datetime(dfsorteredeallekampe['date'], format="%B %d, %Y at %I:%M:%S %p")
        dfsorteredeallekampe['date'] = dfsorteredeallekampe['date'].dt.strftime('%d-%m-%Y')
        dfsorteredeallekampe = dfsorteredeallekampe.transpose()
        dfoverskrifter = dfsorteredeallekampe[:2]
        dfsorteredeallekampe = dfsorteredeallekampe[2:].apply(pd.to_numeric, errors='coerce')
        dfsorteredeallekampe = pd.concat([dfoverskrifter,dfsorteredeallekampe])
        dfsorteredeallekampe = dfsorteredeallekampe.dropna(how='all')
        dfsorteredeallekampe = dfsorteredeallekampe.rename_axis('Parameter').astype(str)
        dfsorteredeallekampe = dfsorteredeallekampe.transpose()


        goals_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.goals')]
        shots_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.shots')]
        xg_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.xg')]
        duels_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.duels')]
        duelswon_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.duelsSuccessful')]
        possession_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.possessionPercent')]
        ppda_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.ppda')]

        # Create a new dataframe with the average values for each team
        team_data = {}
        for team in set([col.split('.')[1] for col in shots_cols]):
            team_goals = dfsorteredeallekampe[[col for col in goals_cols if(team) in col]].mean(axis=1)    
            team_shots = dfsorteredeallekampe[[col for col in shots_cols if(team) in col]].mean(axis=1)
            team_xg = dfsorteredeallekampe[[col for col in xg_cols if (team) in col]].mean(axis=1)
            team_duels = dfsorteredeallekampe[[col for col in duels_cols if (team) in col]].mean(axis=1)
            team_duelswon = dfsorteredeallekampe[[col for col in duelswon_cols if (team) in col]].mean(axis=1)
            team_possession = dfsorteredeallekampe[[col for col in possession_cols if (team) in col]].mean(axis=1)
            team_ppda = dfsorteredeallekampe[[col for col in ppda_cols if (team) in col]].mean(axis=1)

            team_data[team] = pd.concat([team_goals,team_shots, team_xg, team_duels,team_duelswon,team_possession,team_ppda], axis=1)
            
        team_df = pd.concat(team_data, axis=0, keys=team_data.keys())
        team_df.columns = ['Goals','Shots', 'Xg', 'Duels','Duels won','Possession %','PPDA']
        team_df = team_df.groupby(level=0).mean()
        team_df= team_df.round(decimals=2)


        forward_passes_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.forwardPasses')]
        forward_passes_successful_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.forwardPassesSuccessful')]
        passes_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.passes')]
        touches_in_box_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.touchesInBox')]
        xg_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.xg')]
        xgpershot_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.xgPerShot')]
        dzshots_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.shotsFromDangerZone')]
        possessionantal_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.possessionNumber')]
        possessionanmodstandershalvdel_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.reachingOpponentHalf')]
        possessionanmodstandersfelt_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.reachingOpponentBox')]
        challenge_intensity_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.challengeIntensity')]
        recoveries_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.recoveriesTotal')]
        opponenthalfrecoveries_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.opponentHalfRecoveries')]
        ppda_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.ppda')]

        # Create a new dataframe with the average values for each team
        team_data_målbare_alle = {}
        for team in set([col.split('.')[1] for col in shots_cols]):
            team_forward_passes = dfsorteredeallekampe[[col for col in forward_passes_cols if(team) in col]].mean(axis=1)    
            team_forward_passes_successful = dfsorteredeallekampe[[col for col in forward_passes_successful_cols if(team) in col]].mean(axis=1)
            team_passes = dfsorteredeallekampe[[col for col in passes_cols if (team) in col]].mean(axis=1)
            team_touches_in_box = dfsorteredeallekampe[[col for col in touches_in_box_cols if (team) in col]].mean(axis=1)
            team_xg = dfsorteredeallekampe[[col for col in xg_cols if (team) in col]].mean(axis=1)
            team_xgpershot = dfsorteredeallekampe[[col for col in xgpershot_cols if (team) in col]].mean(axis=1)
            team_dzshots = dfsorteredeallekampe[[col for col in dzshots_cols if (team) in col]].mean(axis=1)
            team_possessionantal = dfsorteredeallekampe[[col for col in possessionantal_cols if (team) in col]].mean(axis=1)
            team_possessionmodstandershalvdel = dfsorteredeallekampe[[col for col in possessionanmodstandershalvdel_cols if (team) in col]].mean(axis=1)
            team_possessionmodstandersfelt = dfsorteredeallekampe[[col for col in possessionanmodstandersfelt_cols if (team) in col]].mean(axis=1)
            team_challenge_intensity = dfsorteredeallekampe[[col for col in challenge_intensity_cols if (team) in col]].mean(axis=1)
            team_recoveries = dfsorteredeallekampe[[col for col in recoveries_cols if (team) in col]].mean(axis=1)
            team_opponenthalfrecoveries = dfsorteredeallekampe[[col for col in opponenthalfrecoveries_cols if (team) in col]].mean(axis=1)

            team_ppda = dfsorteredeallekampe[[col for col in ppda_cols if (team) in col]].mean(axis=1)

            team_data_målbare_alle[team] = pd.concat([team_forward_passes,team_forward_passes_successful, team_passes, team_touches_in_box,team_xg,team_xgpershot,team_dzshots,team_possessionantal,team_possessionmodstandershalvdel,team_possessionmodstandersfelt,team_challenge_intensity,team_recoveries,team_opponenthalfrecoveries,team_ppda], axis=1)
            
        team_df_målbare_alle = pd.concat(team_data_målbare_alle, axis=0, keys=team_data_målbare_alle.keys())
        team_df_målbare_alle.columns = ['Forward passes','Forward passes successful', 'Passes', 'Touches in box','xG','xG/shot','Dangerzone shots','Antal possessions','Antal possessions der når modstanders halvdel','Antal possessions der når modstanders felt','Challenge intensity','Recoveries','Opp half recoveries','PPDA']
        team_df_målbare_alle = team_df_målbare_alle.groupby(level=0).mean()
        team_df_målbare_alle['Forward pass %'] = (team_df_målbare_alle['Forward passes successful']/team_df_målbare_alle['Forward passes'])*100
        team_df_målbare_alle['Forward pass share'] = (team_df_målbare_alle['Forward passes']/team_df_målbare_alle['Passes'])*100
        team_df_målbare_alle['Forward pass score'] = team_df_målbare_alle[['Forward pass share','Forward pass %']].mean(axis=1)
        team_df_målbare_alle['Possession to opp box'] = team_df_målbare_alle['Antal possessions der når modstanders felt']
        team_df_målbare_alle['Possession to opp half %'] = (team_df_målbare_alle['Antal possessions der når modstanders halvdel']/team_df_målbare_alle['Antal possessions'])*100
        team_df_målbare_alle['Possession to opp box %'] = (team_df_målbare_alle['Antal possessions der når modstanders felt']/team_df_målbare_alle['Antal possessions'])*100
        team_df_målbare_alle = team_df_målbare_alle[['Forward pass score','Touches in box','xG','xG/shot','Dangerzone shots','Possession to opp box','Possession to opp half %','Possession to opp box %','Challenge intensity','Recoveries','Opp half recoveries','PPDA']]
        team_df_målbare_alle = team_df_målbare_alle.round(decimals=3)
        #hold = 'Horsens U15'
        #team_df_målbare_andre_hold = team_df_målbare.drop(hold)
        team_df_målbare_alle['xG against'] = team_df_målbare_alle['xG'].mean()
        team_df_målbare_alle['Danger zone shots against'] = team_df_målbare_alle['Dangerzone shots'].mean()
        team_df_målbare_alle['Touches in box against'] = team_df_målbare_alle['Touches in box'].mean()
        team_df_målbare_alle['Duels won %'] = (team_df['Duels won']/team_df['Duels'])*100
        team_df_målbare_alle = team_df_målbare_alle.round(decimals=2)
        Benchmark = team_df_målbare_alle.mean(axis=0)
        team_df_målbare_alle.loc['Liga Gennemsnit'] = Benchmark
        mask = team_df_målbare_alle.index.str.contains('Liga Gennemsnit')
        team_df_målbare_alle = team_df_målbare_alle[mask]


        df = pd.read_csv('Teamsheet alle kampe U17 sidste sæson.csv')

        dfsorteredekampesidstesæson = df.iloc[: , 1:]
        dfsorteredekampesidstesæson['date'] = dfsorteredekampesidstesæson['date'].astype(str)
        dfsorteredekampesidstesæson['date'] = dfsorteredekampesidstesæson['date'].str.replace(r'\sGMT.*$', '', regex=True)
        dfsorteredekampesidstesæson['date'] = pd.to_datetime(dfsorteredekampesidstesæson['date'], format="%B %d, %Y at %I:%M:%S %p")
        dfsorteredekampesidstesæson['date'] = dfsorteredekampesidstesæson['date'].dt.strftime('%d-%m-%Y')
        dfsorteredekampesidstesæson = dfsorteredekampesidstesæson.transpose()
        dfoverskrifter = dfsorteredekampesidstesæson[:2]
        dfsorteredekampesidstesæson = dfsorteredekampesidstesæson[2:].apply(pd.to_numeric, errors='coerce')
        dfsorteredekampesidstesæson = pd.concat([dfoverskrifter,dfsorteredekampesidstesæson])
        dfsorteredekampesidstesæson = dfsorteredekampesidstesæson.dropna(how='all')
        dfsorteredekampesidstesæson = dfsorteredekampesidstesæson.rename_axis('Parameter').astype(str)
        dfsorteredekampesidstesæson = dfsorteredekampesidstesæson.transpose()


        goals_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.goals')]
        shots_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.shots')]
        xg_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.xg')]
        duels_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.duels')]
        duelswon_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.duelsSuccessful')]
        possession_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.possessionPercent')]
        ppda_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.ppda')]

        # Create a new dataframe with the average values for each team
        team_data_sidstesæson = {}
        for team in set([col.split('.')[1] for col in shots_cols]):
            team_goals = dfsorteredekampesidstesæson[[col for col in goals_cols if(team) in col]].mean(axis=1)    
            team_shots = dfsorteredekampesidstesæson[[col for col in shots_cols if(team) in col]].mean(axis=1)
            team_xg = dfsorteredekampesidstesæson[[col for col in xg_cols if (team) in col]].mean(axis=1)
            team_duels = dfsorteredekampesidstesæson[[col for col in duels_cols if (team) in col]].mean(axis=1)
            team_duelswon = dfsorteredekampesidstesæson[[col for col in duelswon_cols if (team) in col]].mean(axis=1)
            team_possession = dfsorteredekampesidstesæson[[col for col in possession_cols if (team) in col]].mean(axis=1)
            team_ppda = dfsorteredekampesidstesæson[[col for col in ppda_cols if (team) in col]].mean(axis=1)

            team_data_sidstesæson[team] = pd.concat([team_goals,team_shots, team_xg, team_duels,team_duelswon,team_possession,team_ppda], axis=1)
            
        team_df_sidstesæson = pd.concat(team_data_sidstesæson, axis=0, keys=team_data_sidstesæson.keys())
        team_df_sidstesæson.columns = ['Goals','Shots', 'Xg', 'Duels','Duels won','Possession %','PPDA']
        team_df_sidstesæson = team_df_sidstesæson.groupby(level=0).mean()


        team_df_sidstesæson= team_df_sidstesæson.round(decimals=2)


        forward_passes_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.forwardPasses')]
        forward_passes_successful_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.forwardPassesSuccessful')]
        passes_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.passes')]
        touches_in_box_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.touchesInBox')]
        xg_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.xg')]
        xgpershot_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.xgPerShot')]
        dzshots_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.shotsFromDangerZone')]
        possessionantal_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.possessionNumber')]
        possessionanmodstandershalvdel_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.reachingOpponentHalf')]
        possessionanmodstandersfelt_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.reachingOpponentBox')]
        challenge_intensity_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.challengeIntensity')]
        recoveries_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.recoveriesTotal')]
        opponenthalfrecoveries_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.opponentHalfRecoveries')]
        ppda_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.ppda')]

        # Create a new dataframe with the average values for each team
        team_data_målbare_sidstesæson = {}
        for team in set([col.split('.')[1] for col in shots_cols]):
            team_forward_passes = dfsorteredekampesidstesæson[[col for col in forward_passes_cols if(team) in col]].mean(axis=1)    
            team_forward_passes_successful = dfsorteredekampesidstesæson[[col for col in forward_passes_successful_cols if(team) in col]].mean(axis=1)
            team_passes = dfsorteredekampesidstesæson[[col for col in passes_cols if (team) in col]].mean(axis=1)
            team_touches_in_box = dfsorteredekampesidstesæson[[col for col in touches_in_box_cols if (team) in col]].mean(axis=1)
            team_xg = dfsorteredekampesidstesæson[[col for col in xg_cols if (team) in col]].mean(axis=1)
            team_xgpershot = dfsorteredekampesidstesæson[[col for col in xgpershot_cols if (team) in col]].mean(axis=1)
            team_dzshots = dfsorteredekampesidstesæson[[col for col in dzshots_cols if (team) in col]].mean(axis=1)
            team_possessionantal = dfsorteredekampesidstesæson[[col for col in possessionantal_cols if (team) in col]].mean(axis=1)
            team_possessionmodstandershalvdel = dfsorteredekampesidstesæson[[col for col in possessionanmodstandershalvdel_cols if (team) in col]].mean(axis=1)
            team_possessionmodstandersfelt = dfsorteredekampesidstesæson[[col for col in possessionanmodstandersfelt_cols if (team) in col]].mean(axis=1)
            team_challenge_intensity = dfsorteredekampesidstesæson[[col for col in challenge_intensity_cols if (team) in col]].mean(axis=1)
            team_recoveries = dfsorteredekampesidstesæson[[col for col in recoveries_cols if (team) in col]].mean(axis=1)
            team_opponenthalfrecoveries = dfsorteredekampesidstesæson[[col for col in opponenthalfrecoveries_cols if (team) in col]].mean(axis=1)

            team_ppda = dfsorteredekampesidstesæson[[col for col in ppda_cols if (team) in col]].mean(axis=1)

            team_data_målbare_sidstesæson[team] = pd.concat([team_forward_passes,team_forward_passes_successful, team_passes, team_touches_in_box,team_xg,team_xgpershot,team_dzshots,team_possessionantal,team_possessionmodstandershalvdel,team_possessionmodstandersfelt,team_challenge_intensity,team_recoveries,team_opponenthalfrecoveries,team_ppda], axis=1)
            
        team_df_målbaresidstesæson = pd.concat(team_data_målbare_sidstesæson, axis=0, keys=team_data_målbare_sidstesæson.keys())
        team_df_målbaresidstesæson.columns = ['Forward passes','Forward passes successful', 'Passes', 'Touches in box','xG','xG/shot','Dangerzone shots','Antal possessions','Antal possessions der når modstanders halvdel','Antal possessions der når modstanders felt','Challenge intensity','Recoveries','Opp half recoveries','PPDA']
        team_df_målbaresidstesæson = team_df_målbaresidstesæson.groupby(level=0).mean()
        team_df_målbaresidstesæson['Forward pass %'] = (team_df_målbaresidstesæson['Forward passes successful']/team_df_målbaresidstesæson['Forward passes'])*100
        team_df_målbaresidstesæson['Forward pass share'] = (team_df_målbaresidstesæson['Forward passes']/team_df_målbaresidstesæson['Passes'])*100
        team_df_målbaresidstesæson['Forward pass score'] = team_df_målbaresidstesæson[['Forward pass share','Forward pass %']].mean(axis=1)
        team_df_målbaresidstesæson['Possession to opp box'] = team_df_målbaresidstesæson['Antal possessions der når modstanders felt']
        team_df_målbaresidstesæson['Possession to opp half %'] = (team_df_målbaresidstesæson['Antal possessions der når modstanders halvdel']/team_df_målbaresidstesæson['Antal possessions'])*100
        team_df_målbaresidstesæson['Possession to opp box %'] = (team_df_målbaresidstesæson['Antal possessions der når modstanders felt']/team_df_målbaresidstesæson['Antal possessions'])*100
        team_df_målbaresidstesæson = team_df_målbaresidstesæson[['Forward pass score','Touches in box','xG','xG/shot','Dangerzone shots','Possession to opp box','Possession to opp half %','Possession to opp box %','Challenge intensity','Recoveries','Opp half recoveries','PPDA']]
        team_df_målbaresidstesæson = team_df_målbaresidstesæson.round(decimals=3)

        team_df_målbaresidstesæson['xG against'] = team_df_målbaresidstesæson['xG'].mean()
        team_df_målbaresidstesæson['Danger zone shots against'] = team_df_målbaresidstesæson['Dangerzone shots'].mean()
        team_df_målbaresidstesæson['Touches in box against'] = team_df_målbaresidstesæson['Touches in box'].mean()
        team_df_målbaresidstesæson['Duels won %'] = (team_df_sidstesæson['Duels won']/team_df_sidstesæson['Duels'])*100
        mask = team_df_målbaresidstesæson.index.str.contains('Horsens')
        team_df_målbaresidstesæson = team_df_målbaresidstesæson[mask]
        team_df_målbaresidstesæson = team_df_målbaresidstesæson.round(decimals=2)
        frames = [team_df_målbare_alle,team_df_målbare,team_df_målbaresidstesæson]
        Benchmark = pd.concat(frames)
        st.dataframe(Benchmark)
        import plotly.graph_objs as go
        import numpy as np
        from plotly.subplots import make_subplots

        trace1 = go.Indicator(mode="gauge+number",    value=Benchmark['Forward pass score'][1],domain={'row' : 1, 'column' : 1},title={'text': "Forward pass score"},gauge={'axis':{'range':[Benchmark['Forward pass score'][2],Benchmark['Forward pass score'][0]]},})
        trace2 = go.Indicator(mode="gauge+number",    value=Benchmark['Touches in box'][1],domain={'row' : 1, 'column' : 2},title={'text': "Touches in box"},gauge={'axis':{'range':[Benchmark['Touches in box'][2],Benchmark['Touches in box'][0]]},})
        trace3 = go.Indicator(mode="gauge+number",    value=Benchmark['xG'][1],domain={'row' : 1, 'column' : 3},title={'text': "xG"},gauge={'axis':{'range':[Benchmark['xG'][2],Benchmark['xG'][0]]},})
        trace4 = go.Indicator(mode="gauge+number",    value=Benchmark['xG/shot'][1],domain={'row' : 1, 'column' : 4},title={'text': "xG/shot"},gauge={'axis':{'range':[Benchmark['xG/shot'][2],Benchmark['xG/shot'][0]]},'steps':[{'range':[0,Benchmark['xG/shot'][2]],'color':'red'}]})
        trace5 = go.Indicator(mode="gauge+number",    value=Benchmark['Dangerzone shots'][1],domain={'row' : 2, 'column' : 1},title={'text': "Dangerzone shots"},gauge={'axis':{'range':[Benchmark['Dangerzone shots'][2],Benchmark['Dangerzone shots'][0]]},})
        trace6 = go.Indicator(mode="gauge+number",    value=Benchmark['Possession to opp box'][1],domain={'row' : 2, 'column' : 2},title={'text': "Possession to opp box"},gauge={'axis':{'range':[Benchmark['Possession to opp box'][2],Benchmark['Possession to opp box'][0]]},})
        trace7 = go.Indicator(mode="gauge+number",    value=Benchmark['Possession to opp half %'][1],domain={'row' : 2, 'column' : 3},title={'text': "Possession to opp half %"},gauge={'axis':{'range':[Benchmark['Possession to opp half %'][2],Benchmark['Possession to opp half %'][0]]},})
        trace8 = go.Indicator(mode="gauge+number",    value=Benchmark['Possession to opp box %'][1],domain={'row' : 2, 'column' : 4},title={'text': "Possession to opp box %"},gauge={'axis':{'range':[Benchmark['Possession to opp box %'][2],Benchmark['Possession to opp box %'][0]]},})
        
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
        
        trace9 = go.Indicator(mode="gauge+number",    value=Benchmark['xG against'][1],domain={'row' : 1, 'column' : 1},title={'text': "xG against"},gauge={'axis':{'range':[Benchmark['xG against'][2],Benchmark['xG against'][0]]}})
        trace10 = go.Indicator(mode="gauge+number",    value=Benchmark['PPDA'][1],domain={'row' : 1, 'column' : 2},title={'text': "PPDA"},gauge={'axis':{'range':[Benchmark['PPDA'][2],Benchmark['PPDA'][0]]}})
        trace11 = go.Indicator(mode="gauge+number",    value=Benchmark['Danger zone shots against'][1],domain={'row' : 1, 'column' : 3},title={'text': "Danger zone shots against"},gauge={'axis':{'range':[Benchmark['Danger zone shots against'][2],Benchmark['Danger zone shots against'][0]]}})
        trace12 = go.Indicator(mode="gauge+number",    value=Benchmark['Challenge intensity'][1],domain={'row' : 1, 'column' : 4},title={'text': "Challenge intensity"},gauge={'axis':{'range':[Benchmark['Challenge intensity'][0],Benchmark['Challenge intensity'][2]]}})
        trace13 = go.Indicator(mode="gauge+number",    value=Benchmark['Recoveries'][1],domain={'row' : 2, 'column' : 1},title={'text': "Recoveries"},gauge={'axis':{'range':[Benchmark['Recoveries'][2],Benchmark['Recoveries'][0]]}})
        trace14 = go.Indicator(mode="gauge+number",    value=Benchmark['Opp half recoveries'][1],domain={'row' : 2, 'column' : 2},title={'text': "Opp half recoveries"},gauge={'axis':{'range':[Benchmark['Opp half recoveries'][2],Benchmark['Opp half recoveries'][0]]}})
        trace15 = go.Indicator(mode="gauge+number",    value=Benchmark['Touches in box against'][1],domain={'row' : 2, 'column' : 3},title={'text': "Touches in box against"},gauge={'axis':{'range':[Benchmark['Touches in box against'][2],Benchmark['Touches in box against'][0]]}})
        trace16 = go.Indicator(mode="gauge+number",    value=Benchmark['Duels won %'][1],domain={'row' : 2, 'column' : 4},title={'text': "Duels won %"},gauge={'axis':{'range':[Benchmark['Duels won %'][2],Benchmark['Duels won %'][0]]}})
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
        
    def U19():
        import pandas as pd
        import csv
        import streamlit as st
        import numpy as np
        from datetime import datetime
        df = pd.read_csv('Teamsheet egne kampe U19.csv')
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
        team_df= team_df.round(decimals=2)
        st.dataframe(team_df)

        forward_passes_cols = [col for col in dfsorteredekampe.columns if col.endswith('.forwardPasses')]
        forward_passes_successful_cols = [col for col in dfsorteredekampe.columns if col.endswith('.forwardPassesSuccessful')]
        passes_cols = [col for col in dfsorteredekampe.columns if col.endswith('.passes')]
        touches_in_box_cols = [col for col in dfsorteredekampe.columns if col.endswith('.touchesInBox')]
        xg_cols = [col for col in dfsorteredekampe.columns if col.endswith('.xg')]
        xgpershot_cols = [col for col in dfsorteredekampe.columns if col.endswith('.xgPerShot')]
        dzshots_cols = [col for col in dfsorteredekampe.columns if col.endswith('.shotsFromDangerZone')]
        possessionantal_cols = [col for col in dfsorteredekampe.columns if col.endswith('.possessionNumber')]
        possessionanmodstandershalvdel_cols = [col for col in dfsorteredekampe.columns if col.endswith('.reachingOpponentHalf')]
        possessionanmodstandersfelt_cols = [col for col in dfsorteredekampe.columns if col.endswith('.reachingOpponentBox')]
        challenge_intensity_cols = [col for col in dfsorteredekampe.columns if col.endswith('.challengeIntensity')]
        recoveries_cols = [col for col in dfsorteredekampe.columns if col.endswith('.recoveriesTotal')]
        opponenthalfrecoveries_cols = [col for col in dfsorteredekampe.columns if col.endswith('.opponentHalfRecoveries')]
        ppda_cols = [col for col in dfsorteredekampe.columns if col.endswith('.ppda')]

        # Create a new dataframe with the average values for each team
        team_data_målbare = {}
        for team in set([col.split('.')[1] for col in shots_cols]):
            team_forward_passes = dfsorteredekampe[[col for col in forward_passes_cols if(team) in col]].mean(axis=1)    
            team_forward_passes_successful = dfsorteredekampe[[col for col in forward_passes_successful_cols if(team) in col]].mean(axis=1)
            team_passes = dfsorteredekampe[[col for col in passes_cols if (team) in col]].mean(axis=1)
            team_touches_in_box = dfsorteredekampe[[col for col in touches_in_box_cols if (team) in col]].mean(axis=1)
            team_xg = dfsorteredekampe[[col for col in xg_cols if (team) in col]].mean(axis=1)
            team_xgpershot = dfsorteredekampe[[col for col in xgpershot_cols if (team) in col]].mean(axis=1)
            team_dzshots = dfsorteredekampe[[col for col in dzshots_cols if (team) in col]].mean(axis=1)
            team_possessionantal = dfsorteredekampe[[col for col in possessionantal_cols if (team) in col]].mean(axis=1)
            team_possessionmodstandershalvdel = dfsorteredekampe[[col for col in possessionanmodstandershalvdel_cols if (team) in col]].mean(axis=1)
            team_possessionmodstandersfelt = dfsorteredekampe[[col for col in possessionanmodstandersfelt_cols if (team) in col]].mean(axis=1)
            team_challenge_intensity = dfsorteredekampe[[col for col in challenge_intensity_cols if (team) in col]].mean(axis=1)
            team_recoveries = dfsorteredekampe[[col for col in recoveries_cols if (team) in col]].mean(axis=1)
            team_opponenthalfrecoveries = dfsorteredekampe[[col for col in opponenthalfrecoveries_cols if (team) in col]].mean(axis=1)

            team_ppda = dfsorteredekampe[[col for col in ppda_cols if (team) in col]].mean(axis=1)

            team_data_målbare[team] = pd.concat([team_forward_passes,team_forward_passes_successful, team_passes, team_touches_in_box,team_xg,team_xgpershot,team_dzshots,team_possessionantal,team_possessionmodstandershalvdel,team_possessionmodstandersfelt,team_challenge_intensity,team_recoveries,team_opponenthalfrecoveries,team_ppda], axis=1)
            
        team_df_målbare = pd.concat(team_data_målbare, axis=0, keys=team_data_målbare.keys())
        team_df_målbare.columns = ['Forward passes','Forward passes successful', 'Passes', 'Touches in box','xG','xG/shot','Dangerzone shots','Antal possessions','Antal possessions der når modstanders halvdel','Antal possessions der når modstanders felt','Challenge intensity','Recoveries','Opp half recoveries','PPDA']
        team_df_målbare = team_df_målbare.groupby(level=0).mean()
        team_df_målbare['Forward pass %'] = (team_df_målbare['Forward passes successful']/team_df_målbare['Forward passes'])*100
        team_df_målbare['Forward pass share'] = (team_df_målbare['Forward passes']/team_df_målbare['Passes'])*100
        team_df_målbare['Forward pass score'] = team_df_målbare[['Forward pass share','Forward pass %']].mean(axis=1)
        team_df_målbare['Possession to opp box'] = team_df_målbare['Antal possessions der når modstanders felt']
        team_df_målbare['Possession to opp half %'] = (team_df_målbare['Antal possessions der når modstanders halvdel']/team_df_målbare['Antal possessions'])*100
        team_df_målbare['Possession to opp box %'] = (team_df_målbare['Antal possessions der når modstanders felt']/team_df_målbare['Antal possessions'])*100
        team_df_målbare = team_df_målbare[['Forward pass score','Touches in box','xG','xG/shot','Dangerzone shots','Possession to opp box','Possession to opp half %','Possession to opp box %','Challenge intensity','Recoveries','Opp half recoveries','PPDA']]
        team_df_målbare = team_df_målbare.round(decimals=3)
        hold = 'Horsens U19'
        team_df_målbare_andre_hold = team_df_målbare.drop(hold)
        team_df_målbare['xG against'] = team_df_målbare_andre_hold['xG'].mean()
        team_df_målbare['Danger zone shots against'] = team_df_målbare_andre_hold['Dangerzone shots'].mean()
        team_df_målbare['Touches in box against'] = team_df_målbare_andre_hold['Touches in box'].mean()
        team_df_målbare['Duels won %'] = (team_df['Duels won']/team_df['Duels'])*100
        mask = team_df_målbare.index.str.contains('Horsens')
        team_df_målbare = team_df_målbare[mask]
        team_df_målbare = team_df_målbare.round(decimals=2)

        import pandas as pd
        import csv
        import streamlit as st
        import numpy as np
        from datetime import datetime

        df = pd.read_csv('Teamsheet alle kampe U19.csv')

        dfsorteredeallekampe = df.iloc[: , 1:]
        dfsorteredeallekampe['date'] = dfsorteredeallekampe['date'].astype(str)
        dfsorteredeallekampe['date'] = dfsorteredeallekampe['date'].str.replace(r'\sGMT.*$', '', regex=True)
        dfsorteredeallekampe['date'] = pd.to_datetime(dfsorteredeallekampe['date'], format="%B %d, %Y at %I:%M:%S %p")
        dfsorteredeallekampe['date'] = dfsorteredeallekampe['date'].dt.strftime('%d-%m-%Y')
        dfsorteredeallekampe = dfsorteredeallekampe.transpose()
        dfoverskrifter = dfsorteredeallekampe[:2]
        dfsorteredeallekampe = dfsorteredeallekampe[2:].apply(pd.to_numeric, errors='coerce')
        dfsorteredeallekampe = pd.concat([dfoverskrifter,dfsorteredeallekampe])
        dfsorteredeallekampe = dfsorteredeallekampe.dropna(how='all')
        dfsorteredeallekampe = dfsorteredeallekampe.rename_axis('Parameter').astype(str)
        dfsorteredeallekampe = dfsorteredeallekampe.transpose()


        goals_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.goals')]
        shots_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.shots')]
        xg_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.xg')]
        duels_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.duels')]
        duelswon_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.duelsSuccessful')]
        possession_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.possessionPercent')]
        ppda_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.ppda')]

        # Create a new dataframe with the average values for each team
        team_data = {}
        for team in set([col.split('.')[1] for col in shots_cols]):
            team_goals = dfsorteredeallekampe[[col for col in goals_cols if(team) in col]].mean(axis=1)    
            team_shots = dfsorteredeallekampe[[col for col in shots_cols if(team) in col]].mean(axis=1)
            team_xg = dfsorteredeallekampe[[col for col in xg_cols if (team) in col]].mean(axis=1)
            team_duels = dfsorteredeallekampe[[col for col in duels_cols if (team) in col]].mean(axis=1)
            team_duelswon = dfsorteredeallekampe[[col for col in duelswon_cols if (team) in col]].mean(axis=1)
            team_possession = dfsorteredeallekampe[[col for col in possession_cols if (team) in col]].mean(axis=1)
            team_ppda = dfsorteredeallekampe[[col for col in ppda_cols if (team) in col]].mean(axis=1)

            team_data[team] = pd.concat([team_goals,team_shots, team_xg, team_duels,team_duelswon,team_possession,team_ppda], axis=1)
            
        team_df = pd.concat(team_data, axis=0, keys=team_data.keys())
        team_df.columns = ['Goals','Shots', 'Xg', 'Duels','Duels won','Possession %','PPDA']
        team_df = team_df.groupby(level=0).mean()
        team_df= team_df.round(decimals=2)


        forward_passes_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.forwardPasses')]
        forward_passes_successful_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.forwardPassesSuccessful')]
        passes_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.passes')]
        touches_in_box_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.touchesInBox')]
        xg_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.xg')]
        xgpershot_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.xgPerShot')]
        dzshots_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.shotsFromDangerZone')]
        possessionantal_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.possessionNumber')]
        possessionanmodstandershalvdel_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.reachingOpponentHalf')]
        possessionanmodstandersfelt_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.reachingOpponentBox')]
        challenge_intensity_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.challengeIntensity')]
        recoveries_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.recoveriesTotal')]
        opponenthalfrecoveries_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.opponentHalfRecoveries')]
        ppda_cols = [col for col in dfsorteredeallekampe.columns if col.endswith('.ppda')]

        # Create a new dataframe with the average values for each team
        team_data_målbare_alle = {}
        for team in set([col.split('.')[1] for col in shots_cols]):
            team_forward_passes = dfsorteredeallekampe[[col for col in forward_passes_cols if(team) in col]].mean(axis=1)    
            team_forward_passes_successful = dfsorteredeallekampe[[col for col in forward_passes_successful_cols if(team) in col]].mean(axis=1)
            team_passes = dfsorteredeallekampe[[col for col in passes_cols if (team) in col]].mean(axis=1)
            team_touches_in_box = dfsorteredeallekampe[[col for col in touches_in_box_cols if (team) in col]].mean(axis=1)
            team_xg = dfsorteredeallekampe[[col for col in xg_cols if (team) in col]].mean(axis=1)
            team_xgpershot = dfsorteredeallekampe[[col for col in xgpershot_cols if (team) in col]].mean(axis=1)
            team_dzshots = dfsorteredeallekampe[[col for col in dzshots_cols if (team) in col]].mean(axis=1)
            team_possessionantal = dfsorteredeallekampe[[col for col in possessionantal_cols if (team) in col]].mean(axis=1)
            team_possessionmodstandershalvdel = dfsorteredeallekampe[[col for col in possessionanmodstandershalvdel_cols if (team) in col]].mean(axis=1)
            team_possessionmodstandersfelt = dfsorteredeallekampe[[col for col in possessionanmodstandersfelt_cols if (team) in col]].mean(axis=1)
            team_challenge_intensity = dfsorteredeallekampe[[col for col in challenge_intensity_cols if (team) in col]].mean(axis=1)
            team_recoveries = dfsorteredeallekampe[[col for col in recoveries_cols if (team) in col]].mean(axis=1)
            team_opponenthalfrecoveries = dfsorteredeallekampe[[col for col in opponenthalfrecoveries_cols if (team) in col]].mean(axis=1)

            team_ppda = dfsorteredeallekampe[[col for col in ppda_cols if (team) in col]].mean(axis=1)

            team_data_målbare_alle[team] = pd.concat([team_forward_passes,team_forward_passes_successful, team_passes, team_touches_in_box,team_xg,team_xgpershot,team_dzshots,team_possessionantal,team_possessionmodstandershalvdel,team_possessionmodstandersfelt,team_challenge_intensity,team_recoveries,team_opponenthalfrecoveries,team_ppda], axis=1)
            
        team_df_målbare_alle = pd.concat(team_data_målbare_alle, axis=0, keys=team_data_målbare_alle.keys())
        team_df_målbare_alle.columns = ['Forward passes','Forward passes successful', 'Passes', 'Touches in box','xG','xG/shot','Dangerzone shots','Antal possessions','Antal possessions der når modstanders halvdel','Antal possessions der når modstanders felt','Challenge intensity','Recoveries','Opp half recoveries','PPDA']
        team_df_målbare_alle = team_df_målbare_alle.groupby(level=0).mean()
        team_df_målbare_alle['Forward pass %'] = (team_df_målbare_alle['Forward passes successful']/team_df_målbare_alle['Forward passes'])*100
        team_df_målbare_alle['Forward pass share'] = (team_df_målbare_alle['Forward passes']/team_df_målbare_alle['Passes'])*100
        team_df_målbare_alle['Forward pass score'] = team_df_målbare_alle[['Forward pass share','Forward pass %']].mean(axis=1)
        team_df_målbare_alle['Possession to opp box'] = team_df_målbare_alle['Antal possessions der når modstanders felt']
        team_df_målbare_alle['Possession to opp half %'] = (team_df_målbare_alle['Antal possessions der når modstanders halvdel']/team_df_målbare_alle['Antal possessions'])*100
        team_df_målbare_alle['Possession to opp box %'] = (team_df_målbare_alle['Antal possessions der når modstanders felt']/team_df_målbare_alle['Antal possessions'])*100
        team_df_målbare_alle = team_df_målbare_alle[['Forward pass score','Touches in box','xG','xG/shot','Dangerzone shots','Possession to opp box','Possession to opp half %','Possession to opp box %','Challenge intensity','Recoveries','Opp half recoveries','PPDA']]
        team_df_målbare_alle = team_df_målbare_alle.round(decimals=3)
        #hold = 'Horsens U15'
        #team_df_målbare_andre_hold = team_df_målbare.drop(hold)
        team_df_målbare_alle['xG against'] = team_df_målbare_alle['xG'].mean()
        team_df_målbare_alle['Danger zone shots against'] = team_df_målbare_alle['Dangerzone shots'].mean()
        team_df_målbare_alle['Touches in box against'] = team_df_målbare_alle['Touches in box'].mean()
        team_df_målbare_alle['Duels won %'] = (team_df['Duels won']/team_df['Duels'])*100
        team_df_målbare_alle = team_df_målbare_alle.round(decimals=2)
        Benchmark = team_df_målbare_alle.mean(axis=0)
        team_df_målbare_alle.loc['Liga Gennemsnit'] = Benchmark
        mask = team_df_målbare_alle.index.str.contains('Liga Gennemsnit')
        team_df_målbare_alle = team_df_målbare_alle[mask]


        df = pd.read_csv('Teamsheet alle kampe U19 sidste sæson.csv')

        dfsorteredekampesidstesæson = df.iloc[: , 1:]
        dfsorteredekampesidstesæson['date'] = dfsorteredekampesidstesæson['date'].astype(str)
        dfsorteredekampesidstesæson['date'] = dfsorteredekampesidstesæson['date'].str.replace(r'\sGMT.*$', '', regex=True)
        dfsorteredekampesidstesæson['date'] = pd.to_datetime(dfsorteredekampesidstesæson['date'], format="%B %d, %Y at %I:%M:%S %p")
        dfsorteredekampesidstesæson['date'] = dfsorteredekampesidstesæson['date'].dt.strftime('%d-%m-%Y')
        dfsorteredekampesidstesæson = dfsorteredekampesidstesæson.transpose()
        dfoverskrifter = dfsorteredekampesidstesæson[:2]
        dfsorteredekampesidstesæson = dfsorteredekampesidstesæson[2:].apply(pd.to_numeric, errors='coerce')
        dfsorteredekampesidstesæson = pd.concat([dfoverskrifter,dfsorteredekampesidstesæson])
        dfsorteredekampesidstesæson = dfsorteredekampesidstesæson.dropna(how='all')
        dfsorteredekampesidstesæson = dfsorteredekampesidstesæson.rename_axis('Parameter').astype(str)
        dfsorteredekampesidstesæson = dfsorteredekampesidstesæson.transpose()


        goals_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.goals')]
        shots_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.shots')]
        xg_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.xg')]
        duels_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.duels')]
        duelswon_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.duelsSuccessful')]
        possession_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.possessionPercent')]
        ppda_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.ppda')]

        # Create a new dataframe with the average values for each team
        team_data_sidstesæson = {}
        for team in set([col.split('.')[1] for col in shots_cols]):
            team_goals = dfsorteredekampesidstesæson[[col for col in goals_cols if(team) in col]].mean(axis=1)    
            team_shots = dfsorteredekampesidstesæson[[col for col in shots_cols if(team) in col]].mean(axis=1)
            team_xg = dfsorteredekampesidstesæson[[col for col in xg_cols if (team) in col]].mean(axis=1)
            team_duels = dfsorteredekampesidstesæson[[col for col in duels_cols if (team) in col]].mean(axis=1)
            team_duelswon = dfsorteredekampesidstesæson[[col for col in duelswon_cols if (team) in col]].mean(axis=1)
            team_possession = dfsorteredekampesidstesæson[[col for col in possession_cols if (team) in col]].mean(axis=1)
            team_ppda = dfsorteredekampesidstesæson[[col for col in ppda_cols if (team) in col]].mean(axis=1)

            team_data_sidstesæson[team] = pd.concat([team_goals,team_shots, team_xg, team_duels,team_duelswon,team_possession,team_ppda], axis=1)
            
        team_df_sidstesæson = pd.concat(team_data_sidstesæson, axis=0, keys=team_data_sidstesæson.keys())
        team_df_sidstesæson.columns = ['Goals','Shots', 'Xg', 'Duels','Duels won','Possession %','PPDA']
        team_df_sidstesæson = team_df_sidstesæson.groupby(level=0).mean()


        team_df_sidstesæson= team_df_sidstesæson.round(decimals=2)


        forward_passes_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.forwardPasses')]
        forward_passes_successful_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.forwardPassesSuccessful')]
        passes_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.passes')]
        touches_in_box_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.touchesInBox')]
        xg_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.xg')]
        xgpershot_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.xgPerShot')]
        dzshots_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.shotsFromDangerZone')]
        possessionantal_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.possessionNumber')]
        possessionanmodstandershalvdel_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.reachingOpponentHalf')]
        possessionanmodstandersfelt_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.reachingOpponentBox')]
        challenge_intensity_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.challengeIntensity')]
        recoveries_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.recoveriesTotal')]
        opponenthalfrecoveries_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.opponentHalfRecoveries')]
        ppda_cols = [col for col in dfsorteredekampesidstesæson.columns if col.endswith('.ppda')]

        # Create a new dataframe with the average values for each team
        team_data_målbare_sidstesæson = {}
        for team in set([col.split('.')[1] for col in shots_cols]):
            team_forward_passes = dfsorteredekampesidstesæson[[col for col in forward_passes_cols if(team) in col]].mean(axis=1)    
            team_forward_passes_successful = dfsorteredekampesidstesæson[[col for col in forward_passes_successful_cols if(team) in col]].mean(axis=1)
            team_passes = dfsorteredekampesidstesæson[[col for col in passes_cols if (team) in col]].mean(axis=1)
            team_touches_in_box = dfsorteredekampesidstesæson[[col for col in touches_in_box_cols if (team) in col]].mean(axis=1)
            team_xg = dfsorteredekampesidstesæson[[col for col in xg_cols if (team) in col]].mean(axis=1)
            team_xgpershot = dfsorteredekampesidstesæson[[col for col in xgpershot_cols if (team) in col]].mean(axis=1)
            team_dzshots = dfsorteredekampesidstesæson[[col for col in dzshots_cols if (team) in col]].mean(axis=1)
            team_possessionantal = dfsorteredekampesidstesæson[[col for col in possessionantal_cols if (team) in col]].mean(axis=1)
            team_possessionmodstandershalvdel = dfsorteredekampesidstesæson[[col for col in possessionanmodstandershalvdel_cols if (team) in col]].mean(axis=1)
            team_possessionmodstandersfelt = dfsorteredekampesidstesæson[[col for col in possessionanmodstandersfelt_cols if (team) in col]].mean(axis=1)
            team_challenge_intensity = dfsorteredekampesidstesæson[[col for col in challenge_intensity_cols if (team) in col]].mean(axis=1)
            team_recoveries = dfsorteredekampesidstesæson[[col for col in recoveries_cols if (team) in col]].mean(axis=1)
            team_opponenthalfrecoveries = dfsorteredekampesidstesæson[[col for col in opponenthalfrecoveries_cols if (team) in col]].mean(axis=1)

            team_ppda = dfsorteredekampesidstesæson[[col for col in ppda_cols if (team) in col]].mean(axis=1)

            team_data_målbare_sidstesæson[team] = pd.concat([team_forward_passes,team_forward_passes_successful, team_passes, team_touches_in_box,team_xg,team_xgpershot,team_dzshots,team_possessionantal,team_possessionmodstandershalvdel,team_possessionmodstandersfelt,team_challenge_intensity,team_recoveries,team_opponenthalfrecoveries,team_ppda], axis=1)
            
        team_df_målbaresidstesæson = pd.concat(team_data_målbare_sidstesæson, axis=0, keys=team_data_målbare_sidstesæson.keys())
        team_df_målbaresidstesæson.columns = ['Forward passes','Forward passes successful', 'Passes', 'Touches in box','xG','xG/shot','Dangerzone shots','Antal possessions','Antal possessions der når modstanders halvdel','Antal possessions der når modstanders felt','Challenge intensity','Recoveries','Opp half recoveries','PPDA']
        team_df_målbaresidstesæson = team_df_målbaresidstesæson.groupby(level=0).mean()
        team_df_målbaresidstesæson['Forward pass %'] = (team_df_målbaresidstesæson['Forward passes successful']/team_df_målbaresidstesæson['Forward passes'])*100
        team_df_målbaresidstesæson['Forward pass share'] = (team_df_målbaresidstesæson['Forward passes']/team_df_målbaresidstesæson['Passes'])*100
        team_df_målbaresidstesæson['Forward pass score'] = team_df_målbaresidstesæson[['Forward pass share','Forward pass %']].mean(axis=1)
        team_df_målbaresidstesæson['Possession to opp box'] = team_df_målbaresidstesæson['Antal possessions der når modstanders felt']
        team_df_målbaresidstesæson['Possession to opp half %'] = (team_df_målbaresidstesæson['Antal possessions der når modstanders halvdel']/team_df_målbaresidstesæson['Antal possessions'])*100
        team_df_målbaresidstesæson['Possession to opp box %'] = (team_df_målbaresidstesæson['Antal possessions der når modstanders felt']/team_df_målbaresidstesæson['Antal possessions'])*100
        team_df_målbaresidstesæson = team_df_målbaresidstesæson[['Forward pass score','Touches in box','xG','xG/shot','Dangerzone shots','Possession to opp box','Possession to opp half %','Possession to opp box %','Challenge intensity','Recoveries','Opp half recoveries','PPDA']]
        team_df_målbaresidstesæson = team_df_målbaresidstesæson.round(decimals=3)

        team_df_målbaresidstesæson['xG against'] = team_df_målbaresidstesæson['xG'].mean()
        team_df_målbaresidstesæson['Danger zone shots against'] = team_df_målbaresidstesæson['Dangerzone shots'].mean()
        team_df_målbaresidstesæson['Touches in box against'] = team_df_målbaresidstesæson['Touches in box'].mean()
        team_df_målbaresidstesæson['Duels won %'] = (team_df_sidstesæson['Duels won']/team_df_sidstesæson['Duels'])*100
        mask = team_df_målbaresidstesæson.index.str.contains('Horsens')
        team_df_målbaresidstesæson = team_df_målbaresidstesæson[mask]
        team_df_målbaresidstesæson = team_df_målbaresidstesæson.round(decimals=2)
        frames = [team_df_målbare_alle,team_df_målbare,team_df_målbaresidstesæson]
        Benchmark = pd.concat(frames)
        st.dataframe(Benchmark)
        import plotly.graph_objs as go
        import numpy as np
        from plotly.subplots import make_subplots

        trace1 = go.Indicator(mode="gauge+number",    value=Benchmark['Forward pass score'][1],domain={'row' : 1, 'column' : 1},title={'text': "Forward pass score"},gauge={'axis':{'range':[Benchmark['Forward pass score'][2],Benchmark['Forward pass score'][0]]},})
        trace2 = go.Indicator(mode="gauge+number",    value=Benchmark['Touches in box'][1],domain={'row' : 1, 'column' : 2},title={'text': "Touches in box"},gauge={'axis':{'range':[Benchmark['Touches in box'][2],Benchmark['Touches in box'][0]]},})
        trace3 = go.Indicator(mode="gauge+number",    value=Benchmark['xG'][1],domain={'row' : 1, 'column' : 3},title={'text': "xG"},gauge={'axis':{'range':[Benchmark['xG'][2],Benchmark['xG'][0]]},})
        trace4 = go.Indicator(mode="gauge+number",    value=Benchmark['xG/shot'][1],domain={'row' : 1, 'column' : 4},title={'text': "xG/shot"},gauge={'axis':{'range':[Benchmark['xG/shot'][2],Benchmark['xG/shot'][0]]},'steps':[{'range':[0,Benchmark['xG/shot'][2]],'color':'red'}]})
        trace5 = go.Indicator(mode="gauge+number",    value=Benchmark['Dangerzone shots'][1],domain={'row' : 2, 'column' : 1},title={'text': "Dangerzone shots"},gauge={'axis':{'range':[Benchmark['Dangerzone shots'][2],Benchmark['Dangerzone shots'][0]]},})
        trace6 = go.Indicator(mode="gauge+number",    value=Benchmark['Possession to opp box'][1],domain={'row' : 2, 'column' : 2},title={'text': "Possession to opp box"},gauge={'axis':{'range':[Benchmark['Possession to opp box'][2],Benchmark['Possession to opp box'][0]]},})
        trace7 = go.Indicator(mode="gauge+number",    value=Benchmark['Possession to opp half %'][1],domain={'row' : 2, 'column' : 3},title={'text': "Possession to opp half %"},gauge={'axis':{'range':[Benchmark['Possession to opp half %'][2],Benchmark['Possession to opp half %'][0]]},})
        trace8 = go.Indicator(mode="gauge+number",    value=Benchmark['Possession to opp box %'][1],domain={'row' : 2, 'column' : 4},title={'text': "Possession to opp box %"},gauge={'axis':{'range':[Benchmark['Possession to opp box %'][2],Benchmark['Possession to opp box %'][0]]},})
        
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
        
        trace9 = go.Indicator(mode="gauge+number",    value=Benchmark['xG against'][1],domain={'row' : 1, 'column' : 1},title={'text': "xG against"},gauge={'axis':{'range':[Benchmark['xG against'][2],Benchmark['xG against'][0]]}})
        trace10 = go.Indicator(mode="gauge+number",    value=Benchmark['PPDA'][1],domain={'row' : 1, 'column' : 2},title={'text': "PPDA"},gauge={'axis':{'range':[Benchmark['PPDA'][2],Benchmark['PPDA'][0]]}})
        trace11 = go.Indicator(mode="gauge+number",    value=Benchmark['Danger zone shots against'][1],domain={'row' : 1, 'column' : 3},title={'text': "Danger zone shots against"},gauge={'axis':{'range':[Benchmark['Danger zone shots against'][2],Benchmark['Danger zone shots against'][0]]}})
        trace12 = go.Indicator(mode="gauge+number",    value=Benchmark['Challenge intensity'][1],domain={'row' : 1, 'column' : 4},title={'text': "Challenge intensity"},gauge={'axis':{'range':[Benchmark['Challenge intensity'][2],Benchmark['Challenge intensity'][0]]}})
        trace13 = go.Indicator(mode="gauge+number",    value=Benchmark['Recoveries'][1],domain={'row' : 2, 'column' : 1},title={'text': "Recoveries"},gauge={'axis':{'range':[Benchmark['Recoveries'][0],Benchmark['Recoveries'][2]]}})
        trace14 = go.Indicator(mode="gauge+number",    value=Benchmark['Opp half recoveries'][1],domain={'row' : 2, 'column' : 2},title={'text': "Opp half recoveries"},gauge={'axis':{'range':[Benchmark['Opp half recoveries'][2],Benchmark['Opp half recoveries'][0]]}})
        trace15 = go.Indicator(mode="gauge+number",    value=Benchmark['Touches in box against'][1],domain={'row' : 2, 'column' : 3},title={'text': "Touches in box against"},gauge={'axis':{'range':[Benchmark['Touches in box against'][2],Benchmark['Touches in box against'][0]]}})
        trace16 = go.Indicator(mode="gauge+number",    value=Benchmark['Duels won %'][1],domain={'row' : 2, 'column' : 4},title={'text': "Duels won %"},gauge={'axis':{'range':[Benchmark['Duels won %'][2],Benchmark['Duels won %'][0]]}})
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


    Årgange = {'U15':U15,
           'U17':U17,
           'U19':U19,
    }
    rullemenu = st.selectbox('Vælg årgang',Årgange.keys())
    Årgange[rullemenu]()
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
