import dash
from dash import dcc, html, Output, Input 
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import os

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="JSE Stock Candlestick Chart"),
        dcc.Graph(id="candlestick-chart"),
        dcc.Interval(id="interval-component", interval=60 * 1000, n_intervals=0),  # Update every minute
    ],
    style={"width": "80%", "margin": "auto","overflowX":"hidden"}
)

@app.callback(Output("candlestick-chart", "figure"), Input("interval-component", "n_intervals"))
def update_candlestick_chart(n):
    jse = yf.Ticker('JSE.JO')
    df = pd.DataFrame(jse.history(period='1mo'))  # Fetch data for the past month
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])
    fig.update_layout(
    xaxis=dict(
        rangeslider=dict(visible=False),  # Hide the rangeslider
        type="category",  # Treat x-axis as categorical for better scrolling
        tickmode='array',
        tickvals=df.index,
        ticktext=df.index.strftime('%d')  # Format to display only the day
    ),
 
    )
    return fig

if __name__ == "__main__":
    app.run_server(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8888)))