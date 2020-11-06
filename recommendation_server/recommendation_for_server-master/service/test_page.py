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
# @Time    : 2020-08-23 10:05
# @File    : test_page.py
import sys
sys.path.append('..')
from dao import redis_db
import json

class PageSize(object):
    def __init__(self):
        self._redis = redis_db.Redis()

    def get_data_with_page(self, page, page_size):
        #1   1~10
        #2   11~20
        #3   21~30
        start = (page - 1) * page_size
        end = start + page_size
        data = self._redis.redis.zrange("rec_list", start, end)
        lst = list()
        for x in data:
            info = self._redis.redis.get("news_detail:" + x)
            lst.append(info)
        return lst


if __name__ == '__main__':
    page_size = PageSize()
    print(page_size.get_data_with_page(1, 20))

