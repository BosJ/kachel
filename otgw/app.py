import dash                                                                                                                        
import dash_core_components as dcc                                                                                                 
import dash_html_components as html                                                                                                
from dash.dependencies import Input, Output                                                                                        
import pandas as pd                                                                                                                
import plotly.graph_objs as go                                                                                                     
import datetime                                                                                                                    
                                                                                                                                   
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']                                                              
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)                                                               
                                                                                                                                   
''' Retreive- and Preprocess Data '''                                                                                                                                                                                                                                
def get_df():                                                                                                                      
    #df = pd.read_csv('https://raw.githubusercontent.com/BosJ/kachel/master/otgw/log.txt')                                         
    df = pd.read_csv('/home/jaco/log.txt')               
    #df = pd.read_csv('/home/pi/otgw/log.txt')
               
    df['date2'] = pd.to_datetime(df.date)
    df.date = pd.to_datetime(df.date)
    df[' CH mode'] = df[' CH mode'].replace([' 1'], '100')                   
    df[' DHW mode'] = df[' DHW mode'].replace([' 1'], '100')
    df[' Flame status'] = df[' Flame status'].replace([' 1'], '100')
    return df    

def get_dff():
    dff = get_df()
    dff['date_idx'] = dff.date
    dff = dff.set_index('date_idx')
    dff = dff.groupby(dff.index.date).sum()
    dff['date'] = get_df().date
    return dff

df = get_df()                        
ys = list(df.columns.values)         
                                   
''' App Layout '''                    
                        
app.layout = html.Div([

    dcc.Graph(id = 'bar'),

    dcc.Graph(id = 'graph-with-slider'),
                           
    dcc.DatePickerRange(             
        id = 'my-date-picker-range', 
        min_date_allowed = get_df().iloc[0].date2.date(),
        max_date_allowed = get_df().iloc[-1].date2.date() + datetime.timedelta(days = 2),
        start_date = get_df().iloc[-1].date2.date(),
        end_date = get_df().iloc[-1].date2.date() + datetime.timedelta(days = 1),
        style = { "margin-left": 60 },
    ),        
    html.Div(id='output-container-date-picker-range'),
            
    dcc.Dropdown(      
        id = 'opt-dropdown',
        multi = True,                
        value = ys[2:3],                                  
        style = { "margin-left": 30,  
                  "margin-top": 10,
                  "width": 285 },
    ),
 dcc.Dropdown(         
        id = 'opt-dropdown_highlight',
        placeholder = "Highlight",
        multi = True,
        style = { "margin-left": 30,
                  "margin-top": 10,
                  "width": 285 },
    ),
])

''' Build Plot Callback '''

@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('opt-dropdown', 'value'),
     Input('opt-dropdown_highlight', 'value'),
     Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')])

def update_figure(value, highlight, start_date, end_date):

    traces = []
    df = get_df()
    selected_df = df[ (df['date2'] > start_date) & (df['date2'] < end_date) ]

    if value:
        for i in value:
            traces.append(go.Scatter(
                x = selected_df.date,
                y = selected_df[i],
                text = selected_df[i],
                name = i
            ))

    if highlight:
        for i in highlight:
            traces.append(go.Scatter(
                x = selected_df.date,
                y = selected_df[i],
                text = selected_df[i],
                fill='toself',
                opacity=0.1,
                name = i
            ))
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis = {'type': 'date'},
            margin = {'l': 80, 'b': 50, 't': 50, 'r': 80},
            legend = {'x': 0, 'y': 1},
            hovermode = 'closest'
        )
    }

@app.callback(
    Output('bar', 'figure'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')])

def update_figure(start_date, end_date):

    dff = get_dff()
    traces = []

    traces.append(go.Bar(
        x = dff.index,
        y = dff[' Relative modulation level'],
        text = dff[' Relative modulation level'],

    ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis = {'type': 'date'},
            margin = {'l': 80, 'b': 50, 't': 50, 'r': 80},
            legend = {'x': 0, 'y': 1},
            hovermode = 'closest',
            height = 250,
        )
    }

''' Selection Callback '''

@app.callback(
    Output('opt-dropdown', 'options'),
    [Input('opt-dropdown', 'value')])

def update_date_dropdown( val ):
    return [ {'label': i, 'value': i} for i in ys[1:4] ]

@app.callback(
    Output('opt-dropdown_highlight', 'options'),
    [Input('opt-dropdown_highlight', 'value')])

def update_date_dropdown( val ):
    return [ {'label': i, 'value': i} for i in ys[4:7] ]

if __name__ == '__main__':
    #app.run_server(host='0.0.0.0')
    app.run_server(debug=True)
