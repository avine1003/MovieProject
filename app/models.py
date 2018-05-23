# -*- coding: utf-8 -*-
from datetime import datetime

__author__ = "wuyou"
__date__ = "2018/5/18 10:34"

from app import db

# class UserInfo(db.Model):
#     # 测试
#     __tablename__ = 'userinfo'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True)
#     email = db.Column(db.String(50), unique=True)
#     address = db.Column(db.String(100))
#
#     # add_time = db.Column(db.DateTime)
#
#     def __init__(self, username, email, address):
#         self.username = username
#         self.email = email
#         self.address = address
#
#     def __str__(self):
#         return self.username

# 会员数据模型
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(200))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(11), unique=True)
    info = db.Column(db.Text)
    face = db.Column(db.String(255), unique=True)
    add_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 注册时间
    uuid = db.Column(db.String(255), unique=True)   # 唯一标识
    # user_logs = db.relationship('userlog', backref='user')   # 会员日志外键关系关联

    def __str__(self):
        return self.name

    # 验证密码，采用hash256加密算法保存密码
    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)

'''
# 会员登录日志
class UserLog(db.Model):
    __tablename__ = 'userlog'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ip = db.Column(db.String(100))
    add_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    def __str__(self):
        return self.id


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    add_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    movies = db.relationship('movie', backref='tag')
    # 电影外键关联

    def __str__(self):
        return self.name


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255), unique=True)
    info = db.Column(db.Text)
    logo = db.Column(db.String(255), unique=True)
    star = db.Column(db.Integer)
    play_num = db.Column(db.BigInteger)  # 播放量
    comment_num = db.Column(db.BigInteger)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))  # 所属标签
    area = db.Column(db.String(255))  # 上映地区
    release_time = db.Column(db.Date)  # 上映时间
    length = db.Column(db.String(100))  # 播放时间
    add_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    comments = db.relationship('comment', backref='movie')
    movie_cols = db.relationship('moviecol', backref='movie')  # 收藏

    def __str__(self):
        return self.title

# 上映预告
class Preview(db.Model):
    __tablename__ = 'preview'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    logo = db.Column(db.String(255), unique=True)
    add_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __str__(self):
        return self.title


class Comment(db.Model):
    __tablename__  = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    add_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __str__(self):
        return self.id


# 电影收藏
class MovieCol(db.Model):
    __tablename__ = 'moviecol'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    add_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __str__(self):
        return self.id


# 权限
class Auth(db.Model):
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    url = db.Column(db.String(255), unique=True)
    add_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __str__(self):
        return self.name

# 角色
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    auths = db.Column(db.String(600))  # 角色权限列表
    add_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    admins = db.relationship('admin', backref='role')

    def __str__(self):
        return self.name

# 管理员
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    is_super = db.Column(db.SmallInteger)  # 是否为超级管理员, 0为超级管理员
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    add_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    admin_logs = db.relationship('adminlog', backref='admin')  # 管理员登录日志外键关联
    op_logs = db.relationship('oplog', backref='admin')   # 管理员操作日志外键关联

    def __str__(self):
        return self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 管理员登录日志
class AdminLog(db.Model):
    __tablename__ = 'adminlog'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    ip = db.Column(db.String(100))
    add_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __str__(self):
        return self.id


# 操作日志
class OpLog(db.Model):
    __tablename__ = 'oplog'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    ip = db.Column(db.String(100))
    reason = db.Column(db.String(600))
    add_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __str__(self):
        return self.id


# if __name__ == '__main__':
    # db.create_all()
    # user1 = UserInfo(username='xiaohai', email='1@163.com', address='beijing')
    # user2 = UserInfo(username='xiaohei', email='2@163.com', address='beijing')
    # user3 = UserInfo(username='xiaoming', email='3@163.com', address='wuhan')
    # users = [user1, user2, user3]
    # db.session.add_all(users)
    # db.session.commit()
'''