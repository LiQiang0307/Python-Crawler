import requests
import re
import os
import urllib.request

#下载视频
def download():
    #获取网页源代码
    url="http://www.pearvideo.com/category_8"
    #模拟浏览器去请求服务器
    headers={
        'User-Agent':'Mozilla / 5.0(Windows NT 10.0;WOW64;rv:62.0) Gecko / 20100101Firefox / 62.0',
    }
    #状态码
    html=requests.get(url,headers=headers)
    #print(html.text)

    #获取视频id   .*？匹配所有
    reg='<a href="(.*?)" class="vervideo-lilink actplay">'
    video_id=re.findall(reg,html.text)
    #print(video_id)

    #拼接URL地址
    video_url=[]#接收拼接好的url
    starturl='http://www.pearvideo.com'+''
    for vid in video_id:
        newurl=starturl+'/'+vid
        #print(newurl)
        video_url.append(newurl)



        #获取视频播放地址
        for purl in video_url:
            html=requests.get(purl,headers=headers)
            reg='ldUrl="",srcUrl="(.*?)"'
            playurl=re.findall(reg,html.text)
            #print(playurl)
            #获取视频标题
            reg='<h1 class="video-tt">(.*?)</h1>'
            video_name=re.findall(reg,html.text)
            #print(video_name[0])

            #下载视频
            print('正在下载视频%s'%video_name)

            path='video'
            if path not in os.listdir():
                os.mkdir(path)
            filepath=path+"/%s"%video_name[0]+'.mp4'
            #下载
            urllib.request.urlretrieve(playurl[0],filepath)

download()

