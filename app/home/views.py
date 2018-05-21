# -*- coding: utf-8 -*-
__author__ = "wuyou"
__date__ = "2018/5/18 9:37"

from flask import Response, render_template

from . import home


@home.route('/')
def index():
    return render_template('home/index.html')


@home.route('/login')
def home_login():
   return render_template("home/login.html")


@home.route("/add_user/<string:username>/<string:email>/<string:address>")
def home_add_user(username, email, address):
    # 传入model层存储数据库
    from app import db
    from app.models import UserInfo
    user = UserInfo(username=username, email=email, address=address)
    import db_control
    db_control.add_record(user)
    # db.session.add(user)
    # db.session.commit()
    import json
    data = {'username': username, 'email': email, 'address': address}
    result = {'code': 200, 'msg': 'ok', 'data': data}
    return Response(json.dumps(result))


@home.route('/query/<string:username>')
def home_query_user(username):
    # 查找
    from app.models import UserInfo
    user = UserInfo.query.filter_by(username=username).first()
    # print(user)
    import json
    data = {'username': user.username, 'email': user.email, 'address': user.address}
    return Response(json.dumps(data))


@home.route('/del/<string:username>')
def home_del_user(username):
    from app.models import UserInfo
    from app import db
    user = UserInfo.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    return '删除成功'


@home.route('/change/<string:username>/<string:newname>')
def home_change_user(username, newname):
    from app.models import UserInfo
    from app import db
    users = UserInfo.query.all()
    print(users)
    li = []
    for user in users:
        li.append(user.username)
    if username not in li:
        return '不存在'
    user = UserInfo.query.filter_by(username=username).first()
    user.username = newname
    db.session.commit()
    return '修改成功'
