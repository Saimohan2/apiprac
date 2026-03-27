import requests
import pandas as pd

url = "https://dummyjson.com/carts"

response = requests.get(url, timeout = 10)

if response.status_code != 200:
    raise Exception(f"API Failed with status code: {response.status_code}")

try:
    data = response.json().get('carts', [])
except Exception as e:
    print("JSON parse failed")

orders = []
order_items = []

for row in data:

    total = row.get("total")
    discounted_price = row.get("discountedTotal")
    uniqprod = row.get("totalProducts")
    order_quantity = row.get("totalQuantity")

    orders.append({
        "order_id": row.get("id"),
        "user_id": row.get("userId"),
        "total_order_price": float(total) if total else None,
        "discounted_order_price": float(discounted_price) if discounted_price else None,
        "unq_items": int(uniqprod) if uniqprod else None,
        "order_quantity": int(order_quantity) if order_quantity else None
    })
    
    for product in row.get("products", []):

        price = product.get("price")
        quantity = product.get("quantity")
        itotal = product.get("total")
        discountedtotal = product.get("discountedTotal")

        order_items.append({
            "order_id": row.get("id"),
            "item_id": product.get("id"),
            "item_name": product.get("title"),
            "price": float(price) if price else None,
            "item_quantity": int(quantity) if quantity else None,
            "item_total": float(itotal) if itotal else None,
            "discounted_item_total": float(discountedtotal) if discountedtotal else None
        })

orders_df = pd.DataFrame(orders)
order_items_df = pd.DataFrame(order_items)

print(orders_df.head())
print(order_items_df.head())