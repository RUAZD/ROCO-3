import asyncpg
from fastapi import APIRouter, Depends, Form

from app import schemes
from app.exceptions import Forbidden
from app.queries import q_courses, q_teachers
from app.user_hash import get_current_user
from app.utils import format_records, format_record

router = APIRouter(prefix='/course', tags=['Обучающие курсы'])


@router.post('/create', summary='Создание нового курса [TEACHER]', response_model=schemes.Created)
async def func(
        teacher: asyncpg.Record = Depends(get_current_user),
        name: str = Form(description='Название'),
        description: str = Form(None, description='Описание')) -> schemes.Created:
    await q_teachers.teacher_get(teacher.get('id'))
    await q_courses.course_add(name, description, teacher.get('id'))
    return schemes.Created()


@router.get('/list', summary='Список всех курсов', response_model=list[schemes.CourseComplex])
async def func():
    out = list()
    for C in await q_courses.course_list():
        teacher = await q_teachers.teacher_get(C.get('id'))
        out.append(schemes.CourseComplex(
            course=format_record(C, schemes.CourseBase),
            teacher=format_record(teacher, schemes.UserTeacherBase)
        ))
    return format_records(await q_courses.course_list(), schemes.CourseComplex)


@router.put('/edit', summary='Изменение данных о курсе [TEACHER]', response_model=schemes.Updated)
async def func(
        teacher: asyncpg.Record = Depends(get_current_user),
        course_id: int = Form(description='ID'),
        name: str = Form(None, description='Название'),
        description: str = Form(None, description='Описание')) -> schemes.Updated:
    await q_teachers.teacher_get(teacher.get('id'))
    if (await q_courses.course_get(course_id)).get('teacher_id') != teacher.get('id'):
        raise Forbidden()
    await q_courses.course_edit(course_id, teacher.get('id'), name=name, description=description)
    return schemes.Updated()


@router.delete('/del', summary='Удаление курса [TEACHER]', response_model=schemes.Deleted)
async def func(teacher: asyncpg.Record = Depends(get_current_user),
               course_id: int = Form(description='ID курса')):
    await q_teachers.teacher_get(teacher.get('id'))
    if (await q_courses.course_get(course_id)).get('teacher_id') != teacher.get('id'):
        raise Forbidden()
    await q_courses.course_del(course_id)
    return schemes.Deleted()
