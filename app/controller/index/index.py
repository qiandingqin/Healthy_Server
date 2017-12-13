# coding=utf-8
# -*- coding: utf-8 -*-
from flask import Blueprint, request, g, render_template, session, redirect, url_for
from conf.config import appID,appsecret
from app.auth import requery_auth
from urllib import urlencode
import requests
import urllib
import httplib
import json
import hashlib
import time
model = Blueprint('index', __name__)

@model.route('/')
def index():
    uri = urlencode({"url": "http://www.dnanren.cn/index"})
    url_tpl = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=" + str(appID) + "&redirect_uri=" + uri[4:-1] + "&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect"
    return "<script>window.location.href='"+url_tpl+"'</script>"

@model.route("/index")
def index():
    code = request.args.get('code')
    token_url = requests.get("https://api.weixin.qq.com/sns/oauth2/access_token?appid="+appID+"&secret="+appsecret+"&code="+code+"&grant_type=authorization_code");
    json_lode = json.loads(token_url.content)
    openid = json_lode["openid"]
    access_token = json_lode["access_token"]
    user_info = requests.get("https://api.weixin.qq.com/sns/userinfo?access_token="+access_token+"&openid="+openid+"&lang=zh_CN")
    json_user_info = json.loads(user_info.content)
    return json_user_info

@model.route("/admin")
@requery_auth
def admin():
    return "aaaa"



