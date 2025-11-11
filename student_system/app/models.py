from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='guest', nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def is_admin(self):
        return self.role == 'admin'
    
    def __repr__(self):
        return f'<User {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Major(db.Model):
    __tablename__ = 'majors'
    id = db.Column(db.Integer, primary_key=True)
    major_name = db.Column(db.String(100), unique=True, nullable=False)
    department = db.Column(db.String(100), nullable=False)  # 所属院系
    description = db.Column(db.Text)  # 专业描述
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    students = db.relationship('Basicinfo', backref='major', lazy='dynamic', 
                              cascade="all, delete-orphan")  # 级联删除
    
    def __repr__(self):
        return f'<Major {self.major_name}>'


class Basicinfo(db.Model):
    __tablename__ = 'basicinfo'
    id = db.Column(db.String(20), primary_key=True)  # 学号
    studentname = db.Column(db.String(64), nullable=False)
    studentbirthday = db.Column(db.String(20), nullable=False)
    ismale = db.Column(db.Boolean, nullable=False)
    major_id = db.Column(db.Integer, db.ForeignKey('majors.id'), nullable=False)
    admission_year = db.Column(db.String(4))  # 入学年份
    address = db.Column(db.Text)  # 家庭地址
    phone = db.Column(db.String(20))  # 联系电话
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, 
                          onupdate=datetime.utcnow)
    
    # 添加与成绩等其他表的关联基础（如果需要）
    # scores = db.relationship('Score', backref='student', lazy='dynamic')
    
    def __repr__(self):
        return f'<Student {self.id}: {self.studentname}>'
    
    def get_gender(self):
        """返回性别中文描述"""
        return '男' if self.ismale else '女'