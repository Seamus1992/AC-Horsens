from azure.storage.fileshare import ShareServiceClient
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
import os
import streamlit as st
connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 21-22/U15 Ligaen/'


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
df.columns = df.columns.str.replace('66870','Horsens U15 sidste sæson')
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
#df.columns = df.columns.str.replace('general.','')
#possession_cols = [col for col in df.columns if col.startswith('possession')]
#df.columns = df.columns.where(~df.columns.str.startswith('possession.'), df.columns.str.replace('possession.', ''))
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
dfegnekampe.to_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Teamsheet alle kampe U15 sidste sæson.csv',index=False)

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
#df.columns = df.columns.str.replace('general.','')
#possession_cols = [col for col in df.columns if col.startswith('possession')]
#df.columns = df.columns.where(~df.columns.str.startswith('possession.'), df.columns.str.replace('possession.', ''))
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
#dfegnekampe = dfegnekampe[dfegnekampe['label'].str.contains('Horsens')]
dfegnekampe.to_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Teamsheet alle kampe U15.csv',index=False)

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
#df.columns = df.columns.str.replace('general.','')
#possession_cols = [col for col in df.columns if col.startswith('possession')]
#df.columns = df.columns.where(~df.columns.str.startswith('possession.'), df.columns.str.replace('possession.', ''))
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
dfegnekampe.to_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Teamsheet egne kampe U15.csv',index=False)


#Start på U17
connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 21-22/U17 Ligaen/'


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
df.columns = df.columns.str.replace('30685','Horsens U17 sidste sæson')
df.columns = df.columns.str.replace('27148','Esbjerg U17')
df.columns = df.columns.str.replace('27144','København U17')
df.columns = df.columns.str.replace('27147','Silkeborg U17')
df.columns = df.columns.str.replace('62977','SønderjyskE U17')
df.columns = df.columns.str.replace('27142','AAB U17')
df.columns = df.columns.str.replace('27143','OB U17')
df.columns = df.columns.str.replace('27141','Vejle U17')
df.columns = df.columns.str.replace('27140','Randers U17')
df.columns = df.columns.str.replace('27149','FC Nordsjælland U17')
df.columns = df.columns.str.replace('27139','Midtjylland U17')
df.columns = df.columns.str.replace('27145','AGF U17')
df.columns = df.columns.str.replace('27152','Lyngby U17')
df.columns = df.columns.str.replace('27146','Brøndby IF U17')
#df.columns = df.columns.str.replace('general.','')
#possession_cols = [col for col in df.columns if col.startswith('possession')]
#df.columns = df.columns.where(~df.columns.str.startswith('possession.'), df.columns.str.replace('possession.', ''))
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
dfegnekampe.to_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Teamsheet alle kampe U17 sidste sæson.csv',index=False)

from azure.storage.fileshare import ShareServiceClient
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
import os
import streamlit as st
connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 22-23/U17 Ligaen/'


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
df.columns = df.columns.str.replace('30685','Horsens U17')
df.columns = df.columns.str.replace('27148','Esbjerg U17')
df.columns = df.columns.str.replace('27144','København U17')
df.columns = df.columns.str.replace('27147','Silkeborg U17')
df.columns = df.columns.str.replace('62977','SønderjyskE U17')
df.columns = df.columns.str.replace('27142','AAB U17')
df.columns = df.columns.str.replace('27143','OB U17')
df.columns = df.columns.str.replace('27141','Vejle U17')
df.columns = df.columns.str.replace('27140','Randers U17')
df.columns = df.columns.str.replace('27149','FC Nordsjælland U17')
df.columns = df.columns.str.replace('27139','Midtjylland U17')
df.columns = df.columns.str.replace('27145','AGF U17')
df.columns = df.columns.str.replace('27152','Lyngby U17')
df.columns = df.columns.str.replace('27146','Brøndby IF U17')
#df.columns = df.columns.str.replace('general.','')
#possession_cols = [col for col in df.columns if col.startswith('possession')]
#df.columns = df.columns.where(~df.columns.str.startswith('possession.'), df.columns.str.replace('possession.', ''))
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
#dfegnekampe = dfegnekampe[dfegnekampe['label'].str.contains('Horsens')]
dfegnekampe.to_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Teamsheet alle kampe U17.csv',index=False)

from azure.storage.fileshare import ShareServiceClient
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
import os
import streamlit as st
connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 22-23/U17 Ligaen/'


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
df.columns = df.columns.str.replace('30685','Horsens U17')
df.columns = df.columns.str.replace('27148','Esbjerg U17')
df.columns = df.columns.str.replace('27144','København U17')
df.columns = df.columns.str.replace('27147','Silkeborg U17')
df.columns = df.columns.str.replace('62977','SønderjyskE U17')
df.columns = df.columns.str.replace('27142','AAB U17')
df.columns = df.columns.str.replace('27143','OB U17')
df.columns = df.columns.str.replace('27141','Vejle U17')
df.columns = df.columns.str.replace('27140','Randers U17')
df.columns = df.columns.str.replace('27149','FC Nordsjælland U17')
df.columns = df.columns.str.replace('27139','Midtjylland U17')
df.columns = df.columns.str.replace('27145','AGF U17')
df.columns = df.columns.str.replace('27152','Lyngby U17')
df.columns = df.columns.str.replace('27146','Brøndby IF U17')
#df.columns = df.columns.str.replace('general.','')
#possession_cols = [col for col in df.columns if col.startswith('possession')]
#df.columns = df.columns.where(~df.columns.str.startswith('possession.'), df.columns.str.replace('possession.', ''))
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
dfegnekampe.to_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Teamsheet egne kampe U17.csv',index=False)


