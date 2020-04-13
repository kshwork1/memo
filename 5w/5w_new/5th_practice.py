from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta


## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/memo', methods=['GET'])
def listing():
    # 1. 모든 document 찾기 & _id 값은 출력에서 제외하기
    articles = list(db.articles.find({},{'_id':0}))
    # 2. articles라는 키 값으로 영화정보 내려주기
    return jsonify({'result':'success', 'msg':'GET 연결되었습니다!', "articles" : articles})


@app.route('/memo', methods=['POST'])
def saving():
    # 1. 클라이언트로부터 데이터를 받기
    article_url = request.form['article_url']
    comment = request.form['comment']

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(article_url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    # 2. meta tag를 스크래핑하기

    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')

    print(og_image.get('content'))
    print(og_title.get('content'))
    print(og_description.get('content'))

    data = {
        'url' : article_url,
        'image' : og_image.get('content'),
        'title' : og_title.get('content'),
        'description' : og_description.get('content'),
        'comment' : comment
    }
    db.articles.insert_one(data)

    # 3. mongoDB에 데이터를 넣기
    return jsonify({'result': 'success', 'msg':'POST 연결되었습니다!'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)