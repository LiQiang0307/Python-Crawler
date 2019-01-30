#获取链家网数据
import requests
import re
from bs4 import BeautifulSoup
from multiprocessing import Pool

urls=[]
header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0'}
#获取17个地区的连接地址存入到urls中
def getAreaUrls():
    url="https://bj.lianjia.com/zufang"
    html=requests.get(url,headers=header)
    soup=BeautifulSoup(html.text,'lxml')
    areas=soup.find_all(attrs={'data-type':'district'})
    #print(areas)
    for area in areas[1:]:
        url_area=(area.a)['href']
        area_name=(area.a).text
        urls.append(url_area)
        #print(url_area,area_name)


# getAreaUrls()
# print(urls)
#获取每个地区的租房信息
def oneArea(url):
    # https: // bj.lianjia.com / zufang / dongcheng / pg1 /  # contentList
    title_list = []
    address_list = []
    prices_list = []
    i=1
    url0="https://bj.lianjia.com"+url+'pg%s/#contentList'%i
    print(url0)
    html=requests.get(url0,headers=header)
    #获取每个地区租房信息的页数page
    page=re.findall('data-totalPage=(.*?) data-curPage=1>',html.text)
    print(int(page[0]))
    pages=int(page[0])#总的页数
    for i in range(1,pages+1):
        url1 = "https://bj.lianjia.com" + url + 'pg%s/#contentList' % i
        print(url1)
        content=requests.get(url1,headers=header)
        soup=BeautifulSoup(content.text,'lxml')
        # 获取标题
        titles = soup.find_all(class_='content__list--item--title twoline')
        # 获取地点
        addrs = soup.find_all(class_='content__list--item--des')
        # 获取价格
        prices = soup.find_all(class_='content__list--item-price')
        for title in titles:
            title_list.append(title.a.text.strip())
        for addr in addrs:
            address_list.append(addr.text.replace('\n', '').replace(' ', ''))
        for p in prices:
            prices_list.append(p.text)
        allInfo = zip(title_list, address_list, prices_list)

        #将获取到的信息存入到text文件中。
        for info in allInfo:
            with open(url[8:-1]+'.txt','a',encoding='utf-8') as f:
                f.write(str(info))
            print(info)



if __name__ == '__main__':
    pool = Pool()
    getAreaUrls()#获取所有的地区
    pool.map(oneArea,[i for i in urls])
