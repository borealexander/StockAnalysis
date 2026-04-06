import pandas as pd
import matplotlib.pyplot as plt
from visualizer.line_plot import line_plot
from visualizer.line_plot_sma import line_plot_sma


class StockVisualizer:
    def __init__(self):
        self.style = "ggplot"
        self.title = "Price"
        self.colors = {"price": "#2E5A88",
                       "sma50": "darkorange",
                       "sma200": "firebrick"}

    
    def plot_line(self, ticker, data):
        
        line_plot(ticker, data, self.title)

    def plot_line_sma(self, ticker, data, sma50, sma200, colors = None, title = None):

        if colors is None:
            colors = self.colors
        
        plot_title = title if title else self.title

        line_plot_sma(ticker, data, sma50, sma200, colors = self.colors, title = plot_title)