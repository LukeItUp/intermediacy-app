from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from celery import Celery


app = Flask(__name__)
app.config.from_object('app.configuration.Config')
db = SQLAlchemy(app)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


from app import models
from app import views
from app import controllers