from datetime import timedelta, date
from uuid import uuid4

import asyncpg
from fastapi import APIRouter, Depends, Form, status
from fastapi.responses import JSONResponse
from pydantic import EmailStr

from app import schemes
from app.database import DataBase
from app.exceptions import BadRequest, NotFound
from app.queries import q_admin, q_adv, q_courses, q_groups, q_teachers, q_topics, q_users, q_users_advs
from app.queries import q_users_courses, q_users_friends, q_users_groups, q_users_topics, q_videos
from app.user_hash import get_hashed_password, verify_password, create_access_token, get_current_user
from app.utils import format_record, format_records

router = APIRouter(prefix='/user', tags=['Пользователи'])


@router.post('/sign_up', summary='Регистрация нового пользователя')
async def func(
        email: EmailStr = Form(title='Электронная почта'),
        password: str = Form(title='Пароль'),
        firstname: str = Form(None, title='Имя'),
        lastname: str = Form(None, title='Фамилия')
) -> JSONResponse:
    uuid = str(uuid4())
    while await DataBase.fetchrow(f'SELECT * FROM users WHERE id = ($1)', uuid):
        uuid = str(uuid4())
    user = dict(id=uuid, email=email, password=get_hashed_password(password), scores=0, firstname=firstname,
                lastname=lastname)
    await q_users.user_add(**user)
    access_token = create_access_token(subject=dict(dub=uuid), expires_delta=timedelta(minutes=44640))
    content = dict(access_token=access_token, token_type='bearer')
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=content)


@router.post('/login', summary='Авторизация пользователя')
async def func(
        username: EmailStr = Form(description='Электронная почта'),
        password: str = Form(description='Пароль')
) -> JSONResponse:
    user = await DataBase.fetchrow(f'SELECT * FROM users WHERE email = ($1)', username)
    if not user:
        raise NotFound('Пользователь не найден!')
    if not verify_password(password, user.get('password')):
        raise BadRequest('Неверная почта или пароль!')
    access_token = create_access_token(subject=user.get('id'), expires_delta=timedelta(minutes=44640))
    content = dict(access_token=access_token, token_type='bearer')
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@router.get('/account', summary='Полная информация о пользователе', response_model=schemes.UserComplex)
async def func_9(user: asyncpg.Record = Depends(get_current_user)):
    user_id = user.get('id')
    advs = [await q_adv.adv_get(adv.get('advancement_id'))
            for adv in await q_users_advs.user_adv_list(user_id)]
    courses = [await q_courses.course_get(course.get('course_id'))
               for course in await q_users_courses.user_course_list(user_id)]
    friends = [await q_users.user_get(friend.get('friend_id'))
               for friend in await q_users_friends.user_friend_list(user_id)]
    groups = [await q_groups.group_get(qroup.get('group_id'))
              for qroup in await q_users_groups.user_group_list(user_id)]
    topics = [await q_topics.topic_get(topic.get('topic_id'))
              for topic in await q_users_topics.user_topic_list(user.get('id'))]
    return schemes.UserComplex(
        user=format_record(user, schemes.UserBase),
        advs=format_records(advs, schemes.AdvBase),
        courses=format_records(courses, schemes.UserCourse),
        friends=format_records(friends, schemes.UserFriend),
        groups=format_records(groups, schemes.UserGroup),
        topics=format_records(topics, schemes.TopicBase)
    )


@router.get('/list', summary='Список всех пользователей', response_model=list[schemes.UserComplex])
async def func():
    return [await func_9(u) for u in await q_users.user_list()]


@router.post('/edit', summary='Редактирует информацию о пользователе [ВЛАДЕЛЕЦ]', response_model=schemes.Updated)
async def func(
        user: asyncpg.Record = Depends(get_current_user),
        email: EmailStr = Form(None, description='Электронная почта'),
        nickname: str = Form(None, description='Псевдоним'),
        scores: int = Form(None, description='Баллы'),
        firstname: str = Form(None, description='Имя'),
        lastname: str = Form(None, description='Фамилия'),
        patronymic: str = Form(None, description='Отчество'),
        avatar: str = Form(None, description='Аватарка'),
        birthday: date = Form(None, description='День Рожденья пользователя'),
        phone: str = Form(None, description='Телефон'),
        gender: str = Form(None, description='Пол'),
        profession: str = Form(None, description='Профессия (Курс/Направление/Класс)'),
        company: str = Form(None, description='Компание (Университет/Школа)')
):
    await q_users.user_edit(
        uuid=user.get('id'), email=email, nickname=nickname, scores=scores, firstname=firstname, lastname=lastname,
        patronymic=patronymic, avatar=avatar, birthday=birthday, phone=phone, gender=gender, profession=profession,
        company=company)
    return schemes.Updated()


@router.delete('/del', summary='Удаляет пользователя', response_model=schemes.Deleted)
async def func(user: asyncpg.Record = Depends(get_current_user)):
    await q_users.user_del(user.get('id'))
    return schemes.Deleted()
