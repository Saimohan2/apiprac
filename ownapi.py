import requests
import pandas as pd
import time

records = []
page = 0
max_pages = 3

while page<max_pages:

    url = "https://www.cheapshark.com/api/1.0/deals?"

    params = {
        'storeID': 1,
        'pageNumber': page,
        'pageSize': 50
    }

    max_tries = 3
    success = False

    for i in range(max_tries):

        response = requests.get(url, params = params, timeout = 10)

        if response.status_code == 200:
            success = True
            print(f"Connection good. Adding more rows✅")
            break
        elif response.status_code == 429:
            print(f"Rate Limit Reached: {response.status_code} 🛑")
            time.sleep(5)
        else:
            print('Error: ', response.status_code)

    if not success:
        print(f"Page {page} Gracefully Failed After Multiple Retries")
        page += 1
        continue

    try:
        data = response.json()
    except Exception as e:
        print(f"[Page {page}] JSON Parse Failed {e}")
        page += 1
        continue

    if not data:
        break

    for row in data:

        record = {
            'internal_name': row.get('internalName'),
            'title': row.get('title'),
            'deal_id': row.get('dealId'),
            'game_id': row.get('gameID'),
            'store_id': row.get('storeID'),
            'sale_price': float(row.get('salePrice')) if row.get('salePrice') else None,
            'normal_price': float(row.get('normalPrice')) if row.get('normalPrice') else None,
            'is_on_sale': int(row.get('isOnSale')) if row.get('isOnSale') else None,
            'rating': row.get('steamRatingText'),
            'rating_pct': float(row.get('steamRatingPercent')) if row.get('steamRatingPercent') else None,
            'ratings': int(row.get('steamRatingCount')) if row.get('steamRatingCount') else None
        }

        records.append(record)

    print(f"Total Rows Loaded: {len(records)}")

    page += 1
    time.sleep(5)

print('Data Loaded Successfully 🔥')

deals = pd.DataFrame(records)
print(deals.tail())

deals.to_csv('game_deals.csv', index = False)