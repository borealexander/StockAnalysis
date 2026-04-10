import matplotlib.pyplot as plt
from visualizer.line_plot_sma import line_plot_sma

def line_plot_sma_multiple(ticker, price_data, sma50, sma200, colors, title = "Stock"):

    fig, axes = plt.subplots(1, 3, figsize = (18, 6))

    days_in_year = 250
    periods = [("1 year", days_in_year),
                ("3 year", 3*days_in_year),
                ("5 year", 5*days_in_year)]
    
    for i, (plot_label, days) in enumerate(periods):
        ax = axes[i]

        price_plot = price_data.tail(days)
        sma50_plot = sma50.tail(days)
        sma200_plot = sma200.tail(days)

        line_plot_sma(ticker = ticker,
                      price_data = price_plot,
                      sma50 = sma50_plot,
                      sma200 = sma200_plot,
                      colors = colors,
                      title = plot_label,
                      ax = ax,
                      show_legend = (i == 0),
                      show_xlabel = False,
                      show_ylabel = False)
        ax.tick_params(axis='x', rotation=45)

    fig.suptitle(f"{title} ({ticker})", fontsize=18, fontweight='bold', y=1.05)

    fig.text(0.5, 0.01, 'Date', ha='center', fontsize=14)
    fig.text(0.01, 0.5, 'Price', va='center', rotation='vertical', fontsize=14)
    
    plt.tight_layout(rect=[0.03, 0.03, 1, 0.95])
    
    safe_ticker = ticker.replace(".", "_")
    plt.savefig(f"plots/multiple_sma_{safe_ticker}.png", bbox_inches='tight')
    plt.close()
        

