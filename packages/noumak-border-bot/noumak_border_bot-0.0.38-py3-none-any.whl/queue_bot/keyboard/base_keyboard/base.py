from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from queue_bot.middleware import _

__all__ = (
    "ikb_menu",
    "ikb_main",
    "ikb_poland",
    "ikb_lithuania",
    "ikb_latvia",
    "ikb_tiket",
    "ikb_admin",
    "ikb_back_help",
    "ikb_lk",
    "ikb_lk_add_number",
    "ikb_lk_edit_number",
    "ikb_lk_del_number",
    "ikb_lk_back",
    "ikb_language",
)


def ikb_language() -> InlineKeyboardMarkup:
    ikb_language = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    ikb1 = InlineKeyboardButton(text="Русский 🇷🇺", callback_data="ru")
    ikb2 = InlineKeyboardButton(text="English 🇺🇸", callback_data="en")
    ikb3 = InlineKeyboardButton(text="Poland 🇵🇱", callback_data="pl")
    ikb_language.add(ikb1, ikb2, ikb3)
    return ikb_language


def ikb_menu() -> InlineKeyboardMarkup:
    ikb_menu = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    ikb1 = InlineKeyboardButton(text=_("Пункты пропуска 🏢"), callback_data="checkpoint")
    ikb2 = InlineKeyboardButton(text=_("Личный кабинет 👤"), callback_data="lk")
    ikb3 = InlineKeyboardButton(text=_("Мониторинг 🔔"), callback_data="monitoring")
    ikb_menu.add(ikb1, ikb2, ikb3)
    return ikb_menu


def ikb_main() -> InlineKeyboardMarkup:
    ikb_main = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    ikb1 = InlineKeyboardButton(text=_("Польша 🇵🇱"), callback_data="poland")
    ikb2 = InlineKeyboardButton(text=_("Литва 🇱🇹"), callback_data="lithuania")
    ikb3 = InlineKeyboardButton(text=_("Латвия 🇱🇻"), callback_data="latvia")
    ikb4 = InlineKeyboardButton(text=_("Назад ↩️"), callback_data="back_menu")
    ikb_main.add(ikb1)
    ikb_main.add(ikb3, ikb2)
    ikb_main.add(ikb4)
    return ikb_main


def ikb_poland() -> InlineKeyboardMarkup:
    ikb_poland = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    ikb1 = InlineKeyboardButton(text=_("Берестовица"), callback_data="berestovitsa")
    ikb2 = InlineKeyboardButton(text=_("Брест"), callback_data="brest")
    ikb3 = InlineKeyboardButton(text=_("Назад ↩️"), callback_data="back_state")
    ikb_poland.add(ikb1, ikb2, ikb3)
    return ikb_poland


def ikb_lithuania() -> InlineKeyboardMarkup:
    ikb_lithuania = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    ikb1 = InlineKeyboardButton(text=_("Котловка"), callback_data="kotlovka")
    ikb2 = InlineKeyboardButton(text=_("Каменный Лог"), callback_data="kamenny_log")
    ikb3 = InlineKeyboardButton(text=_("Бенякони"), callback_data="beniakoni")
    ikb4 = InlineKeyboardButton(text=_("Назад ↩️"), callback_data="back_state")
    ikb_lithuania.add(ikb1, ikb2, ikb3)
    ikb_lithuania.add(ikb4)
    return ikb_lithuania


def ikb_latvia() -> InlineKeyboardMarkup:
    ikb_latvia = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    ikb1 = InlineKeyboardButton(text=_("Григоровщина"), callback_data="grigorovshcina")
    ikb2 = InlineKeyboardButton(text=_("Урбаны"), callback_data="urbany")
    ikb3 = InlineKeyboardButton(text=_("Назад ↩️"), callback_data="back_state")
    ikb_latvia.add(ikb1, ikb2, ikb3)
    return ikb_latvia


def ikb_back_help() -> InlineKeyboardMarkup:
    ikb_back_help = InlineKeyboardMarkup()
    ikb1 = InlineKeyboardButton(text=_("Назад ↩️"), callback_data="back_help")
    ikb_back_help.add(ikb1)
    return ikb_back_help


def ikb_tiket() -> InlineKeyboardMarkup:
    ikb_tiket = InlineKeyboardMarkup(row_width=1)
    ikb1 = InlineKeyboardButton(
        text=_("Чат поддержки ✉️"),
        callback_data="tiket",
        url="https://t.me/+d5bX4AX0hQtkZmRi",
    )
    ikb2 = InlineKeyboardButton(text=_("Назад ↩️"), callback_data="back_help")
    ikb_tiket.add(ikb1, ikb2)
    return ikb_tiket


