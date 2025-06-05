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