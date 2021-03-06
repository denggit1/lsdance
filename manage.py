# coding=utf-8
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf.csrf import CsrfProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from sha import sha
import re
import redis

app = Flask(__name__)
manage = Manager(app)
# en64=base64.b64encode(uuid.uuid4().bytes)
app.config['SECRET_KEY'] = 'XL57Byw6Tj2q3U7gtDWDIw=='
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/lsdance'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
CsrfProtect(app)
db = SQLAlchemy(app)
Migrate(app, db)
manage.add_command("db", MigrateCommand)


class RegistForm(FlaskForm):
    stuid = IntegerField(label=u'学号', validators=[DataRequired(u'学号不能为空')])
    upwd = PasswordField(label=u'密码', validators=[DataRequired(u'密码不能为空')])
    upwd2 = PasswordField(label=u'密码2', validators=[DataRequired(u'密码不能为空'), EqualTo('upwd', u'两次密码输入不一致')])


class RedisHelper():
    def __init__(self, host='localhost', port=6379):
        self.__redis = redis.StrictRedis(host=host, port=port)

    def set(self, key, value):
        self.__redis.set(key, value)

    def get(self, key):
        return self.__redis.get(key)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    stuid = db.Column(db.Integer, unique=True, nullable=False)
    pwd = db.Column(db.String(40), unique=False, nullable=False)
    name = db.Column(db.String(32), unique=False, nullable=True)
    phone = db.Column(db.String(32), unique=False, nullable=True)
    college = db.Column(db.String(32), unique=False, nullable=True)
    userclass = db.Column(db.String(32), unique=False, nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), default=1)

    def __repr__(self):
        return '<学号 %d>' % self.stuid


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(32), unique=False, nullable=False)
    users = db.relationship("User", backref="role")

    def __repr__(self):
        return self.role


class Mv(db.Model):
    __tablename__ = 'mv'
    id = db.Column(db.Integer, primary_key=True)
    mvname = db.Column(db.String(32), unique=True, nullable=False)
    mvurl = db.Column(db.String(128), unique=True, nullable=False)


class Music(db.Model):
    __tablename__ = 'music'
    id = db.Column(db.Integer, primary_key=True)
    musicname = db.Column(db.String(32), unique=True, nullable=False)
    musicurl = db.Column(db.String(128), unique=True, nullable=False)


def Info():
    stuid = session.get('stuid')
    if stuid is not None:
        info1 = db.session.query(User).filter(User.stuid == stuid).first().name
        info2 = '<a href="/userinfo">用户中心</a>'.decode('utf-8')
        info3 = '<a href="/sessionpop">退出</a>'.decode('utf-8')
    else:
        info1 = '欢迎'.decode('utf-8')
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
    mv = db.session.query(Mv).all()
    return render_template('dancemv.html', info=info, mv=mv)


@app.route('/dancemusic')
def dancemusic():
    info = Info()
    music = db.session.query(Music).all()
    return render_template('dancemusic.html', info=info, music=music)


@app.route('/stuid')
def stuid():
    stuid = session.get('stuid', '')
    data = {'stuid': stuid}
    return jsonify(data)


