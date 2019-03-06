from datetime import timedelta

from tests.conftest import weather_example, get_api_url
from weather.error_codes import ErrorCodes

weather = weather_example()


def test_get_correct(test_client):
    """
    GIVEN the weather application
    WHEN the /api/v1/weather is requested (GET) with the right parameters
    THEN check if the response is valid
     """
    city_code = weather.get('city_code')
    from_date = weather.get('from_date').strftime('%Y-%m-%d')
    to_date = weather.get('to_date').strftime('%Y-%m-%d')
    url = get_api_url(city_code, from_date, to_date)
    response = test_client.get(url)
    assert response.status_code == 200
    assert b'max_rain' in response.data
    assert b'max_temp' in response.data
    assert b'min_temp' in response.data


def test_wrong_date_position(test_client):
    """
        GIVEN the weather application
        WHEN the /api/v1/weather is requested (GET) with the to_date earlier than the from_date
        THEN check if the response status is error and the error message is correct
         """
    city_code = weather.get('city_code'),
    from_date = weather.get('to_date').strftime('%Y-%m-%d')
    to_date = weather.get('from_date').strftime('%Y-%m-%d')
    url = get_api_url(city_code, from_date, to_date)
    response = test_client.get(url)
    assert response.status_code == 400
    assert str.encode(ErrorCodes.WRONG_DATE_POSITION) in response.data


def test_wrong_date_format(test_client):
    """
        GIVEN the weather application
        WHEN the /api/v1/weather is requested (GET) with the the date format wrong
        THEN check if the response status is error and the error message is correct
         """
    city_code = weather.get('city_code'),
    from_date = weather.get('from_date').strftime('%d-%m-%Y')
    to_date = weather.get('to_date').strftime('%d-%m-%Y')
    url = get_api_url(city_code, from_date, to_date)
    response = test_client.get(url)
    assert response.status_code == 400
    assert str.encode(ErrorCodes.DATE_FORMAT_INVALID) in response.data


def test_date_before_today(test_client):
    """
        GIVEN the weather application
        WHEN the /api/v1/weather is requested (GET) with the the date exceeded the previously chosen limit
        THEN check if the response status is error and the error message is correct
         """
    city_code = weather.get('city_code'),
    from_date = (weather.get('from_date') + timedelta(-1)).strftime('%Y-%m-%d')
    to_date = weather.get('to_date').strftime('%Y-%m-%d')
    url = get_api_url(city_code, from_date, to_date)
    response = test_client.get(url)
    assert response.status_code == 400
    assert str.encode(ErrorCodes.DATE_BEFORE_TODAY) in response.data


def test_date_exceed_limit(test_client):
    """
        GIVEN the weather application
        WHEN the /api/v1/weather is requested (GET) with the the date exceeded the previously chosen limit
        THEN check if the response status is error and the error message is correct
         """
    city_code = weather.get('city_code'),
    from_date = weather.get('from_date').strftime('%Y-%m-%d')
    to_date = (weather.get('to_date') + timedelta(1)).strftime('%Y-%m-%d')
    url = get_api_url(city_code, from_date, to_date)
    response = test_client.get(url)
    assert response.status_code == 400
    assert str.encode(ErrorCodes.DATE_LIMIT_INVALID) in response.data


def test_without_city_code_parameter(test_client):
    """
    GIVEN the weather application
    WHEN the /api/v1/weather is requested (GET) without the city_code parameter
    THEN check if the response status is error and the error message is correct
     """
    url = '/api/v1/weather?from_date={from_date}&to_date={to_date}'.format(
        from_date=weather.get('from_date').strftime('%Y-%m-%d'),
        to_date=weather.get('to_date').strftime('%Y-%m-%d')
    )
    response = test_client.get(url)
    assert response.status_code == 400
    assert str.encode(ErrorCodes.WRONG_REQUEST_PARAMETERS) in response.data


def test_without_from_date_parameter(test_client):
    """
    GIVEN the weather application
    WHEN the /api/v1/weather is requested (GET) without the from_date parameter
    THEN check if the response status is error and the error message is correct
     """
    url = '/api/v1/weather?city_code={city_code}&to_date={to_date}'.format(
        city_code=weather.get('city_code'),
        to_date=weather.get('to_date').strftime('%Y-%m-%d')
    )
    response = test_client.get(url)
    assert response.status_code == 400
    assert str.encode(ErrorCodes.WRONG_REQUEST_PARAMETERS) in response.data


def test_without_to_date_parameter(test_client):
    """
    GIVEN the weather application
    WHEN the /api/v1/weather is requested (GET) without the to_date parameter
    THEN check if the response status is error and the error message is correct
     """
    url = '/api/v1/weather?city_code={city_code}&from_date={from_date}'.format(
        city_code=weather.get('city_code'),
        from_date=weather.get('from_date').strftime('%Y-%m-%d')
    )
    response = test_client.get(url)
    assert response.status_code == 400
    assert str.encode(ErrorCodes.WRONG_REQUEST_PARAMETERS) in response.data
