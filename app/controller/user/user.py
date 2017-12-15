# coding=utf-8
# -*- coding: utf-8 -*-
from flask import Blueprint, request, session, g, render_template,jsonify
from conf.config import appID,appsecret, users, dietetic_daily, comprehensive_daily, recipes, DB
import bson,time, json
from bson.json_util import dumps
from app.controller import common
from datetime import datetime
import os
model = Blueprint('user', __name__)

@model.route("/user/user_info/")
def user_info():
    """
       @api {GET} /user/user_info/ 01. 我的(会员用户)-信息
       @apiGroup U_用户_USER
       @apiVersion 1.0.0
       @apiSuccessExample {json} JSON.result 对象
       {
       }
    """
    try:
        # user_id = session["user_id"]
        user_id = str("5a30d3694aee3086ea6d7c29")
        find = users.find_one({"_id": user_id, "status": 0, "type": 0})
        return common.find(find=find)
    except BaseException:
        return common.find(code=-1)


@model.route("/user/today_recipes/")
def today_recipes():
    """
       @api {GET} /user/today_recipes/ 02. 我的-食谱列表
       @apiGroup U_用户_USER
       @apiVersion 1.0.0
       @apiPermission 访问授权
       @apiParam {str} next_start 分页起始ID 默认值: null
       @apiSuccessExample {json} JSON.result 对象
       {
         today_recipes:[
            {
                id: String # 食谱ID
                content: String # 食谱内容
                timed : Long 时间
            }
         ]
       }
    """
    if request.args.get('next_start'):
        next_start = int(request.args.get('next_start'))*10
    else:
        return "参数错误"
    # user_id = session["user_id"]
    user_id = "5a30d8954aee308711f1cfa2"
    find_all = recipes.find({"user_id": user_id or ""}).skip(next_start).limit(10)
    return common.findAll(find_all)



@model.route("/user/dietetic_daily_list/")
def dietetic_daily_list():
    """
       @api {GET} /user/dietetic_daily_list/ 03. 我的-饮食日报列表
       @apiGroup U_用户_USER
       @apiVersion 1.0.0
       @apiPermission 访问授权
       @apiParam {str} next_start 分页起始ID 默认值: null
       @apiSuccessExample {json} JSON.result 对象
       {
         dietetic_daily:[
            {
                id: String # 饮食日报ID
                timed : Long 时间
            }
         ]
       }
    """

    if request.args.get('next_start'):
        next_start = int(request.args.get('next_start'))*10
    else:
        return "参数错误"
    user_id = "5a30d8954aee308711f1cfa2"
    # user_id = session["user_id"]
    find_all = DB.dietetic_daily.find_one({"user_id": user_id or "", "status": 0}).skip(next_start).limit(10)
    return common.findAll(find_all)


