from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from db import db
from weather import create_weather_app

weather_app = create_weather_app()
migrate = Migrate(weather_app, db)

manager = Manager(weather_app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
