import os
import json
from reader.StockReader import StockReader
from analyzer.StockAnalyzer import StockAnalyzer
from visualizer.StockVisualizer import StockVisualizer

class StockRunner:

    def __init__(self, source_type = "json", json_path = None, sheet_url = None, category = "stocks"):
        self.source_type = source_type.lower()
        self.json_path = json_path
        self.sheet_url = sheet_url
        self.category = category

        self.setup_data = self._load_config()
        self.names = self.setup_data.get("name_conversion", {})


    def _load_config(self):
        with open(self.json_path, "r", encoding = "utf-8") as f:
            return json.load(f)
        
    def run_stock_analysis(self):
        

        try:

            reader = StockReader(input_file = self.json_path, 
                                 category_name = self.category, 
                                 period = "5y", interval = "1d")

            analyzer = StockAnalyzer(reader)
            visualizer = StockVisualizer()

            tickers = reader.get_ticker()
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