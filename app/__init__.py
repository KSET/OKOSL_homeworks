from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_uploads import configure_uploads, UploadSet, IMAGES

app = Flask(__name__)
app.config.from_object(Config)
configure_uploads(app, UploadSet('images', IMAGES))
# disable fsqla's event system - unused, but if wastes resources if enabled
# more info: https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes  # noqa
