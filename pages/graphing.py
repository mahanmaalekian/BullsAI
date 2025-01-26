# for graphs
from pathlib import Path
from dash import Dash, dcc, html, Input, Output, register_page, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Load sample stock data
#df = pd.read_csv(r'data\trade_data_A_period_1.csv')
#sampled_df = df.sample(n=100, random_state=42)
df = None
sampled_df = None
df_predict = None
sampled_df_predict = None
# Convert the 'date' column to datetime format for easier filtering
#df["date"] = pd.to_datetime(df["date"])

register_page(__name__, path="/graphing")
layout = html.Div(
    className="container",
    children=
    [   
        html.Div(id="hidden-div", style={"display": "none"}),  # Invisible element

        html.Div(className="sidebar", children=[
        html.H4("Stock Data"),
        html.P(id="top-price", children="Top Price: $0.00"),
        html.P(id="bottom-price", children="Bottom Price: $0.00"),
        html.P(id="opening-price", children="Opening Price: $0.00"),
        html.P(id="closing-price", children="Closing Price: $0.00"),
        html.P(id="average-price", children="Average Price: $0.00"),
    ]),
        html.Div(
        className="content", children=
        [
        html.A(href="/", children=[
            html.Img(src="/assets/logo.png"),
        ]),
        html.Div(className="header", children=[
 
        dcc.Dropdown(
            id="stock-dropdown",
            className="dropdown",
            options=[{"label": "Company " + stock, "value": stock} for stock in ["A", "B", "C", "D", "E"]],
            value="A",
            clearable=False,
        ),
        dcc.Dropdown(
            id="day",
            className="dropdown",
            options=[{"label": day, "value": day} for day in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]],
            value="1",
            clearable=False,
        ),
        ]),

        html.Div(className="filter-bar", id="time-periods", children=[
            html.Div([html.P("Past"), 
            dcc.RadioItems(options=["5S", "30S", "1M", "3M", "10M", "1H"], value='1M', id='time-period-past', inline=True),
                      ]),
            html.Div([html.P("Future"),
            dcc.RadioItems(options=["5S", "30S", "1M", "3M", "10M", "1Hs"], value='1M', id='time-period-future', inline=True),
            
        ]),
        
        
        ]),
        html.H4("STOCK PRICE ANALYSIS"),
        dcc.Graph(id="time-series-chart", style={"width": "90%"}),
        html.H4("MODEL PREDICTION"),
        dcc.Graph(id="model-prediction", style={"width": "90%"}),
        html.H4("VOLUME ANALYSIS"),
        dcc.Graph(id="volume-chart", style={"width": "90%", "height": "300px"}),
        html.H4("ROLLING STANDARD DEVIATION"),
        dcc.RadioItems(options=["30S", "60S"], value='30S', id='time-period-std-dev', inline=True),
        dcc.Graph(id='line-graph',style={"width": "90%", "height": "300px"})
    ]),


    ]),

def calculate_60_sec_std(dataframe):
    
    df_copy = dataframe.copy()

    # Set the timestamp as the index for rolling calculations
    df_copy.set_index('timestamp', inplace=True)

    # Calculate rolling standard deviation with a window of 30 seconds
    rolling_std_dev = df_copy['price'].rolling(window=60, min_periods=1).std().reset_index()
    rolling_std_dev.columns = ['timestamp', '30_sec_rolling_std_dev']

    return rolling_std_dev



def calculate_30_sec_std(dataframe):
    
    df_copy = dataframe.copy()

    # Set the timestamp as the index for rolling calculations
    df_copy.set_index('timestamp', inplace=True)

    # Calculate rolling standard deviation with a window of 30 seconds
    rolling_std_dev = df_copy['price'].rolling(window=30, min_periods=1).std().reset_index()
    rolling_std_dev.columns = ['timestamp', '30_sec_rolling_std_dev']

    return rolling_std_dev

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
    elif period == "10M":
        return pd.Timedelta(minutes=10)
    elif period == "1H":
        return pd.Timedelta(minutes=60)
    else:
        raise ValueError(f"Invalid period: {period}")
    

def filter_data_by_period_start(df, period):
    """Filters the data based on the selected time period."""
    end_date = df["timestamp"].max()
    print("end date", end_date)
    start_date = end_date - period_to_time(period)

    return df[df["timestamp"] >= start_date - pd.Timedelta(seconds=5) ]


#callback(Output("time-series-chart", "figure"), [Input("day", "value"), Input("stock-dropdown", "value"), Input("time-period-past", "value")])
def update_df(day, stock):
    global df, sampled_df, df_predict, sampled_df_predict  # Access the global variables

    path = Path('data') / stock / f'clean_trade_data_{stock}{day}.csv'
    df = pd.read_csv(path)
    sampled_df = df.sort_values(by='timestamp')
    sampled_df["timestamp"] = pd.to_datetime(sampled_df["timestamp"])

    path = Path('pred_data')/ stock /f'pred_trade_data_{stock}{day}.csv'
    df_predict = pd.read_csv(path)
    sampled_df_predict = df_predict.sort_values(by='timestamp')
    sampled_df_predict["timestamp"] = pd.to_datetime(sampled_df_predict["timestamp"])


