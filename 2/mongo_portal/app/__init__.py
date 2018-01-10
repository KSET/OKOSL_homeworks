from flask import Flask
from config import Config
from pymongo import MongoClient

app = Flask(__name__)
app.config.from_object(Config)
mongo = MongoClient("192.168.56.12", 27017).nmbp

from app import routes
