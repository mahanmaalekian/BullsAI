from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load sample stock data
df = px.data.stocks()
df.head()


# Convert the 'date' column to datetime format for easier filtering
df["date"] = pd.to_datetime(df["date"])

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H4("Stock Price Analysis"),
        dcc.Graph(id="time-series-chart"),
        html.P("Select Stock:"),
        dcc.Dropdown(
            id="ticker",
            options=[{"label": stock, "value": stock} for stock in ["AMZN", "FB", "NFLX"]],
            value="AMZN",
            clearable=False,
        ),
        html.P("Select Time Period:"),
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
    ]
)


def filter_data_by_period(df, period):
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


@app.callback(
    Output("time-series-chart", "figure"),
    [Input("ticker", "value"), Input("time-period", "value")],
)
def update_time_series(ticker, period):
    filtered_df = filter_data_by_period(df, period)
    fig = px.line(filtered_df, x="date", y=ticker, title=f"{ticker} Stock Price")
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
