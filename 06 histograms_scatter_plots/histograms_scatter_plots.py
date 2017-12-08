"""Histograms and scatter plots"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def symbol_to_path(symbol, base_dir="../../data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if "SPY" not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, "SPY")

    # Read and join data for each symbol
    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col="Date", 
        parse_dates=True, usecols=["Date", "Adj Close"], na_values=["nan"])
        
        # Rename to "Adj Close" for each symbol to prevent clash
        df_temp = df_temp.rename(columns={"Adj Close": symbol})
        
        df = df.join(df_temp)
        if symbol == "SPY": # drop dates SPY didn"t trade
            df = df.dropna(subset=["SPY"])

    return df


def compute_daily_returns(df):
    """Compute and return the daily return values"""
    daily_returns = df.pct_change()
    daily_returns.iloc[0,:] = 0
    return daily_returns


def test_run():
    # Define a date range
    dates = pd.date_range("2009-01-01", "2012-12-31")

    # Choose stock symbols to read
    symbols = ["SPY", "XOM", "GLD"]
    
    # Get stock data
    df = get_data(symbols, dates)

    # Compute daily returns for SPY and XOM
    daily_returns = compute_daily_returns(df)

    # Plot both histograms on the same plot
    daily_returns["SPY"].hist(bins=20, label="SPY")
    daily_returns["XOM"].hist(bins=20, label="XOM")
    plt.legend(loc="upper right")
    plt.show()
    # Another way to plot the above histogram
    #daily_returns.plot(kind="hist", bins=20, y=["SPY", "XOM"])


    # Scatterplot SPY vs. XOM and SPY vs. GLD and the respective best fitting lines
    # Two subplots appear side by side
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    
    # The first subplot SPY vs. XOM and its best fitting line
    ax1.scatter(daily_returns["SPY"], daily_returns["XOM"])
    beta_XOM, alpha_XOM = np.polyfit(daily_returns["SPY"], daily_returns["XOM"], 1)
    print ("beta_XOM = {}\nalpha_XOM = {}".format(beta_XOM, alpha_XOM))
    ax1.plot(daily_returns["SPY"], beta_XOM*daily_returns["SPY"] + alpha_XOM, "-", color="r")
    
    # The first subplot SPY vs. GLD and its best fitting line
    ax2.scatter(daily_returns["SPY"], daily_returns["GLD"])
    beta_GLD, alpha_GLD = np.polyfit(daily_returns["SPY"], daily_returns["GLD"], 1)
    print ("beta_GLD = {}\nalpha_GLD = {}".format(beta_GLD, alpha_GLD))
    ax2.plot(daily_returns["SPY"], beta_GLD*daily_returns["SPY"] + alpha_GLD, "-", color="r")
    
    plt.show()


    """
    # Plot the above scatterplots into separate graphs
    # Scatterplot SPY vs. XOM    
    daily_returns.plot(kind="scatter", x="SPY", y="XOM")
    beta_XOM, alpha_XOM = np.polyfit(daily_returns["SPY"], daily_returns["XOM"], 1)
    print ("beta_XOM = {}\nalpha_XOM={}".format(beta_XOM, alpha_XOM))
    plt.plot(daily_returns["SPY"], beta_XOM*daily_returns["SPY"] + alpha_XOM, "-", color="r")
    plt.show()

    # Scatterplot SPY vs. GLD    
    daily_returns.plot(kind="scatter", x="SPY", y="GLD")
    beta_GLD, alpha_GLD = np.polyfit(daily_returns["SPY"], daily_returns["GLD"], 1)
    print ("beta_GLD = {}\nalpha_GLD={}".format(beta_GLD, alpha_GLD))
    plt.plot(daily_returns["SPY"], beta_GLD*daily_returns["SPY"] + alpha_GLD, "-", color="r")
    plt.show()
    """

    # Calculate the correlation coefficient
    print (daily_returns.corr(method="pearson"))

if __name__ == "__main__":
    test_run()
