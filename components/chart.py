from dash import dcc, html

layout = html.Div(id="chart",
    children=[
        html.H1("Stock Candlestick Chart", style={"textAlign": "center"}),
        dcc.Dropdown(
            id="drop_down_list",

            ),
        html.Div(id="current-share-value"),
        dcc.Graph(id="candlestick-chart"),
         html.Div(id='output-container'),
    ],
    
)