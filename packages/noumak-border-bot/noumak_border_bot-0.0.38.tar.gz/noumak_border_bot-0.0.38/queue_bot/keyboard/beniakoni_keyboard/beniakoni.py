from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from queue_bot.middleware import _

__all__ = (
    "ikb_beniakoni_bus",
    "ikb_beniakoni_passenger",
    "ikb_beniakoni_cargo",
    "ikb_beniakoni_ts",
)


def ikb_beniakoni_bus() -> InlineKeyboardMarkup:
    ikb_beniakoni_bus = InlineKeyboardMarkup(row_width=2)
    ikb1 = InlineKeyboardButton(
        text=_("Место в очереди"), callback_data="beniakoni_place_in_queue_bus"
    )
    ikb2 = InlineKeyboardButton(
        text=_("Длинна очереди"), callback_data="beniakoni_queue_len_bus"
    )
    ikb3 = InlineKeyboardButton(
        text=_("Пропущено за час"), callback_data="beniakoni_an_hour_bus"
    )
    ikb4 = InlineKeyboardButton(
        text=_("Пропущено за сутки"), callback_data="beniakoni_an_day_bus"
    )
    ikb5 = InlineKeyboardButton(text=_("Назад ↩️"), callback_data="back_beniakoni_bus")
    ikb_beniakoni_bus.add(ikb1, ikb2, ikb3, ikb4, ikb5)
    return ikb_beniakoni_bus


def ikb_beniakoni_passenger() -> InlineKeyboardMarkup:
    ikb_beniakoni_passenger = InlineKeyboardMarkup(row_width=2)
    ikb1 = InlineKeyboardButton(
        text=_("Место в очереди"), callback_data="beniakoni_place_in_queue_passenger"
    )
    ikb2 = InlineKeyboardButton(
        text=_("Длинна очереди"), callback_data="beniakoni_queue_len_passenger"
    )
    ikb3 = InlineKeyboardButton(
        text=_("Пропущено за час"), callback_data="beniakoni_an_hour_passenger"
    )
    ikb4 = InlineKeyboardButton(
        text=_("Пропущено за сутки"), callback_data="beniakoni_an_day_passenger"
    )
    ikb5 = InlineKeyboardButton(
        text=_("Назад ↩️"), callback_data="back_beniakoni_passenger"
    )
    ikb_beniakoni_passenger.add(ikb1, ikb2, ikb3, ikb4, ikb5)
    return ikb_beniakoni_passenger


def ikb_beniakoni_cargo() -> InlineKeyboardMarkup:
    ikb_beniakoni_cargo = InlineKeyboardMarkup(row_width=2)
    ikb1 = InlineKeyboardButton(
        text=_("Место в очереди"), callback_data="beniakoni_place_in_queue_cargo"
    )
    ikb2 = InlineKeyboardButton(
        text=_("Длинна очереди"), callback_data="beniakoni_queue_len_cargo"
    )
    ikb3 = InlineKeyboardButton(
        text=_("Пропущено за час"), callback_data="beniakoni_an_hour_cargo"
    )
    ikb4 = InlineKeyboardButton(
        text=_("Пропущено за сутки"), callback_data="beniakoni_an_day_cargo"
    )
    ikb5 = InlineKeyboardButton(
        text=_("Назад ↩️"), callback_data="back_beniakoni_cargo"
    )
    ikb_beniakoni_cargo.add(ikb1, ikb2, ikb3, ikb4, ikb5)
    return ikb_beniakoni_cargo


def ikb_beniakoni_ts() -> InlineKeyboardMarkup:
    ikb_beniakoni_ts = InlineKeyboardMarkup(row_width=1)
    ikb1 = InlineKeyboardButton(text=_("Автобус 🚌"), callback_data="beniakoni_bus")
    ikb2 = InlineKeyboardButton(
        text=_("Легковой транспорт 🚘"), callback_data="beniakoni_passenger"
    )
    ikb3 = InlineKeyboardButton(
        text=_("Грузовой транспорт 🚛"), callback_data="beniakoni_cargo"
    )
    ikb4 = InlineKeyboardButton(text=_("Назад ↩️"), callback_data="back_beniakoni")
    ikb_beniakoni_ts.add(ikb1, ikb2, ikb3, ikb4)
    return ikb_beniakoni_ts
