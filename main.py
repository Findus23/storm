import json

import requests
import telegram
from bs4 import BeautifulSoup

from config import telegram_token, telegram_chat_id

try:
    with open("cache.json") as f:
        cache = json.load(f)
except FileNotFoundError:
    cache = {}

s = requests.Session()


def notify(text):
    print(text)
    bot = telegram.Bot(token=telegram_token)
    message = "🌩️🌪️🌀\n" + text
    bot.sendMessage(chat_id=telegram_chat_id, text=message)


for day in ["heute", "morgen", "uebermorgen"]:
    r = s.get(f'https://warnungen.zamg.at/html/de/{day}/wind/at/wien/wien_waehring/wien_waehring/')

    soup = BeautifulSoup(r.text, 'html.parser')
    warnings = [tag.get_text() for tag in soup.find_all("p", class_="warnung_text")]
    text = "\n".join(warnings)
    if day not in cache or text != cache[day]:
        # if text:
        notify(text)
        cache[day] = text
    print(text)

with open("cache.json", "w") as f:
    json.dump(cache, f)
