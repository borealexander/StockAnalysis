import matplotlib.pyplot as plt

def line_plot(ticker, data, title):
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data[ticker])
    plt.title(title)
    plt.show()