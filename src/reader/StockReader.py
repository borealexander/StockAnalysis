import json
import os
import pandas as pd
import yfinance as yf
from curl_cffi import requests

class StockReader:
    def __init__(self, tickers, period = "10d", interval = "1d"):


        self.tickers = tickers if isinstance(tickers, list) else [tickers]
        self.period = period
        self.interval = interval

        self.price_data = None
        self.volume_data = None

        self.get_history(period = self.period, interval = self.interval)


    def get_tickers(self):

        return self.tickers
    

    def get_history(self, period = "5y", interval = "1d"):

        tickers = self.get_tickers()

        if not tickers:
            return None
        
        session = requests.Session(impersonate="chrome")
        
        try:
           
            data = yf.download(tickers, 
                period = period,
                interval = interval,
                session = session, 
                progress = False,
                auto_adjust = False)

            if not data.empty:
                self.price_data = data['Close'].round(2)
                self.volume_data = data['Volume'].round(0).astype('Int64')
            else:
                print("No data found!")

            return self
        except Exception as e:
            print(f"Could not get stock data: {e}")
            return None

    def get_price_data(self):

        return self.price_data
    
    def get_volume_data(self):

        return self.volume_data
    
    def get_currency(self, ticker):

        ticker_obj = yf.Ticker(ticker)
        currency = ticker_obj.info.get("currency", "Unknown")

        return currency
    
    def get_exchange_rates(self):

        currencies = ["USDSEK=X", "EURSEK=X", "DKKSEK=X"]
        data = yf.download(currencies, period = "5d")["Close"].ffill().bfill().iloc[-1]

        rates = {"USD": data["USDSEK=X"],
                 "EUR": data["EURSEK=X"],
                 "DKK": data["DKKSEK=X"],
                 "SEK": 1.0}
        
        return rates