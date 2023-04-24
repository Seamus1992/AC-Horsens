import gspread
import pandas as pd
import streamlit as st
import numpy as np

gc = gspread.service_account()
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1haWEtNQdhthKaSQjb2BRHlq2FLexicUOAHbjNFRAUAk/edit#gid=1984878556')
ws = sh.worksheet('Samlet')
df = pd.DataFrame(ws.get_all_records())
df.to_csv('ny wellness.csv',index=False)
print('Wellness data hentet')
