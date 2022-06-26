from flask import Blueprint, jsonify

from bp_films.utils import search_by_title, search_by_years, search_by_rating, search_by_genre

bp_films = Blueprint("bp_api", __name__)


@bp_films.route("/movie/<title>/")
def movie_by_title(title):
    """
    Вьюшка поиска фильма по названию
    """
    film = search_by_title(title.lower())
    return jsonify(film)


@bp_films.route("/movie/<int:year_1>/to/<int:year_2>")
def movie_by_years(year_1, year_2):
    """
    Вьюшка поиска фильма по названию
    """
    films = search_by_years(year_1, year_2)
    return jsonify(films)


@bp_films.route("/movie/rating/<rating>")
def movie_by_rating(rating):
    """
    Вьюшка поиска фильма по возрастному рейтингу
    """
    if rating == "children":
        list_of_rating = ("""('G')""")
        films = search_by_rating(list_of_rating)
        return jsonify(films)

    elif rating == "family":
        list_of_rating = ("""('G','PG','PG-13')""")
        films = search_by_rating(list_of_rating)
        return jsonify(films)

    elif rating == "adult":
        list_of_rating = ("""('R','NC-17')""")
        films = search_by_rating(list_of_rating)
        return jsonify(films)
    else:
        return "Неверно указан rating"


@bp_films.route("/genre/<genre>")
def movie_by_genre(genre):
    """
    Вьюшка поиска фильма по названию
    """
    films = search_by_genre(genre.lower())
    return jsonify(films)