@callback(
    Output("average-price", "children"),
    [Input("time-period-past", "value"), Input("day", "value"), Input("stock-dropdown", "value")],
)
def average_price(period, day, stock):
    # Update the dataset based on the selected day and stock
    update_df(day, stock)
    
    # Filter the data for the specified period
    filtered_df = filter_data_by_period_start(sampled_df, period)
    
    # Check if the filtered DataFrame is empty to avoid errors
    if filtered_df.empty:
        return "No data available for the selected period"
    
    # Calculate the average price for the period
    avg_price = filtered_df["price"].mean()
    
    # Return the average price as formatted text
    return f"Average Price: ${avg_price:.2f}"


@callback(
    Output("closing-price", "children"),
    [Input("time-period-past", "value"), Input("day", "value"), Input("stock-dropdown", "value"),],
)
def closing_price(period, day, stock):
    update_df(day, stock)
    filtered_df = filter_data_by_period_start(sampled_df, period)
    last_price = filtered_df["price"].iloc[-1]
    return f"Closing Price: ${last_price:.2f}"

@callback(
    Output("opening-price", "children"),
    [Input("time-period-past", "value"), Input("day", "value"), Input("stock-dropdown", "value"),],
)
def opening_price(period, day, stock):
    update_df(day, stock)
    filtered_df = filter_data_by_period_start(sampled_df, period)
    first_price = filtered_df["price"].iloc[0]
    return f"Opening Price: ${first_price:.2f}"

@callback(
    Output("top-price", "children"),
    [Input("time-period-past", "value"), Input("day", "value"), Input("stock-dropdown", "value"),],
)
def stock_data(period, day, stock):
    update_df(day, stock)
    filtered_df = filter_data_by_period_start(sampled_df, period)
    max_price = filtered_df["price"].max()
    return f"Top Price: ${max_price:.2f}"

@callback(
    Output("bottom-price", "children"),
    [Input("time-period-past", "value"), Input("day", "value"), Input("stock-dropdown", "value"),],
)
def stock_data_bottom(period, day, stock):
    update_df(day, stock)
    filtered_df = filter_data_by_period_start(sampled_df, period)
    max_price = filtered_df["price"].min()
    return f"Min Price: ${max_price:.2f}"

@callback(
    Output("time-series-chart", "figure"),
    [Input("day", "value"), Input("stock-dropdown", "value"), Input("time-period-past", "value")],
)
def update_time_series(day, stock, period):
    update_df(day, stock)
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
            font=dict(color="#c9b375"),          # Global font color for titles and legends

        template="plotly_dark"
    )
    return fig

#TODO: Implement the model prediction chart
@callback(
    Output("model-prediction", "figure"),
    [Input("day", "value"), Input("stock-dropdown", "value"), Input("time-period-past", "value")],
)
def update_model_prediction(day, stock, period):
    update_df(day, stock)
    filtered_df = filter_data_by_period_start(sampled_df_predict, period)
    if filtered_df.empty:
        print(f"Filtered dataframe is empty for period: {period}")
        return px.line(title="No data available for the selected period")

    current_date = filtered_df["timestamp"].max()
    time_delta = period_to_time(period)
    print(f"Updating figure with {len(filtered_df)} points")

    fig = px.line(filtered_df, x="timestamp", y="Test prediction", title=f"Stock Price")
    fig.update_layout(
        xaxis=dict(
            range=[current_date - time_delta, current_date],
            title="Timestamp"
        ),
        yaxis=dict(title="Price"),
            font=dict(color="#c9b375"),          # Global font color for titles and legends

        template="plotly_white"
    )
    return fig

@callback(
    Output("volume-chart", "figure"),
    [Input("day", "value"), Input("stock-dropdown", "value"), Input("time-period-past", "value")],
)
def update_volume_chart(day, stock, period):
    update_df(day, stock)
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
        font=dict(color="#c9b375"),          # Global font color for titles and legends

        template="plotly_dark"
    )
    return fig

@callback(
    Output("line-graph", "figure"),  # Update the figure of 'line-graph'
    [Input("day", "value"), Input("stock-dropdown", "value"), Input("time-period-past", "value"), Input("time-period-std-dev", "value")]
)
def update_standard_deviation_chart(day, stock, period, std_dev_period):
    update_df(day, stock)
    # Calculate rolling standard deviation for the full DataFrame
    if std_dev_period == "60S":
        standard_dev_df = calculate_60_sec_std(sampled_df)
    else:
        standard_dev_df = calculate_30_sec_std(sampled_df)
    
    # Filter the data based on the selected period
    filtered_df = filter_data_by_period_start(standard_dev_df, period)
    
    if filtered_df.empty:
        print(f"Filtered dataframe is empty for period: {period}")
        return go.Figure()  # Return an empty figure if no data
    
    # Create the figure for rolling standard deviation
    fig = go.Figure()

    # Add the rolling standard deviation line
    fig.add_trace(go.Scatter(
        x=filtered_df['timestamp'],
        y=filtered_df['30_sec_rolling_std_dev'],
        mode='lines',  # Line graph mode
        name='Rolling Standard Deviation',
        line=dict(color='blue')
    ))

    # Update the layout of the figure
    fig.update_layout(
        title=f"Rolling Standard Deviation (Period: {period})",
        xaxis=dict(title="Timestamp"),
        yaxis=dict(title="Standard Deviation"),
        font=dict(color="#c9b375"),          # Global font color for titles and legends
        template="plotly_dark"
    )

    return fig