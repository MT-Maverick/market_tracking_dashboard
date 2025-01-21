from dash import html, Input, Output, callback_context
from IPython.display import Markdown
import yfinance as yf

def ButtonComponent(app):  
    button = html.Button('Click me', id='my-button')

    @app.callback(
        Output('output-container', 'children'),
        Input('statisticsButton', 'n_clicks'),
        Input('dividendsButton', 'n_clicks'),
        Input('recommendationsButton', 'n_clicks'),
        Input('infoButton', 'n_clicks'),
        
    )
    def update_output(statisticsButton,dividendsButton,recommendationsButton,infoButton):
        jse = yf.Ticker("JSE.JO")
        info = jse.info


        #Statistics Data:
        open = jse.history(period="5d")["Open"].iloc[-1]
        close = jse.history(period="5d")["Close"].iloc[-1]    
        enterpriseValue = info.get("enterpriseValue","N/A")
        averageDailyVolume10Day = info.get("averageDailyVolume10Day","N/A")
        shortRatio = info.get("shortRatio","N/A")

        #Dividence Data
        dividendRate = info.get("dividendRate", "N/A")
        dividendYield = info.get("dividendYield", "N/A")
        payoutRatio = info.get("payoutRatio", "N/A")
        fiveYearAvgDividendYield = info.get("fiveYearAvgDividendYield", "N/A")        
        volatility =  jse.history(period="1mo")["Close"].std()

        #Suggestions Data:
        recommendationKey = info.get("recommendationKey","N/A")
        numberOfAnalystOpinions = info.get("numberOfAnalystOpinions","N/A")

        #More info:
        address = info.get("address2","N/A") +" "+ info.get("city","N/A")+" "+info.get("zip","N/A")+" "+info.get("country","N/A")
        phone = info.get("phone","N/A")
        sector = info.get("sector", "N/A")
        website = info.get("website","N/A")
        

        dividendInfo = html.Div(id="dividendInfo",
            children=[
            html.P(f"dividend Rate: {dividendRate}"),
            html.P(f"dividend Yield: {dividendYield}"),
            html.P(f"payout Ratio: {payoutRatio}"),
            html.P(f"5-Year Avg Dividend Yield: {fiveYearAvgDividendYield}"),
            html.P(f"Volatility (30-day): {volatility:.2f}")
        ])

        statisticsInfo = html.Div(id="statisticsInfo",
            children=[
            html.P(f"open: {open}"),
            html.P(f"close: {close}"),
            html.P(f"enterpriseValue: {enterpriseValue}"),
            html.P(f"averageDailyVolume10Day: {averageDailyVolume10Day}"),
            html.P(f"shortRatio: {shortRatio}")
        ]) 

        suggestionsInfo = html.Div(id="suggestionsInfo",
            children=[
            html.P(f"recommendationKey: {recommendationKey}"),
            html.P(f"numberOfAnalystOpinions: {numberOfAnalystOpinions}"),

        ])

        moreInfo = html.Div(id="moreInfo",
            children=[
            html.P(f"Address: {address}"),
            html.P(f"Industry: {sector}"),
            html.P(f"Phone: {phone}"),
            html.P(f"Site: {website}"),
        ]) 

        ctx = callback_context

        button_id = ctx.triggered[0]["prop_id"].split(".")[0] 
        
        if button_id == "statisticsButton":
            return statisticsInfo
        elif button_id == "dividendsButton":
            return dividendInfo
        elif button_id == "recommendationsButton":
            return suggestionsInfo
        elif button_id == "infoButton":
            return moreInfo
