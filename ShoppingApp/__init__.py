import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = 'SECRET_KEY'
db_path = os.path.join(os.path.dirname(__file__), 'myapp.db')
db_uri = 'sqlite:///{}'.format(db_path)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
login = LoginManager()
login.init_app(app)
login.login_view = 'login'


from ShoppingApp import routes , models


