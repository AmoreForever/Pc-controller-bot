from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
from data import tg_id


class IsAdmin(BoundFilter):
    async def check(self, message: Message):
        return message.from_user.id == tg_id
