# main file to run stock analysis

import pandas as pd
import yfinance as yf
import json 
import os
import matplotlib
matplotlib.use('Qt5Agg') 
import matplotlib.pyplot as plt
from reader.StockReader import StockReader
from analyzer.StockAnalyzer import StockAnalyzer
from visualizer.StockVisualizer import StockVisualizer

def main():

    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "setup.json")

    with open(json_path, 'r', encoding='utf-8') as f:
        setup_data = json.load(f)

    names = setup_data.get("name_conversion", {})

    category = "stocks"

    reader = StockReader(json_path, category, period = "5y")
    """
    try:

        tickers = reader.get_ticker()

        for ticker in tickers:
            nbr = reader.get_number_for_ticker(ticker)
            print(f"Stock: {ticker} | Number in portfolio: {nbr}" )

    except Exception as e:
        print(f"ERROR: {e}")

    """

    try:
    
        analyzer = StockAnalyzer(reader)
        visualizer = StockVisualizer()
        
        # Hämta listan med alla tickers från din JSON
        tickers = reader.get_ticker()
        prices = reader.get_price_data()

        print(f"Hittade {len(tickers)} aktier. Startar analys...")

        for ticker in tickers:
            print(f"Genererar graf för: {ticker}")
            
            title_name = names.get(ticker, ticker)
            # Vi sätter en unik titel för varje graf
            visualizer.title = f"Analys: {ticker}"
            
            # Anropa din SMA-plot för den aktuella aktien i loopen
            visualizer.plot_line_sma(
                ticker, 
                prices, 
                analyzer.sma50, 
                analyzer.sma200,
                title = title_name
            )

            visualizer.plot_line_sma_multiple(
                ticker, 
                prices, 
                analyzer.sma50, 
                analyzer.sma200,
                title = title_name
            )

        print("Analys klar för alla aktier!")

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
