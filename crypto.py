import requests
import pandas as pd
import time

needed = []
page = 1
max_pages = 2

while page<=max_pages:
        
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 10,
        'page': page
    }
    url = "https://api.coingecko.com/api/v3/coins/markets"
    response = requests.get(url, params = params)
    print(f"Status: {response.status_code}")
    
    max_retries = 5
    for attempt in range(5):

        if response.status_code == 200:
            break
        elif response.status_code == 429:
            wait_time = 2 ** attempt
            print("Rate Limited. Waiting...")
            time.sleep(wait_time)
        else:
            print("Error: ", response.status_code)
            break
    
    if response.status_code != 200:
        print('Failed after retries!!')
        break

    data = response.json()

    if isinstance(data, dict):
        print("Error response:", data)
        break

    if not data:
        break

    for coin in data:

        record = {
            'name': coin.get('name'),
            'symbol': coin.get('symbol'),
            'current_price': coin.get('current_price'),
            'market_cap': coin.get('market_cap'),
            'circulating_supply': coin.get('circulating_supply'),
            'total_supply': coin.get('total_supply'),
            'max_supply': coin.get('max_supply'),
            'alltime_high': coin.get('ath'),
            'ath_date': coin.get('ath_date')
        }

        needed.append(record)

    print(f"Fetched page {page}, records: {len(data)}")
    
    page += 1
    time.sleep(6)

coins = pd.DataFrame(needed)

print(coins.head())

coins.to_csv('20coins.csv')