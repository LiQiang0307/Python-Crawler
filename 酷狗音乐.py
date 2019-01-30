import time
import requests
from bs4 import BeautifulSoup


headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:58.0) Gecko/20100101 Firefox/58.0'}


def top(url):
    html = requests.get(url, headers=headers)
    soup=BeautifulSoup(html.text,'lxml')
    No = soup.select('.pc_temp_num')
    titles = soup.select('.pc_temp_songname')
    href = soup.select('.pc_temp_songname')
    time = soup.select('.pc_temp_time')
    for No,titles,time,href in zip(No,titles,time,href):
        data={
            'NO':No.get_text().strip(),
            'titles':titles.get_text(),
            'time':time.get_text().strip(),
            'href':href.get('href')        }
        print(data)



if __name__=='__main__':
    urls = {'http://www.kugou.com/yy/rank/home/{}-8888.html'.format(str(i)) for i in range(1,24)}
    for url in urls:
        time.sleep(5)
        top(url)