@model.route("/user/create/dietetic_daily/", methods=['post'])
def dietetic_daily():
    """
       @api {POST} /user/create/dietetic_daily/ 04. 用户发布饮食日报信息
       @apiGroup U_用户_USER
       @apiVersion 1.0.0
       @apiPermission 访问授权
       @apiParam {int} type 类别：[0=早餐/1=午餐/2=晚餐]
       @apiParam {str} content 内容
       @apiParam {list} images 饮食图片资料数组
       @apiSuccessExample {json} JSON.result 对象
       {
       }
    """
    # "user_id": session["user_id"],
    user_id = "5a30d8954aee308711f1cfa2"
    type = int(request.form.get("type"))
    if type == None or (type >= 3):
        return "用餐类别异常"
    images = request.form.getlist("images"),

    # 通过当天时间戳查询数据库
    times = int(time.strftime('%Y%m%d', time.localtime(time.time())))
    find_one = DB.dietetic_daily.find_one({"day": times, "status": 0, "user_id": user_id})
    if find_one == None:
        data = {
            "_id": bson.objectid.ObjectId().__str__(),
            # "user_id": session["user_id"],
            "user_id": user_id,
            "dietetics": [{
                "content": request.form.get("content"),
                "images": [{
                        "url": "sdfghhgfdssdfghgfd",  # 图片地址
                        "ratio": float(0),  # 图片宽高比
                    }],
                "timed": int(time.time()),
                "type": type,
            }],
            "day": times,
            "status": int(0),
            "timed": int(time.time())
        }
        insert_one = DB.dietetic_daily.insert_one(data)
        if insert_one.inserted_id:
            # 更新用户表里面的最新饮食日报发布时间，根据时间判断是否已报
            updates = DB.users.update_one({"_id": user_id}, {"$set": {"diet_timed": time.time()}})
            if updates > 0:
                return jsonify({"code": 0, "msg": "添加数据成功"})
            else:
                return jsonify({"code": -1, "msg": "添加数据失败"})
        else:
            return jsonify({"code": -1, "msg": "添加数据失败"})
    else:
        data = {
                "content": request.form.get("content"),
                "images": [{
                    "url": "阿凡达广发华福感到十分",  # 图片地址
                    "ratio": float(0),  # 图片宽高比
                }],
                "timed": int(time.time()),
                "type": type,
            }
        dietetic_daily_id = find_one["_id"]
        for type_detil in find_one["dietetics"]:
            dietetic_daily_type = type_detil["type"]
            if dietetic_daily_type == type:
                update_dietetic_daily = DB.dietetic_daily.save({"_id": dietetic_daily_id, "user_id": user_id,"dietetics.type": dietetic_daily_type, "day": times, "status": 0}, {"$set": {"dietetics": [data]}})
            else:
                update_dietetic_daily = DB.dietetic_daily.save({"_id": dietetic_daily_id, "user_id": user_id, "dietetics.type": dietetic_daily_type, "day": times, "status": 0}, {"$set": {"dietetics": [data]}})
        if update_dietetic_daily.matched_count > 0:
            # 更新用户表里面的最新饮食日报发布时间，根据时间判断是否已报
            updates = DB.users.update_one({"_id": user_id}, {"$set": {"diet_timed": time.time()}})
            if updates.matched_count > 0:
                return jsonify({"code": 0, "msg": "添加数据成功"})
            else:
                return jsonify({"code": -1, "msg": "添加数据失败"})
        else:
            return jsonify({"code": -1, "msg": "添加数据失败"})


@model.route("/user/get/dietetic_daily_info/<string:diet_id>/")
def dietetic_daily_info(diet_id):
    """
       @api {GET} /user/get/dietetic_daily_info/<diet_id>/ 05. 我的-发布饮食日报详细信息
       @apiGroup U_用户_USER
       @apiVersion 1.0.0
       @apiPermission 访问授权
       @apiParam {str} diet_id 饮食日报ID
       @apiSuccessExample {json} JSON.result 对象
       {
             "dietetic" : [{
                "content": String # 内容
                "images": [  # 饮食图片资料数组
                    {
                    "url": String # 图片地址
                    "ratio": Float # 图片宽高比
                    }
                    ]
                "type": Int # 日报类别: [0=早餐/1=午餐/2=晚餐]
                "timed": Long # 餐饮时间
             }]
             "timed": Long # 创建时间
       }
    """
    if diet_id:
        diet_ids = diet_id
    else:
        return "参数错误"
    # user_id = session["user_id"]
    find = DB.dietetic_daily.find_one({"_id": diet_ids, "status": 0})
    return common.find(find)

@model.route("/user/get/user_comprehensive_daily/")
def user_comprehensive_daily():
    """
       @api {GET} /user/get/user_comprehensive_daily/ 06. 我的-获取综合日报列表信息
       @apiGroup U_用户_USER
       @apiVersion 1.0.0
       @apiPermission 访问授权
       @apiParam {str} next_start 分页起始ID 默认值: null
       @apiSuccessExample {json} JSON.result 对象
       {
            "local_weight" : Double # 原始体重 [单位：kg]
            "arrange_weight" : Double # 变化体重 [单位：kg]
            "today_weight" : Double # 今日体重 [单位：kg]
             "comprehensive" : [{
                "weight": Double # 今日体重
                "arrange_weight" : Double # 变化体重 [单位：kg]
                "timed": Long # 创建时间
             }]
             "timed": Long # 创建时间
       }
       comprehensive_daily
    """
    if request.args.get('next_start'):
        next_start = int(request.args.get('next_start'))*10
    else:
        return "参数错误"
    user_id = "5a30d8954aee308711f1cfa2"
    # user_id = session["user_id"]
    find_all = DB.comprehensive_daily.find({"user_id": user_id}).skip(next_start).limit(10)
    return common.findAll(find_all)



