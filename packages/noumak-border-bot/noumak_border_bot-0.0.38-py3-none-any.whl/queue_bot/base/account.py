from queue_bot.db.models import User, Numbers
from queue_bot import keyboard
from aiogram.dispatcher.filters.state import StatesGroup, State
from abc import ABC, abstractmethod
from queue_bot.middleware import _


class ClientStateGroup(StatesGroup):
    add_bus = State()
    add_car = State()
    add_truck = State()
    delete_bus = State()
    delete_car = State()
    delete_truck = State()
    edit_bus = State()
    edit_car = State()
    edit_truck = State()


class BaseUser(ABC):
    @abstractmethod
    async def _get_user(self):
        ...

    @abstractmethod
    async def _get_numbers(self) -> Numbers:
        ...


class Account(BaseUser):
    def __init__(self, user_id):
        self._user_id = user_id

    async def _get_user(self):
        self._model: User = (
            await User.filter(telegram_id=self._user_id).prefetch_related().first()
        )

    async def _get_numbers(self) -> Numbers:
        await self._get_user()
        return await self._model.number

    async def edit_number(self):
        numbers = await self._get_numbers()
        if numbers != None:
            self.response = _("Выберите нужный транспорт")
            self.keyboard = keyboard.ikb_lk_edit_number
        else:
            self.response = _("Вы не отслеживаете ни один вид транспорта")
            self.keyboard = keyboard.ikb_lk_back

    async def edit_bus(self):
        numbers = await self._get_numbers()
        if numbers.bus != None:
            self.response = _("Введите номер автобуса")
            return await ClientStateGroup.edit_bus.set(), True
        self.response = _("За вами нет закрепленного автобуса")
        self.keyboard = keyboard.ikb_lk_back
        return False

    async def edit_passenger(self):
        numbers = await self._get_numbers()
        if numbers.car != None:
            self.response = _("Введите номер авто")
            return await ClientStateGroup.edit_car.set(), True
        self.response = _("За вами нет закрепленного авто")
        self.keyboard = keyboard.ikb_lk_back
        return False

    async def edit_cargo(self):
        numbers = await self._get_numbers()
        if numbers.truck != None:
            self.response = _("Введите номер грузовой")
            return await ClientStateGroup.edit_truck.set(), True
        self.response = _("За вами нет закрепленного грузового транспорта")
        self.keyboard = keyboard.ikb_lk_back
        return False

    async def add_number(self):
        numbers = await self._get_numbers()
        if numbers != None:
            self.response = _("Выберите нужный транспорт")
        else:
            numbers = await Numbers.create()
            await self._model.update_from_dict({"number_id": numbers.id})
            await self._model.save()
            self.response = _("Выберите нужный транспорт")
        self.keyboard = keyboard.ikb_lk_add_number

    async def add_bus(self):
        numbers = await self._get_numbers()
        if numbers.bus == None:
            self.response = _("Введите номер автобуса")
            return await ClientStateGroup.add_bus.set(), True
        else:
            self.response = _("За вами закреплен автобус с номером '{}'").format(
                numbers.bus
            )
            self.keyboard = keyboard.ikb_lk_back
            return False

    async def add_passenger(self):
        numbers = await self._get_numbers()
        if numbers.car == None:
            self.response = _("Введите номер авто")
            return await ClientStateGroup.add_car.set(), True
        else:
            self.response = _("За вами закреплено авто с номером '{}'").format(
                numbers.car
            )
            self.keyboard = keyboard.ikb_lk_back
            return False

    async def add_cargo(self):
        numbers = await self._get_numbers()
        if numbers.truck == None:
            self.response = _("Введите номер грузового транспорта")
            return await ClientStateGroup.add_truck.set(), True
        else:
            self.response = _(
                "За вами закреплен грузовой транспорт с номером '{}'"
            ).format(numbers.truck)
            self.keyboard = keyboard.ikb_lk_back
            return False

    async def del_number(self):
        numbers = await self._get_numbers()
        if numbers != None:
            self.response = _("Выберите нужный транспорт")
            self.keyboard = keyboard.ikb_lk_del_number
        else:
            self.response = _("Вы не отслеживаете ни один вид транспорта")
            self.keyboard = keyboard.ikb_lk_back

    async def del_bus(self):
        self.numbers = await self._get_numbers()
        if self.numbers.bus:
            old_number = self.numbers.bus
            await self.numbers.update_from_dict({"bus": None})
            await self.numbers.save()
            self.response = _("Автобус с номером '{}' удален").format(old_number)
        else:
            self.response = _("За вами нет закрепленного автобуса")
        self.keyboard = keyboard.ikb_lk_back

    async def del_passenger(self):
        self.numbers = await self._get_numbers()
        if self.numbers.car:
            old_number = self.numbers.car
            await self.numbers.update_from_dict({"car": None})
            await self.numbers.save()
            self.response = _("Легковая с номером '{}' удалена").format(old_number)
        else:
            self.response = _("За вами нет закрепленного авто")
        self.keyboard = keyboard.ikb_lk_back

    async def del_cargo(self):
        self.numbers = await self._get_numbers()
        if self.numbers.truck:
            old_number = self.numbers.truck
            await self.numbers.update_from_dict({"truck": None})
            await self.numbers.save()
            self.response = _("Грузовая с номером '{}' удалена").format(old_number)
        else:
            self.response = _("За вами нет закрепленного грузового транспорта")
        self.keyboard = keyboard.ikb_lk_back

    async def show_number(self):
        await self._get_user()
        try:
            val = {
                k: (v if v != None else _("Не отслеживается"))
                for (k, v) in (await self._model.number.values()).items()
                if k != "id"
            }
            self.response = _(
                "Закрепленный за вами транспорт:\n"
                "<b>Автобус:</b> {bus} 🚌\n"
                "<b>Легковая:</b> {car} 🚘\n"
                "<b>Грузовая:</b> {truck} 🚛"
            ).format(
                bus=val["bus"],
                car=val["car"],
                truck=val["truck"],
            )
        except AttributeError:
            self.response = _("Вы не отслеживаете ни один вид транспорта")
        finally:
            self.keyboard = keyboard.ikb_lk_back

    async def del_numbers(self):
        numbers = await self._get_numbers()
        if numbers:
            await numbers.delete()
            self.response = _("Весь отслеживаемый транспорт успешно удален")
        else:
            self.response = _("Вы не отслеживаете ни один вид транспорта")
        self.keyboard = _(keyboard.ikb_lk_back)


