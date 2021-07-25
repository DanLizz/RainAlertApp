import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient


OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
weather_params = {
    "appid": "xxxxxxxxx",
    "lat": xxxxxxxxx,
    "lon": xxxxxxxxx,
    "exclude": "current,minutely,daily",
    }
will_rain = False

account_sid = "xxxxxxxxx"
auth_token = "xxxxxxxxx"


response = requests.get(OWM_Endpoint, params=weather_params)
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]
for hour_data in weather_slice:
    hourly = hour_data["weather"][0]["id"]
    rain = hourly < 600
    if rain:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ["https_proxy"]}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
                    .create(
                         body="It's going to rain today 🌧️ , Remember to take an umbrella ☂️",
                         from_='+1xxxxxxxxx',
                         to='+1xxxxxxxxx'
                     )

print(message.status)
