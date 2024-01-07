import os
from nsepython import *
series = "EQ"
start_date = "01-12-2023"
end_date ="05-12-2023"
with open('symbols2.csv') as f:
    lines = f.read().splitlines()
    for symbol in lines:
        print(symbol)
        data=equity_history(symbol,series,start_date,end_date)
        if data.empty:
            continue
        columns = ['CH_OPENING_PRICE', 'CH_TRADE_HIGH_PRICE', 'CH_TRADE_LOW_PRICE', 'CH_CLOSING_PRICE', 'TIMESTAMP', 'CH_TOT_TRADED_QTY']
        data = data[columns]

	# Rename columns for consistency with ta library
        data = data.rename(columns={
        'CH_OPENING_PRICE': 'open',
        'CH_TRADE_HIGH_PRICE': 'high',
        'CH_TRADE_LOW_PRICE': 'low',
        'CH_CLOSING_PRICE': 'close',
        'mTIMESTAMP': 'date',
        'CH_TOT_TRADED_QTY': 'volume'
        })
        data = data.sort_values(by='date')
        data.to_csv("datasets/{}_out.csv".format(symbol))

