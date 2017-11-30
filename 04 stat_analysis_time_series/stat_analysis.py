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


def get_bollinger_bands(rm, rstd):
    """
    Return upper and lower Bollinger Bands.
    :param rm: rolling mean of a series
    :param rmstd: rolling std of a series
    :return: Bollinger upper band and lower band
    """
    upper_band = rm + rstd*2
    lower_band = rm - rstd*2
    return upper_band, lower_band    


def compute_daily_returns(df):
    """Compute and return the daily return values"""
    daily_returns = df.pct_change()
    daily_returns.ix[0,:] = 0
    return daily_returns


def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()


def test_run():
    # Define a date range
    dates = pd.date_range('2012-01-01', '2012-12-31')

    # Choose stock symbols to read
    symbols = ['SPY', 'XOM']
    
    # Get stock data
    df = get_data(symbols, dates)

    # Compute Bollinger Bands for SPY
    # 1. Compute rolling mean
    rm_SPY = df['SPY'].rolling(window=20).mean()

    # 2. Compute rolling standard deviation
    rstd_SPY = df['SPY'].rolling(window=20).std()

    # 3. Compute upper and lower bands
    upper_band, lower_band = get_bollinger_bands(rm_SPY, rstd_SPY)
    
    # Plot raw SPY values, rolling mean and Bollinger Bands
    ax = df['SPY'].plot(title="Bollinger Bands", label='SPY')
    rm_SPY.plot(label='Rolling mean', ax=ax)
    upper_band.plot(label='upper band', ax=ax)
    lower_band.plot(label='lower band', ax=ax)

    # Add axis labels and legend
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc='upper left')
    plt.show()

    # Compute and plot daily returns for SPY and XOM
    daily_returns = compute_daily_returns(df)
    plot_data(daily_returns, title="Daily returns", ylabel="Daily returns")


if __name__ == "__main__":
    test_run()
