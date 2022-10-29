import asyncpg
from fastapi import APIRouter, Depends, Form

from app import schemes
from app.database import DataBase
from app.utils import format_record, format_records
from app.queries import q_teachers, q_groups, q_users, q_users_groups
from app.user_hash import get_current_user

router = APIRouter(prefix='/group', tags=['Группы'])


@router.post('/create', summary='Создание новой группы [TEACHER]', response_model=schemes.Created)
async def func(
        teacher: asyncpg.Record = Depends(get_current_user),
        name: str = Form(description='Название')
) -> schemes.Created:
    await q_teachers.teacher_get(teacher.get('id'))
    await q_groups.group_add(name, teacher.get('id'))
    return schemes.Created()


@router.get('/list', summary='Список всех групп', response_model=list[schemes.GroupComplex])
async def func():
    return [schemes.GroupComplex(
        group=format_record(group, schemes.GroupBase),
        users=format_records([await q_users.user_get(u.get('user_id'))
                              for u in await q_users_groups.group_users_list(group.get('id'))],
                             schemes.UserBase),
        teacher=format_record(await q_users.user_get(group.get('teacher_id')), schemes.UserTeacherBase))
        for group in await q_groups.group_list()]


@router.delete('/disband', summary='Расформировать группу [TEACHER]', response_model=schemes.Deleted)
async def func(
        teacher: asyncpg.Record = Depends(get_current_user),
        group_id: int = Form(description='ID группы')
) -> schemes.Deleted:
    await q_teachers.teacher_get(teacher.get('id'))
    await q_groups.group_get(group_id)
    await DataBase.execute('DELETE FROM "groups" WHERE id = ($1)', group_id)
    return schemes.Deleted()
