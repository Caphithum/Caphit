from flask import Flask, render_template, request, redirect, url_for
import os
import pymysql
from pymysql import Error
from flask import Flask, render_template, request, redirect, url_for, session
import json
from werkzeug.security import generate_password_hash, check_password_hash
import cv2

app = Flask(__name__)
app.secret_key = 'dsdfsfdaxxx'
app.config['UPLOAD_FOLDER'] = 'uploads/'

def get_db_connection():
    # 连接数据库
    db = pymysql.connect(user='root', password='123456', host='localhost', port=3306, database='project_data')
    return db

def save_to_db_images(filename):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # query = "INSERT INTO images (image_path) VALUES (%s)"
        # query = "INSERT INTO images (image) VALUES (LOAD_FILE(%s))"
        filename = filename.replace("\\", "/")
        print(filename)
        query1 = "SELECT MAX(autoid) FROM images"
        cursor.execute(query1)
        result = cursor.fetchone()
        last_row_number = result[0] if result[0] else 0
        last_row_number = int(last_row_number) + 1
        print(last_row_number)
        # params = (last_row_number, filename)  # 将两个参数放在一个元组中
        # cursor.execute(query, params)  # 将元组作为第二个参数传递给execute()
        cursor.execute(
            "INSERT INTO images (autoid,image) VALUES ('{}', LOAD_FILE('{}') )".format(last_row_number, filename))
        print(filename,last_row_number)
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(e)

def getFile_images():
    # 打开数据库连接
    connection = get_db_connection()
    cursor = connection.cursor()
    query1 = "SELECT MAX(autoid) FROM images"
    cursor.execute(query1)
    result = cursor.fetchone()
    last_row_number = result[0] if result[0] else 0
    last_row_number = int(last_row_number)
    sql = "SELECT image FROM images where autoid = '{}'".format(last_row_number)
    cursor.execute(sql)
    data = cursor.fetchone()
    # 保存 BLOB 数据到文件
    blob_data = data[0]
    #with open('存放文件的位置/文件名.扩展名', 'wb') as f:
    #    f.write(base64.b64decode(data[2]))
    #例如下面
    with open('static/worked_images/worked.png', 'wb') as f:
    	f.write(blob_data)#解密即可
    # 释放内存
    cursor.close()
    connection.close()

# 保存图片到数据库
def save_to_db_videos(filename,name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # query = "INSERT INTO images (image_path) VALUES (%s)"
        # query = "INSERT INTO images (image) VALUES (LOAD_FILE(%s))"
        filename = filename.replace("\\","/")
        cap = cv2.VideoCapture(filename)
        isOpened = cap.isOpened
        imageNum = 0
        sum = 0
        timef = 60
        print(filename)
        query1 = "SELECT MAX(autoid) FROM videoimages"
        cursor.execute(query1)
        result = cursor.fetchone()
        last_row_number = result[0] if result[0] else 0
        last_row_number = int(last_row_number) + 1
        print("last:")
        print(last_row_number)
        # # query = "INSERT INTO images (autoid,image) VALUES (%d,LOAD_FILE(%s))"
        # # cursor.execute(query, last_row_number, filename)  # 修改为你的本地目录路径和文件名
        # # query = "INSERT INTO images (autoid,image) VALUES (%d,LOAD_FILE(%s))"
        # # params = (last_row_number, filename)  # 将两个参数放在一个元组中
        # # cursor.execute(query, params)  # 将元组作为第二个参数传递给execute()
        # cursor.execute("INSERT INTO videos (autoid,video) VALUES ('{}', LOAD_FILE('{}') )".format(last_row_number,filename))
        while (isOpened):
            if imageNum == 200:
                break
            sum += 1
            (frameState, frame) = cap.read()

            if frameState == True and sum % timef == 0:
                imageNum += 1
                fileName = 'D:\\heirun\\xxxxxl\\framework\\static\\videos_img' + '/' + str(name) +  "-" + str(imageNum) + '.jpg'
                cv2.imwrite(fileName, frame)
                print(fileName + " successfully write in")
                # cursor.execute("INSERT INTO videoimages (autoid,videoname,image) VALUES ('{}', '{}',LOAD_FILE('{}') )".format(last_row_number,filename,fileName))
                cursor.execute(
                    "INSERT INTO videoimages (autoid,videoname,image) VALUES ('{}','{}','{}')".format(
                        last_row_number, name, frame))

                last_row_number = last_row_number + 1
            elif frameState == False:
                break
        print('finish!')
        cap.release()  # 释放视频资源
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(e)

def getFile_videos(name):
    # 打开数据库连接
    connection = get_db_connection()
    cursor = connection.cursor()
    query1 = "SELECT MAX(autoid) FROM videos"
    cursor.execute(query1)
    result = cursor.fetchone()
    last_row_number = result[0] if result[0] else 0
    last_row_number = int(last_row_number)
    sql = "SELECT video FROM videos where autoid = '{}'".format(last_row_number)
    cursor.execute(sql)
    data = cursor.fetchone()
    # 保存 BLOB 数据到文件
    # blob_data = data[0]
    #with open('存放文件的位置/文件名.扩展名', 'wb') as f:
    #    f.write(base64.b64decode(data[2]))
    #例如下面
    # with open('static/worked_videos/worked.mp4', 'wb') as f:
    # 	f.write(blob_data)#解密即可
    # 释放内存
    cursor.close()
    connection.close()



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
        # print(username)
        users[username] = [generate_password_hash(password), name]
        fl.seek(0)
        json.dump(users, fl)
        fl.truncate()
    return True

def verify_user(username, password):
    # print("verify_user")
    file = users_file
    global userName
    userName = username
    with open(file) as f:
        users = json.load(f)
        # 用户存在且密码验证通过
        return username in users and check_password_hash(users[username][0], password)

@app.route('/', methods=['GET'])
def index():  # put application's code here
    return render_template("login.html")

@app.route('/login', methods=['POST', 'GET'])
def login():
    username = request.form.get("username")
    password = request.form.get('password')
    if verify_user(username, password):
        # print("yes_teacher3")
        return render_template('index.html')
    else:
        print("no")
        return render_template('login.html')

@app.route('/toRegister', methods=['GET'])
def toRegister():
    return render_template('register.html')

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


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['image']  # 从请求中获取文件
        filename = os.path.join(os.getcwd(), 'static/uploaded_images', file.filename)  # 拼接文件绝对路径
        file.save(filename)  # 将文件保存到本地文件系统
        save_to_db_images(filename)  # 将文件存储到数据库中
        getFile_images()
        return redirect(url_for('uploaded_file', filename=file.filename))  # 重定向到文件上传成功的页面
    return render_template('upload.html')

@app.route('/uploaded_file/<filename>')
def uploaded_file(filename):
    return render_template('index1.html', filename=filename)  # 显示已上传的图片

@app.route('/upload_video', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        file = request.files['video']  # 从请求中获取文件
        filename = os.path.join(os.getcwd(), 'static/uploaded_videos', file.filename)  # 拼接文件绝对路径
        file.save(filename)  # 将文件保存到本地文件系统
        save_to_db_videos(filename,file.filename)  # 将文件存储到数据库中
        getFile_videos(filename,file.filename)
        return redirect(url_for('uploaded_file1', filename=file.filename))  # 重定向到文件上传成功的页面
    return render_template('upload_video.html')

@app.route('/uploaded_file1/<filename>')
def uploaded_file1(filename):
    return render_template('index2.html', filename=filename)  # 显示已上传的视频

if __name__ == '__main__':
    app.run(debug=True)
