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

import pandas as pd
import streamlit as st
import seaborn as sns
import os
import glob
import matplotlib.pyplot as plt
import openpyxl as xlsxwriter
from pandas import DataFrame
os.chdir(r'C:\Users\SéamusPeareBartholdy\OneDrive - AC Horsens A S\Akademi\Excel Organisering og indhold af træning framework\GPS udtræk')
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
df = pd.DataFrame(combined_csv)
df = df.dropna()
print ('GPS csv filer kombineret')
df2 = pd.read_excel(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\GPS spillere.xlsx')
dforiginal = df.merge(df2)
os.chdir(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens')
dforiginal.to_excel(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\samlet gps data.xlsx', index=False)
dforiginal = pd.read_excel(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\samlet gps data.xlsx')
writer = pd.ExcelWriter(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\samlet gps data.xlsx', engine='xlsxwriter')
dforiginal.to_excel(writer,sheet_name='Sheet1', index=None, header=True)


workbook  = writer.book
worksheet = writer.sheets['Sheet1']

formatdict = {'num_format':'dd-mm-yyyy'}
fmt = workbook.add_format(formatdict)
worksheet.set_column('A:A', None, fmt)

formatdict = {'num_format':'hh:mm:ss'}
fmt = workbook.add_format(formatdict)
worksheet.set_column('F:G', None, fmt)

writer.close()
dforiginal = pd.read_excel(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\samlet gps data.xlsx',decimal=',')
Ugenummer = dforiginal['Date'].apply(lambda x: x.isocalendar()[1])
dforiginal.insert(loc = 48, column = 'Ugenummer', value= Ugenummer)
dforiginal.to_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\samlet gps data.csv', index=False)
os.remove(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\samlet gps data.xlsx')
print('GPS færdig')