import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

UPLOAD_FOLDER = '../images'

app = Flask(__name__)   
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://italo:1234@localhost/handRecog'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
app.secret_key = '123456789'

from handRecog.views.recog import recog
app.register_blueprint(recog)