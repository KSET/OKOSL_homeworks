import os


class Config(object):
    """
    This class contains configuration key-value pairs, for various features
    used throughout the app.

    Most notably, the secret key, the DB settings and some user-related settings are configured.
    """

    APP_NAME = "OKOSL Homeworks"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "my-pass-pimpek-penis-27"
    # URI format: dialect+driver://username:password@host:port/database
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning

    # PostgreSQL settings
    DB_USER = os.environ.get("DB_USER") or "okosl"
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT") or "5432"
    DB_NAME = os.environ.get("DB_NAME")
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(DB_USER,
                                                                   DB_PASSWORD,
                                                                   DB_HOST,
                                                                   DB_PORT,
                                                                   DB_NAME)

    # Flask-User settings - see https://flask-user.readthedocs.io/en/v0.6/customization.html
    # Should mail-related features be used, a SMTP server needs to be specified using e.g. Flask-Mail
    USER_APP_NAME = APP_NAME  # Shown in and email templates and page footers
    USER_ENABLE_USERNAME = True
    USER_ENABLE_EMAIL = False
    USER_ENABLE_REGISTRATION = False  # disable user registration through the website - an admin will add users by hand

    FLASK_ADMIN_SWATCH = 'superhero'  # colorscheme for bootstrap layout of Flask-Admin
