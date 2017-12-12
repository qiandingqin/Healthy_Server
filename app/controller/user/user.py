# coding=utf-8
# -*- coding: utf-8 -*-
from flask import Blueprint, request, session, g, render_template
model = Blueprint('user', __name__)

#客户端用户列表
@model.route("/user_list")
def user_list():
    return "qqqq"

#客户端用户订单列表
@model.route("/user_order_list")
def user_order_list():
    return render_template("user/user_order_list.html")

#客户端用户订单详情
@model.route("/order_info")
def order_info():
    return render_template("user/order_info.html")


#客户端用户详细信息
@model.route("/user_info")
def user_info():
    return render_template("user/user_info.html")

#客户端用户状态标记view
@model.route("/mark")
def mark():
    return '1'

#提交状态标记
@model.route("/submit_mark")
def submit_mark():
    return '1'


#所有用户订单列表
@model.route('/all_order_list')
def all_order_list():
    return render_template('user/user_order_list.html')

#订单明细
@model.route('/orderinfo')
def orderinfo():
    return render_template('user/order_info.html')