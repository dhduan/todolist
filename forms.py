#!/usr/bin/python
#-*- coding: UTF-8 -*-
from __future__ import unicode_literals
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, StringField, PasswordField,DateField
from wtforms.validators import DataRequired, Length

class TodoListForm(FlaskForm):
    wrk_date = DateField('日期', default='', validators=[DataRequired()], format='%Y/%m/%d')
    title = StringField('地点', validators=[DataRequired(), Length(1, 64)])
    content = StringField('内容', validators=[DataRequired(), Length(1, 64)])
    status = RadioField('工时', validators=[DataRequired()],  choices=[("1", '1工时'),("1.5",'1.5工时')])
    submit = SubmitField('提交')


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 24)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 24)])
    submit = SubmitField('登录')
