from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import pandas as pd
import openmeteo_requests
import requests_cache
from retry_requests import retry


cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

#измените на свои каардинаты и часовой пояс
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 59.1333,
    "longitude": 37.9,
    "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "precipitation", "rain", "snowfall", "wind_speed_10m"],
    "timezone": "Europe/Moscow"
}
responses = openmeteo.weather_api(url, params=params)

# Обработка первого ответа
response = responses[0]
current = response.Current()

current_temperature_2m = current.Variables(0).Value()
current_relative_humidity_2m = current.Variables(1).Value()
current_apparent_temperature = current.Variables(2).Value()
current_precipitation = current.Variables(3).Value()
current_rain = current.Variables(4).Value()
current_snowfall = current.Variables(5).Value()
current_wind_speed_10m = current.Variables(6).Value()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Я бот для отображения погоды в Череповце. Напишите /pogoda")

async def pogoda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Текущая температура: {current_temperature_2m}°C")
    await update.message.reply_text(f"Относительная влажность: {current_relative_humidity_2m}%")
    await update.message.reply_text(f"Ощущаемая температура: {current_apparent_temperature}°C")
    await update.message.reply_text(f"Осадки: {current_precipitation} мм")
    await update.message.reply_text(f"Дождь: {current_rain} мм")
    await update.message.reply_text(f"Снег: {current_snowfall} мм")
    await update.message.reply_text(f"Скорость ветра: {current_wind_speed_10m} м/с")
    
    print[a]
def main():
    app = ApplicationBuilder().token('токен бота').build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pogoda", pogoda))

    app.run_polling()

if __name__ == '__main__':
    main()
