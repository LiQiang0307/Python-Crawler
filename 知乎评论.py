import requests
import json
import time

def content(a):
    url="https://www.zhihu.com/api/v4/articles/19991701/comments"
    date={
        'include':'data[*].author,collapsed,reply_to_author,disliked,content,voting,vote_count,is_parent_author,is_author,algorithm_right',
        'limit':'20',
        'offset':str(a),
        'order':'normal',
        'status':'open'
    }
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0'}

    html=requests.get(url,params=date,headers=headers)
    #print(html.json()['data'])
    for i in html.json()['data']:
        content=i['content']
        id=i['author']['member']['id']
        name=i['author']['member']['name']
        print(name+str(id)+":"+content)
        #数据写入文档的过程中可能出现UnicodeEncodeError: 'gbk' codec can't encode character '\uXXX' in position XXX: illegal multibyte sequence
        #使用try，except忽略，并不影响数据的写入。
        with open("pinglun.txt",'a')as f:
            try:
                f.write(name+str(id)+":"+content)
            except:
                print("")


if __name__ == '__main__':
    for i in range(0,4):
        content(i*20)
        time.sleep(5)

