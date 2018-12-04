# coding=utf-8
from flask import Flask, render_template
from flask_script import Manager

app = Flask(__name__)
manage = Manager(app)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    manage.run()
