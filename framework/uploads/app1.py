from flask import Flask, render_template, request, redirect, url_for
import os
import pymysql
from pymysql import Error
from flask import Flask, render_template, request, redirect, url_for, session
import json
from werkzeug.security import generate_password_hash, check_password_hash
import cv2
from ultralytics import YOLO
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'dsdfsfdaxxx'
app.config['UPLOAD_FOLDER'] = 'uploads/'


def yolo(pt_path, img_path, save_path, class_red):
    # 加载 YOLO 模型
    model = YOLO(pt_path)
    # 读取图片路径
    imgPath = img_path
    # 运行模型进行推理
    results = model(imgPath, augment=True)
    # 读取原始图片
    img = cv2.imread(imgPath)
    # 遍历所有检测框
    for result in results:
        # 获取检测框和类别
        boxes = result.boxes
        for box in boxes:
            # 获取坐标和类别
            x1, y1, x2, y2 = box.xyxy[0].numpy().astype(int)
            cls = int(box.cls[0].item())
            conf = box.conf[0].item()

            # 如果置信度大于阈值，绘制矩形框和标签
            if conf >= 0.85:
                label = model.names[cls]
                if label == class_red:
                    fill_color = (0, 0, 255)
                else:
                    fill_color = (0, 255, 0)

                # 计算文本大小
                font_scale = 0.5
                font_thickness = 2
                (text_width, text_height), baseline = cv2.getTextSize(f'{label} {conf:.2f}', cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)

                # 绘制目标位置框（与背景框颜色一致）
                cv2.rectangle(img, (x1, y1), (x2, y2), fill_color, 2)

                # 绘制背景矩形框
                cv2.rectangle(img, (x1, y1 - text_height - baseline), (x1 + text_width, y1), fill_color, -1)

                # 绘制文字（白色）
                cv2.putText(img, f'{label} {conf:.2f}', (x1, y1 - baseline), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness)

    # 保存处理后的图片
    save_path = save_path
    cv2.imwrite(save_path, img)


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
def andex():  # put application's code here
    return render_template("login.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    username = request.form.get("username")
    password = request.form.get('password')
    if verify_user(username, password):
        # print("yes_teacher3")
        return render_template('homepage.html')
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
        file = request.files['image']
        if file.filename == '':
            return "未选择文件", 400

        # 安全处理文件名
        filename = file.filename

        # 确保上传和处理目录存在
        upload_dir = 'static/uploaded_images'
        worked_dir = 'static/worked_images'
        os.makedirs(upload_dir, exist_ok=True)
        os.makedirs(worked_dir, exist_ok=True)

        # 保存原始图片
        upload_path = os.path.join(upload_dir, filename)
        file.save(upload_path)

        # 处理图片（YOLO）
        modelpath = 'static/model/best.pt'
        save_path = os.path.join(worked_dir, filename)  # 处理后图片保存路径
        yolo(modelpath, upload_path, save_path,'drowner')

        # 传递两个图片路径到模板
        return render_template('index1.html',
                               original_img=url_for('static', filename=f'uploaded_images/{filename}'),
                               processed_img=url_for('static', filename=f'worked_images/{filename}'))

    return render_template('upload.html')


# @app.route('/upload_video', methods=['GET', 'POST'])
# def upload_video():
#     if request.method == 'POST':
#         file = request.files['video']  # 从请求中获取文件
#         filename = os.path.join(os.getcwd(), 'static/uploaded_videos', file.filename)  # 拼接文件绝对路径
#         file.save(filename)  # 将文件保存到本地文件系统
#         # save_to_db_videos(filename, file.filename)  # 将文件存储到数据库中
#         # getFile_videos(filename,file.filename)
#
#
#         return redirect(url_for('uploaded_file1', filename=file.filename))  # 重定向到文件上传成功的页面
#     return render_template('upload_video.html')

@app.route('/upload_video', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        file = request.files['video']
        if file.filename == '':
            return "未选择文件", 400

        # 确保上传目录存在
        video_dir = 'static/uploaded_videos'
        frame_dir = 'static/videos_img'
        worked_dir = 'static/worked_videos'
        os.makedirs(video_dir, exist_ok=True)
        os.makedirs(frame_dir, exist_ok=True)
        os.makedirs(worked_dir, exist_ok=True)

        # 保存视频文件
        video_path = os.path.join(video_dir, file.filename)
        file.save(video_path)

        # 抽帧处理
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_indices = [int(i * total_frames / 6) for i in range(1, 6)]  # 均匀抽取5帧

        saved_frames = []
        for i, frame_idx in enumerate(frame_indices):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            if ret:
                frame_filename = f"{os.path.splitext(file.filename)[0]}_frame_{i + 1}.jpg"
                frame_path = os.path.join(frame_dir, frame_filename)
                cv2.imwrite(frame_path, frame)
                saved_frames.append(frame_filename)

        cap.release()

        # 传递抽帧结果到模板
        return redirect(url_for('uploaded_file1', filename=file.filename))  # 重定向到文件上传成功的页面

    return render_template('upload_video.html')

@app.route('/uploaded_file1/<filename>')
def uploaded_file1(filename):
    return render_template('index2.html', filename=filename)  # 显示已上传的视频


@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    return render_template('homepage.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/indexfall', methods=['GET', 'POST'])
def indexfall():
    return render_template('indexfall.html')


@app.route('/indexfight', methods=['GET', 'POST'])
def indexfight():
    return render_template('indexfight.html')


# @app.route('/uploadfall', methods=['GET', 'POST'])
# def uploadfall():
#     return render_template('uploadfall.html')

@app.route('/uploadfall', methods=['GET', 'POST'])
def uploadfall():
    if request.method == 'POST':
        file = request.files['image']
        if file.filename == '':
            return "未选择文件", 400

        # 安全处理文件名
        filename = file.filename

        # 确保上传和处理目录存在
        upload_dir = 'static/uploaded_images'
        worked_dir = 'static/worked_images'
        os.makedirs(upload_dir, exist_ok=True)
        os.makedirs(worked_dir, exist_ok=True)

        # 保存原始图片
        upload_path = os.path.join(upload_dir, filename)
        file.save(upload_path)

        # 处理图片（YOLO）
        modelpath = 'static/model/yolov8l.pt'
        save_path = os.path.join(worked_dir, filename)  # 处理后图片保存路径
        yolo(modelpath, upload_path, save_path,'falldown')

        # 传递两个图片路径到模板
        return render_template('index1fall.html',
                               original_img=url_for('static', filename=f'uploaded_images/{filename}'),
                               processed_img=url_for('static', filename=f'worked_images/{filename}'))

    return render_template('uploadfall.html')



@app.route('/index1fall', methods=['GET', 'POST'])
def index1fall():
    return render_template('index1fall.html')


# @app.route('/uploadfight', methods=['GET', 'POST'])
# def uploadfight():
#     return render_template('uploadfight.html')


@app.route('/index1fight', methods=['GET', 'POST'])
def index1fight():
    return render_template('index1fight.html')

@app.route('/uploadfight', methods=['GET', 'POST'])
def uploadfight():
    if request.method == 'POST':
        file = request.files['image']
        if file.filename == '':
            return "未选择文件", 400

        # 安全处理文件名
        filename = file.filename

        # 确保上传和处理目录存在
        upload_dir = 'static/uploaded_images'
        worked_dir = 'static/worked_images'
        os.makedirs(upload_dir, exist_ok=True)
        os.makedirs(worked_dir, exist_ok=True)

        # 保存原始图片
        upload_path = os.path.join(upload_dir, filename)
        file.save(upload_path)

        # 处理图片（YOLO）
        modelpath = 'static/model/yolov8l.pt'
        save_path = os.path.join(worked_dir, filename)  # 处理后图片保存路径
        yolo(modelpath, upload_path, save_path,'fight')

        # 传递两个图片路径到模板
        return render_template('index1fight.html',
                               original_img=url_for('static', filename=f'uploaded_images/{filename}'),
                               processed_img=url_for('static', filename=f'worked_images/{filename}'))

    return render_template('uploadfight.html')

if __name__ == '__main__':
    app.run(debug=True)
