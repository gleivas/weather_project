from flask import request, Blueprint, jsonify, Flask
from flask_sqlalchemy import SQLAlchemy

from weather.error_codes import InvalidRequest, ErrorCodes
from weather.util import get_weather_conditions

db = SQLAlchemy()
weather_api = Blueprint('weather_api', __name__, url_prefix='/api/v1')

weather_app = Flask(__name__)
weather_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/weather.db'
weather_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@weather_app.errorhandler(InvalidRequest)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@weather_api.route('/weather')
def get_weather():
    city_code = request.args.get('city_code')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    if not city_code or not from_date or not to_date:
        raise InvalidRequest(ErrorCodes.WRONG_REQUEST_PARAMETERS)
    return jsonify(get_weather_conditions(city_code, from_date, to_date))


weather_app.register_blueprint(weather_api)
db.init_app(weather_app)
