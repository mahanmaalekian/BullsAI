# for graphs
from dash import Dash, dcc, html, Input, Output, register_page, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Load sample stock data
df = pd.read_csv(r'data\trade_data_A_period_1.csv')
#sampled_df = df.sample(n=100, random_state=42)
sampled_df = df.sort_values(by='timestamp')
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
            id="stock-dropdown",
            className="dropdown",
            options=[{"label": stock, "value": stock} for stock in ["AAPL", "GOOG", "MCSFT"]],
            value="AAPL",
            clearable=False,
        ),]),
        html.H4("Stock Price Analysis"),
        html.Div(id="time-periods", children=[
            html.Div([html.P("Past"), 
            dcc.RadioItems(options=["5S", "30S", "1M", "3M", "6M", "10M"], value='1M', id='time-period-past', inline=True),
                      ]),
            html.Div([html.P("Future"),
            dcc.RadioItems(options=["5S", "30S", "1M", "3M", "6M", "10M"], value='1M', id='time-period-future', inline=True),
        ]),]),
        dcc.Graph(id="time-series-chart"),
        html.H4("Volume Analysis"),
        dcc.Graph(id="volume-chart"),

    ]),


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

    return df[df["timestamp"] >= start_date - pd.Timedelta(seconds=5) ]


@callback(
    Output("time-series-chart", "figure"),
    [Input("time-period-past", "value")],
)
def update_time_series(period):
    filtered_df = filter_data_by_period_start(sampled_df, period)
    if filtered_df.empty:
        print(f"Filtered dataframe is empty for period: {period}")
        return px.line(title="No data available for the selected period")

    current_date = filtered_df["timestamp"].max()
    time_delta = period_to_time(period)
    print(f"Updating figure with {len(filtered_df)} points")

    fig = px.line(filtered_df, x="timestamp", y="price", title=f"Stock Price")
    fig.update_layout(
        xaxis=dict(
            range=[current_date - time_delta, current_date],
            title="Timestamp"
        ),
        yaxis=dict(title="Price"),
        template="plotly_white"
    )
    return fig

@callback(
    Output("volume-chart", "figure"),
    [Input("time-period-past", "value")],
)
def update_volume_chart(period):
    filtered_df = filter_data_by_period_start(sampled_df, period)
    if filtered_df.empty:
        print(f"Filtered dataframe is empty for period: {period}")
        return px.histogram(title="No data available for the selected period")

    current_date = filtered_df["timestamp"].max()
    time_delta = period_to_time(period)
    print(f"Updating figure with {len(filtered_df)} points")

    filtered_df.set_index("timestamp", inplace=True)
    filtered_df["price_change"] = filtered_df["price"].diff()

    aggregated_df = filtered_df.resample(time_delta/50).sum().reset_index()
    aggregated_df["price_change"] = aggregated_df["price"].diff()
    aggregated_df["color"] = aggregated_df["price_change"].diff().apply(lambda x: "green" if x > 0 else "red")


    fig = px.bar(
    aggregated_df,
    x="timestamp",
    y="volume",
    color="color",  # Use the 'color' column for the bar colors
    title="Stock Volume",
    color_discrete_map={"green": "green", "red": "red"}  # Map colors to 'green' and 'red'
    )
    #fig = px.histogram(filtered_df, x="timestamp", y="volume", title=f"Stock Volume")
    fig.update_layout(
        xaxis=dict(
            range=[current_date - time_delta, current_date],
            title="Timestamp"
        ),
        yaxis=dict(title="Volume"),
        template="plotly_white"
    )
    return fig

