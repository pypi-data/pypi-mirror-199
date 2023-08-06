import aiofiles
import json
from abc import ABC
from datetime import datetime
from queue_bot.db.models import User
from queue_bot.middleware import _


class Parser(ABC):
    _checkpoints = "queue_bot/checkpoint/statistic/checkpoint.json"

    async def _get_user(self, user_id):
        self._model: User = await User.filter(telegram_id=user_id).first()

    async def _get_numbers(self, user_id):
        await self._get_user(user_id)
        try:
            numbers = await self._model.number.values("bus", "car", "truck")
        except AttributeError:
            return False
        return numbers


class TransportParser(Parser, ABC):
    transport = None

    async def _queue_promotion(self, filename) -> dict:
        path = f"queue_bot/checkpoint/statistic/{filename}.json"
        self.time = datetime.today().strftime("%Y-%m-%d %H:%M")
        async with aiofiles.open(path, "r") as file:
            res = json.loads(await file.read())
            return res

    async def _get_queue_per_day(self, data):
        transport = self.__class__.transport + "LastDay"
        self.response = _(
            "По состоянию на {time}:\nПропущено за сутки - {promotion}"
        ).format(time=self.time, promotion=data[transport])

    async def _get_queue_per_hour(self, data):
        transport = self.__class__.transport + "LastHour"
        self.response = _(
            "По состоянию на {time}:\nПропущено за час - {promotion}"
        ).format(time=self.time, promotion=data[transport])

    async def _get_len_queue(self, checkpoint_name):
        async with aiofiles.open(Parser._checkpoints, "r") as file:
            checkpoints = json.loads(await file.read())["result"]
            for checkpoint in checkpoints:
                if checkpoint["name"].lower() == checkpoint_name:
                    ts = "count" + self.__class__.transport.title()
                    time = datetime.today().strftime("%Y-%m-%d %H:%M")
                    self.response = _(
                        "По состоянию на {time}:\nДлинна очереди зоны ожидания - {queue}"
                    ).format(time=time, queue=checkpoint[ts])
                    break

    async def _get_params(self, auto: dict):
        time_edit, data_edit = auto["changed_date"].strip().split(" ")
        if auto["status"] == 2:
            time = datetime.today().strftime("%Y-%m-%d %H:%M")
            self.response = _(
                "По состоянию на {time}:\n" "Ваше авто {place} в очереди"
            ).format(time=time, place=auto["order_id"])
        elif auto["status"] == 3:
            self.response = _(
                "Вас вызвали в пункт пропуска:\nВремя вызова: {time}\n" "Дата: {data}"
            ).format(time=time_edit, data=data_edit)
        else:
            self.response = _(
                "Ваш транспорт аннулирован:\nВремя аннулирования: {time}\n"
                "Дата: {data}"
            ).format(time=time_edit, data=data_edit)

    async def _get_place(self, checkpoint_name, user_id):
        path = f"/home/ubuntu/python/queue_tel_bot/queue_bot/checkpoint/{checkpoint_name}.json"
        numbers = await self._get_numbers(user_id)
        if numbers:
            if numbers[self.__class__.transport]:
                transport = self.transport + "LiveQueue"
                async with aiofiles.open(path, "r") as file:
                    queue = json.loads(await file.read())[transport]
                    if queue:
                        for auto in queue:
                            if auto["regnum"] == numbers[self.transport]:
                                await self._get_params(auto)
                                break
                        else:
                            self.response = _("Вы не состоите в очереди")
                    else:
                        time = datetime.today().strftime("%Y-%m-%d %H:%M")
                        self.response = _(
                            "По состоянию на {}:\nДлинна очереди зоны ожидания - 0"
                        ).format(time)
            else:
                self.response = _("Вы не привязали номер авто к своему аккаунту")
        else:
            self.response = _("Вы не отслеживаете ни один вид транспорта")

    async def queue_promotion_per_day(self):
        data = await self._queue_promotion(self.checkpoint.lower())
        await self._get_queue_per_day(data)

    async def queue_promotion_per_hour(self):
        data = await self._queue_promotion(self.checkpoint.lower())
        await self._get_queue_per_hour(data)

    async def len_queue(self):
        await self._get_len_queue(self.checkpoint.lower())

    async def get_place(self, user_id):
        await self._get_place(self.checkpoint.lower(), user_id)


class BusParser(TransportParser):
    transport = "bus"

    def __init__(self, checkpoint):
        self.checkpoint = checkpoint


class PassengerParser(TransportParser):
    transport = "car"

    def __init__(self, checkpoint):
        self.checkpoint = checkpoint


class CargoParser(TransportParser):
    transport = "truck"

    def __init__(self, checkpoint):
        self.checkpoint = checkpoint
