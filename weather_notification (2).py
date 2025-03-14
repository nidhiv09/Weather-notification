import requests
from datetime import datetime
from plyer import notification
import schedule
import time

def get_weather(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json()

def check_rain(weather_data, target_time):
    for entry in weather_data['list']:
        forecast_time = datetime.fromtimestamp(entry['dt'])
        if forecast_time.strftime('%Y-%m-%d %H:%M') == target_time.strftime('%Y-%m-%d %H:%M'):
            if 'rain' in entry['weather'][0]['main'].lower():
                return True
    return False

def send_notification(message):
    notification.notify(
        title='Weather Alert',
        message=message,
        timeout=10
    )

def job():
    api_key = '5a8cffbef5085b5575be11fec9516bd0'
    city = 'Shivamogga'

    weather_data = get_weather(api_key, city)
    target_time = datetime.now().replace(hour=9, minute=30)
    notify_time = target_time.replace(minute=0)

    if check_rain(weather_data, target_time):
        send_notification("Hey, don't forget to carry an umbrella. There is a chance of rain at 9:30 AM.")

schedule.every().day.at("09:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
