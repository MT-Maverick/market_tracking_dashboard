from dash import dcc, html

layout = html.Div(id="chart",
    children=[
        html.H1("JSE Stock Candlestick Chart", style={"textAlign": "center"}),
        dcc.Graph(id="candlestick-chart"),
    ],
    
)