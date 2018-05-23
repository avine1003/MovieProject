# -*- coding: utf-8 -*-

__author__ = "wuyou"
__date__ = "2018/5/18 9:38"

from flask import render_template, redirect, url_for, flash, session, request
# 从模块的初始化文件中导入蓝图
from . import admin

# 路由定义使用装饰器进行定义
@admin.route('/')
def index():
    # return "<h1 style='color:blue'>admin管理后台主页</h1>"
    return render_template('admin/index.html')

@admin.route('/login/')
def login():
    from .forms import LoginForm
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        from app.models import Admin
        admin = Admin.query.filter_by(name=data['account']).first()
        # 密码错误时，check_pwd返回false,则此时not check_pwd(data["pwd"])为真。
        if not admin.check_pwd(data['pwd']):
            flash('密码错误!')
            return redirect(url_for('admin.login'))
        # 如果是正确的，就要定义session的会话进行保存。
        session['admin'] = data['account']
        return redirect(request.args.get('next') or url_for('admin.index'))
    return render_template('admin/login.html', form=form)


@admin.route('/logout/')
def logout():
    session.pop('admin', None)
    return redirect(url_for('admin.login'))


# 装饰器的访问控制
from functools import wraps

def admin_login_req(f):
    '''登录装饰器'''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('admin.login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function
