from abc import abstractproperty
from ensurepip import bootstrap
from flask import Flask,render_template,session,redirect,url_for,flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField,SelectField
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
bootstrap=Bootstrap(app)
# 设置密钥，用于session和表单验证
app.config['SECRET_KEY']='your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:gjp136332@localhost/studentinfo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db=SQLAlchemy(app)
class Major(db.Model):
    __tablename__='majors'
    id=db.Column(db.Integer,primary_key=True)
    major_name=db.Column(db.String(100),unique=True,nullable=False)
    students=db.relationship('Basicinfo',backref='major',lazy='dynamic')
    def __repr__(self):
        return f'<Major {self.major_name}>'
class Basicinfo(db.Model):
    __tablename__='basicinfo'
    id=db.Column(db.String(255),primary_key=True)
    studentname=db.Column(db.String(255))
    studentbirthday=db.Column(db.String(255))
    ismale=db.Column(db.Boolean)
    major_id=db.Column(db.Integer,db.ForeignKey('majors.id'),nullable=True)
   
class NameForm(FlaskForm):
    id=StringField('请输入学号：')
    name=StringField('请输入姓名：')
    birthday=StringField('请输入出生日期：')
    ismale=BooleanField('请选择性别：')
    major=SelectField('请选择专业：',choices=[],coerce=int)
    submit=SubmitField('提交')
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.major.choices=[(major.id,major.major_name) for major in Major.query.order_by('major_name').all()]

@app.route('/',methods=['GET','POST'])
def index():
    studs=Basicinfo.query.all()
    majors=Major.query.all()
    return render_template('index.html',studs=studs,majors=majors) 
@app.route("/major/<int:major_id>")
def filter_by_major(major_id):
    major=Major.query.get_or_404(major_id)
    studs=major.students.all()
    majors=Major.query.all()
    return render_template('index.html',studs=studs,majors=majors)
@app.route('/new',methods=['GET','POST'])
def new_stud():
    form=NameForm()
    if form.validate_on_submit():
        id=form.id.data
        name=form.name.data
        birthday=form.birthday.data
        ismale=form.ismale.data
        major_id=form.major.data
        new_stud=Basicinfo(id=id,studentname=name,studentbirthday=birthday,ismale=ismale,major_id=major_id)
        db.session.add(new_stud)
        db.session.commit()
        flash('学生信息添加成功！')
        return redirect(url_for('index'))
    return render_template('new_stud.html',form=form)
@app.route('/edit/<string:id>',methods=['GET','POST'])
def edit_stud(id):
    stud=Basicinfo.query.get(id)
    form=NameForm()
    if form.validate_on_submit():
        stud.id=form.id.data
        stud.studentname=form.name.data
        stud.studentbirthday=form.birthday.data
        stud.ismale=form.ismale.data
        stud.major_id=form.major.data
        db.session.commit()
        flash('学生信息更新成功！')
        return redirect(url_for('index'))
    form.id.data=stud.id
    form.name.data=stud.studentname
    form.birthday.data=stud.studentbirthday
    form.ismale.data=stud.ismale
    form.major.data=stud.major_id
    return render_template('edit_stud.html',form=form)
@app.route('/<username>')
def test2(username):
    return render_template('111.html',username=username)
@app.route('/hello/<name>')
def hello_name(name):
    commments=['你好1','你好2','你好3']
    return render_template('user.html',name=name,commments=commments)
@app.route('/hello',methods=['GET','POST'])
def hello2():
    form=NameForm()
    if form.validate_on_submit():
        oldname=session.get('name')
        if oldname is not None and oldname!=form.name.data:
            flash('您的姓名已经更新成功！')
        session['name']=form.name.data
        return redirect(url_for('hello2'))
    return render_template('user.html',form=form,name=session.get('name')) 
@app.route('/testvariables')
def testvariables():
    mylist=[1,2,3,4,5,6]
    mydict={'name':'zhangsan','age':18}
    return render_template('testvariables.html',mylist=mylist,mydict=mydict)
if __name__ == "__main__":
    app.run(debug=True)
    