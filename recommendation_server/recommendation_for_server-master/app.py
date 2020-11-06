from flask import Flask, request, jsonify
import json
import hashlib
from dao.mysql_db import Mysql
from entity.user import User
app = Flask(__name__)
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from service.LogData import LogData
log_data = LogData()
from service.test_page import PageSize
page_query = PageSize()





app = Flask(__name__)


@app.route("/recommendation/get_rec_list", methods=['POST', 'GET'])  # 进行请求
def get_rec_list():
    if request.method == 'POST':
        req_json = request.get_data() # 请求的是json
        rec_obj = json.loads(req_json)
        page_size = rec_obj['page_size']
        page_num = rec_obj['page_num']
        user_id = rec_obj['user_id']
        types = rec_obj['types']

        try:
            #data = "page_size:" + page_size + ", page_num:" + page_num + ", user_id:" + user_id + ", types:" + types
            #data = page_data.get_data_with_page(page_num, page_size)
            data = page_query.get_data_with_page(page_num, page_size)
            print(data)
            #return jsonify({"code":0, "msg":"请求成功", "data":str(data)})
            return jsonify({"code": 0, "msg": "请求成功", "data": data, "user_id": user_id, "types": types})
        except Exception as e:
            print(str(e))  # 打印输出异常
            return jsonify({"code":2000, "msg":"error"})



@app.route("/recommendation/register", methods=['POST', 'GET'])
def register():  # 注册
    if request.method == 'POST':
        req_json = request.get_data()
        rec_obj = json.loads(req_json)
        user = User()
        user.username = rec_obj['username']
        user.nick = rec_obj['nick']
        user.age = rec_obj['age']
        user.gender = rec_obj['gender']
        user.city = rec_obj['city']
        user.password = str(hashlib.md5(rec_obj['password'].encode()).hexdigest())
    try:
        mysql = Mysql()
        sess = mysql._DBSession()
        if sess.query(User.id).filter(User.username == user.username).count() > 0:
            return jsonify({"code":1000, "msg":"用户已存在"})
        sess.add(user)
        sess.commit()
        sess.close()

        result = jsonify({"code":0, "msg":"注册成功"})
        return result



    except Exception as e:  #
        print(str(e))
        return jsonify({"code":2000, "msg":"error"})


@app.route("/recommendation/login", methods=['POST'])
def login():  # 登录
    if request.method == 'POST':
        req_json = request.get_data()
        rec_obj = json.loads(req_json)
        username = rec_obj['username']
        password = str(hashlib.md5(rec_obj['password'].encode()).hexdigest())
    try:
        mysql = Mysql()
        sess = mysql._DBSession()
        res = sess.query(User.id).filter(User.username == username, User.password == password)
        if res.count() > 0:  # 判断是否相同，如果相同 则 登录成功
            for x in res.all():
                data = {"user_id": str(x[0])}
                info = jsonify({"code": 0, "msg": "登录成功", "data":data})
                return info
        else:  # 如果不同，则提示用户名或密码错误
            return jsonify({"code": 1000, "msg": "用户名或密码错误"})
    except Exception as e:
        print(str(e))
        return jsonify({"code": 2000, "msg": "error"})



@app.route("/recommendation/likes", methods=['POST'])
def likes():  # 点赞
    if request.method == 'POST':
        req_json = request.get_data()
        rec_obj = json.loads(req_json)
        user_id = rec_obj['user_id']
        content_id = rec_obj['content_id']
        title = rec_obj['title']
    try:
        mysql = Mysql()
        sess = mysql._DBSession()
        if sess.query(User.id).filter(User.id == user_id).count() > 0:
            if log_data.insert_log(user_id, content_id, title, "likes") and log_data.modify_article_detail("news_detail:"+content_id, "likes"):
                return jsonify({"code": 0, "msg": "点赞成功"})
            else:
                return jsonify({"code": 1001, "msg": "点赞失败"})
        else:
            return jsonify({"code": 1000, "msg": "用户名不存在"})

    except Exception as e:
        return jsonify({"code": 2000, "msg": "error"})



@app.route("/recommendation/read", methods=['POST'])
def read():  # 阅读
    if request.method == 'POST':
        req_json = request.get_data()
        rec_obj = json.loads(req_json)
        user_id = rec_obj['user_id']
        content_id = rec_obj['content_id']
        title = rec_obj['title']
    try:
        mysql = Mysql()
        sess = mysql._DBSession()
        if sess.query(User.id).filter(User.id == user_id).count() > 0:
            if log_data.insert_log(user_id, content_id, title, "reads") and log_data.modify_article_detail("news_detail:"+content_id, "reads"):
                return jsonify({"code": 0, "msg": "阅读成功"})
            else:
                return jsonify({"code": 1001, "msg": "阅读失败"})
        else:
            return jsonify({"code": 1000, "msg": "用户名不存在"})

    except Exception as e:
        return jsonify({"code": 2000, "msg": "error"})



@app.route("/recommendation/collections", methods=['POST'])
def collections():  # 收藏
    if request.method == 'POST':
        req_json = request.get_data()
        rec_obj = json.loads(req_json)
        user_id = rec_obj['user_id']
        content_id = rec_obj['content_id']
        title = rec_obj['title']
    try:
        mysql = Mysql()
        sess = mysql._DBSession()
        if sess.query(User.id).filter(User.id == user_id).count() > 0:
            if log_data.insert_log(user_id, content_id, title, "collections") and log_data.modify_article_detail("news_detail:"+content_id, "collections"):
                return jsonify({"code": 0, "msg": "收藏成功"})
            else:
                return jsonify({"code": 1001, "msg": "收藏失败"})
        else:
            return jsonify({"code": 1000, "msg": "用户名不存在"})

    except Exception as e:
        return jsonify({"code": 2000, "msg": "error"})


@app.route("/recommendation/get_reads", methods=['POST'])
def get_reads():  # 获得阅读的列表
    if request.method == 'POST':
        req_json = request.get_data()
        rec_obj = json.loads(req_json)
        user_id = rec_obj['user_id']  # 传入用户id
    try:
        data = log_data.get_logs(user_id, 'reads')
        #print(data)
        return jsonify({"code": 0, "data": str(data)})

    except Exception as e:
        return jsonify({"code": 2000, "msg": "error"})

@app.route("/recommendation/get_likes", methods=['POST'])
def get_likes():  # 获得点赞的列表
    if request.method == 'POST':
        req_json = request.get_data()
        rec_obj = json.loads(req_json)
        user_id = rec_obj['user_id']  # 传入用户id
    try:
        data = log_data.get_logs(user_id, 'likes')
        #print(data)
        return jsonify({"code": 0, "data": str(data)})

    except Exception as e:
        return jsonify({"code": 2000, "msg": "error"})


@app.route("/recommendation/get_collections", methods=['POST'])
def get_collections():  # 获得收藏的列表
    if request.method == 'POST':
        req_json = request.get_data()
        rec_obj = json.loads(req_json)
        user_id = rec_obj['user_id']
    try:
        data = log_data.get_logs(user_id, 'collections')
        print(data)

        return jsonify({"code": 0, "data": str(data)})

    except Exception as e:
        print(e)
        return jsonify({"code": 2000, "msg": "error"})



if __name__ == '__main__':  # 用main函数进行启动
    app.run(debug=True, host='0.0.0.0', port=2222, threaded=True)