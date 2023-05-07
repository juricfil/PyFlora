import http.client
from ast import literal_eval
import pandas as pd

conn = http.client.HTTPSConnection("api.open-meteo.com")
conn.request('GET', "/v1/forecast?latitude=45.81&longitude=15.98&hourly=temperature_2m")
result = conn.getresponse()
data = literal_eval(result.read().decode('utf-8'))

rounded_time = str(pd.Timestamp.now().round('60min').to_pydatetime())
rounded_time_str = str(rounded_time)[0:-3]


for date, temperature in zip(data['hourly']['time'],data['hourly']['temperature_2m']):
    if date.replace('T',' ') == rounded_time_str:
        current_temp = temperature
