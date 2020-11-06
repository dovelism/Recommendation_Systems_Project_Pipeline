#!/usr/bin/env python 
# -*- coding: utf-8 -*-
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
# @Time    : 2020-08-22 11:18
# @Author  : Dovelism
# @File    : simple_rec.py
from dao import redis_db
from dao.mongo_db import MongoDB


class SimpleRecList(object):
    def __init__(self):
        self._redis = redis_db.Redis()
        self.mongo = MongoDB(db='information')
        self.db_loginfo = self.mongo.db_loginfo
        self.collection = self.db_loginfo['content_labels']

    def get_news_order_by_time(self):
        data = self.collection.find().sort([{"$news_date", -1}])
        count = 10000

        for news in data:
            self._redis.redis.zadd("rec_list", {str(news['_id']): count})
            count -= 1
            #if count % 10 == 0:
                #print(count)


if __name__ == '__main__':
    simple = SimpleRecList()
    simple.get_news_order_by_time()