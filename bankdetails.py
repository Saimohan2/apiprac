import requests
import pandas as pd

URL = "https://dummyjson.com/users"

response = requests.get(URL, timeout = 10)

users = response.json().get("users", [])

user_data = []

for user in users:

    userid = user.get("id")

    if userid is None:
        continue

    age = user.get("age")
    address = user.get("address", {})
    lat = address.get("coordinates", {}).get("lat")
    lon = address.get("coordinates", {}).get("lng")
    bank = user.get("bank", {})

    user_data.append({
        "user_id": userid,
        "user_name": user.get("username"),
        "age": int(age) if age else None,
        "city": address.get("city"),
        "latitude": float(lat) if lat else None,
        "longitude": float(lon) if lon else None,
        "currency": bank.get("currency") #commit
    })

print(user_data[:3])

users_df = pd.DataFrame(user_data)
print(users_df.head())