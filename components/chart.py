from dash import dcc, html

layout = html.Div(id="chart",
    children=[
        html.H1("JSE Stock Candlestick Chart", style={"textAlign": "center"}),
        html.Div(id="current-share-value"),
        dcc.Graph(id="candlestick-chart"),
         html.Div(id='output-container'),
    ],
    
)