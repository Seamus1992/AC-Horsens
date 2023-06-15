import streamlit as st
st.set_page_config(layout = 'wide')

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
    
    Spiller = filtreretdfkamp['Spiller'].drop_duplicates(keep='first')
    option5 = st.multiselect('Vælg spiller (Hvis ingen spiller er valgt, vises alle)',Spiller)
    if len(option5) > 0:
        filtreretdfspiller = option5
    else:
        filtreretdfspiller = Spiller

    filtreretdfspiller = df.loc[df.loc[df['Spiller'].isin(filtreretdfspiller),'Spiller'].index.values]

    førtræning = filtreretdfspiller[['Tidsstempel','Spiller','Hvilken årgang er du?','Hvor frisk er du?','Hvordan har du det mentalt','Har du fået nok at spise inden træning/kamp?','Hvordan har din søvn været?','Hvor mange timer sov du i nat?']]
    eftertræning = filtreretdfspiller[['Tidsstempel','Spiller','Hvilken årgang er du?','Træning/kamp - tid i minutter?','Hvor hård var træning/kamp? (10 er hårdest)','Hvor udmattet er du?','Bedøm din muskelømhed','Hvordan har du det mentalt?','Jeg følte mig tilpas udfordret under træning/kamp','Min tidsfornemmelse forsvandt under træning/kamp','Jeg oplevede at tanker og handlinger var rettet mod træning/kamp']]
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
    st.write('Før aktivitet')
    st.dataframe(førtræning)
    st.write('Efter aktivitet')
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
    df_GPSgennemsnit1 = df_GPS[['Ugenummer','Player Name','Date','Distance (km)', 'Top Speed (km/h)', 'Højintens løb', 'Sprint', 'Hårde Accelerationer', 'Hårde deccelerationer','Tid med høj puls']]
    df_GPSgennemsnit = df_GPSgennemsnit1.groupby(['Date']).mean(numeric_only=True)
    df_GPSgennemsnit['Ugenummer'] = df_GPSgennemsnit['Ugenummer'].astype(int)
    Ugenummer = df_GPSgennemsnit['Ugenummer'].drop_duplicates()
    df = df_GPSgennemsnit
    option2 = st.multiselect('Vælg ugenummer)',Ugenummer)
    if len(option2) > 0:
        temp_select = option2
    else:
        temp_select = Ugenummer

    df_GPSgennemsnit = df.loc[df.loc[df.Ugenummer.isin(temp_select),'Ugenummer'].index.values]

    st.write('Trupgennemsnit pr. dag')
    st.line_chart(df_GPSgennemsnit,y=['Sprint','Distance (km)','Top Speed (km/h)','Højintens løb','Hårde Accelerationer','Hårde deccelerationer','Tid med høj puls'],)
    st.dataframe(df_GPSgennemsnit)
    spillere = df_GPSgennemsnit1.drop_duplicates(subset=['Player Name'])
    option4 = st.selectbox('Vælg spiller',spillere['Player Name'])
    
    df = df_GPSgennemsnit1.loc[df_GPSgennemsnit1.loc[df_GPSgennemsnit1['Player Name'] == option4,'Player Name'].index.values]
    df = df.loc[df.loc[df.Ugenummer.isin(temp_select),'Ugenummer'].index.values]

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
        #dfsorteredekampe['date'] = dfsorteredekampe['date'].astype(str)
        #dfsorteredekampe['date'] = dfsorteredekampe['date'].str.replace(r'\sGMT.*$', '', regex=True)
        #dfsorteredekampe['date'] = pd.to_datetime(dfsorteredekampe['date'], format="%B %d, %Y at %I:%M:%S %p")
        #dfsorteredekampe['date'] = dfsorteredekampe['date'].dt.strftime('%d-%m-%Y')
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
        st.write('Skalaen går fra eget gennemsnit i seneste sæson til denne sæsons ligagennemsnit, ved ingen udfyldning er den rød, delvis udfyldning er gul, helt fyldt er grøn')
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
        st.write('Skalaen går fra eget gennemsnit i seneste sæson til denne sæsons ligagennemsnit, ved ingen udfyldning er den rød, delvis udfyldning er gul, helt fyldt er grøn')
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
        #dfsorteredekampe['date'] = dfsorteredekampe['date'].astype(str)
        #dfsorteredekampe['date'] = dfsorteredekampe['date'].str.replace(r'\sGMT.*$', '', regex=True)
        #dfsorteredekampe['date'] = pd.to_datetime(dfsorteredekampe['date'], format="%B %d, %Y at %I:%M:%S %p")
        #dfsorteredekampe['date'] = dfsorteredekampe['date'].dt.strftime('%d-%m-%Y')
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
        st.write('Skalaen går fra eget gennemsnit i seneste sæson til denne sæsons ligagennemsnit, ved ingen udfyldning er den rød, delvis udfyldning er gul, helt fyldt er grøn')
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
        st.write('Skalaen går fra eget gennemsnit i seneste sæson til denne sæsons ligagennemsnit, ved ingen udfyldning er den rød, delvis udfyldning er gul, helt fyldt er grøn')
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
        #dfsorteredekampe['date'] = dfsorteredekampe['date'].astype(str)
        #dfsorteredekampe['date'] = dfsorteredekampe['date'].str.replace(r'\sGMT.*$', '', regex=True)
        #dfsorteredekampe['date'] = pd.to_datetime(dfsorteredekampe['date'], format="%B %d, %Y at %I:%M:%S %p")
        #dfsorteredekampe['date'] = dfsorteredekampe['date'].dt.strftime('%d-%m-%Y')
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
        st.write('Skalaen går fra eget gennemsnit i seneste sæson til denne sæsons ligagennemsnit, ved ingen udfyldning er den rød, delvis udfyldning er gul, helt fyldt er grøn')
        st.plotly_chart(fig,use_container_width=True)
        
        trace9 = go.Indicator(mode="gauge+number",    value=Benchmark['xG against'][1],domain={'row' : 1, 'column' : 1},title={'text': "xG against"},gauge={'axis':{'range':[Benchmark['xG against'][2],Benchmark['xG against'][0]]}})
        trace10 = go.Indicator(mode="gauge+number",    value=Benchmark['PPDA'][1],domain={'row' : 1, 'column' : 2},title={'text': "PPDA"},gauge={'axis':{'range':[Benchmark['PPDA'][2],Benchmark['PPDA'][0]]}})
        trace11 = go.Indicator(mode="gauge+number",    value=Benchmark['Danger zone shots against'][1],domain={'row' : 1, 'column' : 3},title={'text': "Danger zone shots against"},gauge={'axis':{'range':[Benchmark['Danger zone shots against'][2],Benchmark['Danger zone shots against'][0]]}})
        trace12 = go.Indicator(mode="gauge+number",    value=Benchmark['Challenge intensity'][1],domain={'row' : 1, 'column' : 4},title={'text': "Challenge intensity"},gauge={'axis':{'range':[Benchmark['Challenge intensity'][0],Benchmark['Challenge intensity'][2]]}})
        trace13 = go.Indicator(mode="gauge+number",    value=Benchmark['Recoveries'][1],domain={'row' : 2, 'column' : 1},title={'text': "Recoveries"},gauge={'axis':{'range':[Benchmark['Recoveries'][0],Benchmark['Recoveries'][2]]}})
        trace14 = go.Indicator(mode="gauge+number",    value=Benchmark['Opp half recoveries'][1],domain={'row' : 2, 'column' : 2},title={'text': "Opp half recoveries"},gauge={'axis':{'range':[Benchmark['Opp half recoveries'][2],Benchmark['Opp half recoveries'][0]]}})
        trace15 = go.Indicator(mode="gauge+number",    value=Benchmark['Touches in box against'][1],domain={'row' : 2, 'column' : 3},title={'text': "Touches in box against"},gauge={'axis':{'range':[Benchmark['Touches in box against'][0],Benchmark['Touches in box against'][2]]}})
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
        st.write('Skalaen går fra eget gennemsnit i seneste sæson til denne sæsons ligagennemsnit, ved ingen udfyldning er den rød, delvis udfyldning er gul, helt fyldt er grøn')
        st.plotly_chart(fig1,use_container_width=True)    


    Årgange = {'U15':U15,
           'U17':U17,
           'U19':U19,
    }
    rullemenu = st.selectbox('Vælg årgang',Årgange.keys())
    Årgange[rullemenu]()
    
