import asyncpg
from fastapi import APIRouter, Depends, Form

from app.utils import format_record, format_records
from app import schemes
from app.queries import q_teachers, q_admin, q_users, q_courses, q_videos, q_groups
from app.user_hash import get_current_user

router = APIRouter(prefix='/teacher', tags=['Преподаватели'])


@router.post('/create', summary='Сделать пользователя преподавателем [ADMIN]', response_model=schemes.Created)
async def func(
        admin: asyncpg.Record = Depends(get_current_user),
        user_id: str = Form(description='UUID4 пользователя')
) -> schemes.Created:
    await q_admin.admin_get(admin.get('id'))
    await q_users.user_get(user_id)
    await q_teachers.teacher_add(user_id)
    return schemes.Created()


@router.get('/list', summary='Список преподавателей', response_model=list[schemes.TeacherComplex])
async def func():
    return [schemes.TeacherComplex(
        teacher=format_record(await q_users.user_get(T.get('id')), schemes.UserTeacherBase),
        courses=format_records(await q_courses.teacher_course_list(T.get('id')), schemes.CourseBase),
        videos=format_records(await q_videos.teacher_video_list(T.get('id')), schemes.VideoBase),
        groups=format_records(await q_groups.teacher_group_list(T.get('id')), schemes.GroupBase))
        for T in await q_teachers.teacher_list()]


# @router.get('/info', summary='Информация о преподавателе [ALL]', response_model=list[TeacherComplex])
# async def func(teacher_id: str = Form(description='UUID4 преподавателя')):
#     # TODO Инфа о преподе
#     pass


# @router.get('/account', summary='Личный кабинет преподавателя [TEACHER]', response_model=list[TeacherComplex])
# async def func(teacher: asyncpg.Record = Depends(get_current_user)):
#     # TODO Аккаунт препода
#     pass


@router.delete('/leave', summary='Уйти с поста преподавателя [TEACHER]', response_model=schemes.Deleted)
async def func(teacher: asyncpg.Record = Depends(get_current_user)) -> schemes.Deleted:
    await q_teachers.teacher_get(teacher.get('id'))
    await q_teachers.teacher_del(teacher.get('id'))
    return schemes.Deleted()


@router.delete('/remove', summary='Снять преподавателя [ADMIN]', response_model=schemes.Deleted)
async def func(
        admin: asyncpg.Record = Depends(get_current_user),
        teacher_id: str = Form(description='UUID4 преподавателя')
) -> schemes.Deleted:
    await q_admin.admin_get(admin.get('id'))
    await q_teachers.teacher_get(teacher_id)
    await q_teachers.teacher_del(teacher_id)
    return schemes.Deleted()
