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

# @Time    : 2020/10/19 12:47
# @Author  : Dovelism
# @File    : read_news_data.py
from dao.mongo_db import MongoDB
import os
class NewsData(object):
    def __init__(self):
        self.mongo = MongoDB(db='information')
        self.db_loginfo = self.mongo.db_loginfo
        self.likes_collection = self.db_loginfo['likes']
    """"
     # TODO
     点赞2分，收藏3分，阅读1分，同时存在两个加1分，同时存在加2分
    """
    def get_data(self):
        result = list()
        data = self.likes_collection.find()
        for info in data:
            result.append(str(info['user_id']) +',2,'+str(info['content_id']))
        print(result)
        self.to_csv(result,'../data/news_score/news_log.csv')

    def rec_users(self):  #有推荐列表的 也就是有使用记录的用户
        data = self.likes_collection.distinct('user_id')

    def to_csv(self,user_score_content,res_file):
        if not os.path.exists('../data/news_score'):
            os.mkdir('../data/news_score')
        with open(res_file,mode='w',encoding='utf-8') as wf:
            for info in user_score_content:
                wf.write(info + '\n')
        print(len(user_score_content))

if __name__ == '__main__':
    news_data = NewsData()
    news_data.get_data()

    