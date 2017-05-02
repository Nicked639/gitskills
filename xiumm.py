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
		
def get_page(url):
    html_source = requests.get(url)
    html_source.encoding = 'utf-8'
    soup = BeautifulSoup(html_source.text, 'html.parser')
    return soup
    
def parse_page(html):
    items = html.findAll("div",{"class":"desktop"})
    for item in items:
        print("title: {}\nurl: {}".format(item.img['title'],re_page(item.img['src'])))
        
def re_page(html):
    pattern = re.compile('(.*?).295x184_q100.png')
    items = re.findall(pattern, html)
    for item in items:
        return item
        
def download_image(url):
    html = get_page(url)
    parse_page(html)
    
if __name__ == '__main__':
    url = "http://www.xiumm.org/photos/LUGirls-17208.html"
    page_total = 8
    url_list = generate_url_list(url, page_total)
    html_source = requests.get(url)
    html_source.encoding = 'utf-8'
    soup = BeautifulSoup(html_source.text, 'html.parser')
    print('Folder: '+soup.title.contents[0].split('-')[0])

    # pool = ThreadPool(6)
    # pool.map(download_image, url_list)
    # pool.close()
    # pool.join() 
