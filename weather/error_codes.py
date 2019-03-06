from datetime import date
from datetime import timedelta

from weather.config import max_date_from_today


class InvalidRequest(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.message
        return rv


class ErrorCodes:

    DATE_FORMAT_INVALID = 'The date format is invalid, it should be YYYY-MM-DD'

    DATE_LIMIT_INVALID = 'The date can\'t be more than {}'.format(
        (date.today() + timedelta(max_date_from_today)).strftime('%Y-%m-%d')
    )

    WRONG_DATE_POSITION = 'The first date should be before the second date'

    WRONG_REQUEST_PARAMETERS = 'Wrong request parameters, it should contain city_code, from_date and to_date'

    DATE_BEFORE_TODAY = 'The date can\'t be less than {}'.format(
        (date.today()).strftime('%Y-%m-%d')
    )
