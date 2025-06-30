from ultralytics import YOLO

# 加载预训练模型
model = YOLO('yolov8n.pt')  # 会自动下载yolov8n模型

# 进行预测
results = model('https://ultralytics.com/images/bus.jpg')

# 显示结果
results[0].show()