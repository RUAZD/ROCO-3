from fastapi import APIRouter, Depends, Form

from app.queries import *
from app.schemes import *
from app.user_hash import get_current_user
from app.utils import format_record, format_records

router = APIRouter(prefix='/video', tags=['Видеоролики'])


@router.post('/publish', summary='Публикация нового видеоролика [TEACHER]', response_model=Created)
async def func(
        teacher: asyncpg.Record = Depends(get_current_user),
        link: str = Form(description='Ссылка на видеоролик'),
        title: str = Form(description='Название видеоролика'),
        description: str = Form(None, description='Описание видеоролика')
) -> Created:
    await teacher_get(teacher.get('id'))
    await video_add(link, title, description, teacher.get('id'))
    return Created()


@router.get('/list', summary='Список всех видеороликов', response_model=list[VideoComplex])
async def func():
    out = list()
    for video in await video_list():
        obj_video = await video_get(video.get('ID'))
        obj_teacher = await user_get(video.get('creator_id'))
        fr_video = format_record(obj_video, VideoBase)
        fr_creator = format_record(obj_teacher, UserTeacherBase)
        cpx = VideoComplex(video=fr_video, creator=fr_creator)
        out.append(cpx)
    return out


@router.put('/edit', summary='Изменение данных о видеоролике [TEACHER]', response_model=Updated)
async def func(
        teacher: asyncpg.Record = Depends(get_current_user),
        video_id: int = Form(description='ID'),
        title: str = Form(None, description='Название'),
        description: str = Form(None, description='Описание')
) -> Updated:
    await teacher_get(teacher.get('id'))
    if (await video_get(video_id)).get('creator_id') != teacher.get('id'):
        raise Forbidden()
    await video_edit(video_id, title, description)
    return Updated()


@router.delete('/del', summary='Удаление видеоролика [TEACHER]', response_model=Deleted)
async def func(
        teacher: asyncpg.Record = Depends(get_current_user),
        video_id: int = Form(description='ID')
) -> Deleted:
    if (await video_get(video_id)).get('creator_id') != teacher.get('id'):
        raise Forbidden()
    await video_del(video_id)
    return Deleted()
