from app import create_app, db
from app.models import User, Basicinfo, Major

app = create_app()

# 新增：首次运行自动创建数据库表
with app.app_context():
    db.create_all()

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Basicinfo=Basicinfo, Major=Major)

if __name__ == '__main__':
    app.run(debug=True)