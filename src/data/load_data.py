import os
import shutil
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, mean, stddev, when, count, desc, lit, first
from pyspark.sql.window import Window
from pyspark.sql.functions import sum as _sum
# Khởi tạo Spark session
spark = SparkSession.builder \
    .appName("Pre-processing") \
    .getOrCreate()

# Sử dụng Path để định nghĩa đường dẫn đầu vào
base_raw_path = Path("data/raw")
input_file = base_raw_path / "Course_info.csv"

# Đọc file CSV vào DataFrame
df = spark.read.option("header", True).option("inferSchema", True).csv(str(input_file))

# Đếm số giá trị null trên từng cột
null_counts = df.select([
    _sum(when(col(c).isNull(), 1).otherwise(0)).alias(c)
    for c in df.columns
])

# Chuyển về dạng pandas để transpose
null_df = null_counts.toPandas().transpose().reset_index()
null_df.columns = ['column_name', 'missing_count']

# In ra để xem
print(null_df)

# Xử lí missing values bằng cách loại bỏ các dòng có giá trị null
df_clean = df.dropna()

# Xác định các cột số để chuẩn hoá (ngoại trừ 'price' và 'avg_rating')
numeric_cols = [field.name for field in df_clean.schema.fields if str(field.dataType) in ['IntegerType', 'DoubleType', 'FloatType']
                and field.name not in ['price', 'avg_rating']]

# Chuẩn hoá các cột số bằng z-score
for col_name in numeric_cols:
    avg = df_clean.select(mean(col(col_name))).first()[0]
    std = df_clean.select(stddev(col(col_name))).first()[0]
    if std != 0:
        df_clean = df_clean.withColumn(col_name + "_z", (col(col_name) - avg) / std)

# Xác định giá trị 'price' phổ biến nhất theo từng 'category'
mode_price_window = Window.partitionBy("category").orderBy(desc("count"))
price_mode_df = df_clean.groupBy("category", "price") \
    .agg(count("*").alias("count")) \
    .withColumn("rank", first("price").over(mode_price_window)) \
    .drop("count")

# Thêm giá trị price phổ biến nhất vào df_clean
price_mode = price_mode_df.groupBy("category").agg(first("price").alias("most_common_price"))
df_with_mode = df_clean.join(price_mode, on="category", how="left")

# Tạo cột result theo điều kiện
df_result = df_with_mode.withColumn(
    "result",
    when(col("is_paid") == False, 1).   # miễn phí thì luôn thành công
    when((col("is_paid") == True) & (col("avg_rating") > 3.5) & (col("price") <= col("most_common_price")), 1).
    when((col("is_paid") == True) & (col("avg_rating") > 3.5) & (col("price") > col("most_common_price")), 0).
    otherwise(0)
)
# Tóm tắt kết quả
result_summary_df = df_result.groupBy("result").count()
result_summary_df.show()

# Định nghĩa các đường dẫn bằng Path
base_processed_path = Path("data/processed")
output_dir = base_processed_path / "tmp_output"
final_output_path = base_processed_path / "data_cleaned.csv"

# Đảm bảo thư mục đích tồn tại
base_processed_path.mkdir(parents=True, exist_ok=True)

# Ghi dữ liệu vào thư mục tạm (chuyển Path thành chuỗi)
df_result.coalesce(1).write.mode("overwrite").option("header", True).csv(str(output_dir))

# Tìm và di chuyển file kết quả
for file_name in os.listdir(output_dir):
    if file_name.startswith("part-") and file_name.endswith(".csv"):
        # Sử dụng Path để tạo đường dẫn nguồn một cách an toàn
        source_file = output_dir / file_name
        shutil.move(source_file, final_output_path)
        break

# Xóa thư mục tạm
shutil.rmtree(output_dir)
print(f"Ket qua da duoc luu vao: {final_output_path}")

# Dừng Spark session
spark.stop()