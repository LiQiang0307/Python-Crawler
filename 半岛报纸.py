import requests
from PyPDF2 import PdfFileMerger
import random
import requests
import datetime
from lxml import etree

timeout=5
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Host': 'bddsb.bandao.cn',
    'Referer': 'http://bddsb.bandao.cn/pc/bddsb/20180318/PageA01BC.htm',
    'Upgrade-Insecure-Requests': '1',
}


def Parse(url,pattern):
    response = requests.get(url, timeout=timeout, headers=headers)
    # 解析
    html = response.content
    selector = etree.HTML(html)
    items = selector.xpath(pattern)
    return items


def download(url,file_path='tmp'):
    '''根据链接下载到本地同文件夹下'''
    response = requests.get(url, timeout=timeout, headers=headers)
    with open(file_path,'wb')as f:
        f.write(response.content)

def getDate():
    '''获取前一天的日期'''
    now_time = datetime.datetime.now()
    yes_time = now_time + datetime.timedelta(days=-1)
    yes_time_nyr = yes_time.strftime('%Y%m%d')
    return yes_time_nyr

def SplicePDF(pdf_list, filename):
    '''拼接完整 pdf'''
    merger = PdfFileMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    merger.write(filename)
    merger.close()

def main():
    # 获得报纸各版的 pdf 链接
    print('正在获取PDF下载链接……')
    per_page_list = []
    date = getDate()
    host = 'http://bddsb.bandao.cn/pc/bddsb'
    index_url = '%s/%s/PageArticleIndexBT.htm'%(host, date)
    # items = Parse(index_url, '//div[@class="ban"]//a[1]')
    items = Parse(index_url, '//div[@class="banmianlist_box"]/a[@href]')
    page_sum = len(items)
    print ('The latest newspaper(%s) is a total of %d pages...'%(date, page_sum))
    for item in items:
        # url = '%s/%s/%s'%(host, date, item.attrib['href'].strip('.'))
        paper_no = item.text.split('[')[-1].split(']')[0].strip()
        url = '%s/%s/%s.pdf'%(host, date, paper_no)
        # print url
        per_page_list.append(url)


    # 下载报纸各版本 pdf
    print ('Downloading pdf of each page of newspaper...')
    pdf_list = []
    for i, page_url in enumerate(per_page_list):
        filename = page_url.split('/')[-1]
        file_path = 'content\\%s'%(filename)
        pdf_list.append(file_path)
        print ('[%d/%d] Downloading %s...'%(i+1, page_sum, filename))
        download(page_url, file_path)


    # 拼接完整 pdf
    print ('Splicing pdf...')
    full_pdf_filename = '半岛报纸'+str(date)+'.pdf'
    SplicePDF(pdf_list, full_pdf_filename)


if __name__ == '__main__':
    main()