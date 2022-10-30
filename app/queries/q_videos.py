import time
from datetime import datetime

import asyncpg

from app.exceptions import NotFound, NotChange
from app.database import DataBase
from app.utils import clear_none, sql_update


async def video_add(link: str, title: str, description: str, posting_time: datetime, creator_id: str):
    """ Добавляет новое видео в базу данных. """
    if posting_time is None:
        posting_time = datetime.fromtimestamp(time.time())
    sql = 'INSERT INTO videos (link, title, description, posting_time, creator_id) VALUES ($1, $2, $3, $4, $5)'
    await DataBase.execute(sql, link, title, description, posting_time, creator_id)


async def video_list() -> list[asyncpg.Record]:
    """ Возвращает список видео из базы данных. """
    return await DataBase.fetch('SELECT * FROM videos')


async def teacher_video_list(creator_id: str) -> list[asyncpg.Record]:
    return await DataBase.fetch('SELECT * FROM videos WHERE creator_id = ($1)', creator_id)


async def video_get(video_id: int) -> asyncpg.Record:
    """ Возвращает данные о видео из базы данных. """
    res = await DataBase.fetchrow('SELECT * FROM videos WHERE id = ($1)', video_id)
    if res is None:
        raise NotFound()
    return res


async def video_edit(video_id: int, title: str = None, description: str = None):
    """ Редактирует данные о видео в базе данных. """
    await video_get(video_id)
    kwargs = dict(title=title, description=description)
    sql = sql_update('video', **kwargs)
    if len(sql) < 10:
        raise NotChange()
    await DataBase.execute(sql, video_id, *clear_none(kwargs).values())


async def video_del(video_id: int):
    """ Удаляет видео из базы данных. """
    await video_get(video_id)
    await DataBase.execute('DELETE FROM videos WHERE id = ($1)', video_id)
