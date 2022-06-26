from flask import Flask

from bp_films.views import bp_films

app = Flask(__name__)

app.register_blueprint(bp_films)
app.config['JSON_SORT_KEYS'] = False

if __name__ == "__main__":
    app.run(debug=True)

