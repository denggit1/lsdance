# coding=utf-8
from flask import Flask, render_template
from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

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
    uname = StringField(label=u'学号', validators=[DataRequired(u'学号不能为空')])
    upwd = PasswordField(label=u'密码', validators=[DataRequired(u'密码不能为空')])
    upwd2 = PasswordField(label=u'密码2', validators=[DataRequired(u'密码不能为空'), EqualTo('upwd', u'两次密码输入不一致')])


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


@app.route('/login')
def login():
    form = RegistForm()
    return render_template('login.html', form=form)


@app.route('/register')
def register():
    form = RegistForm()
    return render_template('register.html', form=form)


if __name__ == '__main__':
    manage.run()
