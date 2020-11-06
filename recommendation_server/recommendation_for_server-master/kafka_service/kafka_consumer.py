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

# @Time    : 2020/9/14 19:35
# @Author  : Dovelism
# @File    : kafka_consumer.py

from kafka import KafkaConsumer
from kafka.structs import TopicPartition
import time
class Consumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
            group_id="test",
            auto_offset_reset="earliest",
            enable_auto_commit=False,
            bootstrap_servers=["localhost:9092"]
        )

    def consumer_data(self,topic,partition):
        my_partition = TopicPartition(topic=topic,partition=partition)
        self.consumer.assign([my_partition])

        print(f"consumer start position:{self.consumer.position(my_partition)}")
        try:
            while True:
                poll_num = self.consumer.poll(timeout_ms=1000,max_records=5)
                if poll_num == {}:
                    print("empty")
                    exit(1)
                for key,record in poll_num.items():
                    for message in record:
                        print(
                            f"{message.topic}:{message.partition}:{message.offset}:key={message.key}:value={message.value}"
                        )
                try:
                    self.consumer.commit_async()
                    time.sleep(2)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

        finally:
            try:
                self.consumer.commit()
            finally:
                self.consumer.close()

def main():
    topic = "recommendation"
    partition = 0
    my_consumer =Consumer()
    my_consumer.consumer_data(topic,partition)



if __name__ == '__main__':
    main()

    