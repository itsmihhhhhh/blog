from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
# from flask_migrate import Migrate
from flask_admin import Admin

app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)


admin = Admin(app,template_mode='bootstrap3')
# migrate = Migrate(app,db,render_as_batch=True)
from app import views, models

from .models import User

login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()
