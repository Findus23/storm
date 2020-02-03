import requests
import telegram
import yaml
from bs4 import BeautifulSoup

from config import telegram_token

try:
    with open("cache.yaml") as f:
        cache = yaml.safe_load(f)
except FileNotFoundError:
    cache = {}

with open("db.yaml") as f:
    db = yaml.safe_load(f)

s = requests.Session()

pretty_daynames = {"heute": "Heute", "morgen": "Morgen", "uebermorgen": "Übermorgen"}


def notify(text, prettyday):
    bot = telegram.Bot(token=telegram_token)
    message = f"🌩️🌪️🌀 ({prettyday})\n" + text
    for chat_id in db["subscribed"].keys():
        bot.sendMessage(chat_id=chat_id, text=message)


for day in pretty_daynames.keys():
    r = s.get(f'https://warnungen.zamg.at/html/de/{day}/wind/at/wien/wien_waehring/wien_waehring/')

    soup = BeautifulSoup(r.text, 'html.parser')
    warnings = [tag.get_text() for tag in soup.find_all("p", class_="warnung_text")]
    text = "\n".join(warnings)
    if day not in cache or text != cache[day]:
        if text:
            notify(text, pretty_daynames[day])
        cache[day] = text

with open("cache.yaml", "w") as f:
    yaml.safe_dump(cache, f)
