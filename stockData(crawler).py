#本程序为“股票数据定向爬虫”
#来自北理工网络公开课——Python网络爬虫与信息提取
#课程链接http://open.163.com/movie/2019/5/I/O/MEEMCM1NP_MEF0L2JIO.html
#功能描述
'''
目标：获取上交所和深交所所有股票的名称和交易信息
输出：保存到文件中
技术方案：requests-bs4-re
候选网站：
1、新浪股票：http://finance.sina.com.cn/stock/
2、百度股票：https://gupiao.baidu.com/stock/
选取原则：股票信息静态存放在HTML页面中，非js代码生成，没有robots协议限制

新浪股票：js代码生成
百度股票：嵌在html代码中（更适合定向爬虫）

确定所有股票列表
使用另一个网站：东方财富网http://quote.eastmoney.com/stock_list.html

程序的结构设计：
1、从东方财富网获取股票列表
2、根据股票列表逐个到百度股票获取个股信息
3、将结果存储到文件中

根据百度股票对个股信息的保留方式，我们考虑采用字典的方式来进行存储

小结：
非常有特征的数据，我们可以通过正则表达式来获取；
存在的区域相对固定，可以用bs，然后再用正则表达式
'''
import requests
from bs4 import BeautifulSoup
import traceback
import re

#获得URL对应的页面
def getHTMLText(url,code='utf-8'):
    try:
        r=requests.get(url,timeout=30)
        r.raise_for_status()
        '''
        速度提高：编码识别的优化
        r.apparent_encoding是将获得的html页面文本内容交给程序来判断
        而r.encoding只是从html的头文件中解析其用的方式
        '''
        #r.encoding=r.apparent_encoding
        r.encoding=code
        return r.text
    except:
        return ""

#获得股票的信息列表
def getStockList(lst,stockURL):
    html=getHTMLText(stockURL,'GB2312')
    soup=BeautifulSoup(html,'html.parser')
    #通过观察东方财富网的源代码，我们发现我们要找的股票代码都存在了<a>标签里，所以我们需要找到所有的<a>标签
    a=soup.find_all('a')
    for i in a:
        # 我们找到<a>标签里面的href属性中的最后html前面有股票代码我们将其提取出来即可
        # <a target="_blank" href="http://quote.eastmoney.com/sh201000.html">
        # 股票代码的规律，上交所的为“sh+6位数字”，深交所的为“sz+6位数字”
        try:
            href=i.attrs['href']
            lst.append(re.findall(r"[s][hz]\d{6}",href)[0])
        except:
            continue#出现异常程序继续执行即可，可能一些匹配出现问题



#获得每一个个股的股票信息，并将其存在一个文件中
def getStockInfo(lst,stockURL,fpath):
    #在百度股票中
    count = 0
    for stock in lst:
        url=stockURL+stock+".html"
        html=getHTMLText(url)
        try:
            if html=="":
                continue
            #定义一个字典，存储从页面中返回的所有的个股信息
            infoDict={}
            soup=BeautifulSoup(html,"html.parser")
            stockInfo=soup.find('div',attrs={'class':'stock-bets'})
            name=stockInfo.find_all(attrs={'class':'bets-name'})[0]
            #可能待会儿在这出现差错，是因为在东方财富网上的有关基金在百度股票网上找不到对应的股票
            infoDict.update({'股票名称':name.text.split()[0]})

            keyList=stockInfo.find_all('dt')
            valueList=stockInfo.find_all('dd')

            for i in range(len(keyList)):
                key=keyList[i].text
                val=valueList[i].text
                infoDict[key]=val#字典的用法

            #体验提高：增加动态进度显示

            with open(fpath,'a',encoding='utf-8') as f:
                f.write(str(infoDict)+'\n')
                count+=1
                print("\r当前进度：{:.2f}%".format(count*100/len(lst)),end="")#\r打印的内容会覆盖之前的内容

        except:
            #traceback.print_exc()#知道哪些地方发生了异常，获得错误信息
            count+=1
            print("\r当前进度：{:.2f}%".format(count * 100 / len(lst)), end="")
            continue



if __name__ == '__main__':
    stock_list_url="http://quote.eastmoney.com/stock_list.html"#股票列表的网站
    stock_info_url='https://gupiao.baidu.com/stock/'
    output_file="D://BaiduStockInfo.txt"
    slist=[]#存储股票的信息
    getStockList(slist,stock_list_url)
    getStockInfo(slist,stock_info_url,output_file)
