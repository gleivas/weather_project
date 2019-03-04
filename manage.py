from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from db import db
from weather.weather import weather_app


migrate = Migrate(weather_app, db)

manager = Manager(weather_app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
