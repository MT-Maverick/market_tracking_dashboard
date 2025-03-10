from dash import html

layout = html.Div(id="share_stats",
    children=[
        html.H3("Share Statistics"),
        html.Div(id="stats-content"),
    ],
)
