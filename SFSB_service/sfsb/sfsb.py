import asyncio

from apscheduler.schedulers.background import BackgroundScheduler
from playsound import playsound

import arduino
import cortex
import listeners
import weather
from global_variable import Config, Metrics


def weather_job():
    Metrics.current_weather = weather.get_weather("Busan,KR")


def feedback_job():
    if pow_listener.metric:
        print("집중")
        playsound(Config.config.get("Sounds.Ping"))
        controller.led_on()

    if met_listener.metric:
        print("흥분")
        playsound(Config.config.get("Sounds.Alert"))
        controller.led_on()


async def main():
    token, session = await api.prepare()
    await api.subscribe(token, session, ["pow", "met"])
    await asyncio.sleep(Config.config.get("App.Run_Time"))
    await api.unsubscribe(token, session, ["pow", "met"])


controller = arduino.SFSBClient(Config.config.get("Arduino.Port"))

api = cortex.Wrapper(client_id=Config.config.get("Emotiv.Client_ID"),
                     client_secret=Config.config.get("Emotiv.Client_Secret"),
                     main=main)

pow_listener = listeners.PowerListener()
met_listener = listeners.MetricListener()

api.register_listener(pow_listener)
api.register_listener(met_listener)

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(weather_job, "interval", minutes=5)
scheduler.add_job(feedback_job, "interval", seconds=3)