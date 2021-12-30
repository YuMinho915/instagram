from flask import Flask, render_template, request, jsonify
from requests.api import post
from datetime import datetime
app = Flask(__name__)
import requests
import certifi
from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.u0c0t.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=certifi.where())
db = client.dbinstagram

@app.route('/')
def index():
    return render_template('instagram.html')

# 구현정 댓글 작업 중==============================================================
# 댓글 달기
@app.route("/comment", methods=["GET"])
def comment_get():
    comment_list = list(db.comment.find({},{'_id':False}))
    return jsonify({'comment':comment_list,'msg': 'GET 연결 완료!'})


# 댓글 user 정보랑 저장.
@app.route("/comment", methods=["POST"])
def insta_comment():
    # user_name_receive = request.form['user_name_give']
    # post_num_receive = request.form['post_num_give']
    comment_receive = request.form['comment_give']

    doc = {
        'comment': comment_receive
    }

    db.comment.insert_one(doc)

    return jsonify({'msg': 'POST /comment/ 저장'})






if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)