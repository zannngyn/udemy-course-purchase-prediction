# 📘 Hướng dẫn quy trình làm việc với Git

Tài liệu này mô tả quy trình phân nhánh (branching strategy) và các bước làm việc với Git cho dự án "Dự đoán mua khóa học Udemy". Việc tuân thủ quy trình này giúp đảm bảo mã nguồn được quản lý nhất quán, dễ theo dõi và hạn chế xung đột.

---

## 🚩 Các Nhánh Chính

Dự án sử dụng 2 nhánh chính không bao giờ bị xóa:

| Tên nhánh | Mục đích |
|-----------|----------|
| `main`    | Nhánh ổn định nhất, chỉ chứa phiên bản sản phẩm đã được kiểm thử và có thể chạy được. **Nghiêm cấm commit trực tiếp lên `main`**. |
| `dev`     | Nhánh phát triển chính. Tất cả các nhánh chức năng sẽ được hợp nhất (merge) vào `dev`. Đây là nơi chứa các tính năng đã hoàn thành và sẵn sàng cho lần release tiếp theo. |

---

## 🌿 Các Nhánh Chức Năng (Feature Branches)

Khi phát triển một chức năng mới, bạn **PHẢI** tạo một nhánh mới từ `dev`. Tên nhánh nên tuân theo quy ước sau:

`feature/<ten-chuc-nang-ngan-gon>`

**Ví dụ các nhánh chức năng cho dự án:**

| Tên nhánh gợi ý | Công việc tương ứng |
|-------------------------|--------------------------------------------------|
| `feature/data-cleaning` | Làm sạch, gán nhãn và chuẩn hóa dữ liệu. |
| `feature/eda` | Phân tích dữ liệu khám phá (EDA), vẽ biểu đồ. |
| `feature/model-training`| Xây dựng và huấn luyện mô hình hồi quy logistic. |
| `feature/ui-form` | Phát triển giao diện người dùng (UI) bằng Tkinter. |
| `feature/utils` | Viết các hàm tiện ích dùng chung. |
| `feature/reporting` | Tạo báo cáo, lưu kết quả đánh giá mô hình. |

Ngoài ra, nếu cần sửa lỗi gấp, bạn có thể tạo nhánh `bugfix/<ten-loi>`.

---

