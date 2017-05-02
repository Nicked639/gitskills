from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup
import requests
import re
def get_page(url):
    html = requests.get(url).text
    bsobj = BeautifulSoup(html, 'lxml')
    return bsobj
def parse_page(html):
    items = html.findAll("div",{"class":"desktop"})
    for item in items:
        print("title: {}\nurl: {}".format(item.img['title'],re_page(item.img['src'])))
def re_page(html):
    pattern = re.compile('(.*?).295x184_q100.png')
    items = re.findall(pattern, html)
    for item in items:
        return item
def main(page):
    url = "http://simpledesktops.com/browse/{}/".format(page)
    html = get_page(url)
    parse_page(html)
if __name__ == '__main__':
    url = "http://www.xiumm.org/photos/LUGirls-17208.html"
    
    html_source = requests.get(url)
    html_source.encoding = 'utf-8'
    soup = BeautifulSoup(html_source.text, 'html.parser')
    print(soup.title.contents)

    # pool = ThreadPool(6)
    # pool.map(main, [page for page in range(1,2)])
    # pool.close()
    # pool.join()