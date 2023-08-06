import aiofiles
import json
from aiogram import types
from aiogram import types
from queue_bot.db.models import Tracking
from queue_bot import settings
from aiogram import Bot
from queue_bot.middleware import _
from queue_bot.base.template import _m, _k
from aiogram.utils.exceptions import BotBlocked


class Monitoring:
    def __init__(self, model):
        self._model: Tracking = model

    async def _get_all_users(self):
        self._users = await self._model.all()
        return self._users

    async def _get_params(self, user: Tracking):
        self._number = user.number
        self._checkpoint = user.checkpoint
        self._intensity = user.intensity
        self._place = user.place
        self._car = await user.car

    async def _get_data(self):
        file_path = settings.BASE_DIR / "checkpoint" / (self._checkpoint + ".json")
        async with aiofiles.open(file_path, mode="r") as file:
            transport = self._car.transport + "LiveQueue"
            self._content = json.loads(await file.read())[transport]
            if self._content:
                return True
            return False

    async def search_transport(self, bot):
        if await self._get_all_users():
            for user in self._users:
                await self._get_params(user)
                if await self._get_data():
                    self._user: Tracking = user
                    if await self._search_user():
                        await self.send_message(bot)
                        continue
                    continue
                self._status = 0
                await self.send_message(bot)

    async def _check_status(self):
        """
        status 0: deleted from queue
        status 2: arriver at tge checkpoint
        status 3: called to the checkpoint
        status 9: transport cancelled

        """
        if self._status == 2:
            return True

    async def _edit_data(self):
        if self._place != int(self.new_place):
            if self._place - int(self.new_place) >= self._intensity:
                await self._user.update_from_dict({"place": self.new_place})
                return await self._user.save(), True

    async def _search_user(self):
        for auto in self._content:
            number = auto["regnum"]
            if number != self._number:
                continue
            self._status = int(auto["status"])
            if await self._check_status():
                self.new_place = int(auto["order_id"])
                if await self._edit_data():
                    return True
                return False
            return True
        self._status = 0
        return True

    async def send_message(self, bot: Bot):
        await self._user.fetch_related("user")
        user_id = self._user.user.telegram_id
        lang_code = self._user.user.language_code
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        try:
            if await self._check_status():
                await bot.send_message(
                    user_id,
                    text=_m("Ваш транспорт {} в очереди", lang_code).format(
                        self.new_place
                    ),
                    reply_markup=kb.add(
                        types.KeyboardButton(text=_k("Главное меню", lang_code))
                    ),
                )
            else:
                if self._status == 3:
                    await self._user.delete()
                    await bot.send_message(
                        text=_m("Вас вызвали в пункт пропуска", lang_code),
                        chat_id=user_id,
                        reply_markup=kb.add(
                            types.KeyboardButton(text=_k("Главное меню", lang_code))
                        ),
                    )
                elif self._status == 0:
                    await self._user.delete()
                    await bot.send_message(
                        text=_m("Вы больше не состоите в очереди", lang_code),
                        chat_id=user_id,
                        reply_markup=kb.add(
                            types.KeyboardButton(text=_k("Главное меню", lang_code))
                        ),
                    )
                elif self._status == 9:
                    await self._user.delete()
                    await bot.send_message(
                        text=_m("Ваш транспорт аннулирован", lang_code),
                        chat_id=user_id,
                        reply_markup=kb.add(
                            types.KeyboardButton(text=_k("Главное меню", lang_code))
                        ),
                    )
        except BotBlocked:
            await self._user.delete()


async def start_monitoring(bot: Bot):
    monitoring = Monitoring(Tracking)
    await monitoring.search_transport(bot)
