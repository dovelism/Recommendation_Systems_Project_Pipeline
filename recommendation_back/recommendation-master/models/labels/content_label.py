#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from datetime import datetime
from dao.mongo_db import MongoDB
from dao.mysql_db import Mysql
from models.keywords.extract_keyword import Segment
from sqlalchemy import distinct
from models.labels.entity.content import Content

class ContentLabel(object):
    def __init__(self):
        self.seg = Segment(stopword_files=[], userdict_files=[])
        self.engine = Mysql()
        self.session = self.engine._DBSession()
        self.mongo = MongoDB(db='information')
        self.db_loginfo = self.mongo.db_loginfo
        self.collection = self.db_loginfo['content_labels']


    def get_data_from_mysql(self):
        types = self.session.query(distinct(Content.type))
        for i in types:
            #print(i[0])
            res = self.session.query(Content).filter(Content.type == i[0])
            if res.count() > 0:
                for x in res.all():
                    keywords = self.get_keywords(x.desc, 10)
                    word_nums = self.get_words_nums(x.desc)
                    times = x.times
                    create_time = datetime.utcnow()
                    content_collection = dict()
                    content_collection['describe'] = x.desc
                    content_collection['keywords'] = keywords
                    content_collection['word_num'] = word_nums
                    content_collection['news_date'] = times
                    content_collection['hot_heat'] = 10000
                    content_collection['type'] = x.type
                    content_collection['title'] = x.title
                    content_collection['likes'] = 0
                    content_collection['reads'] = 0
                    content_collection['collections'] = 0

                    content_collection['create_time'] = create_time
                    print(content_collection)
                    self.collection.insert_one(content_collection)

    def get_keywords(self, contents, nums=10):
        keywords = self.seg.extract_keyword(contents)[:nums]
        return keywords


    def get_words_nums(self, contents):
        ch = re.findall('([\u4e00-\u9fa5])', contents)
        nums = len(ch)
        return nums


if __name__ == '__main__':
    content_label = ContentLabel()
    content_label.get_data_from_mysql()