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
    val_users   = users[int(0.8 * n):int(0.9 * n)]
    test_users  = users[int(0.9 * n):]

    train_df = df[df[user_col].isin(train_users)]
    val_df   = df[df[user_col].isin(val_users)]
    test_df  = df[df[user_col].isin(test_users)]
    return train_df, val_df, test_df

def preprocess_data(split=False, return_all=False):
    user_log = pd.read_csv('./user_log_format1.csv')
    user_info = pd.read_csv('./user_info_format1.csv')
    df = user_log.copy()

    df = reduce_mem_usage(df)
    user_info = reduce_mem_usage(user_info)

    # 构建行为特征
    action_pivot = df.pivot_table(index=['user_id', 'item_id'], columns='action_type', aggfunc='size', fill_value=0).reset_index()
    action_pivot.columns.name = None
    action_pivot.columns = ['user_id', 'item_id', 'click', 'cart', 'buy', 'fav'][:action_pivot.shape[1]]

    # 构建标签
    df['label'] = (df['action_type'] == 2).astype(int)
    labels = df.groupby(['user_id', 'item_id'])['label'].max().reset_index()

    # 合并行为与标签
    df = pd.merge(action_pivot, labels, on=['user_id', 'item_id'], how='left')
    df = pd.merge(df, user_info, on='user_id', how='left')

    # 商家画像
    seller_stats = user_log.groupby('seller_id')['action_type'].value_counts().unstack().fillna(0)
    seller_stats.columns = ['merchant_click_ratio', 'merchant_cart_ratio', 'merchant_fav_ratio', 'merchant_buy_ratio'][:seller_stats.shape[1]]
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
