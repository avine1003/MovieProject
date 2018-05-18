# -*- coding: utf-8 -*-
__author__ = "wuyou"
__date__ = "2018/5/18 9:38"

from flask import render_template

from . import admin

@admin.route('/')
def index():
    return "<h1 style='color:blue'>admin管理后台主页</h1>"