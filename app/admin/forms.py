# -*- coding: utf-8 -*-
from app.models import Admin, Tag, Movie

__author__ = "wuyou"
__date__ = "2018/5/18 9:38"

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError, EqualTo


class LoginForm(FlaskForm):
    """
    管理员登录表单
    """
    account = StringField(
        label="账号",
        validators=[
            DataRequired("账号不能为空")
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号！",
            "required": "required"
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("密码不能为空")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码！",
            "required": "required"
        }
    )
    submit = SubmitField(
        '登录',
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",
        }
    )

    def validate_account(self, field):
        account = field.data
        admin = Admin.query.filter_by(name=account).count()
        if admin == 0:
            raise ValidationError('帐号不存在!')


class AdminForm(FlaskForm):
    name = StringField(
        label='管理员名称',
        validators=[
            DataRequired('管理员名称不能为空!')
        ],
        description='管理员名称',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入管理员名称!',
        }
    )
    pwd = PasswordField(
        label='管理员密码',
        validators=[
            DataRequired('管理员密码不能为空!')
        ],
        description='管理员密码',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入管理员密码!',
        }
    )
    repwd = PasswordField(
        label='管理员重复密码',
        validators=[
            DataRequired('密码不能为空!'),
            EqualTo('pwd', message='两次密码不一致!')
        ],
        description='管理员重复密码',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入重复密码!',
        }
    )
    submit = SubmitField(
        "管理员注册",
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",
        }
    )

    def validate_name(self, field):
        name = field.data
        admin = Admin.query.filter_by(name=name).count()
        if admin == 1:
            raise ValidationError("管理员已经存在!")


class TagForm(FlaskForm):
    name = StringField(
        label='名称',
        validators=[
            DataRequired('标签名不能为空')
        ],
        description='标签',
        render_kw={
            'class': 'form-control',
            'id': 'input_name',
            'placeholder': '请输入标签名称!'
        }
    )
    submit = SubmitField(
        '提交',
        render_kw={
            'class': 'btn btn-primary',
        }
    )
    def validate_name(self, field):
        name = field.data
        tag = Tag.query.filter_by(name=name).count()
        if tag == 1:
            raise ValidationError("标签已经存在!")


class MovieForm(FlaskForm):
    '''电影表单'''
    title = StringField(
        label='片名',
        validators=[
            DataRequired('请输入片名!')
        ],
        render_kw={
            'class': 'form-control',
            'id': 'input_title',
            'placeholder': '请输入片名'
        }
    )
    url = FileField(
        label='文件',
        validators=[DataRequired('请上传文件')],
    )
    info = TextAreaField(
        label='简介',
        validators=[DataRequired('请输入简介')],
        render_kw={
            'class': 'form-control',
            'rows': 10,
        }
    )
    logo = FileField(
        label='封面',
        validators=[DataRequired('请输入封面')],
    )
    star = SelectField(
        label='星级',
        validators=[DataRequired('请选择星级')],
        coerce=int,
        choices=[(1, '1星'), (2, '2星'), (3, '3星'), (4, '4星'), (5, '5星')],
        render_kw={
            'class': 'form-control',
        }
    )
    tag_id = SelectField(
        label='标签',
        validators=[DataRequired('请选择标签')],
        coerce=int,
        choices=[(tag.id, tag.name) for tag in Tag.query.all()],
        render_kw={
            'class': 'form-control',
        }
    )
    area = StringField(
        label='地区',
        validators=[
            DataRequired('请输入地区')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入地区'
        }
    )
    length = StringField(
        label='片长',
        validators=[DataRequired('请输入片长')],
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入片长'
        }
    )
    release_time = StringField(
        label='上映时间',
        validators=[DataRequired('请输入上映时间!')],
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入上映时间',
            'id': 'input_release_time',
        }
    )
    submit = SubmitField(
        '提交',
        render_kw={
            'class': 'btn btn-primary'
        }
    )

    def validate_title(self, field):
        title = field.data
        movie = Movie.query.filter_by(title=title).count()
        if movie == 1:
            raise ValidationError("片名已经存在!")









