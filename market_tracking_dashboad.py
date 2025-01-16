from dash import dash, dcc, html, Output, Input
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import os

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H2("Current Share Value", style={"textAlign": "center"}),
                html.Div(id="current-share-value", style={"fontSize": "24px", "textAlign": "center"}),
            ],
            style={
                "width": "10%",
                "float":"Left",
                "height": "100vh",
                "backgroundColor": "#f0f0f0", 
                "padding": "20px",
            },
        ),
        html.Div(
            children=[
                html.H1("JSE Stock Candlestick Chart", style={"textAlign": "center"}),
                dcc.Graph(id="candlestick-chart"),
                dcc.Interval(id="interval-component", interval=60 * 1000, n_intervals=0),
            ],
            style={
                "width": "80%",
                "float": "right",
                "height": "100vh",
                "padding": "10px",
            },
        ),
    ],
    style={"overflow": "hidden"},  
)

@app.callback(
    Output("current-share-value", "children"),
    Output("candlestick-chart", "figure"),
    Input("interval-component", "n_intervals")
)
def update_data(n):
    jse = yf.Ticker("JSE.JO")
    current_price = jse.history_metadata.get("regularMarketPrice")  

    df = pd.DataFrame(jse.history(period="1mo"))
    print("current_price,df")
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(visible=False),
            type="category",
            tickmode="array",
            tickvals=df.index,
            ticktext=df.index.strftime("%d"),
        ),
    )
    return  f"R {current_price}",fig  

if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8888)))