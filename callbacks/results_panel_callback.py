from dash import html, Input, Output, callback_context
from prettytable import PrettyTable
import os
import yfinance as yf
from dotenv import load_dotenv
from google import genai

#Call back method to display stock info onto webpage div object
def ButtonComponent(app):  
    button = html.Button('Click me', id='my-button')

    @app.callback(
        Output('output-container', 'children'),
        Input('statisticsButton', 'n_clicks'),
        Input('dividendsButton', 'n_clicks'),
        Input('recommendationsButton', 'n_clicks'),
        Input('infoButton', 'n_clicks'),
        Input('financialsButton', 'n_clicks'),
        Input('balanceSheetButton', 'n_clicks'),
        

    )
    #Method to setup response of what each button is to display
    def update_output(statisticsButton,dividendsButton,recommendationsButton,infoButton,financialsButton,balanceSheetButton):
        
        jse = yf.Ticker("JSE.JO")
        info = jse.info

        #AI api to generate prompt using stats        
        load_dotenv(dotenv_path='./.gitignore/storage.env')
        api_key = os.getenv('gemini_api_key')
        client = genai.Client(api_key=api_key)
        
        #Statistics Data:
        open = jse.history(period="5d")["Open"].iloc[-1].round(2)
        close = jse.history(period="5d")["Close"].iloc[-1].round(2)    
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
        recommendationKey = jse.info.get('recommendationKey')
        numberOfAnalystOpinions = info.get("numberOfAnalystOpinions")

        #AI api with data prompt for current preformance.
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=f"as a qualified technical analyst who has been provided with the following data: open of {open}, volatility of {volatility}, averageDailyVolume10Day of{averageDailyVolume10Day}, enterpriseValue of {enterpriseValue}, and shortRatio of {shortRatio} for the company {jse.info.get("longName")} along with the finacial statement {jse.financials} and balanceSheet {jse.balancesheet} provide tips on on it projection in 15 lines. consider current market conditions and semantics around the index aswell"
            )
        print(response)

        #More info:
        address = info.get("address2","N/A") +" "+ info.get("city","N/A")+" "+info.get("zip","N/A")+" "+info.get("country","N/A")
        phone = info.get("phone","N/A")
        sector = info.get("sector", "N/A")
        website = info.get("website","N/A")
        details = info.get("longBusinessSummary","N/A")
        """
        #Finacials information:
        finacials = jse.financials
        balanceSheet = jse.balancesheet"""

        #More info:
        phone = info.get("phone","N/A")
        sector = info.get("sector", "N/A")
        website = info.get("website","N/A")
        details = info.get("longBusinessSummary","N/A")
        

        
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
            html.P(f"recomendation:{response.text}"),

        ])
        moreInfo = html.Div(id="moreInfo",
            children=[
            html.P(f"Address: {address}"),
            html.P(f"Industry: {sector}"),
            html.P(f"Phone: {phone}"),
            html.A(f"Site: {website}", href=f"{website}",target=website),
            html.P(f"{details}"),
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
        elif button_id == "financialsButton":
            return None
        elif button_id == "balanceSheetButton":
            return None

