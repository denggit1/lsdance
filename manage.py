# coding=utf-8
from flask import Flask, render_template
from flask_script import Manager

app = Flask(__name__)
manage = Manager(app)


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


if __name__ == '__main__':
    manage.run()
