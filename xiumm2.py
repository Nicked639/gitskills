from multiprocessing.dummy import Pool as ThreadPool
import os
import requests
import re

def generate_url_list(url, page_total):
	url_list = []
	url_list.append(url)
	for i in range(2, page_total+1):
		url_list.append(url.split('.html')[0]+'-'+str(i)+'.html')
	return url_list

def create_folder(url):
	hs = requests.get(url)
	hs.encoding = 'utf-8'
	pattern = '(?<=<title>).*(?=\-)'
	match = re.findall(pattern, hs.text)
	return match[0]

def download_img(url):
	hs = requests.get(url)
	hs.encoding = 'utf-8'
	pattern_url = '(?<=/data).*\.jpg'
	match_url = re.findall(pattern_url, hs.text)
	pattern_name = '\d{14}\.jpg'
	img_url = []
	img_name = []
	for m in match_url:
		img_url.append('http://www.xiumm.org/data'+m)
		img_name.append(re.findall(pattern_name, m)[0])
	for i in range(0,len(img_url)):
		print(img_url[i]+'\n'+img_name[i]+'\n')

if __name__ == '__main__':
	url = "http://www.xiumm.org/photos/UGirls-17207.html"
	page_total = 1
    # 生成图像页码页面，用于map函数进行多线程下载
	url_list = generate_url_list(url, page_total)
    # 生成的文件夹名字
	folder_name = create_folder(url)
	folder_path = r'G:\\工作目录\\Desktop\\' + folder_name
	print('Folder: '+ folder_path)
	if os.path.isdir(folder_path):
		pass
	else:
		os.makedirs(folder_path)
	pool = ThreadPool(4)
	r= pool.map(download_img, url_list)
	print(type(r))
	pool.close()
	pool.join() 

