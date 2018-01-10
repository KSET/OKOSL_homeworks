from flask import Flask
from config import Config
from pymongo import MongoClient
from flask_uploads import configure_uploads, UploadSet, IMAGES

app = Flask(__name__)
app.config.from_object(Config)
configure_uploads(app, UploadSet('images', IMAGES))
mongo = MongoClient("192.168.56.12", 27017).nmbp

from app import routes
