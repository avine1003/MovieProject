# -*- coding: utf-8 -*-
__author__ = "wuyou"
__date__ = "2018/5/18 15:39"

from app import db, app
from app.models import UserInfo

def create_database():
    db.create_all()

def query_dataset():
    return UserInfo.query.all()

def add_record(user):
    # create_database()
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    create_database()
