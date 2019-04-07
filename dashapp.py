import dash
import dash_core_components as dcc 
import dash_html_components as html
from dash.dependencies import Input, Output 
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
df_paystub = reduce(lambda  left,right: pd.merge(left,right,on=['Date'], 
                                                how='outer'), data_frames)

df_paystub['Date'] = pd.to_datetime(df_paystub['Date'], format='%Y-%m-%d')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})

app.layout = html.Div(children=[
    html.H1(children='paystub', className= 'nine columns'),
    html.Img(
                src="https://unitedcoolair.com/wp-content/uploads/UCAlogo_withTagline-white-outline-1.png",
                className='three columns',
                style={
                    'height': '15%',
                    'width': '15%',
                    'float': 'right',
                    'position': 'relative',
                    'margin-top': 20,
                    'margin-right': 20,
                },
            ),
    html.Div([
        html.Div(children='A web application where paystubs are graphed', className= 'twelve columns'),
    ], className='row'),    

    html.Div([
        html.Div([
            dcc.RadioItems(
                        id='data-view',
                        options=[
                            {'label': 'Weekly View', 'value': 'Weekly'},
                            {'label': 'Monthly View', 'value': 'Monthly'},
                        ],
                        value='Weekly',
                        labelStyle={'display': 'inline-block'}
                    ),
        ], className = 'two columns'),
            
        html.Div([
            dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date_placeholder_text="Start Date",
                    end_date_placeholder_text="End Date",
                    start_date=df_paystub['Date'].iloc[0],
                    end_date=df_paystub['Date'].iloc[-1],
                )   
        ], className = 'ten columns'),
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
            )
        ], className='six columns')
    ], className='row'),

    # HTML ROW CREATED IN DASH
    html.Div([
        # HTML COLUMN CREATED IN DASH
        html.Div([
            # PLOTLY PIE CHART
            dcc.Graph(
                id='withholdings-pie',
                figure={
                    'data': [
                        go.Pie(
                            labels = ['A', 'B', 'C', 'D'],
                            values = [4500,2500,1053,500],
                        )
                    ]
                }
            )
        ], className='six columns'),
        # HTML COLUMN CREATED IN DASH
        html.Div([
            # PLOTLY BAR CHART
            dcc.Graph(
                id='withholdings-bar',
                figure={
                    'data':[
                        go.Bar(
                            x = df_whold['FedTax'],
                            y = df_whold['Date'],
                            name = 'Federal Tax',
                            orientation = 'h',
                        ),
                         go.Bar(
                            x = df_whold['Social_Security'],
                            y = df_whold['Date'],
                            name = 'Social Security',
                            orientation = 'h',
                        ),                        
                    ],
                    'layout': go.Layout(
                        xaxis=dict(
                            showgrid=False,
                            showline=False,
                            showticklabels=False,
                            zeroline=False,
                            domain=[0.15, 1]
                        ),
                        yaxis=dict(
                            showgrid=False,
                            showline=False,
                            # showticklables=False,
                            zeroline=False,
                        ),
                        barmode='stack',
                        paper_bgcolor='rgb(248, 248, 255)',
                        plot_bgcolor='rgb(248, 248, 255)',
                        showlegend=False,                       
                    )
                }
            )
        ], className='six columns')
    ], className='row')

], className='ten columns offset-by-one')

# HOURS GRAPH CALLBACK
@app.callback(
    dash.dependencies.Output('pay', 'figure'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
    dash.dependencies.Input('date-picker-range', 'end_date'),
    dash.dependencies.Input('data-view', 'value')]
)
def figupdate(start_date, end_date, value):
    df = df_paystub
    df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    df_monthly = df.groupby(pd.Grouper(key='Date', freq='M')).sum().reset_index()
    df = df if value == 'Weekly' else df_monthly
    figure={
        'data': [
            go.Bar(  
                x = df['Date'],
                y = df['CheckTotal'],
                name = 'Take Home Pay',
            ),
                go.Bar(
                x = df['Date'],
                y = df['EarnTotal'],
                name = 'Earnings',
            )
        ],
        'layout': go.Layout(
            title = 'Take Home Pay vs. Earnings',
            barmode = 'group',
            yaxis = dict(title = 'Pay (U.S. Dollars)'),
            xaxis =  dict(title = 'Date Paid',
                          tickformat = '%d %B (%a)<br>%Y',                      

            )
        )
    }
    return figure

@app.callback(Output('hours', 'figure'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
    dash.dependencies.Input('date-picker-range', 'end_date'),
    dash.dependencies.Input('data-view', 'value')]
)
def dataview_hours(start_date, end_date, value):
    df = df_paystub
    df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    df_monthly = df.groupby(pd.Grouper(key='Date', freq='M')).sum().reset_index()
    df = df if value == 'Weekly' else df_monthly
    figure={
        'data': [
            go.Scatter(
                x = df['Date'],
                y = df['RegHours'],
                mode = 'lines',
                name = 'Regular Hours',
            ),
            go.Scatter(
                x = df['Date'],
                y = df['OtHours'],
                mode = 'lines',
                name = 'Overtime Hours',
            )
        ]
    }
    return figure

if __name__ == "__main__":
    app.run_server(debug=True)