from dash import dcc, html

#Layout of stock title, current share price ,chart canvas:
layout = html.Div(id="chart",
    children=[
        html.H1("Stock Candlestick Chart", style={"textAlign": "center"}),
        dcc.Dropdown(
            id="drop_down_list",
            placeholder="JSE",
            ),
        html.Div(id="current-share-value"),
        dcc.Graph(id="candlestick-chart"),
         html.Div(id='output-container'),
    ],
    
)