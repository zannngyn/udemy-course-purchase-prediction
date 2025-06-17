import tkinter as tk
from tkinter import messagebox
from src.models.create_models import train_all_models


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

def create_form_window(parent, title_text, fields, validation_rules):
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

    def on_submit():
        if validate_entries(entries, validation_rules):
            messagebox.showinfo("Thành công", "Dữ liệu hợp lệ và đã được gửi!")
            form.destroy()

    submit_btn = tk.Button(form, text="Gửi", command=on_submit)
    submit_btn.pack(pady=20)

def open_dudoan_window(parent):
    train_all_models()
    window = tk.Toplevel(parent)
    window.title("Phân tích dự đoán")
    window.geometry("700x600")
    window.configure(bg="#d0edf5")

    title = tk.Label(window, text="Phân tích dự đoán dựa trên dữ liệu nhập vào", fg="red",
                     bg="#d0edf5", font=("Arial", 14, "bold"))
    title.pack(pady=(20, 5))

    subtitle = tk.Label(window, text="Các mẫu đã huấn luyện sẵn (dưới đây là các đầu vào)",
                        fg="darkred", bg="#d0edf5", font=("Arial", 11))
    subtitle.pack(pady=(0, 20))

    input_options = [
        ("Mẫu 1: Danh mục, Giá, Tổng số bài giảng, Điểm dánh giá TB", [
            "Danh mục khoá học", "Giá", "Tổng số bài giảng", "Điểm đánh giá TB của khoá"
        ], {
            "Giá": lambda x: float(x) >= 0,
            "Tổng số bài giảng": lambda x: int(x) > 0,
            "Điểm đánh giá TB của khoá": lambda x: 0 <= float(x) <= 5
        }),

        ("Mẫu 2: Danh mục, Số người đăng ký, Số người đánh giá, Số bình luận, Điểm đánh giá trung bình", [
            "Danh mục khoá học", "Số người đăng ký", "Số người đánh giá", "Tổng số bình luận", "Điểm đánh giá trung bình"
        ], {
            "Số người đăng ký": lambda x: int(x) >= 0,
            "Số người đánh giá": lambda x: int(x) >= 0,
            "Tổng số bình luận": lambda x: int(x) >= 0,
            "Điểm đánh giá trung bình": lambda x: 0 <= float(x) <= 5
        }),

        ("Mẫu 3: Danh mục, chủ đề, ngôn ngữ sở dụng, giá", [
            "Danh mục khoá học", "Chủ đề khoá học", "Ngôn ngữ sử dụng", "Giá bán"
        ], {
            "Giá bán": lambda x: float(x) >= 0
        }),

        ("Mẫu 4: Danh mục, chủ đề nhỏ, ngôn ngữ, giá bán", [
            "Danh mục khoá học", "Chủ đề nhỏ của khoá học", "Ngôn ngữ sử dụng", "Giá bán"
        ], {
            "Giá bán": lambda x: float(x) >= 0
        }),

        ("Mẫu 5", [
            "Phân loại khoá học", "Tổng số bài giảng", "Thời lượng khoá học", "Số người đăng ký", "Số người đánh giá", "Số bình luận"
        ], {
            "Tổng số bài giảng": lambda x: int(x) > 0,
            "Thời lượng khoá học": lambda x: float(x) > 0,
            "Số người đăng ký": lambda x: int(x) >= 0,
            "Số người đánh giá": lambda x: int(x) >= 0,
            "Số bình luận": lambda x: int(x) >= 0
        }),

        ("Tự chọn dữ liệu", [
            "Tập dữ liệu bạn chọn (đường dẫn)"
        ], {
        }),
    ]

    btn_frame = tk.Frame(window, bg="#d0edf5")
    btn_frame.pack()

    for i, (title_text, fields, rules) in enumerate(input_options):
        btn = tk.Button(
            btn_frame, text=title_text, font=("Arial", 10), width=30, height=4, wraplength=170,
            command=lambda t=title_text, f=fields, r=rules: create_form_window(window, t, f, r)
        )
        btn.grid(row=i//2, column=i%2, padx=10, pady=10)

# Để chạy thử
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Main Window")
    root.geometry("300x200")

    open_btn = tk.Button(root, text="Phân tích dự đoán", command=lambda: open_dudoan_window(root))
    open_btn.pack(pady=50)

    root.mainloop()
