import os

climatempo_token = os.getenv('CLIMATEMPO_TOKEN')
max_date_from_today = 7


def city_url(city_code):
    return 'http://apiadvisor.climatempo.com.br/api/v1/locale/city/{city_code}?token={token}'.format(
            city_code=city_code, token=climatempo_token
        )


def forecast_url(city_code):
    return 'http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/{city_code}/days/15?token={token}'.format(
            city_code=city_code, token=climatempo_token
        )
