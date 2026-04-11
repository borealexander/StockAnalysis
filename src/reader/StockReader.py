import json
import os
import pandas as pd
import yfinance as yf
from curl_cffi import requests

class StockReader:
    def __init__(self, input_file, category_name, period = "10d", interval = "1d"):

        self.input_file = input_file
        self.category_name = category_name
        self.period = period
        self.interval = interval
        self.data = None
        self.price_data = None
        self.volume_data = None

        self.get_history(period = self.period, interval = self.interval)

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

    def get_history(self, period = "5y", interval = "1d"):

        tickers = self.get_ticker()

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
