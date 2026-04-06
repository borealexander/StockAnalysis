import pandas as pd

class StockAnalyzer:
    def __init__(self, reader):

        self.reader = reader
        self.price_data = reader.get_price_data()
        self.volume_data = reader.get_volume_data()
        self.sma50 = self.get_moving_average(window = 50)
        self.sma200 = self.get_moving_average(window = 200)


    def get_moving_average(self, window):

        if self.price_data is None:
            print("No price data available!")
            return None

        moving_average = self.price_data.rolling(window = window, min_periods = 1).mean()
        
        return moving_average.round(2)
    
    def get_above_moving_average(self):

        return None