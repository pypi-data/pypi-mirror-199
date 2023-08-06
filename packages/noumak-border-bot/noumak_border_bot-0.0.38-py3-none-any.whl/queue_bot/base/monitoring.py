import aiofiles
import os
import json
from pathlib import Path
from aiogram import types
from aiogram import types
from queue_bot.db.models import Tracking, Numbers, User
from queue_bot.base.account import BaseUser
from queue_bot import settings
from queue_bot.middleware import _
from queue_bot.base.template import _m
from queue_bot import keyboard
from aiogram.dispatcher import FSMContext


class BaseMonitoring(BaseUser):
    async def _get_user(self):
        self._model = await User.get(telegram_id=self._user_id)
        self.lang_code = self._model.language_code

    async def _get_numbers(self):
        await self._get_user()
        return await self._model.number

    async def _get_monitoring(self):
        await self._get_user()
        return await self._model.monitoring


class AddMonitoring(BaseMonitoring):
    def __init__(self, user_id):
        self._user_id = user_id
        self._model: User = None
        self._file_paths = []
        self._status = None

    async def _create_keyboard(self):
        self._buttons = []
        val = {
            k: v
            for k, v in (await self._model.number.values()).items()
            if k != "id"
            if v is not None
        }
        if val:
            for num in val:
                if num == "bus":
                    self._buttons.append(
                        types.InlineKeyboardButton(
                            text=_("Автобус  {bus}  🚌").format(**val),
                            callback_data="bus_monitoring",
                        )
                    )
                elif num == "car":
                    self._buttons.append(
                        types.InlineKeyboardButton(
                            text=_("Легковая  {car}  🚘").format(**val),
                            callback_data="passenger_monitoring",
                        )
                    )
                else:
                    self._buttons.append(
                        types.InlineKeyboardButton(
                            text=_("Грузовая  {truck}  🚛").format(**val),
                            callback_data="cargo_monitoring",
                        )
                    )
            self.transport = types.InlineKeyboardMarkup(row_width=1)
            self.transport.add(*self._buttons)
            self.transport.add(
                types.InlineKeyboardButton(
                    text=_("Назад ↩️"), callback_data="back_monitoring"
                )
            )
            return True
        return False

    async def add_monitoring(self):
        numbers: Numbers = await self._get_numbers()
        if not await self._model.monitoring:
            if numbers != None:
                if await self._create_keyboard():
                    self.response = _("Выберите нужный транспорт")
                    return
                self.response = _("Вы не отслеживаете ни один вид транспорта")
                self.transport = keyboard.ikb_back_monitoring()
            else:
                self.response = _("Вы не отслеживаете ни один вид транспорта")
                self.transport = keyboard.ikb_back_monitoring()
        else:
            monitoring: Tracking = await self._model.monitoring
            self.response = _(
                _("Уже включен мониторинг для транспорта с номером '{}'")
            ).format(monitoring.number)
            self.transport = keyboard.ikb_back_monitoring()

    async def add_transport(self, ts_id, ts_temp, state: FSMContext):
        numbers: Numbers = await self._get_numbers()
        if ts_id == 1:
            number = numbers.bus
            transport = "bus"
        elif ts_id == 2:
            number = numbers.car
            transport = "car"
        else:
            number = numbers.truck
            transport = "truck"
        async with state.proxy() as data:
            data["ts_id"] = ts_id
            data["ts_tem"] = ts_temp
            data["number"] = number
            data["transport"] = transport
        self.response = _("Выберите частоту уведомлений:")

    async def add_intensity(self, intensity, state: FSMContext):
        async with state.proxy() as data:
            data["intensity"] = intensity
            number: Numbers = data["number"]
        self.response = _(
            "Параметры мониторинга:\n"
            "<b>Номер:</b> {number}\n<b>Вид транспорта:</b> "
            "{data}\n<b>Частота уведомлений:</b> {intensity}"
        ).format(number=number, data=data["ts_tem"], intensity=intensity)


class SaveMonitoring(BaseMonitoring):
    def __init__(self, user_id):
        self._user_id = user_id
        self._model: User = None
        self._status = None

    async def _get_path(self):
        return [
            file.path
            for file in os.scandir(settings.BASE_DIR / "checkpoint")
            if file.is_file()
        ]

    async def _get_params(self, state: FSMContext):
        async with state.proxy() as data:
            self._ts_id = data["ts_id"]
            self._number = data["number"]
            self._intensity = data["intensity"]
            self._transport = data["transport"]

    async def save(self, state):
        try:
            await self._get_params(state)
            if await self._get_place_monitoring():
                monitoring = await Tracking.create(**self._params)
                self._model.monitoring = monitoring
                await self._model.save()
                self.response = _(
                    "✅ Мониторинг подключен\n"
                    "<b>Номер:</b> {number}\n"
                    "<b>Пункт пропуска:</b> {checkpoint}\n"
                    "<b>Периодичность:</b> {intensity}\n"
                    "<b>Текущее место в очереди: </b> {place}"
                ).format(
                    number=self._number,
                    checkpoint=_m(self._checkpoint_ru, self.lang_code),
                    intensity=self._intensity,
                    place=self._params["place"],
                )
            else:
                if self._status == None:
                    self.response = _(
                        "❌ Транспорт с номером '{}' не зарегистрирован ни в одной зоне ожидания,"
                        " проверьте правильность введенного номера или повторите попытку через несколько минут"
                    ).format(self._number)
                    return
                elif self._status == 3:
                    self.response = _(
                        "Транспорт имеет статус '{}'\nМониторинг не может быть подключен"
                    ).format(_m("Вызван в ПП", self.lang_code))
                else:
                    self._status = "Аннулирован"
                self.response = _(
                    "Транспорт имеет статус '{}'\nМониторинг не может быть подключен"
                ).format(_m("Аннулирован", self.lang_code))
        finally:
            await state.finish()

    async def _get_place_monitoring(self):
        for file_path in await self._get_path():
            async with aiofiles.open(file_path, mode="r") as file:
                res = json.loads(await file.read())
                transport = self._transport + "LiveQueue"
                if res[transport]:
                    for auto in res[transport]:
                        if self._number == auto["regnum"]:
                            if auto["status"] == 2:
                                self._params = {
                                    "number": self._number,
                                    "checkpoint": Path(file_path).name.split(".")[0],
                                    "car_id": self._ts_id,
                                    "intensity": self._intensity,
                                    "place": auto["order_id"],
                                }
                                self._checkpoint_ru = res["info"]["name"]
                                return await self._get_user(), True
                            await self._get_user()
                            self._status = int(auto["status"])
                            return False
        return False

    async def delete(self):
        monitoring: Tracking = await self._get_monitoring()
        if monitoring:
            await monitoring.delete()
            self.response = _(
                "Мониторинг для транспорта с номером '{}' был удален"
            ).format(monitoring.number)
        else:
            self.response = _("Вы не подключали услугу мониторинга")
