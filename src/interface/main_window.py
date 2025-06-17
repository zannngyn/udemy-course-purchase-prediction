import tkinter as tk
# from src.interface.screen_mota import open_mota_window
# from src.interface.screen_dudoan import open_dudoan_window
import notebooks.eda as ne

def main_window():
    ne.resolve_csv_path()
    root = tk.Tk()
    root.title("Phân tích xu hướng")
    root.geometry("500x550")
    root.configure(bg="#d7ede5")

    # Tiêu đề
    title = tk.Label(root, text="Phân tích xu hướng lựa chọn mua khoá học trên Udemy",
                     fg="red", bg="#d7ede5", font=("Arial", 12, "bold"))
    title.pack(pady=(20, 0))

    subtitle = tk.Label(root, text="Tác giả: Nhóm 9 - Lớp Phân tích dữ liệu lớn - 20242IT6077001",
                        fg="red", bg="#d7ede5", font=("Arial", 10))
    subtitle.pack(pady=(5, 30))

    # Nút
    btn1 = tk.Button(root, text="Phân tích mô tả", font=("Arial", 14, "bold"),
                     bg="#c9c1c1", width=20, height=3)
    btn1.pack(pady=20)

    btn2 = tk.Button(root, text="Phân tích dự đoán", font=("Arial", 14, "bold"),
                     bg="#c9c1c1", width=20, height=3)
    btn2.pack()

    root.mainloop()