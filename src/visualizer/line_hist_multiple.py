import matplotlib.pyplot as plt
from visualizer.line_plot_sma import line_plot_sma
from visualizer.hist_plot_returns import plot_hist_returns

def plot_line_hist_multiple(ticker, price_data, sma50, sma200, log_returns, colors, title, bins = 30, show_density = True):

    fig, axes = plt.subplots(2,3, figsize = (22,12))

    days_in_year = 250

    periods = [("1 year", days_in_year),
                ("3 year", 3*days_in_year),
                ("5 year", 5*days_in_year)]
    
    for i, (plot_label, days) in enumerate(periods):

        ax_sma = axes[0, i]

        price_plot = price_data.tail(days)
        sma50_plot = sma50.tail(days)
        sma200_plot = sma200.tail(days)

        line_plot_sma(ticker = ticker,
                      price_data = price_plot,
                      sma50 = sma50_plot,
                      sma200 = sma200_plot,
                      colors = colors,
                      title = plot_label,
                      ax = ax_sma,
                      show_legend = (i == 0),
                      show_xlabel = (i == 1),
                      show_ylabel = (i == 0))
        
        ax_hist = axes[1, i]
        returns_plot = log_returns[ticker].tail(days)

        plot_hist_returns(ticker = ticker,
                          log_returns_data = returns_plot,
                          colors = colors,
                          title = plot_label,
                          ax = ax_hist,
                          bins = bins,
                          show_density = show_density)
        
    fig.suptitle(f"{title} ({ticker})", fontsize=18, fontweight='bold', y=1.05)

    plt.tight_layout()

    safe_ticker = ticker.replace(".", "_")
    plt.savefig(f"plots/line_hist_plot_multiple_{safe_ticker}.png", bbox_inches='tight')
    plt.close()
