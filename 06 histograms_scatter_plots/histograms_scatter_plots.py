"""Stat analysis for time series"""

import os
import pandas as pd
import matplotlib.pyplot as plt

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
    daily_returns.ix[0,:] = 0
    return daily_returns


def test_run():
    # Define a date range
    dates = pd.date_range("2009-01-01", "2012-12-31")

    # Choose stock symbols to read
    symbols = ["SPY", "XOM"]
    
    # Get stock data
    df = get_data(symbols, dates)

    # Compute daily returns for SPY and XOM
    daily_returns = compute_daily_returns(df)

    # Plot both histograms on the same plot
    daily_returns["SPY"].hist(bins=20, label="SPY")
    daily_returns["XOM"].hist(bins=20, label="XOM")
    plt.legend(loc="upper right")
    plt.show()


if __name__ == "__main__":
    test_run()
