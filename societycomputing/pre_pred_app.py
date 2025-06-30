# 数据预处理并划分 train / val / test
import pandas as pd
import numpy as np
from tools import reduce_mem_usage


def get_train_val_test_split(df, user_col='user_id', seed=42):
    users = df[user_col].unique()
    np.random.seed(seed)
    np.random.shuffle(users)

    n = len(users)
    train_users = users[:int(0.8 * n)]
    val_users = users[int(0.8 * n):int(0.9 * n)]
    test_users = users[int(0.9 * n):]

    train_df = df[df[user_col].isin(train_users)]
    val_df = df[df[user_col].isin(val_users)]
    test_df = df[df[user_col].isin(test_users)]
    return train_df, val_df, test_df


def preprocess_data(split=False, return_all=False):
    # 读取原始数据
    user_log = pd.read_csv('./user_log_format1.csv')
    user_info = pd.read_csv('./user_info_format1.csv')

    # 获取前20个不同的用户ID（按首次出现顺序）
    first_20_users = user_log['user_id'].drop_duplicates().head(20).tolist()

    # 筛选只包含这20个用户的数据
    user_log = user_log[user_log['user_id'].isin(first_20_users)]
    user_info = user_info[user_info['user_id'].isin(first_20_users)]

    df = user_log.copy()

    df = reduce_mem_usage(df)
    user_info = reduce_mem_usage(user_info)

    # 构建行为特征
    action_pivot = df.pivot_table(index=['user_id', 'item_id'], columns='action_type', aggfunc='size',
                                  fill_value=0).reset_index()
    action_pivot.columns.name = None
    action_pivot.columns = ['user_id', 'item_id', 'click', 'cart', 'buy', 'fav'][:action_pivot.shape[1]]

    # 构建标签
    df['label'] = (df['action_type'] == 2).astype(int)
    labels = df.groupby(['user_id', 'item_id'])['label'].max().reset_index()

    # 合并行为与标签
    df = pd.merge(action_pivot, labels, on=['user_id', 'item_id'], how='left')
    df = pd.merge(df, user_info, on='user_id', how='left')

    # 商家画像（只计算这20个用户相关的商家）
    seller_stats = user_log.groupby('seller_id')['action_type'].value_counts().unstack().fillna(0)
    seller_stats.columns = ['merchant_click_ratio', 'merchant_cart_ratio', 'merchant_fav_ratio', 'merchant_buy_ratio'][
                           :seller_stats.shape[1]]
    seller_stats['merchant_total_action'] = seller_stats.sum(axis=1)
    seller_stats = seller_stats.reset_index()

    df = pd.merge(df, user_log[['item_id', 'seller_id']].drop_duplicates(), on='item_id', how='left')
    df = pd.merge(df, seller_stats, on='seller_id', how='left')
    df.drop(columns=['seller_id'], inplace=True)
    df.columns = df.columns.str.replace('_x', '').str.replace('_y', '')

    if return_all:
        return df, user_info, seller_stats
    elif split:
        return get_train_val_test_split(df)
    else:
        return df


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
test_users = test_df['user_id'].drop_duplicates().head(20).values
features = ['click', 'cart', 'fav', 'gender', 'age_range',
            'merchant_click_ratio', 'merchant_cart_ratio', 'merchant_fav_ratio', 'merchant_total_action']

print(" 执行 Top-K 推荐...")
topk_df = get_topk_recommendations(model, test_users, test_df, features, k=10)

print(" 计算命中率...")
hit_table, metrics = evaluate_topk_hit(topk_df, test_df)

# 读取用户信息文件
user_info = pd.read_csv('user_info_format1.csv')
# 转换gender为字符串表示
gender_map = {0: 'Female', 1: 'Male', 2: 'Unknown'}
user_info['gender'] = user_info['gender'].map(gender_map)

# 读取用户行为日志文件
user_log = pd.read_csv('user_log_format1.csv')

# 获取前20个不同的用户ID（按首次出现顺序）
first_20_users = user_log['user_id'].drop_duplicates().head(20).tolist()

# 准备最终的用户数据列表
users = []

i = 0

# 为每个用户构建数据
for user_id in first_20_users:
    # 获取用户基本信息
    user_data = user_info[user_info['user_id'] == user_id].iloc[0]

    # 获取用户行为历史
    user_history = user_log[user_log['user_id'] == user_id]
    history_records = []
    for _, row in user_history.iterrows():
        history_records.append({
            "item_id": row['item_id'],
            "cat_id": row['cat_id'],
            "seller_id": row['seller_id'],
            "brand_id": row['brand_id'],
            "time_stamp": str(row['time_stamp']).zfill(4),  # 保证4位时间戳
            "action_type": row['action_type']
        })

    # 从topk_df获取该用户的推荐结果
    user_recommendations_list = topk_df.groupby('user_id')['recommended_items'].apply(list).tolist()
    user_recommendations = user_recommendations_list[i]
    i = i + 1

    # 构建用户对象
    user_obj = {
        "user_id": user_id,
        "gender": user_data['gender'],
        "age": user_data['age_range'],
        "history": history_records,
        "recommendations": user_recommendations  # 使用实际的推荐结果
    }

    users.append(user_obj)

# 将结果保存为JSON文件
with open('user_data_with_history.json', 'w') as f:
    json.dump(users, f, indent=2)

print(f"已处理完成，共生成 {len(users)} 个用户的数据")
print("结果已保存到 user_data_with_history.json 文件")