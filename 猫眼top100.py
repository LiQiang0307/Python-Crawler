import requests
import re
import json
import pymysql
from multiprocessing import Pool
from requests.exceptions import RequestException
headers={
    "User-Agent":"Mozilla / 5.0(Windows NT 10.0;WOW64;rv:63.0) Gecko / 20100101Firefox / 63.0",
    'Host':'maoyan.com',
    'Accept':'text / html, application / xhtml + xml, application / xml;q = 0.9, * / *;q = 0.8',
    'Accept-Language':'zh - CN, zh;q = 0.8, zh - TW;q = 0.7, zh - HK;q = 0.5, en - US;q = 0.3, en;q = 0.2',
    'Accept-Encoding':'gzip, deflate',
    'Connection':'keep-alive',
    'Upgrade - Insecure - Requests':'1',
    'Cache - Control':'max - age = 0'
}

class Sql(object):
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='mysql',
        db='ccunews',
        charset='utf8')

    def addnews(self,movienum,moviename,moviegrade,movietime,moviemessage,moviecountry):
        cur=self.conn.cursor()
        cur.execute("insert into mymovie(movienum,moviename,moviegrade,movietime,moviemessage,moviecountry) values('%s','%s','%s','%s','%s','%s') "%(movienum,moviename,moviegrade,movietime,moviemessage,moviecountry))
        lastrowid=cur.lastrowid
        cur.close()#关闭游标
        self.conn.commit()
        return lastrowid

mysql=Sql()

def get_one_page(url):
    try:

        response=requests.get(url,headers=headers)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern=re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'+'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'+'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
    items=re.findall(pattern,html)
    for item in items:
        yield {
            'index':item[0],
            'image':item[1].split('@')[0],
            'title':item[2],
            'actor':item[3].strip()[3:],
            'time':item[4].strip()[5:15],
            'score':item[5]+item[6],
            'country':item[4].strip()[16:-1]
        }
        # print(item[4])
        # print(item[4].strip()[5:15])
        # print(item[4].strip()[16:-1])



def write_to_file(content):

    with open('result.txt','a',encoding='utf-8')as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()



def main(offset):

    url='http://maoyan.com/board/4?offset='+ str(offset)
    html=get_one_page(url)
    for item in parse_one_page(html):

        #mysql.addnews(item['index'], item['title'], item['score'], item['time'], item['actor'],item['country'])
        #print(item)
        write_to_file(item)
        


if __name__=='__main__':
    pool=Pool()
    pool.map(main,[i*10 for i in range(10)])

