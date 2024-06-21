from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import API


def pay_btn(lang: str):
    markup = InlineKeyboardBuilder()
    if lang == 'uz':
        markup.button(text="Тўлаш", pay=True)
    else:
        markup.button(text="Оплата", pay=True)
    markup.button(text="❌", callback_data="❌")
    return markup.as_markup()


def back_btn(lang: str):
    if lang == 'uz':
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="🔙 Ортга")
                ]
            ],
            resize_keyboard=True,
        )
    else:
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="🔙 Назад")
                ]
            ],
            resize_keyboard=True
        )
    return markup


def main_btn(lang: str, tg_id: int):
    if lang == 'uz':
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🖋 МАВЗУЛАР РЎЙХАТИ", web_app=WebAppInfo(url=f"{API}/themes/{tg_id}/?lang=uz"))],
                [KeyboardButton(text="🗓 Обунани активлаштиринг")],
                [
                    KeyboardButton(text="✍️ Мурожат қилинг!"),
                    KeyboardButton(text="Маълумотлар!", web_app=WebAppInfo(url=f"{API}/about?lang=uz")),
                ],
                [
                    KeyboardButton(text="🔄 Тилни алмаштириш")
                ]
            ],
            resize_keyboard=True
        )
    else:
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🖋 СПИСОК ТЕМ", web_app=WebAppInfo(url=f"{API}/themes/{tg_id}/?lang=ru"))],
                [KeyboardButton(text="🗓 Активируйте подписку")],
                [
                    KeyboardButton(text="✍️ Обращайтесь!"),
                    KeyboardButton(text="Информации!", web_app=WebAppInfo(url=f"{API}/about?lang=ru")),
                ],
                [
                    KeyboardButton(text="🔄 Изменение языка")
                ]
            ],
            resize_keyboard=True
        )
    return markup


lang_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 Ўзбек тили", callback_data="uz"),
            InlineKeyboardButton(text="🇷🇺 Русский язык", callback_data="ru"),
        ]
    ]
)


def phone_btn(lang: str):
    if lang == 'uz':
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="📞 Телефон рақамни юбориш", request_contact=True)
                ]
            ],
            resize_keyboard=True
        )
    else:
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="📞 Отправить номер телефона", request_contact=True)
                ]
            ],
            resize_keyboard=True
        )
    return markup
