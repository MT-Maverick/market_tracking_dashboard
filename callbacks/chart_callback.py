from dash import Output, Input
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

#Call back method for chart:
def register_callback(app):
    @app.callback(
        Output("current-share-value", "children"),
        Output("candlestick-chart", "figure"),
        [Input("interval-component", "n_intervals")]
    )
    def update_data(n):

        jse = yf.Ticker("JSE.JO")   #Create ticker object to access yahoo API
        current_price = jse.history(period="5d")['Close'].iloc[-1] #Get closing/current price of share

        

        df = pd.DataFrame(jse.history(period="ytd")) #Get trading history of share
        df['PriceChange'] = df['Close']-df['Open']
        colour = ['green' if change > 0 else 'red' for change in df['PriceChange']]

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
                            name='Volume',
                            marker_color=colour,
                            opacity=0.6,
                            ),
                            row=2, col=1, 
                            )

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

        return f"Current Price: R{current_price.round(2)}",fig