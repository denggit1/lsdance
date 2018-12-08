# coding=utf-8
from flask import Flask, render_template, request, jsonify, session, redirect
from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from sha import sha

app = Flask(__name__)
manage = Manager(app)
# en64=base64.b64encode(uuid.uuid4().bytes)
app.config['SECRET_KEY'] = 'XL57Byw6Tj2q3U7gtDWDIw=='
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/lsdance'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
Migrate(app, db)
manage.add_command("db", MigrateCommand)


class RegistForm(FlaskForm):
    stuid = IntegerField(label=u'学号', validators=[DataRequired(u'学号不能为空')])
    upwd = PasswordField(label=u'密码', validators=[DataRequired(u'密码不能为空')])
    upwd2 = PasswordField(label=u'密码2', validators=[DataRequired(u'密码不能为空'), EqualTo('upwd', u'两次密码输入不一致')])


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    stuid = db.Column(db.Integer, unique=True, nullable=False)
    pwd = db.Column(db.String(40), unique=False, nullable=False)
    name = db.Column(db.String(32), unique=False, nullable=True)
    phone = db.Column(db.Integer, unique=False, nullable=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), default=1)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), default=1)


class Class(db.Model):
    __tablename__ = 'class'
    id = db.Column(db.Integer, primary_key=True)
    Class = db.Column(db.String(32), unique=True, nullable=True)
    college = db.Column(db.String(32), unique=False, nullable=True)
    users = db.relationship("User", backref="class")


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(32), unique=False, nullable=False)
    users = db.relationship("User", backref="role")


def Info():
    stuid = session.get('stuid')
    if stuid is not None:
        info1 = db.session.query(User).filter(User.stuid == stuid).first().name
        info2 = '<a href="/userinfo">用户中心</a>'.decode('utf-8')
        info3 = '<a href="/sessionpop">退出</a>'.decode('utf-8')
    else:
        info1 = ''
        info2 = '<a href="/login">登录</a>'.decode('utf-8')
        info3 = '<a href="/register">注册</a>'.decode('utf-8')
    info = {'info1': info1, 'info2': info2, 'info3': info3}
    return info


@app.route('/')
def index():
    info = Info()
    return render_template('index.html', info=info)


@app.route('/photo')
def photo():
    info = Info()
    return render_template('photo.html', info=info)


@app.route('/introduce')
def introduce():
    info = Info()
    return render_template('introduce.html', info=info)


@app.route('/dancetype')
def dancetype():
    info = Info()
    return render_template('dancetype.html', info=info)


@app.route('/dancemv')
def dancemv():
    info = Info()
    return render_template('dancemv.html', info=info)


@app.route('/dancemusic')
def dancemusic():
    info = Info()
    return render_template('dancemusic.html', info=info)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = RegistForm()
    if request.method == 'POST':
        stuid = form.stuid.data
        upwd = form.upwd.data
        s1 = sha()
        s1.update(upwd)
        pwd = s1.hexdigest()
        if db.session.query(User).filter(User.stuid == stuid).count() <= 0:
            x = 'sid0'
        elif db.session.query(User).filter(User.stuid == stuid).filter(User.pwd == pwd).count() <= 0:
            x = 'pwd0'
        else:
            x = 'ok'
            # 保存stuid
            session['stuid'] = db.session.query(User).filter(User.stuid == stuid).filter(User.pwd == pwd).first().stuid
        data = {'status': x}
        return jsonify(data)
    return render_template('login.html', form=form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistForm()
    if request.method == 'POST':
        stuid = form.stuid.data
        upwd = form.upwd.data
        namestr = str(stuid)
        if namestr[2:3] == '2':
            name = namestr[:2] + '届单招生'
        elif namestr[2:3] == '3':
            name = namestr[:2] + '届统招生'
        else:
            name = '成员'
        s1 = sha()
        s1.update(upwd)
        pwd = s1.hexdigest()
        if db.session.query(User).filter(User.stuid == stuid).count() > 0:
            x = 'sid1'
        else:
            x = 'sid0'
            user1 = User(stuid=int(stuid), pwd=pwd, name=name)
            db.session.add(user1)
            db.session.commit()
            # 保存stuid
            session['stuid'] = db.session.query(User).filter(User.stuid == stuid).filter(User.pwd == pwd).first().stuid
        data = {'status': x}
        return jsonify(data)
    return render_template('register.html', form=form)


@app.route('/sessionpop')
def sessionpop():
    session.pop('stuid')
    return redirect('/')


@app.route('/userinfo')
def userinfo():
    return 'userinfo'


if __name__ == '__main__':
    manage.run()
