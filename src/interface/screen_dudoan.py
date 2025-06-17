import tkinter as tk
from tkinter import messagebox
import os
import numpy as np
from pyspark.ml import PipelineModel  # Dùng để load mô hình đã huấn luyện bằng PySpark
from pyspark.sql import SparkSession
from pyspark.sql import Row

from src.models.create_models import train_all_models  # Hàm huấn luyện tất cả các mô hình nếu cần

# Hàm kiểm tra đầu vào người dùng theo quy tắc nhập liệu
def validate_entries(entries, rules):
    for key, entry in entries.items():
        val = entry.get().strip()
        if not val:
            messagebox.showerror("Lỗi", f"Trường '{key}' không được để trống.")
            return False
        if key in rules:
            try:
                if not rules[key](val):
                    messagebox.showerror("Lỗi", f"Giá trị không hợp lệ ở trường '{key}'.")
                    return False
            except:
                messagebox.showerror("Lỗi", f"Trường '{key}' phải đúng định dạng.")
                return False
    return True

# Hàm thực hiện dự đoán và hiển thị kết quả
def predict_and_show_result(model_index, fields, raw_values):
    try:
        # Tạo SparkSession để xử lý với mô hình PySpark
        spark = SparkSession.builder.appName("PredictSingleSample").getOrCreate()

        # Đường dẫn đến thư mục chứa model đã huấn luyện
        model_path = os.path.join("models", f"model{model_index}")
        model = PipelineModel.load(model_path)  # Load model PySpark đã lưu

        # Ghép cặp field: value để tạo Row cho Spark DataFrame
        data = {field: try_parse(value) for field, value in zip(fields, raw_values)}
        df_input = spark.createDataFrame([Row(**data)])

        # Dự đoán bằng mô hình
        prediction = model.transform(df_input)
        result = prediction.select("probability", "prediction").first()

        prob = result["probability"][1]  # Xác suất dự đoán label=1 (mua)
        decision = "Mua khoá học" if prob >= 0.5 else "Không mua"

        messagebox.showinfo("Kết quả dự đoán", f"Quyết định: {decision}")
        spark.stop()

    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể dự đoán: {e}")

# Hàm ép kiểu dữ liệu từ string sang float/int nếu có thể
def try_parse(value):
    try:
        if '.' in value:
            return float(value)
        else:
            return int(value)
    except:
        return value.strip()

# Tạo cửa sổ form nhập liệu tương ứng với mỗi mô hình
def create_form_window(parent, title_text, fields, validation_rules, model_index):
    form = tk.Toplevel(parent)
    form.title(title_text)
    form.geometry("400x500")
    form.configure(bg="#f0f8ff")

    tk.Label(form, text=title_text, font=("Arial", 12, "bold"), bg="#f0f8ff", fg="darkblue").pack(pady=10)

    form_frame = tk.Frame(form, bg="#f0f8ff")
    form_frame.pack(pady=10)

    entries = {}
    for field in fields:
        tk.Label(form_frame, text=field, anchor="w", bg="#f0f8ff").pack(fill='x', padx=10)
        entry = tk.Entry(form_frame)
        entry.pack(fill='x', padx=10, pady=5)
        entries[field] = entry

    # Khi nhấn nút "Dự đoán"
    def on_submit():
        if validate_entries(entries, validation_rules):
            try:
                raw_values = [entries[f].get().strip() for f in fields]
                predict_and_show_result(model_index, fields, raw_values)
                form.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi xử lý dữ liệu: {e}")

    submit_btn = tk.Button(form, text="Dự đoán", command=on_submit)
    submit_btn.pack(pady=20)

# Cửa sổ chọn mô hình dự đoán (mở từ cửa sổ chính)
def open_dudoan_window(parent):
    # Nếu chưa huấn luyện mô hình, sẽ gọi train
    train_all_models()

    window = tk.Toplevel(parent)
    window.title("Phân tích dự đoán")
    window.geometry("700x600")
    window.configure(bg="#d0edf5")

    title = tk.Label(window, text="Phân tích dự đoán dựa trên dữ liệu nhập vào", fg="red",
                     bg="#d0edf5", font=("Arial", 14, "bold"))
    title.pack(pady=(20, 5))

    subtitle = tk.Label(window, text="Chọn 1 mô hình để nhập dữ liệu đầu vào",
                        fg="darkred", bg="#d0edf5", font=("Arial", 11))
    subtitle.pack(pady=(0, 20))

    # Cấu hình từng mô hình: mô tả, danh sách trường nhập, và điều kiện kiểm tra
    input_options = [
        ("Mẫu 1: category, price, num_lectures, avg_rating", [
            "category", "price", "num_lectures", "avg_rating"
        ], {
            "price": lambda x: float(x) >= 0,
            "num_lectures": lambda x: int(x) > 0,
            "avg_rating": lambda x: 0 <= float(x) <= 5
        }),

        ("Mẫu 2: category, num_subscribers, num_reviews, num_comments, avg_rating", [
            "category", "num_subscribers", "num_reviews", "num_comments", "avg_rating"
        ], {
            "num_subscribers": lambda x: int(x) >= 0,
            "num_reviews": lambda x: int(x) >= 0,
            "num_comments": lambda x: int(x) >= 0,
            "avg_rating": lambda x: 0 <= float(x) <= 5
        }),

        ("Mẫu 3: category, topic, language, price", [
            "category", "topic", "language", "price"
        ], {
            "price": lambda x: float(x) >= 0
        }),

        ("Mẫu 4: category, num_lectures, content_length_min, avg_rating", [
            "category", "num_lectures", "content_length_min", "avg_rating"
        ], {
            "num_lectures": lambda x: int(x) > 0,
            "content_length_min": lambda x: float(x) > 0,
            "avg_rating": lambda x: 0 <= float(x) <= 5
        }),

        ("Mẫu 5: price, subcategory, content_length_min", [
            "price", "subcategory", "content_length_min"
        ], {"price": lambda x: float(x) >= 0,
            "content_length_min": lambda x: float(x) > 0
        }),

        ("Mẫu 6: price, num_subscribers, avg_rating, category", [
            "price", "num_subscribers", "avg_rating", "category"
        ], {
            "price": lambda x: float(x) >= 0,
            "num_subscribers": lambda x: int(x) >= 0,
            "avg_rating": lambda x: 0 <= float(x) <= 5
        })
    ]

    btn_frame = tk.Frame(window, bg="#d0edf5")
    btn_frame.pack()

    for i, (title_text, fields, rules) in enumerate(input_options):
        btn = tk.Button(
            btn_frame, text=title_text, font=("Arial", 10), width=30, height=4, wraplength=170,
            command=lambda t=title_text, f=fields, r=rules, idx=i+1: create_form_window(window, t, f, r, idx)
        )
        btn.grid(row=i//2, column=i%2, padx=10, pady=10)

# Cửa sổ chính khởi chạy chương trình
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Main Window")
    root.geometry("300x200")

    open_btn = tk.Button(root, text="Phân tích dự đoán", command=lambda: open_dudoan_window(root))
    open_btn.pack(pady=50)

    root.mainloop()