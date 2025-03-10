from dash import Dash, Output, Input, html, no_update,callback_context
import yfinance as yf
import pandas as pd

def register_callback(app):
    @app.callback(
        Output("stats-content", "children"),
        Input("statistics-button", "n_clicks"),
        Input("dividends-button", "n_clicks"),
        Input("recommendations-button", "n_clicks"),
        Input("info-button", "n_clicks"),
    )
    def update_stats(statistics_clicks, dividends_clicks, recommendations_clicks, info_clicks):
        """
        Updates the content of the 'stats-content' div based on which button was clicked.

        Args:
            statistics_clicks (int): The number of clicks on the statistics button.
            dividends_clicks (int): The number of clicks on the dividends button.
            recommendations_clicks (int): The number of clicks on the recommendations button.
            info_clicks (int): The number of clicks on the info button.

        Returns:
            html.Div: The updated content for the 'stats-content' div.
        """

        # Get the JSE ticker object from yfinance
        jse = yf.Ticker("JSE.JO")

        # Get all the info from the jse object
        info = jse.info

        # Determine which input triggered the callback
        triggered_inputs = callback_context.triggered
        if not triggered_inputs:
            # No button has been clicked yet (initial load)
            return html.Div("Click a button to view information.")
        
        #extract the first change if there is one.
        changed_id = triggered_inputs[0]["prop_id"]

        if "statistics-button" in changed_id:
            # Fetch and format statistics data
            stats = jse.history(period="1mo")
            stats_html = [html.P(f"{key}: {value}") for key, value in stats.iloc[-1].items()]
            return html.Div(stats_html)
        elif "dividends-button" in changed_id:
            # Fetch and format dividends data
            dividends = jse.dividends
            dividends_html = [html.P(f"{key}: {value}") for key, value in dividends.items()]
            return html.Div(dividends_html)
        elif "recommendations-button" in changed_id:
            # Fetch and format recommendations data
            recommendations = jse.recommendations
            recommendations_html = [html.P(f"{key}: {value}") for key, value in recommendations.iloc[-1].items()]
            return html.Div(recommendations_html)
        elif "info-button" in changed_id:
            # Format the entire info of the jse stock.
            info_html = [html.P(f"{key}: {value}") for key, value in info.items()]
            return html.Div(info_html)
        else:
            # This should technically not happen, but it's a good safety net
            return html.Div("Error: Unknown trigger.")
