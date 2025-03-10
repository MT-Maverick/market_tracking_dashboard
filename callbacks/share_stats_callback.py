import os
import yfinance as yf
import pandas as pd
from cachetools import cached, TTLCache
import google.generativeai as genai
from dotenv import load_dotenv
from dash import Dash, Output, Input, html,callback_context
import yfinance as yf
import pandas as pd
from cachetools import cached, TTLCache

data_cache = TTLCache(maxsize=10, ttl=3600)

@cached(data_cache)
def get_jse_data():
    """Fetches and caches JSE data from yfinance."""
    jse = yf.Ticker("JSE.JO")
    data = {
        "info": jse.info,
        "history": jse.history(period="1mo"),
        "dividends": jse.dividends,
        "recommendations": jse.recommendations,
        "financials":jse.financials,
        "balance_sheet":jse.balance_sheet
    }
    return data

@cached(data_cache)
def get_current_price():
    jse = yf.Ticker("JSE.JO")
    current_price = jse.history(period="1d")['Close'].iloc[0]
    return current_price


def register_callback(app):
    @app.callback(
        Output("stats-content", "children"),
        Input("statistics-button", "n_clicks"),
        Input("dividends-button", "n_clicks"),
        Input("recommendations-button", "n_clicks"),
        Input("info-button", "n_clicks"),
        Input("Finacials", "n_clicks"),
        Input("Balancesheet", "n_clicks"),
    )
    def update_stats(statistics_clicks, dividends_clicks, recommendations_clicks, info_clicks,Finacials,Balancesheet):
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
            stats_html = [html.P(f"{key}: R{value}") for key, value in stats.iloc[-1].items()]
            return html.Div(stats_html)
       
        elif "dividends-button" in changed_id:
            # Fetch and format dividends data
            dividends = jse.dividends
            dividends_html = [html.P(f"{key.strftime('%y-%m-%d')}: R{round(value,2)}") for key, value in dividends.items()]
            return html.Div(dividends_html)
       
        elif "recommendations-button" in changed_id:
            # Fetch and format recommendations data
            recommendations = jse.recommendations
            recommendations_html = [html.P(f"{key}: {value}") for key, value in recommendations.iloc[-1].items()]
            return html.Div(recommendations_html)
       
        elif "info-button" in changed_id:
            # Format the entire info of the jse stock.
            info_html = [html.P(f"{key}: {value}") for key, value in info.items()]
            return html.Div(info_html[:11])
        
        elif "Finacials" in changed_id:
            # Format the entire info of the jse stock.
            finacials = jse.financials
            return html.Div(run_gemini_prompt(finacials))

       
        elif "Balancesheet" in changed_id:
            # Format the entire info of the jse stock.
            balancesheet = jse.balance_sheet
            return html.Div(run_gemini_prompt(balancesheet))
        
        else:
            # This should technically not happen, but it's a good safety net
            return html.Div("Error: Unknown trigger.")
