import tkinter as tk

#////////////////////////////////////////////////////////////////////
#//                          _ooOoo_                               //
#//                         o8888888o                              //
#//                         88" . "88                              //
#//                         (| ^_^ |)                              //
#//                         O\  =  /O                              //
#//                      ____/`---'\____                           //
#//                    .'  \\|     |//  `.                         //
#//                   /  \\|||  :  |||//  \                        //
#//                  /  _||||| -:- |||||-  \                       //
#//                  |   | \\\  -  /// |   |                       //
#//                  | \_|  ''\---/''  |   |                       //
#//                  \  .-\__  `-`  ___/-. /                       //
#//                ___`. .'  /--.--\  `. . ___                     //
#//              ."" '<  `.___\_<|>_/___.'  >'"".                  //
#//            | | :  `- \`.;`\ _ /`;.`/ - ` : | |                 //
#//            \  \ `-.   \_ __\ /__ _/   .-` /  /                 //
#//      ========`-.____`-.___\_____/___.-`____.-'========         //
#//                           `=---='                              //
#//      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^        //
#//         佛祖保佑       永无BUG     永不修改                     //
#////////////////////////////////////////////////////////////////////

# 自定义图形库
class Graphics:
    def __init__(self, canvas):
        self.canvas = canvas  # 画布对象，用于绘制图形
        self.color = "black"  # 默认绘制颜色为黑色

    # 设置绘制颜色
    def set_color(self, color):
        self.color = color

    # 绘制一个点
    def draw_point(self, x, y):
        # 创建一个长度为1的线条来模拟点
        self.canvas.create_line(x, y, x + 1, y, fill=self.color)

    # 绘制一条直线
    def draw_line(self, x1, y1, x2, y2):
        self.canvas.create_line(x1, y1, x2, y2, fill=self.color)

    # 绘制一个矩形
    def draw_rect(self, x, y, width, height):
        self.canvas.create_rectangle(x, y, x + width, y + height, outline=self.color)

    # 绘制一个圆形
    def draw_circle(self, x, y, radius):
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, outline=self.color)

# 窗口管理器，支持多窗口
class WindowManager:
    def __init__(self, icon_path=None):
        self.windows = {}  # 存储所有窗口的信息
        self.current_window = None  # 当前活动窗口的名称
        self.icon_path = icon_path  # 用于存储自定义图标的路径

    # 创建一个新窗口
    def create_window(self, name):
        root = tk.Tk()  # 创建一个新的Tk窗口
        root.title(name)  # 设置窗口标题
        
        # 如果提供了图标路径，则设置窗口图标
        if self.icon_path:  
            icon = tk.PhotoImage(file=self.icon_path)
            root.iconphoto(False, icon)

        # 创建一个画布并设置为白色背景
        canvas = tk.Canvas(root, width=800, height=600, bg="white")
        canvas.pack()  # 将画布添加到窗口中
        
        # 创建一个Graphics对象，用于在该画布上绘制图形
        graphics = Graphics(canvas)
        
        # 将窗口对象及其关联的图形对象存储到windows字典中
        self.windows[name] = {"root": root, "graphics": graphics}
        self.current_window = name  # 设置当前活动窗口

    # 获取当前活动窗口的绘图对象
    def get_graphics(self):
        if self.current_window is None:
            raise ValueError("当前没有活动的窗口。")  # 抛出错误，如果没有创建任何窗口
        return self.windows[self.current_window]["graphics"]

    # 显示所有窗口
    def show_windows(self):
        for window_data in self.windows.values():
            window_data["root"].mainloop()  # 进入Tk的主事件循环，显示窗口
