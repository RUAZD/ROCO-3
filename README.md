<h3>Команда ROCO</h3>
<h1 align="center">
  <br>
  <br>
  <br>
  <a href="#">Микролернинг в образовании. Тик ток «по-научному»</a>
  <br>
</h1>

<h4 align="center"></h4>

<p align="center">
  <a href="#фичи">Фичи</a> •
  <a href="#стек">Стек</a> •
  <a href="#команда">Команда</a> •
  <a href="#запуск">Запуск</a> •  
  <a href="#архитектура решения">Архитектура</a>
</p>



## Фичи

- Личный кабинет пользователя и использование сайтом
1.Внедрение системы достижений
2. Личный кабинет ученика и преподавателя
3. Напоминания про здоровье
4. Улучшения знакомства с сайтом
5. Частичное внедрение социальных сетей
6. Создание системы рейтинга для пользователей
7. Создание системы баллов
8. Внедрение деловых игр и соревнований по дисциплинам
9. Возможность получения бесплатного курса при сдаче экзамена на 100%.
10. Микрооткрытия - создание короткометражных (до 2 мин.) видео на научные темы
11. Создание маскота



## Стек

Этот проект написан с помощью:

- [Python 3.9/10](https://www.python.org/)
- [fastapi](https://fastapi.tiangolo.com)
- [uvicorn](https://www.uvicorn.org)
- [asyncpg](https://magicstack.github.io/asyncpg/current/)
- [passlib](https://pypi.org/project/passlib/)
- [python-jose](https://pypi.org/project/python-jose/)
- [email-validator](https://pypi.org/project/email-validator/)
- [python-multipart](https://pypi.org/project/python-multipart/)
- [bcrypt](https://pypi.org/project/bcrypt/)



## Архитектура решения

База данных:

<p align="center">
<img width="70%" src="https://github.com/RUAZD/ROCO-3-FastAPI/blob/main/architecture.png">
</p>


## Запуск

- Установи Python 3.9 или 3.10
- Установить PostgreSQL 15
- Войти в консоль и создать базу данных
- Установи <a href="#стек">библиотеки</a>
- Виртуальные переменные окружения:
1) DATABASE_URL_s = postgres://{user}:{password}@localhost:5432/{название database} пример: postgres://postgres:12345678@localhost:5432/database1
2) JWT_SECRET_KEY = pouier
3) TIMEOUT = 44640


## Команда 

Микролернинг в образовании. Тик ток "по-научному" разработан командой ROCO в рамках Технохакатона

ROCO - это мы:
- Долинин Никита - продукт-менеджер
- Кондратьева Полина - верстальщик
- Ботова Юлия - UI&UX designer
- Тропина Марина - Специалист по маркетингу
- Зайцев Алексей - backend разработчик
