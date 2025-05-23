# /home/mfundosindane0/market_tracking_dashboard/callbacks/chart_callback.py
from dash import Output, Input, html
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# create a dictionary to store the last price.
previous_prices = {}

def register_callback(app):
    @app.callback(
        Output("candlestick-chart", "figure"),
        Output("current-share-value", "children"),
        Input("interval-component", "n_intervals")
    )
    
    def update_data(n):

        jse = yf.Ticker("JSE.JO")   #Create ticker object to access yahoo API

        current_price = jse.history(period="1d")['Close'].iloc[0] #Get closing/current price of share

        df = pd.DataFrame(jse.history(period="1mo")) #Get trading history of share

        #Create 2 graphs on dcc.Graph canvas using subplots
        fig = make_subplots(rows=2,
                            cols=1,
                            shared_xaxes=True,
                            vertical_spacing=0.01,
                            row_heights=[0.7, 0.3])

        #Create 1st graph that displays market preformance
        fig.add_trace(go.Candlestick(x=df.index,
                                    open=df['Open'],
                                    high=df['High'],
                                    low=df['Low'],
                                    close=df['Close']),
                    row=1, col=1)

        #Create 2nd graph that displays volume of share trade
        fig.add_trace(go.Bar(x=df.index,
                            y=df['Volume'],
                            name='Volume'),
                            row=2, col=1)

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
            plot_bgcolor="#252526",  # Set plot background color
            paper_bgcolor="#252526",
            font_color="#d4d4d4"
        )

        price_class = "current_price"  # Default class

        if "JSE.JO" in previous_prices:
            previous_price = previous_prices["JSE.JO"]
            if current_price > previous_price:
                price_class = "current_price price-up"
            elif current_price < previous_price:
                price_class = "current_price price-down"
        
        previous_prices["JSE.JO"] = current_price

        return fig, html.P(f"R {current_price:.2f}", className=price_class)
