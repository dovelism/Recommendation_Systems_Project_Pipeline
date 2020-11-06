#!/usr/bin/env python
# -*- coding:utf-8 -*-


# @Time    : 2020/10/14 18:49
# @Author  : Dovelism
# @File    : item_based_CF.py
import math
from tqdm import tqdm
# 基于item的CF算法部分
class Item_Based_CF(object):
    def __init__(self,train_file):
        self.train = dict()  #最后会形成一个很大的字典，用于存储score。好处是查询快，但是缺点是内存会爆掉。后期可以通过存入临时文件解决。
        self.user_item_history = dict()
        self.item_to_item = dict()
        self.item_count = dict()
        self.read_data(train_file)
    # step1:定义数据的读取部分
    def read_data(self,train_file):
        '''
        :param train_file: 读文件，并生成数据集（user，score，item）
        :return: {person_id:{content_id:predict_score}}
        '''
        with open(train_file, mode='r', encoding='utf-8') as rf:
            for line in tqdm(rf.readlines()):
                user,score,item = line.strip().split(",")
                self.train.setdefault(user,{})    # 如果读不到的话，设置一个默认
                self.user_item_history.setdefault(user,{})

                self.train[user][item] = int(score)
                self.user_item_history[user].append(item)


    # step2：定义训练协同过滤算法部分
    def cf_item_train(self):
        """
        基于item的CF,计算相似度
        :return:  相似度矩阵{content_id:{content_id:相似度得分}}
        """

        for user,items in self.train.items():  # 找item
            for i in items.keys:
                self.item_count.setdefault(i,{})
                self.item_count[i] +=1  # 每一个item出现一次就加1
                '''
                下面注释的这四行逻辑上需要，这样写没有错误，但是没必要。因为是对角阵。因此不写这个是第一步优化，计算量大幅度减小。
                '''
                #for j in user:
                    #if i == j :
                        #continue
                    #self.item_to_item[i][j] += 1
        for user,items in self.train.items():
            for i in items.keys:
                self.item_to_item.setdefault(i,{})
                for j in items.keys():
                    if i == j :
                        continue
                    self.item_to_item[i].setdefault(i,{})
                    self.item_to_item[i][j] += 1 / (math.sqrt(self.item_count[i] * self.item_count[j]))#共现一次就加1

        # 计算相似度矩阵
        for _item in self.item_to_item:
            self.item_to_item[_item] = dict(sorted(self.item_to_item[_item].items()),
                                            key=lambda x:x[1],reverse=True[:30])



    # step3:定义模型的保存
    def save_variable(self):
        return

    # step4:定义协同过滤的召回列表，并返回这个列表
    def cal_rec_item(self , user , N=10):

        """
        给user推荐前N个感兴趣的文章
        :param user
        :param N:取多少个物品推荐给用户
        :return: 所推荐出来的文章的列表
        """
        rank = dict()   # 记录user的推荐文章（没有历史行为的文章）和感兴趣程度
        try:
            action_item = self.train[user]
            for item,score in action_item.items():
                for j,wj in self.item_to_item[item].items():
                    if j in action_item.keys():  #如果文章j已经被阅读过，就去重不推荐
                        continue
                    rank.setdefault(j,0)
                    rank[j] += score * wj / 1000 # 如果文章j没有被阅读过，则累计文章j与item的相似度
            res = dict(sorted(rank.items(),key=lambda x:x[1],reverse=True)[0:N])
            return list(res)
        except:
            return {}





    