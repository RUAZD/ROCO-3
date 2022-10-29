from app.exceptions import NotFound, AlreadyExists
from app.queries.q_topics import topic_get
from app.queries.q_users import user_get
from app.database import DataBase


async def user_topic_add(uuid: str, topic_id: int):
    """ Добавляет пользователю тему инетерсов в базе данных. """
    await user_topic_get(uuid, topic_id, True)  # check
    sql = f'INSERT INTO "users_topics" ("user_id", "topic_id") VALUES ($1, $2)'
    await DataBase.execute(sql, uuid, topic_id)


async def user_topic_list(uuid: str):
    """ Возвращает темы интересов пользователя. """
    await user_get(uuid)  # check
    return await DataBase.fetch('SELECT * FROM users_topics')


async def user_topic_get(uuid: str, topic_id: int, is_reverse=False):
    """ Возвращает тему интересов пользователя. """
    await user_get(uuid)
    await topic_get(topic_id)
    sql = f'SELECT * FROM users_topics WHERE user_id = ($1) and topic_id = ($2)'
    result = await DataBase.fetchrow(sql, uuid, topic_id)
    if is_reverse and result:
        raise AlreadyExists()
    if not (is_reverse or result):
        raise NotFound()
    return result


async def user_topic_del(uuid: str, topic_id: int):
    """ Удаляет тему интересов у пользователя. """
    await user_topic_get(uuid, topic_id)  # check
    sql = 'DELETE FROM users_topics WHERE user_id = ($1) and topic_id = ($2)'
    await DataBase.execute(sql, uuid, topic_id)
