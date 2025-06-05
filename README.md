# Dự đoán mua khóa học Udemy

Dự án sử dụng mô hình hồi quy logistic để dự đoán xem một người dùng có mua khóa học trên Udemy hay không, dựa trên thông tin về khóa học.

---

## 📁 Cấu trúc thư mục

- `data/`: Chứa dữ liệu thô và dữ liệu đã xử lý
- `notebooks/`: Các file Jupyter Notebook phân tích dữ liệu, thử mô hình
- `src/`: Mã nguồn Python được tổ chức theo module
  - `src/data`: Load và xử lý dữ liệu
  - `src/features`: Tạo và chọn đặc trưng
  - `src/models`: Huấn luyện, dự đoán, đánh giá
  - `src/utils`: Hàm tiện ích dùng chung
- `models/`: Mô hình đã huấn luyện (.pkl)
- `reports/`: Biểu đồ, hình ảnh và báo cáo
- `requirements.txt`: Danh sách thư viện cần cài đặt
- `.gitignore`: Loại bỏ file không cần thiết
- `README.md`: Giới thiệu và hướng dẫn dự án

---

## 📦 Công nghệ sử dụng

| Thành phần | Công nghệ |
|------------|-----------|
| **Ngôn ngữ lập trình** | Python 3.9+ |
| **Phân tích dữ liệu & mô hình** | Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn |
| **Giao diện người dùng (UI)** | Tkinter |
| **Lưu mô hình** | `joblib` hoặc `pickle` |
| **Môi trường phát triển** | Jupyter Notebook (EDA & mô hình), PyCharm (Tkinter & module) |
| **Quản lý thư viện** | `requirements.txt` |
| **Hệ điều hành** | Đa nền tảng (macOS, Windows, Linux) |

---

## 📋 Kế hoạch công việc & hướng dẫn cộng tác

### Công cụ làm việc
- **Code phân tích dữ liệu**: Jupyter Notebook (`/notebooks`)
- **Code giao diện & pipeline dự đoán**: Viết trong Pycharm (`/src`)

### Nhiệm vụ chính

| Nhiệm vụ | Mô tả |
|----------|------|
| Tiền xử lý | Chuẩn hóa dữ liệu cho huấn luyện. Dữ liệu gốc để phân tích mô tả |
| Gán nhãn | Dựa trên `is_paid`, `price`, `avg_rating`, `category` |
| Phân tích mô tả | Vẽ biểu đồ, phân tích mối liên hệ giữa các biến, xuất dữ liệu ra Excel |
| Huấn luyện | Dùng hồi quy logistic, tuning `threshold`, `learning_rate` |
| Dự đoán | Giao diện nhập liệu hoặc batch (all), dùng model để dự đoán |
| Giao diện | Form nhập đầu vào (Tkinter) và kết nối mô hình |
| Dự đoán theo tiêu chí | Cho phép chọn `rating`, `time`, `latest_update` để lọc dự đoán |

---

## ✅ Hướng dẫn cài đặt

```bash
git clone https://github.com/ten-cua-ban/udemy-course-purchase-prediction.git
cd udemy-course-purchase-prediction
pip install -r requirements.txt
```

## 📋 Phân công công việc & Hướng dẫn đóng góp

Dự án tuân theo quy trình phân nhánh **Git Flow** đơn giản. Mọi thay đổi đều được phát triển trên các **nhánh `feature`**, sau đó được hợp nhất vào nhánh `dev` thông qua **Pull Request**.

> Để xem hướng dẫn chi tiết về quy trình làm việc với Git, vui lòng đọc file **[GIT_WORKFLOW.md](./git_workflow.md)**.

Dưới đây là mô tả chi tiết công việc cho từng nhánh chức năng:

---

### nhánh `feature/data-cleaning`
* **Mục tiêu:** Chuẩn bị dữ liệu sạch để phân tích và huấn luyện.
* **Công việc cụ thể:**
    * Viết code trong `src/data/load_data.py` để đọc file `Course_info.csv`.
    * Xử lý các giá trị bị thiếu (missing values).
    * **Gán nhãn (label):** Dựa vào các cột như `is_paid`, `price`, `avg_rating`, `num_subscribers` để tạo ra cột mục tiêu `will_purchase` (1 là mua, 0 là không mua).
    * Lưu DataFrame đã làm sạch vào thư mục `data/processed/`.

---

### nhánh `feature/eda`
* **Mục tiêu:** Khám phá và tìm hiểu sâu hơn về dữ liệu.
* **Công việc cụ thể:**
    * Làm việc chính trong file `notebooks/eda.ipynb`.
    * Tính toán các thống kê mô tả (giá trung bình, số lượng bài giảng, v.v.).
    * **Vẽ biểu đồ:** Dùng Matplotlib/Seaborn để vẽ biểu đồ phân phối, biểu đồ tương quan để tìm ra các yếu tố ảnh hưởng đến quyết định mua hàng.
    * Lưu các biểu đồ quan trọng vào thư mục `reports/figures/`.

---

### nhánh `feature/model-training`
* **Mục tiêu:** Xây dựng, huấn luyện và đánh giá mô hình dự đoán.
* **Công việc cụ thể:**
    * **Tạo đặc trưng:** Viết code trong `src/features/build_features.py` để chuẩn hóa (scale) các cột số và mã hóa (encode) các cột chữ.
    * **Huấn luyện:** Viết code trong `src/models/train_model.py` để huấn luyện mô hình Hồi quy Logistic.
    * **Đánh giá:** Viết code trong `src/models/evaluate_model.py` để tính các chỉ số như Accuracy, F1-score và vẽ ma trận nhầm lẫn (Confusion Matrix).
    * Lưu mô hình đã huấn luyện vào thư mục `models/` (ví dụ: `logistic_model.pkl`).

---

### nhánh `feature/ui-form`
* **Mục tiêu:** Tạo giao diện người dùng để tương tác với mô hình.
* **Công việc cụ thể:**
    * Sử dụng **Tkinter** để thiết kế giao diện (form) cho phép người dùng nhập thông tin của một khóa học.
    * Viết logic cho nút "Dự đoán": Lấy dữ liệu người dùng nhập, xử lý nó, tải mô hình từ file `.pkl` và hiển thị kết quả dự đoán ra màn hình.
    * Tạo một file riêng ở thư mục gốc, ví dụ: `app_ui.py`.

---

### nhánh `feature/utils`
* **Mục tiêu:** Viết các hàm có thể tái sử dụng cho toàn bộ dự án.
* **Công việc cụ thể:**
    * Tạo file `src/utils/helpers.py`.
    * Viết các hàm tiện ích chung, ví dụ: một hàm để lưu biểu đồ, một hàm để tải cấu hình, hoặc thiết lập logging.

---
