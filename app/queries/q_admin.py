from app.exceptions import Forbidden
from app.database import DataBase


async def admin_add(user_id: str):
    if not await DataBase.fetchrow('SELECT * FROM admins WHERE id = ($1)', user_id):
        await DataBase.execute('INSERT INTO admins (id) VALUES ($1)', user_id)


async def admin_get(user_id: str):
    if await DataBase.fetchrow('SELECT * FROM admins WHERE id = ($1)', user_id) is None:
        raise Forbidden()


async def admin_del(user_id: str):
    await DataBase.execute('DELETE FROM admins WHERE id = ($1)', user_id)
