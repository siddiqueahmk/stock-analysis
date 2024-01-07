import os
from nsepython import equity_history, nse_quote
import pandas as pd
from datetime import datetime, timedelta

series = "EQ"

def get_start_date(end_date_str, num_months=15):
    end_date = pd.to_datetime(end_date_str, format='%d-%m-%Y')
    start_date = end_date - pd.DateOffset(months=num_months)
    start_date =  start_date.strftime("%d-%m-%Y")
    #print(f"#########{start_date}#############")
    return start_date

def download_equity_history(symbol, start_date, end_date):
    # Convert start_date and end_date to 'YYYY-MM-DD' format
    # start_date = pd.to_datetime(start_date).strftime("%d-%m-%Y")
    # end_date = pd.to_datetime(end_date).strftime("%d-%m-%Y")

    print(f"start_date={start_date}, end_date= {end_date}",end='\r')
    data = equity_history(symbol, series, start_date, end_date)
    if data.empty:
        return None
    columns = ['CH_OPENING_PRICE', 'CH_TRADE_HIGH_PRICE', 'CH_TRADE_LOW_PRICE', 'CH_CLOSING_PRICE', 'CH_TIMESTAMP', 'CH_TOT_TRADED_QTY']
    data = data[columns]

    # Rename columns for consistency with ta library
    data = data.rename(columns={
        'CH_OPENING_PRICE': 'open',
        'CH_TRADE_HIGH_PRICE': 'high',
        'CH_TRADE_LOW_PRICE': 'low',
        'CH_CLOSING_PRICE': 'close',
        'CH_TIMESTAMP': 'date',
        'CH_TOT_TRADED_QTY': 'volume'
    })
    #data['date'] = pd.to_datetime(data['date'])

    data = data.sort_values(by='date')
    return data

def update_dataset(symbol):
    # Read existing data from the file, if it exists
    file_path = "datasets/{}.csv".format(symbol)
    if os.path.exists(file_path):
        existing_data = pd.read_csv(file_path)

        # Find the last date available in the existing data
        last_date_str = pd.to_datetime(existing_data['date']).max().strftime('%d-%m-%Y')
        # Download only the missing data between the last date and the current date
        missing_data = download_equity_history(symbol, last_date_str, datetime.today().strftime("%d-%m-%Y"))
        print(missing_data)
        if missing_data is not None:
            # Concatenate existing data with the missing data and keep only the last 3 months
            combined_data = pd.concat([existing_data, missing_data])
            combined_data['date'] = pd.to_datetime(combined_data['date'])
            combined_data = combined_data.sort_values(by='date').drop_duplicates('date', keep='last')
            combined_data = combined_data[combined_data['date'] >= (combined_data['date'].max() - pd.DateOffset(months=15))]

            # Save the updated data back to the file
            combined_data.to_csv(file_path, index=False)
    else:
        end_date_str = datetime.today().strftime("%d-%m-%Y")

        # Download only the missing data between the last date and the current date
        data = download_equity_history(symbol, get_start_date(end_date_str), end_date_str)
        print(data)
        if data is not None:
            # If the file doesn't exist, save the new data directly
           data.to_csv(file_path, index=False)

def main():
    with open('symbols.csv') as f:
        lines = f.read().splitlines()
        for symbol in lines:
            print(symbol)
            #data=nse_quote(symbol)
            #print(data)
            update_dataset(symbol)

if __name__ == "__main__":
    main()

