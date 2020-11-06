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

# @Time    : 2020/9/14 19:16
# @Author  : Dovelism
# @File    : kafka_producer.py
 

from kafka import KafkaProducer
from kafka.errors import KafkaError

def main():
    # 这里传列表形式，因为多机我们还可以传其他的地址，但是因为是本地所以此时只有一个
    producer = KafkaProducer(bootstrap_servers = ["localhost:9092"])

    for i in range(100):
        future = producer.send("recommendation",b"msg")
        try:
            record_metadata = future.get(timeout=10)
            print(record_metadata)
        except KafkaError as e:
            print(e)

if __name__ == '__main__':
    main()
