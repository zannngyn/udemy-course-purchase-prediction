from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from sklearn.metrics import confusion_matrix, f1_score, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import os

def evaluate_model(model, df, label_col="result", model_name=None, model_path=None):
    # Dự đoán
    predictions = model.transform(df).select(label_col, "prediction")

    # Convert to pandas để dễ dùng sklearn
    pdf = predictions.toPandas()

    y_true = pdf[label_col]
    y_pred = pdf["prediction"]

    acc = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average='weighted')

    print("====== ĐÁNH GIÁ MÔ HÌNH ======")
    if model_name:
        print(f" Model: {model_name}")
    print(f" Accuracy: {acc:.4f}")
    print(f" F1-score: {f1:.4f}")

    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title(f"Confusion Matrix{f' - {model_name}' if model_name else ''}")
    plt.tight_layout()
    plt.show()
    
    # Lưu mô hình 
    if model_path:
        # Kiểm tra nếu thư mục đã tồn tại thì xóa
        if os.path.exists(model_path):
            import shutil
            shutil.rmtree(model_path)

        model.save(model_path)
        print(f" Mô hình đã được lưu vào: {model_path}")
