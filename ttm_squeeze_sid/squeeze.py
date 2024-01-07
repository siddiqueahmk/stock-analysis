import os
import ta
import plotly.graph_objects as go
import pandas as pd

dataframes = {}
symbols_in_squeeze = []
symbols_exiting_squeeze = []
symbols_all = []
symbols_breaking_out = []

symbols_in_squeeze2 = []
symbols_exiting_squeeze2 = []

for filename in os.listdir('datasets'):
    symbol = filename.split(".")[0]
    #print(symbol)
    data = pd.read_csv('datasets/{}'.format(filename))
    if data.empty or len(data) < 20:
        continue
    # Method 1 -> use the equations directly
    data['20sma'] = data['close'].rolling(window=20).mean()
    data['stddev'] = data['close'].rolling(window=20).std()
    data['upBB'] = data['20sma'] + (3 * data['stddev'])
    data['lowBB'] = data['20sma'] - (3 * data['stddev'])


    data['TR'] = abs(data['high'] - data['low'])
    data['ATR'] = data['TR'].rolling(window=20).mean()

    # Keltner 2x
    data['upKCWide'] = data['20sma'] + (data['ATR'] * 2)
    data['lowKCWide'] = data['20sma'] - (data['ATR'] * 2)

    # Keltner 1.5x
    data['upKCNormal'] = data['20sma'] + (data['ATR'] * 1.5)
    data['lowKCNormal'] = data['20sma'] - (data['ATR'] * 1.5)

    # Keltner 1x
    data['upKCNarrow'] = data['20sma'] + (data['ATR'])
    data['lowKCNarrow'] = data['20sma'] - (data['ATR'])

    data['sqzOnWide'] = (data['lowBB'] >= data['lowKCWide']) & (data['upBB'] <= data['upKCWide'])  # WIDE SQUEEZE: ORANGE
    data['sqzOnNormal'] = (data['lowBB'] >= data['lowKCNormal']) & (data['upBB'] <= data['upKCNormal'])  # NORMAL SQUEEZE: RED
    data['sqzOnNarrow'] = (data['lowBB'] >= data['lowKCNarrow']) & (data['upBB'] <= data['upKCNarrow'])  # NARROW SQUEEZE: YELLOW
    data['sqzOffWide'] = (data['lowBB'] < data['lowKCWide']) & (data['upBB'] > data['upKCWide'])  # FIRED WIDE SQUEEZE: GREEN
    data['noSqz'] = ~((data['sqzOnWide']) | (data['sqzOffWide']))  # NO SQUEEZE: BLUE

    #latest_row = data.iloc[-1]
   # if (latest_row['sqzOnWide'] or latest_row['sqzOnNormal'] or latest_row['sqzOnNarrow']) and not (latest_row['sqzOffWide']):
    #    symbols_in_squeeze.append(symbol)
    #elif latest_row['sqzOffWide']:
    #    symbols_exiting_squeeze.append(symbol)


    if data.iloc[-2]['sqzOnNarrow'] and not data.iloc[-1]['sqzOnNarrow']:
        symbols_exiting_squeeze.append(symbol)
    elif(data.iloc[-1]['sqzOnNarrow']):
        symbols_in_squeeze.append(symbol)

    #Method 2 -> use technical analysis tool 
    #bollinger_bands = ta.volatility.BollingerBands(data['close'], window=20, window_dev=2)
    #data['bb_upper'] = bollinger_bands.bollinger_hband()
    #data['bb_middle'] = bollinger_bands.bollinger_mavg()
    #data['bb_lower'] = bollinger_bands.bollinger_lband()
    #data['bb_width'] = data['bb_upper'] - data['bb_lower']

    # Calculate Keltner Channels
    #data['kc_upper'] = ta.volatility.keltner_channel_hband(data['high'], data['low'], data['close'])
    #data['kc_middle'] = ta.volatility.keltner_channel_mband(data['high'], data['low'], data['close'])
    #data['kc_lower'] = ta.volatility.keltner_channel_lband(data['high'], data['low'], data['close'])
    #data['kc_width'] = data['kc_upper'] - data['kc_lower']

    # Calculate Average True Range (ATR)
    #data['atr'] = ta.volatility.average_true_range(data['high'], data['low'], data['close'])

    # Calculate TTM Squeeze
    #data['squeeze'] = ((data['bb_width'] < data['kc_width'])  & (data['atr'] < data['bb_middle']))

    #if data.iloc[-3]['squeeze'] and not data.iloc[-1]['squeeze']:
    #    symbols_exiting_squeeze2.append(symbol)
    #elif(data.iloc[-1]['squeeze']):
    #    symbols_in_squeeze2.append(symbol)


    # Method 3 -> keep the keltners channel standard and change  bllinger bands width
    #data['20sma'] = data['close'].rolling(window=20).mean()
    #data['stddev'] = data['close'].rolling(window=20).std()
    #data['lower_band'] = data['20sma'] - (3 * data['stddev'])
    #data['upper_band'] = data['20sma'] + (3 * data['stddev'])

    #data['TR'] = abs(data['high'] - data['low'])
    #data['ATR'] = data['TR'].rolling(window=20).mean()

    #data['lower_keltner'] = data['20sma'] - (data['ATR'] * 1.5)
    #data['upper_keltner'] = data['20sma'] + (data['ATR'] * 1.5)

    #def in_squeeze(data):
    #    return data['lower_band'] > data['lower_keltner'] and data['upper_band'] < data['upper_keltner']

    #data['squeeze_on'] = data.apply(in_squeeze, axis=1)

    #if data.iloc[-3]['squeeze_on'] and not data.iloc[-1]['squeeze_on']:
    #    symbols_exiting_squeeze.append(symbol)
    #elif(data.iloc[-1]['squeeze_on']):
    #    symbols_in_squeeze.append(symbol)

    data['volume_20sma'] = data['volume'].rolling(window=20).mean()
    data['volume_50sma'] = data['volume'].rolling(window=50).mean()

    if (data['volume'].iloc[-1] > (3 * data['volume_20sma'].iloc[-1])) and (data['volume'].iloc[-1] > (2 * data['volume_50sma'].iloc[-1])):
        symbols_breaking_out.append(symbol)

    # save all dataframes to a dictionary
    # we can chart individual names below by calling the chart() function
    dataframes[symbol] = data
    #data.to_csv('datasets/{}.csv'.format(symbol))


