import os, pandas
import plotly.graph_objects as go

dataframes = {}

symbols_in_squeeze = []
symbols_exiting_squeeze = []
symbols_all = []

for filename in os.listdir('datasets'):
    #print(filename)
    symbol = filename.split(".")[0]
    symbols_all.append(symbol)
    #print(symbol)
    df = pandas.read_csv('datasets/{}'.format(filename))
    if df.empty:
        continue

    df['20sma'] = df['close'].rolling(window=20).mean()
    df['stddev'] = df['close'].rolling(window=20).std()
    df['lower_band'] = df['20sma'] - (2 * df['stddev'])
    df['upper_band'] = df['20sma'] + (2 * df['stddev'])

    df['TR'] = abs(df['high'] - df['low'])
    df['ATR'] = df['TR'].rolling(window=20).mean()

    df['lower_keltner'] = df['20sma'] - (df['ATR'] * 1.5)
    df['upper_keltner'] = df['20sma'] + (df['ATR'] * 1.5)

    def in_squeeze(df):
        return df['lower_band'] > df['lower_keltner'] and df['upper_band'] < df['upper_keltner']

    df['squeeze_on'] = df.apply(in_squeeze, axis=1)

    if df.iloc[-3]['squeeze_on'] and not df.iloc[-1]['squeeze_on']:
        # print("{} is coming out the squeeze".format(symbol))
        symbols_exiting_squeeze.append(symbol)
    elif(df.iloc[-1]['squeeze_on']):
        symbols_in_squeeze.append(symbol)

    

    # save all dataframes to a dictionary
    # we can chart individual names below by calling the chart() function
    dataframes[symbol] = df


def chart(df):
    candlestick = go.Candlestick(x=df['date'], open=df['open'], high=df['high'], low=df['low'], close=df['close'])
    upper_band = go.Scatter(x=df['Date'], y=df['upper_band'], name='Upper Bollinger Band', line={'color': 'red'})
    lower_band = go.Scatter(x=df['Date'], y=df['lower_band'], name='Lower Bollinger Band', line={'color': 'red'})

    upper_keltner = go.Scatter(x=df['Date'], y=df['upper_keltner'], name='Upper Keltner Channel', line={'color': 'blue'})
    lower_keltner = go.Scatter(x=df['Date'], y=df['lower_keltner'], name='Lower Keltner Channel', line={'color': 'blue'})

    fig = go.Figure(data=[candlestick, upper_band, lower_band, upper_keltner, lower_keltner])
    fig.layout.xaxis.type = 'category'
    fig.layout.xaxis.rangeslider.visible = False
    fig.show()

# df = dataframes['GOOGL']
# chart(df)

# df = dataframes['AAPL']
# chart(df)

def list_symbols(mode=None, symbols=None):

    print('\n')

    if(mode=='in_squeeze'):
        msg=f'Symbols currently in a Squeeze:'

    elif(mode=='exiting_squeeze'):
        msg=f'Symbols currently exiting a Squeeze:'

    print(msg)

    for symbol in symbols:
        if(mode=='in_squeeze'):
            msg=f'{symbol} (In Squeeze)'

        elif(mode=='exiting_squeeze'):
            msg=f'{symbol} (Exiting Squeeze)'

        print(msg)

    print('\n')



# list_symbols(symbols=symbols_all)
list_symbols(mode='in_squeeze', symbols=symbols_in_squeeze)
list_symbols(mode='exiting_squeeze', symbols=symbols_exiting_squeeze)
