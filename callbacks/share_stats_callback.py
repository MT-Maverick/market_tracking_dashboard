# /home/mfundosindane0/market_tracking_dashboard/callbacks/share_stats_callback.py
import yfinance as yf
import pandas as pd
from cachetools import cached, TTLCache
from dash import Dash, Output, Input, html, callback_context

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

def format_dataframe_as_html_table(df):
    """Formats a Pandas DataFrame as an HTML table."""
    if df is None or df.empty:
      return html.Div("No data to display", className="stats-content")
    # Replace any NaN values with empty strings
    df = df.fillna('')
    return html.Table([html.Tr([html.Th(col) for col in df.columns])] + [html.Tr([html.Td(df.iloc[i][col]) for col in df.columns]) for i in range(len(df))])

def format_dataframe_as_html_list(df):
    """Formats a Pandas DataFrame as a list of key-value pairs (one per row)."""
    if df is None or df.empty:
      return html.Div("No data to display", className="stats-content")
    # Replace any NaN values with empty strings
    df = df.fillna('')
    items = []
    for index, row in df.iterrows():
        items.append(html.H6(index))
        for col, value in row.items():
            items.append(html.P(f"{col}: {value}"))
    return html.Div(items)

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
            return html.Div("Click a button to view information.", className="stats-content")
        
        #extract the first change if there is one.
        changed_id = triggered_inputs[0]["prop_id"]

        if "statistics-button" in changed_id:
            # Fetch and format statistics data
            stats = jse.history(period="1mo")
            stats_html = [html.P(f"{key}: R{value}") for key, value in stats.iloc[-1].items()]
            return html.Div(stats_html, className="stats-content")
       
        elif "dividends-button" in changed_id:
            # Fetch and format dividends data
            dividends = jse.dividends
            dividends_html = [html.P(f"{key.strftime('%y-%m-%d')}: R{round(value,2)}") for key, value in dividends.items()]
            return html.Div(dividends_html, className="stats-content")
       
        elif "recommendations-button" in changed_id:
            # Fetch and format recommendations data
            recommendations = jse.recommendations
            recommendations_html = [html.P(f"{key}: {value}") for key, value in recommendations.iloc[-1].items()]
            return html.Div(recommendations_html, className="stats-content")
       
        elif "info-button" in changed_id:
            # Format the entire info of the jse stock.
            info_html = [html.P(f"{key}: {value}") for key, value in info.items()]
            return html.Div(info_html[:11], className="stats-content")
        
        elif "Finacials" in changed_id:
            # Format the entire info of the jse stock.
            financials = jse.financials
            return format_dataframe_as_html_list(financials)

       
        elif "Balancesheet" in changed_id:
            # Format the entire info of the jse stock.
            balancesheet = jse.balance_sheet
            return format_dataframe_as_html_list(balancesheet)
        
        else:
            # This should technically not happen, but it's a good safety net
            return html.Div("Error: Unknown trigger.", className="stats-content")
