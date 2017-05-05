# -*- coding: utf-8 -*-
from multiprocessing.dummy import Pool as ThreadPool
import os
import requests
import re
import time
import sys
def generate_url_list(url, page_total):
	url_list = []
	url_list.append(url)
	for i in range(2, page_total+1):
		url_list.append(url.split('.html')[0]+'-'+str(i)+'.html')
	return url_list

def config_url(url):
	hs = requests.get(url)
	hs.encoding = 'utf-8'
	pattern_page = '(?<=共).*(?=页)'
	pattern_name = '(?<=<title>).*(?= \-)'
	page = re.findall(pattern_page, hs.text)[0]
	folder_name = re.findall(pattern_name, hs.text)[0]
	print(folder_name)
	desktop_path = os.path.join(os.path.expanduser("~"),'Desktop')
	path = desktop_path + '\\' + folder_name
	config = {'page_total': int(page), 'folder_name': folder_name, 'folder_path': path}	
	return config

def folder_size(folder_path):
	#size = sum(os.path.getsize(f) for f in os.listdir(folder_path) if os.path.isfile(f))
	total_size = 0
	for dirpath, dirnames, filenames in os.walk(folder_path):
		for f in filenames:
			fp = os.path.join(dirpath, f)
			total_size += os.path.getsize(fp)
	if total_size//1024>=1024:
		total_size=str(round(total_size//1024//1024,1))+'MB'
	else:
		total_size=str(total_size//1024)+'KB'
	return total_size

def download_url(url):
	hs = requests.get(url)
	hs.encoding = 'utf-8'
	pattern_url = '(?<=/data).*\.jpg'
	match_url = re.findall(pattern_url, hs.text)
	img_url = []
	for m in match_url:
		img_url.append('http://www.xiumm.org/data'+m)
	return img_url

def download_img(url):
	global down_count, dp_count, img_num
	down_count = down_count+1
	dp_count = dp_count+1
	dp='□'*15
	status = '下载中'
	if dp_count > 14:
		dp_count = 0
	elif down_count == img_num:
		dp_count=15
		status='完成!'
	else:
		pass
	dp = dp.replace('□','■',dp_count)
	sys.stdout.write('\r'+status+dp+'('+str(down_count)+'/'+str(img_num)+')')
	sys.stdout.flush()
	
	img_data = requests.get(url, timeout=3).content
	img_name = url.split('/')[-1]
	with open(folder_path + '\\' + img_name,'wb') as handler:
		handler.write(img_data)

if __name__ == '__main__':
    # 初始化设置
	global folder_path
	down_count = 0
	dp_count = 0
	config = {}
	url = 'http://www.xiumm.org/photos/BoLoLI-17239.html'
	config = config_url(url)

    # 生成的存储图像路径，map 的函数接受一个参数，故用了全局参数作为存图路径
	folder_name = config['folder_name']
	folder_path = config['folder_path']
	if os.path.isdir(folder_path):
		pass
	else:
		os.makedirs(folder_path)

	# 生成图像页码页面，用于map函数进行多线程下载
	page_total= 1 #config['page_total']
	url_list = generate_url_list(url, page_total)

	# 获取图像 url list
	pool = ThreadPool(4)
	down_url = pool.map(download_url, url_list)
	pool.close()
	pool.join() 
	download_url_list = []
	for i in down_url:
		for j in i:
			download_url_list.append(j)
	# 下载图像
	img_num = len(download_url_list)
	t1 = int(time.time())
	pool2 = ThreadPool(6)
	pool2.map(download_img, download_url_list)
	pool2.close()
	pool2.join()
	t2 = int(time.time())	
	total_size = folder_size(folder_path)
	print('\n共计下载图片: '+str(len(download_url_list))+'张\n耗时: '+str(t2-t1)+'秒。\n文件夹大小:'+total_size+'\n文件默认保存在桌面:'+folder_name)
