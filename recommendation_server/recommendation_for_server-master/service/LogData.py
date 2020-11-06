from dao import mongo_db
from datetime import datetime
from dao import redis_db

class LogData(object):
    def __init__(self):
        self._mongo = mongo_db.MongoDB(db='information')
        self.__redis = redis_db.Redis()

    def insert_log(self, user_id, content_id, title, tables):
        collections = self._mongo.db_loginfo[tables]
        info = {}
        info['user_id'] = user_id
        info['content_id'] = content_id
        info['title'] = title
        info['news_date'] = datetime.utcnow()
        collections.insert_one(info)
        return True


    def get_logs(self, user_id, tables):
        collections = self._mongo.db_loginfo[tables]
        data = collections.find(
            {"user_id": user_id}
        )
        results = []
        for x in data:
            results.append(x)

        return results


    def modify_article_detail(self, key ,ops):
        # 第一步：取数据 . set方式存的， 可以用get取
        try:
            detail = self.__redis.redis.get(key)
            #print(info)
            info = eval(detail) #转化成字典
            # 第二步：处理阅读、点赞、收藏
            info[ops] += 1
            # 第三步：写回redis数据库
            self.__redis.redis.set(key ,str(info))
            return True

        except Exception as e:
            print(e)
            return False




#
# if __name__ == '__main__':
#     log_data = LogData()
#     log_data.modify_article_detail("reads")
#     log_data.modify_article_detail("likes")
#     log_data.modify_article_detail("collections")



