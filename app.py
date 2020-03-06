#!/usr/bin/python
#-*- coding: UTF-8 -*-
from __future__ import unicode_literals

from flask import (Flask, render_template, redirect, url_for, request, flash)
from flask_bootstrap import Bootstrap
from flask_login import login_required, login_user, logout_user, current_user

from forms import TodoListForm, LoginForm
from ext import db, login_manager
from models import TodoList, User

SECRET_KEY = 'This is my key'

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://dhduan:Union!234@localhost/test"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route('/', methods=['GET', 'POST'])
@login_required
def show_todo_list(page=None):
    if not page:
        page = 1
    form = TodoListForm()
    if request.method == 'GET' and current_user.id == 1:
        todolists = TodoList.query.all()
        return render_template('index.html', todolists=todolists,form=form)
    elif current_user.id != 1:
        tdl = TodoList.query.filter_by(user_id=current_user.id).order_by(TodoList.create_time.desc()).paginate(page=page, per_page=5)
        return render_template('index.html', todolists=tdl.items,  pagination=tdl,form=form)
    else:
        if form.validate_on_submit():
            todolist = TodoList(current_user.id, form.title.data, form.content.data, form.status.data, current_user.username)
            db.session.add(todolist)
            db.session.commit()
            flash('新内容添加成功！')
        else:
            flash(form.errors)
        return redirect(url_for('show_todo_list'))

@app.route('/dolist<int:page>',methods=['GET'])
@login_required
def show_page(page=None):
    # 每个人只能看自己发表的
    if not page:
        page = 1
    form = TodoListForm()
    # paginate方法返回一个sqlalchemy.Pagination类型对象
    blogs = TodoList.query.filter_by(user_id=current_user.id).order_by(TodoList.create_time.desc()).paginate(page=page, per_page=5)
    return render_template('index.html', todolists=blogs.items, form=form, pagination=blogs)

@app.route('/add',methods=['POST'])
@login_required
def add_todo_list():
    form = TodoListForm()
    if request.method =='POST':
        if form.validate_on_submit():
            todolist = TodoList(current_user.id, form.title.data, form.content.data, form.status.data,current_user.username)
            db.session.add(todolist)
            db.session.commit()
            flash(current_user.username+'添加了一条新的工作内容')
        else:flash(form.errors)
    return redirect(url_for('show_todo_list'))


@app.route('/delete/<int:id>')
@login_required
def delete_todo_list(id):
     todolist = TodoList.query.filter_by(id=id).first_or_404()
     db.session.delete(todolist)
     db.session.commit()
     flash('You have delete a todo list')
     return redirect(url_for('show_todo_list'))


@app.route('/change/<int:id>', methods=['GET', 'POST'])
@login_required
def change_todo_list(id):
    if request.method == 'GET':
        todolist = TodoList.query.filter_by(id=id).first_or_404()
        form = TodoListForm()
        form.title.data = todolist.title
        form.status.data = str(todolist.status)
        todolist.content = form.content.data
        return render_template('modify.html', form=form)
    else:
        form = TodoListForm()
        if form.validate_on_submit():
            todolist = TodoList.query.filter_by(id=id).first_or_404()
            todolist.title = form.title.data
            todolist.status = form.status.data
            todolist.content = form.content.data
            db.session.commit()
            flash(current_user.username+'修改了第'+str(id)+'条记录')
        else:
            flash(form.errors)
        return redirect(url_for('show_todo_list'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        if user:
            login_user(user)
            flash('you have logged in!')
            return redirect(url_for('show_todo_list'))
        else:
            flash('Invalid username or password')
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you have logout!')
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
