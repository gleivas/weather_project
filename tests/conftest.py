from datetime import date, timedelta

import pytest

from weather.config import max_date_from_today
from weather.models import Weather
from weather import db, create_weather_app


def get_api_url(city_code, from_date, to_date):
    url = '/api/v1/weather?city_code={city_code}&from_date={from_date}&to_date={to_date}'.format(
        city_code=city_code,
        from_date=from_date,
        to_date=to_date
    )
    return url


def weather_example():
    today = date.today()
    response = {
        'city_code': 3477,
        'from_date': today,
        'to_date': (date.today() + timedelta(max_date_from_today)),
        'day_max_temp': today,
        'max_temp': 35,
        'day_min_temp': today,
        'min_temp': 15,
        'day_rain_forecast': today,
        'rain_forecast': 15
    }
    return response


@pytest.fixture(scope='module')
def new_weather():
    user = Weather(**weather_example())
    return user


@pytest.fixture(scope='module')
def test_client():
    weather_app = create_weather_app(debug=True, testing=True)
    testing_client = weather_app.test_client()
    ctx = weather_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture(scope='module')
def init_database():
    db.create_all()
    user1 = Weather(**weather_example())
    db.session.add(user1)
    db.session.commit()

    yield db

    db.drop_all()
