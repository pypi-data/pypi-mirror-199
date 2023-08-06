from flask import Flask
from flask_login import LoginManager
from foalorm.flask import FoalORM
from .config import config
from .models import db

app = Flask(__name__)
app.config.update(config)

FoalORM(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.User.get(id=user_id)
