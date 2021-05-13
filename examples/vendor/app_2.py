# -*- coding: utf-8 -*-

import pyreadstat
import pandas as pd
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import plotly.express as px
import time

dc=pd.read_csv('examples/vendor/datas/eudc-app-2.csv')

#dfx=dc.groupby(['reg', 'country', 'Education']).mean().reset_index()

dfx=dc.groupby(['reg', 'country', 'Education']).mean().reset_index()
dfx['P']=pd.qcut(dfx['P'], q=5).astype('category')
dfx['R']=pd.qcut(dfx['R'], q=5).astype('category')
dfx['K']=pd.qcut(dfx['K'], q=5).astype('category')
dfx['E']=pd.qcut(dfx['E'], q=5).astype('category')

def fact_col(x): 
    return pd.factorize(x)[0] + 1

dfx[["P", "R", 'E', 'K']]=dfx[["P", "R", 'E', 'K']].apply(fact_col)

cat_opt =dc.loc[:, ['AgeCategories','cohort','Education', 'Urban_Rural', 'sex']]
prek_opt =dc.loc[:, ['P','R','E', 'K']]


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

controls = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("Select x"),
                dcc.Dropdown(
                    id='x-filter',
                    options=[{'label': i.title(), 'value': i} for i in dfx.columns],
                    value='att7'),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Select y"),
                dcc.Dropdown(
                    id='y-filter',
                    options=[{'label': i.title(), 'value': i} for i in dfx.columns],
                    value='att9')
            ]
        ),
        dbc.FormGroup(
            [
                html.Abbr("Size of the points", title="greater the size of the point, larger the value of the indicator" ),
                dcc.Dropdown(
                    id='size-filter',
                    options=[{'label': i.title(), 'value': i} for i in prek_opt],
                    value='P')
            ]
        ),        
        dbc.FormGroup(
            [
                html.Abbr("Select demographic 1", title="Select a demographic variable for the violin plot"),
                dcc.Dropdown(
                    id='cat1-filter',
                    options=[{'label': i.title(), 'value': i} for i in cat_opt],
                    placeholder="Select a categorical var", ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Select demographic variable 2"),
                dcc.Dropdown(
                    id='cat2-filter',
                    options=[{'label': i.title(), 'value': i} for i in cat_opt],
                    value="Education"),
            ]
        ),
    ],
    body=True,
)
app.layout = dbc.Container(
    [        
        html.H1("Scatterplots for aggregate regions and violin plots for the regions"),
        html.P(
            "Click on a point on the scatter plot to see its distribution"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(dcc.Graph(
                    id='scatter',
                    clickData={'points': [{'hovertext': 'Zürich'}]}
                ), md=8),
            ],
            align="center",
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='x-violin'), md=6),
                dbc.Col(dcc.Graph(id='y-violin'), md=6),
            ],
            align="center",
        ),
    ],
    fluid=True,
)


@app.callback(
    Output('scatter', 'figure'),
    [Input('x-filter', 'value'),
     Input('y-filter', 'value'),
     Input('size-filter', 'value')])
def update_graph(x_i, y_i, siz):
    fig = px.scatter(dfx, x=x_i, y=y_i, hover_name='reg', size=siz, size_max=10,color='country', marginal_x="rug", trendline="ols", marginal_y="rug")
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    return fig


@app.callback(
    Output('x-violin', 'figure'),
    [Input('scatter', 'clickData'), Input('x-filter', 'value'), Input('cat1-filter', 'value'),
     Input('cat2-filter', 'value')])
def create_violin(clickData, x_in, cat1, cat2):
    coun = clickData['points'][0]['hovertext']
    dfc = dc[dc['reg'] == coun]
    fig = px.violin(dfc, y=x_in, x=cat1, color=cat2 , box=True, points="all")
    return fig


@app.callback(
    Output('y-violin', 'figure'),
    [Input('scatter', 'clickData'), Input('y-filter', 'value'), Input('cat1-filter', 'value'),
     Input('cat2-filter', 'value')])
def create_violin(clickData, y_in, cat1, cat2):
    coun = clickData['points'][0]['hovertext']
    dfc = dc[dc['reg'] == coun]
    fig = px.violin(dfc, y=y_in, x=cat1, color=cat2 , box=True, points="all", title=coun)
    return fig


if __name__ == "__main__":
    app.run_server(debug=True, port=8888)

