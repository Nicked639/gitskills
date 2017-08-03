# -*- coding: utf-8 -*-
from multiprocessing.dummy import Pool as ThreadPool
import os
import requests
import re
import time
import sys
from bs4 import BeautifulSoup as bs
from tkinter import *
import tkinter.messagebox as messagebox

proxies = {'http': 'http://127.0.0.1:1080',
           'https': 'https://127.0.0.1:1080', }

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.nameInput = Entry(self)
        self.nameInput.pack()
        self.alertButton = Button(self, text='下载', command=self.hello)
        self.alertButton.pack()

    def hello(self):
        name = self.nameInput.get()
        download(name)

def folder_size(folder_path):
    #size = sum(os.path.getsize(f) for f in os.listdir(folder_path) if os.path.isfile(f))
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    if total_size // 1024 >= 1024:
        total_size = str(round(total_size // 1024 // 1024, 1)) + 'MB'
    else:
        total_size = str(total_size // 1024) + 'KB'
    return total_size


def download_img(url):
    global down_count, dp_count, img_num
    down_count = down_count + 1
    dp_count = dp_count + 1
    dp = '□' * 15
    status = '下载中'
    if dp_count > 14:
        dp_count = 0
    elif down_count == img_num:
        dp_count = 15
        status = '完成!'
    else:
        pass
    dp = dp.replace('□', '■', dp_count)
    sys.stdout.write('\r' + status + dp +
                        '(' + str(down_count) + '/' + str(img_num) + ')')
    sys.stdout.flush()

    img_data = requests.get(url, proxies=proxies, timeout=10).content
    img_name = url.split('/')[-1]
    with open(folder_path + '\\' + img_name, 'wb') as handler:
        handler.write(img_data)

def download(url):
    #url = 'http://www.xiuren.org/XiuRen-N00766.html'
    global folder_path, img_num
    hs = requests.get(url, proxies=proxies)
    try:
        hs.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % (exc))
    hs.encoding = 'utf-8'
    soup = bs(hs.text, 'html.parser')
    # 创建文件夹
    folder_name = soup.select('#title h1')[0].getText()
    print(folder_name)
    desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')
    folder_path = os.path.join(desktop_path, folder_name)
    if os.path.isdir(folder_path):
        pass
    else:
        os.makedirs(folder_path)
    # 下载图片
    imgurls = soup.select('.photoThum a')
    imglist = []
    for i in imgurls:
        imglist.append(i.get('href'))
    img_num = len(imglist)
    t1 = int(time.time())
    pool2 = ThreadPool(30)
    pool2.map(download_img, imglist)
    pool2.close()
    pool2.join()
    t2 = int(time.time())
    total_size = folder_size(folder_path)
    print('\n共计下载图片: ' + str(img_num) + '张\n耗时: ' + str(t2 - t1) +
            '秒。\n文件夹大小:' + total_size + '\n文件默认保存在桌面:' + folder_name + '\n\n')


# 初始化设置
down_count = 0
dp_count = 0
app = Application()
# 设置窗口标题:
app.master.title('下载')
# 主消息循环:
app.mainloop()