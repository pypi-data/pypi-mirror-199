from tkinter import Tk, Canvas

class Game():

	def __init__(self, title, width, height, useKey=False, useMouse=False, useLoop=0):
		# 窗体设置
		self.root = Tk()
		self.root.title(title)
		self.root.resizable(False, False)
		self.center(width, height)
		# Canvas
		self.canvas = Canvas(self.root)
		self.canvas.place(x=0, y=0, width=width, height=height)
		# 初始化状态
		self.initState()
		# 画第一帧
		self.paint()
		# 绑定事件
		useKey and self.root.bind("<Key>", self.bindKey)
		useMouse and self.root.bind("<Button>", self.bindClick)
		# 开启重画线程
		useLoop != 0 and self.loop(useLoop)
		# 主循环
		self.root.mainloop()

	# 让窗体居中
	def center(self, width, height):
		sw = self.root.winfo_screenwidth()
		sh = self.root.winfo_screenheight()
		x = (sw - width) / 2
		y = (sh - height) / 2
		self.root.geometry("%dx%d+%d+%d" % (width, height, x, y))

	# 重画线程
	def loop(self, interval):
		self.paint()
		self.root.after(interval, lambda: self.loop(interval))

	def initState(self):
		pass

	def paint(self):
		pass

	def bindKey(self, e):
		pass

	def bindClick(self, e):
		pass

class Example(Game):

	def __init__(self):
		print("Keyboard:\tW,S")
		print("Mouse:\t\tLeft")
		super().__init__("标题", 400, 400, useKey=True, useMouse=True, useLoop=300)

	# 初始化状态
	def initState(self):
		self.index = 0
		self.index2 = 0
		self.direction = True

	# 每帧更新状态
	def updateState(self):
		if self.direction:
			if self.index < 3:
				self.index += 1
			else:
				self.index = 0
		else:
			if self.index > 0:
				self.index -= 1
			else:
				self.index = 3

	# 画画
	def paint(self):
		self.updateState()
		pen = self.canvas
		pen.delete("all")
		pen.create_rectangle(0, 0, 400, 400, fill="white", width=0)
		pen.create_rectangle(self.index * 100, self.index2 * 100, self.index * 100 + 100, self.index2 * 100 + 100,
							 fill="red", outline="red")

	# 键盘事件
	def bindKey(self, e):
		if e.keycode == 87 and self.index2 >= 1:
			self.index2 -= 1
		elif e.keycode == 83 and self.index2 <= 2:
			self.index2 += 1

	# 鼠标事件
	def bindClick(self, e):
		if e.num == 1:
			self.direction = not self.direction
