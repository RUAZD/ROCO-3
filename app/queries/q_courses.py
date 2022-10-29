import asyncpg

from app.exceptions import NotFound, AlreadyExists, NotChange
from app.database import DataBase
from app.utils import clear_none, sql_update


async def course_add(name: str, description: str = None, teacher_id: str = None):
    """ Добавляет новый курс в базу данных. """
    csql = 'SELECT * FROM courses WHERE "name" = ($1) and teacher_id = ($2)'
    if await DataBase.fetchrow(csql, name, teacher_id):  # check
        raise AlreadyExists()
    sql = 'INSERT INTO courses ("name", description, teacher_id) VALUES ($1, $2, $3)'
    await DataBase.execute(sql, name, description, teacher_id)


async def course_list() -> list[asyncpg.Record]:
    """ Возвращает список курсов из базы данных. """
    return await DataBase.fetch('SELECT * FROM courses')


async def teacher_course_list(teacher_id: str) -> list[asyncpg.Record]:
    return await DataBase.fetch('SELECT * FROM courses WHERE teacher_id = ($1)', teacher_id)


async def course_get(course_id: int) -> asyncpg.Record:
    """ Возвращает данные о курсе из базы данных. """
    res = await DataBase.fetchrow('SELECT * FROM courses WHERE id = ($1)', course_id)
    if res is None:  # check
        raise NotFound
    return res


async def course_edit(course_id: int, teacher_id: str, **kwargs):
    """ Редактирует данные о курсе в базе данных. """
    await course_get(course_id)
    csql = 'SELECT * FROM courses WHERE "name" = ($1) and teacher_id = ($2)'
    if 'name' in kwargs and await DataBase.fetchrow(csql, kwargs.get('name'), teacher_id):  # check
        raise AlreadyExists()
    sql = sql_update('courses', **kwargs)
    if len(sql) < 0:
        raise NotChange()
    await DataBase.execute(sql, course_id, *clear_none(kwargs).values())


async def course_del(course_id: int):
    """ Удаляет курс из базы данных. """
    await course_get(course_id)  # check
    await DataBase.execute('DELETE FROM courses WHERE id = ($1)', course_id)
