from flask import jsonify, Flask
from flask_sqlalchemy import SQLAlchemy

from weather.blueprint import weather_api
from weather.config import secret_key, track_modifications, database_uri
from weather.error_codes import InvalidRequest

db = SQLAlchemy()


def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def initialize_weather_app(weather_app):
    db.init_app(weather_app)
    weather_app.register_blueprint(weather_api)
    weather_app.register_error_handler(InvalidRequest, handle_invalid_usage)


def create_weather_app(debug=False, testing=False):
    weather_app = Flask(__name__)
    weather_app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    weather_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = track_modifications
    weather_app.config['SECRET_KEY'] = secret_key
    weather_app.config['DEBUG'] = debug
    weather_app.config['TESTING'] = testing
    initialize_weather_app(weather_app)
    return weather_app
