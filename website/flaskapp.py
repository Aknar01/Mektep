from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:////Users/aknar/PycharmProjects/Мектеп/website/database/db.db'

with app.app_context():
    db.init_app(app)

app.config['SECRET_KEY'] = 'my secret key'

