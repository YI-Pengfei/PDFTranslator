# -*- coding: utf-8 -*-
"""
Tkinter教程 https://www.jianshu.com/p/91844c5bca78
百度翻译api: http://api.fanyi.baidu.com/doc/21
在Linux上pip install pyscreenshot，然后把from PIL import imagegrab改成import pyscreenshot as ImageGrab，其他无需改动

PyInstaller封装命令：
    pyinstaller --icon="baidufanyi.ico" -F Translator-Tkinter.py -w
"""
import os
import tkinter
import tkinter.filedialog
from tkinter import ttk
import time
import requests
import random
import hashlib 
import base64
from PIL import ImageGrab
#import pyscreenshot as ImageGrab

fromLang='auto' # 源语言
toLang='zh' # 目标语言

# 1. 第一部分 百度翻译API做文本翻译 
def BaiduTranslator(text,fromLang='auto',toLang='zh'):
    request_url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
    appid="20200405000412790" #申请的账号
    secretKey = 'hjlwBKKmIiKczeM8A5Aq'#账号密码
    salt = random.randint(32768, 65536)
    sign = appid + text + str(salt) + secretKey
    md = hashlib.md5()
    md.update(sign.encode(encoding='utf-8'))
    sign = md.hexdigest()
    params = {'appid':appid, 
              'from':fromLang,
              'to':toLang,
              'salt':salt,
              'q':text,
              'sign':sign}
    headers = {'Referer':'https://fanyi-api.baidu.com/',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36X-Requested-With: XMLHttpRequest' }
    response = requests.post(request_url, data=params, headers=headers) # post请求 
    if response:
        return response.json()['trans_result']
    return "error"



# 2. GUI
def translate_TK(content=''):
    """ 文本翻译 (给button的方法)
    """
    output1_TEXT.delete(0.0,tkinter.END) # 清空文本框中的内容
    output2_TEXT.delete(0.0,tkinter.END) 
    if not content: # 没有直接传进 待翻译的内容，则从文本框1中读取
        content = input1_TEXT.get(0.0,tkinter.END) # 接收输入的文本 0.0表示从第0行第0列开始读取 End表示最后一个字符
    else: # 有直接传进来的内容（是OCR的结果）
        input1_TEXT.delete(0.0,tkinter.END) 
        input1_TEXT.insert(0.0,content) # 显示OCR识别的原始结果
    content = content.replace('\n',' ').strip()
    Results = BaiduTranslator(content, fromLang, toLang)
    output1_TEXT.insert(0.0,content) # 原文
    output2_TEXT.insert(0.0,Results[0]['dst']) # 译文



# 2. 第二部分 自由截屏  
class FreeCapture():
    """ 用来显示全屏幕截图并响应二次截图的窗口类
    """
    def __init__(self, img):
        #变量X和Y用来记录鼠标左键按下的位置
        self.X = tkinter.IntVar(value=0)
        self.Y = tkinter.IntVar(value=0)
        #屏幕尺寸
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()
        #创建顶级组件容器
        self.top = tkinter.Toplevel(root, width=screenWidth, height=screenHeight)
        #不显示最大化、最小化按钮
        self.top.overrideredirect(True)
        self.canvas = tkinter.Canvas(self.top,bg='white', width=screenWidth, height=screenHeight)
        #显示全屏截图，在全屏截图上进行区域截图 
        self.image = tkinter.PhotoImage(file=img)
        self.canvas.create_image(screenWidth//2, screenHeight//2, image=self.image)
        
        self.lastDraw = None
        #鼠标左键按下的位置
        def onLeftButtonDown(event):
            self.X.set(event.x)
            self.Y.set(event.y)
            #开始截图
            self.sel = True

        self.canvas.bind('<Button-1>', onLeftButtonDown)
        
        def onLeftButtonMove(event):
            #鼠标左键移动，显示选取的区域
            if not self.sel:
                return
            try: #删除刚画完的图形，要不然鼠标移动的时候是黑乎乎的一片矩形
                self.canvas.delete(self.lastDraw)
            except Exception as e:
                pass
            self.lastDraw = self.canvas.create_rectangle(self.X.get(), self.Y.get(), event.x, event.y, outline='green')

        def onLeftButtonUp(event):
            #获取鼠标左键抬起的位置，保存区域截图
            self.sel = False
            try:
                self.canvas.delete(self.lastDraw)
            except Exception as e:
                pass

            time.sleep(0.5)
            #考虑鼠标左键从右下方按下而从左上方抬起的截图
            left, right = sorted([self.X.get(), event.x])
            top, bottom = sorted([self.Y.get(), event.y])
            pic = ImageGrab.grab((left+1, top+1, right, bottom))
#            #弹出保存截图对话框
#            fileName = tkinter.filedialog.asksaveasfilename(title='保存截图', filetypes=[('image', '*.jpg *.png')])
            fileName = 'temp2.png'
            if fileName:
                pic.save(fileName)
            #关闭当前窗口
            self.top.destroy()

        self.canvas.bind('<B1-Motion>', onLeftButtonMove) # 按下左键
        self.canvas.bind('<ButtonRelease-1>', onLeftButtonUp) # 抬起左键
        #让canvas充满窗口，并随窗口自动适应大小
        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES) #


def screenShot_TK():
    """ 自由截屏的函数 (button按钮的事件)
    """
#    print("test")
    root.state('icon')  # 最小化主窗体
    time.sleep(0.5)
    im = ImageGrab.grab()
    # 暂存全屏截图
    im.save('temp.png')
    im.close()
    # 进行自由截屏 
    w = FreeCapture('temp.png')
    screenShot_BUTTON.wait_window(w.top)
    # 截图结束，恢复主窗口，并删除temp.png文件
    root.state('normal')
    os.remove('temp.png')
    ## 完成自由截屏，OCR识别截屏内容
    content = OCR()
    translate_TK(content=content)


# 3. 第三部分 OCR文字识别
def OCR(pic='temp2.png'):
    TOKEN = ""  # 签名
    EXPIRES = -1  # 签名过期时间
    def get_token():
        """获取Access Token (网址: https://ai.baidu.com/ai-doc/REFERENCE/Ck3dwjgn3)
        """
        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        AK = 'cNhWvLGqpSZzpAMNTU3ibfYx'
        SK = 'GxylATKF5OlV5YyuV749oREFMqpQD71D'
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(AK,SK)
        response = requests.get(host)
        if response:
            token = response.json()['access_token']
            expires = response.json()['expires_in']
            return token, expires
    
    if not (TOKEN and EXPIRES>24*3*3600):  # 有效期在三天以上
        TOKEN, EXPIRES = get_token()

    # 二进制方式打开图片文件
    f = open(pic, 'rb') #
    img = base64.b64encode(f.read())
    f.close()
    os.remove(pic) # 删除缓存文件
    # 通用文字识别 （调用量限制 50000次/天免费）
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    params = {"image":img,
              'access_token':TOKEN}
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers) # post请求 
    content = ""
    if response:
        for item in response.json()['words_result']:
            content+= item["words"]+ "\n"
            
    return content


