import os
import jieba
import jieba.posseg as pseg
import re
import jieba.analyse


class Segment(object):
    def __init__(self, stopword_files=[], userdict_files=[], jieba_tmp_dir=None):
        if jieba_tmp_dir:
            jieba.dt.tmp_dir = jieba_tmp_dir
            if not os.path.exists(jieba_tmp_dir):
                os.makedirs(jieba_tmp_dir)

        self.stopwords = set()
        for stopword_file in stopword_files:
            with open(stopword_file, "r", encoding="utf-8") as rf:
                for row in rf.readlines():
                    word = row.strip()
                    if len(word) > 0:
                        self.stopwords.add(word)

        for userdict in userdict_files:
            jieba.load_userdict(userdict)

    def cut(self, text):
        word_list = []
        text.replace('\n', '').replace('\u3000', '').replace('\u00A0', '')
        text = re.sub('[a-zA-Z0-9.。:：,，]', '', text)
        words = pseg.cut(text)

        for word in words:
            print(word.word, word.flag)
            word = word.strip()
            if word in self.stopwords or len(word) == 0:
                continue
            word_list.append(word)

        return word_list

    def extract_keyword(self,text,use_pos = True,algorithm='joint_union'):
        text = re.sub('[a-zA-Z0-9.。,，:：]','',text)
        if use_pos:
            allow_pos = ('n','nr','nz','ns','vn','v')
        else:
            allow_pos = ()

        if algorithm == 'tfidf':
            TFIDF_keywords = jieba.analyse.extract_tags(text,withWeight=False)
            print(type(TFIDF_keywords))
            print(len(TFIDF_keywords))
            return TFIDF_keywords

        elif algorithm == 'textrank':
            TR_keywords = jieba.analyse.textrank(text,withWeight=False,allowPOS=allow_pos)
            print(type(TR_keywords))
            print(len(TR_keywords))
            return TR_keywords

        elif algorithm == 'joint_intersection': # 取交集
            Joint_keywords1 =[]
            TFIDF_keywords = jieba.analyse.extract_tags(text, withWeight=False)
            TR_keywords = jieba.analyse.textrank(text,withWeight=False,allowPOS=allow_pos)

            # 暴力取交集
            # for word in TFIDF_keywords:
            #     if word in TR_keywords:
            #         Joint_keywords1.append(word)

            # 精致取交集
            Joint_keywords1= list(set(TFIDF_keywords) & set(TR_keywords))
            print(type(Joint_keywords1))
            print(len(Joint_keywords1))
            return Joint_keywords1

        elif algorithm == 'joint_union': # topK个关键词取并集

            TFIDF_keywords = jieba.analyse.extract_tags(text, withWeight=False)[:6]
            TR_keywords = jieba.analyse.textrank(text,withWeight=False,allowPOS=allow_pos)[:6]

            # 这里并集也有两种写法
            #Joint_keywords2 = list(set(TFIDF_keywords+TR_keywords))
            Joint_keywords2 = list(set(TFIDF_keywords) | set(TR_keywords))
            print(type(Joint_keywords2))
            print(len(Joint_keywords2))
            return Joint_keywords2

'''
if __name__ == '__main__':
    seg = Segment(stopword_files=[], userdict_files=[])
    text = "孙新军介绍，北京的垃圾处理能力相对比较宽松，全市有44座处理设施，总设计能力是每天处理3.2万吨，焚烧场11座，处理能力是1.67万吨每天，生化设施23座，日处理能力达8130吨，包括餐饮单位厨余垃圾日处理能力2380吨，家庭厨余垃圾日处理能力5750吨。"
    textrank = seg.extract_keyword(text,algorithm='textrank', use_pos=True)[:10]
    tfidfs = seg.extract_keyword(text,algorithm='tfidf', use_pos=True)[:10]
    print(textrank)
    print(tfidfs)
    print(set(textrank) & set(tfidfs))
'''