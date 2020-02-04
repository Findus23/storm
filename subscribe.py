import telegram
import yaml
from telegram import Message, User, Chat
from telegram.error import Unauthorized

from config import telegram_token

try:
    with open("db.yaml") as f:
        db = yaml.safe_load(f)
except FileNotFoundError:
    db = {"subscribed": {}, "last_update": 0}

bot = telegram.Bot(token=telegram_token)
for update in bot.get_updates(offset=db["last_update"] + 1):
    message: Message = update.message
    text = message.text
    user: User = update.effective_user
    chat: Chat = update.effective_chat
    if "/subscribe" in text:
        if chat.id in db["subscribed"]:
            bot.sendMessage(chat_id=chat.id,
                            text="Du bekommst bereits die Nachrichten. Verwende /unsubscribe zum Abmelden.")
        else:
            subscriber = {
                "first_name": chat.first_name,
                "last_name": chat.last_name,
                "username": chat.username,
            }
            db["subscribed"][chat.id] = subscriber
            bot.send_message(chat_id=chat.id,
                             text="Du bekommst nun regelmäßige Nachrichten. Verwende /unsubscribe zum Abmelden.")
    elif "/unsubscribe" in text:
        if chat.id in db["subscribed"]:
            del db["subscribed"][chat.id]
            bot.sendMessage(chat_id=chat.id,
                            text="Du bekommst keine Nachrichten mehr. Verwende /subscribe um sie wieder zu bekommen.")
        else:
            bot.sendMessage(chat_id=chat.id,
                            text="Du bekommst bereits keine Nachrichten. Verwende /subscribe um sie wieder zu bekommen.")
    elif "/start" in text or "/help" in text:
        try:
            bot.sendMessage(chat_id=chat.id,
                            text="Verwende /subscribe um regelmäßige Nachrichten zu bekommen. Mit /unsubscribe kannst du dich wieder abmelden. "
                                 "Es kann bis zu 5 Minuten dauern, bis eine Bestätigung kommt.")
        except Unauthorized:
            pass
    db["last_update"] = update.update_id

with open("db.yaml", "w") as f:
    yaml.safe_dump(db, f)
