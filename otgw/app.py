# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from datetime import datetime as dt

app = dash.Dash('Hello World')

data = pd.read_csv('https://raw.githubusercontent.com/BosJ/kachel/master/otgw/log.txt')

ys = list(data.columns.values)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': data['date'], 'y': data[ys[1]], 'type': 'line', 'name': ys[1]},
                {'x': data['date'], 'y': data[ys[2]], 'type': 'line', 'name': ys[2]},
                {'x': data['date'], 'y': data[ys[3]], 'type': 'line', 'name': ys[3]},
                {'x': data['date'], 'y': data[ys[4]], 'type': 'line', 'name': ys[4]},
                {'x': data['date'], 'y': data[ys[5]], 'type': 'line', 'name': ys[5]},
                {'x': data['date'], 'y': data[ys[6]], 'type': 'line', 'name': ys[6]},
                {'x': data['date'], 'y': data[ys[7]], 'type': 'line', 'name': ys[7]},
            ],
            'layout': {
                'title': 'Lekkuh waam?', 'height': 525
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0')
