# -*- coding: utf-8 -*-
from datetime import datetime

import os

from werkzeug.utils import secure_filename

from app import db, app
from app.admin.forms import MovieForm
from app.models import Admin, Movie

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


# 修改文件名称, 用于文件上传
def change_filename(filename):
    import os, uuid
    from datetime import datetime
    fileinfo = os.path.splitext(filename)
    filename = datetime.now().strftime('%Y%m%d%H%M%S') + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


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


# 登录
@admin.route('/login/', methods=['GET', 'POST'])
def login():
    from app.admin.forms import LoginForm
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


# 退出
@admin.route('/logout/')
@admin_login_req
def logout():
    session.pop('admin', None)
    return redirect(url_for('admin.login'))


@admin.route('/add/', methods=['GET', 'POST'])
@admin_login_req
def admin_add():
    '''添加管理员'''
    from app.admin.forms import AdminForm
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


# 标签列表
@admin.route('/tag/list/<int:page>/', methods=['GET', 'POST'])
@admin_login_req
def tag_list(page):
    from app.models import Tag
    if page is None:
        page = 1
    page_data = Tag.query.order_by(Tag.add_time.asc()).paginate(page=page, per_page=3)
    return render_template('admin/tag_list.html', page_data=page_data)


# 标签删除
@admin.route('/tag/del/<int:id>/', methods=['GET', 'POST'])
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


# 电影添加
@admin.route('/movie/add/', methods=['GET', 'POST'])
@admin_login_req
def movie_add():
    from app.admin.forms import MovieForm
    from app.models import Movie
    from app import db, app
    from werkzeug.utils import secure_filename
    form = MovieForm()
    if form.validate_on_submit():
        data = form.data
        # 上传文件
        file_url = secure_filename(form.url.data.filename)
        file_logo = secure_filename(form.logo.data.filename)
        # 自动创建上传文件
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 777)

        url = change_filename(file_url)
        logo = change_filename(file_logo)
        form.url.data.save(app.config['UP_DIR'] + url)
        form.logo.data.save(app.config['UP_DIR'] + logo)
        movie = Movie(
            title=data['title'],
            url=url,
            info=data['info'],
            logo=logo,
            star=int(data['star']),
            play_num=0,
            comment_num=0,
            tag_id=int(data['tag_id']),
            area=data['area'],
            release_time=data['release_time'],
            length=data['length']
        )
        db.session.add(movie)
        db.session.commit()
        flash('添加电影成功', 'ok')
        return redirect(url_for('admin.movie_add'))
    return render_template('admin/movie_add.html', form=form)


# 电影列表
@admin.route('/movie/list/<int:page>', methods=['GET', 'POST'])
@admin_login_req
def movie_list(page=None):
    from app.models import Movie, Tag
    if page is None:
        page = 1
    pages = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id
    ).order_by(Movie.add_time.desc())
    page_data = pages.paginate(page=page, per_page=5)
    return render_template('admin/movie_list.html', page_data=page_data)


@admin.route('/movie/del/<int:id>', methods=['GET'])
@admin_login_req
def movie_del(id=None):
    '''电影删除'''
    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()
    flash('电影删除成功', 'ok')
    return redirect(url_for('admin.movie_list', page=1))


@admin.route('/movie/edit/<int:id>', methods=['GET', 'POST'])
@admin_login_req
def movie_edit(id=None):
    '''编辑电影页面'''
    form = MovieForm()
    form.url.validators = []
    form.logo.validators = []
    movie = Movie.query.get_or_404(id)
    if request.method == 'GET':
        form.info.data = movie.info
        form.tag_id.data = movie.tag_id
        form.star.data = movie.star

    if form.validate_on_submit():
        data = form.data
        # 创建目录
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 771)
        # 上传视频
        if form.url.data != '':
            file_url = secure_filename(form.url.data.filename)
            movie.url = change_filename(file_url)
            form.url.data.save(app.config['UP_DIR'] + movie.url)
        # 上传图片
        if form.logo.data != '':
            file_logo = secure_filename(form.logo.data.filename)
            movie.logo = change_filename(file_logo)
            form.logo.data.save(app.config['UP_DIR'] + movie.logo)

        movie.star = data['star']
        movie.tag_id = data['tag_id']
        movie.info = data['info']
        movie.title = data['title']
        movie.area = data["area"]
        movie.length = data["length"]
        movie.release_time = data["release_time"]
        db.session.add(movie)
        db.session.commit()
        flash("修改电影成功！", "ok")
        return redirect(url_for('admin.movie_edit', id=id))
    return render_template("admin/movie_edit.html", form=form, movie=movie)






