import sqlite3
from collections import Counter
from flask import json


def connection():
    with sqlite3.connect("./netflix.db") as con:
        cur = con.cursor()
    return cur


def search_by_title(title):
    """
    Поиск названию фильма
    """
    cur = connection()
    sqlite_query = f"""
                    SELECT title, country, release_year, listed_in, description
                    FROM netflix
                    WHERE title LIKE '%{title}%'
                    ORDER BY release_year DESC 
                    LIMIT 1
                    """

    cur.execute(sqlite_query)
    result = cur.fetchall()

    dict_data = {
        "title": result[0][0],
        "country": result[0][1],
        "release_year": result[0][2],
        "genre": result[0][3],
        "description": result[0][4]
    }

    return dict_data


def search_by_years(year_1, year_2):
    """
    Поиск по диапазону лет фильма
    """
    cur = connection()
    sqlite_query = f"""
                    SELECT title, release_year
                    FROM netflix
                    WHERE release_year BETWEEN {year_1} AND {year_2}
                    ORDER BY release_year
                    LIMIT 100
                        """

    cur.execute(sqlite_query)
    result = cur.fetchall()

    list_of_films = []

    for i in range(len(result)):
        dict_data = {
            "title": result[i][0],
            "release_year": result[i][1]
        }
        list_of_films.append(dict_data)

    return list_of_films


def search_by_rating(list_of_rating):
    """
    Поиск фильма по возрастному рейтингу
    """
    cur = connection()
    sqlite_query = f"""
                    SELECT title, rating, description
                    FROM netflix
                    WHERE rating IN {list_of_rating}
                    """
    cur.execute(sqlite_query)
    result = cur.fetchall()

    list_of_films = []
    for i in range(len(result)):
        dict_data = {
            "title": result[i][0],
            "rating": result[i][1],
            "description": result[i][2]
        }
        list_of_films.append(dict_data)

    return list_of_films


def search_by_genre(listed_in):
    """
    Поиск фильма по жанру
    """
    cur = connection()
    sqlite_query = f"""
                    SELECT title, listed_in, date_added, description
                    FROM netflix
                    WHERE listed_in LIKE '%{listed_in}%'
                    ORDER BY date_added DESC 
                    LIMIT 10
                    """
    cur.execute(sqlite_query)
    result = cur.fetchall()

    list_of_films = []
    for i in range(len(result)):
        dict_data = {
            "title": result[i][0],
            "description": result[i][3]
        }
        list_of_films.append(dict_data)

    return list_of_films


def search_actors(one, two):
    """
    Функция получает имена двух актёров, сохраняет
    всех актёров из колонки "cast" и возвращает список тех,
    кто играет с ними в паре больше 2 раз
    """
    cur = connection()
    sqlite_query = f"""
                    SELECT "cast"
                    FROM netflix
                    WHERE "cast" LIKE '%{one}%'
                    AND "cast" LIKE '%{two}%'
                    """
    cur.execute(sqlite_query)
    result = cur.fetchall()

    #  Сохраняем всех актёров в список
    full_cast = []
    for i in result:
        for actor in i:
            full_cast.append(actor)

    #  Преобразуем в корректный список без лишних знаков
    full_cast_str = ", ".join(full_cast)
    full_cast_list = full_cast_str.split(", ")

    #  Подсчитываем кол-во повторений и добавляем актёров в новый список
    #  (тех, кто присутствует больше 2 раз)
    counter = Counter(full_cast_list)
    new_result = []
    for k, v in counter.items():
        if v >= 2 and k != one and k != two:
            new_result.append(k)

    return new_result


def search_film_by_type_year_ganre(type, release_year, listed_in):
    """
    В функцию передается тип, год выпуска и жанр фильма.
    На выходе получается список названий картин с их
    описаниями в JSON
    """
    cur = connection()
    sqlite_query = f"""
                    SELECT title, "type", release_year, listed_in, description 
                    FROM netflix
                    WHERE "type" == '{type}'
                    AND release_year == '{release_year}'
                    AND listed_in LIKE '%{listed_in}%'
                    """
    cur.execute(sqlite_query)
    result = cur.fetchall()

    list_of_films = []
    for i in range(len(result)):
        dict_data = {
            "title": result[i][0],
            "description": result[i][4]
        }
        list_of_films.append(dict_data)

    return json.dumps(list_of_films)



