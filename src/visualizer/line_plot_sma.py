import matplotlib.pyplot as plt

def line_plot_sma(ticker, price_data, sma50, sma200, colors, title: "Stock", ax = None, show_legend = True, show_labels = True):

    if ax is None:
        fig, ax = plt.subplots(figsize = (15,9))
        is_standalone = True
    else:
        fig = ax.get_figure()
        is_standalone = False

    price_plot = price_data[ticker].dropna()
    sma50_plot = sma50[ticker].dropna() if sma50 is not None else None
    sma200_plot = sma200[ticker].dropna() if sma200 is not None else None

    if price_plot.empty:
        return

    ax.plot(price_plot.index, price_plot.values, label='Price', color=colors['price'], linewidth=1, alpha=0.9)
    
    if sma50_plot is not None and not sma50_plot.empty:
        ax.plot(sma50_plot.index, sma50_plot.values, color=colors["sma50"], linestyle="--", label="SMA 50")
    
    if sma200_plot is not None and not sma200_plot.empty:
        ax.plot(sma200_plot.index, sma200_plot.values, color=colors["sma200"], linestyle="--", label="SMA 200")


    ax.set_title(title)
    
    if show_labels:
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
    
    ax.grid(True, alpha = 0.25)

    if show_legend:
        ax.legend()


    if is_standalone:
        safe_ticker = ticker.replace(".", "_")
        file_path = f"plots/sma_plot_{safe_ticker}.png"
        plt.savefig(file_path)
        plt.close()


    
