# -*- coding: utf-8 -*-
"""
Tkinter教程 https://www.jianshu.com/p/91844c5bca78
百度翻译api: http://api.fanyi.baidu.com/doc/21
"""
import tkinter
import time
from urllib import request, parse
import json
import random
import hashlib 

## 1. 调用百度翻译API进行文本翻译 
class BaiduTranslate:
    def __init__(self,fromLang,toLang):
        self.url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
        self.appid="20200405000412790" #申请的账号
        self.secretKey = 'hjlwBKKmIiKczeM8A5Aq'#账号密码
        self.fromLang = fromLang
        self.toLang = toLang
        self.salt = random.randint(32768, 65536)
        self.head_data = {'Referer':'https://fanyi-api.baidu.com/',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36X-Requested-With: XMLHttpRequest' }

    def BdTrans(self,text):
        sign = self.appid + text + str(self.salt) + self.secretKey
        md = hashlib.md5()
        md.update(sign.encode(encoding='utf-8'))
        sign = md.hexdigest()
        form_data = {'appid':self.appid,
                     'q':text,
                     'from':self.fromLang,
                     'to':self.toLang,
                     'salt':self.salt,
                     'sign':sign
                     }
        data = parse.urlencode(form_data).encode('utf-8')
        req = request.Request(self.url, data, self.head_data)
        response = request.urlopen(req)
        html = response.read().decode('utf-8')
        translate_results = json.loads(html)
        translate_results = translate_results['trans_result']
        
        return translate_results


# 2. GUI
def translate(input1_text,txt,txt2):
    content = input1_text.get(0.0,tkinter.END) # 接收输入的文本 0.0表示从第0行第0列开始读取 End表示最后一个字符
    content = content.replace('\n',' ')
    BaiduTranslate_test = BaiduTranslate('auto','zh')
    Results = BaiduTranslate_test.BdTrans(content)#要翻译的词组
    txt.insert(tkinter.END,content) # 原文
    txt2.insert(tkinter.END,Results[0]['dst']) # 译文
#    input1_entry.delete(0, END)  # 清空输入

""" 
Label: 标签 单行文本显示
Entry	输入框	接收单行文本输入


place布局方法
x,y 控件的位置
relx,rely 相对位置 0.0-1.0
height, width:高度宽度
relheight,relwidth:相对高度、宽度 0.0-1.0

"""


root = tkinter.Tk()
root.geometry('900x600')
root.title('百度翻译')
# 提示内容--请输入
label1 = tkinter.Label(root, text='请输入您要查询的内容', font=('微软雅黑',16),)
label1.place(relx=0.2, rely=0.05,relwidth=0.6, relheight=0.1)  # , relwidth=0.8, relheight=0.1
# 接收多行文本输入
input1_text = tkinter.Text(root)
input1_text.place(relx=0.1, rely=0.2, relwidth=0.7, relheight=0.2)
#
#
# 可传参的 command方法
btn1 = tkinter.Button(root, text='查询', command=lambda:translate(input1_text,txt,txt2))
btn1.place(relx=0.8, rely=0.2, relwidth=0.1, relheight=0.1)


txt = tkinter.Text(root)
txt.place(relx=0.1, rely=0.45, relwidth=0.7, relheight=0.2)


txt2 = tkinter.Text(root)
txt2.place(relx=0.1, rely=0.7, relwidth=0.7, relheight=0.2)
## 创建Scrollbar组件，设置该组件与text2的纵向滚动关联
#scroll = tkinter.Scrollbar(root, command=txt2.yview)
#scroll.place()
### 设置text2的纵向滚动影响scroll滚动条
#txt2.configure(yscrollcommand=scroll.set)

root.mainloop()