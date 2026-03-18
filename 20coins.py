import pandas as pd

rawcoins = pd.read_csv('20coins.csv')
rawcoins = rawcoins.drop(columns = ['Unnamed: 0'])
rawcoins['max_supply'] = rawcoins['max_supply'].fillna(0)
rawcoins['max_supply'] = rawcoins['max_supply'].astype('int64')
rawcoins['total_supply'] = rawcoins['total_supply'].astype('int64')
rawcoins['circulating_supply'] = rawcoins['circulating_supply'].astype('int64')
rawcoins['ath_date'] = pd.to_datetime(rawcoins['ath_date']).dt.date
rawcoins['symbol'] = rawcoins['symbol'].str.strip().str.upper()

rawcoins.to_csv('cleaned_coins.csv', index = False)