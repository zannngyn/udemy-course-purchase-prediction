from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
import os

def train_and_save(df, stages, label_col, model_path):
    lr = LogisticRegression(featuresCol="features", labelCol=label_col)
    pipeline = Pipeline(stages=stages + [lr])

    model = pipeline.fit(df)
    # tự tạo thư mục nếu chưa có
    model.write().overwrite().save(model_path)  
    return model

