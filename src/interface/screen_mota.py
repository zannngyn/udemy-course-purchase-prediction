import tkinter as tk
import notebooks.eda as ne

def open_mota_window(parent):
    df = ne.pre_eda()
    window = tk.Toplevel(parent)
    window.title("Phân tích mô tả")
    window.geometry("800x650")
    window.configure(bg="#e5ecbd")

    title = tk.Label(window, text="Phân tích mô tả", fg="red", bg="#e5ecbd", font=("Arial", 14, "bold"))
    title.pack(pady=(20, 10))

    btn_frame = tk.Frame(window, bg="#e5ecbd")
    btn_frame.pack()

    btn1 = tk.Button(btn_frame, text="Tạo báo cáo cơ bản về phân tích các cột số", font=("Arial", 12),
                     width=20, height=4, wraplength=150, command=lambda: ne.describe_numeric_columns(df))
    btn1.grid(row=0, column=0, padx=10)

    btn2 = tk.Button(btn_frame, text="Tạo báo cáo nâng cao về các cột dữ liệu số", font=("Arial", 12),
                     width=20, height=4, wraplength=150, command=lambda: ne.describe_extended(df))
    btn2.grid(row=0, column=1, padx=10)

    # Câu hỏi hỗ trợ
    label = tk.Label(window, text="Các câu hỏi cho dữ liệu hỗ trợ phân tích",
                     bg="#e5ecbd", font=("Arial", 13))
    label.pack(pady=(30, 10))

    questions = [
        ("Liệu mức giá cao/thấp ảnh hưởng đến quyết định mua", lambda: ne.price_effect_on_result(df)),
        ("Khoá học có nhiều người đăng ký thì có tỷ lệ mua cao hơn không?",
         lambda: ne.num_subscribers_effect_on_result(df)),
        ("Rating ảnh hưởng đến tỷ lệ mua khoá học như thế nào?", lambda: ne.avg_rating_effect_on_result(df)),
        ("Độ dài khoá học ảnh hưởng đến tỷ lệ mua khoá học như thế nào?",
         lambda: ne.content_length_min_effect_on_result(df)),
        ("Có phải review càng nhiều thì rating càng cao?", lambda: ne.num_reviews_effect_on_avg_rating(df)),
        ("Phân tích ảnh hưởng của số lượng review đến quyết định mua",
         lambda: ne.num_reviews_effect_on_result(df)),
        ("Mối tương quan nào giữa giá của khoá học và số lượng bài giảng",
         lambda: ne.price_effect_on_num_lectures(df)),
    ]

    q_frame = tk.Frame(window, bg="#e5ecbd")
    q_frame.pack()

    for i, (text, func) in enumerate(questions):
        btn = tk.Button(
            q_frame,
            text=text,
            font=("Arial", 10),
            width=20,
            height=3,
            wraplength=150,
            command=func  # gán hàm cho nút
        )
        btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
