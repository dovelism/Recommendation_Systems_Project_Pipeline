#!/usr/bin/env python
# -*- coding:utf-8 -*-
#                       _oo0oo_
#                      o8888888o
#                      88" . "88
#                      (| -_- |)
#                      0\  =  /0
#                    ___/`---'\___
#                  .' \\|     |// '.
#                 / \\|||  :  |||// \
#                / _||||| -:- |||||- \
#               |   | \\\  -  /// |   |
#               | \_|  ''\---/''  |_/ |
#               \  .-\__  '-'  ___/-. /
#             ___'. .'  /--.--\  `. .'___
#          ."" '<  `.___\_<|>_/___.' >' "".
#         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#         \  \ `_.   \_ __\ /__ _/   .-` /  /
#     =====`-.____`.___ \_____/___.-`___.-'=====
#                       `=---='
#
#
#     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#               佛祖保佑         永无BUG
#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/8/17 16:42
# @Author  : Dovelism
# @File    : Mongo_DB.py
 


import pymongo
import datetime
import jieba

class MongoDB(object):
    def __init__(self,db):
        mongo_client = self._connect('localhost',27017,'','',db)
        self.db_loginfo = mongo_client['information']
        #self.collection_test = self.db_loginfo['test_colllections'  ]
        return

    def _connect(self,host,port,user,password,db):
        mongo_info = self._splicing(host ,port,user ,password,db)
        mongo_client = pymongo.MongoClient(mongo_info,connectTimeoutMS=12000,connect=False)  #connect=True 的时候，                                        # 每一次都会重连，当好多好多用户同时请求的时候就会耗时大。
        return mongo_client

    @staticmethod
    def _splicing(host,port,user,password,db):
        client = 'mongodb://' + host + ":" + str(port) + "/"
        if user != '':
            client = 'mongodb://' + user + ":" + password + "@" + host + ":" + str(port) + "/"

            if db != '':
                client += db
        return client
    # def test_insert(self):
    #     test = dict()
    #     test['name'] = 'user'
    #     test['job'] = 'programmer'
    #     test['dates'] = datetime.datetime.utcnow()
    #     self.collection_test.insert_one(test)


# if __name__ == '__main__':
#     mongo = MongoDB(db='test')
#     mongo.test_insert()