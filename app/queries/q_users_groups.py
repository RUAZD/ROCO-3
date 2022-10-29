from app.exceptions import NotFound, AlreadyExists
from app.queries.q_groups import group_get
from app.queries.q_users import user_get
from app.database import DataBase


async def user_group_add(user_id: str, group_id: int, status: int):
    await user_group_get(user_id, group_id, True)
    sql = f'INSERT INTO users_groups (user_id, group_id, status) VALUES ($1, $2, $3)'
    await DataBase.execute(sql, user_id, group_id, status)


async def user_group_list(uuid: str):
    await user_get(uuid)
    return await DataBase.fetch('SELECT * FROM users_groups WHERE user_id = ($1)', uuid)


async def group_users_list(group_id: int):
    await group_get(group_id)
    return await DataBase.fetch('SELECT * FROM users_groups WHERE group_id = ($1)', group_id)


async def user_group_list_status(user_id: str, status: int):
    await user_get(user_id)
    sql = 'SELECT * FROM users_groups WHERE user_id = ($1) and status = ($2)'
    return await DataBase.fetch(sql, user_id, status)


async def user_group_get(user_id: str, group_id: int, is_reverse=False):
    check = (await user_get(user_id), await group_get(group_id))
    sql = f'SELECT * FROM users_groups WHERE user_id = ($1) and group_id = ($2)'
    result = await DataBase.fetchrow(sql, user_id, group_id)
    if is_reverse and result:
        raise AlreadyExists()
    if not (is_reverse or result):
        raise NotFound()
    return result


async def user_group_edit(user_id: str, group_id: int, status: int):
    await user_group_get(user_id, group_id)
    sql = 'UPDATE users_groups SET status = ($3) WHERE user_id = ($1) and group_id = ($2)'
    await DataBase.execute(sql, user_id, group_id, status)


async def user_group_del(user_id: str, group_id: int):
    await user_group_get(user_id, group_id)
    sql = 'DELETE FROM users_groups WHERE user_id = ($1) and group_id = ($2)'
    await DataBase.execute(sql, user_id, group_id)
