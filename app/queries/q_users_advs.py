from app.exceptions import NotFound, AlreadyExists
from app.queries.q_adv import adv_get
from app.queries.q_users import user_get
from app.database import DataBase


async def user_adv_add(uuid: str, adv_id: int):
    """ Добавляет пользователю достижение в базе данных. """
    await user_adv_get(uuid, adv_id, True)  # check
    sql = f'INSERT INTO users_advancements (user_id, advancement_id) VALUES ($1, $2)'
    await DataBase.execute(sql, uuid, adv_id)


async def user_adv_list(uuid: str):
    """ Возвращает достижения пользователя. """
    await user_get(uuid)  # check
    return await DataBase.fetch('SELECT * FROM users_advancements WHERE user_id = ($1)', uuid)


async def user_adv_get(uuid: str, adv_id: int, is_reverse=False):
    """ Возвращает достижение пользователя. """
    await user_get(uuid)
    await adv_get(adv_id)
    sql = f'SELECT * FROM users_advancements WHERE user_id = ($1) and advancement_id = ($2)'
    result = await DataBase.fetchrow(sql, uuid, adv_id)
    if is_reverse and result:
        raise AlreadyExists()
    if not (is_reverse or result):
        raise NotFound()
    return result


async def user_adv_del(uuid: str, adv_id: int):
    """ Удаляет достижение у пользователя. """
    await user_adv_get(uuid, adv_id)  # check
    sql = 'DELETE FROM users_advancements WHERE user_id = ($1) and advancement_id = ($2)'
    await DataBase.execute(sql, uuid, adv_id)
