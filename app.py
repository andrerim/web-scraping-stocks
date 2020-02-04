import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import csv

csv.register_dialect('nor', delimiter=';')

df = pd.read_csv("../scraped_data/historical_dataEQNR.csv", dialect='nor')
print(df.head())


fig = go.Figure(data=[go.Scatter(x=df["Date"], y=df["Adj Close**"], name="awd")])
#fig.add_trace(go.Figure(data=[go.Scatter(x=df["Date"], y=df["Volume"], name="awd")]))
#fig.show()
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Stock analyser'),

    html.Div(children='''
        A project for learning web scraping and dash.
    '''),

    dcc.Graph(
    id='stock-graph',
        figure=fig,
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)