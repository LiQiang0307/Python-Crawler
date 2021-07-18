'''
Descripttion: 
version: 
Author: LiQiang
Date: 2021-07-18 20:34:49
LastEditTime: 2021-07-18 20:52:29
'''
import requests
import urllib.request
import re
 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
    'Host': 'openaccess.thecvf.com'
}

url_cvpr='https://openaccess.thecvf.com/CVPR2021?day=all'
html=requests.get(url=url_cvpr,headers=headers)
# print(html.content)


reg = r'<a href="(.*?)">pdf</a>'
urlList=re.findall(reg,html.text)
# print(urlList)
for i in urlList:
    url='https://openaccess.thecvf.com'+i
    urllib.request.urlretrieve(url,i.split('/')[-1])
    print("正在爬取：",i.split('/')[-1])
