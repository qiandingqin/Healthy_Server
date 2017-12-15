# coding=utf-8
# -*- coding: utf-8 -*-
from flask import Blueprint, request, g, render_template, session, redirect, url_for, jsonify
from conf.config import appID,appsecret, users, dietetic_daily, comprehensive_daily, recipes
from app.auth import requery_auth
from urllib import urlencode
import requests, bson, os, urllib, httplib, json, time
model = Blueprint('index', __name__)

@model.route('/')
def put_code():
    uri = urlencode({"url": "http://www.dnanren.cn/indexs"})
    url_tpl = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=" + str(appID) + "&redirect_uri=" + uri[4:-1] + "&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect"
    return "<script>window.location.href='"+url_tpl+"'</script>"

@model.route("/index")
def index():
    code = request.args.get('code')
    token_url = requests.get("https://api.weixin.qq.com/sns/oauth2/access_token?appid="+appID+"&secret="+appsecret+"&code="+code+"&grant_type=authorization_code");
    json_lode = json.loads(token_url.content)
    openid = json_lode["openid"]
    access_token = json_lode["access_token"]
    if openid:
        user_data = users.find_one({"oauth.open_id": openid})
        if user_data == None:
            user_info = requests.get("https://api.weixin.qq.com/sns/userinfo?access_token=" + access_token + "&openid=" + openid + "&lang=zh_CN")
            json_user_info = json.loads(user_info.content)
            object_id = bson.objectid.ObjectId().__str__()
            # 用户数据
            data = {
                "_id": object_id,
                "account": "",
                "password": "",
                "type": int(0),
                "name": json_user_info["nickname"],
                "oauth": [{
                    "open_id": str(openid),
                    "name": json_user_info["nickname"],
                    "avatar": str(json_user_info["headimgurl"]),
                    "sex": int(json_user_info["sex"]),
                }],
                "phone": "",
                "avatar": str(json_user_info["headimgurl"]),
                "sex": int(json_user_info["sex"]),
                "apply_weight": float(0),
                "age": int(0),
                "height": int(0),
                "weight": float(0),
                "sport": "",
                "apply_status": int(2),
                "assessment": "",
                "diet_timed": int(0),
                "is_report": int(0),
                "status": int(0),
                "online": int(1),
                "address": "",
                "times": {
                    "timed": int(time.time()),
                    "logined": int(time.time()),
                    "stoped": int(0),
                    "stop_elapse": int(0),
                },
            }
            set_data = users.insert_one(data)
            if set_data.inserted_id:
                session["user_id"] = set_data.inserted_id
                return "普通用户页面"
        else:
            type = user_data["type"]
            session["user_id"] = user_data["_id"]
            if int(type) == 0:
                return "普通用户页面"
            elif int(type) == 1:
                return "商家页面"



@model.route("/uploads")
def uploads():
    return render_template("upload.html")

@model.route("/admin_files")
# @requery_auth
def admin_files():
    abpath = os.path.abspath('/upload/')
    aaa = request.files.getlist("file")
    for upload in request.files.getlist("file"):
        file_name = upload.filename.rsplit("/")[0]
        destination = "/".join([abpath, file_name])
        upload.save(destination)
        result = (file_name, destination)
    return jsonify({"code": 0, "filename": "%s" % result})



