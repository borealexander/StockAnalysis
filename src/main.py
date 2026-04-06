# main file to run stock analysis

import pandas as pd
import yfinance as yf
import json 
import os
from reader.StockReader import StockReader

def main():

    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "setup.json")

    category = "stocks"

    reader = StockReader(json_path, category)

    try:

        tickers = reader.get_ticker()

        for ticker in tickers:
            nbr = reader.get_number_for_ticker(ticker)
            print(f"Stock: {ticker} | Number in portfolio: {nbr}" )

    except Exception as e:
        print(f"ERROR: {e}")


    try:

        reader.get_history(period = "5y")

        stock_price = reader.get_price_data()
        stock_volume = reader.get_volume_data()

        print(stock_price)

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
