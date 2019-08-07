from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_user import UserManager
from datetime import datetime


app = Flask(__name__)
app.config.from_object(Config)
# disable fsqla's event system - unused, but if wastes resources if enabled
# more info: https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .models import User, Role # noqa

user_manager = UserManager(app, db, User)
db.create_all()


# Create 'okosl@kset.org' user with no roles
if not User.query.filter(User.email == 'okosl@kset.org').first():
    user = User(
        email='okosl@kset.org',
        email_confirmed_at=datetime.utcnow(),
        password=user_manager.hash_password('Password1'),
    )
    db.session.add(user)
    db.session.commit()

# Create 'rincewind@kset.org' user with 'Admin' and 'Agent' roles
if not User.query.filter(User.email == 'rincewind@kset.org').first():
    user = User(
        email='rincewind@kset.org',
        email_confirmed_at=datetime.utcnow(),
        password=user_manager.hash_password('Password1'),
    )
    user.roles.append(Role(name='Admin'))
    db.session.add(user)
    db.session.commit()

from app import routes  # noqa
