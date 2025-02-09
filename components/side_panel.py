from dash import html

#Side panel for stock details(I.e Dividence yield, market recomendations, current dividences allocation per share etc..):
layout = html.Div(id="side_panel",
    children=[
        html.H3("Menu:"),
        html.Button("Details", id="infoButton"),  # Add toggle button
        html.Button("Stats.", id="statisticsButton"),  # Add toggle button
        html.Button("Dividends Yield", id="dividendsButton"),  # Add toggle button
        html.Button("Suggestions", id="recommendationsButton"),  # Add toggle button
        html.H3("Finacials:"),
        html.Button("Finacials", id="financialsButton"),  # Add toggle button
        html.Button("Balance sheet", id="balanceSheetButton"),  # Add toggle button


    ]
   
)