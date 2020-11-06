#!/usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2020/10/29 17:33
# @Author  : Dovelism
# @File    : combine_recall.py

from models.recall.LFM_recall import LFM_model
from config import params
#from utilu import log_utils
import pickle
#logger = log_utils.logger
class CombineRecallTrain(object):

    def __init__(self):
        self.model_train()
        self.predict("7")
        self.save_to_redis()
    def model_train(self,model):
        """
        训练联合模型，hot_recall,itemCF 和 LFM
        """
        self.LFM_train()
        self.CF_train()
        self.NMF_train()


    def LFM_train(self):
        #logger.info("start train LFM model")

        news_model_train = LFM_model(params.NEWS_SCORE)
        news_model_train.lfm_train()

        #logger.info("end train LFM model")

        with open("LFMmodel.pkl",mode="wb") as news_f:
            pickle.dumps(news_model_train)


    def model_predict(self,user_id):
        news_model_train = LFM_model(params.NEWS_SCORE)
        news_model_train.lfm_train()
        result_recall = news_model_train.model_predict(user_id)
        return result_recall

    def save_to_redis(self):
        return


if __name__ == '__main__':
    cr = CombineRecallTrain()
    cr.LFM_train()



