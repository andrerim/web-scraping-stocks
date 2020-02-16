import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

import csv
import os
import datetime

from src.scrape_historical_data import scrape_historical_data
from src.user_search_history import search_history
csv.register_dialect('nor', delimiter=';')



def last_modified(path_to_file):
    try:
        last_modified = os.path.getmtime(path_to_file)
        return last_modified
    except OSError:
        # File probably doesnt exist
        return -1


def draw_plot_stock(ticker):
    filename = "../scraped_data/historical_data_" + ticker + ".csv"

    is_file = os.path.isfile(filename)
    if is_file:
        date_time = datetime.datetime.fromtimestamp(int(last_modified(filename)))
        if not date_time.date() == datetime.date.today():
            instr_name = scrape_historical_data(ticker)
    else:
        instr_name = scrape_historical_data(ticker)

    df = pd.read_csv(filename, dialect='nor')

    try:
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(go.Scatter(x=df["Date"].iloc[::-1], y=df["Adj Close**"].iloc[::-1], name="Stock price"),
                      secondary_y=False)

        fig.add_trace(go.Bar(x=df["Date"].iloc[::-1], y=df["Volume"].iloc[::-1], opacity=0.3, name="Volume"),
                      secondary_y=True)

        last_close = float(df["Close*"][0])

        last_open = float(df["Open"][0])
        last_change = ((last_close / last_open) - 1) * 100

        title = ticker.upper() + "<br>Price: " + str(last_close) + ", " + str(last_change.__round__(2)) + "%"
        fig.update_layout(title_text=title)

        fig.update_xaxes(title_text="Date")
        fig.update_yaxes(title_text="Price NOK", secondary_y=False)
        fig.update_yaxes(title_text="Volume NOK", secondary_y=True)

        return fig
    except:
        print("Error")
        return -1


fig = draw_plot_stock("EQNR")



table = search_history(init=True)

# fig.show()

#external_stylesheets = ['./style.css']

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Stock analyser'),

    html.Div(children='''
        A project for learning web scraping and dash.
    '''),

    dcc.Graph(
        id='stock-graph',
        figure=fig,
    ),

    dcc.Input(
        id="ticker",
        type="text",
        value=None,
        placeholder="Ticker, e.g. EQNR, DNB..",
        debounce=True
    ),

    dcc.Graph(
        id='search-history',
        figure=table
    )
])


@app.callback(
    [Output("stock-graph", "figure"),
     Output("search-history", "figure")],
    [Input("ticker", "value")]

)
def load_stock(val):
    if val is not None:
        val = val.upper()
        fig = draw_plot_stock(val)
        if not fig == -1:
            return fig, search_history(val)
    return draw_plot_stock("EQNR"), search_history("EQNR")


if __name__ == '__main__':
    app.run_server(debug=True)
