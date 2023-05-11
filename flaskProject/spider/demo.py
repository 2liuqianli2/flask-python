# import re
# result=re.compile("导演:(.*)...",re.S)
# data=re.findall(pattern=result,string="导演: 拉娜·沃卓斯基 Lana Wachowski / 莉莉·沃卓斯基 Lilly Wachowski   ...")
# print(data)
import pymysql

con = pymysql.Connection(host='localhost', user='root', password='mysql123', port=3306, charset='utf8',database="douban")
cursor = con.cursor()
cursor.execute("select * from movie;")
movie_data = cursor.fetchall()
print(movie_data)
cursor.close()
con.close()