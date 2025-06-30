import json
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score
from config import METRICS_PATH, FEATURE_PLOT_PATH

def evaluate_model(model, X_val, y_val):
    y_pred_prob = model.predict_proba(X_val)[:, 1]
    y_pred = (y_pred_prob > 0.5).astype(int)

    metrics = {
        "roc_auc": roc_auc_score(y_val, y_pred_prob),
        "accuracy": accuracy_score(y_val, y_pred),
        "precision": precision_score(y_val, y_pred),
        "recall": recall_score(y_val, y_pred),
    }

    with open(METRICS_PATH, 'w') as f:
        json.dump(metrics, f, indent=2)

    print(f" 验证评估结果已保存至 {METRICS_PATH}")

    # 特征重要性图
    importance = model.booster_.feature_importance()
    names = model.booster_.feature_name()

    plt.figure(figsize=(8, 6))
    plt.barh(names, importance)
    plt.title("Feature Importance")
    plt.tight_layout()
    plt.savefig(FEATURE_PLOT_PATH)
    print(f" 特征重要性图已保存至 {FEATURE_PLOT_PATH}")
