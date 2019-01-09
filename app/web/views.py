# -*- coding:utf-8 _*-  
""" 
@author: ronething 
@file: views.py 
@time: 2019/01/09
@github: github.com/ronething 

Less is more.
"""

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from app.web.forms import TodoListForm, LoginForm, RegisterForm
from app.models import TodoList, User
from app import db, login_manager
from werkzeug.security import generate_password_hash
from . import web


@web.route('/', methods=['GET', 'POST'])
@login_required
def show_todo_list():
    form = TodoListForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            todolist = TodoList(current_user.id, form.title.data, form.status.data)
            db.session.add(todolist)
            db.session.commit()
            flash('You have add a new todo list', 'success')
            return redirect(url_for('web.show_todo_list'))
        else:
            flash(form.errors)
    todolists = TodoList.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', todolists=todolists, form=form)


@web.route('/delete/<int:id>/')
@login_required
def delete_todo_list(id):
    todolist = TodoList.query.filter_by(id=id).first_or_404()
    db.session.delete(todolist)
    db.session.commit()
    flash('You have delete a todo list', 'info')
    return redirect(url_for('web.show_todo_list'))


@web.route('/change/<int:id>/', methods=['GET', 'POST'])
@login_required
def change_todo_list(id):
    form = TodoListForm()
    todolist = TodoList.query.filter_by(id=id).first_or_404()
    if request.method == 'POST':
        if form.validate_on_submit():
            todolist = TodoList.query.filter_by(id=id).first_or_404()
            todolist.title = form.title.data
            todolist.status = form.status.data
            db.session.commit()
            flash('You have modify a todolist', 'info')
            return redirect(url_for('web.show_todo_list'))
        else:
            flash(form.errors)
    form.title.data = todolist.title
    form.status.data = str(todolist.status)
    return render_template('modify.html', form=form)


@web.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            password=generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        flash("register success and please login", "success")
        return redirect(url_for('web.login'))
    return render_template('register.html', form=form)


@web.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user.check_password(password):
            login_user(user)
            flash('you have logged in!', 'info')
            return redirect(url_for('web.show_todo_list'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)


@web.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('you have logout!', 'info')
    return redirect(url_for('web.login'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()
