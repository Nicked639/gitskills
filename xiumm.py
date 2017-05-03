from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup
import requests
import re

def generate_url_list(url, page_total):
	url_list = []
	for i in range(2, page_total+1):
		url_list.append(url.split('.html')[0]+'-'+str(i)+'.html')
	return url_list		     
        
def download_image(url):
    html_source = requests.get(url)
    html_source.encoding = 'utf-8'
    soup = BeautifulSoup(html_source.text, 'html.parser')
    items = soup.findAll("div",{"class":"pic_box"})
    items_img = []
    items_img.append(items[0].img['src'])
    for i in range(1,5):
        items_img.append('http://www.xiumm.org'+items[i].img['src'])
    for item in items_img:
        print(item+'\n') 
    
def download_image_else(url):
    html_source = requests.get(url)
    html_source.encoding = 'utf-8'
    soup = BeautifulSoup(html_source.text, 'html.parser')
    items = soup.findAll("div",{"class":"pic_box"})
    items_img = []
    for i in range(1,6):
        items_img.append('http://www.xiumm.org'+items[i].img['src'])
    for item in items_img:
        print(item+'\n') 

if __name__ == '__main__':
    url = "http://www.xiumm.org/photos/LUGirls-17208.html"
    page_total = 8
    # 生成图像页码页面，用于map函数进行多线程下载
    url_list = generate_url_list(url, page_total)
    html_source = requests.get(url)
    # 直接用 requests.get(url).test 会得到乱码，通过分析网页meta发现用 utf-8 编码
    html_source.encoding = 'utf-8'
    soup = BeautifulSoup(html_source.text, 'html.parser')
    # 生成的文件夹名字
    print('Folder: '+soup.title.contents[0].split('-')[0])
    # 下载第一页，区别对待
    download_image(url)
    # 后面的页码
    pool = ThreadPool(4)
    pool.map(download_image_else, url_list)
    pool.close()
    pool.join() 


