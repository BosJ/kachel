import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id = 'graph-with-slider'),
    html.Button('update', id = 'button')
])

@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('button', 'n_clicks')])
def update_figure(n_clicks):

    df = pd.read_csv('/home/jaco/log.txt')
    ys = list(df.columns.values)

    traces = []
    for i in ys[1:]:
        traces.append(go.Line(
            x = df.date,
            y = df[i],
            text = df[i],
            name = i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis = {'type': 'date'},
            margin = {'l': 80, 'b': 20, 't': 50, 'r': 80},
            legend = {'x': 0, 'y': 1},
            hovermode = 'closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug = True)
