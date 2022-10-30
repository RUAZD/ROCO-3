from fastapi import APIRouter, Depends, Form

from app.queries import *
from app.schemes import *
from app.user_hash import get_current_user
from app.utils import format_record, format_records

router = APIRouter(prefix='/user/topics', tags=['Пользователь и темы интересов'])


@router.post('/add', summary='Добавить тему интересов', response_model=Created)
async def func(
        user: asyncpg.Record = Depends(get_current_user),
        topic_id: int = Form(description='ID темы интересов')):
    await user_get(user.get('id'))
    await topic_get(topic_id)
    await user_topic_add(user.get('id'), topic_id)
    return Created()
