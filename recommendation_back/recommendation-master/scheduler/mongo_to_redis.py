#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020-08-22 10:57
# @File    : mongo_to_redis.py

import pymongo
from dao import redis_db
from dao.mongo_db import MongoDB


class write_to_redis(object):
    def __init__(self):
        self._redis = redis_db.Redis()
        self.mongo = MongoDB(db='information')
        self.db_loginfo = self.mongo.db_loginfo
        self.collection = self.db_loginfo['content_labels']

    def get_from_mongoDB(self):
        pipelines = [{
            '$group':{
                '_id': "$type"
            }
        }]

        types = self.collection.aggregate(pipelines)
        count = 0
        for type in types:
            cx = {"type": type['_id']}
            data = self.collection.find(cx)
            for info in data:
                result = dict()
                result['title'] = str(info['title'])
                result['describe'] = str(info['describe'])
                result['type'] = str(info['type'])
                result['news_date'] = str(info['news_date'])
                result['content_id'] = str(info['_id'])
                result['likes'] = info['likes']
                result['reads'] = info['reads']
                result['hot_heat'] = info['hot_heat']
                result['collections'] = info['collections']
                print(result)
                # self._redis.redis.delete(str(info['_id']))
                self._redis.redis.set("news_detail:"+str(info['_id']), str(result))



if __name__ == '__main__':
    write_to_redis = write_to_redis()
    write_to_redis.get_from_mongoDB()
