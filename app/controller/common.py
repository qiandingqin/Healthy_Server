# coding=utf-8
# -*- coding: utf-8 -*-

from flask import Blueprint, request, g, render_template, session, redirect, url_for
from conf.config import appID,appsecret
import requests, time, json, hashlib
from flask import jsonify, json, request, current_app, make_response
import datetime, time

def ticket():
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

def timestamp(date=None):
    if date is None:
        date = datetime.datetime.now()
    t = time.mktime(date.timetuple())
    return long(t)


def apiresult(obj=None, code=0, **kwargs):
    t = timestamp()
    result = isinstance(obj, dict) and obj or {}
    for k in kwargs:
        result[k] = kwargs[k]
    return jsonify(code=code, timestamp=t, result=result)


def abort(code, msg=None):
    if code == 10000 and not msg:
        msg = '请求的参数错误'
    # raise ApiException(code, msg)

def item_count(def_val=10, max_val=50):
    count = request.values.get('item_count')
    if count:
        try:
            count = int(count)
        except:
            count = 0
        count = count <= 0 and def_val or (count >= max_val and max_val or count)
    else:
        count = def_val
    return count

def next_start(def_val= 0):
    page = request.values.get("next_start")
    if page:
        try:
            page = int(page)
        except:
            page = 0
    else:
        page = def_val
    return page*item_count()

def findAll(find_all, code=1):
    data = []
    for finds in find_all:
        data.append(finds)
    datas = {
        "code": code,
        "result": data
    }
    return jsonify(datas)

def find(find,code=0):
    datas = {
        "code": code,
        "result": find
    }
    return jsonify(datas)

