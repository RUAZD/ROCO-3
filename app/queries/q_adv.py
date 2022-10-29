import asyncpg

from app.exceptions import NotFound, AlreadyExists, NotChange
from app.database import DataBase
from app.utils import clear_none, sql_update


async def adv_add(title: str, description: str = None, level: str = None):
    """ Добавляет данные о достижении в базу данных. """
    if await DataBase.fetchrow('SELECT * FROM advancements WHERE title = ($1)', title):  # check
        raise AlreadyExists()
    sql = 'INSERT INTO advancements (title, description, level) VALUES ($1, $2, $3)'
    await DataBase.execute(sql, title, description, level)


async def adv_list() -> list[asyncpg.Record]:
    """ Возвращает список достижений из базы данных. """
    return await DataBase.fetch('SELECT * FROM advancements')


async def adv_get(adv_id: int) -> asyncpg.Record:
    """ Возвращает данные о достижении из базы данных. """
    res = await DataBase.fetchrow('SELECT * FROM advancements WHERE id = ($1)', adv_id)
    if res is None:  # check
        raise NotFound
    return res


async def adv_edit(adv_id: int, **kwargs):
    """ Редактирует данные о достижении в базе данных. """
    await adv_get(adv_id)  # check
    title = kwargs.get('title')  # check
    if title and await DataBase.fetchrow('SELECT * FROM advancements WHERE title = ($1)', title):
        raise AlreadyExists()
    sql = sql_update('advancements', **kwargs)
    if len(sql) == 0:  # check
        raise NotChange()
    await DataBase.execute(sql, adv_id, *clear_none(kwargs).values())


async def adv_del(adv_id: int):
    """ Удаляет достижение из базы данных. """
    await adv_get(adv_id)  # check
    await DataBase.execute('DELETE FROM advancements WHERE id = ($1)', adv_id)
