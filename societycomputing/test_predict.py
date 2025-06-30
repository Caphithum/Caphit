from preprocess import preprocess_data
from utils.inference import get_topk_recommendations, evaluate_topk_hit
import lightgbm as lgb
import pandas as pd
import json
import os

print(" Top-K 推荐测试评估启动...")
_, _, test_df = preprocess_data(split=True)

print(" 加载训练好的模型...")
model = lgb.Booster(model_file='./output/lgb_model.txt')

print(" 筛选测试用户...")
# test_users = test_df['user_id'].unique()
test_users = test_df['user_id'].drop_duplicates().head(20).values
features = ['click', 'cart', 'fav', 'gender', 'age_range',
            'merchant_click_ratio', 'merchant_cart_ratio', 'merchant_fav_ratio', 'merchant_total_action']

print(" 执行 Top-K 推荐...")
topk_df = get_topk_recommendations(model, test_users, test_df, features, k=10)

print(" 计算命中率...")
hit_table, metrics = evaluate_topk_hit(topk_df, test_df)

os.makedirs("output", exist_ok=True)
hit_table.to_csv("output/hit_table.csv", index=False)
with open("output/hit_metrics.json", "w") as f:
    json.dump(metrics, f, indent=2, ensure_ascii=False)

