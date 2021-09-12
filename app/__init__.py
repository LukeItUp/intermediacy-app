from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from celery import Celery


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object('app.configuration.Config')
db = SQLAlchemy(app)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


from app import models
from app import views
from app import controllers