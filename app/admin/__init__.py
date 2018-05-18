# -*- coding: utf-8 -*-
__author__ = "wuyou"
__date__ = "2018/5/18 9:37"

from flask import Blueprint

admin = Blueprint('admin', __name__)

import app.admin.views