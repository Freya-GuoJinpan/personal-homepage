from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, PasswordField
# 新增 Email 验证器
from wtforms.validators import DataRequired, Length, EqualTo, Email

class NameForm(FlaskForm):
    id = StringField('请输入学号：')
    name = StringField('请输入姓名：')
    birthday = StringField('请输入出生日期：')
    ismale = BooleanField('请选择性别：')
    major = SelectField('请选择专业：', choices=[], coerce=int)
    submit = SubmitField('提交')
    
    def __init__(self, *args, **kwargs):
        super(NameForm, self).__init__(*args, **kwargs)
        from .models import Major
        self.major.choices = [(major.id, major.major_name) for major in Major.query.all()]

class LoginForm(FlaskForm):
    username = StringField('请输入用户名：', validators=[DataRequired(), Length(3, 20)])
    password = PasswordField('请输入密码：', validators=[DataRequired(), Length(6, 16)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class RegisterForm(FlaskForm):
    username = StringField('请输入用户名：', validators=[
        DataRequired(message='用户名不能为空'),
        Length(min=3, max=20, message='用户名长度必须在3-20个字符之间')
    ])
    # 新增邮箱字段
    email = StringField('请输入邮箱：', validators=[
        DataRequired(message='邮箱不能为空'),
        Email(message='请输入有效的邮箱地址')
    ])
    password = PasswordField('请输入密码：', validators=[
        DataRequired(message='密码不能为空'),
        Length(min=6, max=16, message='密码长度必须在6-16个字符之间')
    ])
    confirm_password = PasswordField('请确认密码：', validators=[
        DataRequired(message='确认密码不能为空'),
        EqualTo('password', message='两次输入密码不一致')
    ])
    submit = SubmitField('注册')