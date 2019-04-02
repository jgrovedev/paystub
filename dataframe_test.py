import dash
import dash_core_components as dcc 
import dash_html_components as html 
import plotly.plotly as py
import plotly.graph_objs as go
import sqlite3
import pandas as pd
import datetime
from functools import reduce

conn = sqlite3.connect('paychecks.db')

df_ct = pd.read_sql('SELECT * FROM CheckTotal',conn)
df_earn = pd.read_sql('SELECT * FROM Earnings', conn)
df_whold = pd.read_sql('SELECT * FROM Withholdings', conn)


data_frames = [df_ct, df_earn, df_whold]
df_paystub = reduce(lambda  left,right: pd.merge(left,right,on=['Date'], how='outer'), data_frames)

# CREATES A YEAR, MONTH, DAY, COLUMN, AND GROUPS BY MONTH AND SUMS COLUMNS
def monthly_sums(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.strftime('%Y')
    df['Month'] = df['Date'].dt.strftime('%B')
    df['Day'] = df['Date'].dt.strftime('%d')
    df = df.groupby(['Month']).sum()
    df = df.reset_index()
    return print(df)

df_monthly = monthly_sums(df_paystub)

print(df_monthly)