#Start på U19
connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 21-22/U19 Ligaen/'


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
df.columns = df.columns.str.replace('38324','Horsens U19 sidste sæson')
df.columns = df.columns.str.replace('23735','Esbjerg U19')
df.columns = df.columns.str.replace('23732','København U19')
df.columns = df.columns.str.replace('23736','Silkeborg U19')
df.columns = df.columns.str.replace('23738','SønderjyskE U19')
df.columns = df.columns.str.replace('23730','AAB U19')
df.columns = df.columns.str.replace('23726','OB U19')
df.columns = df.columns.str.replace('23733','Vejle U19')
df.columns = df.columns.str.replace('23737','Randers U19')
df.columns = df.columns.str.replace('23727','FC Nordsjælland U19')
df.columns = df.columns.str.replace('23729','Midtjylland U19')
df.columns = df.columns.str.replace('25612','AGF U19')
df.columns = df.columns.str.replace('23731','Lyngby U19')
df.columns = df.columns.str.replace('23734','Brøndby IF U19')
#df.columns = df.columns.str.replace('general.','')
#possession_cols = [col for col in df.columns if col.startswith('possession')]
#df.columns = df.columns.where(~df.columns.str.startswith('possession.'), df.columns.str.replace('possession.', ''))
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
dfegnekampe.to_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Teamsheet alle kampe U19 sidste sæson.csv',index=False)

from azure.storage.fileshare import ShareServiceClient
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
import os
import streamlit as st
connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 22-23/U19 Ligaen/'


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
df.columns = df.columns.str.replace('38324','Horsens U19')
df.columns = df.columns.str.replace('23735','Esbjerg U19')
df.columns = df.columns.str.replace('23732','København U19')
df.columns = df.columns.str.replace('23736','Silkeborg U19')
df.columns = df.columns.str.replace('23738','SønderjyskE U19')
df.columns = df.columns.str.replace('23730','AAB U19')
df.columns = df.columns.str.replace('23726','OB U19')
df.columns = df.columns.str.replace('23733','Vejle U19')
df.columns = df.columns.str.replace('23737','Randers U19')
df.columns = df.columns.str.replace('23727','FC Nordsjælland U19')
df.columns = df.columns.str.replace('23729','Midtjylland U19')
df.columns = df.columns.str.replace('25612','AGF U19')
df.columns = df.columns.str.replace('23731','Lyngby U19')
df.columns = df.columns.str.replace('23734','Brøndby IF U19')
#df.columns = df.columns.str.replace('general.','')
#possession_cols = [col for col in df.columns if col.startswith('possession')]
#df.columns = df.columns.where(~df.columns.str.startswith('possession.'), df.columns.str.replace('possession.', ''))
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
#dfegnekampe = dfegnekampe[dfegnekampe['label'].str.contains('Horsens')]
dfegnekampe.to_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Teamsheet alle kampe U19.csv',index=False)

from azure.storage.fileshare import ShareServiceClient
import json
import pandas as pd
from pandas import json_normalize
import numpy as np
import os
import streamlit as st
connection_string = 'SharedAccessSignature=sv=2020-08-04&ss=f&srt=sco&sp=rl&se=2025-01-11T22:47:25Z&st=2022-01-11T14:47:25Z&spr=https&sig=CXdXPlHz%2FhW0IRugFTfCrB7osNQVZJ%2BHjNR1EM2s6RU%3D;FileEndpoint=https://divforeningendataout1.file.core.windows.net/;'
share_name = 'divisionsforeningen-outgoingdata'
dir_path = 'KampData/Sæson 22-23/U19 Ligaen/'


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
df.columns = df.columns.str.replace('38324','Horsens U19')
df.columns = df.columns.str.replace('23735','Esbjerg U19')
df.columns = df.columns.str.replace('23732','København U19')
df.columns = df.columns.str.replace('23736','Silkeborg U19')
df.columns = df.columns.str.replace('23738','SønderjyskE U19')
df.columns = df.columns.str.replace('23730','AAB U19')
df.columns = df.columns.str.replace('23726','OB U19')
df.columns = df.columns.str.replace('23733','Vejle U19')
df.columns = df.columns.str.replace('23737','Randers U19')
df.columns = df.columns.str.replace('23727','FC Nordsjælland U19')
df.columns = df.columns.str.replace('23729','Midtjylland U19')
df.columns = df.columns.str.replace('25612','AGF U19')
df.columns = df.columns.str.replace('23731','Lyngby U19')
df.columns = df.columns.str.replace('23734','Brøndby IF U19')
#df.columns = df.columns.str.replace('general.','')
#possession_cols = [col for col in df.columns if col.startswith('possession')]
#df.columns = df.columns.where(~df.columns.str.startswith('possession.'), df.columns.str.replace('possession.', ''))
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
dfegnekampe.to_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Teamsheet egne kampe U19.csv',index=False)
