from queue_bot.middleware import _


response_en_monitoring = {
    "Ваш транспорт {} в очереди": "Your transport {} is in the queue",
    "Вас вызвали в пункт пропуска": "You have been called to the checkpoint",
    "Вы больше не состоите в очереди": "You are no longer in line",
    "Ваш транспорт аннулирован": "Your transport has been cancelled.",
    "Бенякони": "Benyakoni",
    "Берестовица": "Berestovitsa",
    "Брест БТС": "Brest",
    "Григоровщина": "Grigorovshchina",
    "Каменный Лог": "Kamenny Log",
    "Котловка": "Kotlovka",
    "Урбаны": "Urbany",
    "Вызван в ПП": "Summoned to the checkpoint",
    "Аннулирован": "Canceled",
}
response_pl_monitoring = {
    "Ваш транспорт {} в очереди": "Twój transport {} w kolejce",
    "Вас вызвали в пункт пропуска": "Zostałeś wyzwany do granicy",
    "Вы больше не состоите в очереди": "Nie jesteś już w kolejce",
    "Ваш транспорт аннулирован": "Twój transport został anulowany",
    "Бенякони": "Bieniakoni",
    "Берестовица": "Berestowica",
    "Брест БТС": "Brest",
    "Григоровщина": "Grigorowszczina",
    "Каменный Лог": "Kamenny Log",
    "Котловка": "Kotlowka",
    "Урбаны": "Urbany",
    "Вызван в ПП": "Wyzwany do granicy",
    "Аннулирован": "Anulowany",
}


def _m(message, lang_code):
    if lang_code == "ru":
        return message
    elif lang_code == "en":
        return response_en_monitoring[message]
    else:
        return response_pl_monitoring[message]


def _k(text, lang_code):
    if lang_code == "ru":
        return text
    elif lang_code == "en":
        return "Main menu"
    else:
        return "Menu główne"


def srart_template():
    return _(
        "Здесь ты можешь узнать информацию об очереди на границе в зонах ожидания(ЗО)"
    )


def help_template():
    return _(
        """
⚙️ Доступные команды:
/long - сменить язык

/tiket - отправить сообщение об ошибке 
 
/beniakoni_info - получить контактную информацию о пункте пропуска  Бенякони

/berestovica_info - получить контактную информацию о пункте пропуска  Берестовица

/brest_info - получить контактную информацию о пункте пропуска  Брест

/grigorovshcina_info - получить контактную информацию о пункте пропуска Григоровщина

/kamenny_log_info - получить контактную информацию о пункте пропуска \nКаменный Лог

/kotlovka_info - получить контактную информацию о пункте пропуска Котловка

/urbany_info - получить контактную информацию о пункте пропуска Урбаны

Подробное описание бота и инструкции как им пользоваться изложена по (<a href="https://telegra.ph/FAQ-03-10-12">ссылке</a>)

Остались вопросы? Задайте их нам в чате поддержки
        """
    )


def tiket_template():
    return _(
        """
Для отправки сообщения об ошибке, будь-то неверная информация или отсутствие ответа от бота,
перейдите по кнопке в чат поддержки, опишите всю ситуацию(желательно приложив скриншот), укажите в каком
именно месте у вас возникла ошибка (пункт пропуска/транспорт).
Ваше сообщение будет рассмотрено в ближайшее время, а ошибка исправлена.
"""
    )


def monitoring_template():
    return _(
        "Бот сканирует зоны ожидания и ищет в них ваш транспорт, чтобы в последующем следить и сообщать пользователю об движении в очереди"
    )
