# Vehicle-classification-System
Vehicle-classification System
这是一个利用百EasyDL开发平台接口的程序，需要联网才能使用。

1、本课题的研究目的、内容：
  为了解决问题,满足日益增长的服务和效率需求,人工智能技术随之产生。智能车辆分类系统的目的是，为了实现基础识别系统，为了让人们通过此系统，上传照片，便能告诉人们结果是属于什么车辆，这是人工智能的基础部分。此系统的功能包括上传照片，通过用户上传一张车辆照片，实现识别属于什么车辆的分类。此系统有两个页面，首页面为上传路径的页面，结果页面为上传路径后，通过API调用，识别上传的照片并输出结果为车辆的概率。
  
 2、数据集收集及预处理：
  通过八爪鱼采集器，百度图片模块进行数据集的收集。此集合有轿车，摩托车，大卡车的图片，每一类照片压缩成一个压缩包，再通过压缩包上传到EasyDL平台创建模型。在创建模型的过程中进行数据集分类，为同一类车辆进行标签，在添加标签过程中，删除部分广告图片，或者不相关的图片从而提升精确率。
  
 3、系统概要设计：
  此系统设计包含两个页面，首页面有车辆识别系统标题和上传图片的按钮，通过上传图片函数，返回图片所在的路径，直接API调用，弹出第二个识别结果页面，此页面包含此路径的图片显示，结果通过tkinter的place函数放置合适位置，把最有可能的结果放在图片上方，极小可能的结果放在图片下方，再加上一个可以再次识别图片的按钮，此按钮的作用是再次调用上传图片的函数返回路径给API调用，再次弹出识别结果页面。

 4、程序详细设计：
  首页面的设计如下：通过tkinter库函数实现首页面。
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

主要关键的upload_path函数通过tkinter库中的filedialog.askopenfilename函数返回路径赋值给path参数，再通过API(path)直接调用API函数。
path = tk.filedialog.askopenfilename()
		API(path)

API函数设计如下：
修改client_id和client_secret参数的值，这两个值在百度智能云中的公有云部署应用列表可查看。再修改接口地址，此接口地址在EasyDL平台中我的模型的服务详细可查找。
client_id = 'roEeuDIxp7GDlAoOldj8qsPh'
	client_secret = 'wES5P1CdhWAZ5SGMLtddMbiVP4BVwzML'
request_url= 	"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/classification/LukaJamol"

通过access_token调用，输出所上传图片的结果概率。
request_url = request_url + "?access_token=" + access_token
	response = session.post(request_url, headers=headers, json=params)
	content = response.content.decode('UTF-8')
	for key, value in json.loads(content).items():
    	output = value

输出的结果由三个部分，数据集标签名称和对应的概率。所以要通过for循环三次分别	将数据集名称和概率通过append函数添加到字符串car_name和odds中，再通过调用	identification(path)跳转去识别结果的页面。
		for i in range(3):
    		car_name.append(output[i].get('name'))
    		odds.append(output[i].get('score'))
		identification(path)


Identification函数页面设计如下：
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
	lb1.place(x=30, y=30, width=50, height=50)
	output1 = Label(window, text=odds[0], width=40, height=3)
	output1.place(x=70, y=30)

	lb2 = Label(window, text=car_name[1], width=20, height=5)
	lb2.place(x=30, y=400, width=50, height=50)
	output2 = Label(window, text=odds[1], width=40, height=3)
	output2.place(x=70, y=400)

	lb3 = Label(window, text=car_name[2], width=20, height=5)
	lb3.place(x=30, y=500, width=50, height=50)
	output3 = Label(window, text=odds[2], width=40, height=3)
	output3.place(x=70, y=500)

再次上传图片的按钮设计如下：再次API调用需要先把上一次的结果清空，也就是car_name.clear()和odds.clear()，这样更方便于结果不会重复出现。
Button(window, text="再次", command=lambda: [window.destroy(), upload_path()], 	width=5, height=2).pack(side="bottom")
	car_name.clear()
	odds.clear()
	window.mainloop()  # 循环窗口保持更新
