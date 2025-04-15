import random
import socket
import sqlite3
import tkinter as tk
from tkinter import messagebox

# ────── DB設定 ────── #
server_path = r"./fools_day.db"
db_table = "fools_day"


# 取得使用者 IP
def get_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "unknown"


user_ip = get_ip()
click_count = 0  # 滑鼠點擊次數

# ────── GUI 設定 ────── #
root = tk.Tk()
root.title("工程整合介面")
root.geometry("400x300")

canvas = tk.Canvas(root, width=400, height=200, bg="white")
canvas.pack()

ribbons = ["🎀", "🎊", "🎉", "✨", "💫", "🌟"]
fail_count = 0
is_running_away = False


def throw_ribbons(message=""):
    canvas.delete("all")
    canvas.create_text(200, 50, text="🤡", font=("Arial", 40))
    for _ in range(10):
        x = random.randint(50, 350)
        y = random.randint(100, 250)
        ribbon = random.choice(ribbons)
        canvas.create_text(x, y, text=ribbon, font=("Arial", 20), fill="red")
    if message:
        canvas.create_text(
            200, 100, text=message, font=("Arial", 16, "bold"), fill="blue"
        )


def show_jiong():
    canvas.delete("all")
    canvas.create_text(200, 100, text="囧", font=("Arial", 60), fill="gray")


def move_button_randomly():
    if is_running_away:
        new_x = random.randint(50, 300)
        new_y = random.randint(200, 270)
        btn.place(x=new_x, y=new_y)
        root.after(500, move_button_randomly)


def check_password():
    global fail_count, is_running_away
    pw = entry.get()
    if pw == "20250401":
        throw_ribbons("你還真的按~ Happy April Fool's Day")
        btn.place_forget()
        btn.pack()
        fail_count = 0
        is_running_away = False
    else:
        fail_count += 1
        if fail_count == 1:
            show_jiong()
        elif fail_count == 2:
            throw_ribbons("what day is today? (YYYYMMDD)")
        else:
            throw_ribbons()
        if fail_count >= 2:
            is_running_away = True
            btn.pack_forget()
            move_button_randomly()
        else:
            messagebox.showerror("錯誤", f"帳號錯誤（第 {fail_count} 次）")


# ────── 滑鼠點擊偵測 ────── #
def record_click(event):
    global click_count
    click_count += 1


root.bind("<Button>", record_click)  # 綁定所有滑鼠點擊事件


# ────── 關閉時寫入資料庫 ────── #
def on_closing():
    try:
        conn = sqlite3.connect(server_path)
        cursor = conn.cursor()

        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {db_table} (
                ip TEXT PRIMARY KEY,
                times INTEGER
            )
        """
        )

        cursor.execute(
            f"""
            INSERT INTO {db_table} (ip, times)
            VALUES (?, ?)
            ON CONFLICT(ip) DO UPDATE SET times = times + ?
        """,
            (user_ip, click_count, click_count),
        )

        conn.commit()
        conn.close()
        print(f"[LOG] IP {user_ip} 點擊紀錄已更新（+{click_count}）")
    except Exception as e:
        print(f"[ERROR] 回傳資料失敗：{e}")
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)

# ────── 元件區域 ────── #
label = tk.Label(root, text="使用者(公司登入帳號)：")
label.pack()

entry = tk.Entry(root, show="*")
entry.pack()

btn = tk.Button(root, text="確認", command=check_password)
btn.pack()

# ────── 執行 ────── #
root.mainloop()
# yoga到此一遊