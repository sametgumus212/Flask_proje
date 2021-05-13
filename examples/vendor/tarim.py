
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Gunler": ["1", "2", "3", "4", "5", "6","7","8", "1","2", "3","4", "5","6", "7","8"],
    "Buyume": [36, 37.5,  39,  40.5,42.4,44.7,45,47,28,28,28.5,29.4,30,34.6,37,38],
    "Bitkiler": ["Buğday","Buğday","Buğday","Buğday","Buğday","Buğday","Buğday","Buğday", "Arpa", "Arpa", "Arpa", "Arpa", "Arpa", "Arpa", "Arpa", "Arpa"]
 })

fig = px.bar(df, x="Gunler", y="Buyume", color="Bitkiler", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Buğday - Arpa büyüme oranları'),

    html.Div(children='''
       kolay ve basit bir uygulama 
    '''),

    dcc.Graph(
        id='tarim',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)