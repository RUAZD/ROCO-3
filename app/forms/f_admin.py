import asyncpg
from fastapi import APIRouter, Depends, Form

from app import schemes
from app.exceptions import BadRequest
from app.queries import q_admin
from app.user_hash import get_hashed_password, verify_password, get_current_user

router = APIRouter(tags=['Администраторы'])


@router.post('/become_an_administrator', summary='Стать администратором!')
async def func(user: asyncpg.Record = Depends(get_current_user),
               password: str = Form(description='Пароль консоли администратора')) -> schemes.Updated:
    """
    <h1>Администратор имеет полный контроль над темами интересов и достижениями! <br>
    Администратор может снимать и добавлять преподавателей! <br>
    Администратор может удалять пользователей! <br>
    <br>
    Пароль: admin</h1>
    """
    if not verify_password(password, get_hashed_password('admin')):
        raise BadRequest('Неверный пароль!')
    await q_admin.admin_add(user.get('id'))
    return schemes.Updated()


@router.delete('/leave_the_post_of_administrator', summary='Покинуть пост администратора!')
async def func(user: asyncpg.Record = Depends(get_current_user)) -> schemes.Deleted:
    await q_admin.admin_del(user.get('id'))
    return schemes.Deleted()
