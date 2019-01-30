#爬取喜马拉雅音乐排行榜中所有的音乐

import requests
import json,time

#https://www.ximalaya.com/revision/play/album?albumId=3595841&pageNum=3&sort=-1&pageSize=30

def xima(a):
    url = "https://www.ximalaya.com/revision/play/album?albumId=3595841&pageNum="+(str)(a)+"&sort=-1&pageSize=30"
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0',
    }
    html=requests.get(url,headers=headers)
    ret=html.content.decode()#返回字符串类型数据
    #print(ret)
    result = json.loads(ret)
    #print(result['data']['tracksAudioPlay'][0]['src'])
    for i in result['data']['tracksAudioPlay']:
        #print(i['src'])
        src=i['src']
        name=i['trackName']
        #print(name)
    #保存数据
        with open("./{}.mp3".format(name),'ab')as f:
            music=requests.get(src,headers=headers)
            f.write(music.content)

if __name__ == '__main__':
    for i in range(1,7):
        xima(i)
        time.sleep(5)

