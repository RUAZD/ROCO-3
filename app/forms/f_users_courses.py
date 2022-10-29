from fastapi import APIRouter, Depends, Form

from app.queries import *
from app.schemes import *
from app.user_hash import get_current_user
from app.utils import format_record, format_records

router = APIRouter(prefix='/user/course', tags=['Пользователь и курсы'])


@router.post('/join', summary='Присоединиться к курсу', response_model=Created)
async def func(
        user: asyncpg.Record = Depends(get_current_user),
        course_id: int = Form(title='ID курса')):
    await user_get(user.get('id'))
    await user_course_add(user.get('id'), course_id, 0)
    return Created()


# @router.get('/list', summary='Список курсов', response_model=list[UserCourse])
# async def func(user: asyncpg.Record = Depends(get_current_user)):
#     out = list()
#     for course in await user_course_list(user.get('id')):
#         obj_course = await course_get(course.get('course_id'))
#
#         fr_adv = format_record(obj_adv, UserCourse)
#         out.append(fr_adv)
#     return out
