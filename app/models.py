# -*- coding: utf-8 -*-
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

# def create_database():
#     db.create_all()


if __name__ == '__main__':
    # create_database()
    db.create_all()
    user1 = UserInfo(username='xiaohai', email='1@163.com', address='beijing')
    user2 = UserInfo(username='xiaohei', email='2@163.com', address='beijing')
    user3 = UserInfo(username='xiaoming', email='3@163.com', address='wuhan')
    users = [user1, user2, user3]
    db.session.add_all(users)
    db.session.commit()