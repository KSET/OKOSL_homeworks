from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_user import UserManager
from flask_admin import Admin
from .admin import SecureAdminView

app = Flask(__name__)
app.config.from_object(Config)
# disable fsqla's event system - unused, but it wastes resources if enabled
# more info: https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .models import User, Role, Homework, Task, Subtask, SolutionGroup, Solution, Remark, UserRoles, Student, SolvedHomework # noqa

model_list = [User, Role, Homework, Task, Subtask, SolutionGroup, Solution, Remark, UserRoles, Student, SolvedHomework]

user_manager = UserManager(app, db, User)

admin = Admin(app, name=app.config['APP_NAME'], template_mode='bootstrap3')

for model in model_list:
    admin.add_view(SecureAdminView(model, db.session, name=model.__tablename__))

from app import routes  # noqa
