from dash import dcc, html

layout = html.Div(id="chart",
    children=[
        html.H1("Microsoft Stock Candlestick Chart", style={"textAlign": "center"}),
        html.Datalist(id="searchList"),
        html.Div(id="current-share-value"),
        dcc.Graph(id="candlestick-chart"),
         html.Div(id='output-container'),
    ],
    
)