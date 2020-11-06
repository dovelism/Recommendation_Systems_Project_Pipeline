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

# @Time    : 2020/10/14 19:10
# @Author  : Dovelism
# @File    : sched_rec_news.py
from read_data import read_news_data
from models.recall import item_based_CF
class SchedRecNews(object):
    def __init__(self):
        self.news_data = read_news_data.NewsData()


    def schedule_job(self):
        # 1.计算得分 2.训练模型 3.推荐 4.把推荐的结果存入数据库
        # 1.计算得分。首先要知道给谁计算得分，i.e.也就是说要知道推荐用户的列表。分成冷启动用户和有推荐列表的。
        # 暂时可以认为是有阅读记录的人才会有推荐列表。所以第一步就是找到有阅读记录的人
        user_list = self.news_data.rec_users()


    def cal_score(self,user_set):
        return

    def rec_list(self,user_id):
        # 把用于传进来，然后调用模型预测这个用户的推荐列表
        return

    def to_redis(self,user_id,rec_content_score):
        return



