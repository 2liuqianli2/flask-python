from wordcloud import WordCloud
import jieba
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
import  pymysql


#准备词云需要的文字
con=pymysql.Connection(password='mysql123',port=3306,user='root',host='localhost',database='douban',charset='utf8')
cursor=con.cursor()
cursor.execute("select quote from movie")
datas=cursor.fetchall()
text=""
# print(len(datas))
for i in datas:
    str = i[0]
    text +=str
#     text +=i[0]
# cut=jieba.cut(text)
# str=' '.join(cut)
print(text)

img=Image.open(r'../static/picture/pikaqu.jpeg')
img_arr=np.array(img)
plt.imshow(img_arr)
plt.show()
wc=WordCloud(
    background_color='white',
    mask=img_arr,
    width=450,
    height=600,
    font_path="../static/font/msyhbd.ttc",
    # stopwords=['的','是','你','人','了','都','不','和','我','无','在','最','让','就','有',]
)
wc.generate_from_text(text)

plt.imshow(wc)
plt.axis('off')#关闭坐标轴
plt.savefig(r'../static/picture/6.jpg',dpi=600)
plt.show()

