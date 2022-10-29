from app.exceptions import NotFound, AlreadyExists
from app.database import DataBase


async def teacher_add(user_id: str):
    if await DataBase.fetchrow('SELECT * FROM teachers WHERE id = ($1)', user_id):
        raise AlreadyExists('Пользователь уже является преподавателем!')
    await DataBase.execute('INSERT INTO teachers (id) VALUES ($1)', user_id)


async def teacher_list():
    return await DataBase.fetch('SELECT * FROM teachers')


async def teacher_get(user_id: str):
    res = await DataBase.fetchrow('SELECT * FROM teachers WHERE id = ($1)', user_id)
    if res is None:
        raise NotFound('Пользователь не является преподавателем!')
    return res


async def teacher_del(user_id: str):
    await DataBase.execute('DELETE FROM teachers WHERE id = ($1)', user_id)
