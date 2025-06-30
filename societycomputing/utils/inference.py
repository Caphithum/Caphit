import pandas as pd
from tqdm import tqdm

def get_topk_recommendations(model, test_users, full_df, features, k=10):
    print(f"📌 使用每个用户未交互过的所有商品作为候选池（个性化推荐）...")

    # 全量商品集合
    all_items = full_df['item_id'].unique()

    # item 特征索引表（避免重复 merge）
    item_info_map = (
        full_df[['item_id', 'merchant_click_ratio', 'merchant_cart_ratio',
                 'merchant_fav_ratio', 'merchant_total_action']]
        .drop_duplicates('item_id')
        .set_index('item_id')
    )

    rows = []

    for uid in tqdm(test_users, desc="Top-K推荐中"):
        # 用户已交互商品
        interacted_items = full_df[full_df['user_id'] == uid]['item_id'].unique()
        # 候选池 = 未交互过的商品
        candidate_items = [iid for iid in all_items if iid not in interacted_items]

        if not candidate_items:
            continue

        test_pairs = pd.DataFrame({'item_id': candidate_items})
        test_pairs['user_id'] = uid

        # 加入用户画像
        user_row = full_df[full_df['user_id'] == uid][['gender', 'age_range']].drop_duplicates().iloc[0]
        test_pairs['gender'] = user_row['gender']
        test_pairs['age_range'] = user_row['age_range']

        # 拼接商品画像
        test_pairs = test_pairs.set_index('item_id').join(item_info_map, on='item_id').reset_index()

        # 加入空行为（测试集中不存在）
        test_pairs['click'] = 0
        test_pairs['cart'] = 0
        test_pairs['fav'] = 0
        test_pairs.fillna(0, inplace=True)

        # 批量预测打分
        X = test_pairs[features]
        test_pairs['score'] = model.predict(X)

        # 取 Top-K 推荐结果
        topk_items = (
            test_pairs.sort_values(by='score', ascending=False)
            .head(k)['item_id']
            .tolist()
        )

        rows.append({'user_id': uid, 'recommended_items': topk_items})

    return pd.DataFrame(rows)



def evaluate_topk_hit(topk_df, test_df):
    # 提取测试用户
    test_users = topk_df['user_id'].unique()
    
    # ✅ 加载原始日志（只加载 user_id, item_id, action_type 三列）
    log = pd.read_csv('./user_log_format1.csv', usecols=['user_id', 'item_id', 'action_type'])
    
    # ✅ 只保留测试用户且是交互行为（1,2,3）
    log = log[log['user_id'].isin(test_users)]
    log = log[log['action_type'].isin([1, 2, 3])]
    
    hit_rows = []
    hit_count = 0

    for _, row in topk_df.iterrows():
        uid = row['user_id']
        rec_items = set(row['recommended_items'])
        real_items = log[log['user_id'] == uid]['item_id'].unique()

        hit = len(rec_items & set(real_items)) > 0
        hit_count += int(hit)

        hit_rows.append({
            'user_id': uid,
            'recommended_items': list(rec_items),
            'real_items': list(real_items),
            'hit': int(hit)
        })

    result_df = pd.DataFrame(hit_rows)
    metrics = {
        "TopK": len(row['recommended_items']),
        "hit_user_count": hit_count,
        "test_user_count": len(topk_df),
        "hit_rate": round(hit_count / len(topk_df), 4)
    }

    return result_df, metrics
