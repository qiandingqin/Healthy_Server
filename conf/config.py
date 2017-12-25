# coding=utf-8

import os
import pymongo
basedir = os.path.abspath(os.path.dirname(__file__))

# 静态文件和模板
template_path = os.path.join(os.path.dirname(__file__), "templates")
static_path = os.path.join(os.path.dirname(__file__), "static")

# 连接数据库
client = pymongo.MongoClient('192.168.6.111', 27018)
DB = client.lose_weight
DB.authenticate("lose_weight", "lose_weight")
# 数据表部分
# 用户表
users = DB.users
# 饮食日报表
dietetic_daily = DB.dietetic_daily
# 综合日报表
comprehensive_daily = DB.comprehensive_daily
# 今日食谱表
recipes = DB.recipes


appID = "wxac1db4284d6b9a88"
appsecret = "173bb837a1b4b3c6696d27c0a781a34d"

SECRET_KEY = os.urandom(36)
DEBUG = True

