import json
import os
import pandas as pd
import yfinance as yf
import requests


class StockReader:
    def __init__(self, input_file, category_name):

        self.input_file = input_file
        self.category_name = category_name
        self.data = None

    def _load_file(self):
        if not os.path.exists(self.input_file):
            raise FileNotFoundError(f"File {self.input_file} does not exist!")
        
        with open(self.input_file, "r", encoding = "utf-8") as f:
            full_json = json.load(f)
            self.data = full_json.get(self.category_name, {})

    def get_category(self):

        if self.data is None:
            self._load_file()
        return self.data

    def get_ticker(self):

        category_data = self.get_category()
        return list(category_data.keys())
    
    def get_number_for_ticker(self,ticker):

        category_data = self.get_category()
        return category_data.get(ticker, 0)

    def get_history(self, period = "5y"):

        tickers = self.get_ticker()

        if not tickers:
            return None
        
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        })

        #session = requests.Session(impersonate="chrome")
        
        #a = yf.download("VOLV-B.ST", start="2023-01-01", end="2024-01-01")
        
        try:
           
            data = yf.download(tickers, 
                period = period,
                interval = "1d",
                session = session, 
                progress = False,
                auto_adjust = True)

            if len(tickers) > 1:
                return data['Close']
            else:
                return data['Close'] 
                
        except Exception as e:
            print(f"Could not get stock data: {e}")
            return None

        #data = yf.download(tickers, period = period, interval = "1d")['Close']
        return(data)
