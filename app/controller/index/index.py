# coding=utf-8
# -*- coding: utf-8 -*-
from flask import Blueprint, request, session, g, render_template, session
model = Blueprint('index', __name__)
from conf.config import appID,appsecret
from app.auth import requery_auth
import requests
import urllib2
import httplib
import json
import hashlib
import time
@model.route('/')
def login():
    get_token = requests.get("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid="+appID+"&secret="+appsecret)
    json_load = json.loads(get_token.content)
    access_token = json_load['access_token']
    jsapi_ticket_url = requests.get("https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token="+access_token+"&type=jsapi")
    jsapi_ticket_arr = json.loads(jsapi_ticket_url.content)
    Unix_time = int(time.time())
    noncestr_sha1 = hashlib.sha1("string1").hexdigest()
    session["ticket"] = jsapi_ticket_arr["ticket"]
    str_key = "jsapi_ticket=" + str(jsapi_ticket_arr["ticket"]) + "&noncestr=" + str(noncestr_sha1) + "&timestamp=" + str(Unix_time) + "&url=http://www.dnanren.cn/"
    dict_str = {
        "appID": appID,
        "jsapiTicket": jsapi_ticket_arr["ticket"],
        "nonceStr": noncestr_sha1,
        "time": Unix_time,
        "signature": hashlib.sha1(str_key).hexdigest()
    }
    encode_json = json.dumps(dict_str)
    return encode_json

@model.route("/index")
def index():
    auth_url = requests.get("https://open.weixin.qq.com/connect/oauth2/authorize?appid="+appID+"&redirect_uri=health.ext.gzhxyc.com&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect")
    content_token = json.loads(auth_url.content)
    token = content_token['token']
@model.route("/admin")
@requery_auth
def admin():
    return "aaaa"



