# -*- coding: utf-8 -*-
import os

__author__ = "wuyou"
__date__ = "2018/5/18 9:35"

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    from flask import session
    login_flag = 0
    user_name = ''
    if session.get('user'):
        login_flag = 1
        user_name = session['user']
    return render_template('home/index.html', login_flag=login_flag, username=user_name)
    # return render_template('home/index.html')    # 工程主页面

#################### SQLALCHEMY START ###########
from flask_sqlalchemy import SQLAlchemy
mysql_conn_str = "mysql+pymysql://root:123456@127.0.0.1:3306/movie?charset=utf8"
# 用于连接数据的数据库
app.config["SQLALCHEMY_DATABASE_URI"] = mysql_conn_str
# 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SECRET_KEY'] = '12345678'
app.config['UP_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads/')
db = SQLAlchemy(app)

from app import models
######################SQLALCHEMY END ############


# 不要在生成db之前导入注册蓝图
# 从前台，后台模块中导入我们的蓝图对象
from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint
# 使用app对象，调用register_blueprint函数进行蓝图的注册
# 第一个参数是蓝图，第二个参数是url地址的前缀。通过地址前缀划分前后台的路由
app.register_blueprint(home_blueprint, url_prefix='/home')
app.register_blueprint(admin_blueprint, url_prefix='/admin')




