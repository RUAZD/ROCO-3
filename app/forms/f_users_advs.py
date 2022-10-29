from fastapi import APIRouter, Depends, Form

from app.queries import *
from app.schemes import *
from app.user_hash import get_current_user
from app.utils import format_record, format_records

router = APIRouter(prefix='/user/advs', tags=['Пользователь и достижения'])


@router.post('/grant', summary='Выдать достижение пользователю', response_model=Created)
async def func(
        user_id: str = Form(title='UUID4 пользователя'),
        advancement_id: int = Form(title='ID достижения')):
    await user_adv_add(user_id, advancement_id)
    return Created()


@router.get('/list', summary='Список достижений пользователя', response_model=list[AdvBase])
async def func(user: asyncpg.Record = Depends(get_current_user)):
    out = list()
    for adv in await user_adv_list(user.get('id')):
        obj_adv = await adv_get(adv.get('id'))
        fr_adv = format_record(obj_adv, AdvBase)
        out.append(fr_adv)
    return out


@router.delete('/revoke', summary='Отозвать достижение пользователя', response_model=Deleted)
async def func(
        user_id: str = Form(title='UUID4 пользователя'),
        advancement_id: int = Form(title='ID достижения')):
    await user_get(user_id)
    await adv_get(advancement_id)
    await user_adv_del(user_id, advancement_id)
    return Deleted()
