from preprocess import preprocess_data
from model import train_lgb_model
from evaluate import evaluate_model

print(" 多行为预测系统启动...")
print(" 读取数据...")
train_df, val_df, _ = preprocess_data(split=True)

print(" 特征构建完成")
print(" 划分训练与验证集...")
model, X_val, y_val = train_lgb_model(train_df, val_df)

print(" 模型评估中...")
evaluate_model(model, X_val, y_val)
