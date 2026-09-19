import pandas as pd
import numpy as np
import quantstats as qs

class StockAnalyzer:
    def __init__(self, reader: StockReader):

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

    def get_above_moving_average(self, ticker, window = 50):

        price = self.price_data[ticker].dropna()
        sma = self.get_sma(window)[ticker].dropna()

        # check if last day price is above sma
        is_above = price.iloc[-1] > sma.iloc[-1]
    
        count = 0
        for i in range(1, len(price)):
            p = price.iloc[-i]
            s = sma.iloc[-i]

            if is_above:
                if p > s:
                    count +=1
                else:
                    break
            else:
                if p < s:
                    count += 1
                else:
                    break

        return count if is_above else - count

    def get_above_moving_average_all(self, window = 50):

        results = {}
        for ticker in self.price_data.columns:
            results[ticker] = self.get_above_moving_average(ticker, window)

        return results
    

    def get_sharpe_ratio(self, r_f = 0.02, days_in_year = 250, period = 250):

        if self.log_returns is None:
            return None
        
        ret_data = self.log_returns.tail(period)
        
        #daily_rf = r_f/days_in_year
        daily_rf = np.log(1 + r_f) / days_in_year

        daily_returns = ret_data - daily_rf
        avg_returns = daily_returns.mean()

        sd = ret_data.std()
        #qs.stats.sharpe(ret_data, rf=0.02)
        #qs.stats.sharpe(pd.to_numeric(ret_data, errors='coerce').dropna())
        #qs.stats.sharpe(ret_data.iloc[:,1], rf=0.02)

        sharp_ratios = (avg_returns/sd) * np.sqrt(days_in_year)
    
        return sharp_ratios
    
    

############################################

    def calculate_portfolio_value(self):

        total_value = 0

        return total_value
    

    def get_summary(self, amount, exchange_rates):

        summary_df = pd.DataFrame(index = self.price_data.columns)
        
        summary_df["price"] = self.price_data.ffill().iloc[-1]
        summary_df["amount"] = summary_df.index.map(amount).fillna(0).astype(int)
        summary_df["currency"] = [self.reader.get_currency(t) for t in summary_df.index]
        summary_df["above_sma50"] = [self.get_above_moving_average(t, 50) for t in summary_df.index]
        summary_df["above_sma200"] = [self.get_above_moving_average(t, 200) for t in summary_df.index]
        summary_df["1-year_sharpe"] = self.get_sharpe_ratio(r_f = 0.02, days_in_year = 250, period = 250)
        summary_df["3-year_sharpe"] = self.get_sharpe_ratio(r_f = 0.02, days_in_year = 250, period = 750)

        def calculate_sek(row):
            rate = exchange_rates.get(row["currency"], 1.0)
            return row["price"] * row["amount"] * rate

        summary_df["value"] = summary_df.apply(calculate_sek, axis = 1).round(0)

        return summary_df