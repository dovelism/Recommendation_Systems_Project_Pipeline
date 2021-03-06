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
# @Time    : 2020-11-05 19:56
# @Author  : Hongbo Huang
# @File    : read_data.py
from dao.mongo_db import MongoDB
from dao.mysql_db import Mysql
from sqlalchemy import distinct
from entity.content import Content
from entity.user import User
import pandas as pd

class ReadData(object):
    def __init__(self):
        self.engine = Mysql()
        self.session = self.engine._DBSession()
        self.mongo = MongoDB(db='loginfo')
        self.db_loginfo = self.mongo.collection_test
        self.like_collection = self.db_loginfo['likes']  #likes, read, favourite
        self.content_collection = self.db_loginfo['content_labels']  #likes, read, favourite


    def read_user_info_from_mysql(self):
        """
        (241, 'huxuzhe', '江苏省/苏州市', 'male', 'Hu_xz', '27')
        (242, 'huxuzhe1993', '江苏省/苏州市', 'male', 'hu_xz', '27')
        (243, '1', '天津市/天津市', 'male', '1', '1')
        (244, 'lujunhao', '河北省/石家庄市', 'male', 'ljh', '20')
        (245, 'hhb123', '河北省/唐山市', 'male', 'hhb', '25')
        (246, 'jay', '内蒙古自治区/兴安盟', 'male', '哈哈哈哈哈', '22')
        (247, 'root', 'beijing', '1', 'root', '15')
        (248, 'zjf', '江西省/赣州市', 'male', 'xiaozhuzhu', '23')
        """
        types = self.session.query(User.id, User.username, User.city, User.gender, User.nick, User.age).all()
        cnt = 0
        user_info = list()
        for info in types:
            user_info.append(info)
        user_info = pd.DataFrame(user_info, columns=['user_id', 'name_1', 'city', 'gender', 'name_2', 'age'])
        user_info.to_csv('./data/user_info.csv', index=False)

    """
    {'_id': ObjectId('5fa35b89321ccea257f2d860'), 'user_id': 245, 'content_id': '5f58bfa7298d4369c3109469', 'title': '国民党想参加“海峡论坛”遭陆委会阻挠 马英九回应', 'date': datetime.datetime(2020, 11, 5, 1, 55, 21, 770000)}
    {'_id': ObjectId('5fa35b89321ccea257f2d860'), 'user_id': 245, 'content_id': '5f58bfa7298d4369c3109469', 'title': '国民党想参加“海峡论坛”遭陆委会阻挠 马英九回应', 'date': datetime.datetime(2020, 11, 5, 1, 55, 21, 770000)}
    {'_id': ObjectId('5fa35b89321ccea257f2d860'), 'user_id': 245, 'content_id': '5f58bfa7298d4369c3109469', 'title': '国民党想参加“海峡论坛”遭陆委会阻挠 马英九回应', 'date': datetime.datetime(2020, 11, 5, 1, 55, 21, 770000)}
    {'_id': ObjectId('5fa35b89321ccea257f2d860'), 'user_id': 245, 'content_id': '5f58bfa7298d4369c3109469', 'title': '国民党想参加“海峡论坛”遭陆委会阻挠 马英九回应', 'date': datetime.datetime(2020, 11, 5, 1, 55, 21, 770000)}
    """
    def read_history_info_from_mongodb(self):
        data = self.mongo.collection_test.find()
        cnt = 0
        for info in data:
            print(info)
            break
            cnt += 1
        print(cnt)

    """
    {'_id': ObjectId('5fa359880574d6367aaf1aa4'), 'describe': '新浪娱乐讯 今日有网友晒出快本路透图，谢霆锋、白冰、霍汶希等人现身录制现场，并称白冰替代容祖儿录快本？新浪娱乐为此求证节目组，对方称“今天快本录制，白冰作为英皇艺人代表和谢霆锋一起给自家艺人助阵。”(责编：明侦探)', 'keywords': [['白冰', 1.2808679467392856], ['谢霆锋', 0.8154122144428572], ['录制', 0.6515395827757143], ['艺人', 0.5720738171535714], ['娱乐', 0.5391463039757143], ['容祖儿', 0.4964527732857143], ['节目组', 0.4716975168357143], ['责编', 0.4572166201178572], ['晒出', 0.42695598224642856], ['霍汶希', 0.42695598224642856]], 'word_num': 93, 'news_date': datetime.datetime(2020, 7, 21, 18, 24), 'hot_heat': 10000, 'type': 'zongyi', 'title': '白冰替代容祖儿录制《快本》？节目组这样回应', 'likes': 0, 'read': 0, 'collections': 0, 'create_time': datetime.datetime(2020, 11, 5, 1, 46, 48, 682000)}
    {'_id': ObjectId('5fa359880574d6367aaf1aa5'), 'describe': '新浪娱乐讯\xa0在《乘风破浪的姐姐》中，吴昕与黄圣依谈到面对节目播出后的观众反馈。黄圣依认为“你做什么都会有人说好，也会有人说不好。管他呢，做自己完了”，同时还表示自己不看这些消息，认为好的内容是自我催眠，负面内容会影响心情。吴昕表示大家都是人，再怎么不在乎，看到这些评价都不会开心，同时自己和弟弟达成了共识，有事的时候弟弟会收走自己的手机几天。对于姐姐们清醒的态度，网友们表示外界声音只是参考，希望姐姐们要加油做自己。(责编：明侦探)', 'keywords': [['吴昕', 0.4981153126208333], ['黄圣依', 0.4981153126208333], ['姐姐', 0.4155389812575], ['弟弟', 0.30087826942208334], ['责编', 0.26670969506875003], ['表示', 0.24457604160375002], ['收走', 0.23317973856041666], ['侦探', 0.21613160682083332], ['催眠', 0.21436999456875003], ['内容', 0.21392847395541667]], 'word_num': 191, 'news_date': datetime.datetime(2020, 7, 21, 17, 1), 'hot_heat': 10000, 'type': 'zongyi', 'title': '如何看待网友评价？吴昕黄圣依心态大不同', 'likes': 0, 'read': 0, 'collections': 0, 'create_time': datetime.datetime(2020, 11, 5, 1, 46, 48, 724000)}
    {'_id': ObjectId('5fa359880574d6367aaf1aa6'), 'describe': '新浪娱乐讯\xa0《定义》作为《乘风破浪的姐姐》的衍生专题访谈节目，姐姐们展现了更为真实的一面。在今天的《定义》访谈里，谈及被偷拍的经历，郁可唯称自己曾被狗仔偷拍到家里的照片，于是采取了“每天拉窗帘”的措施，因为长期晒不到太阳而缺钙。当主持人问到“你是在开玩笑吗？”，郁可唯称“很烦”、“不想被拍到”。姐姐的神回复也是高情商了，希望大家给艺人一些私人空间~(责编：明侦探)', 'keywords': [['郁可唯', 0.6130650001487179], ['偷拍', 0.5947739773846153], ['姐姐', 0.5114325923169231], ['访谈', 0.47419063086256413], ['定义', 0.36891360591641026], ['责编', 0.32825808623846153], ['情商', 0.3151599933205128], ['缺钙', 0.2771701332974359], ['拍到', 0.2738923545410256], ['侦探', 0.26600813147179486]], 'word_num': 152, 'news_date': datetime.datetime(2020, 7, 21, 16, 11), 'hot_heat': 10000, 'type': 'zongyi', 'title': '郁可唯拉窗帘为防偷拍 晒不到太阳导致缺钙', 'likes': 0, 'read': 0, 'collections': 0, 'create_time': datetime.datetime(2020, 11, 5, 1, 46, 48, 763000)}
    {'_id': ObjectId('5fa359880574d6367aaf1aa7'), 'describe': '新浪娱乐讯(责编：明侦探)', 'keywords': [['责编', 4.2673551211000005], ['侦探', 3.458105709133333], ['娱乐', 2.51601608522]], 'word_num': 10, 'news_date': datetime.datetime(2020, 7, 21, 14, 32), 'hot_heat': 10000, 'type': 'zongyi', 'title': '《不止冠军》定档722 聚焦女排运动员的B面人生', 'likes': 0, 'read': 0, 'collections': 0, 'create_time': datetime.datetime(2020, 11, 5, 1, 46, 48, 795000)}
    {'_id': ObjectId('5fa359880574d6367aaf1aa8'), 'describe': '新浪娱乐讯 据韩媒报道，罗PD新综艺《暑假》被质疑抄袭日本游戏《我的暑假》。随后节目组否认了抄袭质疑，称完全不知道该游戏，更不存在参考，只是在寻找房子的时候，找了这个村子最古老的房子，却忽略了装修问题，“很抱歉给观众带来不舒服的感觉，是我们不够细心。我们将以观众提出的意见，在进行第二次拍摄前重新修改装潢。”(责编：小5)', 'keywords': [['抄袭', 0.5492074604842105], ['观众', 0.3871225258757895], ['质疑', 0.37318606325578946], ['节目组', 0.34756659135263157], ['责编', 0.3368964569289474], ['房子', 0.3324160302294737], ['罗新', 0.31459914481315787], ['该游戏', 0.2883220703368421], ['综艺', 0.28217431109473684], ['装潢', 0.2603511701773684]], 'word_num': 136, 'news_date': datetime.datetime(2020, 7, 20, 22, 0), 'hot_heat': 10000, 'type': 'zongyi', 'title': '罗英锡否认新节目《暑假》抄袭日本游戏', 'likes': 0, 'read': 0, 'collections': 0, 'create_time': datetime.datetime(2020, 11, 5, 1, 46, 48, 830000)}
    {'_id': ObjectId('5fa359880574d6367aaf1aa9'), 'describe': '新浪娱乐讯 2020年疫情下直播带货异军突起，造就了薇娅、辛巴等头部主播带货顶流。直播电商的爆发式增长带来电商主播人才的巨大市场需求，广州、杭州等各地纷纷出台相关扶持政策，重点培养电商直播人才。为了给年轻主播搭建开放，培养、选拔明星主播，为行业注入新的活力，由北京场景互娱传媒科技有限公司、浙江蓝象传媒有限公司联合出品，腾讯视频平台独家播出的《爆款星主播》已全面开启海选。《爆款星主播》作为国内首档聚焦直播电商生态的职场真人秀网络综艺节目，致力于让所有怀揣主播梦想的人，展现自己独特的带货方式。同时，节目邀请到业内带货顶流、圈内明星和全行业品牌主一起进行点评和研判，深挖直播行业痛点，揭示带货主播行业的争议和内幕。根据节目组云海选的要求，只要参赛者年满18岁，不限男女均有资格报名参加选拔，通过海选的主播可参与《爆款星主播》节目录制。《爆款星主播》作为一个带货主播真人秀节目，获得了全行业海量品牌主的底价支持。品牌作为节目中的隐形参与者，通过内容丰富、观赏性强的节目内容将主持人、明星、选手与品牌自然连接，借助节目中不同性格、形象的节目嘉宾达到品牌传播的目的，既加强了观众对品牌的认知和印象，又巧妙地与节目建立了新的互动方式。综艺真人秀节目已不是什么新鲜事，但“直播”概念的加入为节目注入了新鲜血液。通过多方位呈现主播特色，为年轻主播们搭建了一个个人IP独家打造的舞台，一次乘风破浪C位出道的捷径，明星大咖、带货顶流、来自电商、游戏、二次元等各个圈层主播的加入为节目内容增加了精彩看点，更充满了无限想象力。(责编：明侦探)', 'keywords': [['主播', 0.5007232461947644], ['节目', 0.43450403091141365], ['电商', 0.32176020260471205], ['直播', 0.2860173960119372], ['爆款', 0.2503616230973822], ['星主', 0.22637979473507855], ['真人秀', 0.19305612156282725], ['品牌', 0.18959653500910995], ['货顶', 0.18777121732303664], ['明星', 0.1410671680251309]], 'word_num': 590, 'news_date': datetime.datetime(2020, 7, 20, 18, 20), 'hot_heat': 10000, 'type': 'zongyi', 'title': '《爆款星主播》开启海选，寻找全民“薇娅辛巴”', 'likes': 0, 'read': 0, 'collections': 0, 'create_time': datetime.datetime(2020, 11, 5, 1, 46, 48, 891000)}
    {'_id': ObjectId('5fa359880574d6367aaf1aaa'), 'describe': '新浪娱乐讯 7月20日，新一期播出的中阿kenn老师为了激发伊能静跳宅舞的可爱感，让张含韵扮演她的女儿唱《冰雪奇缘》中“一起堆雪人”的可爱歌曲。下午，伊能静在微博晒出一张自己与小黄鸭的对比照以及张含韵举着猫咪图片的自拍，并发文：“韵宝~你给我做的小鸭子~~~好可爱~~我们不去玩雪人，一起去玩鸭子和猫猫吧！！！” 照片中伊能静的五官和表情神似小黄鸭，而张含韵的大眼睛也与呆萌的猫咪非常相像。20日晚间，张含韵转发了伊能静的发文，并表示：“一张拼图5块，但是给静姐免费！这样姐夫能不带我去爬山了吗？”网友纷纷评论道：“好可爱鸭哈哈哈”“韵韵子的大眼睛太像猫咪了！”两个小姐姐都好好看”(责编：麦子七)', 'keywords': [['伊能静', 0.8209436056067797], ['张含韵', 0.8104927120610169], ['猫咪', 0.7068141178983051], ['可爱', 0.5165024342427119], ['黄鸭', 0.40524635603050846], ['发文', 0.2596086232718644], ['小鸭子', 0.2356047059661017], ['自拍', 0.2169841587], ['责编', 0.2169841587], ['小姐姐', 0.21210819137118644]], 'word_num': 245, 'news_date': datetime.datetime(2020, 7, 20, 18, 9), 'hot_heat': 10000, 'type': 'zongyi', 'title': '伊能静分享与小黄鸭神似对比照 表白张含韵像猫咪', 'likes': 0, 'read': 0, 'collections': 0, 'create_time': datetime.datetime(2020, 11, 5, 1, 46, 48, 944000)}

    """
    def read_content_label(self):
        content_info = list()
        cnt = 0
        for info in self.mongo.content_labels.find():
            content_info.append([str(info['_id']), info['type'], info['title']])
        content_info = pd.DataFrame(content_info, columns=['content_id', 'type', 'title'])
        content_info.to_csv("./data/content_info.csv", index=False)

if __name__ == '__main__':
    read_data = ReadData()
    read_data.read_user_info_from_mysql()
    # read_data.read_history_info_from_mongodb()
    read_data.read_content_label()