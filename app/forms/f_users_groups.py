from fastapi import APIRouter, Depends, Form

from app.queries import *
from app.schemes import *
from app.user_hash import get_current_user
from app.utils import format_record, format_records

router = APIRouter(prefix='/user/group', tags=['Пользователь и группы'])


@router.post('/join', summary='Присоединитсья к группе', response_model=Created)
async def func(
        user: asyncpg.Record = Depends(get_current_user),
        group_id: int = Form(description='ID группы')):
    await user_get(user.get('id'))
    await group_get(group_id)
    await user_group_add(user.get('id'), group_id, 0)
    return Created()
