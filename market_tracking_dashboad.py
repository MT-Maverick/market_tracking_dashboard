from dash import dash, dcc, html, Output, Input
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import os

app = dash.Dash(__name__,external_stylesheets=['assets/styles.css'])

app.layout = html.Div(id="header",
    children=[
        html.Div(id="side-panel",
            children=[
                html.H2("Current Share Value"),
                html.Div(id="current-share-value"),
            ]
        ),

        html.Div(id="graph",
            children=[
                html.H1("JSE Stock Candlestick Chart"),
                dcc.Graph(id="candlestick-chart"),
                dcc.Interval(id="interval-component", interval=60 * 1000, n_intervals=0),
            ]
        ),
    ]  
)

@app.callback(
    Output("current-share-value", "children"),
    Output("candlestick-chart", "figure"),
    Input("interval-component", "n_intervals")
)
def update_data(n):
    jse = yf.Ticker("JSE.JO")
    current_price = jse.history(period="1d")['Close'].iloc[0] 

    df = pd.DataFrame(jse.history(period="1mo"))

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,vertical_spacing=0.01, row_heights=[0.7, 0.3])

    fig.add_trace(go.Candlestick(x=df.index,
                                 open=df['Open'], 
                                 high=df['High'],
                                 low=df['Low'], 
                                 close=df['Close']),
                   row=1, col=1)

    fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume'), row=2, col=1)

    fig.update_layout(
        xaxis=dict(
        rangeslider=dict(visible=False),
        type="category",
        tickmode="array",
        tickvals=df.index,
        ticktext=df.index.strftime("%d"),
        ),
        yaxis=dict(title='Price'),  # Add title to price axis
        yaxis2=dict(title='Volume'),  # Add title to volume axis    
    )

    return  f"R {current_price}",fig  

if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8888)))