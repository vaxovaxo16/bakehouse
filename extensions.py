from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config["SECRET_KEY"] = "8X!(yU.)*ed}dzhyg]q_#(=e4$_,N)"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///CookiesShop.db"

db = SQLAlchemy(app)

login_manager = LoginManager(app)