# -*- coding: utf-8 -*-
from datetime import datetime

__author__ = "wuyou"
__date__ = "2018/5/18 10:34"

from app import db


class UserInfo(db.Model):
    __tablename__ = 'userinfo'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    address = db.Column(db.String(100))

    # add_time = db.Column(db.DateTime)

    def __init__(self, username, email, address):
        self.username = username
        self.email = email
        self.address = address

    def __str__(self):
        return self.username


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    add_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    movies = db.relationship('movie', backref='tag', lazy='dynamic')

    # 电影外键关联
    def __init__(self, name, add_time, movies):
        self.name = name
        self.add_time = add_time
        self.movies = movies

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
    play_num = db.Column(db.BigInteger)
    comment_num = db.Column(db.BigInteger)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))  # 外键
    area = db.Column(db.String(255))
    length = db.Column(db.String(100))
    add_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __init__(self, title, url, info, logo, star, play_num, comment_num, tag_id, area, length, add_time):
        self.title = title
        self.url = url
        self.info = info
        self.logo = logo
        self.star = star
        self.play_num = play_num
        self.comment_num = comment_num
        self.tag_id = tag_id
        self.area = area
        self.length = length
        self.add_time = add_time

    def __str__(self):
        return self.title


# def create_database():
#     db.create_all()


# if __name__ == '__main__':
    # create_database()
    # db.create_all()
    # user1 = UserInfo(username='xiaohai', email='1@163.com', address='beijing')
    # user2 = UserInfo(username='xiaohei', email='2@163.com', address='beijing')
    # user3 = UserInfo(username='xiaoming', email='3@163.com', address='wuhan')
    # users = [user1, user2, user3]
    # db.session.add_all(users)
    # db.session.commit()
