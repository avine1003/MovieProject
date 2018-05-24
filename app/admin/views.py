# -*- coding: utf-8 -*-
from datetime import datetime

from app.models import Admin

__author__ = "wuyou"
__date__ = "2018/5/18 9:38"

from flask import render_template, redirect, url_for, flash, session, request
# 从模块的初始化文件中导入蓝图
from . import admin

# 装饰器的访问控制
from functools import wraps

def admin_login_req(f):
    '''登录装饰器'''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)

    return decorated_function


@admin.context_processor
def tpl_extra():
    '''上下文应用处理器'''
    try:
        admin = Admin.query.filter_by(name=session['admin']).first()
    except:
        admin = None
    data = dict(online_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),

                )
    return data


# 路由定义使用装饰器进行定义
@admin.route('/')
@admin_login_req
def index():
    # return "<h1 style='color:blue'>admin管理后台主页</h1>"
    if 'admin' not in session:
        return redirect(url_for('admin.login'))
    return render_template('admin/index.html')


@admin.route('/login/', methods=['GET', 'POST'])
def login():
    from .forms import LoginForm
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        from app.models import Admin
        admin = Admin.query.filter_by(name=data['account']).first()
        # 密码错误时，check_pwd返回false,则此时not check_pwd(data["pwd"])为真。
        if not admin.check_pwd(data['pwd']):
            flash('密码错误!', 'err')
            return redirect(url_for('admin.login'))
        # 如果是正确的，就要定义session的会话进行保存。
        session['admin'] = data['account']
        return render_template('admin/index.html')
    return render_template('admin/login.html', form=form)


@admin.route('/logout/')
@admin_login_req
def logout():
    session.pop('admin', None)
    return redirect(url_for('admin.login'))


@admin.route('/add/', methods=['GET', 'POST'])
@admin_login_req
def admin_add():
    '''添加管理员'''
    from .forms import AdminForm
    from app.models import Admin, db
    form = AdminForm()
    from werkzeug.security import generate_password_hash
    if form.validate_on_submit():
        data = form.data
        admin = Admin(
            name=data['name'],
            pwd=generate_password_hash(data['pwd']),
            is_super=1
        )
        db.session.add(admin)
        db.session.commit()
        flash('管理员注册成功!', 'ok')
    return render_template('admin/admin_add.html', title='管理员注册', form=form)


@admin.route('/tag/add/', methods=['GET', 'POST'])
@admin_login_req
def tag_add():
    from app.admin.forms import TagForm
    from app.models import Tag
    from app import db
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag = Tag(name=data['name'])
        db.session.add(tag)
        db.session.commit()
        flash('添加标签成功!', 'ok')
        return redirect(url_for('admin.tag_add'))
    return render_template('admin/tag_add.html', form=form)


@admin.route('/tag/list/<int:page>/', methods=['GET'])
@admin_login_req
def tag_list(page):
    from app.models import Tag
    if page is None:
        page = 1
    page_data = Tag.query.order_by(Tag.add_time.asc()).paginate(page=page, per_page=3)

    return render_template('admin/tag_list.html', page_data=page_data)


# 标签删除
@admin.route('/tag/del/<int:id>/', methods=['GET'])
@admin_login_req
def tag_del(id=None):
    from app.models import Tag
    from app import db
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash('删除标签成功', 'ok')
    return redirect(url_for('admin.tag_list', page=1))


# 标签修改
@admin.route('/tag/edit/<int:id>', methods=['GET', 'POST'])
@admin_login_req
def tag_edit(id=None):
    from app.admin.forms import TagForm
    from app.models import Tag
    from app import db
    form = TagForm()
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        # tag_count = Tag.query.filter_by(name=data['name']).count()
        # if tag.name != data['name'] and tag_count == 1:
        #     flash('标签已经存在!', 'err')
        #     return redirect(url_for('admin.tag_edit', id=id))
        tag.name = data['name']
        db.session.add(tag)
        db.session.commit()
        flash('修改标签成功', 'ok')
        return redirect(url_for('admin.tag_edit', id=id))
    return render_template('admin/tag_edit.html', title='修改标签', form=form, tag=tag)


