#!/usr/bin/python
#-*- coding: UTF-8 -*-
import time
import datetime
from ext import db
from flask_login import UserMixin


class TodoList(db.Model):
    __tablename__ = 'todolist'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    wrk_date = db.Column(db.DATE, nullable=False)
    title = db.Column(db.String(1024), nullable=False)
    content = db.Column(db.String(1024), nullable=False)
    status = db.Column(db.Float, nullable=False)
    create_user = db.Column(db.String(24), nullable=False)
    create_time = db.Column(db.DATETIME, nullable=False, default=datetime.datetime.now)
    upd_time = db.Column(db.DATETIME, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def __init__(self, user_id, wrk_date,title, content, status, create_user):
        self.user_id = user_id
        self.wrk_date = wrk_date
        self.title = title
        self.content = content
        self.status = status
        self.create_user = create_user
        self.upd_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        self.create_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False)
    password = db.Column(db.String(24), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password