def chart(df):
    # Calculate Bollinger Bands for different parameters

    # Create candlestick trace
    candlestick = go.Candlestick(x=df['date'], open=df['open'], high=df['high'], low=df['low'], close=df['close'])

    # Create upper and lower Bollinger Bands traces for different conditions
    up_bb_normal = go.Scatter(x=df['date'], y=df['upBB'], name='Upper Bollinger Band (Normal)', line={'color': 'blue'})
    low_bb_normal = go.Scatter(x=df['date'], y=df['lowBB'], name='Lower Bollinger Band (Normal)', line={'color': 'blue'})

    #Kelterns channel wide
    up_kc_wide = go.Scatter(x=df['date'], y=df['upKCWide'], name='Upper Keltners Channel (Wide)', line={'color': 'green'})
    low_kc_wide = go.Scatter(x=df['date'], y=df['lowKCWide'], name='Lower Keltners Channel (Wide)', line={'color': 'green'})
    
    #Kelterns channel normal
    up_kc_normal = go.Scatter(x=df['date'], y=df['upKCNormal'], name='Upper Keltners Channel (Normal)', line={'color': 'red'})
    low_kc_normal = go.Scatter(x=df['date'], y=df['lowKCNormal'], name='Lower Keltners Channel (Normal)', line={'color': 'red'})

    #Keltners channel narrow
    up_kc_narrow = go.Scatter(x=df['date'], y=df['upKCNarrow'], name='Upper Keltners Channel (Narrow)', line={'color': 'orange'})
    low_kc_narrow = go.Scatter(x=df['date'], y=df['lowKCNarrow'], name='Lower Keltners Channel (Narrow)', line={'color': 'orange'})

    # Create squeeze dots traces for different conditions
    squeeze_dots_wide = go.Scatter(x=df['date'][df['sqzOnWide']], y=[0] * sum(df['sqzOnWide']),
                                   mode='markers', marker=dict(color='orange', size=10), name='Squeeze Dots (Wide)')

    squeeze_dots_normal = go.Scatter(x=df['date'][df['sqzOnNormal']], y=[0] * sum(df['sqzOnNormal']),
                                    mode='markers', marker=dict(color='red', size=10), name='Squeeze Dots (Normal)')

    squeeze_dots_narrow = go.Scatter(x=df['date'][df['sqzOnNarrow']], y=[0] * sum(df['sqzOnNarrow']),
                                    mode='markers', marker=dict(color='yellow', size=10), name='Squeeze Dots (Narrow)')

    # Create figure
    fig = go.Figure(data=[candlestick, up_kc_wide, low_kc_wide, squeeze_dots_wide,
                          up_kc_normal, low_kc_normal, squeeze_dots_normal,
                          up_kc_narrow, low_kc_narrow, squeeze_dots_narrow, up_bb_normal, low_bb_normal])

    # Update figure layout
    fig.update_layout(xaxis=dict(type='date'), xaxis_rangeslider=dict(visible=False))
    fig.show()
    #fig.layout.xaxis.type = 'category'
    #fig.layout.xaxis.rangeslider.visible = False    #fig.show()

