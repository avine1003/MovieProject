# -*- coding: utf-8 -*-
__author__ = "wuyou"
__date__ = "2018/5/18 9:35"

from flask import Flask, render_template
from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app = Flask(__name__)
app.register_blueprint(home_blueprint, url_prefix='/home')
app.register_blueprint(admin_blueprint, url_prefix='/admin')

@app.route('/')
def index():
    return render_template('home/index.html')


#################### SQLALCHEMY START ###########
from flask_sqlalchemy import SQLAlchemy
mysql_conn_str = "mysql+pymysql://root:123456@127.0.0.1:3306/movie?charset=utf8"

app.config["SQLALCHEMY_DATABASE_URI"] = mysql_conn_str
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

from app import models
######################SQLALCHEMY END ############
