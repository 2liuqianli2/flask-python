import pymysql
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route("/index")
def home():
    return render_template('index.html')

@app.route("/movie")
def movie():
    con=pymysql.Connection(host='localhost',user='root',password='mysql123',port=3306,charset='utf8',database="douban")
    cursor=con.cursor()
    cursor.execute("select * from movie;")
    movie_data=cursor.fetchall()
    cursor.close()
    con.close()
    return render_template('movie.html',movies=movie_data)

@app.route("/team")
def team():
    return render_template('team.html')

@app.route("/word")
def word():
    return render_template('word.html')

@app.route("/score")
def score():
    scores=[]
    nums=[]
    con=pymysql.Connection(host="localhost",port=3306,password='mysql123',database='douban',user='root',charset='utf8')
    cursor=con.cursor()
    cursor.execute(" select pingfen, count(pingfen) from movie group by pingfen;")
    datas=cursor.fetchall()
    for i in datas:
        scores.append(i[0])
        nums.append(i[1])

    cursor.close()
    con.close()

    return render_template('score.html',pingfen=scores,num=nums)

if __name__ == '__main__':
    app.run(debug=True)
