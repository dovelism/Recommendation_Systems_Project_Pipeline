#!/usr/bin/env python
# -*- coding:utf-8 -*-


# @Time    : 2020/10/27 22:45
# @Author  : Dovelism
# @File    : LFM_recall.py

"""
1. 数据加载
2. 训练LFM
3. 预测
4. 推荐

"""
import sys
sys.path.append('..')
import operator
from tqdm import tqdm
from config.LFM_config import model_config
import numpy as np
from config import params
"""
1、数据加载
2、训练LFM
3、预测
4、推荐
"""


class LFM_model(object):
    def __init__(self, train_file):
        self.train_data = self.get_train_data(train_file)
        self.user_vec, self.item_vec = None, None

    def get_train_data(self, train_file):
        data = list()
        with open(train_file, mode='r', encoding='utf-8') as rf:
            for line in tqdm(rf.readlines()):
                userid, score, itemid = line.strip().split(',')
                data.append([userid, 1, itemid])
        return data

    def lfm_train(self):
        """
        训练LFM模型（算法）
        :return:
            dict: key itemid, value:np.ndarray
            dict: key userid, value:np.ndarray
        """
        F, alpth, beta, step = model_config['F'], model_config['alpha'], model_config['beta'], model_config['step']
        user_vec, item_vec = {}, {}
        for s in range(step):
            print("this is the {}th step".format(s + 1))
            for data_instance in tqdm(self.train_data):
                user_id, label, item_id = data_instance
                # print(item_id)
                if user_id not in user_vec:
                    user_vec[user_id] = np.random.randn(F)
                if item_id not in item_vec:
                    item_vec[item_id] = np.random.randn(F)
                delta = label - self.model_predict(user_vec[user_id], item_vec[item_id])
                # print(delta)

                user_vec[user_id] += beta * (delta * item_vec[item_id] - alpth * user_vec[user_id])
                item_vec[item_id] += beta * (delta * user_vec[user_id] - alpth * item_vec[item_id])

            beta = beta * 0.9

        self.user_vec, self.item_vec = user_vec, item_vec

    def model_predict(self, user_vector, item_vector):
        """
        计算user_vec 和 item_vec 的距离
        :param user_vector:
        :param item_vector:
        :return:
            距离
        """
        res = np.dot(user_vector, item_vector) / (np.linalg.norm(user_vector) * np.linalg.norm(item_vector))
        return res

    def cal_rec_item(self, user_id):
        """
            利用LFM模型结果计算推荐结果
        :param user_id:
        :return:
            [(item_id, score),(item_id, score),(item_id, score)]
        """
        fix_num = model_config['fix_num']
        if user_id not in self.user_vec:
            return []
        record = dict()
        rec_list = list()
        user_vector = self.user_vec[user_id]
        for itemid in self.item_vec:
            item_vector = self.item_vec[itemid]
            res = self.model_predict(user_vector, item_vector)
            # res = np.dot(user_vector, item_vector) / (np.linalg.norm(user_vector) * np.linalg.norm(item_vector))
            record[itemid] = res
        for items in sorted(record.items(), key=operator.itemgetter(1), reverse=True)[0:fix_num]:
            itemid = items[0]
            rec_list.append(itemid)

        return rec_list


if __name__ == '__main__':
    file = params.NEWS_SCORE
    lfm = LFM_model(file)
    lfm.lfm_train()
    print("start recommendation")
    rec_result = lfm.cal_rec_item('7')
    print(rec_result)