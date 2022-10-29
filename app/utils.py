from typing import Type

import asyncpg
from pydantic import BaseModel


def format_record(record, model):
    """
    Преобразует данные таблицы в модель ответа.

    :param record: Данные таблицы.
    :param model: Модель ответа.
    :return: Преобразованные данные.
    """
    if not record:
        return None
    return model(**record)


def format_records(records, model):
    """
    Преобразует список данных таблицы в модель ответа.

    :param records: Список данных таблицы.
    :param model: Модель ответа.
    :return: Список преобразованных данных.
    """
    if not records:
        return list()
    return list(map(lambda x: format_record(x, model), records))


def clear_none(old_dict: dict) -> dict:
    """
    Возвращает новый словарь без Null значений.
    """
    new_dict = dict()
    for key in old_dict:
        if old_dict.get(key) is not None:
            new_dict[key] = old_dict.get(key)
    return new_dict


def sql_update(table: str, **kwargs) -> str:
    """
    Генерирует sql запрос обновления данных в таблице.

    :param table: Название таблицы.
    :param kwargs: Столбцы и их значения.
    :return: sql-запрос
    """
    kwargs = clear_none(kwargs)
    keys = list(kwargs.keys())
    columns = ", ".join([f'{keys[i]} = (${i + 2})' for i in range(len(kwargs))])
    if len(columns) == 0:
        return ''
    else:
        return f'UPDATE {table} SET {columns} WHERE "id" = ($1)'
