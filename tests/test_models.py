from tests.conftest import weather_example

weather = weather_example()


def test_new_user(new_weather):
    """
    GIVEN the Weather model
    WHEN a new Weather is created
    THEN check the city_code, from_date, to_date, day_max_temp, max_temp, day_min_temp,
     min_temp, day_rain_forecast and rain_forecast defined correctly
    """
    assert new_weather.city_code == weather.get('city_code')
    assert new_weather.from_date == weather.get('from_date')
    assert new_weather.to_date == weather.get('to_date')
    assert new_weather.day_max_temp == weather.get('day_max_temp')
    assert new_weather.max_temp == weather.get('max_temp')
    assert new_weather.day_min_temp == weather.get('day_min_temp')
    assert new_weather.min_temp == weather.get('min_temp')
    assert new_weather.day_rain_forecast == weather.get('day_rain_forecast')
    assert new_weather.rain_forecast == weather.get('rain_forecast')
