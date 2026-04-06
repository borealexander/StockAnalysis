import matplotlib.pyplot as plt

def line_plot_sma(ticker, price_data, sma50, sma200, colors, title: "Stock"):
    plt.figure(figsize=(10, 5))
    plt.plot(price_data.index, price_data[ticker], label='Pris', color=colors['price'], linewidth=1.25)

    if sma50 is not None and ticker in sma50.columns:
        plt.plot(sma50.index, sma50[ticker], label='SMA 50', color=colors['sma50'], linestyle='--', alpha=0.8)
        
    if sma200 is not None and ticker in sma200.columns:
        plt.plot(sma200.index, sma200[ticker], label='SMA 200', color=colors['sma200'], linestyle='--', alpha=0.8)

    plt.title(f"{title}: {ticker}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend() 
    plt.grid(True, alpha=0.3)
    
    safe_ticker = ticker.replace(".", "_")
    file_path = f"plots/sma_plot_{safe_ticker}.png"
    plt.savefig(file_path)

    plt.close()
