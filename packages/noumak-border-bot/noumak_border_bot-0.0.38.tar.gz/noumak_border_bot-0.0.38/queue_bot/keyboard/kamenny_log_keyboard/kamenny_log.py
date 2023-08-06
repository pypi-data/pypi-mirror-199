from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from queue_bot.middleware import _

__all__ = (
    "ikb_kamenny_log_bus",
    "ikb_kamenny_log_passenger",
    "ikb_kamenny_log_cargo",
    "ikb_kamenny_log_ts",
)


def ikb_kamenny_log_bus() -> InlineKeyboardMarkup:
    ikb_kamenny_log_bus = InlineKeyboardMarkup(row_width=2)
    ikb1 = InlineKeyboardButton(
        text=_("Место в очереди"), callback_data="kamenny_log_place_in_queue_bus"
    )
    ikb2 = InlineKeyboardButton(
        text=_("Длинна очереди"), callback_data="kamenny_log_queue_len_bus"
    )
    ikb3 = InlineKeyboardButton(
        text=_("Пропущено за час"), callback_data="kamenny_log_an_hour_bus"
    )
    ikb4 = InlineKeyboardButton(
        text=_("Пропущено за сутки"), callback_data="kamenny_log_an_day_bus"
    )
    ikb5 = InlineKeyboardButton(
        text=_("Назад ↩️"), callback_data="back_kamenny_log_bus"
    )
    ikb_kamenny_log_bus.add(ikb1, ikb2, ikb3, ikb4, ikb5)
    return ikb_kamenny_log_bus


def ikb_kamenny_log_passenger() -> InlineKeyboardMarkup:
    ikb_kamenny_log_passenger = InlineKeyboardMarkup(row_width=2)
    ikb1 = InlineKeyboardButton(
        text=_("Место в очереди"), callback_data="kamenny_log_place_in_queue_passenger"
    )
    ikb2 = InlineKeyboardButton(
        text=_("Длинна очереди"), callback_data="kamenny_log_queue_len_passenger"
    )
    ikb3 = InlineKeyboardButton(
        text=_("Пропущено за час"), callback_data="kamenny_log_an_hour_passenger"
    )
    ikb4 = InlineKeyboardButton(
        text=_("Пропущено за сутки"), callback_data="kamenny_log_an_day_passenger"
    )
    ikb5 = InlineKeyboardButton(
        text=_("Назад ↩️"), callback_data="back_kamenny_log_passenger"
    )
    ikb_kamenny_log_passenger.add(ikb1, ikb2, ikb3, ikb4, ikb5)
    return ikb_kamenny_log_passenger


def ikb_kamenny_log_cargo() -> InlineKeyboardMarkup:
    ikb_kamenny_log_cargo = InlineKeyboardMarkup(row_width=2)
    ikb1 = InlineKeyboardButton(
        text=_("Место в очереди"), callback_data="kamenny_log_place_in_queue_cargo"
    )
    ikb2 = InlineKeyboardButton(
        text=_("Длинна очереди"), callback_data="kamenny_log_queue_len_cargo"
    )
    ikb3 = InlineKeyboardButton(
        text=_("Пропущено за час"), callback_data="kamenny_log_an_hour_cargo"
    )
    ikb4 = InlineKeyboardButton(
        text=_("Пропущено за сутки"), callback_data="kamenny_log_an_day_cargo"
    )
    ikb5 = InlineKeyboardButton(
        text=_("Назад ↩️"), callback_data="back_kamenny_log_cargo"
    )
    ikb_kamenny_log_cargo.add(ikb1, ikb2, ikb3, ikb4, ikb5)
    return ikb_kamenny_log_cargo


def ikb_kamenny_log_ts() -> InlineKeyboardMarkup:
    ikb_kamenny_log_ts = InlineKeyboardMarkup(row_width=1)
    ikb1 = InlineKeyboardButton(text=_("Автобус 🚌"), callback_data="kamenny_log_bus")
    ikb2 = InlineKeyboardButton(
        text=_("Легковой транспорт 🚘"), callback_data="kamenny_log_passenger"
    )
    ikb3 = InlineKeyboardButton(
        text=_("Грузовой транспорт 🚛"), callback_data="kamenny_log_cargo"
    )
    ikb4 = InlineKeyboardButton(text=_("Назад ↩️"), callback_data="back_kamenny_log")
    ikb_kamenny_log_ts.add(ikb1, ikb2, ikb3, ikb4)
    return ikb_kamenny_log_ts
