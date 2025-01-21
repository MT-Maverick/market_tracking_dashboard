from dash import Output, Input, State, callback_context

def register_callback(app):
    @app.callback(
        Output("side_panel", "style"),
        Input("statisticsButton", "n_clicks"),
        Input("dividendsButton", "n_clicks"),
        Input("recommendationsButton", "n_clicks"),
        Input("infoButton", "n_clicks"),
    )
    def display_content(statisticsButton, dividendsButton, recommendationsButton, infoButton):
        ctx = callback_context

        button_id = ctx.triggered[0]["prop_id"].split(".")[0]    
        
        return button_id
        