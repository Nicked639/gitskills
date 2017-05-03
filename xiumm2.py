from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup
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
	pattern = '(?<=/data).*\.jpg'
	match = re.findall(pattern, hs.text)
	img = []
	for m in match:
		img.append('http://www.xiumm.org/data'+m)
	for i in img:
		print(i+'\n')

if __name__ == '__main__':
    url = "http://www.xiumm.org/photos/UGirls-17207.html"
    page_total = 1
    # 生成图像页码页面，用于map函数进行多线程下载
    url_list = generate_url_list(url, page_total)
    # 生成的文件夹名字
    print('Folder: '+create_folder(url))
    # 后面的页码
    pool = ThreadPool(4)
    pool.map(download_img, url_list)
    pool.close()
    pool.join() 

