import re

import pandas
import requests
import pymysql
from lxml import etree
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from tqdm import tqdm


def get_data(url):
    web=get_web(url)
    data=extract(web)
    return data

def get_web(url):
    header={
        'Accept': 'image/avif, image/webp, image/apng, image/svg + xml, image /*, */*;q = 0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN, zh;q = 0.9',
        'User-Agent': 'Mozilla/5.0(Windows NT 10.0;Win64;x64)AppleWebKit/537.36(KHTML, likeGecko) Chrome/112.0.0.0Safari/537.36'
    }
    # res=requests.get(url=url,headers=header)
    option=Options()
    option.add_argument("--headless")
    driver=WebDriver(options=option)
    driver.get(url)
    res=driver.page_source


    return res



def extract(web):
    data=extract_item(web)
    return data

def extract_item(web):

    etrees=etree.HTML(web)
    etree_list=etrees.xpath("//*[@class='item']")

    # print(etree_list)
    data=extract_data(etree_list)
    return data

def extract_data(datas):
    data_list=[]
    for data in datas:

        datas=[]

        title=data.xpath("./div//span[@class='title']/text()")   #电影名字  0
        if title==[]:
            title="错误"
        else:
            title = data.xpath("./div//span[@class='title']/text()")[0].strip()
        datas.append(title)

        quote=data.xpath("./div//span[@class='inq']/text()")#名言  1
        if quote==[]:
            quote="无"
        else:
            quote = data.xpath("./div//span[@class='inq']/text()")[0].strip()
        datas.append(quote)

        rating_num=data.xpath("./div//span[@class='rating_num']/text()")  #评分  2
        if rating_num == []:
            rating_num = "错误"
        else:
            rating_num = data.xpath("./div//span[@class='rating_num']/text()")[0].strip()
        datas.append(rating_num)


        pingjia=data.xpath("./div//div[@class='star']/span[4]/text()") #评价人数  3
        if pingjia == []:
            pingjia = "错误"
        else:
            pingjia = data.xpath("./div//div[@class='star']/span[4]/text()")[0].strip()
        datas.append(pingjia)

        bd=data.xpath("./div//div[@class='bd']/p/text()")
        bd1=bd[0].strip().replace("/",'')
        # print(bd1,type(bd1))

        #
        dao_yan=re.findall(re.compile(r"导演:(.*?)主演",re.S),bd1) #导演  4
        if dao_yan!=[]:
            dao_yan = re.findall(re.compile(r"导演:(.*?)主演", re.S), bd1)[0].strip().replace("\xa0",'')
        elif dao_yan==[]:
            dao_yan = re.findall(re.compile(r"导演:(.*?)主", re.S), bd1)
        elif dao_yan!=[]:
            dao_yan = re.findall(re.compile(r"导演:(.*?)主", re.S), bd1)[0].strip().replace("\xa0",'')
        elif dao_yan==[]:
            dao_yan = re.findall(re.compile(r"导演:(.*)...", re.S), bd1)
        elif dao_yan!=[]:
            dao_yan = re.findall(re.compile(r"导演:(.*)...", re.S), bd1)[0].strip().replace("\xa0",'')
        else:
            dao_yan = "错误"
        datas.append(dao_yan)


        zhu_yan=re.findall( re.compile(r"主演:(.*)...", re.S),bd1) #主演  5
        if zhu_yan==[]:
            zhu_yan='不详'
        else:
            zhu_yan=re.findall( re.compile(r"主演:(.*)...", re.S),bd1)[0].strip()
        datas.append(zhu_yan)

        ju_qing=bd[1].strip().replace("\xa0",'') #简介 6
        datas.append(ju_qing)


        href=data.xpath("./div//div[@class='hd']/a/@href")[0].strip()  #电影链接  7
        datas.append(href)


        data_list.append(datas)

    return data_list

def get_con():
    con=pymysql.Connect(host='localhost',password='mysql123',user='root',port=3306,database='douban',charset='utf8')
    return con
def execute_insert_sql(data):

    con=get_con()
    cursor=con.cursor()
    for i in data:

        sql="""insert into movie (moviename,daoyan,zhuyan,pingfen,pfnums,quote,jianjie,href) values ("%s","%s","%s","%s","%s","%s","%s","%s");"""%(i[0],i[4],i[5],i[2],i[3],i[1],i[6],i[7])
        print(sql)
        cursor.execute(sql)
        con.commit()
    con.close()


if __name__ == '__main__':
    url='https://movie.douban.com/top250?start=%s&filter='
    datas_list = []
    for i in tqdm(range(10)):
        i=str(i*25)
        data_list=get_data(url%i)
    #     datas_list=data_list+datas_list
        execute_insert_sql(data_list)
    # dic={
    #     'moviename':[],
    #     'daoyan':[],
    #     'zhuyan':[],
    #     'pingfen':[],
    #     'pfnums':[],
    #     'quote':[],
    #     'jianjie':[],
    #     'href':[]
    # }
    # for i in datas_list:
    #     dic['moviename'].append(i[0])
    #     dic['daoyan'].append(i[4])
    #     dic['zhuyan'].append(i[5])
    #     dic['pingfen'].append(i[2])
    #     dic['pfnums'].append(i[3])
    #     dic['quote'].append(i[1])
    #     dic['jianjie'].append(i[6])
    #     dic['href'].append(i[7])
    # aa=pandas.DataFrame(data=dic)
    # aa.to_excel("./douban1.xlsx")
