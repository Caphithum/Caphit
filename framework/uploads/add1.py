import pymysql
from flask import Flask, request, redirect, url_for, render_template
import os
from pymysql import Error

app = Flask(__name__)
app.secret_key = 'dsdfsfdaxxx'

# 数据库连接对象
def get_db_connection():
    # 连接数据库
    db = pymysql.connect(user='root', password='123456', host='localhost', port=3306, database='project_data')
    return db

# 保存图片到数据库
def save_to_db_videos(filename):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # query = "INSERT INTO images (image_path) VALUES (%s)"
        # query = "INSERT INTO images (image) VALUES (LOAD_FILE(%s))"
        filename = filename.replace("\\","/")
        print(filename)
        query1 = "SELECT MAX(autoid) FROM videos"
        cursor.execute(query1)
        result = cursor.fetchone()
        last_row_number = result[0] if result[0] else 0
        last_row_number = int(last_row_number) + 1
        print(last_row_number)
        # query = "INSERT INTO images (autoid,image) VALUES (%d,LOAD_FILE(%s))"
        # cursor.execute(query, last_row_number, filename)  # 修改为你的本地目录路径和文件名
        # query = "INSERT INTO images (autoid,image) VALUES (%d,LOAD_FILE(%s))"
        # params = (last_row_number, filename)  # 将两个参数放在一个元组中
        # cursor.execute(query, params)  # 将元组作为第二个参数传递给execute()
        cursor.execute("INSERT INTO videos (autoid,video) VALUES ('{}', LOAD_FILE('{}') )".format(last_row_number,filename))
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(e)

def getFile_videos():
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
    blob_data = data[0]
    #with open('存放文件的位置/文件名.扩展名', 'wb') as f:
    #    f.write(base64.b64decode(data[2]))
    #例如下面
    with open('static/worked_videos/worked.mp4', 'wb') as f:
    	f.write(blob_data)#解密即可
    # 释放内存
    cursor.close()
    connection.close()

# 上传本地图片
@app.route('/')
@app.route('/upload_video', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        file = request.files['video']  # 从请求中获取文件
        filename = os.path.join(os.getcwd(), 'static/uploaded_videos', file.filename)  # 拼接文件绝对路径
        file.save(filename)  # 将文件保存到本地文件系统
        save_to_db_videos(filename)  # 将文件存储到数据库中
        getFile_videos()
        return redirect(url_for('uploaded_file', filename=file.filename))  # 重定向到文件上传成功的页面
    return render_template('upload_video.html')

@app.route('/uploaded_file/<filename>')
def uploaded_file(filename):
    return render_template('index2.html', filename=filename)  # 显示已上传的视频

if __name__ == '__main__':
    app.run(debug=True)
