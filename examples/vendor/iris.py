
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from sklearn import datasets
from sklearn.cluster import KMeans

import geopandas as gpd

import shapefile
from examples.vendor import nuts_data

fp = r"examples/vendor/datas/NUTS_RG_10M_2016_4326_LEVL_2.shp"  # /home/ahmet/avocado_analytics/



regions = shapefile.Reader(fp).__geo_interface__

df = nuts_data.get_data()
import dash_bootstrap_components as dbc

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


controls = dbc.Card(
    [
        dbc.FormGroup(
            [
                html.Abbr("Select one of the PREK indicator", title="The colors in the map show the value of the indicator" ),
                dcc.Dropdown(
                    id="PREK-filter",
                    options=[{'label': i.title(), 'value': i} for i in df.columns],
                    value="PRG",
                    clearable=False,
                    className="dropdown",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                html.Abbr("Select Context Var(s)", title="select the context var to see the background info" ),
                dcc.Dropdown(
                    id="hov-filter",
                    options=[{'label': i.title(), 'value': i} for i in df.columns],
                    multi=True,
                    value=['GDP', 'RES'],
                    clearable=False,
                    searchable=False,
                    className="dropdown",
                ),
            ]
        ),

    ],
    body=True,
)

app.layout = dbc.Container(
    [
        html.H1("Choropleth map EU regions"),
        html.P(
            "Maps by regions and time series by year"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(dcc.Graph(id='choropleth', clickData={'points': [{'hovertext': 'BE10'}]}), md=8),
            ],
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(md=4),
                dbc.Col(dcc.Slider(
                    id='year-slider',
                    min=df['Year'].min(),
                    max=df['Year'].max(),
                    value=df['Year'].max(),
                    marks={str(year): str(year) for year in df['Year'].unique()},
                    step=None
                ), md=8),

            ],
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='x-time-series'), md=3),
                dbc.Col(dcc.Graph(id='y-time-series'), md=3),
                dbc.Col(dcc.Graph(id='z-time-series'), md=3),
                dbc.Col(dcc.Graph(id='w-time-series'), md=3),

            ],
            align="center",
        ),
    ],
    fluid=True,
)


@app.callback(
    Output('choropleth', 'figure'),
    [Input('PREK-filter', 'value'),
     Input('year-slider', 'value'),
     Input('hov-filter', 'value')])
def update_graph(prek_name, selected_year, indicator_name):
    filtered_df = df[df.Year == selected_year]
    fig = px.choropleth_mapbox(
        filtered_df, geojson=regions, color=prek_name,
        locations="NUTS_ID", featureidkey="properties.NUTS_ID",
        color_continuous_scale="Viridis",
        mapbox_style="open-street-map",
        zoom=3, center={"lat": 51.6, "lon": 15.6},
        opacity=0.5, hover_name='Region_LTN', hover_data=filtered_df[indicator_name])
    fig.update_traces(hovertext=df['NUTS_ID'])
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


@app.callback(

    dash.dependencies.Output('x-time-series', 'figure'),

    [dash.dependencies.Input('choropleth', 'clickData')])
def create_time_series(clickData):
    region_nuts = clickData['points'][0]['hovertext']

    dff = df[df['NUTS_ID'] == region_nuts]

    title = dff['Region_LTN'].unique()[0]

    fig = px.scatter(dff, x='Year', y='PRG')

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',

                       xref='paper', yref='paper', showarrow=False, align='left',

                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)

    fig.update_traces(mode='lines+markers')

    fig.update_xaxes(showgrid=False)

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig


@app.callback(

    dash.dependencies.Output('y-time-series', 'figure'),

    [dash.dependencies.Input('choropleth', 'clickData')])
def create_y_time_series(clickData):
    region_nuts = clickData['points'][0]['hovertext']

    dff = df[df['NUTS_ID'] == region_nuts]

    fig = px.scatter(dff, x='Year', y='RES')

    fig.update_traces(mode='lines+markers')

    fig.update_xaxes(showgrid=False)

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig


@app.callback(

    dash.dependencies.Output('z-time-series', 'figure'),

    [dash.dependencies.Input('choropleth', 'clickData')])
def create_z_time_series(clickData):
    region_nuts = clickData['points'][0]['hovertext']

    dff = df[df['NUTS_ID'] == region_nuts]

    fig = px.scatter(dff, x='Year', y='INT')

    fig.update_traces(mode='lines+markers')

    fig.update_xaxes(showgrid=False)

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig


@app.callback(

    dash.dependencies.Output('w-time-series', 'figure'),

    [dash.dependencies.Input('choropleth', 'clickData')])
def create_w_time_series(clickData):
    region_nuts = clickData['points'][0]['hovertext']

    dff = df[df['NUTS_ID'] == region_nuts]

    fig = px.scatter(dff, x='Year', y='KNW')

    fig.update_traces(mode='lines+markers')

    fig.update_xaxes(showgrid=False)

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig



if __name__ == "__main__":
    app.run_server(debug=True, port=8888)
