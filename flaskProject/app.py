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
    return render_template('score.html')

if __name__ == '__main__':
    app.run(debug=True)
