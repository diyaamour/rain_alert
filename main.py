# One Call Api is no longer provided for free accounts on openweathermap

import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient


OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
# OWM_Endpoint = "https://api.openweathermap.org/data/2.5/weather"
api_key = os.environ.get("OWM_API_KEY")
account_sid = "ACcfdd99d9e1b3cbce3b1a1bd20ee391fd"
auth_token = os.environ.get("AUTH_TOKEN")


weather_params = {
    "lat": 39.044660,
    "lon": -77.390690,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
print(weather_data["hourly"])
weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages.create(
        body="It's going to rain today. Bring an umbrella ☔️",
        from_='+15044144801',
        to='+12026707145'
    )
    print(message.status)

