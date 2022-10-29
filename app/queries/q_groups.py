import asyncpg

from app.exceptions import NotFound, AlreadyExists, NotChange
from app.database import DataBase
from app.utils import clear_none, sql_update


async def group_add(name: str, teacher_id: str = None):
    """ Добавляет новую группу в базу данных. """
    csql = 'SELECT * FROM "groups" WHERE "name" = ($1) and teacher_id = ($2)'
    if await DataBase.fetchrow(csql, name, teacher_id):  # check
        raise AlreadyExists()
    sql = 'INSERT INTO "groups" ("name", teacher_id) VALUES ($1, $2)'
    await DataBase.execute(sql, name, teacher_id)


async def group_list() -> list[asyncpg.Record]:
    """ Возвращает список групп из базы данных. """
    return await DataBase.fetch('SELECT * FROM "groups"')


async def teacher_group_list(teacher_id: str) -> list[asyncpg.Record]:
    return await DataBase.fetch('SELECT * FROM "groups" WHERE teacher_id = ($1)', teacher_id)


async def group_get(group_id: int) -> asyncpg.Record:
    """ Возвращает данные о группе из базы данных. """
    res = await DataBase.fetchrow('SELECT * FROM "groups" WHERE id = ($1)', group_id)
    if res is None:  # check
        raise NotFound
    return res


async def group_edit(group_id: int, teacher_id: str = None, **kwargs):
    """ Редактирует данные о группе в базе данных. """
    await group_get(group_id)  # check
    name = kwargs.get('name')  # check
    csql = 'SELECT * FROM "groups" WHERE "name" = ($1) and teacher_id = ($2)'
    if name and await DataBase.fetchrow(csql, name, teacher_id):
        raise AlreadyExists()
    sql = sql_update('groups', **kwargs)
    if len(sql) == 0:
        raise NotChange()
    await DataBase.execute(sql, group_id, *clear_none(kwargs).values())


async def group_del(group_id: int):
    """ Удаляет группу из базы данных. """
    await group_get(group_id)  # check
    await DataBase.execute('DELETE FROM "groups" WHERE id = ($1)', group_id)
