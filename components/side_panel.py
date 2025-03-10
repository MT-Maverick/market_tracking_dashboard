from dash import html

layout = html.Div(id="side_panel",
    children=[
        html.H2("Current Share Value"),
        html.Div(id="current-share-value", style={"fontSize": "24px", "textAlign": "center"}),
        html.Button("Stats.", id="statistics-button"),  # Add toggle button
        html.Button("Dividends Yield", id="dividends-button"),  # Add toggle button
        html.Button("Recomendations", id="recommendations-button"),  # Add toggle button
        html.Button("More Info.", id="info-button"),  # Add toggle button
        html.Button("Finacials.", id="Finacials"),  # Add toggle button
        html.Button("Balancesheet.", id="Balancesheet"),  # Add toggle button

    ],
   
)