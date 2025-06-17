from pyspark.sql import SparkSession
from features.build_features import build_feature_pipeline
from models.train_model import train_and_save
from models.evaluate_model import evaluate_model
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Tạo SparkSession
spark = SparkSession.builder \
    .appName("LogisticRegressionProject") \
    .getOrCreate()

# Đọc dữ liệu
df = spark.read.csv("data/processed/data_cleaned.csv", header=True, inferSchema=True)

# Cột đích
label = "result"

# Cấu hình mô hình: (features, model_path, tên mô hình)
config1 = [
    (
        ["category", "price", "num_lectures", "avg_rating"],
        "models/model1",
        "Mô hình 1: Dự đoán theo category, price, num_lectures, avg_rating"
    ),
    (
        ["category", "num_subscribers", "num_reviews", "num_comments", "avg_rating"],
        "models/model2",
        "Mô hình 2: Dự đoán theo category, num_subscribers, num_reviews, num_comments, avg_rating"
    )
]
config2 = [
    (
        ["category", "topic", "language", "price"],
        "models/model3",
        "Mô hình 3: Dự đoán theo category, topic, language, price"
    ),
    (
        ["category", "num_lectures", "content_length_min", "avg_rating"],
        "models/model4",
        "Mô hình 4: Dự đoán theo category, num_lectures, content_length_min, avg_rating"
    )
]
config3 = [
    (
        ["price", "subcategory", "language", "content_length_min"],
        "models/model5",
        "Mô hình 5: Dự đoán theo price, subcategory, content_length_min"
    ),
    (
        ["price", "num_subscribers", "avg_rating", "category"],
        "models/model6",
        "Mô hình 6: Dự đoán theo price, num_subscribers, avg_rating, category"
    )
]


# Chạy từng mô hình
for features, model_path, model_name in config1:
    print(f"\n===== Đang huấn luyện: {model_name} =====")
    stages = build_feature_pipeline(df, features)
    model = train_and_save(df, stages, label, model_path)
    evaluate_model(model, df, label_col=label, model_name=model_name, model_path=model_path)

for features, model_path, model_name in config2:
    print(f"\n===== Đang huấn luyện: {model_name} =====")
    stages = build_feature_pipeline(df, features)
    model = train_and_save(df, stages, label, model_path)
    evaluate_model(model, df, label_col=label, model_name=model_name, model_path=model_path)

for features, model_path, model_name in config3:
    print(f"\n===== Đang huấn luyện: {model_name} =====")
    stages = build_feature_pipeline(df, features)
    model = train_and_save(df, stages, label, model_path)
    evaluate_model(model, df, label_col=label, model_name=model_name, model_path=model_path)

# Dừng SparkSession
spark.stop()