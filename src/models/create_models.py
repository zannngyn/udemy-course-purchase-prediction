import io
import sys
from src.models import train_model as tm
from src.models import evaluate_model as em
from pyspark.sql import SparkSession
from src.features import  build_features as bf
import findspark
findspark.init()


def train_all_models():
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
            ["price", "subcategory", "content_length_min"],
            "model/model5",
            "Mô hình 5: Dự đoán theo price, subcategory, content_length_min"
        ),
        (
            ["price", "num_subscribers", "avg_rating", "category"],
            "model/model6",
            "Mô hình 6: Dự đoán theo price, num_subscribers, avg_rating,  category "
        )
    ]

    # Chạy từng mô hình
    for features, model_path, model_name in config1:
        print(f"\n===== Đang huấn luyện: {model_name} =====")
        stages = bf.build_feature_pipeline(df, features)
        model = tm.train_and_save(df, stages, label, model_path)
        em.evaluate_model(model, df, label_col=label, model_name=model_name, model_path=model_path)

    for features, model_path, model_name in config2:
        print(f"\n===== Đang huấn luyện: {model_name} =====")
        stages = bf.build_feature_pipeline(df, features)
        model = tm.train_and_save(df, stages, label, model_path)
        em.evaluate_model(model, df, label_col=label, model_name=model_name, model_path=model_path)

    for features, model_path, model_name in config3:
        print(f"\n===== Đang huấn luyện: {model_name} =====")
        stages = bf.build_feature_pipeline(df, features)
        model = tm.train_and_save(df, stages, label, model_path)
        em.evaluate_model(model, df, label_col=label, model_name=model_name, model_path=model_path)

    # Dừng SparkSession
    spark.stop()