import pandas as pd
import numpy as np

class StockAnalyzer:
    def __init__(self, reader):

        self.reader = reader
        self.price_data = reader.get_price_data()
        self.volume_data = reader.get_volume_data()
        self._sma_cache = {}
        self._log_returns = None

##############################################
    def get_sma(self, window):

        if window not in self._sma_cache:
            self._sma_cache[window] = self._calculate_sma(window)

        return self._sma_cache[window]

    def _calculate_sma(self, window):
        
        if self.price_data is None:
            print("No price data available!")
            return None
        
        sma = self.price_data.rolling(window = window, min_periods = 1).mean()

        return sma
    
    @property
    def sma50(self):
        return self.get_sma(50)
    
    @property
    def sma200(self):
        return self.get_sma(200)
    
    ######################################

    @property
    def log_returns(self):
        if self._log_returns is None:
            self._log_returns = self._calculate_log_returns()

        return self._log_returns
    
    def _calculate_log_returns(self):

        if self.price_data is None:
            print("No price data available!")
            return None

        log_ret = np.log(self.price_data / self.price_data.shift(1))

        return log_ret

##############################################
    
    def get_above_moving_average(self):

        return None