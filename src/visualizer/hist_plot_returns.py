import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import norm

def plot_hist_returns(ticker, log_returns_data, colors, title = None, ax = None, bins = 30, show_density = True):

    if ax is None:
        fig, ax = plt.subplots(figsize = (15,9))
        is_standalone = True
    else:
        is_standalone = False

    log_returns = log_returns_data.dropna()

    sns.histplot(log_returns,
                bins = bins,
                kde = True,
                ax = ax,
                color = colors['log_return'],
                edgecolor = "black",
                stat = "density",
                label = "Data",
                alpha = 0.6)
    
    if show_density:
        mu = log_returns.mean()
        sd = log_returns.std()
        x = np.linspace(log_returns.min(), log_returns.max(), 100)
        p = norm.pdf(x, mu, sd)

        ax.plot(x, p, color = colors['log_return_normal'], linewidth = 2, 
                label=rf'$\mu$={mu:.4f}, $\sigma$={sd:.4f}')
        
        ax.legend(fontsize = 9)

    ax.axvline(0, color='black', linestyle='-', alpha=0.3)
    ax.set_title(title)
    ax.set_xlabel("Log Return")
    ax.set_ylabel("Density")

    if is_standalone:
        safe_ticker = ticker.replace(".", "_")
        file_path = f"plots/log_return_plot_{safe_ticker}.png"
        plt.savefig(file_path)
        plt.close()
