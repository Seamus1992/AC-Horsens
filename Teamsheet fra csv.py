import streamlit as st
def U15():
    import pandas as pd
    import csv
    import streamlit as st
    import numpy as np
    from datetime import datetime
    df = pd.read_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Teamsheet egne kampe U15.csv')
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

    df = pd.read_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Teamsheet alle kampe U15.csv')

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


    df = pd.read_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Teamsheet alle kampe U15 sidste sæson.csv')

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
    
    
def U17():
    import pandas as pd
    import csv
    import streamlit as st
    import numpy as np
    from datetime import datetime
    df = pd.read_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Teamsheet egne kampe U17.csv')
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

    df = pd.read_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Teamsheet alle kampe U17.csv')

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


    df = pd.read_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Teamsheet alle kampe U17 sidste sæson.csv')

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
    df = pd.read_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Teamsheet egne kampe U19.csv')
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

    df = pd.read_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Teamsheet alle kampe U19.csv')

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


    df = pd.read_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Teamsheet alle kampe U19 sidste sæson.csv')

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


