import os

secret_key = os.getenv('SECRET_KEY', 'dev')
climatempo_token = os.getenv('CLIMATEMPO_TOKEN')
database_uri = 'sqlite:////tmp/weather.db'
track_modifications = False
max_date_from_today = 7
climatempo_api_url = 'http://apiadvisor.climatempo.com.br/api/v1/'
