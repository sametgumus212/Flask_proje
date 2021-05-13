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


dc=pd.read_csv('examples/vendor/datas/eudc-app-2.csv')
dc['country'].fillna('none', inplace=True)
dc.country=dc.country.astype('category')

dfx = dc.groupby(['country', 'reg']).mean().reset_index()

cat_opt =dc.loc[:, ['AgeCategories','cohort','Education', 'Urban_Rural', 'sex']]

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        html.H1("National distributions"),
        html.P(
            "Click on a tab to see the patterns about regions in a country "),
        html.Hr(),
        dbc.Tabs(
            [
                dbc.Tab(label="Bar Chart", tab_id="bar"),
                dbc.Tab(label="Box Plot", tab_id="box"),
                dbc.Tab(label="Parallel Categories", tab_id="parcat"),
            ],
            id="tabs",
            active_tab="bar",
        ),
        html.Div(id="tab-content", className="p-4"),
        dbc.Row(
            [
                dbc.Col(dcc.Dropdown(
                    id='x-filter',
                    options=[{'label': i.title(), 'value': i} for i in dc.columns],
                    value='att7'), md=3),
                dbc.Col(dcc.Dropdown(
                    id='y-filter',
                    options=[{'label': i.title(), 'value': i} for i in dc.columns],
                    value='att9'), md=3),
                dbc.Col(dcc.Dropdown(
                    id='cat1-filter',
                    options=[{'label': i.title(), 'value': i} for i in cat_opt],
                    value='Education'), md=3),
                dbc.Col(dcc.Dropdown(
                    id='reg-filter',
                    options=[{'label': i.title(), 'value': i} for i in dc['country'].unique()],
                    value="TURKEY"), md=3),

            ],
            align="center",
        ),
    ],
    fluid=True,
)


@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"), Input("x-filter", "value"), Input("y-filter", "value"),
     Input("cat1-filter", "value"), Input("reg-filter", "value")],
)
def render_tab_content(active_tab, xin, yin, cat1, reg):
    dff = dc[dc['country'] == reg]
    if active_tab == "bar":
        ct = pd.crosstab(dff['reg'], dff.loc[:, xin], dropna=True, normalize='columns')
        df_cross = ct.stack().reset_index()
        fig1 = px.bar(df_cross, x="reg", y=0, color=xin)
        ct = pd.crosstab(dff['reg'], dff.loc[:, yin], dropna=True, normalize='columns')
        df_cross = ct.stack().reset_index()
        fig2 = px.bar(df_cross, x="reg", y=0, color=yin)
        return dbc.Row([
            dbc.Col(dcc.Graph(figure=fig1)),
            dbc.Col(dcc.Graph(figure=fig2)),
        ])
    elif active_tab == "parcat":
        fig3 = px.parallel_categories(dff, dimensions=['sex', 'AgeCategories', 'Education'],
                                      color=xin)
        fig4 = px.parallel_categories(dff, dimensions=['sex', 'AgeCategories', 'Education'],
                                      color=yin)
        return dbc.Row([
            dbc.Col(dcc.Graph(figure=fig3)),
            dbc.Col(dcc.Graph(figure=fig4)),
        ])
    elif active_tab == "box":
        fig5 = px.box(dff, x=cat1, y=xin, color='sex')
        fig6 = px.box(dff, x=cat1, y=yin, color='sex')
        return dbc.Row([
            dbc.Col(dcc.Graph(figure=fig5)),
            dbc.Col(dcc.Graph(figure=fig6)),
        ])

if __name__ == "__main__":
    app.run_server(debug=True, port=8888)