def ikb_admin() -> InlineKeyboardMarkup:
    ikb_admin = InlineKeyboardMarkup(row_width=2)
    ikb1 = InlineKeyboardButton(text="Рассылка", callback_data="mailing")
    ikb2 = InlineKeyboardButton(text="Выдать админку", callback_data="admin_add")
    ikb3 = InlineKeyboardButton(text="Назад ↩️", callback_data="back_menu")
    ikb_admin.add(ikb1, ikb2, ikb3)
    return ikb_admin


def ikb_lk() -> InlineKeyboardMarkup:
    ikb_lk = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    ikb1 = InlineKeyboardButton(text=_("Добавить номер"), callback_data="add_number")
    ikb2 = InlineKeyboardButton(text=_("Изменить номер"), callback_data="edit_number")
    ikb3 = InlineKeyboardButton(text=_("Удалить номер"), callback_data="del_number")
    ikb4 = InlineKeyboardButton(
        text=_("Отслеживаемые т/с"), callback_data="show_number"
    )
    ikb5 = InlineKeyboardButton(text=_("Назад ↩️"), callback_data="back_menu")
    ikb_lk.add(ikb1, ikb2)
    ikb_lk.add(ikb3, ikb4)
    ikb_lk.add(ikb5)
    return ikb_lk


def ikb_lk_add_number() -> InlineKeyboardMarkup:
    ikb_lk_add_number = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    ikb1 = InlineKeyboardButton(text=_("Добавить автобус 🚌"), callback_data="add_bus")
    ikb2 = InlineKeyboardButton(
        text=_("Добавить легковую 🚘"), callback_data="add_passenger"
    )
    ikb3 = InlineKeyboardButton(
        text=_("Добавить грузовую 🚛"), callback_data="add_cargo"
    )
    ikb4 = InlineKeyboardButton(text=_("Назад ↩️"), callback_data="back_lk")
    ikb_lk_add_number.add(ikb1)
    ikb_lk_add_number.add(ikb2)
    ikb_lk_add_number.add(ikb3)
    ikb_lk_add_number.add(ikb4)
    return ikb_lk_add_number


def ikb_lk_edit_number() -> InlineKeyboardMarkup:
    ikb_lk_edit_number = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    ikb1 = InlineKeyboardButton(text=_("Изменить автобус 🚌"), callback_data="edit_bus")
    ikb2 = InlineKeyboardButton(
        text=_("Изменить легковую 🚘"), callback_data="edit_passenger"
    )
    ikb3 = InlineKeyboardButton(
        text=_("Изменить грузовую 🚛"), callback_data="edit_cargo"
    )
    ikb4 = InlineKeyboardButton(text=_("Назад ↩️"), callback_data="back_lk")
    ikb_lk_edit_number.add(ikb1)
    ikb_lk_edit_number.add(ikb2)
    ikb_lk_edit_number.add(ikb3)
    ikb_lk_edit_number.add(ikb4)
    return ikb_lk_edit_number


def ikb_lk_del_number() -> InlineKeyboardMarkup:
    ikb_lk_del_number = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    ikb1 = InlineKeyboardButton(text=_("Удалить автобус 🚌"), callback_data="del_bus")
    ikb2 = InlineKeyboardButton(
        text=_("Удалить легковую 🚘"), callback_data="del_passenger"
    )
    ikb3 = InlineKeyboardButton(text=_("Удалить грузовую 🚛"), callback_data="del_cargo")
    ikb4 = InlineKeyboardButton(
        text=_("Удалить все номера"), callback_data="del_numbers"
    )
    ikb5 = InlineKeyboardButton(text=_("Назад ↩️"), callback_data="back_lk")
    ikb_lk_del_number.add(ikb1, ikb2)
    ikb_lk_del_number.add(ikb3, ikb4)
    ikb_lk_del_number.add(ikb5)
    return ikb_lk_del_number


def ikb_lk_back() -> InlineKeyboardMarkup:
    ikb_lk_back = InlineKeyboardMarkup()
    ikb1 = InlineKeyboardButton(text=_("Назад ↩️"), callback_data="back_lk")
    ikb_lk_back.add(ikb1)
    return ikb_lk_back
