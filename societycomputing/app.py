from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# 从JSON文件加载用户数据
def load_user_data():
    try:
        with open('user_data_with_history.json', 'r') as f:
            users = json.load(f)

        return users
    except FileNotFoundError:
        print("错误：未找到 user_data_with_history.json 文件")
        return []
    except json.JSONDecodeError:
        print("错误：user_data_with_history.json 文件格式不正确")
        return []

# 加载用户数据
users = load_user_data()

@app.route('/')
def index():
    return render_template('multi_user.html', users=users[:min(20, len(users))])

@app.route('/user/<int:user_id>')
def user_details(user_id):
    user = next((user for user in users if user["user_id"] == user_id), None)
    if user:
        return render_template('user_details.html', user=user)
    else:
        return "User not found", 404


if __name__ == '__main__':
    app.run(debug=True)