class NumberNotValid(Exception):
    ...


class BaseNumberValid(ABC):
    def __init__(self, number, state, transport, user_id):
        self._number = number
        self._state = state
        self._transport = transport
        self._user = user_id

    @abstractmethod
    def valid(self):
        ...

    def is_valid(self):
        try:
            self.valid()
        except NumberNotValid:
            return False
        return True


class NumberValid(BaseNumberValid, BaseUser):
    def valid(self):
        if not (self._number.isalnum() and 5 <= len(self._number) <= 11):
            self.response = _(
                "Недопустимый формат, проверьте правильность введенного номера и повторите попытку"
            )
            raise NumberNotValid
        self._transliterate()

    def _transliterate(self):
        letters = {
            "а": "a",
            "в": "b",
            "е": "e",
            "д": "Д",
            "к": "k",
            "м": "m",
            "н": "h",
            "о": "o",
            "р": "p",
            "с": "c",
            "т": "t",
            "у": "y",
            "х": "x",
            "А": "A",
            "В": "B",
            "Е": "E",
            "Д": "D",
            "К": "K",
            "М": "M",
            "Н": "H",
            "О": "O",
            "Р": "P",
            "С": "C",
            "Т": "T",
            "У": "Y",
            "Х": "X",
        }
        for key in letters:
            self._number = self._number.replace(key, letters[key])

    def __str__(self):
        return self._number.upper()

    async def _get_user(self):
        self._model: User = (
            await User.filter(telegram_id=self._user).prefetch_related().first()
        )

    async def _get_numbers(self) -> Numbers:
        await self._get_user()
        return await self._model.number

    async def save(self):
        numbers: Numbers = await self._get_numbers()
        await numbers.update_from_dict({self._transport: str(self)})
        await numbers.save()
        await self._state.finish()
