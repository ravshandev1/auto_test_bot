import logging
import requests
from dotenv import dotenv_values
from aiogram import Bot

ENV = dotenv_values(".env")

BOT_TOKEN = ENV["BOT_TOKEN"]
ADMIN = ENV["ADMIN"]
API = ENV["API"]

bot = Bot(token=BOT_TOKEN, parse_mode='HTML')

users = list()


def set_users(ls: list):
    global users
    users = ls


def append_user(data: dict):
    global users
    r = requests.get(url=f"{API}/")
    try:
        users = r.json()
    except Exception as e:
        logging.exception(e)
    users.append(data)


def get_user_lang(telegram_id: int) -> str:
    global users
    if len(users) == 0:
        r = requests.get(url=f"{API}/")
        try:
            users = r.json()
        except Exception as e:
            logging.exception(e)
    for user in users:
        if telegram_id == user['telegram_id']:
            return user['lang']
    return 'ru'