def Individuelt_dashboard():
    def U15():
        import pandas as pd
        import streamlit as st
        import json
        from pandas import json_normalize
        import ast
        from dateutil import parser
        import plotly.graph_objects as go
        navne = pd.read_excel('Navne.xlsx')
        navne = navne[navne['Trup'].str.contains('U15')]
        navneliste = navne['Spillere'].sort_values(ascending=True)
        df = pd.read_csv('Individuelt dashboard U15.csv')
        df.rename(columns={'playerId': 'Player id'}, inplace=True)
        df = df.astype(str)
        dfevents = pd.read_csv('U15 eventdata alle.csv',low_memory=False)
        dfevents = dfevents[['Player id','Player name','team_name','label','date','matchId']]
        dfspillernavn = df[['Player id','matchId','positions','average','percent','total']]
        dfspillernavn = dfspillernavn.astype(str)
        dfevents['Player id'] = dfevents['Player id'].astype(str)
        dfevents['matchId'] = dfevents['matchId'].astype(str)
        df = dfspillernavn.merge(dfevents)

        df['Player&matchId'] = df['Player id'] + df['matchId']
        df['Player&matchId'] = df['Player&matchId'].drop_duplicates(keep='first')
        df = df.dropna()
        df = df[['Player id','Player name','team_name','matchId','label','date','positions','average','percent','total']]

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
        df = df[['Player name','team_name','matchId','label','date','position_names','position_codes','average','percent','total']]
        df = df.rename(columns={'team_name':'Team name'})
        df['percent'] = df['percent'].apply(lambda x: ast.literal_eval(x))

        # Create a new dataframe with the columns as the dictionary keys and the values as a list
        new_df = pd.DataFrame(df['percent'].to_list(), index=df.index).add_prefix('percent_')

        # Concatenate the new dataframe with the original dataframe
        df = pd.concat([df, new_df], axis=1)

        # Drop the original 'percent' column
        df = df.drop('percent', axis=1)

        df['total'] = df['total'].apply(lambda x: ast.literal_eval(x))

        # Create a new dataframe with the columns as the dictionary keys and the values as a list
        new_df = pd.DataFrame(df['total'].to_list(), index=df.index).add_prefix('total_')

        # Concatenate the new dataframe with the original dataframe
        df = pd.concat([df, new_df], axis=1)

        # Drop the original 'percent' column
        df = df.drop('total', axis=1)

        df['average'] = df['average'].apply(lambda x: ast.literal_eval(x))

        # Create a new dataframe with the columns as the dictionary keys and the values as a list
        new_df = pd.DataFrame(df['average'].to_list(), index=df.index).add_prefix('average_')

        # Concatenate the new dataframe with the original dataframe
        df = pd.concat([df, new_df], axis=1)


        # Drop the original 'percent' column
        df = df.drop('average', axis=1)
        df['position_codes'] = df['position_codes'].astype(str)
        #df['date'] = df['date'].astype(str)
        #df['date'] = df['date'].apply(lambda x: parser.parse(x))

        # Sort the dataframe by the 'date' column
        #df = df.sort_values(by='date',ascending=False)

        # Format the 'date' column to day-month-year format
        #df['date'] = df['date'].apply(lambda x: x.strftime('%d-%m-%Y'))
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date',ascending=False)

        df_backs = df[df['position_codes'].str.contains('|'.join(['lb', 'rb']))]
        df_backsminutter = df_backs[['Player name','Team name','total_minutesOnField']]
        df_backsminutter = df_backsminutter.groupby(['Player id']).sum(numeric_only=True)
        df_backsminutter = df_backsminutter[df_backsminutter['total_minutesOnField'] >= 300]

        df_Stoppere = df[df['position_codes'].str.contains('|'.join(['cb']))]
        df_stoppereminutter = df_Stoppere[['Player name','Team name','total_minutesOnField']]
        df_stoppereminutter = df_stoppereminutter.groupby(['Player id']).sum(numeric_only=True)
        df_stoppereminutter = df_stoppereminutter[df_stoppereminutter['total_minutesOnField'] >= 300]

        df_Centrale_midt = df[df['position_codes'].str.contains('|'.join(['cm','amf','dmf']))]
        df_centraleminutter = df_Centrale_midt[['Player name','Team name','total_minutesOnField']]
        df_centraleminutter = df_centraleminutter.groupby(['Player id']).sum(numeric_only=True)
        df_centraleminutter = df_centraleminutter[df_centraleminutter['total_minutesOnField'] >= 300]

        df_Kanter = df[df['position_codes'].str.contains('|'.join(['rw','lw','ramf','lamf']))]
        df_kanterminutter = df_Kanter[['Player name','Team name','total_minutesOnField']]
        df_kanterminutter = df_kanterminutter.groupby(['Player id']).sum(numeric_only=True)
        df_kanterminutter = df_kanterminutter[df_kanterminutter['total_minutesOnField'] >=300]


        df_Angribere = df[df['position_codes'].str.contains('|'.join(['cf']))]
        df_angribereminutter = df_Angribere[['Player name','Team name','total_minutesOnField']]
        df_angribereminutter = df_angribereminutter.groupby(['Player id']).sum(numeric_only=True)
        df_angribereminutter = df_angribereminutter[df_angribereminutter['total_minutesOnField'] >= 300]


        df_backs = pd.merge(df_backsminutter,df_backs,on=('Player id'))
        df_backs = df_backs[df_backs['total_minutesOnField_y'] >=17]

        df_backs['Accurate crosses score'] = pd.qcut(df_backs['percent_successfulCrosses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Number of crosses score'] = pd.qcut(df_backs['average_crosses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['XA score'] = pd.qcut(df_backs['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Passes to final third score'] = pd.qcut(df_backs['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Successful dribbles score'] = pd.qcut(df_backs['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Defensive duels won score'] = pd.qcut(df_backs['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Progressive runs score'] = pd.qcut(df_backs['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Offensive duels won score'] = pd.qcut(df_backs['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Accelerations score'] = pd.qcut(df_backs['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Duels won score'] = pd.qcut(df_backs['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Interceptions score'] = pd.qcut(df_backs['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Successful defensive actions score'] = pd.qcut(df_backs['average_successfulDefensiveAction'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backssæsonen = df_backs[['Player name','Team name','label','total_minutesOnField_x','total_minutesOnField_y','Number of crosses score','Accurate crosses score','XA score','Passes to final third score','Successful dribbles score','Defensive duels won score','Progressive runs score','Offensive duels won score','Accelerations score','Duels won score','Interceptions score','Successful defensive actions score']]
        df_backssæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
        df_backssæsonen = df_backssæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

        df_backssæsonen['Indlægsstærk'] = (df_backssæsonen['Number of crosses score'] + df_backssæsonen['Accurate crosses score'] + df_backssæsonen['XA score'] + df_backssæsonen['Passes to final third score'])/4
        df_backssæsonen['1v1 færdigheder'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Defensive duels won score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'] + df_backssæsonen['Duels won score'])/6
        df_backssæsonen['Spilintelligens defensivt'] = (df_backssæsonen['Interceptions score'] + df_backssæsonen['Successful defensive actions score'] + df_backssæsonen['Duels won score'] + df_backssæsonen['Defensive duels won score'])/4
        df_backssæsonen['Fart'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'])/4
        df_backssæsonen ['Samlet'] = (df_backssæsonen['Indlægsstærk'] + df_backssæsonen['1v1 færdigheder'] + df_backssæsonen['Spilintelligens defensivt'] + df_backssæsonen['Fart'])/4
        df_backssæsonen = df_backssæsonen[['Indlægsstærk','1v1 færdigheder','Spilintelligens defensivt','Fart','Samlet']]
        df_backssæsonen = df_backssæsonen.sort_values(by='Samlet',ascending=False)

        df_backs['Indlægsstærk'] = (df_backs['Number of crosses score'] + df_backs['Accurate crosses score'] + df_backs['XA score'] + df_backs['Passes to final third score'])/4
        df_backs['1v1 færdigheder'] = (df_backs['Successful dribbles score'] + df_backs['Defensive duels won score'] + df_backs['Progressive runs score'] + df_backs['Offensive duels won score'] + df_backs['Accelerations score'] + df_backs['Duels won score'])/6
        df_backs['Spilintelligens defensivt'] = (df_backs['Interceptions score'] + df_backs['Successful defensive actions score'] + df_backs['Duels won score'] + df_backs['Defensive duels won score'])/4
        df_backs['Fart'] = (df_backs['Successful dribbles score'] + df_backs['Progressive runs score'] + df_backs['Offensive duels won score'] + df_backs['Accelerations score'])/4
        df_backs['Samlet'] = (df_backs['Indlægsstærk'] + df_backs['1v1 færdigheder'] + df_backs['Spilintelligens defensivt'] + df_backs['Fart'])/4


        df_backs = df_backs[['Player name','Team name','label','total_minutesOnField_y','Indlægsstærk','1v1 færdigheder','Spilintelligens defensivt','Fart','Samlet']]
        df_backs = df_backs.sort_values(by='Samlet',ascending=False)
        
        df_backs = navne.merge(df_backs)
        df_backs = df_backs.drop('Player Name',axis=1)
        df_backs = df_backs.drop('Player name',axis=1)    
        df_backssæsonen = df_backssæsonen.reset_index()
        df_backssæsonen = navne.merge(df_backssæsonen)
        df_backs = navne.merge(df_backs)
        df_backssæsonen = df_backssæsonen.drop('Player Name',axis=1)
        df_backssæsonen = df_backssæsonen.drop('Player name',axis=1)
        df_backssæsonen = df_backssæsonen.drop('label',axis=1)


        df_Stoppere = pd.merge(df_stoppereminutter,df_Stoppere,on=('Player id'))
        df_Stoppere = df_Stoppere[df_Stoppere['total_minutesOnField_y'] >=17]

        df_Stoppere['Accurate passes score'] = pd.qcut(df_Stoppere['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Accurate long passes score'] = pd.qcut(df_Stoppere['percent_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Forward passes score'] = pd.qcut(df_Stoppere['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Accurate forward passes score'] = pd.qcut(df_Stoppere['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Accurate progressive passes score'] = pd.qcut(df_Stoppere['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Accurate vertical passes score'] = pd.qcut(df_Stoppere['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Interceptions score'] = pd.qcut(df_Stoppere['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Succesful defensive actions score'] = pd.qcut(df_Stoppere['average_successfulDefensiveAction'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Shots blocked score'] = pd.qcut(df_Stoppere['average_shotsBlocked'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Defensive duels won score'] = pd.qcut(df_Stoppere['average_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Defensive duels won % score'] = pd.qcut(df_Stoppere['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Accurate passes to final third'] = pd.qcut(df_Stoppere['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Accurate through passes'] = pd.qcut(df_Stoppere['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Vertical passes'] = pd.qcut(df_Stoppere['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Through passes'] = pd.qcut(df_Stoppere['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Passes to final third'] = pd.qcut(df_Stoppere['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Progressive runs'] = pd.qcut(df_Stoppere['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Offensive duels won %'] = pd.qcut(df_Stoppere['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Successful dribbles %'] = pd.qcut(df_Stoppere['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Progressive passes score'] = pd.qcut(df_Stoppere['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Aerial duels won score'] = pd.qcut(df_Stoppere['average_fieldAerialDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Aerial duels won % score'] = pd.qcut(df_Stoppere['percent_aerialDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

        df_Stopperesæsonen = df_Stoppere.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
        df_Stopperesæsonen = df_Stoppere.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
        df_Stopperesæsonen['Pasningssikker'] = (df_Stopperesæsonen['Accurate passes score'] + df_Stopperesæsonen['Accurate long passes score'] + df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Accurate vertical passes score'])/6
        df_Stopperesæsonen['Spilintelligens defensivt'] = (df_Stopperesæsonen['Interceptions score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Shots blocked score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Defensive duels won % score']) /5
        df_Stopperesæsonen['Spilintelligens offensivt'] = (df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate passes to final third'] + df_Stopperesæsonen['Passes to final third'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Progressive passes score'] + df_Stopperesæsonen['Through passes'] + df_Stopperesæsonen['Accurate through passes']+ df_Stopperesæsonen['Progressive runs'] + df_Stopperesæsonen['Offensive duels won %'] + df_Stopperesæsonen['Successful dribbles %'])/11
        df_Stopperesæsonen['Nærkamps- og duelstærk'] = (df_Stopperesæsonen['Defensive duels won % score'] + df_Stopperesæsonen['Aerial duels won % score'] + df_Stopperesæsonen['Defensive duels won % score'])/3
        df_Stopperesæsonen['Samlet'] = (df_Stopperesæsonen['Pasningssikker'] + df_Stopperesæsonen['Spilintelligens defensivt'] + df_Stopperesæsonen['Spilintelligens offensivt'] + df_Stopperesæsonen['Nærkamps- og duelstærk'])/4

        df_Stopperesæsonen = df_Stopperesæsonen[['Pasningssikker','Spilintelligens defensivt','Spilintelligens offensivt','Nærkamps- og duelstærk','Samlet']]
        df_Stopperesæsonen = df_Stopperesæsonen.sort_values(by='Samlet',ascending=False)

        df_Stoppere = df_Stoppere[df_Stoppere['Team name'].str.contains('Horsens')]
        df_Stoppere['Pasningssikker'] = (df_Stoppere['Accurate passes score'] + df_Stoppere['Accurate long passes score'] + df_Stoppere['Forward passes score'] + df_Stoppere['Accurate forward passes score'] + df_Stoppere['Accurate progressive passes score'] + df_Stoppere['Accurate vertical passes score'])/6    
        df_Stoppere['Spilintelligens defensivt'] = (df_Stoppere['Interceptions score'] + df_Stoppere['Succesful defensive actions score'] + df_Stoppere['Shots blocked score'] + df_Stoppere['Succesful defensive actions score'] + df_Stoppere['Defensive duels won % score']) /5
        df_Stoppere['Spilintelligens offensivt'] = (df_Stoppere['Forward passes score'] + df_Stoppere['Accurate forward passes score'] + df_Stoppere['Accurate passes to final third'] + df_Stoppere['Passes to final third'] + df_Stoppere['Accurate progressive passes score'] + df_Stoppere['Progressive passes score'] + df_Stoppere['Through passes'] + df_Stoppere['Accurate through passes']+ df_Stoppere['Progressive runs'] + df_Stoppere['Offensive duels won %'] + df_Stoppere['Successful dribbles %'])/11
        df_Stoppere['Nærkamps- og duelstærk'] = (df_Stoppere['Defensive duels won % score'] + df_Stoppere['Aerial duels won % score'] + df_Stoppere['Defensive duels won % score'])/3
        df_Stoppere['Samlet'] = (df_Stoppere['Pasningssikker'] + df_Stoppere['Spilintelligens defensivt'] + df_Stoppere['Spilintelligens offensivt'] + df_Stoppere['Nærkamps- og duelstærk'])/4
        df_Stoppere = df_Stoppere[['Player name','Team name','label','total_minutesOnField_y','Pasningssikker','Spilintelligens defensivt','Spilintelligens offensivt','Nærkamps- og duelstærk','Samlet']]
        df_Stoppere = df_Stoppere.sort_values(by='Samlet',ascending=False)


        df_Stoppere = navne.merge(df_Stoppere)
        df_Stoppere = df_Stoppere.drop('Player Name',axis=1)
        df_Stoppere = df_Stoppere.drop('Player name',axis=1)    
        df_Stopperesæsonen = df_Stopperesæsonen.reset_index()
        df_Stopperesæsonen = navne.merge(df_Stopperesæsonen)
        df_Stoppere = navne.merge(df_Stoppere)
        df_Stopperesæsonen = df_Stopperesæsonen.drop('Player Name',axis=1)
        df_Stopperesæsonen = df_Stopperesæsonen.drop('Player name',axis=1)
        df_Stopperesæsonen = df_Stopperesæsonen.drop('label',axis=1)


        df_Centrale_midt = pd.merge(df_centraleminutter,df_Centrale_midt,on=('Player id'))
        df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['total_minutesOnField_y'] >=17]

        df_Centrale_midt['Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Passes #'] = pd.qcut(df_Centrale_midt['average_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Forward Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Forward Passes #'] = pd.qcut(df_Centrale_midt['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Long Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Long Passes #'] = pd.qcut(df_Centrale_midt['average_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Smart passes %'] = pd.qcut(df_Centrale_midt['percent_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Smart passes #'] = pd.qcut(df_Centrale_midt['average_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Key passes %'] = pd.qcut(df_Centrale_midt['percent_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Key passes #'] = pd.qcut(df_Centrale_midt['average_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Passes to final third %'] = pd.qcut(df_Centrale_midt['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Passes to final third #'] = pd.qcut(df_Centrale_midt['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Vertical passes %'] = pd.qcut(df_Centrale_midt['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Vertical passes #'] = pd.qcut(df_Centrale_midt['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Through passes %'] = pd.qcut(df_Centrale_midt['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Through passes #'] = pd.qcut(df_Centrale_midt['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Progressive passes %'] = pd.qcut(df_Centrale_midt['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Progressive passes #'] = pd.qcut(df_Centrale_midt['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Offensive duels %'] = pd.qcut(df_Centrale_midt['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Received passes'] = pd.qcut(df_Centrale_midt['average_receivedPass'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Succesful dribbles %'] = pd.qcut(df_Centrale_midt['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Succesful dribbles #'] = pd.qcut(df_Centrale_midt['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Duels won %'] = pd.qcut(df_Centrale_midt['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Duels won #'] = pd.qcut(df_Centrale_midt['average_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Interceptions'] = pd.qcut(df_Centrale_midt['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Counterpressing recoveries #'] = pd.qcut(df_Centrale_midt['average_counterpressingRecoveries'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Defensive duels won #'] = pd.qcut(df_Centrale_midt['average_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Defensive duels won %'] = pd.qcut(df_Centrale_midt['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

        df_Centrale_midtsæsonen = df_Centrale_midt.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
        df_Centrale_midtsæsonen = df_Centrale_midt.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
        df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #'] + df_Centrale_midtsæsonen['Forward Passes %'] + df_Centrale_midtsæsonen['Forward Passes #'] + df_Centrale_midtsæsonen['Long Passes %'] + df_Centrale_midtsæsonen['Long Passes #']+ df_Centrale_midtsæsonen['Smart passes %'] + df_Centrale_midtsæsonen['Smart passes #'] + + df_Centrale_midtsæsonen['Key passes %'] + df_Centrale_midtsæsonen['Key passes #'] + df_Centrale_midtsæsonen['Passes to final third %'] + df_Centrale_midtsæsonen['Passes to final third #']+ df_Centrale_midtsæsonen['Vertical passes %'] + df_Centrale_midtsæsonen['Vertical passes #']+ df_Centrale_midtsæsonen['Through passes %'] + df_Centrale_midtsæsonen['Through passes #']+ df_Centrale_midtsæsonen['Progressive passes %'] + df_Centrale_midtsæsonen['Progressive passes #'])/18
        df_Centrale_midtsæsonen['Boldfast'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #']+ df_Centrale_midtsæsonen['Offensive duels %'] + df_Centrale_midtsæsonen['Received passes'] + df_Centrale_midtsæsonen['Succesful dribbles %'] + df_Centrale_midtsæsonen['Succesful dribbles #'])/6
        df_Centrale_midtsæsonen['Spilintelligens defensivt'] = (df_Centrale_midtsæsonen['Duels won %'] + df_Centrale_midtsæsonen['Duels won #'] +df_Centrale_midtsæsonen['Interceptions'] + df_Centrale_midtsæsonen['Counterpressing recoveries #'] + df_Centrale_midtsæsonen['Defensive duels won %'] + df_Centrale_midtsæsonen['Defensive duels won #'])/6
        df_Centrale_midtsæsonen['Samlet'] = (df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] + df_Centrale_midtsæsonen['Boldfast'] + df_Centrale_midtsæsonen['Spilintelligens defensivt'])/3
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen[['Pasningssikker/Spilvendinger','Boldfast','Spilintelligens defensivt','Samlet']]
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.sort_values(by='Samlet',ascending=False)

        df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['Team name'].str.contains('Horsens')]
        df_Centrale_midt['Pasningssikker/Spilvendinger'] = (df_Centrale_midt['Passes %'] + df_Centrale_midt['Passes #'] + df_Centrale_midt['Forward Passes %'] + df_Centrale_midt['Forward Passes #'] + df_Centrale_midt['Long Passes %'] + df_Centrale_midt['Long Passes #']+ df_Centrale_midt['Smart passes %'] + df_Centrale_midt['Smart passes #'] + + df_Centrale_midt['Key passes %'] + df_Centrale_midt['Key passes #'] + df_Centrale_midt['Passes to final third %'] + df_Centrale_midt['Passes to final third #']+ df_Centrale_midt['Vertical passes %'] + df_Centrale_midt['Vertical passes #']+ df_Centrale_midt['Through passes %'] + df_Centrale_midt['Through passes #']+ df_Centrale_midt['Progressive passes %'] + df_Centrale_midt['Progressive passes #'])/18
        df_Centrale_midt['Boldfast'] = (df_Centrale_midt['Passes %'] + df_Centrale_midt['Passes #']+ df_Centrale_midt['Offensive duels %'] + df_Centrale_midt['Received passes'] + df_Centrale_midt['Succesful dribbles %'] + df_Centrale_midt['Succesful dribbles #'])/6
        df_Centrale_midt['Spilintelligens defensivt'] = (df_Centrale_midt['Duels won %'] + df_Centrale_midt['Duels won #'] +df_Centrale_midt['Interceptions'] + df_Centrale_midt['Counterpressing recoveries #'] + df_Centrale_midt['Defensive duels won %'] + df_Centrale_midt['Defensive duels won #'])/6
        df_Centrale_midt['Samlet'] = (df_Centrale_midt['Pasningssikker/Spilvendinger'] + df_Centrale_midt['Boldfast'] + df_Centrale_midt['Spilintelligens defensivt'])/3
        df_Centrale_midt = df_Centrale_midt[['Player name','Team name','label','total_minutesOnField_y','Pasningssikker/Spilvendinger','Boldfast','Spilintelligens defensivt','Samlet']]
        df_Centrale_midt = df_Centrale_midt.sort_values(by='Samlet',ascending=False)

        df_Centrale_midt = navne.merge(df_Centrale_midt)
        df_Centrale_midt = df_Centrale_midt.drop('Player Name',axis=1)
        df_Centrale_midt = df_Centrale_midt.drop('Player name',axis=1)    
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.reset_index()
        df_Centrale_midtsæsonen = navne.merge(df_Centrale_midtsæsonen)
        df_Centrale_midt = navne.merge(df_Centrale_midt)
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.drop('Player Name',axis=1)
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.drop('Player name',axis=1)
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.drop('label',axis=1)


        df_Kanter = pd.merge(df_kanterminutter,df_Kanter,on=('Player id'))
        df_Kanter = df_Kanter[df_Kanter['total_minutesOnField_y'] >=17]

        df_Kanter['Shots on target %'] = pd.qcut(df_Kanter['percent_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Shots on target #'] = pd.qcut(df_Kanter['average_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['XG'] = pd.qcut(df_Kanter['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Successful dribbles #'] = pd.qcut(df_Kanter['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Successful dribbles %'] = pd.qcut(df_Kanter['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Offensive duels %'] = pd.qcut(df_Kanter['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Offensive duels #'] = pd.qcut(df_Kanter['average_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Passes %'] = pd.qcut(df_Kanter['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Passes #'] = pd.qcut(df_Kanter['average_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Forward Passes %'] = pd.qcut(df_Kanter['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Forward Passes #'] = pd.qcut(df_Kanter['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Smart passes %'] = pd.qcut(df_Kanter['percent_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Smart passes #'] = pd.qcut(df_Kanter['average_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Key passes %'] = pd.qcut(df_Kanter['percent_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Key passes #'] = pd.qcut(df_Kanter['average_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Passes to final third %'] = pd.qcut(df_Kanter['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Passes to final third #'] = pd.qcut(df_Kanter['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Vertical passes %'] = pd.qcut(df_Kanter['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Vertical passes #'] = pd.qcut(df_Kanter['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Through passes %'] = pd.qcut(df_Kanter['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Through passes #'] = pd.qcut(df_Kanter['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Progressive passes %'] = pd.qcut(df_Kanter['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Progressive passes #'] = pd.qcut(df_Kanter['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Goal conversion %'] = pd.qcut(df_Kanter['percent_goalConversion'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['XG per 90'] = pd.qcut(df_Kanter['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['XA per 90'] = pd.qcut(df_Kanter['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Successful attacking actions'] = pd.qcut(df_Kanter['average_successfulAttackingActions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Progressive runs'] = pd.qcut(df_Kanter['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Accelerations score'] = pd.qcut(df_Kanter['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

        df_Kantersæsonen = df_Kanter.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    
        df_Kantersæsonen = df_Kanter.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

        df_Kantersæsonen['Sparkefærdigheder'] = (df_Kantersæsonen['Shots on target %'] + df_Kantersæsonen['Shots on target #'] + df_Kantersæsonen['XG'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Vertical passes %'])/6
        df_Kantersæsonen['Kombinationsstærk'] = (df_Kantersæsonen['Passes %'] + df_Kantersæsonen['Passes #'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Forward Passes #'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Passes to final third #'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
        df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] = (df_Kantersæsonen['XA per 90'] + df_Kantersæsonen['XG per 90'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Smart passes %'] + df_Kantersæsonen['Smart passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Key passes %'] + df_Kantersæsonen['Key passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
        df_Kantersæsonen['1v1 offensivt'] = (df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Offensive duels #'] + df_Kantersæsonen['Offensive duels %'] + df_Kantersæsonen['Progressive runs'])/5
        df_Kantersæsonen['Fart'] = (df_Kantersæsonen['Progressive runs'] + df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Accelerations score'])/5
        df_Kantersæsonen['Samlet'] = (df_Kantersæsonen['Sparkefærdigheder'] + df_Kantersæsonen['Kombinationsstærk'] + df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] + df_Kantersæsonen['1v1 offensivt'] + df_Kantersæsonen['Fart'])/5
        df_Kantersæsonen = df_Kantersæsonen[['Sparkefærdigheder','Kombinationsstærk','Spilintelligens offensivt/indlægsstærk','1v1 offensivt','Fart','Samlet']]
        df_Kantersæsonen = df_Kantersæsonen.sort_values(by='Samlet',ascending=False)
        df_Kanter = df_Kanter[df_Kanter['Team name'].str.contains('Horsens')]
        df_Kanter['Sparkefærdigheder'] = (df_Kanter['Shots on target %'] + df_Kanter['Shots on target #'] + df_Kanter['XG'] + df_Kanter['Passes to final third %'] + df_Kanter['Forward Passes %'] + df_Kanter['Vertical passes %'])/6
        df_Kanter['Kombinationsstærk'] = (df_Kanter['Passes %'] + df_Kanter['Passes #'] + df_Kanter['Forward Passes %'] + df_Kanter['Forward Passes #'] + df_Kanter['Passes to final third %'] + df_Kanter['Passes to final third #'] + df_Kanter['Through passes %'] + df_Kanter['Through passes #'] + df_Kanter['Progressive passes %'] + df_Kanter['Progressive passes #'] + df_Kanter['Successful attacking actions'])/11
        df_Kanter['Spilintelligens offensivt/indlægsstærk'] = (df_Kanter['XA per 90'] + df_Kanter['XG per 90'] + df_Kanter['Through passes %'] + df_Kanter['Through passes #'] + df_Kanter['Smart passes %'] + df_Kanter['Smart passes #'] + df_Kanter['Progressive passes %'] + df_Kanter['Progressive passes #'] + df_Kanter['Key passes %'] + df_Kanter['Key passes #'] + df_Kanter['Successful attacking actions'])/11
        df_Kanter['1v1 offensivt'] = (df_Kanter['Successful dribbles #'] + df_Kanter['Successful dribbles %'] + df_Kanter['Offensive duels #'] + df_Kanter['Offensive duels %'] + df_Kanter['Progressive runs'])/5
        df_Kanter['Fart'] = (df_Kanter['Progressive runs'] + df_Kanter['Successful dribbles #'] + df_Kanter['Successful dribbles %'] + df_Kanter['Accelerations score'])/5
        df_Kanter['Samlet'] = (df_Kanter['Sparkefærdigheder'] + df_Kanter['Kombinationsstærk'] + df_Kanter['Spilintelligens offensivt/indlægsstærk'] + df_Kanter['1v1 offensivt'] + df_Kanter['Fart'])/5
        df_Kanter = df_Kanter[['Player name','Team name','label','total_minutesOnField_y','Sparkefærdigheder','Kombinationsstærk','Spilintelligens offensivt/indlægsstærk','1v1 offensivt','Fart','Samlet']]
        df_Kanter = df_Kanter.sort_values(by='Samlet',ascending=False)

        df_Kanter = navne.merge(df_Kanter)
        df_Kanter = df_Kanter.drop('Player Name',axis=1)
        df_Kanter = df_Kanter.drop('Player name',axis=1)    
        df_Kantersæsonen=df_Kantersæsonen.reset_index()
        df_Kantersæsonen = navne.merge(df_Kantersæsonen)
        df_Kanter = navne.merge(df_Kanter)
        df_Kantersæsonen= df_Kantersæsonen.drop('Player Name',axis=1)
        df_Kantersæsonen = df_Kantersæsonen.drop('Player name',axis=1)
        df_Kantersæsonen = df_Kantersæsonen.drop('label',axis=1)
    
        
        df_Angribere = pd.merge(df_angribereminutter,df_Angribere,on=('Player id'))
        df_Angribere = df_Angribere[df_Angribere['total_minutesOnField_y'] >=17]

        df_Angribere['Målfarlighed udregning'] = df_Angribere['average_goals'] - df_Angribere['average_xgShot']
        df_Angribere['Målfarlighed score'] =  pd.qcut(df_Angribere['Målfarlighed udregning'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['xG per 90 score'] = pd.qcut(df_Angribere['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Goals per 90 score'] = pd.qcut(df_Angribere['average_goals'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)  
        df_Angribere['Shots on target, % score'] = pd.qcut(df_Angribere['percent_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)   
        df_Angribere['Offensive duels won, % score'] = pd.qcut(df_Angribere['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Duels won, % score'] = pd.qcut(df_Angribere['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Accurate passes, % score'] = pd.qcut(df_Angribere['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Successful dribbles, % score'] = pd.qcut(df_Angribere['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['xA per 90 score'] = pd.qcut(df_Angribere['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Touches in box per 90 score'] = pd.qcut(df_Angribere['average_touchInBox'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Progressive runs'] = pd.qcut(df_Angribere['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Accelerations score'] = pd.qcut(df_Angribere['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Progressive passes per 90 score'] = pd.qcut(df_Angribere['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Successful attacking actions per 90 score'] = pd.qcut(df_Angribere['average_successfulAttackingActions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Successful dribbles #'] = pd.qcut(df_Angribere['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

        df_Angriberesæsonen = df_Angribere.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)

        df_Angriberesæsonen = df_Angribere.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

        df_Angriberesæsonen['Sparkefærdigheder'] = (df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Goals per 90 score'] + df_Angriberesæsonen['Shots on target, % score'])/4
        df_Angriberesæsonen['Boldfast'] = (df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Duels won, % score'] + df_Angriberesæsonen['Accurate passes, % score'] + df_Angriberesæsonen['Successful dribbles, % score'])/5
        df_Angriberesæsonen['Spilintelligens offensivt'] = (df_Angriberesæsonen['xA per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['Progressive passes per 90 score'] + df_Angriberesæsonen['Successful attacking actions per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['xG per 90 score'])/7
        df_Angriberesæsonen['Målfarlighed'] = (df_Angriberesæsonen['xG per 90 score']+df_Angriberesæsonen['Goals per 90 score']+df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Målfarlighed score'])/4
        df_Angriberesæsonen['Fart'] = (df_Angriberesæsonen['Progressive runs'] + + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Successful dribbles #'] + df_Angriberesæsonen['Successful dribbles, % score'] + df_Angriberesæsonen['Accelerations score'] + df_Angriberesæsonen['Offensive duels won, % score'])/7
        df_Angriberesæsonen = df_Angriberesæsonen[['Sparkefærdigheder','Boldfast','Spilintelligens offensivt','Målfarlighed','Fart']]
        df_Angriberesæsonen['Samlet'] = (df_Angriberesæsonen['Sparkefærdigheder']+df_Angriberesæsonen['Boldfast']+df_Angriberesæsonen['Spilintelligens offensivt']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Fart'])/7
        df_Angriberesæsonen = df_Angriberesæsonen.sort_values(by='Samlet',ascending=False)
        df_Angriberesæsonen = df_Angriberesæsonen[df_Angriberesæsonen.index.get_level_values('Team name').str.contains('Horsens')]

        df_Angribere = df_Angribere[df_Angribere['Team name'].str.contains('Horsens')]
        df_Angribere['Sparkefærdigheder'] = (df_Angribere['xG per 90 score'] + df_Angribere['xG per 90 score'] + df_Angribere['Goals per 90 score'] + df_Angribere['Shots on target, % score'])/4
        df_Angribere['Boldfast'] = (df_Angribere['Offensive duels won, % score'] + df_Angribere['Offensive duels won, % score'] + df_Angribere['Duels won, % score'] + df_Angribere['Accurate passes, % score'] + df_Angribere['Successful dribbles, % score'])/5
        df_Angribere['Spilintelligens offensivt'] = (df_Angribere['xA per 90 score'] + df_Angribere['xG per 90 score'] + df_Angribere['Touches in box per 90 score'] + df_Angribere['Progressive passes per 90 score'] + df_Angribere['Successful attacking actions per 90 score'] + df_Angribere['Touches in box per 90 score'] + df_Angribere['xG per 90 score'])/7
        df_Angribere['Målfarlighed'] = (df_Angribere['xG per 90 score']+df_Angribere['Goals per 90 score']+df_Angribere['xG per 90 score'] + df_Angribere['Målfarlighed score'])/4
        df_Angribere['Fart'] = (df_Angribere['Progressive runs'] + + df_Angribere['Progressive runs'] + df_Angribere['Progressive runs'] + df_Angribere['Successful dribbles #'] + df_Angribere['Successful dribbles, % score'] + df_Angribere['Accelerations score'] + df_Angribere['Offensive duels won, % score'])/7
        df_Angribere = df_Angribere[['Player name','Team name','label','total_minutesOnField_y','Sparkefærdigheder','Boldfast','Spilintelligens offensivt','Målfarlighed','Fart']]
        df_Angribere['Samlet'] = (df_Angribere['Sparkefærdigheder']+df_Angribere['Boldfast']+df_Angribere['Spilintelligens offensivt']+df_Angribere['Målfarlighed']+df_Angribere['Målfarlighed']+df_Angribere['Målfarlighed']+df_Angribere['Fart'])/7
        df_Angribere = df_Angribere.sort_values(by='Samlet',ascending=False)
        
        kampe = df['label']
        kampe = kampe[kampe.str.contains('Horsens')]
        kampe = kampe.drop_duplicates(keep='first')  
        
        df_Angribere = navne.merge(df_Angribere)
        df_Angribere = df_Angribere.drop('Player Name',axis=1)
        df_Angribere = df_Angribere.drop('Player name',axis=1)
        df_Angriberesæsonen=df_Angriberesæsonen.reset_index()
        df_Angriberesæsonen = navne.merge(df_Angriberesæsonen)
        df_Angribere = navne.merge(df_Angribere)
        df_Angriberesæsonen= df_Angriberesæsonen.drop('Player Name',axis=1)
        df_Angriberesæsonen = df_Angriberesæsonen.drop('Player name',axis=1)
        df_Angriberesæsonen = df_Angriberesæsonen.drop('label',axis=1)
        
        option2 = st.selectbox('Vælg spiller',navneliste)
        df_Angriberesæsonen = df_Angriberesæsonen[df_Angriberesæsonen['Spillere'].str.contains(option2)]
        df_Angribere = df_Angribere[df_Angribere['Spillere'].str.contains(option2)]
        df_Kantersæsonen = df_Kantersæsonen[df_Kantersæsonen['Spillere'].str.contains(option2)]
        df_Kanter = df_Kanter[df_Kanter['Spillere'].str.contains(option2)]
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen[df_Centrale_midtsæsonen['Spillere'].str.contains(option2)]
        df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['Spillere'].str.contains(option2)]
        df_Stopperesæsonen = df_Stopperesæsonen[df_Stopperesæsonen['Spillere'].str.contains(option2)]
        df_Stoppere = df_Stoppere[df_Stoppere['Spillere'].str.contains(option2)]
        df_backssæsonen = df_backssæsonen[df_backs['Spillere'].str.contains(option2)]
        df_backs = df_backs[df_backs['Spillere'].str.contains(option2)]

        option = st.multiselect('Vælg kamp (Hvis ingen kamp er valgt, vises alle)',kampe)
        if len(option) > 0:
            temp_select = option
        else:
            temp_select = kampe

        df_backs = df_backs[df_backs['label'].isin(temp_select)]
        df_backs = df_backs.drop('label',axis=1)
        df_backssæsonen = df_backssæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()
        
        df_backs = df_backs.groupby(['Spillere','Trup','Team name']).agg({
        'total_minutesOnField_y':'sum',
        'Indlægsstærk':'mean',
        '1v1 færdigheder':'mean',
        'Spilintelligens defensivt':'mean',
        'Fart':'mean',
        'Samlet':'mean'
        })

        df_backs = df_backs.sort_values(by='Samlet',ascending=False)
        df_backs = df_backs.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
        df_backs = df_backs.reset_index()
        df_backs = df_backs.set_index(['Spillere','Trup','Team name'])
        df_backssæsonen = df_backssæsonen.reset_index()
        df_backssæsonen = df_backssæsonen.set_index(['Spillere','Trup','Team name'])
        df_backs = pd.concat([df_backs,df_backssæsonen],axis=0)        

        df_Stoppere = df_Stoppere[df_Stoppere['label'].isin(temp_select)]
        df_Stoppere = df_Stoppere.drop('label',axis=1)
        df_Stopperesæsonen = df_Stopperesæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()
        
        df_Stoppere = df_Stoppere.groupby(['Spillere','Trup','Team name']).agg({
        'total_minutesOnField_y':'sum',
        'Pasningssikker':'mean',
        'Spilintelligens offensivt':'mean',
        'Spilintelligens defensivt':'mean',
        'Nærkamps- og duelstærk':'mean',
        'Samlet':'mean'
        })

        df_Stoppere = df_Stoppere.sort_values(by='Samlet',ascending=False)
        df_Stoppere = df_Stoppere.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
        df_Stoppere = df_Stoppere.reset_index()
        df_Stoppere = df_Stoppere.set_index(['Spillere','Trup','Team name'])
        df_Stopperesæsonen = df_Stopperesæsonen.reset_index()
        df_Stopperesæsonen = df_Stopperesæsonen.set_index(['Spillere','Trup','Team name'])
        df_Stoppere = pd.concat([df_Stoppere,df_Stopperesæsonen],axis=0)

        df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['label'].isin(temp_select)]
        df_Centrale_midt = df_Centrale_midt.drop('label',axis=1)
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()
        
        df_Centrale_midt = df_Centrale_midt.groupby(['Spillere','Trup','Team name']).agg({
        'total_minutesOnField_y':'sum',
        'Pasningssikker/Spilvendinger':'mean',
        'Boldfast':'mean',
        'Spilintelligens defensivt':'mean',
        'Samlet':'mean'
        })

        df_Centrale_midt = df_Centrale_midt.sort_values(by='Samlet',ascending=False)
        df_Centrale_midt = df_Centrale_midt.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
        df_Centrale_midt = df_Centrale_midt.reset_index()
        df_Centrale_midt = df_Centrale_midt.set_index(['Spillere','Trup','Team name'])
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.reset_index()
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.set_index(['Spillere','Trup','Team name'])
        df_Centrale_midt = pd.concat([df_Centrale_midt,df_Centrale_midtsæsonen],axis=0)
    
            
        df_Kanter = df_Kanter[df_Kanter['label'].isin(temp_select)]
        df_Kanter = df_Kanter.drop('label',axis=1)
        df_Kantersæsonen = df_Kantersæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()
        
        df_Kanter = df_Kanter.groupby(['Spillere','Trup','Team name']).agg({
        'total_minutesOnField_y':'sum',
        'Sparkefærdigheder':'mean',
        'Kombinationsstærk':'mean',
        'Spilintelligens offensivt/indlægsstærk':'mean',
        '1v1 offensivt':'mean',
        'Fart':'mean',
        'Samlet':'mean'
        })
        
        df_Kanter = df_Kanter.sort_values(by='Samlet',ascending=False)
        df_Kanter = df_Kanter.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
        df_Kanter = df_Kanter.reset_index()
        df_Kanter = df_Kanter.set_index(['Spillere','Trup','Team name'])
        df_Kantersæsonen = df_Kantersæsonen.reset_index()
        df_Kantersæsonen = df_Kantersæsonen.set_index(['Spillere','Trup','Team name'])
        df_Kanter = pd.concat([df_Kanter,df_Kantersæsonen],axis=0)

        
        df_Angribere = df_Angribere[df_Angribere['label'].isin(temp_select)]
        df_Angribere = df_Angribere.drop('label',axis=1)
        df_Angriberesæsonen = df_Angriberesæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()

        df_Angribere = df_Angribere.groupby(['Spillere','Trup','Team name']).agg({
        'total_minutesOnField_y':'sum',
        'Sparkefærdigheder': 'mean',
        'Boldfast': 'mean',
        'Spilintelligens offensivt':'mean',
        'Målfarlighed':'mean',
        'Fart':'mean',
        'Samlet':'mean',
        })

        df_Angribere = df_Angribere.sort_values(by = 'Samlet',ascending=False)
        df_Angribere = df_Angribere.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
        df_Angribere = df_Angribere.reset_index()
        df_Angribere = df_Angribere.set_index(['Spillere','Trup','Team name'])
        df_Angriberesæsonen = df_Angriberesæsonen.reset_index()
        df_Angriberesæsonen = df_Angriberesæsonen.set_index(['Spillere','Trup','Team name'])
        df_Angribere = pd.concat([df_Angribere,df_Angriberesæsonen],axis=0)
        #st.dataframe(df_Angribere)
        #st.write('Angribere')
        dataframe_names = ['Stopper', 'Back', 'Central midt', 'Kant', 'Angriber']

        # Create the selectbox in Streamlit
        selected_dataframe = st.selectbox('Position', options=dataframe_names)

        # Based on the selected dataframe, retrieve the corresponding dataframe object
        if selected_dataframe == 'Stopper':
            selected_df = df_Stoppere
        elif selected_dataframe == 'Back':
            selected_df = df_backs
        elif selected_dataframe == 'Central midt':
            selected_df = df_Centrale_midt
        elif selected_dataframe == 'Kant':
            selected_df = df_Kanter
        elif selected_dataframe == 'Angriber':
            selected_df = df_Angribere

        st.dataframe(selected_df)
        df_filtered = selected_df.iloc[:, 1:]

        # Create a scatterpolar plot using plotly
        fig = go.Figure()

        # Iterate over each row in the dataframe
        for _, row in df_filtered.iterrows():
            fig.add_trace(go.Scatterpolar(
                r=row.values,
                theta=df_filtered.columns,
                fill='toself'
            ))
        fig.data[0].name = 'Valgte periode'
        fig.data[1].name = 'Hele sæsonen'
        # Set plot title and layout
        fig.update_layout(
            title='Scatterpolar Plot',
            template='plotly_dark',
            polar=dict(
                radialaxis=dict
                    (visible=True,
                    range=[1,5]
                )
            )
        )
        # Render the plot within Streamlit
        st.plotly_chart(fig)
    def U17():
        import pandas as pd
        import streamlit as st
        import json
        from pandas import json_normalize
        import ast
        from dateutil import parser
        import plotly.graph_objects as go
        navne = pd.read_excel('Navne.xlsx')
        navne = navne[navne['Trup'].str.contains('U17')]
        navneliste = navne['Spillere'].sort_values(ascending=True)
        df = pd.read_csv('Individuelt dashboard U17.csv')
        df.rename(columns={'playerId': 'Player id'}, inplace=True)
        df = df.astype(str)
        dfevents = pd.read_csv('U17 eventdata alle.csv',low_memory=False)
        dfevents = dfevents[['Player id','Player name','team_name','label','date','matchId']]
        dfspillernavn = df[['Player id','matchId','positions','average','percent','total']]
        dfspillernavn = dfspillernavn.astype(str)
        dfevents['Player id'] = dfevents['Player id'].astype(str)
        dfevents['matchId'] = dfevents['matchId'].astype(str)
        df = dfspillernavn.merge(dfevents)

        df['Player&matchId'] = df['Player id'] + df['matchId']
        df['Player&matchId'] = df['Player&matchId'].drop_duplicates(keep='first')
        df = df.dropna()
        df = df[['Player id','Player name','team_name','matchId','label','date','positions','average','percent','total']]

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
        df = df[['Player name','team_name','matchId','label','date','position_names','position_codes','average','percent','total']]
        df = df.rename(columns={'team_name':'Team name'})
        df['percent'] = df['percent'].apply(lambda x: ast.literal_eval(x))

        # Create a new dataframe with the columns as the dictionary keys and the values as a list
        new_df = pd.DataFrame(df['percent'].to_list(), index=df.index).add_prefix('percent_')

        # Concatenate the new dataframe with the original dataframe
        df = pd.concat([df, new_df], axis=1)

        # Drop the original 'percent' column
        df = df.drop('percent', axis=1)

        df['total'] = df['total'].apply(lambda x: ast.literal_eval(x))

        # Create a new dataframe with the columns as the dictionary keys and the values as a list
        new_df = pd.DataFrame(df['total'].to_list(), index=df.index).add_prefix('total_')

        # Concatenate the new dataframe with the original dataframe
        df = pd.concat([df, new_df], axis=1)

        # Drop the original 'percent' column
        df = df.drop('total', axis=1)

        df['average'] = df['average'].apply(lambda x: ast.literal_eval(x))

        # Create a new dataframe with the columns as the dictionary keys and the values as a list
        new_df = pd.DataFrame(df['average'].to_list(), index=df.index).add_prefix('average_')

        # Concatenate the new dataframe with the original dataframe
        df = pd.concat([df, new_df], axis=1)


        # Drop the original 'percent' column
        df = df.drop('average', axis=1)
        df['position_codes'] = df['position_codes'].astype(str)
        #df['date'] = df['date'].astype(str)
        #df['date'] = df['date'].apply(lambda x: parser.parse(x))

        # Sort the dataframe by the 'date' column
        #df = df.sort_values(by='date',ascending=False)

        # Format the 'date' column to day-month-year format
        #df['date'] = df['date'].apply(lambda x: x.strftime('%d-%m-%Y'))
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date',ascending=False)

        df_backs = df[df['position_codes'].str.contains('|'.join(['lb', 'rb']))]
        df_backsminutter = df_backs[['Player name','Team name','total_minutesOnField']]
        df_backsminutter = df_backsminutter.groupby(['Player id']).sum(numeric_only=True)
        df_backsminutter = df_backsminutter[df_backsminutter['total_minutesOnField'] >= 300]

        df_Stoppere = df[df['position_codes'].str.contains('|'.join(['cb']))]
        df_stoppereminutter = df_Stoppere[['Player name','Team name','total_minutesOnField']]
        df_stoppereminutter = df_stoppereminutter.groupby(['Player id']).sum(numeric_only=True)
        df_stoppereminutter = df_stoppereminutter[df_stoppereminutter['total_minutesOnField'] >= 300]

        df_Centrale_midt = df[df['position_codes'].str.contains('|'.join(['cm','amf','dmf']))]
        df_centraleminutter = df_Centrale_midt[['Player name','Team name','total_minutesOnField']]
        df_centraleminutter = df_centraleminutter.groupby(['Player id']).sum(numeric_only=True)
        df_centraleminutter = df_centraleminutter[df_centraleminutter['total_minutesOnField'] >= 300]

        df_Kanter = df[df['position_codes'].str.contains('|'.join(['rw','lw','ramf','lamf']))]
        df_kanterminutter = df_Kanter[['Player name','Team name','total_minutesOnField']]
        df_kanterminutter = df_kanterminutter.groupby(['Player id']).sum(numeric_only=True)
        df_kanterminutter = df_kanterminutter[df_kanterminutter['total_minutesOnField'] >=300]


        df_Angribere = df[df['position_codes'].str.contains('|'.join(['cf']))]
        df_angribereminutter = df_Angribere[['Player name','Team name','total_minutesOnField']]
        df_angribereminutter = df_angribereminutter.groupby(['Player id']).sum(numeric_only=True)
        df_angribereminutter = df_angribereminutter[df_angribereminutter['total_minutesOnField'] >= 300]


        df_backs = pd.merge(df_backsminutter,df_backs,on=('Player id'))
        df_backs = df_backs[df_backs['total_minutesOnField_y'] >=17]

        df_backs['Accurate crosses score'] = pd.qcut(df_backs['percent_successfulCrosses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Number of crosses score'] = pd.qcut(df_backs['average_crosses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['XA score'] = pd.qcut(df_backs['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Passes to final third score'] = pd.qcut(df_backs['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Successful dribbles score'] = pd.qcut(df_backs['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Defensive duels won score'] = pd.qcut(df_backs['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Progressive runs score'] = pd.qcut(df_backs['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Offensive duels won score'] = pd.qcut(df_backs['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Accelerations score'] = pd.qcut(df_backs['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Duels won score'] = pd.qcut(df_backs['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Interceptions score'] = pd.qcut(df_backs['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Successful defensive actions score'] = pd.qcut(df_backs['average_successfulDefensiveAction'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backssæsonen = df_backs[['Player name','Team name','label','total_minutesOnField_x','total_minutesOnField_y','Number of crosses score','Accurate crosses score','XA score','Passes to final third score','Successful dribbles score','Defensive duels won score','Progressive runs score','Offensive duels won score','Accelerations score','Duels won score','Interceptions score','Successful defensive actions score']]
        df_backssæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
        df_backssæsonen = df_backssæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

        df_backssæsonen['Indlægsstærk'] = (df_backssæsonen['Number of crosses score'] + df_backssæsonen['Accurate crosses score'] + df_backssæsonen['XA score'] + df_backssæsonen['Passes to final third score'])/4
        df_backssæsonen['1v1 færdigheder'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Defensive duels won score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'] + df_backssæsonen['Duels won score'])/6
        df_backssæsonen['Spilintelligens defensivt'] = (df_backssæsonen['Interceptions score'] + df_backssæsonen['Successful defensive actions score'] + df_backssæsonen['Duels won score'] + df_backssæsonen['Defensive duels won score'])/4
        df_backssæsonen['Fart'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'])/4
        df_backssæsonen ['Samlet'] = (df_backssæsonen['Indlægsstærk'] + df_backssæsonen['1v1 færdigheder'] + df_backssæsonen['Spilintelligens defensivt'] + df_backssæsonen['Fart'])/4
        df_backssæsonen = df_backssæsonen[['Indlægsstærk','1v1 færdigheder','Spilintelligens defensivt','Fart','Samlet']]
        df_backssæsonen = df_backssæsonen.sort_values(by='Samlet',ascending=False)

        df_backs['Indlægsstærk'] = (df_backs['Number of crosses score'] + df_backs['Accurate crosses score'] + df_backs['XA score'] + df_backs['Passes to final third score'])/4
        df_backs['1v1 færdigheder'] = (df_backs['Successful dribbles score'] + df_backs['Defensive duels won score'] + df_backs['Progressive runs score'] + df_backs['Offensive duels won score'] + df_backs['Accelerations score'] + df_backs['Duels won score'])/6
        df_backs['Spilintelligens defensivt'] = (df_backs['Interceptions score'] + df_backs['Successful defensive actions score'] + df_backs['Duels won score'] + df_backs['Defensive duels won score'])/4
        df_backs['Fart'] = (df_backs['Successful dribbles score'] + df_backs['Progressive runs score'] + df_backs['Offensive duels won score'] + df_backs['Accelerations score'])/4
        df_backs['Samlet'] = (df_backs['Indlægsstærk'] + df_backs['1v1 færdigheder'] + df_backs['Spilintelligens defensivt'] + df_backs['Fart'])/4


        df_backs = df_backs[['Player name','Team name','label','total_minutesOnField_y','Indlægsstærk','1v1 færdigheder','Spilintelligens defensivt','Fart','Samlet']]
        df_backs = df_backs.sort_values(by='Samlet',ascending=False)
        
        df_backs = navne.merge(df_backs)
        df_backs = df_backs.drop('Player Name',axis=1)
        df_backs = df_backs.drop('Player name',axis=1)    
        df_backssæsonen = df_backssæsonen.reset_index()
        df_backssæsonen = navne.merge(df_backssæsonen)
        df_backs = navne.merge(df_backs)
        df_backssæsonen = df_backssæsonen.drop('Player Name',axis=1)
        df_backssæsonen = df_backssæsonen.drop('Player name',axis=1)
        df_backssæsonen = df_backssæsonen.drop('label',axis=1)


        df_Stoppere = pd.merge(df_stoppereminutter,df_Stoppere,on=('Player id'))
        df_Stoppere = df_Stoppere[df_Stoppere['total_minutesOnField_y'] >=17]

        df_Stoppere['Accurate passes score'] = pd.qcut(df_Stoppere['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Accurate long passes score'] = pd.qcut(df_Stoppere['percent_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Forward passes score'] = pd.qcut(df_Stoppere['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Accurate forward passes score'] = pd.qcut(df_Stoppere['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Accurate progressive passes score'] = pd.qcut(df_Stoppere['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Accurate vertical passes score'] = pd.qcut(df_Stoppere['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Interceptions score'] = pd.qcut(df_Stoppere['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Succesful defensive actions score'] = pd.qcut(df_Stoppere['average_successfulDefensiveAction'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Shots blocked score'] = pd.qcut(df_Stoppere['average_shotsBlocked'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Defensive duels won score'] = pd.qcut(df_Stoppere['average_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Defensive duels won % score'] = pd.qcut(df_Stoppere['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Accurate passes to final third'] = pd.qcut(df_Stoppere['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Accurate through passes'] = pd.qcut(df_Stoppere['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Vertical passes'] = pd.qcut(df_Stoppere['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Through passes'] = pd.qcut(df_Stoppere['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Passes to final third'] = pd.qcut(df_Stoppere['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Progressive runs'] = pd.qcut(df_Stoppere['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Offensive duels won %'] = pd.qcut(df_Stoppere['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Successful dribbles %'] = pd.qcut(df_Stoppere['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Progressive passes score'] = pd.qcut(df_Stoppere['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Aerial duels won score'] = pd.qcut(df_Stoppere['average_fieldAerialDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Aerial duels won % score'] = pd.qcut(df_Stoppere['percent_aerialDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

        df_Stopperesæsonen = df_Stoppere.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
        df_Stopperesæsonen = df_Stoppere.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
        df_Stopperesæsonen['Pasningssikker'] = (df_Stopperesæsonen['Accurate passes score'] + df_Stopperesæsonen['Accurate long passes score'] + df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Accurate vertical passes score'])/6
        df_Stopperesæsonen['Spilintelligens defensivt'] = (df_Stopperesæsonen['Interceptions score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Shots blocked score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Defensive duels won % score']) /5
        df_Stopperesæsonen['Spilintelligens offensivt'] = (df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate passes to final third'] + df_Stopperesæsonen['Passes to final third'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Progressive passes score'] + df_Stopperesæsonen['Through passes'] + df_Stopperesæsonen['Accurate through passes']+ df_Stopperesæsonen['Progressive runs'] + df_Stopperesæsonen['Offensive duels won %'] + df_Stopperesæsonen['Successful dribbles %'])/11
        df_Stopperesæsonen['Nærkamps- og duelstærk'] = (df_Stopperesæsonen['Defensive duels won % score'] + df_Stopperesæsonen['Aerial duels won % score'] + df_Stopperesæsonen['Defensive duels won % score'])/3
        df_Stopperesæsonen['Samlet'] = (df_Stopperesæsonen['Pasningssikker'] + df_Stopperesæsonen['Spilintelligens defensivt'] + df_Stopperesæsonen['Spilintelligens offensivt'] + df_Stopperesæsonen['Nærkamps- og duelstærk'])/4

        df_Stopperesæsonen = df_Stopperesæsonen[['Pasningssikker','Spilintelligens defensivt','Spilintelligens offensivt','Nærkamps- og duelstærk','Samlet']]
        df_Stopperesæsonen = df_Stopperesæsonen.sort_values(by='Samlet',ascending=False)

        df_Stoppere = df_Stoppere[df_Stoppere['Team name'].str.contains('Horsens')]
        df_Stoppere['Pasningssikker'] = (df_Stoppere['Accurate passes score'] + df_Stoppere['Accurate long passes score'] + df_Stoppere['Forward passes score'] + df_Stoppere['Accurate forward passes score'] + df_Stoppere['Accurate progressive passes score'] + df_Stoppere['Accurate vertical passes score'])/6    
        df_Stoppere['Spilintelligens defensivt'] = (df_Stoppere['Interceptions score'] + df_Stoppere['Succesful defensive actions score'] + df_Stoppere['Shots blocked score'] + df_Stoppere['Succesful defensive actions score'] + df_Stoppere['Defensive duels won % score']) /5
        df_Stoppere['Spilintelligens offensivt'] = (df_Stoppere['Forward passes score'] + df_Stoppere['Accurate forward passes score'] + df_Stoppere['Accurate passes to final third'] + df_Stoppere['Passes to final third'] + df_Stoppere['Accurate progressive passes score'] + df_Stoppere['Progressive passes score'] + df_Stoppere['Through passes'] + df_Stoppere['Accurate through passes']+ df_Stoppere['Progressive runs'] + df_Stoppere['Offensive duels won %'] + df_Stoppere['Successful dribbles %'])/11
        df_Stoppere['Nærkamps- og duelstærk'] = (df_Stoppere['Defensive duels won % score'] + df_Stoppere['Aerial duels won % score'] + df_Stoppere['Defensive duels won % score'])/3
        df_Stoppere['Samlet'] = (df_Stoppere['Pasningssikker'] + df_Stoppere['Spilintelligens defensivt'] + df_Stoppere['Spilintelligens offensivt'] + df_Stoppere['Nærkamps- og duelstærk'])/4
        df_Stoppere = df_Stoppere[['Player name','Team name','label','total_minutesOnField_y','Pasningssikker','Spilintelligens defensivt','Spilintelligens offensivt','Nærkamps- og duelstærk','Samlet']]
        df_Stoppere = df_Stoppere.sort_values(by='Samlet',ascending=False)


        df_Stoppere = navne.merge(df_Stoppere)
        df_Stoppere = df_Stoppere.drop('Player Name',axis=1)
        df_Stoppere = df_Stoppere.drop('Player name',axis=1)    
        df_Stopperesæsonen = df_Stopperesæsonen.reset_index()
        df_Stopperesæsonen = navne.merge(df_Stopperesæsonen)
        df_Stoppere = navne.merge(df_Stoppere)
        df_Stopperesæsonen = df_Stopperesæsonen.drop('Player Name',axis=1)
        df_Stopperesæsonen = df_Stopperesæsonen.drop('Player name',axis=1)
        df_Stopperesæsonen = df_Stopperesæsonen.drop('label',axis=1)


        df_Centrale_midt = pd.merge(df_centraleminutter,df_Centrale_midt,on=('Player id'))
        df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['total_minutesOnField_y'] >=17]

        df_Centrale_midt['Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Passes #'] = pd.qcut(df_Centrale_midt['average_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Forward Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Forward Passes #'] = pd.qcut(df_Centrale_midt['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Long Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Long Passes #'] = pd.qcut(df_Centrale_midt['average_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Smart passes %'] = pd.qcut(df_Centrale_midt['percent_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Smart passes #'] = pd.qcut(df_Centrale_midt['average_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Key passes %'] = pd.qcut(df_Centrale_midt['percent_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Key passes #'] = pd.qcut(df_Centrale_midt['average_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Passes to final third %'] = pd.qcut(df_Centrale_midt['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Passes to final third #'] = pd.qcut(df_Centrale_midt['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Vertical passes %'] = pd.qcut(df_Centrale_midt['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Vertical passes #'] = pd.qcut(df_Centrale_midt['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Through passes %'] = pd.qcut(df_Centrale_midt['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Through passes #'] = pd.qcut(df_Centrale_midt['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Progressive passes %'] = pd.qcut(df_Centrale_midt['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Progressive passes #'] = pd.qcut(df_Centrale_midt['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Offensive duels %'] = pd.qcut(df_Centrale_midt['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Received passes'] = pd.qcut(df_Centrale_midt['average_receivedPass'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Succesful dribbles %'] = pd.qcut(df_Centrale_midt['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Succesful dribbles #'] = pd.qcut(df_Centrale_midt['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Duels won %'] = pd.qcut(df_Centrale_midt['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Duels won #'] = pd.qcut(df_Centrale_midt['average_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Interceptions'] = pd.qcut(df_Centrale_midt['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Counterpressing recoveries #'] = pd.qcut(df_Centrale_midt['average_counterpressingRecoveries'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Defensive duels won #'] = pd.qcut(df_Centrale_midt['average_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Defensive duels won %'] = pd.qcut(df_Centrale_midt['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

        df_Centrale_midtsæsonen = df_Centrale_midt.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
        df_Centrale_midtsæsonen = df_Centrale_midt.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
        df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #'] + df_Centrale_midtsæsonen['Forward Passes %'] + df_Centrale_midtsæsonen['Forward Passes #'] + df_Centrale_midtsæsonen['Long Passes %'] + df_Centrale_midtsæsonen['Long Passes #']+ df_Centrale_midtsæsonen['Smart passes %'] + df_Centrale_midtsæsonen['Smart passes #'] + + df_Centrale_midtsæsonen['Key passes %'] + df_Centrale_midtsæsonen['Key passes #'] + df_Centrale_midtsæsonen['Passes to final third %'] + df_Centrale_midtsæsonen['Passes to final third #']+ df_Centrale_midtsæsonen['Vertical passes %'] + df_Centrale_midtsæsonen['Vertical passes #']+ df_Centrale_midtsæsonen['Through passes %'] + df_Centrale_midtsæsonen['Through passes #']+ df_Centrale_midtsæsonen['Progressive passes %'] + df_Centrale_midtsæsonen['Progressive passes #'])/18
        df_Centrale_midtsæsonen['Boldfast'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #']+ df_Centrale_midtsæsonen['Offensive duels %'] + df_Centrale_midtsæsonen['Received passes'] + df_Centrale_midtsæsonen['Succesful dribbles %'] + df_Centrale_midtsæsonen['Succesful dribbles #'])/6
        df_Centrale_midtsæsonen['Spilintelligens defensivt'] = (df_Centrale_midtsæsonen['Duels won %'] + df_Centrale_midtsæsonen['Duels won #'] +df_Centrale_midtsæsonen['Interceptions'] + df_Centrale_midtsæsonen['Counterpressing recoveries #'] + df_Centrale_midtsæsonen['Defensive duels won %'] + df_Centrale_midtsæsonen['Defensive duels won #'])/6
        df_Centrale_midtsæsonen['Samlet'] = (df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] + df_Centrale_midtsæsonen['Boldfast'] + df_Centrale_midtsæsonen['Spilintelligens defensivt'])/3
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen[['Pasningssikker/Spilvendinger','Boldfast','Spilintelligens defensivt','Samlet']]
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.sort_values(by='Samlet',ascending=False)

        df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['Team name'].str.contains('Horsens')]
        df_Centrale_midt['Pasningssikker/Spilvendinger'] = (df_Centrale_midt['Passes %'] + df_Centrale_midt['Passes #'] + df_Centrale_midt['Forward Passes %'] + df_Centrale_midt['Forward Passes #'] + df_Centrale_midt['Long Passes %'] + df_Centrale_midt['Long Passes #']+ df_Centrale_midt['Smart passes %'] + df_Centrale_midt['Smart passes #'] + + df_Centrale_midt['Key passes %'] + df_Centrale_midt['Key passes #'] + df_Centrale_midt['Passes to final third %'] + df_Centrale_midt['Passes to final third #']+ df_Centrale_midt['Vertical passes %'] + df_Centrale_midt['Vertical passes #']+ df_Centrale_midt['Through passes %'] + df_Centrale_midt['Through passes #']+ df_Centrale_midt['Progressive passes %'] + df_Centrale_midt['Progressive passes #'])/18
        df_Centrale_midt['Boldfast'] = (df_Centrale_midt['Passes %'] + df_Centrale_midt['Passes #']+ df_Centrale_midt['Offensive duels %'] + df_Centrale_midt['Received passes'] + df_Centrale_midt['Succesful dribbles %'] + df_Centrale_midt['Succesful dribbles #'])/6
        df_Centrale_midt['Spilintelligens defensivt'] = (df_Centrale_midt['Duels won %'] + df_Centrale_midt['Duels won #'] +df_Centrale_midt['Interceptions'] + df_Centrale_midt['Counterpressing recoveries #'] + df_Centrale_midt['Defensive duels won %'] + df_Centrale_midt['Defensive duels won #'])/6
        df_Centrale_midt['Samlet'] = (df_Centrale_midt['Pasningssikker/Spilvendinger'] + df_Centrale_midt['Boldfast'] + df_Centrale_midt['Spilintelligens defensivt'])/3
        df_Centrale_midt = df_Centrale_midt[['Player name','Team name','label','total_minutesOnField_y','Pasningssikker/Spilvendinger','Boldfast','Spilintelligens defensivt','Samlet']]
        df_Centrale_midt = df_Centrale_midt.sort_values(by='Samlet',ascending=False)

        df_Centrale_midt = navne.merge(df_Centrale_midt)
        df_Centrale_midt = df_Centrale_midt.drop('Player Name',axis=1)
        df_Centrale_midt = df_Centrale_midt.drop('Player name',axis=1)    
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.reset_index()
        df_Centrale_midtsæsonen = navne.merge(df_Centrale_midtsæsonen)
        df_Centrale_midt = navne.merge(df_Centrale_midt)
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.drop('Player Name',axis=1)
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.drop('Player name',axis=1)
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.drop('label',axis=1)


        df_Kanter = pd.merge(df_kanterminutter,df_Kanter,on=('Player id'))
        df_Kanter = df_Kanter[df_Kanter['total_minutesOnField_y'] >=17]

        df_Kanter['Shots on target %'] = pd.qcut(df_Kanter['percent_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Shots on target #'] = pd.qcut(df_Kanter['average_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['XG'] = pd.qcut(df_Kanter['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Successful dribbles #'] = pd.qcut(df_Kanter['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Successful dribbles %'] = pd.qcut(df_Kanter['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Offensive duels %'] = pd.qcut(df_Kanter['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Offensive duels #'] = pd.qcut(df_Kanter['average_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Passes %'] = pd.qcut(df_Kanter['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Passes #'] = pd.qcut(df_Kanter['average_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Forward Passes %'] = pd.qcut(df_Kanter['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Forward Passes #'] = pd.qcut(df_Kanter['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Smart passes %'] = pd.qcut(df_Kanter['percent_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Smart passes #'] = pd.qcut(df_Kanter['average_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Key passes %'] = pd.qcut(df_Kanter['percent_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Key passes #'] = pd.qcut(df_Kanter['average_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Passes to final third %'] = pd.qcut(df_Kanter['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Passes to final third #'] = pd.qcut(df_Kanter['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Vertical passes %'] = pd.qcut(df_Kanter['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Vertical passes #'] = pd.qcut(df_Kanter['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Through passes %'] = pd.qcut(df_Kanter['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Through passes #'] = pd.qcut(df_Kanter['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Progressive passes %'] = pd.qcut(df_Kanter['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Progressive passes #'] = pd.qcut(df_Kanter['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Goal conversion %'] = pd.qcut(df_Kanter['percent_goalConversion'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['XG per 90'] = pd.qcut(df_Kanter['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['XA per 90'] = pd.qcut(df_Kanter['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Successful attacking actions'] = pd.qcut(df_Kanter['average_successfulAttackingActions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Progressive runs'] = pd.qcut(df_Kanter['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Accelerations score'] = pd.qcut(df_Kanter['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

        df_Kantersæsonen = df_Kanter.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    
        df_Kantersæsonen = df_Kanter.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

        df_Kantersæsonen['Sparkefærdigheder'] = (df_Kantersæsonen['Shots on target %'] + df_Kantersæsonen['Shots on target #'] + df_Kantersæsonen['XG'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Vertical passes %'])/6
        df_Kantersæsonen['Kombinationsstærk'] = (df_Kantersæsonen['Passes %'] + df_Kantersæsonen['Passes #'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Forward Passes #'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Passes to final third #'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
        df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] = (df_Kantersæsonen['XA per 90'] + df_Kantersæsonen['XG per 90'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Smart passes %'] + df_Kantersæsonen['Smart passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Key passes %'] + df_Kantersæsonen['Key passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
        df_Kantersæsonen['1v1 offensivt'] = (df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Offensive duels #'] + df_Kantersæsonen['Offensive duels %'] + df_Kantersæsonen['Progressive runs'])/5
        df_Kantersæsonen['Fart'] = (df_Kantersæsonen['Progressive runs'] + df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Accelerations score'])/5
        df_Kantersæsonen['Samlet'] = (df_Kantersæsonen['Sparkefærdigheder'] + df_Kantersæsonen['Kombinationsstærk'] + df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] + df_Kantersæsonen['1v1 offensivt'] + df_Kantersæsonen['Fart'])/5
        df_Kantersæsonen = df_Kantersæsonen[['Sparkefærdigheder','Kombinationsstærk','Spilintelligens offensivt/indlægsstærk','1v1 offensivt','Fart','Samlet']]
        df_Kantersæsonen = df_Kantersæsonen.sort_values(by='Samlet',ascending=False)
        df_Kanter = df_Kanter[df_Kanter['Team name'].str.contains('Horsens')]
        df_Kanter['Sparkefærdigheder'] = (df_Kanter['Shots on target %'] + df_Kanter['Shots on target #'] + df_Kanter['XG'] + df_Kanter['Passes to final third %'] + df_Kanter['Forward Passes %'] + df_Kanter['Vertical passes %'])/6
        df_Kanter['Kombinationsstærk'] = (df_Kanter['Passes %'] + df_Kanter['Passes #'] + df_Kanter['Forward Passes %'] + df_Kanter['Forward Passes #'] + df_Kanter['Passes to final third %'] + df_Kanter['Passes to final third #'] + df_Kanter['Through passes %'] + df_Kanter['Through passes #'] + df_Kanter['Progressive passes %'] + df_Kanter['Progressive passes #'] + df_Kanter['Successful attacking actions'])/11
        df_Kanter['Spilintelligens offensivt/indlægsstærk'] = (df_Kanter['XA per 90'] + df_Kanter['XG per 90'] + df_Kanter['Through passes %'] + df_Kanter['Through passes #'] + df_Kanter['Smart passes %'] + df_Kanter['Smart passes #'] + df_Kanter['Progressive passes %'] + df_Kanter['Progressive passes #'] + df_Kanter['Key passes %'] + df_Kanter['Key passes #'] + df_Kanter['Successful attacking actions'])/11
        df_Kanter['1v1 offensivt'] = (df_Kanter['Successful dribbles #'] + df_Kanter['Successful dribbles %'] + df_Kanter['Offensive duels #'] + df_Kanter['Offensive duels %'] + df_Kanter['Progressive runs'])/5
        df_Kanter['Fart'] = (df_Kanter['Progressive runs'] + df_Kanter['Successful dribbles #'] + df_Kanter['Successful dribbles %'] + df_Kanter['Accelerations score'])/5
        df_Kanter['Samlet'] = (df_Kanter['Sparkefærdigheder'] + df_Kanter['Kombinationsstærk'] + df_Kanter['Spilintelligens offensivt/indlægsstærk'] + df_Kanter['1v1 offensivt'] + df_Kanter['Fart'])/5
        df_Kanter = df_Kanter[['Player name','Team name','label','total_minutesOnField_y','Sparkefærdigheder','Kombinationsstærk','Spilintelligens offensivt/indlægsstærk','1v1 offensivt','Fart','Samlet']]
        df_Kanter = df_Kanter.sort_values(by='Samlet',ascending=False)

        df_Kanter = navne.merge(df_Kanter)
        df_Kanter = df_Kanter.drop('Player Name',axis=1)
        df_Kanter = df_Kanter.drop('Player name',axis=1)    
        df_Kantersæsonen=df_Kantersæsonen.reset_index()
        df_Kantersæsonen = navne.merge(df_Kantersæsonen)
        df_Kanter = navne.merge(df_Kanter)
        df_Kantersæsonen= df_Kantersæsonen.drop('Player Name',axis=1)
        df_Kantersæsonen = df_Kantersæsonen.drop('Player name',axis=1)
        df_Kantersæsonen = df_Kantersæsonen.drop('label',axis=1)
    
        
        df_Angribere = pd.merge(df_angribereminutter,df_Angribere,on=('Player id'))
        df_Angribere = df_Angribere[df_Angribere['total_minutesOnField_y'] >=17]

        df_Angribere['Målfarlighed udregning'] = df_Angribere['average_goals'] - df_Angribere['average_xgShot']
        df_Angribere['Målfarlighed score'] =  pd.qcut(df_Angribere['Målfarlighed udregning'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['xG per 90 score'] = pd.qcut(df_Angribere['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Goals per 90 score'] = pd.qcut(df_Angribere['average_goals'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)  
        df_Angribere['Shots on target, % score'] = pd.qcut(df_Angribere['percent_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)   
        df_Angribere['Offensive duels won, % score'] = pd.qcut(df_Angribere['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Duels won, % score'] = pd.qcut(df_Angribere['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Accurate passes, % score'] = pd.qcut(df_Angribere['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Successful dribbles, % score'] = pd.qcut(df_Angribere['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['xA per 90 score'] = pd.qcut(df_Angribere['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Touches in box per 90 score'] = pd.qcut(df_Angribere['average_touchInBox'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Progressive runs'] = pd.qcut(df_Angribere['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Accelerations score'] = pd.qcut(df_Angribere['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Progressive passes per 90 score'] = pd.qcut(df_Angribere['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Successful attacking actions per 90 score'] = pd.qcut(df_Angribere['average_successfulAttackingActions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Successful dribbles #'] = pd.qcut(df_Angribere['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

        df_Angriberesæsonen = df_Angribere.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)

        df_Angriberesæsonen = df_Angribere.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

        df_Angriberesæsonen['Sparkefærdigheder'] = (df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Goals per 90 score'] + df_Angriberesæsonen['Shots on target, % score'])/4
        df_Angriberesæsonen['Boldfast'] = (df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Duels won, % score'] + df_Angriberesæsonen['Accurate passes, % score'] + df_Angriberesæsonen['Successful dribbles, % score'])/5
        df_Angriberesæsonen['Spilintelligens offensivt'] = (df_Angriberesæsonen['xA per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['Progressive passes per 90 score'] + df_Angriberesæsonen['Successful attacking actions per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['xG per 90 score'])/7
        df_Angriberesæsonen['Målfarlighed'] = (df_Angriberesæsonen['xG per 90 score']+df_Angriberesæsonen['Goals per 90 score']+df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Målfarlighed score'])/4
        df_Angriberesæsonen['Fart'] = (df_Angriberesæsonen['Progressive runs'] + + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Successful dribbles #'] + df_Angriberesæsonen['Successful dribbles, % score'] + df_Angriberesæsonen['Accelerations score'] + df_Angriberesæsonen['Offensive duels won, % score'])/7
        df_Angriberesæsonen = df_Angriberesæsonen[['Sparkefærdigheder','Boldfast','Spilintelligens offensivt','Målfarlighed','Fart']]
        df_Angriberesæsonen['Samlet'] = (df_Angriberesæsonen['Sparkefærdigheder']+df_Angriberesæsonen['Boldfast']+df_Angriberesæsonen['Spilintelligens offensivt']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Fart'])/7
        df_Angriberesæsonen = df_Angriberesæsonen.sort_values(by='Samlet',ascending=False)
        df_Angriberesæsonen = df_Angriberesæsonen[df_Angriberesæsonen.index.get_level_values('Team name').str.contains('Horsens')]

        df_Angribere = df_Angribere[df_Angribere['Team name'].str.contains('Horsens')]
        df_Angribere['Sparkefærdigheder'] = (df_Angribere['xG per 90 score'] + df_Angribere['xG per 90 score'] + df_Angribere['Goals per 90 score'] + df_Angribere['Shots on target, % score'])/4
        df_Angribere['Boldfast'] = (df_Angribere['Offensive duels won, % score'] + df_Angribere['Offensive duels won, % score'] + df_Angribere['Duels won, % score'] + df_Angribere['Accurate passes, % score'] + df_Angribere['Successful dribbles, % score'])/5
        df_Angribere['Spilintelligens offensivt'] = (df_Angribere['xA per 90 score'] + df_Angribere['xG per 90 score'] + df_Angribere['Touches in box per 90 score'] + df_Angribere['Progressive passes per 90 score'] + df_Angribere['Successful attacking actions per 90 score'] + df_Angribere['Touches in box per 90 score'] + df_Angribere['xG per 90 score'])/7
        df_Angribere['Målfarlighed'] = (df_Angribere['xG per 90 score']+df_Angribere['Goals per 90 score']+df_Angribere['xG per 90 score'] + df_Angribere['Målfarlighed score'])/4
        df_Angribere['Fart'] = (df_Angribere['Progressive runs'] + + df_Angribere['Progressive runs'] + df_Angribere['Progressive runs'] + df_Angribere['Successful dribbles #'] + df_Angribere['Successful dribbles, % score'] + df_Angribere['Accelerations score'] + df_Angribere['Offensive duels won, % score'])/7
        df_Angribere = df_Angribere[['Player name','Team name','label','total_minutesOnField_y','Sparkefærdigheder','Boldfast','Spilintelligens offensivt','Målfarlighed','Fart']]
        df_Angribere['Samlet'] = (df_Angribere['Sparkefærdigheder']+df_Angribere['Boldfast']+df_Angribere['Spilintelligens offensivt']+df_Angribere['Målfarlighed']+df_Angribere['Målfarlighed']+df_Angribere['Målfarlighed']+df_Angribere['Fart'])/7
        df_Angribere = df_Angribere.sort_values(by='Samlet',ascending=False)
        
        kampe = df['label']
        kampe = kampe[kampe.str.contains('Horsens')]
        kampe = kampe.drop_duplicates(keep='first')  
        
        df_Angribere = navne.merge(df_Angribere)
        df_Angribere = df_Angribere.drop('Player Name',axis=1)
        df_Angribere = df_Angribere.drop('Player name',axis=1)
        df_Angriberesæsonen=df_Angriberesæsonen.reset_index()
        df_Angriberesæsonen = navne.merge(df_Angriberesæsonen)
        df_Angribere = navne.merge(df_Angribere)
        df_Angriberesæsonen= df_Angriberesæsonen.drop('Player Name',axis=1)
        df_Angriberesæsonen = df_Angriberesæsonen.drop('Player name',axis=1)
        df_Angriberesæsonen = df_Angriberesæsonen.drop('label',axis=1)
        
        option2 = st.selectbox('Vælg spiller',navneliste)
        df_Angriberesæsonen = df_Angriberesæsonen[df_Angriberesæsonen['Spillere'].str.contains(option2)]
        df_Angribere = df_Angribere[df_Angribere['Spillere'].str.contains(option2)]
        df_Kantersæsonen = df_Kantersæsonen[df_Kantersæsonen['Spillere'].str.contains(option2)]
        df_Kanter = df_Kanter[df_Kanter['Spillere'].str.contains(option2)]
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen[df_Centrale_midtsæsonen['Spillere'].str.contains(option2)]
        df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['Spillere'].str.contains(option2)]
        df_Stopperesæsonen = df_Stopperesæsonen[df_Stopperesæsonen['Spillere'].str.contains(option2)]
        df_Stoppere = df_Stoppere[df_Stoppere['Spillere'].str.contains(option2)]
        df_backssæsonen = df_backssæsonen[df_backs['Spillere'].str.contains(option2)]
        df_backs = df_backs[df_backs['Spillere'].str.contains(option2)]

        option = st.multiselect('Vælg kamp (Hvis ingen kamp er valgt, vises alle)',kampe)
        if len(option) > 0:
            temp_select = option
        else:
            temp_select = kampe

        df_backs = df_backs[df_backs['label'].isin(temp_select)]
        df_backs = df_backs.drop('label',axis=1)
        df_backssæsonen = df_backssæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()
        
        df_backs = df_backs.groupby(['Spillere','Trup','Team name']).agg({
        'total_minutesOnField_y':'sum',
        'Indlægsstærk':'mean',
        '1v1 færdigheder':'mean',
        'Spilintelligens defensivt':'mean',
        'Fart':'mean',
        'Samlet':'mean'
        })

        df_backs = df_backs.sort_values(by='Samlet',ascending=False)
        df_backs = df_backs.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
        df_backs = df_backs.reset_index()
        df_backs = df_backs.set_index(['Spillere','Trup','Team name'])
        df_backssæsonen = df_backssæsonen.reset_index()
        df_backssæsonen = df_backssæsonen.set_index(['Spillere','Trup','Team name'])
        df_backs = pd.concat([df_backs,df_backssæsonen],axis=0)        

        df_Stoppere = df_Stoppere[df_Stoppere['label'].isin(temp_select)]
        df_Stoppere = df_Stoppere.drop('label',axis=1)
        df_Stopperesæsonen = df_Stopperesæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()
        
        df_Stoppere = df_Stoppere.groupby(['Spillere','Trup','Team name']).agg({
        'total_minutesOnField_y':'sum',
        'Pasningssikker':'mean',
        'Spilintelligens offensivt':'mean',
        'Spilintelligens defensivt':'mean',
        'Nærkamps- og duelstærk':'mean',
        'Samlet':'mean'
        })

        df_Stoppere = df_Stoppere.sort_values(by='Samlet',ascending=False)
        df_Stoppere = df_Stoppere.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
        df_Stoppere = df_Stoppere.reset_index()
        df_Stoppere = df_Stoppere.set_index(['Spillere','Trup','Team name'])
        df_Stopperesæsonen = df_Stopperesæsonen.reset_index()
        df_Stopperesæsonen = df_Stopperesæsonen.set_index(['Spillere','Trup','Team name'])
        df_Stoppere = pd.concat([df_Stoppere,df_Stopperesæsonen],axis=0)

        df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['label'].isin(temp_select)]
        df_Centrale_midt = df_Centrale_midt.drop('label',axis=1)
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()
        
        df_Centrale_midt = df_Centrale_midt.groupby(['Spillere','Trup','Team name']).agg({
        'total_minutesOnField_y':'sum',
        'Pasningssikker/Spilvendinger':'mean',
        'Boldfast':'mean',
        'Spilintelligens defensivt':'mean',
        'Samlet':'mean'
        })

        df_Centrale_midt = df_Centrale_midt.sort_values(by='Samlet',ascending=False)
        df_Centrale_midt = df_Centrale_midt.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
        df_Centrale_midt = df_Centrale_midt.reset_index()
        df_Centrale_midt = df_Centrale_midt.set_index(['Spillere','Trup','Team name'])
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.reset_index()
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.set_index(['Spillere','Trup','Team name'])
        df_Centrale_midt = pd.concat([df_Centrale_midt,df_Centrale_midtsæsonen],axis=0)
    
            
        df_Kanter = df_Kanter[df_Kanter['label'].isin(temp_select)]
        df_Kanter = df_Kanter.drop('label',axis=1)
        df_Kantersæsonen = df_Kantersæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()
        
        df_Kanter = df_Kanter.groupby(['Spillere','Trup','Team name']).agg({
        'total_minutesOnField_y':'sum',
        'Sparkefærdigheder':'mean',
        'Kombinationsstærk':'mean',
        'Spilintelligens offensivt/indlægsstærk':'mean',
        '1v1 offensivt':'mean',
        'Fart':'mean',
        'Samlet':'mean'
        })
        
        df_Kanter = df_Kanter.sort_values(by='Samlet',ascending=False)
        df_Kanter = df_Kanter.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
        df_Kanter = df_Kanter.reset_index()
        df_Kanter = df_Kanter.set_index(['Spillere','Trup','Team name'])
        df_Kantersæsonen = df_Kantersæsonen.reset_index()
        df_Kantersæsonen = df_Kantersæsonen.set_index(['Spillere','Trup','Team name'])
        df_Kanter = pd.concat([df_Kanter,df_Kantersæsonen],axis=0)

        
        df_Angribere = df_Angribere[df_Angribere['label'].isin(temp_select)]
        df_Angribere = df_Angribere.drop('label',axis=1)
        df_Angriberesæsonen = df_Angriberesæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()

        df_Angribere = df_Angribere.groupby(['Spillere','Trup','Team name']).agg({
        'total_minutesOnField_y':'sum',
        'Sparkefærdigheder': 'mean',
        'Boldfast': 'mean',
        'Spilintelligens offensivt':'mean',
        'Målfarlighed':'mean',
        'Fart':'mean',
        'Samlet':'mean',
        })

        df_Angribere = df_Angribere.sort_values(by = 'Samlet',ascending=False)
        df_Angribere = df_Angribere.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
        df_Angribere = df_Angribere.reset_index()
        df_Angribere = df_Angribere.set_index(['Spillere','Trup','Team name'])
        df_Angriberesæsonen = df_Angriberesæsonen.reset_index()
        df_Angriberesæsonen = df_Angriberesæsonen.set_index(['Spillere','Trup','Team name'])
        df_Angribere = pd.concat([df_Angribere,df_Angriberesæsonen],axis=0)
        #st.dataframe(df_Angribere)
        #st.write('Angribere')
        dataframe_names = ['Stopper', 'Back', 'Central midt', 'Kant', 'Angriber']

        # Create the selectbox in Streamlit
        selected_dataframe = st.selectbox('Position', options=dataframe_names)

        # Based on the selected dataframe, retrieve the corresponding dataframe object
        if selected_dataframe == 'Stopper':
            selected_df = df_Stoppere
        elif selected_dataframe == 'Back':
            selected_df = df_backs
        elif selected_dataframe == 'Central midt':
            selected_df = df_Centrale_midt
        elif selected_dataframe == 'Kant':
            selected_df = df_Kanter
        elif selected_dataframe == 'Angriber':
            selected_df = df_Angribere

        st.dataframe(selected_df)
        df_filtered = selected_df.iloc[:, 1:]

        # Create a scatterpolar plot using plotly
        fig = go.Figure()

        # Iterate over each row in the dataframe
        for _, row in df_filtered.iterrows():
            fig.add_trace(go.Scatterpolar(
                r=row.values,
                theta=df_filtered.columns,
                fill='toself'
            ))
        fig.data[0].name = 'Valgte periode'
        fig.data[1].name = 'Hele sæsonen'
        # Set plot title and layout
        fig.update_layout(
            title='Scatterpolar Plot',
            template='plotly_dark',
            polar=dict(
                radialaxis=dict
                    (visible=True,
                    range=[1,5]
                )
            )
        )
        # Render the plot within Streamlit
        st.plotly_chart(fig)
    def U19():
        import pandas as pd
        import streamlit as st
        import json
        from pandas import json_normalize
        import ast
        from dateutil import parser
        import plotly.graph_objects as go
        navne = pd.read_excel('Navne.xlsx')
        navne = navne[navne['Trup'].str.contains('U19')]
        navneliste = navne['Spillere'].sort_values(ascending=True)
        df = pd.read_csv('Individuelt dashboard U19.csv')
        df.rename(columns={'playerId': 'Player id'}, inplace=True)
        df = df.astype(str)
        dfevents = pd.read_csv('U19 eventdata alle.csv',low_memory=False)
        dfevents = dfevents[['Player id','Player name','team_name','label','date','matchId']]
        dfspillernavn = df[['Player id','matchId','positions','average','percent','total']]
        dfspillernavn = dfspillernavn.astype(str)
        dfevents['Player id'] = dfevents['Player id'].astype(str)
        dfevents['matchId'] = dfevents['matchId'].astype(str)
        df = dfspillernavn.merge(dfevents)

        df['Player&matchId'] = df['Player id'] + df['matchId']
        df['Player&matchId'] = df['Player&matchId'].drop_duplicates(keep='first')
        df = df.dropna()
        df = df[['Player id','Player name','team_name','matchId','label','date','positions','average','percent','total']]

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
        df = df[['Player name','team_name','matchId','label','date','position_names','position_codes','average','percent','total']]
        df = df.rename(columns={'team_name':'Team name'})
        df['percent'] = df['percent'].apply(lambda x: ast.literal_eval(x))

        # Create a new dataframe with the columns as the dictionary keys and the values as a list
        new_df = pd.DataFrame(df['percent'].to_list(), index=df.index).add_prefix('percent_')

        # Concatenate the new dataframe with the original dataframe
        df = pd.concat([df, new_df], axis=1)

        # Drop the original 'percent' column
        df = df.drop('percent', axis=1)

        df['total'] = df['total'].apply(lambda x: ast.literal_eval(x))

        # Create a new dataframe with the columns as the dictionary keys and the values as a list
        new_df = pd.DataFrame(df['total'].to_list(), index=df.index).add_prefix('total_')

        # Concatenate the new dataframe with the original dataframe
        df = pd.concat([df, new_df], axis=1)

        # Drop the original 'percent' column
        df = df.drop('total', axis=1)

        df['average'] = df['average'].apply(lambda x: ast.literal_eval(x))

        # Create a new dataframe with the columns as the dictionary keys and the values as a list
        new_df = pd.DataFrame(df['average'].to_list(), index=df.index).add_prefix('average_')

        # Concatenate the new dataframe with the original dataframe
        df = pd.concat([df, new_df], axis=1)


        # Drop the original 'percent' column
        df = df.drop('average', axis=1)
        df['position_codes'] = df['position_codes'].astype(str)
        #df['date'] = df['date'].astype(str)
        #df['date'] = df['date'].apply(lambda x: parser.parse(x))

        # Sort the dataframe by the 'date' column
        #df = df.sort_values(by='date',ascending=False)

        # Format the 'date' column to day-month-year format
        #df['date'] = df['date'].apply(lambda x: x.strftime('%d-%m-%Y'))
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date',ascending=False)

        df_backs = df[df['position_codes'].str.contains('|'.join(['lb', 'rb']))]
        df_backsminutter = df_backs[['Player name','Team name','total_minutesOnField']]
        df_backsminutter = df_backsminutter.groupby(['Player id']).sum(numeric_only=True)
        df_backsminutter = df_backsminutter[df_backsminutter['total_minutesOnField'] >= 300]

        df_Stoppere = df[df['position_codes'].str.contains('|'.join(['cb']))]
        df_stoppereminutter = df_Stoppere[['Player name','Team name','total_minutesOnField']]
        df_stoppereminutter = df_stoppereminutter.groupby(['Player id']).sum(numeric_only=True)
        df_stoppereminutter = df_stoppereminutter[df_stoppereminutter['total_minutesOnField'] >= 300]

        df_Centrale_midt = df[df['position_codes'].str.contains('|'.join(['cm','amf','dmf']))]
        df_centraleminutter = df_Centrale_midt[['Player name','Team name','total_minutesOnField']]
        df_centraleminutter = df_centraleminutter.groupby(['Player id']).sum(numeric_only=True)
        df_centraleminutter = df_centraleminutter[df_centraleminutter['total_minutesOnField'] >= 300]

        df_Kanter = df[df['position_codes'].str.contains('|'.join(['rw','lw','ramf','lamf']))]
        df_kanterminutter = df_Kanter[['Player name','Team name','total_minutesOnField']]
        df_kanterminutter = df_kanterminutter.groupby(['Player id']).sum(numeric_only=True)
        df_kanterminutter = df_kanterminutter[df_kanterminutter['total_minutesOnField'] >=300]


        df_Angribere = df[df['position_codes'].str.contains('|'.join(['cf']))]
        df_angribereminutter = df_Angribere[['Player name','Team name','total_minutesOnField']]
        df_angribereminutter = df_angribereminutter.groupby(['Player id']).sum(numeric_only=True)
        df_angribereminutter = df_angribereminutter[df_angribereminutter['total_minutesOnField'] >= 300]


        df_backs = pd.merge(df_backsminutter,df_backs,on=('Player id'))
        df_backs = df_backs[df_backs['total_minutesOnField_y'] >=17]

        df_backs['Accurate crosses score'] = pd.qcut(df_backs['percent_successfulCrosses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Number of crosses score'] = pd.qcut(df_backs['average_crosses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['XA score'] = pd.qcut(df_backs['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Passes to final third score'] = pd.qcut(df_backs['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Successful dribbles score'] = pd.qcut(df_backs['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Defensive duels won score'] = pd.qcut(df_backs['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Progressive runs score'] = pd.qcut(df_backs['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Offensive duels won score'] = pd.qcut(df_backs['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Accelerations score'] = pd.qcut(df_backs['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Duels won score'] = pd.qcut(df_backs['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Interceptions score'] = pd.qcut(df_backs['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backs['Successful defensive actions score'] = pd.qcut(df_backs['average_successfulDefensiveAction'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_backssæsonen = df_backs[['Player name','Team name','label','total_minutesOnField_x','total_minutesOnField_y','Number of crosses score','Accurate crosses score','XA score','Passes to final third score','Successful dribbles score','Defensive duels won score','Progressive runs score','Offensive duels won score','Accelerations score','Duels won score','Interceptions score','Successful defensive actions score']]
        df_backssæsonen.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
        df_backssæsonen = df_backssæsonen.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

        df_backssæsonen['Indlægsstærk'] = (df_backssæsonen['Number of crosses score'] + df_backssæsonen['Accurate crosses score'] + df_backssæsonen['XA score'] + df_backssæsonen['Passes to final third score'])/4
        df_backssæsonen['1v1 færdigheder'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Defensive duels won score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'] + df_backssæsonen['Duels won score'])/6
        df_backssæsonen['Spilintelligens defensivt'] = (df_backssæsonen['Interceptions score'] + df_backssæsonen['Successful defensive actions score'] + df_backssæsonen['Duels won score'] + df_backssæsonen['Defensive duels won score'])/4
        df_backssæsonen['Fart'] = (df_backssæsonen['Successful dribbles score'] + df_backssæsonen['Progressive runs score'] + df_backssæsonen['Offensive duels won score'] + df_backssæsonen['Accelerations score'])/4
        df_backssæsonen ['Samlet'] = (df_backssæsonen['Indlægsstærk'] + df_backssæsonen['1v1 færdigheder'] + df_backssæsonen['Spilintelligens defensivt'] + df_backssæsonen['Fart'])/4
        df_backssæsonen = df_backssæsonen[['Indlægsstærk','1v1 færdigheder','Spilintelligens defensivt','Fart','Samlet']]
        df_backssæsonen = df_backssæsonen.sort_values(by='Samlet',ascending=False)

        df_backs['Indlægsstærk'] = (df_backs['Number of crosses score'] + df_backs['Accurate crosses score'] + df_backs['XA score'] + df_backs['Passes to final third score'])/4
        df_backs['1v1 færdigheder'] = (df_backs['Successful dribbles score'] + df_backs['Defensive duels won score'] + df_backs['Progressive runs score'] + df_backs['Offensive duels won score'] + df_backs['Accelerations score'] + df_backs['Duels won score'])/6
        df_backs['Spilintelligens defensivt'] = (df_backs['Interceptions score'] + df_backs['Successful defensive actions score'] + df_backs['Duels won score'] + df_backs['Defensive duels won score'])/4
        df_backs['Fart'] = (df_backs['Successful dribbles score'] + df_backs['Progressive runs score'] + df_backs['Offensive duels won score'] + df_backs['Accelerations score'])/4
        df_backs['Samlet'] = (df_backs['Indlægsstærk'] + df_backs['1v1 færdigheder'] + df_backs['Spilintelligens defensivt'] + df_backs['Fart'])/4


        df_backs = df_backs[['Player name','Team name','label','total_minutesOnField_y','Indlægsstærk','1v1 færdigheder','Spilintelligens defensivt','Fart','Samlet']]
        df_backs = df_backs.sort_values(by='Samlet',ascending=False)
        
        df_backs = navne.merge(df_backs)
        df_backs = df_backs.drop('Player Name',axis=1)
        df_backs = df_backs.drop('Player name',axis=1)    
        df_backssæsonen = df_backssæsonen.reset_index()
        df_backssæsonen = navne.merge(df_backssæsonen)
        df_backs = navne.merge(df_backs)
        df_backssæsonen = df_backssæsonen.drop('Player Name',axis=1)
        df_backssæsonen = df_backssæsonen.drop('Player name',axis=1)
        df_backssæsonen = df_backssæsonen.drop('label',axis=1)


        df_Stoppere = pd.merge(df_stoppereminutter,df_Stoppere,on=('Player id'))
        df_Stoppere = df_Stoppere[df_Stoppere['total_minutesOnField_y'] >=17]

        df_Stoppere['Accurate passes score'] = pd.qcut(df_Stoppere['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Accurate long passes score'] = pd.qcut(df_Stoppere['percent_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Forward passes score'] = pd.qcut(df_Stoppere['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Accurate forward passes score'] = pd.qcut(df_Stoppere['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Accurate progressive passes score'] = pd.qcut(df_Stoppere['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Accurate vertical passes score'] = pd.qcut(df_Stoppere['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Interceptions score'] = pd.qcut(df_Stoppere['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Succesful defensive actions score'] = pd.qcut(df_Stoppere['average_successfulDefensiveAction'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Shots blocked score'] = pd.qcut(df_Stoppere['average_shotsBlocked'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Defensive duels won score'] = pd.qcut(df_Stoppere['average_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Defensive duels won % score'] = pd.qcut(df_Stoppere['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Accurate passes to final third'] = pd.qcut(df_Stoppere['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Accurate through passes'] = pd.qcut(df_Stoppere['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Vertical passes'] = pd.qcut(df_Stoppere['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Through passes'] = pd.qcut(df_Stoppere['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Passes to final third'] = pd.qcut(df_Stoppere['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Progressive runs'] = pd.qcut(df_Stoppere['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Offensive duels won %'] = pd.qcut(df_Stoppere['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Successful dribbles %'] = pd.qcut(df_Stoppere['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Progressive passes score'] = pd.qcut(df_Stoppere['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Aerial duels won score'] = pd.qcut(df_Stoppere['average_fieldAerialDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Stoppere['Aerial duels won % score'] = pd.qcut(df_Stoppere['percent_aerialDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

        df_Stopperesæsonen = df_Stoppere.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
        df_Stopperesæsonen = df_Stoppere.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
        df_Stopperesæsonen['Pasningssikker'] = (df_Stopperesæsonen['Accurate passes score'] + df_Stopperesæsonen['Accurate long passes score'] + df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Accurate vertical passes score'])/6
        df_Stopperesæsonen['Spilintelligens defensivt'] = (df_Stopperesæsonen['Interceptions score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Shots blocked score'] + df_Stopperesæsonen['Succesful defensive actions score'] + df_Stopperesæsonen['Defensive duels won % score']) /5
        df_Stopperesæsonen['Spilintelligens offensivt'] = (df_Stopperesæsonen['Forward passes score'] + df_Stopperesæsonen['Accurate forward passes score'] + df_Stopperesæsonen['Accurate passes to final third'] + df_Stopperesæsonen['Passes to final third'] + df_Stopperesæsonen['Accurate progressive passes score'] + df_Stopperesæsonen['Progressive passes score'] + df_Stopperesæsonen['Through passes'] + df_Stopperesæsonen['Accurate through passes']+ df_Stopperesæsonen['Progressive runs'] + df_Stopperesæsonen['Offensive duels won %'] + df_Stopperesæsonen['Successful dribbles %'])/11
        df_Stopperesæsonen['Nærkamps- og duelstærk'] = (df_Stopperesæsonen['Defensive duels won % score'] + df_Stopperesæsonen['Aerial duels won % score'] + df_Stopperesæsonen['Defensive duels won % score'])/3
        df_Stopperesæsonen['Samlet'] = (df_Stopperesæsonen['Pasningssikker'] + df_Stopperesæsonen['Spilintelligens defensivt'] + df_Stopperesæsonen['Spilintelligens offensivt'] + df_Stopperesæsonen['Nærkamps- og duelstærk'])/4

        df_Stopperesæsonen = df_Stopperesæsonen[['Pasningssikker','Spilintelligens defensivt','Spilintelligens offensivt','Nærkamps- og duelstærk','Samlet']]
        df_Stopperesæsonen = df_Stopperesæsonen.sort_values(by='Samlet',ascending=False)

        df_Stoppere = df_Stoppere[df_Stoppere['Team name'].str.contains('Horsens')]
        df_Stoppere['Pasningssikker'] = (df_Stoppere['Accurate passes score'] + df_Stoppere['Accurate long passes score'] + df_Stoppere['Forward passes score'] + df_Stoppere['Accurate forward passes score'] + df_Stoppere['Accurate progressive passes score'] + df_Stoppere['Accurate vertical passes score'])/6    
        df_Stoppere['Spilintelligens defensivt'] = (df_Stoppere['Interceptions score'] + df_Stoppere['Succesful defensive actions score'] + df_Stoppere['Shots blocked score'] + df_Stoppere['Succesful defensive actions score'] + df_Stoppere['Defensive duels won % score']) /5
        df_Stoppere['Spilintelligens offensivt'] = (df_Stoppere['Forward passes score'] + df_Stoppere['Accurate forward passes score'] + df_Stoppere['Accurate passes to final third'] + df_Stoppere['Passes to final third'] + df_Stoppere['Accurate progressive passes score'] + df_Stoppere['Progressive passes score'] + df_Stoppere['Through passes'] + df_Stoppere['Accurate through passes']+ df_Stoppere['Progressive runs'] + df_Stoppere['Offensive duels won %'] + df_Stoppere['Successful dribbles %'])/11
        df_Stoppere['Nærkamps- og duelstærk'] = (df_Stoppere['Defensive duels won % score'] + df_Stoppere['Aerial duels won % score'] + df_Stoppere['Defensive duels won % score'])/3
        df_Stoppere['Samlet'] = (df_Stoppere['Pasningssikker'] + df_Stoppere['Spilintelligens defensivt'] + df_Stoppere['Spilintelligens offensivt'] + df_Stoppere['Nærkamps- og duelstærk'])/4
        df_Stoppere = df_Stoppere[['Player name','Team name','label','total_minutesOnField_y','Pasningssikker','Spilintelligens defensivt','Spilintelligens offensivt','Nærkamps- og duelstærk','Samlet']]
        df_Stoppere = df_Stoppere.sort_values(by='Samlet',ascending=False)


        df_Stoppere = navne.merge(df_Stoppere)
        df_Stoppere = df_Stoppere.drop('Player Name',axis=1)
        df_Stoppere = df_Stoppere.drop('Player name',axis=1)    
        df_Stopperesæsonen = df_Stopperesæsonen.reset_index()
        df_Stopperesæsonen = navne.merge(df_Stopperesæsonen)
        df_Stoppere = navne.merge(df_Stoppere)
        df_Stopperesæsonen = df_Stopperesæsonen.drop('Player Name',axis=1)
        df_Stopperesæsonen = df_Stopperesæsonen.drop('Player name',axis=1)
        df_Stopperesæsonen = df_Stopperesæsonen.drop('label',axis=1)


        df_Centrale_midt = pd.merge(df_centraleminutter,df_Centrale_midt,on=('Player id'))
        df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['total_minutesOnField_y'] >=17]

        df_Centrale_midt['Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Passes #'] = pd.qcut(df_Centrale_midt['average_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Forward Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Forward Passes #'] = pd.qcut(df_Centrale_midt['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Long Passes %'] = pd.qcut(df_Centrale_midt['percent_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Long Passes #'] = pd.qcut(df_Centrale_midt['average_successfulLongPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Smart passes %'] = pd.qcut(df_Centrale_midt['percent_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Smart passes #'] = pd.qcut(df_Centrale_midt['average_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Key passes %'] = pd.qcut(df_Centrale_midt['percent_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Key passes #'] = pd.qcut(df_Centrale_midt['average_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Passes to final third %'] = pd.qcut(df_Centrale_midt['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Passes to final third #'] = pd.qcut(df_Centrale_midt['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Vertical passes %'] = pd.qcut(df_Centrale_midt['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Vertical passes #'] = pd.qcut(df_Centrale_midt['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Through passes %'] = pd.qcut(df_Centrale_midt['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Through passes #'] = pd.qcut(df_Centrale_midt['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Progressive passes %'] = pd.qcut(df_Centrale_midt['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Progressive passes #'] = pd.qcut(df_Centrale_midt['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Offensive duels %'] = pd.qcut(df_Centrale_midt['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Received passes'] = pd.qcut(df_Centrale_midt['average_receivedPass'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Succesful dribbles %'] = pd.qcut(df_Centrale_midt['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Succesful dribbles #'] = pd.qcut(df_Centrale_midt['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Duels won %'] = pd.qcut(df_Centrale_midt['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Duels won #'] = pd.qcut(df_Centrale_midt['average_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Interceptions'] = pd.qcut(df_Centrale_midt['average_interceptions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Counterpressing recoveries #'] = pd.qcut(df_Centrale_midt['average_counterpressingRecoveries'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Defensive duels won #'] = pd.qcut(df_Centrale_midt['average_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Centrale_midt['Defensive duels won %'] = pd.qcut(df_Centrale_midt['percent_newDefensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

        df_Centrale_midtsæsonen = df_Centrale_midt.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
        df_Centrale_midtsæsonen = df_Centrale_midt.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)
        df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #'] + df_Centrale_midtsæsonen['Forward Passes %'] + df_Centrale_midtsæsonen['Forward Passes #'] + df_Centrale_midtsæsonen['Long Passes %'] + df_Centrale_midtsæsonen['Long Passes #']+ df_Centrale_midtsæsonen['Smart passes %'] + df_Centrale_midtsæsonen['Smart passes #'] + + df_Centrale_midtsæsonen['Key passes %'] + df_Centrale_midtsæsonen['Key passes #'] + df_Centrale_midtsæsonen['Passes to final third %'] + df_Centrale_midtsæsonen['Passes to final third #']+ df_Centrale_midtsæsonen['Vertical passes %'] + df_Centrale_midtsæsonen['Vertical passes #']+ df_Centrale_midtsæsonen['Through passes %'] + df_Centrale_midtsæsonen['Through passes #']+ df_Centrale_midtsæsonen['Progressive passes %'] + df_Centrale_midtsæsonen['Progressive passes #'])/18
        df_Centrale_midtsæsonen['Boldfast'] = (df_Centrale_midtsæsonen['Passes %'] + df_Centrale_midtsæsonen['Passes #']+ df_Centrale_midtsæsonen['Offensive duels %'] + df_Centrale_midtsæsonen['Received passes'] + df_Centrale_midtsæsonen['Succesful dribbles %'] + df_Centrale_midtsæsonen['Succesful dribbles #'])/6
        df_Centrale_midtsæsonen['Spilintelligens defensivt'] = (df_Centrale_midtsæsonen['Duels won %'] + df_Centrale_midtsæsonen['Duels won #'] +df_Centrale_midtsæsonen['Interceptions'] + df_Centrale_midtsæsonen['Counterpressing recoveries #'] + df_Centrale_midtsæsonen['Defensive duels won %'] + df_Centrale_midtsæsonen['Defensive duels won #'])/6
        df_Centrale_midtsæsonen['Samlet'] = (df_Centrale_midtsæsonen['Pasningssikker/Spilvendinger'] + df_Centrale_midtsæsonen['Boldfast'] + df_Centrale_midtsæsonen['Spilintelligens defensivt'])/3
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen[['Pasningssikker/Spilvendinger','Boldfast','Spilintelligens defensivt','Samlet']]
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.sort_values(by='Samlet',ascending=False)

        df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['Team name'].str.contains('Horsens')]
        df_Centrale_midt['Pasningssikker/Spilvendinger'] = (df_Centrale_midt['Passes %'] + df_Centrale_midt['Passes #'] + df_Centrale_midt['Forward Passes %'] + df_Centrale_midt['Forward Passes #'] + df_Centrale_midt['Long Passes %'] + df_Centrale_midt['Long Passes #']+ df_Centrale_midt['Smart passes %'] + df_Centrale_midt['Smart passes #'] + + df_Centrale_midt['Key passes %'] + df_Centrale_midt['Key passes #'] + df_Centrale_midt['Passes to final third %'] + df_Centrale_midt['Passes to final third #']+ df_Centrale_midt['Vertical passes %'] + df_Centrale_midt['Vertical passes #']+ df_Centrale_midt['Through passes %'] + df_Centrale_midt['Through passes #']+ df_Centrale_midt['Progressive passes %'] + df_Centrale_midt['Progressive passes #'])/18
        df_Centrale_midt['Boldfast'] = (df_Centrale_midt['Passes %'] + df_Centrale_midt['Passes #']+ df_Centrale_midt['Offensive duels %'] + df_Centrale_midt['Received passes'] + df_Centrale_midt['Succesful dribbles %'] + df_Centrale_midt['Succesful dribbles #'])/6
        df_Centrale_midt['Spilintelligens defensivt'] = (df_Centrale_midt['Duels won %'] + df_Centrale_midt['Duels won #'] +df_Centrale_midt['Interceptions'] + df_Centrale_midt['Counterpressing recoveries #'] + df_Centrale_midt['Defensive duels won %'] + df_Centrale_midt['Defensive duels won #'])/6
        df_Centrale_midt['Samlet'] = (df_Centrale_midt['Pasningssikker/Spilvendinger'] + df_Centrale_midt['Boldfast'] + df_Centrale_midt['Spilintelligens defensivt'])/3
        df_Centrale_midt = df_Centrale_midt[['Player name','Team name','label','total_minutesOnField_y','Pasningssikker/Spilvendinger','Boldfast','Spilintelligens defensivt','Samlet']]
        df_Centrale_midt = df_Centrale_midt.sort_values(by='Samlet',ascending=False)

        df_Centrale_midt = navne.merge(df_Centrale_midt)
        df_Centrale_midt = df_Centrale_midt.drop('Player Name',axis=1)
        df_Centrale_midt = df_Centrale_midt.drop('Player name',axis=1)    
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.reset_index()
        df_Centrale_midtsæsonen = navne.merge(df_Centrale_midtsæsonen)
        df_Centrale_midt = navne.merge(df_Centrale_midt)
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.drop('Player Name',axis=1)
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.drop('Player name',axis=1)
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.drop('label',axis=1)


        df_Kanter = pd.merge(df_kanterminutter,df_Kanter,on=('Player id'))
        df_Kanter = df_Kanter[df_Kanter['total_minutesOnField_y'] >=17]

        df_Kanter['Shots on target %'] = pd.qcut(df_Kanter['percent_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Shots on target #'] = pd.qcut(df_Kanter['average_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['XG'] = pd.qcut(df_Kanter['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Successful dribbles #'] = pd.qcut(df_Kanter['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Successful dribbles %'] = pd.qcut(df_Kanter['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Offensive duels %'] = pd.qcut(df_Kanter['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Offensive duels #'] = pd.qcut(df_Kanter['average_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Passes %'] = pd.qcut(df_Kanter['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Passes #'] = pd.qcut(df_Kanter['average_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Forward Passes %'] = pd.qcut(df_Kanter['percent_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Forward Passes #'] = pd.qcut(df_Kanter['average_successfulForwardPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Smart passes %'] = pd.qcut(df_Kanter['percent_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Smart passes #'] = pd.qcut(df_Kanter['average_successfulSmartPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Key passes %'] = pd.qcut(df_Kanter['percent_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Key passes #'] = pd.qcut(df_Kanter['average_successfulKeyPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Passes to final third %'] = pd.qcut(df_Kanter['percent_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Passes to final third #'] = pd.qcut(df_Kanter['average_successfulPassesToFinalThird'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Vertical passes %'] = pd.qcut(df_Kanter['percent_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Vertical passes #'] = pd.qcut(df_Kanter['average_successfulVerticalPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Through passes %'] = pd.qcut(df_Kanter['percent_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Through passes #'] = pd.qcut(df_Kanter['average_successfulThroughPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Progressive passes %'] = pd.qcut(df_Kanter['percent_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Progressive passes #'] = pd.qcut(df_Kanter['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Goal conversion %'] = pd.qcut(df_Kanter['percent_goalConversion'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['XG per 90'] = pd.qcut(df_Kanter['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['XA per 90'] = pd.qcut(df_Kanter['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Successful attacking actions'] = pd.qcut(df_Kanter['average_successfulAttackingActions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Progressive runs'] = pd.qcut(df_Kanter['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Kanter['Accelerations score'] = pd.qcut(df_Kanter['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

        df_Kantersæsonen = df_Kanter.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)
    
        df_Kantersæsonen = df_Kanter.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

        df_Kantersæsonen['Sparkefærdigheder'] = (df_Kantersæsonen['Shots on target %'] + df_Kantersæsonen['Shots on target #'] + df_Kantersæsonen['XG'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Vertical passes %'])/6
        df_Kantersæsonen['Kombinationsstærk'] = (df_Kantersæsonen['Passes %'] + df_Kantersæsonen['Passes #'] + df_Kantersæsonen['Forward Passes %'] + df_Kantersæsonen['Forward Passes #'] + df_Kantersæsonen['Passes to final third %'] + df_Kantersæsonen['Passes to final third #'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
        df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] = (df_Kantersæsonen['XA per 90'] + df_Kantersæsonen['XG per 90'] + df_Kantersæsonen['Through passes %'] + df_Kantersæsonen['Through passes #'] + df_Kantersæsonen['Smart passes %'] + df_Kantersæsonen['Smart passes #'] + df_Kantersæsonen['Progressive passes %'] + df_Kantersæsonen['Progressive passes #'] + df_Kantersæsonen['Key passes %'] + df_Kantersæsonen['Key passes #'] + df_Kantersæsonen['Successful attacking actions'])/11
        df_Kantersæsonen['1v1 offensivt'] = (df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Offensive duels #'] + df_Kantersæsonen['Offensive duels %'] + df_Kantersæsonen['Progressive runs'])/5
        df_Kantersæsonen['Fart'] = (df_Kantersæsonen['Progressive runs'] + df_Kantersæsonen['Successful dribbles #'] + df_Kantersæsonen['Successful dribbles %'] + df_Kantersæsonen['Accelerations score'])/5
        df_Kantersæsonen['Samlet'] = (df_Kantersæsonen['Sparkefærdigheder'] + df_Kantersæsonen['Kombinationsstærk'] + df_Kantersæsonen['Spilintelligens offensivt/indlægsstærk'] + df_Kantersæsonen['1v1 offensivt'] + df_Kantersæsonen['Fart'])/5
        df_Kantersæsonen = df_Kantersæsonen[['Sparkefærdigheder','Kombinationsstærk','Spilintelligens offensivt/indlægsstærk','1v1 offensivt','Fart','Samlet']]
        df_Kantersæsonen = df_Kantersæsonen.sort_values(by='Samlet',ascending=False)
        df_Kanter = df_Kanter[df_Kanter['Team name'].str.contains('Horsens')]
        df_Kanter['Sparkefærdigheder'] = (df_Kanter['Shots on target %'] + df_Kanter['Shots on target #'] + df_Kanter['XG'] + df_Kanter['Passes to final third %'] + df_Kanter['Forward Passes %'] + df_Kanter['Vertical passes %'])/6
        df_Kanter['Kombinationsstærk'] = (df_Kanter['Passes %'] + df_Kanter['Passes #'] + df_Kanter['Forward Passes %'] + df_Kanter['Forward Passes #'] + df_Kanter['Passes to final third %'] + df_Kanter['Passes to final third #'] + df_Kanter['Through passes %'] + df_Kanter['Through passes #'] + df_Kanter['Progressive passes %'] + df_Kanter['Progressive passes #'] + df_Kanter['Successful attacking actions'])/11
        df_Kanter['Spilintelligens offensivt/indlægsstærk'] = (df_Kanter['XA per 90'] + df_Kanter['XG per 90'] + df_Kanter['Through passes %'] + df_Kanter['Through passes #'] + df_Kanter['Smart passes %'] + df_Kanter['Smart passes #'] + df_Kanter['Progressive passes %'] + df_Kanter['Progressive passes #'] + df_Kanter['Key passes %'] + df_Kanter['Key passes #'] + df_Kanter['Successful attacking actions'])/11
        df_Kanter['1v1 offensivt'] = (df_Kanter['Successful dribbles #'] + df_Kanter['Successful dribbles %'] + df_Kanter['Offensive duels #'] + df_Kanter['Offensive duels %'] + df_Kanter['Progressive runs'])/5
        df_Kanter['Fart'] = (df_Kanter['Progressive runs'] + df_Kanter['Successful dribbles #'] + df_Kanter['Successful dribbles %'] + df_Kanter['Accelerations score'])/5
        df_Kanter['Samlet'] = (df_Kanter['Sparkefærdigheder'] + df_Kanter['Kombinationsstærk'] + df_Kanter['Spilintelligens offensivt/indlægsstærk'] + df_Kanter['1v1 offensivt'] + df_Kanter['Fart'])/5
        df_Kanter = df_Kanter[['Player name','Team name','label','total_minutesOnField_y','Sparkefærdigheder','Kombinationsstærk','Spilintelligens offensivt/indlægsstærk','1v1 offensivt','Fart','Samlet']]
        df_Kanter = df_Kanter.sort_values(by='Samlet',ascending=False)

        df_Kanter = navne.merge(df_Kanter)
        df_Kanter = df_Kanter.drop('Player Name',axis=1)
        df_Kanter = df_Kanter.drop('Player name',axis=1)    
        df_Kantersæsonen=df_Kantersæsonen.reset_index()
        df_Kantersæsonen = navne.merge(df_Kantersæsonen)
        df_Kanter = navne.merge(df_Kanter)
        df_Kantersæsonen= df_Kantersæsonen.drop('Player Name',axis=1)
        df_Kantersæsonen = df_Kantersæsonen.drop('Player name',axis=1)
        df_Kantersæsonen = df_Kantersæsonen.drop('label',axis=1)
    
        
        df_Angribere = pd.merge(df_angribereminutter,df_Angribere,on=('Player id'))
        df_Angribere = df_Angribere[df_Angribere['total_minutesOnField_y'] >=17]

        df_Angribere['Målfarlighed udregning'] = df_Angribere['average_goals'] - df_Angribere['average_xgShot']
        df_Angribere['Målfarlighed score'] =  pd.qcut(df_Angribere['Målfarlighed udregning'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['xG per 90 score'] = pd.qcut(df_Angribere['average_xgShot'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Goals per 90 score'] = pd.qcut(df_Angribere['average_goals'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)  
        df_Angribere['Shots on target, % score'] = pd.qcut(df_Angribere['percent_shotsOnTarget'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)   
        df_Angribere['Offensive duels won, % score'] = pd.qcut(df_Angribere['percent_newOffensiveDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Duels won, % score'] = pd.qcut(df_Angribere['percent_newDuelsWon'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Accurate passes, % score'] = pd.qcut(df_Angribere['percent_successfulPasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Successful dribbles, % score'] = pd.qcut(df_Angribere['percent_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['xA per 90 score'] = pd.qcut(df_Angribere['average_xgAssist'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Touches in box per 90 score'] = pd.qcut(df_Angribere['average_touchInBox'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Progressive runs'] = pd.qcut(df_Angribere['average_progressiveRun'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Accelerations score'] = pd.qcut(df_Angribere['average_accelerations'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Progressive passes per 90 score'] = pd.qcut(df_Angribere['average_successfulProgressivePasses'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Successful attacking actions per 90 score'] = pd.qcut(df_Angribere['average_successfulAttackingActions'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)
        df_Angribere['Successful dribbles #'] = pd.qcut(df_Angribere['average_newSuccessfulDribbles'].rank(method='first'), 5,['1','2','3','4','5']).astype(int)

        df_Angriberesæsonen = df_Angribere.rename(columns={'total_minutesOnField_x':'Total minutes'},inplace=True)

        df_Angriberesæsonen = df_Angribere.groupby(['Player name','Team name','Total minutes','label']).mean(numeric_only=True)

        df_Angriberesæsonen['Sparkefærdigheder'] = (df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Goals per 90 score'] + df_Angriberesæsonen['Shots on target, % score'])/4
        df_Angriberesæsonen['Boldfast'] = (df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Offensive duels won, % score'] + df_Angriberesæsonen['Duels won, % score'] + df_Angriberesæsonen['Accurate passes, % score'] + df_Angriberesæsonen['Successful dribbles, % score'])/5
        df_Angriberesæsonen['Spilintelligens offensivt'] = (df_Angriberesæsonen['xA per 90 score'] + df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['Progressive passes per 90 score'] + df_Angriberesæsonen['Successful attacking actions per 90 score'] + df_Angriberesæsonen['Touches in box per 90 score'] + df_Angriberesæsonen['xG per 90 score'])/7
        df_Angriberesæsonen['Målfarlighed'] = (df_Angriberesæsonen['xG per 90 score']+df_Angriberesæsonen['Goals per 90 score']+df_Angriberesæsonen['xG per 90 score'] + df_Angriberesæsonen['Målfarlighed score'])/4
        df_Angriberesæsonen['Fart'] = (df_Angriberesæsonen['Progressive runs'] + + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Progressive runs'] + df_Angriberesæsonen['Successful dribbles #'] + df_Angriberesæsonen['Successful dribbles, % score'] + df_Angriberesæsonen['Accelerations score'] + df_Angriberesæsonen['Offensive duels won, % score'])/7
        df_Angriberesæsonen = df_Angriberesæsonen[['Sparkefærdigheder','Boldfast','Spilintelligens offensivt','Målfarlighed','Fart']]
        df_Angriberesæsonen['Samlet'] = (df_Angriberesæsonen['Sparkefærdigheder']+df_Angriberesæsonen['Boldfast']+df_Angriberesæsonen['Spilintelligens offensivt']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Målfarlighed']+df_Angriberesæsonen['Fart'])/7
        df_Angriberesæsonen = df_Angriberesæsonen.sort_values(by='Samlet',ascending=False)
        df_Angriberesæsonen = df_Angriberesæsonen[df_Angriberesæsonen.index.get_level_values('Team name').str.contains('Horsens')]

        df_Angribere = df_Angribere[df_Angribere['Team name'].str.contains('Horsens')]
        df_Angribere['Sparkefærdigheder'] = (df_Angribere['xG per 90 score'] + df_Angribere['xG per 90 score'] + df_Angribere['Goals per 90 score'] + df_Angribere['Shots on target, % score'])/4
        df_Angribere['Boldfast'] = (df_Angribere['Offensive duels won, % score'] + df_Angribere['Offensive duels won, % score'] + df_Angribere['Duels won, % score'] + df_Angribere['Accurate passes, % score'] + df_Angribere['Successful dribbles, % score'])/5
        df_Angribere['Spilintelligens offensivt'] = (df_Angribere['xA per 90 score'] + df_Angribere['xG per 90 score'] + df_Angribere['Touches in box per 90 score'] + df_Angribere['Progressive passes per 90 score'] + df_Angribere['Successful attacking actions per 90 score'] + df_Angribere['Touches in box per 90 score'] + df_Angribere['xG per 90 score'])/7
        df_Angribere['Målfarlighed'] = (df_Angribere['xG per 90 score']+df_Angribere['Goals per 90 score']+df_Angribere['xG per 90 score'] + df_Angribere['Målfarlighed score'])/4
        df_Angribere['Fart'] = (df_Angribere['Progressive runs'] + + df_Angribere['Progressive runs'] + df_Angribere['Progressive runs'] + df_Angribere['Successful dribbles #'] + df_Angribere['Successful dribbles, % score'] + df_Angribere['Accelerations score'] + df_Angribere['Offensive duels won, % score'])/7
        df_Angribere = df_Angribere[['Player name','Team name','label','total_minutesOnField_y','Sparkefærdigheder','Boldfast','Spilintelligens offensivt','Målfarlighed','Fart']]
        df_Angribere['Samlet'] = (df_Angribere['Sparkefærdigheder']+df_Angribere['Boldfast']+df_Angribere['Spilintelligens offensivt']+df_Angribere['Målfarlighed']+df_Angribere['Målfarlighed']+df_Angribere['Målfarlighed']+df_Angribere['Fart'])/7
        df_Angribere = df_Angribere.sort_values(by='Samlet',ascending=False)
        
        kampe = df['label']
        kampe = kampe[kampe.str.contains('Horsens')]
        kampe = kampe.drop_duplicates(keep='first')  
        
        df_Angribere = navne.merge(df_Angribere)
        df_Angribere = df_Angribere.drop('Player Name',axis=1)
        df_Angribere = df_Angribere.drop('Player name',axis=1)
        df_Angriberesæsonen=df_Angriberesæsonen.reset_index()
        df_Angriberesæsonen = navne.merge(df_Angriberesæsonen)
        df_Angribere = navne.merge(df_Angribere)
        df_Angriberesæsonen= df_Angriberesæsonen.drop('Player Name',axis=1)
        df_Angriberesæsonen = df_Angriberesæsonen.drop('Player name',axis=1)
        df_Angriberesæsonen = df_Angriberesæsonen.drop('label',axis=1)
        
        option2 = st.selectbox('Vælg spiller',navneliste)
        df_Angriberesæsonen = df_Angriberesæsonen[df_Angriberesæsonen['Spillere'].str.contains(option2)]
        df_Angribere = df_Angribere[df_Angribere['Spillere'].str.contains(option2)]
        df_Kantersæsonen = df_Kantersæsonen[df_Kantersæsonen['Spillere'].str.contains(option2)]
        df_Kanter = df_Kanter[df_Kanter['Spillere'].str.contains(option2)]
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen[df_Centrale_midtsæsonen['Spillere'].str.contains(option2)]
        df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['Spillere'].str.contains(option2)]
        df_Stopperesæsonen = df_Stopperesæsonen[df_Stopperesæsonen['Spillere'].str.contains(option2)]
        df_Stoppere = df_Stoppere[df_Stoppere['Spillere'].str.contains(option2)]
        df_backssæsonen = df_backssæsonen[df_backs['Spillere'].str.contains(option2)]
        df_backs = df_backs[df_backs['Spillere'].str.contains(option2)]

        option = st.multiselect('Vælg kamp (Hvis ingen kamp er valgt, vises alle)',kampe)
        if len(option) > 0:
            temp_select = option
        else:
            temp_select = kampe

        df_backs = df_backs[df_backs['label'].isin(temp_select)]
        df_backs = df_backs.drop('label',axis=1)
        df_backssæsonen = df_backssæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()
        
        df_backs = df_backs.groupby(['Spillere','Trup','Team name']).agg({
        'total_minutesOnField_y':'sum',
        'Indlægsstærk':'mean',
        '1v1 færdigheder':'mean',
        'Spilintelligens defensivt':'mean',
        'Fart':'mean',
        'Samlet':'mean'
        })

        df_backs = df_backs.sort_values(by='Samlet',ascending=False)
        df_backs = df_backs.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
        df_backs = df_backs.reset_index()
        df_backs = df_backs.set_index(['Spillere','Trup','Team name'])
        df_backssæsonen = df_backssæsonen.reset_index()
        df_backssæsonen = df_backssæsonen.set_index(['Spillere','Trup','Team name'])
        df_backs = pd.concat([df_backs,df_backssæsonen],axis=0)        

        df_Stoppere = df_Stoppere[df_Stoppere['label'].isin(temp_select)]
        df_Stoppere = df_Stoppere.drop('label',axis=1)
        df_Stopperesæsonen = df_Stopperesæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()
        
        df_Stoppere = df_Stoppere.groupby(['Spillere','Trup','Team name']).agg({
        'total_minutesOnField_y':'sum',
        'Pasningssikker':'mean',
        'Spilintelligens offensivt':'mean',
        'Spilintelligens defensivt':'mean',
        'Nærkamps- og duelstærk':'mean',
        'Samlet':'mean'
        })

        df_Stoppere = df_Stoppere.sort_values(by='Samlet',ascending=False)
        df_Stoppere = df_Stoppere.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
        df_Stoppere = df_Stoppere.reset_index()
        df_Stoppere = df_Stoppere.set_index(['Spillere','Trup','Team name'])
        df_Stopperesæsonen = df_Stopperesæsonen.reset_index()
        df_Stopperesæsonen = df_Stopperesæsonen.set_index(['Spillere','Trup','Team name'])
        df_Stoppere = pd.concat([df_Stoppere,df_Stopperesæsonen],axis=0)

        df_Centrale_midt = df_Centrale_midt[df_Centrale_midt['label'].isin(temp_select)]
        df_Centrale_midt = df_Centrale_midt.drop('label',axis=1)
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()
        
        df_Centrale_midt = df_Centrale_midt.groupby(['Spillere','Trup','Team name']).agg({
        'total_minutesOnField_y':'sum',
        'Pasningssikker/Spilvendinger':'mean',
        'Boldfast':'mean',
        'Spilintelligens defensivt':'mean',
        'Samlet':'mean'
        })

        df_Centrale_midt = df_Centrale_midt.sort_values(by='Samlet',ascending=False)
        df_Centrale_midt = df_Centrale_midt.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
        df_Centrale_midt = df_Centrale_midt.reset_index()
        df_Centrale_midt = df_Centrale_midt.set_index(['Spillere','Trup','Team name'])
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.reset_index()
        df_Centrale_midtsæsonen = df_Centrale_midtsæsonen.set_index(['Spillere','Trup','Team name'])
        df_Centrale_midt = pd.concat([df_Centrale_midt,df_Centrale_midtsæsonen],axis=0)
    
            
        df_Kanter = df_Kanter[df_Kanter['label'].isin(temp_select)]
        df_Kanter = df_Kanter.drop('label',axis=1)
        df_Kantersæsonen = df_Kantersæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()
        
        df_Kanter = df_Kanter.groupby(['Spillere','Trup','Team name']).agg({
        'total_minutesOnField_y':'sum',
        'Sparkefærdigheder':'mean',
        'Kombinationsstærk':'mean',
        'Spilintelligens offensivt/indlægsstærk':'mean',
        '1v1 offensivt':'mean',
        'Fart':'mean',
        'Samlet':'mean'
        })
        
        df_Kanter = df_Kanter.sort_values(by='Samlet',ascending=False)
        df_Kanter = df_Kanter.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
        df_Kanter = df_Kanter.reset_index()
        df_Kanter = df_Kanter.set_index(['Spillere','Trup','Team name'])
        df_Kantersæsonen = df_Kantersæsonen.reset_index()
        df_Kantersæsonen = df_Kantersæsonen.set_index(['Spillere','Trup','Team name'])
        df_Kanter = pd.concat([df_Kanter,df_Kantersæsonen],axis=0)

        
        df_Angribere = df_Angribere[df_Angribere['label'].isin(temp_select)]
        df_Angribere = df_Angribere.drop('label',axis=1)
        df_Angriberesæsonen = df_Angriberesæsonen.groupby(['Spillere','Trup','Team name','Total minutes']).mean()

        df_Angribere = df_Angribere.groupby(['Spillere','Trup','Team name']).agg({
        'total_minutesOnField_y':'sum',
        'Sparkefærdigheder': 'mean',
        'Boldfast': 'mean',
        'Spilintelligens offensivt':'mean',
        'Målfarlighed':'mean',
        'Fart':'mean',
        'Samlet':'mean',
        })

        df_Angribere = df_Angribere.sort_values(by = 'Samlet',ascending=False)
        df_Angribere = df_Angribere.rename(columns={'total_minutesOnField_y':'Total minutes'},inplace=False)
        df_Angribere = df_Angribere.reset_index()
        df_Angribere = df_Angribere.set_index(['Spillere','Trup','Team name'])
        df_Angriberesæsonen = df_Angriberesæsonen.reset_index()
        df_Angriberesæsonen = df_Angriberesæsonen.set_index(['Spillere','Trup','Team name'])
        df_Angribere = pd.concat([df_Angribere,df_Angriberesæsonen],axis=0)
        #st.dataframe(df_Angribere)
        #st.write('Angribere')
        dataframe_names = ['Stopper', 'Back', 'Central midt', 'Kant', 'Angriber']

        # Create the selectbox in Streamlit
        selected_dataframe = st.selectbox('Position', options=dataframe_names)

        # Based on the selected dataframe, retrieve the corresponding dataframe object
        if selected_dataframe == 'Stopper':
            selected_df = df_Stoppere
        elif selected_dataframe == 'Back':
            selected_df = df_backs
        elif selected_dataframe == 'Central midt':
            selected_df = df_Centrale_midt
        elif selected_dataframe == 'Kant':
            selected_df = df_Kanter
        elif selected_dataframe == 'Angriber':
            selected_df = df_Angribere

        st.dataframe(selected_df)
        df_filtered = selected_df.iloc[:, 1:]

        # Create a scatterpolar plot using plotly
        fig = go.Figure()

        # Iterate over each row in the dataframe
        for _, row in df_filtered.iterrows():
            fig.add_trace(go.Scatterpolar(
                r=row.values,
                theta=df_filtered.columns,
                fill='toself'
            ))
        fig.data[0].name = 'Valgte periode'
        fig.data[1].name = 'Hele sæsonen'
        # Set plot title and layout
        fig.update_layout(
            title='Scatterpolar Plot',
            template='plotly_dark',
            polar=dict(
                radialaxis=dict
                    (visible=True,
                    range=[1,5]
                )
            )
        )
        # Render the plot within Streamlit
        st.plotly_chart(fig)


    Årgange = {'U15':U15,
            'U17':U17,
            'U19':U19}
    rullemenu = st.selectbox('Vælg årgang',Årgange.keys())
    Årgange[rullemenu]()


def event_data():
    def U15():
        import pandas as pd
        import streamlit as st
        from mplsoccer.pitch import Pitch
        import matplotlib.pyplot as plt
        import plotly.express as px
        from dateutil import parser

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
        from dateutil import parser

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
        from dateutil import parser

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
