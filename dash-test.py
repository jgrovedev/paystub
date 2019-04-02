import dash
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input, Output
import plotly.plotly as py
import plotly.graph_objs as go
import sqlite3
import pandas as pd
from functools import reduce
import datetime

conn = sqlite3.connect('paychecks.db')

df_ct = pd.read_sql('SELECT * FROM CheckTotal',conn)
df_earn = pd.read_sql('SELECT * FROM Earnings', conn)
df_whold = pd.read_sql('SELECT * FROM Withholdings', conn)

data_frames = [df_ct, df_earn, df_whold]
df_paystub = reduce(lambda  left,right: pd.merge(left,right,on=['Date'], how='outer'), data_frames)

def date_extraction(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.strftime('%Y')
    df['Month'] = df['Date'].dt.strftime('%B')
    df['Day'] = df['Date'].dt.strftime('%d')
    return df

date_extraction(df_paystub)

df_monthly = df_paystub.groupby(['Month']).sum().reset_index()


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})

app.layout = html.Div(children=[

    html.Div([
        html.Div([
            dcc.RadioItems(
                        id='data-view',
                        options=[
                            {'label': 'Weekly', 'value': 'Weekly'},
                            {'label': 'Monthly', 'value': 'Monthly'},
                        ],
                        value='Weekly',
                        labelStyle={'display': 'inline-block'}
                    ),
        ], className = 'two columns'),
            
        html.Div([    
            dcc.Dropdown(
                id='year-dropdown',
                options=[
                        {'label': i, 'value': i} for i in df_paystub['Year'].unique()
                ],
                placeholder="Select a year",
            ),
        ], className='five columns'),
            
        html.Div([    
            dcc.Dropdown(
                id='month-dropdown',
                options=[
                  {'label': i, 'value': i} for i in df_paystub['Month'].unique()
                ],
                placeholder="Select a month(s)",
                multi=True,
            ),
        ], className='five columns'),
    ], className  = 'row'),
      

    # HTML ROW CREATED IN DASH
    html.Div([
        # HTML COLUMN CREATED IN DASH
        html.Div([
            # PLOTLY BAR GRAPH        
            dcc.Graph(
                id='pay',
            )
        ], className  = 'six columns'),
 
        # HTML COLUMN CREATED IN DASH
        html.Div([
            # PLOTLY LINE GRAPH
            dcc.Graph(
                id='hours',
                figure={
                    'data': [
                        go.Scatter(
                            x = df_earn['Date'],
                            y = df_earn['RegHours'],
                            mode = 'lines',
                            name = 'Regular Hours',
                        ),
                        go.Scatter(
                            x = df_earn['Date'],
                            y = df_earn['OtHours'],
                            mode = 'lines',
                            name = 'Overtime Hours',
                        )
                    ]
                }
            )
        ], className='six columns')
    ], className='row')
], className='ten columns offset-by-one')

@app.callback(dash.dependencies.Output('pay', 'figure'),
              [dash.dependencies.Input('data-view', 'value')])

def monthly_selector(value):
    if value == 'Monthly':
        figure={
            'data': [
                go.Bar(
                    x = df_monthly['Month'],
                    y = df_monthly['CheckTotal'],
                    name = 'Take Home Pay',
                ),
                    go.Bar(
                    x = df_monthly['Month'],
                    y = df_monthly['EarnTotal'],
                    name = 'Earnings',
                )
            ],
            'layout': go.Layout(
                title = 'Take Home Pay vs. Earnings',
                barmode = 'stack',
                yaxis = dict(title = 'Pay (U.S. Dollars)'),
                xaxis = dict(title = 'Date Paid')
            )
        }
    elif value == 'Weekly':
        figure={
            'data': [
                go.Bar(
                    x = df_paystub['Date'],
                    y = df_paystub['CheckTotal'],
                    name = 'Take Home Pay',
                ),
                    go.Bar(
                    x = df_paystub['Date'],
                    y = df_earn['EarnTotal'],
                    name = 'Earnings',
                )
            ],
            'layout': go.Layout(
                title = 'Take Home Pay vs. Earnings',
                barmode = 'stack',
                yaxis = dict(title = 'Pay (U.S. Dollars)'),
                xaxis = dict(title = 'Date Paid')
            )
        }
    return figure

if __name__ == "__main__":
    app.run_server(debug=True)