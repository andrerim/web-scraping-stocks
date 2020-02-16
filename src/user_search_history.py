

import pandas as pd
import plotly.graph_objs as go



history_vals = {
    "ticker": [],
    "last": [],
    "change%": []
}

#draw search history table
def search_history(ticker=None, last_change=None, init=False):
    if init:
        return go.Figure(data=[go.Table(header=dict(values=['Ticker', 'Last', 'Change%']),
                                     cells=dict(values=[['-'], ['-'], ['-']]))
                            ])


    filename = "../scraped_data/historical_data_" + ticker + ".csv"
    df = pd.read_csv(filename, dialect='nor')
    history_vals["ticker"].insert(0, ticker)
    history_vals["last"].insert(0, df["Adj Close**"][0])

    last_close = float(df["Close*"][0])
    last_open = float(df["Open"][0])

    last_change = ((last_close / last_open) - 1) * 100


    history_vals["change%"].insert(0, last_change.__round__(2))

    fig = go.Figure(data=[go.Table(header=dict(values=['Ticker', 'Last', 'Change% 1D']),
                                     cells=dict(values=[history_vals["ticker"], history_vals["last"], history_vals["change%"]]))
                            ])
    return fig
