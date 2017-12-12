# coding=utf-8

import os
import pymongo
basedir = os.path.abspath(os.path.dirname(__file__))

template_path = os.path.join(os.path.dirname(__file__), "templates")
static_path = os.path.join(os.path.dirname(__file__), "static")

client = pymongo.MongoClient('192.168.6.111', 27017)
DB = client.lose_weight
DB.authenticate("lose_weight", "lose_weight")

appID = "wxac1db4284d6b9a88"
appsecret = "173bb837a1b4b3c6696d27c0a781a34d"

SECRET_KEY = os.urandom(36)
DEBUG = True

