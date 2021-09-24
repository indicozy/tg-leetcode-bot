import requests
from telegram import ParseMode
import json
from typing import Tuple, Dict, Any, Optional
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Bot
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
import logging
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler,
    CallbackContext,
    ChatMemberHandler,
)
from telegram import Update, Chat, ChatMember, ParseMode, ChatMemberUpdated, KeyboardButtonPollType, Poll, KeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    PollAnswerHandler,
    PollHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)
from telegram.utils import helpers

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

CHAT_ID = -1001386280522

def get_db() -> list():
    url = 'https://leetcode-rating.herokuapp.com/rating'
    r = requests.get(url)
    db = r.json()
    return db

def get_token () -> str:
    with open ("token.txt", "r") as myfile:
        # FUCK YOU HACKERS
        token=myfile.read().replace('\n', '')
    return token

def get_text(n_min = 0, n_max = None) -> str:
    db = get_db()
    response = ""
    
    if n_max == None:
        n_max = len(db)

    for i in db[n_min:n_max]:
        response += f"{i['username']}: {i['score']}\n"

    return response

def select_tail(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    chat = update.effective_chat
    text = update.message.text

    if chat.id != CHAT_ID:
        return

    response = get_text(n_min = -11)
    response += '\nЕсли ты в списке, то иди чаль прогу'

    update.message.reply_text(response)
    return

def select_top(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    chat = update.effective_chat
    text = update.message.text

    if chat.id != CHAT_ID:
        return

    response = get_text(n_min = 0, n_max = 11)
    response += '\nЕсли ты не в списке, то иди чаль прогу'
    update.message.reply_text(response)
    return

def select_me(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    chat = update.effective_chat
    text = update.message.text

    if chat.id != CHAT_ID:
        return

    if len(text.split(' ')) != 2:
        update.message.reply_text("""Брух, есімің кім?\n\n/me <LEETCODE username>""")
        return

    db = get_db()
    leetcode_username = text.split(' ')[1]

    for i in db:
        if leetcode_username.lower() == i['username'].lower():
            update.message.reply_text(f"{i['username']}: {i['score']}\n\nЯ не холодильник, каждый раз открывая ничего не появится. Иди чаль прогу")
            return

    update.message.reply_text("Не нашел.\nЕсли не нашел значит не чалишь. Иди чаль прогу")
    return

def select_stats(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    chat = update.effective_chat
    text = update.message.text

    if chat.id != CHAT_ID:
        return

    if '-y' not in text.split(' ')[:3]:
        update.message.reply_text("""Братиш, где -y? ты что хочешь всех заспамить огромным текстом?

Лучше напиши /top или /me <username>""")
        return

    update.message.reply_text(get_text())
    return


def main() -> None:
    updater = Updater(get_token()) # liberobot
    dispatcher = updater.dispatcher
    logs_handlers = [
#        CommandHandler("stats", select_stats, Filters.chat_type.groups),
        CommandHandler("top", select_top, Filters.chat_type.groups),
        CommandHandler("tail", select_tail, Filters.chat_type.groups),
        CommandHandler("me", select_me, Filters.chat_type.groups),
        ]

    for i in logs_handlers:
       dispatcher.add_handler(i)

    updater.start_polling(allowed_updates=Update.ALL_TYPES)
    updater.idle()

    return

if __name__ == '__main__':
    # print(get_db())
    main()
