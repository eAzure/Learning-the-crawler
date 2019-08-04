#"中国大学排名"定向爬虫示例
#课程地址：http://open.163.com/movie/2019/5/G/6/MEEMCM1NP_MEEU3UFG6.html
#功能描述：
#输入：大学排名URL链接
#输出：大学排名信息的屏幕输出（排名，大学名称，总分）
#使用技术：requests库和bs4
#定向爬虫：仅对输入URL进行爬取，不扩展爬取
#是否可以实现：查看网页源代码判断是否是静态页面
#查看robots协议：网页不存在（无robots协议）
'''
程序的结构设计：
    1、从网络上获取大学排名网页内容——getHTMLText()；
    2、提取网页内容中信息到合适的数据结构——fillUnivList()；
    3、利用数据结构展示并输出结果——printUnivList()
'''

import requests
from bs4 import BeautifulSoup
import bs4

def getHTMLText(url):
    try:
        r=requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return ""

def fillUnivList(ulist,html):
    soup=BeautifulSoup(html,"html.parser")
    for tr in soup.find('tbody').children:
        #过滤非标签信息
        if isinstance(tr,bs4.element.Tag):
            tds =tr('td')#查询
            ulist.append([tds[0].string,tds[1].string,tds[3].string])

#num指打印多少个元素出来
def printUnivList(ulist,num):
    #格式化输出
    '''
    中文字符宽度不够，系统用英文进行填充，导致对齐出现问题
    print("{:^10}\t{:^6}\t{:^10}".format("排名","学校名称","总分"))
    for i in range(num):
        u=ulist[i]
        print("{:^10}\t{:^6}\t{:^10}".format(u[0], u[1], u[2]))
    采用中文字符的空格填充chr(12288)
    '''
    #优化后的格式化输出
    tplt ="{0:^10}\t{1:{3}^10}\t{2:^10}"
    print(tplt.format("排名", "学校名称", "总分",chr(12288)))
    for i in range(num):
        u = ulist[i]
        print(tplt.format(u[0], u[1], u[2],chr(12288)))


if __name__ == '__main__':
    uinfo=[]#大学信息列表
    url="http://www.zuihaodaxue.com/zuihaodaxuepaiming2016.html"
    html=getHTMLText(url)
    fillUnivList(uinfo,html)
    printUnivList(uinfo,20)