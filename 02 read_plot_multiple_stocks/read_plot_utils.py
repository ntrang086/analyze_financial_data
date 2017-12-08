"""Utility functions"""

import os
import pandas as pd
import matplotlib.pyplot as plt

def symbol_to_path(symbol, base_dir="../../data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, 'SPY')

    # Read and join data for each symbol
    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date', 
        parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
        
        # Rename to 'Adj Close' for each symbol to prevent clash
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        
        df = df.join(df_temp)
        if symbol == 'SPY': # drop dates SPY didn't trade
            df = df.dropna(subset=['SPY'])

    return df


def normalize_data(df):
    """Normalize stock prices using the first row of the dataframe"""
    return df/df.iloc[0,:]


def plot_data(df, title="Stock prices"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()


def plot_selected(df, columns, start_index, end_index):
    """Plot the desired columns over index values in the given range."""
    plot_data(df.loc[start_index:end_index, columns])


def test_run():
    # Define a date range
    dates = pd.date_range('2010-01-22', '2010-12-31')

    # Choose stock symbols to read
    symbols = ['GOOG', 'IBM', 'GLD']
    
    # Get stock data
    df = get_data(symbols, dates)

    # Normalize the stock data
    df = normalize_data(df)
    print (df)

    # Slice and plot
    plot_selected(df, ['SPY', 'IBM'], '2010-01-22', '2010-04-01')

if __name__ == "__main__":
    test_run()