@model.route('/user/get/user_comprehensive_info/<string:comprehensive_id>/')
def user_comprehensive_info(comprehensive_id):
    """
        @api {GET} /user/get/user_comprehensive_info/<comprehensive_id>/ 07. 获取综合日报详细信息
        @apiGroup U_用户_USER
        @apiVersion 1.0.0
        @apiPermission 访问授权
        @apiParam {str} comprehensive_id 用户ID
        @apiSuccessExample {json} JSON.result 对象
        {
              "_id": String # 主键，综合日报ID,
              "weight": String # 今日体重
              "waist": String # 今日腰围
              "images":   # 今日运动量
                  {
                  "url": String # 图片地址
                  "ratio": Float # 图片宽高比
                  }
              "timed": Long # 创建时间
        }
    """
    if comprehensive_id:
        comprehensive_ids = comprehensive_id
    else:
        return "参数错误"
    # user_id = session["user_id"]
    find = DB.comprehensive_daily.find_one({"_id": comprehensive_ids})
    return common.find(find)

@model.route('/user/add_comprehensive_daily/', methods=['post'])
def add_comprehensive_daily():
    """
       @api {POST} /user/add_comprehensive_daily/ 08. 添加综合日报
       @apiGroup U_用户_USER
       @apiVersion 1.0.0
       @apiPermission 访问授权
       @apiParam {double} weight 体重
       @apiParam {double} waist 腰围
       @apiParam {list} images 运动量图片2
       @apiSuccessExample {json} JSON.result 对象
       {
       }
    """
    images = ""
    user_id = "5a30d8954aee308711f1cfa2"
    data = {
        "_id": bson.objectid.ObjectId().__str__(),
        # "user_id": session["user_id"],
        "user_id": "5a30d8954aee308711f1cfa2",
        "weight": float(request.form.get("weight")) or float(0),
        "waist": float(request.form.get("waist")) or float(0),
        "images": {
            "url": "阿凡达广发华福感到十分",  # 图片地址
            "ratio": float(0),  # 图片宽高比
        },
        "timed": int(time.time())
    }
    insert_one = DB.comprehensive_daily.insert_one(data)
    if insert_one.inserted_id:
        # 更新用户表
        updates = DB.users.update_one({"_id": user_id}, {"$set": {"assessment": "", "weight": float(request.form.get("weight")) or float(0), "waist": float(request.form.get("waist")) or float(0)}})
        if updates > 0:
            return jsonify({"code": 0, "msg": "添加数据成功", "assessment":""})
        else:
            return jsonify({"code": -1, "msg": "添加数据失败"})
    else:
        return jsonify({"code": -1, "msg": "添加数据失败"})


