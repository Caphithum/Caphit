import json
import os

from flask import Flask, request, jsonify, render_template, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():  # put application's code here
    return render_template("login.html")


users_file = 'static/json/user.json'
iden = 'student'
userName = 'name'

# 确保用户文件存在
if not os.path.exists(users_file):
    with open(users_file, 'w') as f:
        json.dump({}, f)


def save_new_user(username, password, name):
    file = users_file

    with open(file, 'r+') as fl:
        users = json.load(fl)
        if username in users:
            return False
        # 密码哈希化后存储
        print(username)
        users[username] = [generate_password_hash(password), name]
        fl.seek(0)
        json.dump(users, fl)
        fl.truncate()
    return True


def verify_user(username, password):
    print("verify_user")
    file = users_file
    global userName
    userName = username
    with open(file) as f:
        users = json.load(f)
        # 用户存在且密码验证通过
        return username in users and check_password_hash(users[username][0], password)


@app.route('/name', methods=['post'])
def get_name_from_json():
    file = users_file
    with open(file) as f:
        users = json.load(f)
        data = [users[userName][1], iden]
        return jsonify(data)


@app.route('/register', methods=['GET', 'POST'])
def register():
    username = request.form.get("username")
    password = request.form.get('password')
    password2 = request.form.get('password2')
    name = request.form.get('name')
    print(name)
    if password2 != password:
        return render_template('register.html')
    if save_new_user(username, password, name):
        return render_template('login.html')
    else:
        return render_template('register.html')


@app.route('/toRegister', methods=['GET'])
def toRegister():
    return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    username = request.form.get("username")
    password = request.form.get('password')
    if verify_user(username, password):
        print("yes_teacher3")
        return render_template('index.html')
    else:
        print("no")
        return render_template('login.html')


@app.route('/logout')
def logout():
    return render_template("login.html")


@app.route('/search')
def search():
    return render_template("search.html")


if __name__ == '__main__':
    app.run()
