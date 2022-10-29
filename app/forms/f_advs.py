import asyncpg
from fastapi import APIRouter, Depends, Form

from app import schemes
from app.queries import q_admin, q_adv
from app.user_hash import get_current_user
from app.utils import format_records

router = APIRouter(prefix='/advancements', tags=['Достижения'])


@router.post('/create', summary='Создание нового достижения [ADMIN]', response_model=schemes.Created)
async def func(
        admin: asyncpg.Record = Depends(get_current_user),
        title: str = Form(description='Название достижения'),
        description: str = Form(None, description='Описание достижения'),
        level: str = Form(None, description='Уровень достижения')
) -> schemes.Created:
    await q_admin.admin_add(admin.get('id'))
    await q_adv.adv_add(title, description, level)
    return schemes.Created()


@router.get('/list', summary='Список всех достижений', response_model=list[schemes.AdvBase])
async def func(): return format_records(await q_adv.adv_list(), schemes.AdvBase)


@router.put('/edit', summary='Изменение данных о достижении [ADMIN]', response_model=schemes.Updated)
async def func(
        admin: asyncpg.Record = Depends(get_current_user),
        adv_id: int = Form(description='ID достижения'),
        title: str = Form(None, description='Название достижения'),
        description: str = Form(None, description='Описание достижения'),
        level: str = Form(None, description='Уровень достижения')
) -> schemes.Updated:
    await q_admin.admin_add(admin.get('id'))
    await q_adv.adv_edit(adv_id, title=title, description=description, level=level)
    return schemes.Updated()


@router.delete('/del', summary='Удаление достижения [ADMIN]', response_model=schemes.Deleted)
async def func(
        admin: asyncpg.Record = Depends(get_current_user),
        adv_id: int = Form(description='ID достижения')
) -> schemes.Deleted:
    await q_admin.admin_add(admin.get('id'))
    await q_adv.adv_del(adv_id)
    return schemes.Deleted()
