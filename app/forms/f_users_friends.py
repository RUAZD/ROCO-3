from fastapi import APIRouter, Depends, Form

from app.queries import *
from app.schemes import *
from app.user_hash import get_current_user
from app.utils import format_record, format_records

router = APIRouter(prefix='/user/friend', tags=['Пользователь и друзья'])


@router.post('/add', summary='Отправить пользователю заявку в друзья', response_model=Created)
async def func(
        user: asyncpg.Record = Depends(get_current_user),
        user_id: str = Form(description='UUID4 пользователя')):
    await user_get(user.get('id'))
    await user_get(user_id)
    await user_friend_add(user.get('id'), user_id, 0)
    return Created()
