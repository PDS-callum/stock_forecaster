import dash
from dash import dash_table
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
import pandas as pd

# Define your stock symbols (replace with your list)
stock_symbols = ["AAPL", "TSLA", "GOOG"]
def_df = yf.download(stock_symbols[0]).reset_index()

app = dash.Dash(__name__)

# App Layout
app.layout = html.Div([
    html.H1("Stock Price Dashboard"),
    html.Div(id="stock_dropdown_div", children=[
        dcc.Dropdown(
            id="stock_dropdown",
            options=[{"label":x, "value":x} for x in stock_symbols],
            value=stock_symbols[0]
        )
    ]),
    html.Div(id="graph1_div", children=[
        dcc.Graph(id="graph1")
    ]),
    html.Div(id="stock_table_div",children=[
        dash_table.DataTable(
            id="stock_table",
            data=def_df.head().to_dict('records'),
            columns=[{"name": i, "id": i} for i in def_df.columns])
    ])
])

# Dropdown callback to update stock data
@app.callback(
    [Output(component_id="graph1", component_property="figure"),Output(component_id="stock_table", component_property="data")],
    Input(component_id="stock_dropdown", component_property="value")
)
def update_stock_data(stock_symbol):
    print(stock_symbol)
    df = yf.download(stock_symbol,interval="5m",period="1mo").reset_index()
    print(df.columns)
    fig = go.Figure(go.Candlestick(
        x=df.Datetime,
        open=df.Open,
        high=df.High,
        low=df.Low,
        close=df.Close
    ))
    fig.update_xaxes(
        rangebreaks=[
            dict(bounds=[pd.Timestamp("16:00:00"), pd.Timestamp("09:30:00").shift(day=1)], pattern="hour"),
            dict(bounds=["sat","sun"], pattern="day of week"),
            ])
    return fig,df.head().to_dict("records")

if __name__ == "__main__":
    app.run_server(debug=True)