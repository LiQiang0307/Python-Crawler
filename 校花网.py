import requests
import re
#获取网页地址
#http://www.xiaohuar.com/list-1-3.html
#http://www.xiaohuar.com/list-1-5.html


url='http://www.xiaohuar.com/list-1-%s.html'

for i in range(4):#4表示要爬取4页图片，这里可根据需求做出修改。
    temp=url % i
    print(temp)
    #获取网页源码
    response=requests.get(temp)
    html=response.text
    #从源码文本中匹配我们需要的url
    img_urls=re.findall(r'/d/file/\d+/\w+\.jpg',html)

    for img_url in img_urls:
        img_response=requests.get('http://www.xiaohuar.com%s'%img_url)
        print(img_url)
        #图片的二进制信息
        img_data=img_response.content
        girl=img_url.split('/')[-1]
        with open('%s'%girl,'wb') as f:
            f.write(img_data)
