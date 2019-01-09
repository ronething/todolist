# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('app.setting')
bootstrap = Bootstrap(app)

app.secret_key = app.config["SECRET_KEY"]
app.config['SQLALCHEMY_DATABASE_URI'] = app.config["MYSQL_DB_URL"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "web.login"

from app.web import web

app.register_blueprint(web)
