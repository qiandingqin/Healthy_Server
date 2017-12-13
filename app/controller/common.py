# coding=utf-8
# -*- coding: utf-8 -*-

from flask import Blueprint, request, g, render_template, session, redirect, url_for
from conf.config import appID,appsecret
import requests, time, json, hashlib

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

