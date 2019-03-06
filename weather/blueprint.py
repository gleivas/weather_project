from flask import Blueprint, request, jsonify

from weather.error_codes import InvalidRequest, ErrorCodes
from weather.util import get_weather_conditions

weather_api = Blueprint('weather_api', __name__, url_prefix='/api/v1')


@weather_api.route('/weather')
def get_weather():
    city_code = request.args.get('city_code')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    if not city_code or not from_date or not to_date:
        raise InvalidRequest(ErrorCodes.WRONG_REQUEST_PARAMETERS)
    return jsonify(get_weather_conditions(city_code, from_date, to_date))