def list_hist_squeeze_volume(data,symbol):
    for index, row in data.iterrows():
        if index < 2:
            continue

        if (row['volume'] > (3 * row['volume_20sma'])) and (row['volume'] > 2*row['volume_50sma']):
            print(f"{symbol}'s volume broke out on {row['date']}")

        if data['sqzOnNarrow'].iloc[index-2] and not row['sqzOnNarrow']:
            distance_to_upper = abs(row['upBB'] - row['close'])
            distance_to_lower = abs(row['lowBB'] - row['close'])

            if distance_to_upper < distance_to_lower:
                action = 'buy'
            else:
                action = 'sell'
            print(f"{symbol} exited squeeze on {row['date']}")

def list_symbols(mode=None, symbols=None):

    print('\n')

    if(mode=='in_squeeze'):
        msg=f'Symbols currently in a Squeeze:'

    elif(mode=='exiting_squeeze'):
        msg=f'Symbols currently exiting a Squeeze:'

    elif(mode=='volume_bo'):
        msg=f'Symbols currently breaking out in volume:'

    print(msg)

    for symbol in symbols:
        if(mode=='in_squeeze'):
            msg=f'{symbol} (In Squeeze)'

        elif(mode=='exiting_squeeze'):
            msg=f'{symbol} (Exiting Squeeze)'

        elif(mode=='volume_bo'):
            msg=f'{symbol} (Breaking Out)'
        print(msg)

    print('\n')

#symbol='NILKAMAL'
#df = dataframes[symbol]
#print(df)
#chart(df)

# list_symbols(symbols=symbols_all)
list_symbols(mode='in_squeeze', symbols=symbols_in_squeeze)
list_symbols(mode='exiting_squeeze', symbols=symbols_exiting_squeeze)
#list_hist_squeeze_volume(df, symbol)
#list_symbols(mode='in_squeeze', symbols=symbols_in_squeeze2)
#list_symbols(mode='exiting_squeeze', symbols=symbols_exiting_squeeze2)
list_symbols(mode='volume_bo', symbols=symbols_breaking_out)
