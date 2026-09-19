import pandas as pd
import  subprocess
from analyzer.StockAnalyzer import StockAnalyzer
from visualizer.StockVisualizer import StockVisualizer

class StockReporter:
    def __init__(self, analyzer: StockAnalyzer):

        self.analyzer = analyzer
        self.visualizer = StockVisualizer()

    def generate_portfolio_report(self, qmd_path = "", output_path = ""):

        print("Start printing report")


    def generate_create_portfolio_report(self, qmd_path = "", output_path = ""):

        print("Start printing report")

    def generate_update_portfolio_report(self, qmd_path = "", output_path = ""):

        print("Start printing report")
