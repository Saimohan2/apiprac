import requests
import pandas as pd

url = "https://jsonplaceholder.typicode.com/users"

response = requests.get(url)

data = response.json()

records = []

for row in data:

    address = row.get('address', {})
    geo = address.get('geo', {})
    company = row.get('company', {})

    record = {
        'id': row['id'],
        'name': row.get('name'),
        'user_name': row.get('username'),
        'email': row.get('email'),
        'phone': row.get('phone'),
        'street': address.get('street'),
        'zipcode': address.get('zipcode'),
        'city': address.get('city'),
        'latitude': geo.get('lat'),
        'longitude': geo.get('lng'),
        'company_name': company.get('name'),
        'company_bs': company.get('bs')
    }

    records.append(record)

details = pd.DataFrame(records)

print(details.head())