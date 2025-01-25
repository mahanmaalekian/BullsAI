# for graphs
from dash import Dash, dcc, html, Input, Output, register_page, callback
import plotly.express as px
import pandas as pd

# Load sample stock data
df = pd.read_csv(r'data\trade_data_A_period_1.csv')
sampled_df = df.sample(n=100, random_state=42)
sampled_df = sampled_df.sort_values(by='timestamp')
sampled_df["timestamp"] = pd.to_datetime(sampled_df["timestamp"])
#print(sampled_df)
df = pd.read_csv("data/hourly_stock_data.csv")

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
        dcc.RadioItems(options=["price", "volume"], value='price', id='feature'),

        html.P("Select Start Time Period:"),
        dcc.Dropdown(
            id="time-period",
            options=[
                {"label": "5 Seconds", "value": "5S"},
                {"label": "30 Seconds", "value": "30S"},
                {"label": "1 Minute", "value": "1M"},
                {"label": "3 Minutes", "value": "3M"},
                {"label": "6 Minutes", "value": "6M"},
                {"label": "10 Minutes", "value": "10M"},
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

def period_to_time(period)-> int:
    if period == "5S":
        return pd.Timedelta(seconds=5)
    elif period == "30S":
        return pd.Timedelta(seconds=30)
    elif period == "1M":
        return pd.Timedelta(minutes=1)
    elif period == "3M":
        return pd.Timedelta(minutes=3)
    elif period == "6M":
        return pd.Timedelta(minutes=6)
    elif period == "10M":
        return pd.Timedelta(minutes=10)
    else:
        raise ValueError(f"Invalid period: {period}")
    

def filter_data_by_period_start(df, period):
    """Filters the data based on the selected time period."""
    end_date = df["timestamp"].max()
    print("end date", end_date)
    start_date = end_date - period_to_time(period)

    return df[df["timestamp"] >= start_date - pd.Timedelta(seconds=30) ]


@callback(
    Output("time-series-chart", "figure"),
    [Input("feature", "value"), Input("time-period", "value")],
)
def update_time_series(feature, period):
    filtered_df = filter_data_by_period_start(sampled_df, period)
    if filtered_df.empty:
        print(f"Filtered dataframe is empty for period: {period}")
        return px.line(title="No data available for the selected period")

    current_date = filtered_df["timestamp"].max()
    time_delta = period_to_time(period)
    print(f"Updating figure with {len(filtered_df)} points")

    fig = px.line(filtered_df, x="timestamp", y=feature, title=f"{feature} Stock Price")
    fig.update_layout(
        xaxis=dict(
            range=[current_date - time_delta, current_date],
            title="Timestamp"
        ),
        yaxis=dict(title=feature.capitalize()),
        template="plotly_white"
    )
    return fig

