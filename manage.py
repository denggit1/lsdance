# coding=utf-8
from flask import Flask, render_template
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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/photo')
def photo():
    return render_template('photo.html')


@app.route('/introduce')
def introduce():
    return render_template('introduce.html')


@app.route('/dancetype')
def dancetype():
    return render_template('dancetype.html')


@app.route('/dancemv')
def dancemv():
    return render_template('dancemv.html')


@app.route('/dancemusic')
def dancemusic():
    return render_template('dancemusic.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = RegistForm()
    print('login')
    if form.validate_on_submit():
        print('hehe')
        stuid = form.stuid.data
        upwd = form.upwd.data
        s1 = sha()
        s1.update(upwd)
        pwd = s1.hexdigest()
        print(db.session.query(User).filter(User.stuid == stuid).count())
    return render_template('login.html', form=form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistForm()
    if form.validate_on_submit():
        stuid = form.stuid.data
        upwd = form.upwd.data
        s1 = sha()
        s1.update(upwd)
        pwd = s1.hexdigest()
        user1 = User(stuid=int(stuid), pwd=pwd)
        db.session.add(user1)
        db.session.commit()
    return render_template('register.html', form=form)


if __name__ == '__main__':
    manage.run()
