from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import  LoginManager


app = Flask(__name__)

app.config["SECRET_KEY"] = "63dc08a349bdb03a2e3ddfec1c2cae5cb70fcf574dc5ceef9813a633a3b86a37"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "info"
login_manager.login_message = "Please log in to access this page"

from featuria import routes
