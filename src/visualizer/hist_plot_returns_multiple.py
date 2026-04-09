import matplotlib.pyplot as plt
from visualizer.hist_plot_returns import plot_hist_returns

def plot_hist_returns_multiple(ticker, log_returns_data, colors, title = None, bins = 30, show_density = True):

    fig, axes = plt.subplots(1, 3, figsize = (18,6))

    days_in_year = 250

    periods = [("1 year", days_in_year),
                ("3 year", 3*days_in_year),
                ("5 year", 5*days_in_year)]
    
    for i, (plot_label, days) in enumerate(periods):

        ax = axes[i]

        returns_plot = log_returns_data[ticker].tail(days)

        plot_hist_returns(ticker = ticker,
                          log_returns_data = returns_plot,
                          colors = colors,
                          title = plot_label,
                          ax = ax,
                          bins = bins,
                          show_density = show_density)
        
    fig.suptitle(f"{title} ({ticker})", fontsize=18, fontweight='bold', y=1.05)

    plt.tight_layout()

    safe_ticker = ticker.replace(".", "_")
    plt.savefig(f"plots/log_return_plot_multiple_{safe_ticker}.png", bbox_inches='tight')
    plt.close()