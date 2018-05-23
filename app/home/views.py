# -*- coding: utf-8 -*-
__author__ = "wuyou"
__date__ = "2018/5/18 9:37"

from flask import Response, render_template, redirect, url_for, flash, session, request
from werkzeug.security import generate_password_hash
from . import home

from functools import wraps

# 登录装饰器
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('home.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@home.route('/test')
@user_login_req
def mtest():
    return Response('This is my mtest')


@home.route('/')
def index():
    login_flag = 0
    user_name = ''
    if session.get('user'):
        login_flag = 1
        user_name = session['user']
    return render_template('home/index.html', login_flag=login_flag, username=user_name)


@home.route('/login', methods=['GET', 'POST'])
def login():
    from app.home.forms import LoginForm
    from app.models import User
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data['name']).first()
        user1 = User.query.filter_by(email=data['name']).first()
        user2 = User.query.filter_by(phone=data['name']).first()
        user = user or user1 or user2
        if user:
            if not user.check_pwd(data['pwd']):
                flash('密码错误!', 'err')
                return redirect(url_for('home.login'))
        else:
            flash('帐号不存在!', 'err')
            return redirect(url_for('home.login'))
        session['user'] = user.name
        session['user_id'] = user.id
        # flash('登录成功!', 'ok')
        return render_template('home/index.html', login_flag=1, username=user.name)
    return render_template('home/login.html', title='用户登录', form=form)


@home.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    return redirect(url_for('home.login'))


@home.route('/register/', methods=['GET', 'POST'])
def register():
    from app.home.forms import RegisterForm
    from app.models import User
    from app import db
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            pwd=generate_password_hash(data['pwd']),
        )
        db.session.add(user)
        db.session.commit()
        flash('注册成功!', 'ok')
    return render_template('home/register.html', form=form)


# @home.route('/wtflogin', methods=['GET', 'POST'])
# def wtflogin():
#     from app.home.forms import LoginForm
#     from app.models import User
#     form = LoginForm()
#     if form.validate_on_submit():
#         data = form.data
#         user = User.query.filter_by(name=data['name']).first()
#         user1 = User.query.filter_by(email=data['name']).first()
#         user2 = User.query.filter_by(phone=data['name']).first()
#         user = user or user1 or user2
#         if user:
#             if not user.check_pwd(data['pwd']):
#                 flash('密码错误!', 'err')
#                 return redirect(url_for('home.wtflogin'))
#         else:
#             flash('帐号不存在!', 'err')
#             return redirect(url_for('home.wtflogin'))
#         session['user'] = user.name
#         session['user_id'] = user.id
#         flash('登录成功!', 'ok')
#     return render_template('home/wtflogin.html', title='wtf表单登录', form=form)


@home.route('/animation/')
def animation():
    return render_template('home/animation.html')


@home.route('/play/')
def play():
    return render_template('home/play.html')


@home.route('/user/')
def user():
    '''用户中心'''
    return render_template('home/user.html')


@home.route('/pwd/')
def pwd():
    '''修改密码'''
    return render_template('home/pwd.html')


@home.route('/comments/')
def comments():
    '''评论记录'''
    return render_template('home/comments.html')


@home.route('/loginlog/')
def loginlog():
    '''登录日志'''
    return render_template('home/loginlog.html')


@home.route('/moviecol/')
def moviecol():
    '''收藏电影'''
    return render_template('home/moviecol.html')

# @home.route("/add_user/<string:username>/<string:email>/<string:address>")
# def home_add_user(username, email, address):
#     # 传入model层存储数据库
#     from app import db
#     from app.models import UserInfo
#     user = UserInfo(username=username, email=email, address=address)
#     import db_control
#     db_control.add_record(user)
#     # db.session.add(user)
#     # db.session.commit()
#     import json
#     data = {'username': username, 'email': email, 'address': address}
#     result = {'code': 200, 'msg': 'ok', 'data': data}
#     return Response(json.dumps(result))
#
#
# @home.route('/query/<string:username>')
# def home_query_user(username):
#     # 查找
#     from app.models import UserInfo
#     user = UserInfo.query.filter_by(username=username).first()
#     # print(user)
#     import json
#     data = {'username': user.username, 'email': user.email, 'address': user.address}
#     return Response(json.dumps(data))
#
#
# @home.route('/del/<string:username>')
# def home_del_user(username):
#     from app.models import UserInfo
#     from app import db
#     user = UserInfo.query.filter_by(username=username).first()
#     db.session.delete(user)
#     db.session.commit()
#     return '删除成功'
#
#
# @home.route('/change/<string:username>/<string:newname>')
# def home_change_user(username, newname):
#     from app.models import UserInfo
#     from app import db
#     users = UserInfo.query.all()
#     print(users)
#     li = []
#     for user in users:
#         li.append(user.username)
#     if username not in li:
#         return '不存在'
#     user = UserInfo.query.filter_by(username=username).first()
#     user.username = newname
#     db.session.commit()
#     return '修改成功'