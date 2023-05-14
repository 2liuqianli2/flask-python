# import re
# result=re.compile("导演:(.*)...",re.S)
# data=re.findall(pattern=result,string="导演: 拉娜·沃卓斯基 Lana Wachowski / 莉莉·沃卓斯基 Lilly Wachowski   ...")
# print(data)
import pymysql
import numpy as np
from matplotlib import pyplot as plt

con = pymysql.Connection(host='localhost', user='root', password='mysql123', port=3306, charset='utf8',database="douban")
cursor = con.cursor()
cursor.execute("select quote from movie;")
datas = cursor.fetchall()

cursor.close()
con.close()

aa="""
Gui Zexuan is going to climb the hill with his friends. We are discussing. I asked my little brother what plans you are going to in the holiday. He invited us to go his home. He wanted to go Suyukou with us. I was glad to hear the news. Our family decided to go Yingchun to Suyukou on trip
May holiday is coming. Our family is going to do something. Today I called my little brothers phone at the noon. He asked me what I am going to do in the holiday. I told him we want to go on a trip some day during but where we dont decide to go. We are going to sleep in the morning May first. Then we are going to go to Dawukou by bus in the afternoon. We are going to have a day off May 2nd. If its will fine in May 3rd we are going to go out on trip. I am going to go to the Forest Park. Your sisters husband is going to hometown Xiamiao. He wants to go fishing
"""
# with open("./aa.txt",'w',encoding='utf-8') as op:
#     op.write(aa)
#     op.flush()

import jieba     #引用中文分词库
import wordcloud    #引用词云库

#
# with open("./aa.txt",'r',encoding='utf-8') as op:
#     text=op.read()


# for i in datas:
#     text +=i[0]
mask=plt.imread("../static/picture/ad.jpg")
cut=jieba.cut(aa)
str=' '.join(cut)
print(str)

w = wordcloud.WordCloud(font_path='../static/font/msyhbd.ttc',width = 500,\
                        height = 500,background_color = "white",\
                        max_words = 30,mask=mask)                #配置参数
w.generate_from_text(str)       #加载文本
w.to_file("wordcloud.png")      #输出保存