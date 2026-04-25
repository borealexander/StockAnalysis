import os
import json
import pandas as pd
from reader.StockReader import StockReader
from analyzer.StockAnalyzer import StockAnalyzer
from visualizer.StockVisualizer import StockVisualizer

class StockRunner:

    def __init__(self, source_type = "json", json_path = None, sheet_url = None, ticker_col = None, name_col = None, category = "stocks"):
        self.source_type = source_type.lower()
        self.json_path = json_path
        self.sheet_url = sheet_url
        self.ticker_col = ticker_col
        self.category = category

        self.tickers = []
        self.names = {}

        
        #self.setup_data = self._load_config()
        #self.names = self.setup_data.get("name_conversion", {})

        if self.source_type == "googlesheets":
            df = pd.read_csv(self.sheet_url)
            self.tickers = df[self.ticker_col].dropna().unique().tolist()
            self.names = dict(zip(df[self.ticker_col], df[name_col]))

        elif self.source_type == "json":
            config = self._load_config()
            self.names = config.get("name_conversion", {})

            category_data = config.get(self.category, {})
            self.tickers = list(category_data.keys())




    def _load_config(self):
        with open(self.json_path, "r", encoding = "utf-8") as f:
            return json.load(f)
        
    def run_stock_analysis(self):
        

        try:

            reader = StockReader(tickers = self.tickers,
                                 period = "5y", interval = "1d")

            analyzer = StockAnalyzer(reader)
            visualizer = StockVisualizer()

            tickers = reader.get_tickers()
            prices = reader.get_price_data()

            print(f"Found {len(tickers)} stocks. Starting analysis")

            for ticker in tickers:
                print(f"Analyzing: {ticker}")

                title_name = self.names.get(ticker, ticker)
                visualizer.title = f"Analys: {ticker}"

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

                visualizer.hist_plot_log_returns_multiple(
                    ticker=ticker,
                    log_returns=analyzer.log_returns,
                    title=title_name,
                    bins=40
                )

                visualizer.hist_plot_log_returns(
                    ticker=ticker,
                    log_returns=analyzer.log_returns,
                    title=title_name,
                    bins=60,
                    show_density=True
                )


                visualizer.line_hist_multiple(ticker = ticker,
                                        data = prices,
                                        sma50 = analyzer.sma50, 
                                        sma200 = analyzer.sma200,
                                        log_returns = analyzer.log_returns,
                                        title = title_name,
                                        bins = 30)
            
            print(f"Analysis completed!")

        except Exception as e:
            print(f"ERROR IN RUNNER: {e}")
            raise e