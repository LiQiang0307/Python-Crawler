import requests
import re
import pymysql


class Sql(object):
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='mysql',
        db='novel',
        charset='utf8')

    def addnovel(self,sort,sortname,name,imgurl,description,status,author):
        cur=self.conn.cursor()
        cur.execute("insert into novel(sort,sortname,name,imgurl,description,status,author) values('%s','%s','%s','%s','%s','%s','%s') "\
        %(sort,sortname,name,imgurl,description,status,author))

        lastrowid=cur.lastrowid
        cur.close()#关闭游标
        self.conn.commit()
        return lastrowid

    def addchapter(self,novelid,title,content):
        cur=self.conn.cursor()
        cur.execute("insert into chapter(novelid,title,content) values('%s','%s','%s')"%(novelid,title,content))
        cur.close()
        self.conn.commit()

mysql=Sql()#实例对象



sort_dict={
    '1':'玄幻魔法',
    '2':'武侠修真',
    '3':'纯爱耽美',
    '4':'都是言情',
    '5':'职场校园',
    '6':'穿越重生',
    '7':'历史军事',
    '8':'网络动漫',
    '9':'恐怖灵异',
    '10':'科幻小说',
    '11':'美文名著',
}

def getChapterContent(url,lastrowid,title):
    html=requests.get(url)
    html.encoding='gbk'
    #print(html.text)
    reg=r'style5\(\);</script>(.*?)<script type="text/javascript">style6\(\);</script></div>'
    html=re.findall(reg,html.text,re.S)[0]
    mysql.addchapter(lastrowid,title,html)




def getChapterList(url,lastroeid):
    html=requests.get(url)
    html.encoding='gbk'
    reg=r'<li><a href="(.*?)" title=".*?">(.*?)</a></li>'
    chapterInfo=re.findall(reg,html.text)
    for url,title in chapterInfo:
        #print(url)
        getChapterContent(url,lastroeid,title)







def getNovel(url,sort_id,sort_name):
    html=requests.get(url)
    html.encoding='gbk'
    #获取书名
    reg=r'<meta property="og:novel:book_name" content="(.*?)"/>'
    bookname=re.findall(reg,html.text)[0]
    #获取描述
    reg = r'<meta property="og:description" content="(.*?)"/>'
    description=re.findall(reg,html.text,re.S)[0]#re.S支持换行符
    #获取图片
    reg = r'<meta property="og:image" content="(.*?)"/>'
    image=re.findall(reg,html.text)[0]
    #获取作者
    reg=r'<meta property="og:novel:author" content="(.*?)"/>'
    author=re.findall(reg,html.text)[0]
    #获取状态
    reg=r'<meta property="og:novel:status" content="(.*?)"/>'
    status=re.findall(reg,html.text)[0]
    #获取章节地址
    reg=r'<a href="(.*?)" class="reader"'
    chapterUrl=re.findall(reg,html.text)[0]
    print(bookname,author,image,status,chapterUrl)
    #插入数据
    lastrowid=mysql.addnovel(sort_id,sort_name,bookname,image,description,status,author)
    getChapterList(chapterUrl,lastrowid)






def getList(sort_id,sort_name):
    html = requests.get("http://www.quanshuwang.com/list/%s_1.html"%sort_id)
    html.encoding='gbk'
    #print(html.text)
    reg = r'<a target="_blank" href="(.*?)" class="l mr10">'
    urlList=re.findall(reg,html.text)
    #print(urlList)
    for url in urlList:
        getNovel(url,sort_id,sort_name)




for sort_id,sort_name in sort_dict.items():
    getList(sort_id,sort_name)


