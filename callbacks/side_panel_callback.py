from dash import Output, Input, State

def register_callback(app):
    @app.callback(
        Output("side_panel", "style"),
        State("side_panel", "style"),
        [Input("statistics-button", "n_clicks"),
        Input("dividends-button", "n_clicks"),
        Input("recommendations-button", "n_clicks"),
        Input("info-button", "n_clicks"),
        Input("Finacials", "n_clicks"),
        Input("Balancesheet", "n_clicks"),]
    )
    def toggle_sidebar(statistics_button,dividends_button,recommendations_button,info_button,current_style,Finacials,Balancesheet):
        
        return None