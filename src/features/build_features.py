from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler, StandardScaler
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def build_feature_pipeline(df, features):
    dtypes = dict(df.dtypes)
    
    # Tách ra cột dạng chuỗi và số
    string_cols = [c for c in features if dtypes.get(c) == 'string']
    num_cols = [c for c in features if dtypes.get(c) != 'string']

    stages = []

    # Xử lý cột chuỗi
    if string_cols:
        indexers = [StringIndexer(inputCol=c, outputCol=f"{c}_idx", handleInvalid='keep') for c in string_cols]
        encoders = [OneHotEncoder(inputCol=f"{c}_idx", outputCol=f"{c}_vec") for c in string_cols]
        stages += indexers + encoders

    # Xử lý cột số
    if num_cols:
        assembler_num = VectorAssembler(inputCols=num_cols, outputCol="numeric")
        scaler = StandardScaler(inputCol="numeric", outputCol="scaled")
        stages += [assembler_num, scaler]

    # Kết hợp đặc trưng
    final_features = []
    if string_cols:
        final_features += [f"{c}_vec" for c in string_cols]
    if num_cols:
        final_features.append("scaled")

    if not final_features:
        raise ValueError("Không có đặc trưng nào để huấn luyện mô hình.")

    assembler_all = VectorAssembler(inputCols=final_features, outputCol="features")
    stages.append(assembler_all)

    return stages
