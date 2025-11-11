from flask import render_template, redirect, url_for, flash, session
from . import main
from .. import db
from ..models import Basicinfo, Major
from ..forms import NameForm
from flask_login import login_required, current_user
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('您没有权限访问该页面')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    studs = Basicinfo.query.all()
    majors = Major.query.all()
    return render_template('index.html', studs=studs, majors=majors, current_user=current_user)

# 修复：路由参数语法错误 <<int:major_id>> → <int:major_id>
@main.route("/major/<int:major_id>")
@login_required
def filter_by_major(major_id):
    major = Major.query.get_or_404(major_id)
    studs = major.students.all()
    majors = Major.query.all()
    return render_template('index.html', studs=studs, majors=majors, current_user=current_user)

@main.route('/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_stud():
    form = NameForm()
    if form.validate_on_submit():
        new_stud = Basicinfo(
            id=form.id.data,
            studentname=form.name.data,
            studentbirthday=form.birthday.data,
            ismale=form.ismale.data,
            major_id=form.major.data
        )
        db.session.add(new_stud)
        db.session.commit()
        flash('学生信息添加成功！')
        return redirect(url_for('main.index'))
    return render_template('new_stud.html', form=form, current_user=current_user)

@main.route('/edit/<string:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_stud(id):
    stud = Basicinfo.query.get_or_404(id)
    form = NameForm()
    if form.validate_on_submit():
        stud.id = form.id.data
        stud.studentname = form.name.data
        stud.studentbirthday = form.birthday.data
        stud.ismale = form.ismale.data
        stud.major_id = form.major.data
        db.session.commit()
        flash('学生信息更新成功！')
        return redirect(url_for('main.index'))
    form.id.data = stud.id
    form.name.data = stud.studentname
    form.birthday.data = stud.studentbirthday
    form.ismale.data = stud.ismale
    form.major.data = stud.major_id
    return render_template('edit_stud.html', form=form, current_user=current_user)

@main.route('/delete/<string:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_stud(id):
    stud = Basicinfo.query.get_or_404(id)
    db.session.delete(stud)
    db.session.commit()
    flash('学生信息删除成功！')
    return redirect(url_for('main.index'))

@main.route('/<username>')
@login_required
def test2(username):
    return render_template('111.html', username=username, current_user=current_user)

@main.route('/hello/<name>')
@login_required
def hello_name(name):
    commments = ['你好1', '你好2', '你好3']
    return render_template('user.html', name=name, commments=commments, current_user=current_user)

@main.route('/hello', methods=['GET', 'POST'])
@login_required
def hello2():
    form = NameForm()
    if form.validate_on_submit():
        oldname = session.get('name')
        if oldname and oldname != form.name.data:
            flash('您的姓名已经更新成功！')
        session['name'] = form.name.data
        return redirect(url_for('main.hello2'))
    return render_template('user.html', form=form, name=session.get('name'), current_user=current_user)

@main.route('/testvariables')
@login_required
def testvariables():
    mylist = [1,2,3,4,5,6]
    mydict = {'name':'zhangsan','age':18}
    return render_template('testvariables.html', mylist=mylist, mydict=mydict, current_user=current_user)