import requests
import pandas as pd
from datetime import datetime

url = "https://dummyjson.com/carts"

response = requests.get(url)

if response.status_code != 200:
    raise Exception (f"Connection Failed: {response.status_code}")

print(f"Status: {response.status_code}, Loading API Data")

data = response.json()['carts']

orders = []
order_items = []

load_time = datetime.utcnow()

for order in data:

    record = {
        'order_id': order['id'],
        'user_id': order.get('userId'),
        'unique_products': order.get('totalProducts'),
        'total_quantity': order.get('totalQuantity'),
        'order_total': float(order.get('total')) if order.get('total') else None,
        'discounted_total': float(order.get('discountedTotal')) if order.get('discountedTotal') else None,
        'loaded_at': load_time
    }

    orders.append(record)

    for p in order.get('products', []):
        record = {
            'order_id': order['id'],
            'product_id': p.get('id'),
            'product_name': p.get('title'),
            'price': float(p.get('price')) if p.get('price') else None,
            'item_quantity': int(p.get('quantity')) if p.get('quantity') else None,
            'item_total': float(p.get('total')) if p.get('total') else None,
            'discount_pct': p.get('discountPercentage'),
            'discounted_total': float(p.get('discountedTotal')) if p.get('discountedTotal') else None,
            'loaded_at': load_time
        }
    
        order_items.append(record)

print(f"Loaded {len(orders)} rows in orders")
print(f"Loaded {len(order_items)} rows in order_items")

orders_df = pd.DataFrame(orders)
order_items_df = pd.DataFrame(order_items)

print(orders_df.head())
print(order_items_df.head())