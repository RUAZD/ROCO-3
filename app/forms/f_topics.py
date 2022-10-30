import asyncpg
from fastapi import APIRouter, Depends, Form

from app.utils import format_records
from app import schemes
from app.queries import q_topics, q_admin
from app.user_hash import get_current_user

router = APIRouter(prefix='/topic', tags=['Темы интересов [Редактируются администратором]'])


@router.post('/create', summary='Создание новой темы интересов [ADMIN]', response_model=schemes.Created)
async def func(admin: asyncpg.Record = Depends(get_current_user),
               name: str = Form(description='Название новой темы интересов')) -> schemes.Created:
    await q_admin.admin_add(admin.get('id'))
    await q_topics.topic_add(name)
    return schemes.Created()


@router.get('/list', summary='Список всех тем интересов [ALL]', response_model=list[schemes.TopicBase])
async def func(): return format_records(await q_topics.topic_list(), schemes.TopicBase)


@router.put('/topic/edit_name', summary='Изменение названия темы интересов [ADMIN]', response_model=schemes.Updated)
async def func(admin: asyncpg.Record = Depends(get_current_user),
               topic_id: int = Form(description='ID темы интересов'),
               name: str = Form(description='Новое название темы интересов')) -> schemes.Updated:
    await q_admin.admin_add(admin.get('id'))
    await q_topics.topic_edit(topic_id, name)
    return schemes.Updated()


@router.delete('/del', summary='Удаление темы интересов [ADMIN]', response_model=schemes.Deleted)
async def func(user: asyncpg.Record = Depends(get_current_user),
               topic_id: int = Form(description='ID темы интересов')) -> schemes.Deleted:
    await q_admin.admin_add(user.get('id'))
    await q_topics.topic_del(topic_id)
    return schemes.Deleted()
