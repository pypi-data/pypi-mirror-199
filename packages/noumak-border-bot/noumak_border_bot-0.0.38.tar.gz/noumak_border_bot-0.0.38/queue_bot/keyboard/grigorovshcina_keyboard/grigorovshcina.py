from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from queue_bot.middleware import _

__all__ = (
    "ikb_grigorovshcina_bus",
    "ikb_grigorovshcina_passenger",
    "ikb_grigorovshcina_cargo",
    "ikb_grigorovshcina_ts",
)


def ikb_grigorovshcina_bus() -> InlineKeyboardMarkup:
    ikb_grigorovshcina_bus = InlineKeyboardMarkup(row_width=2)
    ikb1 = InlineKeyboardButton(
        text=_("Место в очереди"), callback_data="grigorovshcina_place_in_queue_bus"
    )
    ikb2 = InlineKeyboardButton(
        text=_("Длинна очереди"), callback_data="grigorovshcina_queue_len_bus"
    )
    ikb3 = InlineKeyboardButton(
        text=_("Пропущено за час"), callback_data="grigorovshcina_an_hour_bus"
    )
    ikb4 = InlineKeyboardButton(
        text=_("Пропущено за сутки"), callback_data="grigorovshcina_an_day_bus"
    )
    ikb5 = InlineKeyboardButton(
        text=_("Назад ↩️"), callback_data="back_grigorovshcina_bus"
    )
    ikb_grigorovshcina_bus.add(ikb1, ikb2, ikb3, ikb4, ikb5)
    return ikb_grigorovshcina_bus


def ikb_grigorovshcina_passenger() -> InlineKeyboardMarkup:
    ikb_grigorovshcina_passenger = InlineKeyboardMarkup(row_width=2)
    ikb1 = InlineKeyboardButton(
        text=_("Место в очереди"),
        callback_data="grigorovshcina_place_in_queue_passenger",
    )
    ikb2 = InlineKeyboardButton(
        text=_("Длинна очереди"), callback_data="grigorovshcina_queue_len_passenger"
    )
    ikb3 = InlineKeyboardButton(
        text=_("Пропущено за час"), callback_data="grigorovshcina_an_hour_passenger"
    )
    ikb4 = InlineKeyboardButton(
        text=_("Пропущено за сутки"), callback_data="grigorovshcina_an_day_passenger"
    )
    ikb5 = InlineKeyboardButton(
        text=_("Назад ↩️"), callback_data="back_grigorovshcina_passenger"
    )
    ikb_grigorovshcina_passenger.add(ikb1, ikb2, ikb3, ikb4, ikb5)
    return ikb_grigorovshcina_passenger


def ikb_grigorovshcina_cargo() -> InlineKeyboardMarkup:
    ikb_grigorovshcina_cargo = InlineKeyboardMarkup(row_width=2)
    ikb1 = InlineKeyboardButton(
        text=_("Место в очереди"), callback_data="grigorovshcina_place_in_queue_cargo"
    )
    ikb2 = InlineKeyboardButton(
        text=_("Длинна очереди"), callback_data="grigorovshcina_queue_len_cargo"
    )
    ikb3 = InlineKeyboardButton(
        text=_("Пропущено за час"), callback_data="grigorovshcina_an_hour_cargo"
    )
    ikb4 = InlineKeyboardButton(
        text=_("Пропущено за сутки"), callback_data="grigorovshcina_an_day_cargo"
    )
    ikb5 = InlineKeyboardButton(
        text=_("Назад ↩️"), callback_data="back_grigorovshcina_cargo"
    )
    ikb_grigorovshcina_cargo.add(ikb1, ikb2, ikb3, ikb4, ikb5)
    return ikb_grigorovshcina_cargo


def ikb_grigorovshcina_ts() -> InlineKeyboardMarkup:
    ikb_grigorovshcina_ts = InlineKeyboardMarkup(row_width=1)
    ikb1 = InlineKeyboardButton(text=_("Автобус 🚌"), callback_data="grigorovshcina_bus")
    ikb2 = InlineKeyboardButton(
        text=_("Легковой транспорт 🚘"), callback_data="grigorovshcina_passenger"
    )
    ikb3 = InlineKeyboardButton(
        text=_("Грузовой транспорт 🚛"), callback_data="grigorovshcina_cargo"
    )
    ikb4 = InlineKeyboardButton(text=_("Назад ↩️"), callback_data="back_grigorovshcina")
    ikb_grigorovshcina_ts.add(ikb1, ikb2, ikb3, ikb4)
    return ikb_grigorovshcina_ts
