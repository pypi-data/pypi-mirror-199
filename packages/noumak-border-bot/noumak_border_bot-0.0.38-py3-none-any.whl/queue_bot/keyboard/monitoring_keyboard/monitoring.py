from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from queue_bot.middleware import _

__all__ = (
    "ikb_monitoring",
    "ikb_monitoring_intensity",
    "ikb_monitoring_conf",
    "ikb_monitoring_ts",
    "ikb_back_monitoring",
    "ikb_monitoring_close",
    "ikb_monitoring_back_menu",
)


def ikb_monitoring() -> InlineKeyboardMarkup:
    ikb_monitoring = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    ikb1 = InlineKeyboardButton(
        text=_("Как это работает ❓"), callback_data="help_monitoring"
    )
    ikb2 = InlineKeyboardButton(text=_("Подключить"), callback_data="add_m")
    ikb3 = InlineKeyboardButton(text=_("Отключить"), callback_data="close_m")
    ikb4 = InlineKeyboardButton(text=_("Назад ↩️"), callback_data="back_menu")
    ikb_monitoring.add(ikb1)
    ikb_monitoring.add(ikb2, ikb3)
    ikb_monitoring.add(ikb4)
    return ikb_monitoring


def ikb_monitoring_ts() -> InlineKeyboardMarkup:
    ikb_monitoring_ts = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    ikb1 = InlineKeyboardButton(text=_("Автобус🚌"), callback_data="bus_m")
    ikb2 = InlineKeyboardButton(text=_("Легковой🚘"), callback_data="passenger_m")
    ikb3 = InlineKeyboardButton(text=_("Грузовой🚛"), callback_data="cargo_m")
    ikb4 = InlineKeyboardButton(text=_("Отмена ↩️"), callback_data="back_monitoring")
    ikb_monitoring_ts.add(ikb1, ikb2, ikb3, ikb4)
    return ikb_monitoring_ts


def ikb_monitoring_intensity() -> InlineKeyboardMarkup:
    ikb_monitoring_intensity = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    ikb1 = InlineKeyboardButton(text=_("Каждую машину"), callback_data="intensity_1")
    ikb2 = InlineKeyboardButton(text=_("Каждые 5 машин"), callback_data="intensity_5")
    ikb3 = InlineKeyboardButton(text=_("Каждые 10 машин"), callback_data="intensity_10")
    ikb4 = InlineKeyboardButton(text=_("Каждые 20 машин"), callback_data="intensity_20")
    ikb5 = InlineKeyboardButton(text=_("Каждые 50 машин"), callback_data="intensity_50")
    ikb6 = InlineKeyboardButton(text=_("Отмена ↩️"), callback_data="back_monitoring")
    ikb_monitoring_intensity.add(ikb5, ikb4)
    ikb_monitoring_intensity.add(ikb3)
    ikb_monitoring_intensity.add(ikb2, ikb1)
    ikb_monitoring_intensity.add(ikb6)
    return ikb_monitoring_intensity


def ikb_monitoring_conf() -> InlineKeyboardMarkup:
    ikb_monitoring_conf = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    ikb1 = InlineKeyboardButton(text=_("Подключить мониторинг"), callback_data="reg_m")
    ikb2 = InlineKeyboardButton(text=_("Отмена ↩️"), callback_data="back_monitoring")
    ikb_monitoring_conf.add(ikb1, ikb2)
    return ikb_monitoring_conf


def ikb_back_monitoring() -> InlineKeyboardMarkup:
    ikb_back_monitoring = InlineKeyboardMarkup(resize_keyboard=True)
    ikb1 = InlineKeyboardButton(text=_("Назад ↩️"), callback_data="back_monitoring")
    ikb_back_monitoring.add(ikb1)
    return ikb_back_monitoring


def ikb_monitoring_close() -> InlineKeyboardMarkup:
    ikb_monitoring_close = InlineKeyboardMarkup(resize_keyboard=True)
    ikb1 = InlineKeyboardButton(text=_("Отключить мониторинг"), callback_data="close_m")
    ikb_monitoring_close.add(ikb1)
    return ikb_monitoring_close


def ikb_monitoring_back_menu() -> InlineKeyboardMarkup:
    ikb_monitoring_back_menu = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True
    )
    kb1 = KeyboardButton(text="Главное меню")
    ikb_monitoring_back_menu.add(kb1)
    return ikb_monitoring_back_menu
