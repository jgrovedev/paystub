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

# CONNNECTS AND READS SQL FILES 
conn = sqlite3.connect('paychecks.db')

df_ct = pd.read_sql('SELECT * FROM CheckTotal',conn)
df_earn = pd.read_sql('SELECT * FROM Earnings', conn)
df_whold = pd.read_sql('SELECT * FROM Withholdings', conn)

# MERGES DATA FRAMES AND FORMATS DATE
data_frames = [df_ct, df_earn, df_whold]
df_paystub = reduce(lambda  left,right: pd.merge(left,right,on=['Date'], 
                                                how='outer'), data_frames)

df_paystub['Date'] = pd.to_datetime(df_paystub['Date'], format='%Y-%m-%d')

# START OF DASH APP
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
    
    # GRAPH VIEW AND DATE PICKER SELECTION
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
        ], className = 'twelve columns'),
    ], style = {'margin-bottom' : 30}, className  = 'row'),
    
    # EARNINGS CHART AND TEXT DATA
    html.Div([
        html.Div([
            html.Div([
                html.H3(children='Earnings', style={
                        'textAlign': 'center',
                    }),
                dcc.Graph(
                        id='pay',
                )
            ], style = {'margin-bottom' : 30}),
                html.Div([
                    html.Div('Number of Stubs', style={'margin-bottom:' : 50}),
                    html.Div( id='num-stub',
                            children='',
                            style={'fontSize' : 24,
                                'margin-top' :10,
                                'margin-bottom' :10,
                            },
                    ),
                ], className='three columns'),        
                html.Div([
                    html.Div('Total Take Home Pay', style={'margin-bottom:' : 50}),
                    html.Div( id='total-pay',
                            children='',
                            style={'fontSize' : 24,
                                'margin-top' :10,
                                'margin-bottom' :10,
                            },
                    ),
                ], className='three columns'),            
                html.Div([    
                    html.Div('Average Take Home Pay', style={'margin-bottom:' : 50}),
                    html.Div( id='avg-pay',
                            children='',
                            style={'fontSize' : 24,
                                'margin-top' :10,
                                'margin-bottom' :10,
                            },
                    ),
                ], className='three columns'),       
                html.Div([    
                    html.Div('Largest Stub', style={'margin-bottom:' : 50}),
                    html.Div( id='lg-stub',
                            children='',
                            style={'fontSize' : 24,
                                'margin-top' :10,
                                'margin-bottom' :10,
                            },
                    ),
                ], className='three columns'),       
                html.Div([    
                    html.Div('Smallest Stub', style={'margin-bottom:' : 50}),
                    html.Div( id='sm-stub',
                            children='',
                            style={'fontSize' : 24,
                                'margin-top' :10,
                                'margin-bottom' :10,
                            },
                    ),
                ], className='three columns'), 
        ], style={'textAlign' : 'center', 'margin-bottom' : 20}, className='six columns'),
        
        # HOURS CHART AND TEXT DATA
        html.Div([    
            html.Div([
                html.H3(children='Hours', style={
                        'textAlign': 'center',
                    }),
                dcc.Graph(
                    id='hours',
                ),
            ], style = {'margin-bottom' : 30}),    
                html.Div([    
                    html.Div('Regular Hours', style={'margin-bottom:' : 50}),
                    html.Div( id='hr-reg',
                            children='',
                            style={'fontSize' : 24,
                                'margin-top' :10,
                                'margin-bottom' :10,
                            },
                    ),
                ], className='three columns'),        
                html.Div([    
                    html.Div('Overtime Hours', style={'margin-bottom:' : 50}),
                    html.Div( id='hr-ot',
                            children='',
                            style={'fontSize' : 24,
                                'margin-top' :10,
                                'margin-bottom' :10,
                            },
                    ),
                ], className='three columns'),
                html.Div([    
                    html.Div('Total Hours', style={'margin-bottom:' : 50}),
                    html.Div( id='hr-total',
                            children='',
                            style={'fontSize' : 24,
                                'margin-top' :10,
                                'margin-bottom' :10,
                            },
                    ),
                ], className='three columns'),
                html.Div([    
                    html.Div('Average Hours', style={'margin-bottom:' : 50}),
                    html.Div( id='hr-avg',
                            children='',
                            style={'fontSize' : 24,
                                'margin-top' :10,
                                'margin-bottom' :10,
                            },
                    ),
                ], className='three columns'),
                html.Div([    
                    html.Div('Max Hours', style={'margin-bottom:' : 50}),
                    html.Div( id='hr-max',
                            children='',
                            style={'fontSize' : 24,
                                'margin-top' :10,
                                'margin-bottom' :10,
                            },
                    ),
                ], className='three columns'),
                html.Div([    
                    html.Div('Minimum Hours', style={'margin-bottom:' : 50}),
                    html.Div( id='hr-min',
                            children='',
                            style={'fontSize' : 24,
                                'margin-top' :10,
                                'margin-bottom' :10,
                            },
                    ),
                ], className='three columns'),    
            ], style = {'textAlign' : 'center'}, className='six columns')        
    ], className='row'),

    # WITHHOLDINGS CAHRT
    html.Div([
        html.Div([
            html.H3(children='Withholdings', style={
                    'textAlign' : 'center',
                }),
        ], className='six columns'),
    ], className = 'row'),
    html.Div([
        html.Div([
            html.Div([
                dcc.RadioItems(
                            id = 'earn-view',
                            options = [
                                {'label': 'With Earnings', 'value' : 'earning'},
                                {'label': 'Without Earnings', 'value' : 'no-earning'},
                            ],
                            value = 'no-earning',
                            labelStyle = {'display' : 'inline-block'}
                        ),
            ], className = 'two columns'),
        ], className = 'row'),    
            html.Div([
                dcc.Graph(
                    id='witholdings',
                )
            ], className ='six columns'),
    ], style = {'textAlign' : 'center'}, className = 'row')        
], className ='ten columns offset-by-one')

