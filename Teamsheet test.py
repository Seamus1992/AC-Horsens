from azure.storage.fileshare import ShareServiceClient
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
import os
import streamlit as st
connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 22-23/U15 Ligaen/'


service_client = ShareServiceClient.from_connection_string(connection_string)
share_client = service_client.get_share_client(share_name)
directory_client = share_client.get_directory_client(dir_path)

json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchAdvanceStats' in item.name:
            # If the item is a JSON file with 'MatchAdvanceStats' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
df = pd.json_normalize(json_files)
df = pd.DataFrame(df)
df.columns = df.columns.str.replace('66870','Horsens U15')
df.columns = df.columns.str.replace('65133','Esbjerg U15')
df.columns = df.columns.str.replace('65132','København U15')
df.columns = df.columns.str.replace('65130','Silkeborg U15')
df.columns = df.columns.str.replace('65129','SønderjyskE U15')
df.columns = df.columns.str.replace('65128','AAB U15')
df.columns = df.columns.str.replace('65127','OB U15')
df.columns = df.columns.str.replace('65126','Vejle U15')
df.columns = df.columns.str.replace('65125','Randers U15')
df.columns = df.columns.str.replace('65124','FC Nordsjælland U15')
df.columns = df.columns.str.replace('65122','Midtjylland U15')
df.columns = df.columns.str.replace('65121','AGF U15')
df.columns = df.columns.str.replace('64359','Lyngby U15')
df.columns = df.columns.str.replace('22392','Brøndby IF U15')
df.columns = df.columns.str.replace('general.','')
possession_cols = [col for col in df.columns if col.startswith('possession')]
df.columns = df.columns.where(~df.columns.str.startswith('possession.'), df.columns.str.replace('possession.', ''))
#df.columns = df.columns.str.replace('openplay.','')
#df.columns = df.columns.str.replace('attacks.','')
#df.columns = df.columns.str.replace('transitions.','')
#df.columns = df.columns.str.replace('passes.','')
#df.columns = df.columns.str.replace('defence.','')
#df.columns = df.columns.str.replace('duels.','')
#df.columns = df.columns.str.replace('flanks.','')


json_files = []

def find_json_files(directory_client):
    for item in directory_client.list_directories_and_files():
        if item.is_directory:
            if 'AC Horsens' in item.name:
                # Recursively search for JSON files in the subdirectory if it contains 'AC Horsens' in its name
                sub_directory_client = directory_client.get_subdirectory_client(item.name)
                find_json_files(sub_directory_client)
            else:
                # Otherwise, continue searching in the current directory
                find_json_files(directory_client.get_subdirectory_client(item.name))
        elif item.name.endswith('.json') and 'MatchDetail' in item.name:
            # If the item is a JSON file with 'MatchEvents' in the name, download it and append its data to the list
            json_files.append(json.loads(directory_client.get_file_client(item.name).download_file().readall().decode()))
find_json_files(directory_client)
kampdetaljer = json_normalize(json_files)
kampdetaljer = kampdetaljer[['wyId','label','date']]
kampdetaljer = kampdetaljer.rename(columns={'wyId':'matchId'})

dfegnekampe = kampdetaljer.merge(df)
dfegnekampe['label'] = dfegnekampe['label'].astype(str)
dfegnekampe = dfegnekampe[dfegnekampe['label'].str.contains('Horsens')]
dfegnekampe.to_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Teamsheet egne kampe.csv',index=False)
st.dataframe(dfegnekampe)
