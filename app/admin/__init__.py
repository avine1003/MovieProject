# -*- coding: utf-8 -*-
__author__ = "wuyou"
__date__ = "2018/5/18 9:37"

from flask import Blueprint
'''定义蓝图'''
# 传入两个参数, 一个是蓝图名称, 一个是模块名
admin = Blueprint('admin', __name__)

import app.admin.views