from time import perf_counter
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message

import app.database.requests as db

class LocalizationMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]
                       ) -> Any:
        user = data.get('event_from_user')
        if user:
            user_info = await db.get_user(user.id)
            from_db_language = user_info.language
            for i in from_db_language:
                user_language = i.lang_code
            data['language'] = user_language
        else:
            data['language'] = 'ru'
        return await handler(event, data)