import requests
import urllib.request
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
    'Host': 'openaccess.thecvf.com'
}

urlList=[]

with open('README.md','r',encoding='utf-8')as f:
    data=f.readlines()
    # print(data)
    for i in data:
        try:
            # pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+') # 匹配模式
            url = re.findall(r'\d+\.\d+v\d',str(i))#匹配2和0之前的数据
            urlList.append(f"http://arxiv.org/abs/{url[0]}")
            print(f"http://arxiv.org/abs/{url}")
        except:
            pass

print(urlList)
# urlList=[
#     "http://arxiv.org/abs/2303.17490v1.pdf"
# ]

for url in urlList:
    try:
        html = urlopen(url).read().decode("utf-8")
        html=bs = BeautifulSoup(html, 'html.parser')
        content=bs.find_all(["h1"])
        title=re.findall('<span class="descriptor">Title:</span>(.*?)</h1>',str(content))
        urllib.request.urlretrieve(url, f"{title[0].replace(':','')}.pdf")
        print("正在爬取：",url,title[0])
    except:
        pass