# CHART AND TEXT DATA CALLBACKS
@app.callback(
    [Output('pay', 'figure'),
    Output('hours', 'figure'),
    Output('witholdings', 'figure')],
    [Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    Input('data-view', 'value'),
    Input('earn-view', 'value')]
    )
def dataview_chart(start_date, end_date, value, value2):
    df = df_paystub
    df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    df_monthly = df.groupby(pd.Grouper(key='Date', freq='M')).sum().reset_index()
    df = df if value == 'Weekly' else df_monthly
    
    # EARNINGS BAR CHART
    earnchart={
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
                          tickformat = '%d %B<br>%Y',                      
            )
        )
    }
    
    # HOURS LINE CHART
    hrchart={
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
        ],
        'layout': go.Layout(
                    title = 'Regular Hours vs  Overtime Hours',
                    yaxis = dict(title = 'Hours'),
                    xaxis =  dict(title = 'Date',
                                tickformat = '%d %B<br>%Y',                      
                    )
                )
    }
    
    # WITHHOLDINGS PIE CHART
    dfw = df_whold
    dfw = dfw[(dfw['Date'] >= start_date) & (dfw['Date'] <= end_date)]
    dfw_earn = [df['EarnTotal'].sum(), dfw['Social_Security'].sum(), dfw['Medicare'].sum(),
                dfw['FedTax'].sum(), dfw['PA_unemployment'].sum(),
                dfw['PATax'].sum(), dfw['YCity_LYOY2'].sum(),
                dfw['YCity_YRKCY'].sum()
                ]
    label_earn = ['Earnings','Social Security', 'Medicare', 'Federal', 'Unemployment', 
                'PA Tax', 'York City Tax (LYOY2)', 'York City Tax (YRKCY)'
                 ]
    dfw_noearn = [dfw['Social_Security'].sum(), dfw['Medicare'].sum(),
                  dfw['FedTax'].sum(), dfw['PA_unemployment'].sum(),
                  dfw['PATax'].sum(), dfw['YCity_LYOY2'].sum(),
                  dfw['YCity_YRKCY'].sum()
                 ]
    label_noearn = ['Social Security', 'Medicare', 'Federal', 'Unemployment', 
                    'PA Tax', 'York City Tax (LYOY2)', 'York City Tax (YRKCY)'
                   ]
    whchart = {
        'data': [
            go.Pie(
                    labels = label_earn if  value2 == 'earning' else label_noearn,
                    values = dfw_earn if value2 == 'earning' else dfw_noearn
            )
        ],
        'layout': go.Layout(
            title = 'Taxes',
        )
    }
    return (earnchart, hrchart, whchart)

# TEXT DATA CALLBACK
@app.callback(
    [Output('total-pay', 'children'),
    Output('avg-pay', 'children'),
    Output('num-stub', 'children'),
    Output('lg-stub', 'children'),
    Output('sm-stub', 'children'),
    Output('hr-reg', 'children'),
    Output('hr-ot', 'children'),
    Output('hr-total', 'children'),
    Output('hr-avg', 'children'),
    Output('hr-max', 'children'),
    Output('hr-min', 'children')],
    [Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')],
)
def dataview_text(start_date, end_date):
    df = df_paystub
    df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    totalpay = str(round(df['CheckTotal'].sum(), 2))
    avgpay = str(round(df['CheckTotal'].mean(), 2))
    numstub = str(len(df['Date']))
    lgstub = str(max(df['CheckTotal']))
    smstub = str(min(df['CheckTotal']))
    hrreg = str(df['RegHours'].sum())
    hrot = str(round(df['OtHours'].sum(), 2))
    hrtotal = str(round(df['TotalHours'].sum(), 2))
    hravg = str(round(df['TotalHours'].mean(), 2))
    hrmax = str(round(max(df['TotalHours']), 2))
    hrmin = str(round(min(df['TotalHours']), 2)) 
    return (totalpay, avgpay, numstub, lgstub,
            smstub, hrreg, hrot, hrtotal, hravg,
            hrmax, hrmin
    )

# RUNS SERVER
if __name__ == "__main__":
    app.run_server(debug=True)