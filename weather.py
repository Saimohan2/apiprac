import requests
import pandas as pd
import time

records = []

url = "https://api.open-meteo.com/v1/forecast"

params = {
    'latitude': 17.3850,
    'longitude': 78.4867,
    'hourly': 'temperature_2m,relative_humidity_2m',
    'forecast_days': 7
}

response = requests.get(url, params = params)
status = response.status_code

data = response.json()

hourly = data['hourly']

time = hourly['time']
temp = hourly['temperature_2m']
humidity = hourly['relative_humidity_2m']

records = []

for i in range(len(time)):

    record = {
        'time': time[i],
        'temprature': temp[i],
        'humidity': humidity[i]
    }

    records.append(record)

weather = pd.DataFrame(records)

weather['time'] = pd.to_datetime(weather['time'])

print(weather.head(40))

weather.to_csv('cleaned_forecast.csv', index = False)