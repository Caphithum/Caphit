import lightgbm as lgb
from config import MODEL_PATH

FEATURES = [
    "click", "cart", "fav",
    "gender", "age_range",
    "merchant_click_ratio", "merchant_cart_ratio",
    "merchant_fav_ratio", "merchant_total_action"
]

def train_lgb_model(train_df, val_df):
    X_train = train_df[FEATURES]
    y_train = train_df["label"]
    X_val = val_df[FEATURES]
    y_val = val_df["label"]

    print(" 训练 LightGBM 模型...")
    model = lgb.LGBMClassifier(
        objective='binary',
        learning_rate=0.05,
        num_leaves=31,
        n_estimators=500,
        n_jobs=-1
    )

    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        eval_metric='auc'
        # early_stopping_rounds=50
    )

    model.booster_.save_model(MODEL_PATH)
    print(f" 模型已保存至 {MODEL_PATH}")
    return model, X_val, y_val