@model.route('/user/obesity_test/', methods=['post'])
def obesity_test():
    """
       @api {POST} /user/obesity_test/ 09. 肥胖测试
       @apiGroup U_用户_USER
       @apiVersion 1.0.0
       @apiPermission 访问授权
       @apiParam {int} sex 性别
       @apiParam {int} age 年龄
       @apiParam {int} height 身高
       @apiParam {double} weight 体重
       @apiParam {str} sport 运动量
       @apiSuccessExample {json} JSON.result 对象
       {
        ...
       }
    """
    # "user_id": session["user_id"],
    user_id = "5a30d8954aee308711f1cfa2",
    if request.form.get("weight") and request.form.get("height"):
        weight = request.form.get("weight")
        height = request.form.get("height")
        # 计算
        num = float(height) * float(height)
        Result = float(weight) / num
        if Result >= 24 or Result <= 25:
            standard = "体重超重"
        elif Result > 25 or Result < 28:
            standard = "超重,肥胖"
        elif Result > 28 or Result < 30:
            standard = "轻度肥胖"
        elif Result > 30 or Result < 35:
            standard = "中度肥胖"
        elif Result >= 35:
            standard = "重度肥胖"
        # 175 - 80 * float("70%"[:-1]) / 100
        sum = height - 80 * float("70%"[:-1]) / 100
        update = DB.users.update_one({"_id": user_id}, {"$set": {"assessment": standard}})
        return jsonify({"assessment": standard, "norm_weight": float(sum), "weight": float(request.form.get("weight"))})
    else:
        return "参数错误"

    # "user_id": session["user_id"],
    # user_id = "5a30d8954aee308711f1cfa2",
    # update = DB.users.update_one({"_id": user_id,
    #                               "sex": int(request.form.get("sex")) or 0,
    #                               "age": int(request.form.get("age")) or 0,
    #                               "height": int(request.form.get("height")) or 0,
    #                               "weight": float(request.form.get("weight")) or float(0),
    #                               "sport": request.form.get("sport") or "",
    #                               "assessment": "",
    #                               })
    # if update > 0:
    #     return jsonify({"code": 1, "msg": "数据编辑成功"})
    # else:
    #     return jsonify({"code": 2, "msg": "数据编辑失败"})



@model.route('/user/apply_free_consultation/',methods=['post'])
def apply_free_consultation():
    """
       @api {POST} /user/apply_free_consultation/ 010. 申请免费咨询
       @apiGroup U_用户_USER
       @apiVersion 1.0.0
       @apiPermission 访问授权
       @apiParam {int} sex 性别
       @apiParam {int} age 年龄
       @apiParam {int} height 身高
       @apiParam {double} weight 体重
       @apiParam {str} sport 运动量
       @apiSuccessExample {json} JSON.result 对象
       {
       }
    """
    # "user_id": session["user_id"],
    user_id = "5a30d8954aee308711f1cfa2",
    update = DB.users.update_one({"_id": user_id}, {"$set": {"sex": int(request.form.get("sex")) or 0, "age": int(request.form.get("age")) or 0, "height": int(request.form.get("height")) or 0, "weight": float(request.form.get("double")) or float(0), "sport": request.form.get("sport") or ""}})
    if update > 0:
        return jsonify({"code": 0, "msg": "数据编辑成功"})
    else:
        return jsonify({"code": -1, "msg": "数据编辑失败"})

@model.route('/user/files_upload/',methods=['post'])
def files_upload():
    """
       @api {POST} /user/files_upload/ 11. 文件上传接口
       @apiGroup U_用户_USER
       @apiVersion 1.0.0
       @apiPermission 访问授权
       @apiSuccessExample {json} JSON.result 对象
       {
       }
    """
    abpath = os.path.abspath('./upload/')
    for upload in request.files.getlist("file"):
        file_name = upload.filename.rsplit("/")[0]
        destination = "/".join([abpath, file_name])
        upload.save(str(destination))
        result = {"file_name": file_name, "destination": destination}
    return jsonify({"code": 0, "filename": result})

@model.route('/user/update_user/', methods= ['post'])
def update_user():
    """
       @api {POST} /user/update_user/ 12. 修改个人资料
       @apiGroup U_用户_USER
       @apiVersion 1.0.0
       @apiPermission 访问授权
       @apiParam {list} avatar 头像
       @apiParam {str} name 姓名
       @apiParam {int} sex 性别
       @apiParam {str} phone 电话
       @apiParam {str} address 地址
       @apiSuccessExample {json} JSON.result 对象
       {
       }
    """
    user_id = "5a30d8954aee308711f1cfa2",
    update = DB.users.update_one({"_id": user_id,
                                  "sex": int(request.form.get("sex")) or 0,
                                  "avatar": request.form.get("avatar") or "",
                                  "name": request.form.get("height") or "",
                                  "phone": request.form.get("double") or "",
                                  "address": request.form.get("address") or "",
                                  })
    if update > 0:
        return jsonify({"code": 0, "msg": "数据编辑成功"})
    else:
        return jsonify({"code": -1, "msg": "数据编辑失败"})

