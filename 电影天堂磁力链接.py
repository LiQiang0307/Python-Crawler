import requests
import re


for page in range(1,178):
    url='http://www.ygdy8.net/html/gndy/dyzz/list_23_'+str(page)+'.html'
    print(url)
    html=requests.get(url)
    html.encoding="gb2312"
    #print(html.text)
    data=re.findall('<a href="(.*?)" class="ulink">',html.text)  #返回的是列表
    #print(data)
    for m in data:
        xqurl = 'http://www.ygdy8.net'+m
        #print(xqurl)

        html2=requests.get(xqurl)
        html2.encoding='gb2312'#指定编码
        #print(html2.text)
        try:
            dyLink = re.findall('<a href="(.*?)">ftp://.*?</a></td>',html2.text)[0]
            print(dyLink)
        except:
            print("没有匹配信息")

        with open('电影天堂.txt','a') as f:
            f.write(dyLink+'\n')
