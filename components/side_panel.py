from dash import html

layout = html.Div(id="side_panel",
    children=[
        html.H4("Menu:"),
        html.Button("Stats.", id="statisticsButton"),  # Add toggle button
        html.Button("Dividends Yield", id="dividendsButton"),  # Add toggle button
        html.Button("Suggestions", id="recommendationsButton"),  # Add toggle button
        html.Button("More Info.", id="infoButton"),  # Add toggle button
    ]
   
)