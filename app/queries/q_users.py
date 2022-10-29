import asyncpg

from app.exceptions import NotFound, AlreadyExists, NotChange
from app.database import DataBase
from app.utils import clear_none, sql_update


async def user_add(**kwargs):
    """ Добавляет нового пользователя в базу данных. """
    if await DataBase.fetchrow(f'SELECT * FROM users WHERE email = ($1)', kwargs.get('email')):  # check
        raise AlreadyExists()
    sql_columns = ', '.join(kwargs)
    sql_values = ', '.join([f'${i + 1}' for i in range(len(kwargs))])
    await DataBase.execute(f'INSERT INTO "users" ({sql_columns}) VALUES ({sql_values})', *kwargs.values())


async def user_list() -> list[asyncpg.Record]:
    """ Возвращает список пользователей из базы данных. """
    return await DataBase.fetch('SELECT * FROM users')


async def user_get(uuid: str) -> asyncpg.Record:
    """ Возвращает базовую информацию о пользователе из базы данных. """
    result = await DataBase.fetchrow(f'SELECT * FROM users WHERE id = ($1)', uuid)
    if not result:  # check
        raise NotFound()
    return result


async def user_edit(uuid: str, **kwargs):
    """ Редактирует информацию о пользователе в базе данных. """
    await user_get(uuid)  # check
    if await DataBase.fetchrow('SELECT * FROM users WHERE email = ($1)', kwargs.get('email')):  # check
        raise AlreadyExists()
    sql = sql_update('users', **kwargs)
    if len(sql) < 0:  # check
        raise NotChange()
    await DataBase.execute(sql, uuid, *clear_none(kwargs).values())


async def user_del(uuid: str):
    """ Удаляет пользователя из базы данных. """
    await user_get(uuid)  # check
    await DataBase.execute('DELETE FROM "users" WHERE "id" = ($1)', uuid)
