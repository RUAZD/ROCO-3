from datetime import date, datetime

from pydantic import BaseModel, Field, EmailStr


class AdvBase(BaseModel):
    """ Базовая информация о достижении. """
    id: int = Field(None, description='ID достижения')
    title: str = Field(None, description='Название достижения')
    description: str = Field(None, description='Описание достижения')
    level: str = Field(None, description='Уровень достижения')


class CourseBase(BaseModel):
    """ Базовая информация о курсе. """
    id: int = Field(None, description='ID курса')
    name: str = Field(None, description='Название обучающего курса')
    description: str = Field(None, description='Описание обучающего курса')


class GroupBase(BaseModel):
    """ Базовая информация о группе. """
    id: int = Field(None, description='ID группы')
    name: str = Field(None, description='Название группы')


class TopicBase(BaseModel):
    """ Базовая информация о теме интересов. """
    id: int = Field(None, description='ID')
    name: str = Field(None, description='Название')


class VideoBase(BaseModel):
    """ Базовая информация о видео. """
    id: int = Field(None, description='ID видеоролика')
    link: str = Field(None, description='Ссылка на видеоролик')
    title: str = Field(None, description='Название видеоролика')
    description: str = Field(None, description='Описание видеоролика')
    posting_time: datetime = Field(None, description='Время публикации видеоролика')


class UserBase(BaseModel):
    """ Базовая информация о пользователе. """
    id: str = Field(None, description='UUID4 пользователя')
    email: EmailStr = Field(None, description='Почта пользователя')
    nickname: str = Field(None, description='Псевдоним пользователя')
    scores: int = Field(None, description='Баллы пользователя')
    firstname: str = Field(None, description='Имя пользователя')
    lastname: str = Field(None, description='Фамилия пользователя')
    patronymic: str = Field(None, description='Отчество пользователя')
    avatar: str = Field(None, description='Аватарка пользователя')
    birthday: date = Field(None, description='День Рожденья пользователя')
    phone: str = Field(None, description='Телефон пользователя')
    gender: str = Field(None, description='Пол пользователя')
    profession: str = Field(None, description='Профессия пользователя')
    company: str = Field(None, description='Компания, в которой работает пользователь')


class UserTeacherBase(BaseModel):
    """ Базовая информация о преподавателе. """
    id: str = Field(None, description='UUID4 преподавателя')
    email: EmailStr = Field(None, description='Почта преподавателя')
    nickname: str = Field(None, description='Псевдоним преподавателя')
    firstname: str = Field(None, description='Имя преподавателя')
    lastname: str = Field(None, description='Фамилия преподавателя')
    patronymic: str = Field(None, description='Отчество преподавателя')
    avatar: str = Field(None, description='Аватарка преподавателя')
    birthday: date = Field(None, description='День Рожденья преподавателя')
    phone: str = Field(None, description='Телефон преподавателя')
    profession: str = Field(None, description='Профессия преподавателя')
    company: str = Field(None, description='Компания, в которой работает преподаватель')


class UserCourse(BaseModel):
    state: int = Field(None, description='Номер статуса пользователя в курсе')
    course: CourseBase = Field(None, description='Информация о курсе')


class UserGroup(BaseModel):
    state: int = Field(None, description='Номер статуса пользователя в группе')
    group: GroupBase = Field(None, description='Информация о группе')


class UserFriend(BaseModel):
    state: int = Field(None, description='Номер статуса пользователя с другом')
    friend: UserBase = Field(None, description='Информация о друге')


class UserComplex(BaseModel):
    """ Полная информация о пользователе. """
    user: UserBase = Field(None, description='Информация о пользователе')
    advs: list[AdvBase] = Field(None, description='Достижения пользователя')
    courses: list[UserCourse] = Field(None, description='Информация о курсах пользователя')
    friends: list[UserFriend] = Field(None, description='Информация о друзьях пользователя')
    groups: list[UserGroup] = Field(None, description='Информация о группах пользователя')
    topics: list[TopicBase] = Field(None, title='Список тем интересов пользователя')


class GroupComplex(BaseModel):
    """ Информация о группе и её участниках. """
    group: GroupBase = Field(None, description='Информация о группе')
    users: list[UserBase] = Field(None, description='Информация о участниках группы')
    teacher: UserTeacherBase = Field(None, description='Информация о преподавателе')


class CourseComplex(BaseModel):
    """ Информация о курсе и его преподавателе. """
    course: CourseBase = Field(None, description='Информация о курсе')
    teacher: UserTeacherBase = Field(None, description='Информация о преподавателе')


class TeacherComplex(BaseModel):
    """ Полная информация о преподавателе """
    teacher: UserTeacherBase = Field(None, description='Информация о преподавателе')
    courses: list[CourseBase] = Field(None, description='Курсы преподавателя')
    videos: list[VideoBase] = Field(None, description='Видеоролики преподавателя')
    groups: list[GroupBase] = Field(None, description='Группы преподавателя')


class VideoComplex(BaseModel):
    """ Информация о видео и его авторе. """
    video: VideoBase = Field(None, description='Информация о видео')
    creator: UserTeacherBase = Field(None, description='Информация о авторе')


class Created(BaseModel):
    details: str = Field('Объект успешно создан!', title='Статус операции')


class Updated(BaseModel):
    details: str = Field('Объект успешно обновлён!', title='Статус операции')


class Joined(BaseModel):
    details: str = Field('Добавление прошло успешно!', title='Статус операции')


class Deleted(BaseModel):
    details: str = Field('Удаление прошло успешно!', title='Статус операции')
