import json
from werkzeug.security import generate_password_hash

users_file = 'static/json/user.json'
with open(users_file, "r+", encoding="utf-8") as f1:
    users = {}
    username = 'Kim'
    password = '123456'
    name = 'Li Yuan'
    users[username] = [generate_password_hash(password), name]
    json.dump(users, f1)