def clear_TEXT_TK():
    """ 清空文本框
    """
    input1_TEXT.delete(0.0, tkinter.END)  # 清空输入
    output1_TEXT.delete(0.0,tkinter.END) # 清空文本框中的内容
    output2_TEXT.delete(0.0,tkinter.END) 



""" 初始化一个根窗体实例 """
root = tkinter.Tk()
root.geometry('1000x700')
root.title('百度翻译')
# 提示内容--请输入
label1 = tkinter.Label(root, text='请输入您要查询的内容', font=('微软雅黑',16),)
label1.place(relx=0.2, rely=0.05,relwidth=0.6, relheight=0.1)  # , relwidth=0.8, relheight=0.1
# 接收多行文本输入
input1_TEXT = tkinter.Text(root)
input1_TEXT.place(relx=0.1, rely=0.2, relwidth=0.7, relheight=0.2)
# 组合框
def select_Lang(event):
    """选择目标语言"""
    dic = {0:'zh',1:'en',2:'kor',3:'jp'}
    c = dic[comb.current()]
    global toLang  #在函数中为函数外的变量赋值
    toLang = c
   
comb = ttk.Combobox(root,values=['译汉','译英','译韩','译日'])
comb.place(relx=0.05,rely=0.05,relwidth=0.2)
comb.current(0) # 默认为译汉 
comb.bind('<<ComboboxSelected>>', select_Lang)
# ================== 布置查词按钮 ====================================
query_BUTTON = tkinter.Button(root, text='查询', command=translate_TK)
query_BUTTON.place(relx=0.8, rely=0.2, relwidth=0.1, relheight=0.1)
# ================== 布置截屏按钮 ====================================
screenShot_BUTTON = tkinter.Button(root, text='截屏翻译', command=screenShot_TK)
screenShot_BUTTON.place(relx=0.8, rely=0.3, relwidth=0.1, relheight=0.1)


output1_TEXT = tkinter.Text(root)
output1_TEXT.place(relx=0.55, rely=0.5, relwidth=0.4, relheight=0.4)

output2_TEXT = tkinter.Text(root)
output2_TEXT.place(relx=0.05, rely=0.5, relwidth=0.4, relheight=0.4)


## 创建Scrollbar组件，设置该组件与output2_TEXT的纵向滚动关联
#scroll = tkinter.Scrollbar(root, command=output2_TEXT.yview)
#scroll.place()
### 设置output2_TEXT的纵向滚动影响scroll滚动条
#output2_TEXT.configure(yscrollcommand=scroll.set)
#print(toLang)
root.mainloop()