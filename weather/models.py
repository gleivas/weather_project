from db import db


class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_code = db.Column(db.Integer, nullable=False)
    from_date = db.Column(db.DateTime, nullable=False)
    to_date = db.Column(db.DateTime, nullable=False)
    day_max_temp = db.Column(db.DateTime, nullable=False)
    max_temp = db.Column(db.Integer, nullable=False)
    day_min_temp = db.Column(db.DateTime, nullable=False)
    min_temp = db.Column(db.Integer, nullable=False)
    day_rain_forecast = db.Column(db.DateTime, nullable=False)
    rain_forecast = db.Column(db.Integer, nullable=False)
