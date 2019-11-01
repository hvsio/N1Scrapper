import configparser
import requests
import schedule
import time
from datetime import datetime


def update_timout():
    global timeout

    # get timeout from config
    config = configparser.ConfigParser()
    config.read('scheduler_config.cfg')
    timeout = int(config.get("timeout", "run_every_x_seconds"))

    schedule.clear()
    schedule.every(timeout).seconds.do(job)
    print(f"Operation done successfully, new timeout: {timeout}")


def send_request_scrap():
    requests.get('http://127.0.0.1:8001/scrapper')


def job():
    print(f'Starting new scrapping session at {datetime.now()}... timeout = {timeout}')
    send_request_scrap()
    update_timout()


print('Press Ctrl+C to stop scheduler... ')
timeout = 15
schedule.every(timeout).seconds.do(job)
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print('Scheduler stopping... ')
