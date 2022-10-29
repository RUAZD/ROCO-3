import asyncpg

from app.exceptions import NotFound, AlreadyExists
from app.database import DataBase


async def topic_add(name: str):
    """ Добавляет новую тему интересов в базу данных. """
    if await DataBase.fetchrow('SELECT * FROM topics WHERE "name" = ($1)', name):
        raise AlreadyExists()
    await DataBase.execute('INSERT INTO topics ("name") VALUES ($1)', name)


async def topic_list() -> list[asyncpg.Record]:
    """ Возвращает список тем интересов из базы данных. """
    return await DataBase.fetch('SELECT * FROM topics')


async def topic_get(topic_id: int) -> asyncpg.Record:
    """ Возвращает данные о теме интересов из базы данных. """
    res = await DataBase.fetchrow('SELECT * FROM topics WHERE id = ($1)', topic_id)
    if res is None:
        raise NotFound()
    return res


async def topic_edit(topic_id: int, name: str):
    """ Редактирует название темы интересов в базе данных. """
    await topic_get(topic_id)
    if await DataBase.fetchrow('SELECT * FROM topics WHERE "name" = ($1)', name):
        raise AlreadyExists()
    await DataBase.execute('UPDATE "topics" SET "name" = ($2) WHERE "id" = ($1)', topic_id, name)


async def topic_del(topic_id: int):
    """ Удаляет тему интересов из базы данных. """
    await topic_get(topic_id)
    await DataBase.execute('DELETE FROM topics WHERE id = ($1)', topic_id)
