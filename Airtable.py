import re
import requests
import json

def findMovieData(url,id):
    apiUrl = "https://api.douban.com/v2/movie/subject/"
    airData = requests.get(apiUrl + id, timeout=5)
    data = json.loads(airData.text)
    content = {
        "fields": {
            "Title": data['title'],
            "Original Title": data['original_title'],
            "Year": data['year'],
            "Director": "，".join(map(lambda x:x['name'],data['directors'])),
            "Cast": "，".join(map(lambda x:x['name'],data['casts'])),
            "Genre": "，".join(data['genres']),
            "Country": "，".join(data['countries']),
            "Douban Link": data['alt'],
            "Aka": "，".join(data['aka']),
            "Summary": data['summary'],
            "Douban Rating":data['rating']['average'],
            "Subtype": data['subtype'],
            "Cover": [{
            "url": data['images']['large']
            }]
        }
    }
    postAirtable(content,"Movie")

def findBookData(url,id):
    apiUrl = "https://api.douban.com/v2/book/"

    airData = requests.get(apiUrl + id, timeout=5)
    data = json.loads(airData.text)
    content = {
        "fields": {
            "Title": data['title'],
            "Publish Time": data['pubdate'], 
            "Author": "，".join(data['author']),
            "Translator": "，".join(data['translator']),
            "Pages": data['pages'],
            "Price": data['price'], 
            "Douban Link": data['alt'],
            "Summary": data['summary'],
            "Douban Rating":data['rating']['average'],
            "Read": False,
            "Sub Title": data['subtitle'], 
            "Publisher": data['publisher'], 
            "Author Intro": data['author_intro'], 
            "Cover": [{
            "url": data['images']['large']
            }]
        }
    }
    postAirtable(content,"Book")

def postAirtable(data,type):
    airUrl = 'https://api.airtable.com/v0/appJJmTgbDFTEnJxz/' + type + 's'
    headers ={"Authorization": "Bearer keykc37vqMlAXD3TS"}
    r = requests.post(url = airUrl, headers = headers, json = data)
    if r.json()['id']:
        print('成功！')
    else:
        print('失败！')

if __name__ == '__main__':
    url = input('请输入豆瓣网址：\n')
    idPattern = r'\d{5,8}'
    id = re.findall(idPattern,url)[0]
    print("id: "+ id)
    if re.match(r'(.*)movie(.*)',url):
        data = findMovieData(url,id)
    else:
        data = findBookData(url,id)
