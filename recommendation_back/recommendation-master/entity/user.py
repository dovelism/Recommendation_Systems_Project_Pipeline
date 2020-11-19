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
# @Time    : 2020-11-05 20:01
# @File    : content.py

from sqlalchemy import Column,Integer,DateTime,Text
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from dao.mysql_db import Mysql

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer(), primary_key=True)
    username = Column(DateTime())
    nick = Column(Text())
    gender = Column(Text())
    age = Column(Text())
    city = Column(Text())

    def __init__(self):
        mysql = Mysql()
        engine = mysql.engine
        Base.metadata.create_all(engine)