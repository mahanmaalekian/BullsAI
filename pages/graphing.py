# for graphs
from dash import Dash, dcc, html, Input, Output, register_page, callback
import plotly.express as px
import pandas as pd

# Load sample stock data
foo = px.data.stocks()
print(foo)
df = pd.read_csv("data/hourly_stock_data.csv")
print(df)
# Convert the 'date' column to datetime format for easier filtering
df["date"] = pd.to_datetime(df["date"])

register_page(__name__, path="/graphing")
layout = html.Div(
    [
        html.Div(className="header", children=[
        html.A(href="/", children=[
            html.Img(src="/assets/logo.png"),
        ]),
        dcc.Dropdown(
            id="ticker",
            className="dropdown",
            options=[{"label": stock, "value": stock} for stock in ["AAPL", "GOOG", "MCSFT"]],
            value="AAPL",
            clearable=False,
        ),]),
        html.H4("Stock Price Analysis"),
        html.P("Select Stock:"),
        dcc.RadioItems(options=["AAPL", "GOOG", "MFT"], value='AAPL', id='ticker'),

        html.P("Select Start Time Period:"),
        dcc.Dropdown(
            id="time-period",
            options=[
                {"label": "1 Day", "value": "1D"},
                {"label": "5 Days", "value": "5D"},
                {"label": "1 Month", "value": "1M"},
                {"label": "3 Months", "value": "3M"},
                {"label": "6 Months", "value": "6M"},
                {"label": "1 Year", "value": "1Y"},
            ],
            value="1M",
            clearable=False,
        ),
        dcc.Graph(id="time-series-chart"),

    ]
)

def filter_data_by_period_end(df, period):
    """Filters the data based on the selected time period."""
    start_date = df["date"].min()
    if period == "1D":
        end_date = start_date + pd.Timedelta(days=1)
    else:
        end_date = start_date + pd.Timedelta(days=1)
    return df[(df["date"] >= start_date) & (df["date"] <= end_date)]


def filter_data_by_period_start(df, period):
    """Filters the data based on the selected time period."""
    end_date = df["date"].max()
    if period == "1D":
        start_date = end_date - pd.Timedelta(days=1)
    elif period == "5D":
        start_date = end_date - pd.Timedelta(days=5)
    elif period == "1M":
        start_date = end_date - pd.DateOffset(months=1)
    elif period == "3M":
        start_date = end_date - pd.DateOffset(months=3)
    elif period == "6M":
        start_date = end_date - pd.DateOffset(months=6)
    elif period == "1Y":
        start_date = end_date - pd.DateOffset(years=1)
    else:
        start_date = df["date"].min()  # Default to full data if invalid input
    return df[df["date"] >= start_date]


@callback(
    Output("time-series-chart", "figure"),
    [Input("ticker", "value"), Input("time-period", "value")],
)
def update_time_series(ticker, period):
    filtered_df = filter_data_by_period_start(df, period)
    filtered_df2 = filter_data_by_period_end(df, period)
    fig = px.line(filtered_df, x="date", y=ticker, title=f"{ticker} Stock Price")
    #fig.add_scatter(x=filtered_df2["date"], y=filtered_df2[ticker], mode='lines', name='end')
    return fig