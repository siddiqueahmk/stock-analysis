import os, pandas
import ta
dataframes = {}
buy_symbols = []
sell_symbols = []



for filename in os.listdir('datasets'):
    #print(filename)
    symbol = filename.split(".")[0]
    #print(symbol)
    df = pandas.read_csv('datasets/{}'.format(filename))
    if df.empty:
        continue


    df['date'] = pandas.to_datetime(df['date'])

    df['year_week'] = df['date'].dt.strftime('%G-%V')  # Create a new column combining year and week
    # Identify the last working day of each week
    weeks_closing_data = df.groupby('year_week').tail(1)
    #weeks_closing_data = df.groupby(df['date'].dt.isocalendar().week).tail(1)

    df = weeks_closing_data
    #df.to_csv('datasets_weekly/{}.csv'.format(symbol))

    #df['50sma'] = df['close'].rolling(window=50).mean()
    #df['stddev'] = df['close'].rolling(window=50).std()
    #df['lower_band'] = df['50sma'] - (3 * df['stddev'])
    #df['upper_band'] = df['50sma'] + (3 * df['stddev'])

    bollinger_bands = ta.volatility.BollingerBands(df['close'], window=50, window_dev=3)
    df['bb_upper'] = bollinger_bands.bollinger_hband()
    df['bb_lower'] = bollinger_bands.bollinger_lband()

    df['TR'] = abs(df['high'] - df['low'])
    df['ATR'] = df['TR'].rolling(window=14).mean()

    df['ATR1.8'] = (df['ATR'] * 1.8)

    if (df.iloc[-2]['close'] < df.iloc[-2]['bb_upper']) and (df.iloc[-1]['close'] > df.iloc[-1]['bb_upper']):
        #print(df.iloc[-2]['close'], df.iloc[-2]['upper_band'], df.iloc[-1]['close'],  df.iloc[-1]['upper_band'])
        #print(symbol)
        buy_symbols.append(symbol)

    if symbol == "INFIBEAM": print(df)

    #if(df.iloc[-2]['close'] > df.iloc[-2]['ATR1.8']) and (df.iloc[-1]['close'] < df.iloc[-1]['ATR1.8']):
        #sell_symbols.append(symbol)

    #if(df.iloc[-2]['close'] > df.iloc[-2]['lower_band']) and (df.iloc[-1]['close'] < df.iloc[-1]['lower_band']):
        #sell_symbols.append(symbol)

    dataframes[symbol] = df



def list_symbols(mode=None, symbols=None):

    print('\n')

    if(mode=='buy'):
        msg=f'Stocks to buy:'

    elif(mode=='sell'):
        msg=f'Stocks to sell:'

    print(msg)

    for symbol in symbols:
        if(mode=='buy'):
            msg=f'{symbol}'

        elif(mode=='sell'):
            msg=f'{symbol}'

        print(msg)

    print('\n')


list_symbols(mode='buy', symbols=buy_symbols)
list_symbols(mode='sell', symbols=sell_symbols)