@app.route('/qun')
def qun():
    return render_template('qun.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = RegistForm()
    if request.method == 'POST':
        r = RedisHelper('127.0.0.1', 6379)
        stuid = form.stuid.data
        upwd = form.upwd.data
        s1 = sha()
        s1.update(upwd)
        pwd = s1.hexdigest()
        if r.get(stuid) == pwd:
            x = 'ok'
            # 保存stuid
            session['stuid'] = db.session.query(User).filter(User.stuid == stuid).filter(User.pwd == pwd).first().stuid
        elif db.session.query(User).filter(User.stuid == stuid).count() <= 0:
            x = 'sid0'
        elif db.session.query(User).filter(User.stuid == stuid).filter(User.pwd == pwd).count() <= 0:
            x = 'pwd0'
        else:
            x = 'ok'
            # 保存redis
            r.set(stuid, pwd)
            # 保存stuid
            session['stuid'] = db.session.query(User).filter(User.stuid == stuid).filter(User.pwd == pwd).first().stuid
        data = {'status': x}
        return jsonify(data)
    return render_template('login.html', form=form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistForm()
    if request.method == 'POST':
        if db.session.query(Role).all() == []:
            role1 = Role(id=1, role='people')
            db.session.add(role1)
            db.session.commit()
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
        if re.match('^\d{2}[2-3][0]\d{5}$', str(stuid)) is None:
            x = 'sidzz'
        elif len(upwd) < 6 or len(upwd) > 16:
            x = 'pwderr'
        elif db.session.query(User).filter(User.stuid == stuid).count() > 0:
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
    stuid = session.get('stuid')
    if stuid is None:
        return redirect('/login')
    else:
        id = db.session.query(User).filter(User.stuid == stuid).first().id
        name = db.session.query(User).filter(User.stuid == stuid).first().name
        phone = db.session.query(User).filter(User.stuid == stuid).first().phone
        college = db.session.query(User).filter(User.stuid == stuid).first().college
        userclass = db.session.query(User).filter(User.stuid == stuid).first().userclass
        role = db.session.query(Role).filter(
            Role.id == db.session.query(User).filter(User.stuid == stuid).first().role_id).first().role
    data = {'id': id, 'stuid': stuid, 'name': name, 'phone': phone,
            'college': college, 'userclass': userclass, 'role': role}
    if db.session.query(Role).filter(
            Role.id == db.session.query(User).filter(User.stuid == stuid).first().role_id).first().role == 'super':
        title = u'<a href="/super">Super管理界面</a>'
    elif db.session.query(Role).filter(
            Role.id == db.session.query(User).filter(User.stuid == stuid).first().role_id).first().role == 'svip':
        title = u'<a href="/svip">Svip管理界面</a>'
    else:
        title = u'用户中心'
    return render_template('userinfo.html', data=data, title=title)


@app.route('/userinfo/account', methods=['POST', 'GET'])
def account():
    stuid = session.get('stuid')
    if stuid is None:
        return redirect('/login')
    elif request.method == 'POST':
        r = RedisHelper('127.0.0.1', 6379)
        upwd = request.form.get('upwd', '')
        newpwd = request.form.get('newpwd', '')
        newpwd2 = request.form.get('newpwd2', '')
        s1 = sha()
        s1.update(upwd)
        pwd = s1.hexdigest()
        s2 = sha()
        s2.update(newpwd)
        shanewpwd = s2.hexdigest()
        user = db.session.query(User).filter(User.pwd == pwd).first()
        if upwd != '' and newpwd != '' and newpwd2 != '' and newpwd == newpwd2 and user is not None:
            user.pwd = shanewpwd
            db.session.commit()
            r.set(stuid, shanewpwd)
            return redirect('/userinfo')
        else:
            title = u'密码修改失败'
            return render_template('account.html', title=title)
    title = u'帐号管理'
    return render_template('account.html', title=title)


@app.route('/userinfo/datum', methods=['POST', 'GET'])
def datum():
    stuid = session.get('stuid')
    if stuid is None:
        return redirect('/login')
    elif request.method == 'POST':
        name = request.form.get('name', '')
        phone = request.form.get('phone', '')
        college = request.form.get('college', '')
        userclass = request.form.get('userclass', '')
        if name.strip() != '' and phone.strip() != '' and college.strip() != '' and userclass.strip() != '':
            user = db.session.query(User).filter(User.stuid == stuid).first()
            user.name = name
            user.phone = phone
            user.college = college
            user.userclass = userclass
            db.session.commit()
            return redirect('/userinfo')
        else:
            title = u'资料修改失败'
            return render_template('datum.html', title=title)
    title = u'修改资料'
    return render_template('datum.html', title=title)


@app.route('/super', methods=['GET', 'POST'])
def infosuper():
    if session.get('stuid') is None:
        return redirect('/login')
    elif db.session.query(Role).filter(
            Role.id == db.session.query(User).filter(
                User.stuid == session.get('stuid')).first().role_id).first().role == 'super':
        mv = db.session.query(Mv).all()
        music = db.session.query(Music).all()
        if request.method == 'POST':
            mvid = request.form.get('mvid', '')
            mvname = request.form.get('mvname', '')
            mvurl = request.form.get('mvurl', '')
            if mvid.strip() != '' and mvname.strip() != '' and mvurl.strip() != '':
                mv1 = Mv(id=mvid, mvname=mvname, mvurl=mvurl)
                db.session.add(mv1)
                db.session.commit()
                return redirect('/super')
            musicid = request.form.get('musicid', '')
            musicname = request.form.get('musicname', '')
            musicurl = request.form.get('musicurl', '')
            if musicid.strip() != '' and musicname.strip() != '' and musicurl.strip() != '':
                music1 = Music(id=musicid, musicname=musicname, musicurl=musicurl)
                db.session.add(music1)
                db.session.commit()
                return redirect('/super')
        return render_template('super.html', mv=mv, music=music)
    else:
        return redirect('/userinfo')


@app.route('/superdelete', methods=['POST'])
def superdelete():
    if db.session.query(Role).filter(
            Role.id == db.session.query(User).filter(
                User.stuid == session.get('stuid')).first().role_id).first().role == 'super':
        mvid = request.form.get('mvid', '')
        deid = db.session.query(Mv).filter(Mv.id == mvid).first()
        if deid is not None:
            db.session.delete(deid)
            db.session.commit()
    return redirect('/super')


@app.route('/musicdelete', methods=['POST'])
def musicdelete():
    if db.session.query(Role).filter(
            Role.id == db.session.query(User).filter(
                User.stuid == session.get('stuid')).first().role_id).first().role == 'super':
        musicid = request.form.get('musicid', '')
        deid = db.session.query(Music).filter(Music.id == musicid).first()
        if deid is not None:
            db.session.delete(deid)
            db.session.commit()
    return redirect('/super')


@app.route('/superuser', methods=['GET', 'POST'])
def superuser():
    if session.get('stuid') is None:
        return redirect('/login')
    elif db.session.query(Role).filter(
            Role.id == db.session.query(User).filter(
                User.stuid == session.get('stuid')).first().role_id).first().role == 'super':
        user = db.session.query(User).all()
        if request.method == 'POST':
            userstuid = request.form.get('userstuid', '')
            upwd = request.form.get('upwd', '')
            roleid = request.form.get('roleid', '')
            s1 = sha()
            s1.update(upwd)
            pwd = s1.hexdigest()
            if userstuid.strip() != '' and upwd.strip() != '' and roleid.strip() != '':
                user1 = db.session.query(User).filter(User.stuid == userstuid).first()
                user1.pwd = pwd
                user1.role_id = roleid
                db.session.commit()
                return redirect('/superuser')
        return render_template('superuser.html', user=user)
    else:
        return redirect('/userinfo')


@app.route('/svip', methods=['GET', 'POST'])
def infosvip():
    if session.get('stuid') is None:
        return redirect('/login')
    elif db.session.query(Role).filter(
            Role.id == db.session.query(User).filter(
                User.stuid == session.get('stuid')).first().role_id).first().role == 'svip':
        mv = db.session.query(Mv).all()
        music = db.session.query(Music).all()
        if request.method == 'POST':
            mvid = request.form.get('mvid', '')
            mvname = request.form.get('mvname', '')
            mvurl = request.form.get('mvurl', '')
            if mvid.strip() != '' and mvname.strip() != '' and mvurl.strip() != '':
                mv1 = Mv(id=mvid, mvname=mvname, mvurl=mvurl)
                db.session.add(mv1)
                db.session.commit()
                return redirect('/svip')
            musicid = request.form.get('musicid', '')
            musicname = request.form.get('musicname', '')
            musicurl = request.form.get('musicurl', '')
            if musicid.strip() != '' and musicname.strip() != '' and musicurl.strip() != '':
                music1 = Music(id=musicid, musicname=musicname, musicurl=musicurl)
                db.session.add(music1)
                db.session.commit()
                return redirect('/svip')
        return render_template('svip.html', mv=mv, music=music)
    else:
        return redirect('/userinfo')


if __name__ == '__main__':
    manage.run()
