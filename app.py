import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import re

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'YESMYNAMEDONGWOO'

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.izgwz.mongodb.net/cluster0?retryWrites=true&w=majority')
db = client.dbinsta


#################################
##  HTML을 주는 부분             ##
#################################
# 방식1 : DB에는 파일 이름만 넣어놓고, 이미지 자체는 서버 컴퓨터에 저장하는 방식
@app.route('/fileupload', methods=['POST'])
def file_upload():
    title_receive = request.form['title_give']
    file = request.files['file_give']
    # 해당 파일에서 확장자명만 추출
    extension = file.filename.split('.')[-1]
    # 파일 이름이 중복되면 안되므로, 지금 시간을 해당 파일 이름으로 만들어서 중복이 되지 않게 함!
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'{title_receive}-{mytime}'
    # 파일 저장 경로 설정 (파일은 db가 아니라, 서버 컴퓨터 자체에 저장됨)
    save_to = f'static/sajin/{filename}.{extension}'
    # 파일 저장!

    file.save(save_to)
    img = f'../static/sajin/{filename}.{extension}'


    # 아래와 같이 입력하면 db에 추가 가능!
    token_receive = request.cookies.get('mytoken')

    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    email_id = payload['id']
    doc = {'email_id':email_id,'title': title_receive, 'img': img}
    db.camp.insert_one(doc)

    return jsonify({'result': 'success'})


@app.route('/mypage')
def mypage():

    feeds = list(db.camp.find({}))

    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    email_id = payload['id']
    nicknames_search = db.users.find_one({'email':email_id})

    return render_template('mypage_.html',feeds =feeds, nicknames_search = nicknames_search)


# 구현정 댓글 작업================================================================
# 댓글 달기
@app.route("/comment", methods=["GET"])
def comment_get():
    comment_list = list(db.comment.find({}, {'_id': False}))
    return jsonify({'comment': comment_list, 'msg': 'GET 연결 완료!'})


# 댓글 user 정보랑 저장.
@app.route("/comment", methods=["POST"])
def insta_comment():
    # user_name_receive = request.form['user_name_give']
    # post_num_receive = request.form['post_num_give']
    comment_receive = request.form['comment_give']
    doc = {
        'comment': comment_receive
        # 'post_num' : post_num_receive
    }
    db.comment.insert_one(doc)
    return jsonify({'msg': 'POST /comment/ 저장'})



# 로그인 작업     (김동우)==============================================================
# 아이디 정규표현식
# 아이디 중복확인
def is_email(email1):
    find_id = db.users.find_one({"email": email1}, {"email": True, '_id': False}, )
    if re.search('[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', email1) is None:  # 이메일형식 적합성 검사
        return "이매일 형식을 확인하세요"
    elif find_id is not None:
        return "이미 사용중인 이메일 입니다"
    else:
        print('아이디 적합')
        return True



# 비밀번호 정규표현식
def is_password(pwd):
    special_char = ['!', '@', '#', '_', '*', '.']
    if len(pwd) < 8 or len(pwd) > 21:  # 비밀번호 8자 이상 20자 이하
        return False
    elif re.search('[0-9]+', pwd) is None:  # 최소 1개이상 숫자
        return False
    elif re.search('[a-z A-Z]+', pwd) is None:  # 최소 1개이상 영문자
        return False
    elif not any(c in special_char for c in pwd):  # 최소 1개이상 특수문자
        return False
    else:
        print('비밀번호 적합')
        return True



#################  api 하는곳 (김동우)################################################################
@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    feeds = list(db.camp.find({}))
    print(feeds)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        email_id = payload['id']
        nicknames_search = db.users.find_one({'email': email_id})
        return render_template('instagram.html',feeds=feeds,nicknames_search=nicknames_search)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))



# 회원가입
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email_receive = request.form['email_give']
        name_receive = request.form['name_give']
        nickname_receive = request.form['nickname_give']
        password_receive = request.form['password_give']
        password_hash = hashlib.sha256(
            password_receive.encode('utf-8')).hexdigest()
        # 정규표헌식 예외처리
        email_check = is_email(email_receive)
        if email_check != True:
            return jsonify({'msg': email_check})
        if is_password(password_receive) == False:
            return jsonify({'msg': '영어와 숫자 특수문자를 혼합하여 8자 이상 비밀번호를 만들어주세요 '})
        doc = {"email": email_receive,
               "name": name_receive,
               "nickname": nickname_receive,
               "password": password_hash
               }
        # db.camp.insert_one({"email": email_receive})
        print(email_receive,password_receive)
        db.users.insert_one(doc)
        return jsonify({'result': 'success', 'msg': '회원가입 완료'})



# 로그인 기능 구현
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email_give']
        password = request.form['password_give']
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        result = db.users.find_one({'email': email, 'password': password_hash})

        if result is not None:
            payload = {
                'id': email,
                'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return jsonify({'result': 'success', 'token': token})
        # 찾지 못하면
        else:
            return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})





# # mypage에서 main으로 이동시켜주는 def
# @app.route('/')
# def instagram():
#     return render_template("instagram.html")


# 게시물 올리기로 이동
@app.route('/post')
def post():
    return render_template("post.html")


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)