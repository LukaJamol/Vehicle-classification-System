from tkinter import *
import tkinter as tk
from PIL import ImageTk
from PIL import Image
import time
import json
import base64
import requests
from datetime import datetime
from tkinter import filedialog

output = ''
car_name = []
odds = []
filename = []
path = ''

# 首页面
def window_menu():
    window = tk.Tk()  # 初始化首页面
    window.title("智能实践项目")  # 窗体名字
    window.geometry("400x400")  # 窗体大小
    window.config(background="#00BFFF")
    # 显示文本
    tk.Label(window, text="车辆识别系统", font="宋体", width=20, height=3).pack()
    # 按钮实现引入照片以及转入识别页面
    button1 = Button(window, text="上传图片", width=15, height=3, command=upload_path)
    button1.pack(side="bottom")
    # 显示图片
    img_open = Image.open(r"C:\Users\18508\Pictures\Audi.jpg").resize((350, 250))
    img_jpg = ImageTk.PhotoImage(img_open)
    label_img = tk.Label(window, image=img_jpg)
    label_img.place(x=50, y=100, width=300, height=225)
    window.mainloop()  # 循环窗口保持更新

# 打开文件
def upload_path():
    # 从本地选择一个文件，并返回文件的目录路径
    path = tk.filedialog.askopenfilename()
    API(path)

# API调用
def API(path):
    print(datetime.now())
    # 分别使用网址 以及立即使用 API Key 和Secret Key
    start = time.time()
    appid = 'appid'
    client_id = 'roEeuDIxp7GDlAoOldj8qsPh'
    client_secret = 'wES5P1CdhWAZ5SGMLtddMbiVP4BVwzML'
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials'
    host += "&client_id=%s&client_secret=%s" % (client_id, client_secret)
    session = requests.Session()
    response = session.get(host)
    access_token = response.json().get("access_token")
    request_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/classification/LukaJamol"
    with open(path, 'rb') as f:
        image = base64.b64encode(f.read()).decode('UTF8')
    headers = {
        'Content-Type': 'application/json'
    }

    params = {
        "image": image
    }

    request_url = request_url + "?access_token=" + access_token
    response = session.post(request_url, headers=headers, json=params)
    content = response.content.decode('UTF-8')
    for key, value in json.loads(content).items():
        output = value
    for i in range(3):
        car_name.append(output[i].get('name'))
        odds.append(output[i].get('score'))
    identification(path)

# 识别页面
def identification(path):
    window = Toplevel()
    window.title("智能实践项目")  # 窗体名字
    window.geometry("400x600")  # 窗体大小
    # 显示引用图片
    # label 中设置图片
    img_open = Image.open(path).resize((400, 200))
    photo = ImageTk.PhotoImage(img_open)
    img_label = tk.Label(window, image=photo)
    img_label.place(x=20, y=100, width=350, height=250)

    # 文本框，用于输出分析的数据
    lb1 = Label(window, text=car_name[0], width=20, height=5)
    lb1.place(x=30, y=30, width=35, height=50)
    output1 = Label(window, text=odds[0], width=35, height=2)
    output1.place(x=60, y=30)

    lb2 = Label(window, text=car_name[1], width=20, height=5)
    lb2.place(x=30, y=400, width=35, height=50)
    output2 = Label(window, text=odds[1], width=35, height=2)
    output2.place(x=60, y=400)

    lb3 = Label(window, text=car_name[2], width=20, height=5)
    lb3.place(x=30, y=500, width=35, height=50)
    output3 = Label(window, text=odds[2], width=35, height=2)
    output3.place(x=60, y=500)

    Button(window, text="再次", command=lambda: [window.destroy(), upload_path()], width=5, height=2).pack(side="bottom")
    car_name.clear()
    odds.clear()
    window.mainloop()  # 循环窗口保持更新


if __name__ == '__main__':
    window_menu()
