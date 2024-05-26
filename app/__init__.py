from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from hashids import Hashids

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

login_manager = LoginManager(app)

bcrypt = Bcrypt(app)

hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])

# Import Views and Models
from app import views, models, utils

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(user_id)

