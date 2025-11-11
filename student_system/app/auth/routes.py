from flask import render_template, redirect, url_for, flash, request
from . import auth
from .. import db
from ..models import User
from ..forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required, current_user

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('登录成功')
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('用户名或密码错误')
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已退出登录')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('用户名已存在')
            return redirect(url_for('auth.register'))
        # 新增：传入 email 字段
        role = 'admin' if request.form.get('admin_code') == 'admin123' else 'guest'
        new_user = User(
            username=form.username.data,
            email=form.email.data,  # 新增邮箱赋值
            role=role
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash(f'注册成功!您的角色为{role}')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)