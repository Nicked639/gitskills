from multiprocessing.dummy import Pool as ThreadPool
import os
import requests
import re
import time
import console
import sys

def generate_url_list(url, page_total):
	url_list = []
	url_list.append(url)
	for i in range(2, page_total+1):
		url_list.append(url.split('.html')[0]+'-'+str(i)+'.html')
	return url_list

def count_page(url):
	hs = requests.get(url)
	hs.encoding = 'utf-8'
	pattern = '(?<=共).*(?=页)'
	match = re.findall(pattern, hs.text)
	return match[0]

def create_folder(url):
	hs = requests.get(url)
	hs.encoding = 'utf-8'
	pattern = '(?<=<title>).*(?=\-)'
	match = re.findall(pattern, hs.text)
	return match[0]

def create_path(folder_name):
	path=os.path.abspath('.')
	path_match=re.findall('(?<=/Documents).*',path)
	path=path.replace(path_match[0],'')
	path = path + '/' + folder_name
	return path

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
	console.set_color(.2,.8,.2)
	dp='□'*15
	status = '下载中'
	if dp_count > 14:
		dp_count = 0
	elif down_count == img_num:
		console.set_color(1,0,.8)
		dp_count=15
		status='完成!'
	else:
		pass
	dp = dp.replace('□','■',dp_count)
	sys.stdout.write('\r'+status+dp+'('+str(down_count)+'/'+str(img_num)+')')
	sys.stdout.flush()
	
	img_data = requests.get(url).content
	img_name = url.split('/')[-1]
	with open(folder_path + '/' + img_name,'wb') as handler:
		handler.write(img_data)

if __name__ == '__main__':
	global folder_path
	down_count = 0
	dp_count = 0
	url = "http://www.xiumm.org/photos/YOUMI-17244.html"
	page_total = int(count_page(url))
    # 生成图像页码页面，用于map函数进行多线程下载
	url_list = generate_url_list(url, page_total)
    # 生成的文件夹名字
	folder_name = create_folder(url)
	# map 的函数接受一个参数，故用了全局参数作为存图路径
	folder_path = create_path(folder_name)
	if os.path.isdir(folder_path):
		pass
	else:
		os.makedirs(folder_path)
	# 获取图像url
	pool = ThreadPool(4)
	down_url = pool.map(download_url, url_list)
	pool.close()
	pool.join() 
	download_url_list = []
	for i in down_url:
		for j in i:
			download_url_list.append(j)
	img_num = len(download_url_list)
	# 下载图像
	console.clear()
	console.set_color(1,0,.8)
	console.set_font('Menlo',17)
	t1 = int(time.time())
	pool2 = ThreadPool(6)
	pool2.map(download_img, download_url_list)
	pool2.close()
	pool2.join()
	t2 = int(time.time())	
	total_size = folder_size(folder_path)
	print('\n共计下载图片: '+str(len(download_url_list))+'张\n耗时: '+str(t2-t1)+'秒。\n文件夹大小:'+total_size+'\n文件默认保存在根目录:'+folder_name)
