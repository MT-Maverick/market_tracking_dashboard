from dash import html

layout = html.Div(id="side_panel",
    children=[
        html.H2("Current Share Value"),
        html.Div(id="current-share-value"),
        html.Button("Stats.", id="statistics-button"),  # Add toggle button
        html.Button("Dividends Yield", id="dividends-button"),  # Add toggle button
        html.Button("Suggestions", id="recommendations-button"),  # Add toggle button
        html.Button("More Info.", id="info-button"),  # Add toggle button

    ],
   
)