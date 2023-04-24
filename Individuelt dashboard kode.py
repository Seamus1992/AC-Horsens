import pandas as pd
import streamlit as st
df = pd.read_csv(r'C:\Users\SéamusPeareBartholdy\Documents\GitHub\AC-Horsens\Individuelt dashboard test.csv')
st.dataframe(df)
print(df)