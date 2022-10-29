from app.exceptions import NotFound, AlreadyExists
from app.queries.q_users import user_get
from app.database import DataBase


async def user_friend_add(user_id: str, friend_id: str, status: int):
    await user_friend_get(user_id, friend_id, True)
    sql = f'INSERT INTO users_friends (user_id, friend_id, status) VALUES ($1, $2, $3)'
    await DataBase.execute(sql, user_id, friend_id, status)


async def user_friend_list(user_id: str):
    await user_get(user_id)
    return await DataBase.fetch('SELECT * FROM users_friends WHERE user_id = ($1)', user_id)


async def user_friend_list_status(user_id: str, status: int):
    await user_get(user_id)
    sql = 'SELECT * FROM users_friends WHERE user_id = ($1) and status = ($2)'
    return await DataBase.fetch(sql, user_id, status)


async def user_friend_get(user_id: str, friend_id: str, is_reverse=False):
    check = (await user_get(user_id), await user_get(friend_id))
    sql = f'SELECT * FROM users_friends WHERE user_id = ($1) and friend_id = ($2)'
    result = await DataBase.fetchrow(sql, user_id, friend_id)
    if is_reverse and result:
        raise AlreadyExists()
    if not (is_reverse or result):
        raise NotFound()
    return result


async def user_friend_edit(user_id: str, friend_id: str, status: int):
    await user_friend_get(user_id, friend_id)
    sql = 'UPDATE users_friends SET status = ($3) WHERE user_id = ($1) and friend_id = ($2)'
    await DataBase.execute(sql, user_id, friend_id, status)


async def user_friend_del(user_id: str, friend_id: str):
    await user_friend_get(user_id, friend_id)
    sql = 'DELETE FROM users_friends WHERE user_id = ($1) and friend_id = ($2)'
    await DataBase.execute(sql, user_id, friend_id)
