# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 15:31:11 2020

@author: y1064
"""
import tkinter
import time
from urllib import request, parse
import json
import random
import hashlib 


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



def translate():
    content = inp1.get()
    content = content.replace('\n',' ')
    BaiduTranslate_test = BaiduTranslate('en','zh')
    Results = BaiduTranslate_test.BdTrans(content)#要翻译的词组
    txt.insert(tkinter.END,content) # 原文
    txt2.insert(tkinter.END,Results[0]['dst']) # 译文
#    inp1.delete(0, END)  # 清空输入
    



root = tkinter.Tk()
root.geometry('900x600')
root.title('百度翻译')

lb1 = tkinter.Label(root, text='请输入您要查询的内容')
lb1.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.1)
inp1 = tkinter.Entry(root)
inp1.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.2)


# 方法-直接调用 run1()
btn1 = tkinter.Button(root, text='查询', command=translate)
btn1.place(relx=0.1, rely=0.4, relwidth=0.3, relheight=0.1)


# 在窗体垂直自上而下位置60%处起，布局相对窗体高度40%高的文本框
txt = tkinter.Text(root)
txt.place(rely=0.5, relheight=0.2)

# 在窗体垂直自上而下位置60%处起，布局相对窗体高度40%高的文本框
txt2 = tkinter.Text(root)
txt2.place(rely=0.7, relheight=0.2)

root.mainloop()