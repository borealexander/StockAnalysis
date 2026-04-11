# main file to run stock analysis
import os
import matplotlib
matplotlib.use('Qt5Agg') 
from runner.StockRunner import StockRunner


def main():

    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "setup.json")
    runner = StockRunner(source_type = "json", json_path = json_path, category = "stocks")
    runner.run_stock_analysis()


if __name__ == "__main__":
    main()
