from app.exceptions import NotFound, AlreadyExists
from app.queries.q_courses import course_get
from app.queries.q_users import user_get
from app.database import DataBase


async def user_course_add(uuid: str, course_id: int, status: int):
    """ Добавляет пользователю курс в базе данных. """
    await user_course_get(uuid, course_id, True)  # check
    sql = f'INSERT INTO users_courses (user_id, course_id, status) VALUES ($1, $2, $3)'
    await DataBase.execute(sql, uuid, course_id, status)


async def user_course_list(uuid: str):
    """ Возвращает курсы пользователя из базы данных. """
    await user_get(uuid)  # check
    return await DataBase.fetch('SELECT * FROM users_courses WHERE user_id = ($1)', uuid)


async def user_course_list_status(uuid: str, status: int):
    """ Возвращает курсы пользователя с определённым статусом. """
    await user_get(uuid)  # check
    sql = 'SELECT * FROM users_courses WHERE user_id = ($1) and status = ($2)'
    return await DataBase.fetch(sql, uuid, status)


async def user_course_get(uuid: str, course_id: int, is_reverse=False):
    """ Возвращает курс пользователя из базы данных. """
    await user_get(uuid)
    await course_get(course_id)
    sql = f'SELECT * FROM users_courses WHERE user_id = ($1) and course_id = ($2)'
    result = await DataBase.fetchrow(sql, uuid, course_id)
    if is_reverse and result:
        raise AlreadyExists()
    if not (is_reverse or result):
        raise NotFound()
    return result


async def user_course_edit(uuid: str, course_id: int, status: int):
    """ Изменяет статус курса у пользователя в базе данных. """
    await user_course_get(uuid, course_id)  # check
    sql = 'UPDATE users_courses SET status = ($3) WHERE user_id = ($1) and course_id = ($2)'
    await DataBase.execute(sql, uuid, course_id, status)


async def user_course_del(uuid: str, course_id: int):
    """ Удаляет курс у пользователя из базы данных. """
    await user_course_get(uuid, course_id)  # check
    sql = 'DELETE FROM users_courses WHERE user_id = ($1) and course_id = ($2)'
    await DataBase.execute(sql, uuid, course_id)
