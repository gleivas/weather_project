import json
from datetime import date, timedelta, datetime

import requests

from db import db
from weather.config import max_date_from_today, climatempo_token, climatempo_api_url
from weather.error_codes import ErrorCodes, InvalidRequest
from weather.models import Weather


def validate_date(from_date, to_date):
    # Verificando se o formato é valido
    try:
        from_date = datetime.strptime(from_date, '%Y-%m-%d')
        to_date = datetime.strptime(to_date, '%Y-%m-%d')
    except ValueError:
        raise InvalidRequest(ErrorCodes.DATE_FORMAT_INVALID)

    # Verificando se a segunda data não é maior que a primeira
    if from_date.date() > to_date.date():
        raise InvalidRequest(ErrorCodes.WRONG_DATE_POSITION)

    max_date = (date.today() + timedelta(max_date_from_today))

    # Verificando se a data não é anterior a hoje
    if from_date.date() < date.today():
        raise InvalidRequest(ErrorCodes.DATE_BEFORE_TODAY)

    # Verificando se a data nao excede a data limite
    if to_date.date() > max_date:
        raise InvalidRequest(ErrorCodes.DATE_LIMIT_INVALID)

    return from_date, to_date


def city_url(city_code):
    return '{climatempo_url}locale/city/{city_code}?token={token}'.format(
            city_code=city_code, token=climatempo_token, climatempo_url=climatempo_api_url
        )


def forecast_url(city_code):
    return '{climatempo_url}forecast/locale/{city_code}/days/15?token={token}'.format(
            city_code=city_code, token=climatempo_token, climatempo_url=climatempo_api_url
        )


def make_climatempo_request(url):
    request = requests.get(url)
    if request.status_code != 200:
        error_detail = json.loads(request.content.decode('utf-8')).get('detail')
        error = {'error': error_detail}
        raise InvalidRequest(error)
    return request.content


def save_request_data(data, city_code, from_date, to_date):
    all_data = json.loads(data.decode('utf-8')).get('data')
    get_data_information = False
    max_temp = None
    min_temp = None
    rain_forecast = None
    day_max_temp = None
    day_min_temp = None
    day_rain_forecast = None

    # A partir do momento que encontro a data de inicio começo a pegar as informacoes, na data final saio do loop
    for data in all_data:
        if data['date'] == from_date.strftime('%Y-%m-%d'):
            get_data_information = True

        if get_data_information:
            if not max_temp or int(data['temperature'].get('max')) > max_temp:
                max_temp = int(data['temperature'].get('max'))
                day_max_temp = data['date']
            if not min_temp or int(data['temperature'].get('min')) < min_temp:
                min_temp = int(data['temperature'].get('min'))
                day_min_temp = data['date']
            if not rain_forecast or int(data['rain'].get('precipitation')) > rain_forecast:
                rain_forecast = int(data['rain'].get('precipitation'))
                day_rain_forecast = data['date']

        if data['date'] == to_date.strftime('%Y-%m-%d'):
            break

    # Converto as datas para datetime
    day_max_temp = datetime.strptime(day_max_temp, '%Y-%m-%d').date()
    day_min_temp = datetime.strptime(day_min_temp, '%Y-%m-%d').date()
    day_rain_forecast = datetime.strptime(day_rain_forecast, '%Y-%m-%d').date()

    # Salvo as informacoes no banco de dados
    weather = Weather(
        city_code=city_code, from_date=from_date, to_date=to_date, day_max_temp=day_max_temp, max_temp=max_temp,
        day_min_temp=day_min_temp, min_temp=min_temp, day_rain_forecast=day_rain_forecast, rain_forecast=rain_forecast
    )
    db.session.add(weather)
    db.session.commit()

    return weather


def format_response(weather):
    response = {
        'max_temp': {
            'day': weather.day_max_temp.strftime('%Y-%m-%d'),
            'value': weather.max_temp
        },
        'min_temp': {
            'day': weather.day_min_temp.strftime('%Y-%m-%d'),
            'value': weather.min_temp
        },
        'max_rain': {
            'day': weather.day_rain_forecast.strftime('%Y-%m-%d'),
            'value': weather.rain_forecast
        }
    }

    return response


def get_weather_conditions(city_code, from_date, to_date):
    # Valido se as datas estão corretas
    from_date, to_date = validate_date(from_date, to_date)

    # Procuro no banco de dados se já há as informaçoes que preciso
    weather = Weather.query.filter_by(
        city_code=city_code, from_date=from_date, to_date=to_date
    ).first()

    # Caso não exista irei consumir a api do Climatempo
    if not weather:

        # Faço um primeiro request para saber se o city code existe
        url = city_url(city_code)
        make_climatempo_request(url)

        # E agora o request para extrair as informacoes necessarias
        url = forecast_url(city_code)
        data = make_climatempo_request(url)

        # Trato a data recebida de acordo com o necessario e as salvo no db
        weather = save_request_data(data, city_code, from_date, to_date)

    # Formato as informaçoes para a resposta
    response = format_response(weather)

    return response
