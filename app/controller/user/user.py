# coding=utf-8
# -*- coding: utf-8 -*-
from flask import Blueprint, request, session, g, render_template,jsonify
from conf.config import appID,appsecret, users, dietetic_daily, comprehensive_daily, recipes, DB
import bson,time, json, os, pymongo, httplib
from bson.json_util import dumps
from app.controller import common
from datetime import datetime
model = Blueprint('user', __name__)

@model.route("/user/user_info/")
def user_info():
    """
       @api {GET} /user/user_info/ 01. 我的(会员用户)-信息
       @apiGroup U_用户_USER
       @apiVersion 1.0.0
       @apiSuccessExample {json} JSON.result 对象
        {
            "_id": String # 主键，用户ID,
            "account": String # 账号登录名
            "password": String # 密码(系统自加密存储，不可逆)
            "type": Int # 类别, [0=会员/1=商家]
            "name": String # 姓名/昵称
            "oauth": [
                {
                    "open_id": String # 第三方开放ID
                    "name": String # 第三方昵称
                    "avatar": String # 第三方头像
                    "sex": Int # 第三方性别
                    "timed": Long # 首次授权时间
                }, ...
            ],
            "phone": String #联系方式
            "avatar": String # 头像
            "sex": Int # 性别: [-1=未知/1=男/2=女]
            "apply_weight" : Double #申请减重[单位：kg]
            "estimated_times" : String #预计时间
            "age": Int #年龄
            "height" : Int #身高 [cm]
            "weight" : Double #体重 [kg]
            "local_weight" : Double #原始体重 [kg]
            "local_waist" : Double #原始腰围 [cm]
            "sport" : String # 运动
            "apply_status" : Int # 申请状态[0=申请/1=商家同意/-1=商家不同意/2=默认状态]
            "assessment" : String # 当前评估
            "diet_timed" : Long #最新饮食日报发布时间，根据时间判断是否已报
            "is_report" : Long #最新食谱发布时间，根据时间判断商家是否配餐
            "status": Int # 状态: [0=正常/-1=停止]
            "online": Int # 在线状态: [0=离线/1=在线]
            "address": String # 地址
            "times": {
                "timed": Long # 创建时间
                "logined": Long # 最后登录时间, 0=还没有登录过
                "stoped": Long # 停用起始时间, 如果status=-1时可以通过这个时间恢复正常
                "stop_elapse": Long # 停用时长(秒), -1=永久
            }
        }
    """
    try:
        user_id = session["user_id"]
        # user_id = "5a3a2d504aee300b032c897e"
        find = users.find_one({"_id": user_id, "status": 0, "type": 0})
        if find == None:
            find["new_assessment"] = ""
            return common.find(find=find)
        else:
            weight = find["weight"]
            height = find["height"]
            if weight == float(0) or height == float(0):
                find["new_assessment"] = ""
                return common.find(find=find)
            else:
                heights = float(height) / float(100)
                num = float(heights) * float(heights)
                Result = float(weight) / num
                if Result < 18.5:
                    standard = "营养不良"
                elif Result > 18.5 and Result < 23.9999:
                    standard = "正常体重"
                elif Result >= 24 and Result <= 26:
                    standard = "超重"
                elif Result > 26 and Result < 28:
                    standard = "超重,肥胖"
                elif Result > 28 and Result < 30:
                    standard = "轻度肥胖"
                elif Result > 30 and Result < 35:
                    standard = "中度肥胖"
                elif Result >= 35:
                    standard = "重度肥胖"
                find["new_assessment"] = standard
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
        return jsonify({"code": -10001, "mag": "参数错误"})
    user_id = session["user_id"]
    # user_id = "5a30d3694aee3086ea6d7c29"
    find_all = recipes.find({"user_id": user_id}).skip(next_start).limit(10).sort("day", pymongo.ASCENDING)
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
        return jsonify({"code": -10001, "mag": "参数错误"})
    # user_id = "5a30d3694aee3086ea6d7c29"
    user_id = session["user_id"]
    find_all = DB.dietetic_daily.find(filter={"user_id": user_id, "status": 0}, projection={"id": 1, "timed": 1}).skip(next_start).limit(10).sort("timed", pymongo.DESCENDING)
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
    user_id = session["user_id"]
    # user_id = "5a30d3694aee3086ea6d7c29"
    type = int(request.form.get("type"))
    if type == None or (type >= 3):
        return jsonify({"code": -1001, "msg": "用餐类别异常"})
    images_list = []
    images = request.form.getlist("images")
    if images.__len__() > 0:
        for img in images:
            imgs = {"url": img, "ratio": float(0)}
            images_list.append(imgs)
    else:
        imgs = {"url": "", "ratio": float(0)}
        images_list.append(imgs)
    # 通过当天时间戳查询数据库
    times = int(time.strftime('%Y%m%d', time.localtime(time.time())))
    find_one = DB.dietetic_daily.find_one({"day": times, "status": 0, "user_id": user_id})
    if find_one == None:
        data = {
            "_id": bson.objectid.ObjectId().__str__(),
            # "user_id": session["user_id"],
            "user_id": user_id,
            "dietetics": [{
                "_id": bson.objectid.ObjectId().__str__(),
                "content": request.form.get("content"),
                "images": images_list,
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
            updates = DB.users.update_one({"_id": user_id}, {"$set": {"diet_timed": int(time.time())}})
            if updates.matched_count > 0:
                return jsonify({"code": 0, "msg": "添加数据成功"})
            else:
                return jsonify({"code": -1, "msg": "添加数据失败"})
        else:
            return jsonify({"code": -1, "msg": "添加数据失败"})
    else:
        data = {
            "_id": bson.objectid.ObjectId().__str__(),
            "content": request.form.get("content"),
            "images": images_list,
            "timed": int(time.time()),
            "type": type,
        }
        dietetic_daily_id = find_one["_id"]
        for type_detil in find_one["dietetics"]:
            dietetic_daily_type = type_detil["type"]
            dietetic_id = type_detil["_id"]
            if dietetic_daily_type == type and dietetic_id:
                update_dietetic_daily = DB.dietetic_daily.update({"_id": dietetic_daily_id, "user_id": user_id, "day": times, "status": 0, "dietetics.type": dietetic_daily_type}, {"$set": {"dietetics.$": data}})
                if update_dietetic_daily != None:
                    # 更新用户表里面的最新饮食日报发布时间，根据时间判断是否已报
                    updates = DB.users.update_one({"_id": user_id}, {"$set": {"diet_timed": time.time()}})
                    if updates.matched_count > 0:
                        return jsonify({"code": 0, "msg": "添加数据成功"})
                    else:
                        return jsonify({"code": -1, "msg": "添加数据失败"})
                else:
                    return jsonify({"code": -1, "msg": "添加数据失败"})
            elif dietetic_daily_type != type:
                update_dietetic_daily = DB.dietetic_daily.update({"_id": dietetic_daily_id, "user_id": user_id, "day": times, "status": 0}, {"$addToSet": {"dietetics": data}})
                if update_dietetic_daily != None:
                    # 更新用户表里面的最新饮食日报发布时间，根据时间判断是否已报
                    updates = DB.users.update_one({"_id": user_id}, {"$set": {"diet_timed": int(time.time())}})
                    if updates.matched_count > 0:
                        return jsonify({"code": 0, "msg": "添加数据成功"})
                    else:
                        return jsonify({"code": -1, "msg": "添加数据失败"})
                else:
                    return jsonify({"code": -1, "msg": "添加数据失败"})


@model.route("/user/get/dietetic_daily_info/<string:diet_id>/")
def dietetic_daily_info(diet_id):
    """
       @api {GET} /user/get/dietetic_daily_info/<diet_id>/ 05. 我的-饮食日报详细信息
       @apiGroup U_用户_USER
       @apiVersion 1.0.0
       @apiPermission 访问授权
       @apiParam {str} diet_id 饮食日报ID
       @apiSuccessExample {json} JSON.result 对象
       {
             "dietetics" : [{
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
             "timed": Long # 创建时间lose_weight
       }
    """
    if diet_id:
        diet_ids = diet_id
    else:
        return "参数错误"
    # user_id = session["user_id"]
    find = DB.dietetic_daily.find_one({"_id": diet_ids, "status": 0})
    if find != None:
        find['dietetics'] = sorted(find['dietetics'], cmp=sorts, reverse=False)
        data = {"dietetics": find['dietetics']}
        return common.find(data)
    else:
        return jsonify({"code": -1, "result": []})


def sorts(a, b):
    return a['type']-b['type']

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
    user_id = session["user_id"]
    # user_id = "5a30d3694aee3086ea6d7c29"
    find_all = DB.comprehensive_daily.find({"user_id": user_id}).skip(next_start).limit(10).sort("timed", pymongo.DESCENDING)
    data = []
    if find_all:
        user_infos = DB.users.find_one({"_id": user_id})
        # 用户原始体重
        local_weight = int(user_infos["local_weight"])
        # 用户最新的体重（添加综合日报需要更新）
        new_weight = int(user_infos["weight"])
        # 计算今日体重
        arrange_weight = local_weight - new_weight
        for find_key in find_all:
            # 计算体重变化
            arrange_weight = local_weight - int(find_key["weight"])
            datas = {
                "_id": find_key["_id"],
                "weight": find_key["weight"],
                "arrange_weight": arrange_weight,
                "local_weight": local_weight,
                "timed": find_key["timed"],
            }
            data.append(datas)
        datas = data
        app_data = {"code": 0, "local_weight": local_weight, "today_weight": new_weight, "arrange_weight": arrange_weight, "comprehensive": datas}
        return jsonify(app_data)

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
       @apiParam {Long} day  #时间戳，按天算
       @apiParam {list} images 运动量图片2
       @apiSuccessExample {json} JSON.result 对象
       {
       }
    """

    images = ""

    # 通过当天时间戳查询数据库
    times = int(time.strftime('%Y%m%d', time.localtime(time.time())))
    user_id = session["user_id"]
    # user_id = "5a3a2d504aee300b032c897e"
    images_list = []
    images = request.form.getlist("images")
    if images.__len__() > 0:
        for img in images:
            imgs = {"url": img, "ratio": float(0)}
            images_list.append(imgs)
    else:
        imgs = {"url": "", "ratio": float(0)}
        images_list.append(imgs)
    data = {
        "_id": bson.objectid.ObjectId().__str__(),
        "user_id": user_id,
        "weight": float(request.form.get("weight")) or float(0),
        "waist": float(request.form.get("waist")) or float(0),
        "images": images_list,
        "timed": int(time.time()),
        "day": times
    }
    find_one = DB.comprehensive_daily.find_one({"user_id": user_id, "day": times})
    if find_one == None:
        insert_one = DB.comprehensive_daily.insert_one(data)
        if insert_one.inserted_id:
            # 更新用户表
            update = DB.users.update_one({"_id": user_id}, {"$set": {"weight": float(request.form.get("weight")) or float(0)}})
            if update.matched_count > 0:
                return jsonify({"code": 0, "msg": "添加数据成功"})
            else:
                return jsonify({"code": -1, "msg": "添加数据失败"})
        else:
            return jsonify({"code": -1, "msg": "添加数据失败"})
    else:
        ids = find_one["_id"]
        dataa = {
            "weight": float(request.form.get("weight")) or float(0),
            "waist": float(request.form.get("waist")) or float(0),
            "images": images_list,
        }
        for key in dataa.keys():
            if dataa[key] == None or dataa[key] == "":
                del (dataa[key])
        datas = dataa
        update_one = DB.comprehensive_daily.update_one({"_id": ids}, {"$set": datas})
        if update_one.matched_count > 0:
            # 更新用户表
            update = DB.users.update_one({"_id": user_id},{"$set": {"weight": float(request.form.get("weight")) or float(0)}})
            if update.matched_count > 0:
                return jsonify({"code": 0, "msg": "添加数据成功"})
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
       @apiParam {double} local_weight 体重
       @apiParam {str} sport 运动量
       @apiSuccessExample {json} JSON.result 对象
       {
        ...
       }
    """
    user_id = session["user_id"]
    # user_id = "5a30d3694aee3086ea6d7c29"
    weight = request.form.get("local_weight")
    heights = request.form.get("height")
    sport = request.form.get("sport") or ""
    if weight and heights:
        # 计算
        height = float(heights) / float(100)
        num = float(height) * float(height)
        Result = float(weight) / num
        if Result < 18.5:
            standard = "营养不良"
        elif Result > 18.5 and Result < 23.9:
            standard = "正常体重"
        elif Result >= 24 and Result <= 26:
            standard = "超重"
        elif Result > 26 and Result < 28:
            standard = "超重,肥胖"
        elif Result > 28 and Result < 30:
            standard = "轻度肥胖"
        elif Result > 30 and Result < 35:
            standard = "中度肥胖"
        elif Result >= 35:
            standard = "重度肥胖"
        update = DB.users.update_one({"_id": user_id}, {"$set": {"assessment": standard, "sport": sport, "local_weight": float(request.form.get("local_weight")), "weight": float(request.form.get("local_weight")), "age": request.form.get("age"), "height": float(heights)}})
        if update.matched_count > 0:
            return jsonify({"assessment": standard, "local_weight": float(request.form.get("local_weight")), "weight": float(request.form.get("local_weight"))})
        else:
            return jsonify({"code": -1, "msg": "操作失败"})
    else:
        return jsonify({"code": -1001, "msg": "参数错误"})

@model.route('/user/apply_free_consultation/', methods=['post'])
def apply_free_consultation():
    """
       @api {POST} /user/apply_free_consultation/ 010. 申请免费咨询
       @apiGroup U_用户_USER
       @apiVersion 1.0.0
       @apiPermission 访问授权
       @apiParam {str} estimated_times 预计时间
       @apiParam {float} apply_weight 申请减重[单位：kg]
       @apiParam {str} name 姓名
       @apiParam {str} phone 电话
       @apiSuccessExample {json} JSON.result 对象
       {
       }
    """
    user_id = session["user_id"]
    # user_id = "5a30d3694aee3086ea6d7c29"
    estimated_times = request.form.get("estimated_times")
    apply_weight = request.form.get("apply_weight")
    name = request.form.get("name")
    phone = request.form.get("phone")
    if estimated_times and apply_weight and name and phone:
        data = {
            "estimated_times": estimated_times,
            "apply_weight": float(apply_weight),
            "name": name,
            "phone": phone,
            "apply_status": int(0)
            }
        update = DB.users.update_one({"_id": user_id}, {"$set": data})
        if update.matched_count > 0:
            return jsonify({"code": 0, "msg": "数据编辑成功"})
        else:
            return jsonify({"code": -1, "msg": "数据编辑失败"})
    else:
        return jsonify({"code": -1001, "msg": "参数错误"})

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
    # files = request.files.getlist("file")

    abpath = os.path.abspath('./app/static/upload/')
    file_data = []
    if os.path.isdir('./app/static/upload/') == False:
        os.mkdir("./app/static/upload/")
        for upload in request.files.getlist("file"):
            file_name = upload.filename.rsplit("/")[0]
            destination = "/".join([abpath, file_name])
            upload.save(str(destination))
            result = {"file_name": file_name, "destination": "upload/"+file_name}
            file_data.append(result)
        return jsonify({"code": 0, "filename": file_data})
    else:
        for upload in request.files.getlist("file"):
            file_name = upload.filename.rsplit("/")[0]
            destination = "/".join([abpath, file_name])
            upload.save(destination)
            result = {"file_name": file_name, "destination": "upload/"+file_name}
            file_data.append(result)
        return jsonify({"code": 0, "filename": file_data})

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
    user_id = session["user_id"]
    # user_id = "5a30d3694aee3086ea6d7c29",
    data = {
        "sex": request.form.get("sex") and int(request.form.get("sex")) or "",
        "phone": request.form.get("phone") or "",
        "height": request.form.get("height") and int(request.form.get("height")) or "",
        "weight": request.form.get("weight") and float(request.form.get("weight")) or "",
        "age": request.form.get("age") and int(request.form.get("age")) or "",
        "avatar": request.form.get("avatar") or "",
        "name": request.form.get("name") or "",
        "address": request.form.get("address") or ""
    }
    for key in data.keys():
        if data[key] == None or data[key] == "":
            del(data[key])
    datas = data
    updates = DB.users.update_one({"_id": user_id}, {"$set": datas})
    if updates.matched_count > 0:
        return jsonify({"code": 0, "msg": "数据编辑成功"})
    else:
        return jsonify({"code": -1, "msg": "数据编辑失败"})



# @model.route("/user/not_founts")
# def not_founts():
#     if "user_id" in session:
#         user_id = session["user_id"]
#         if user_id == None:
#             return render_template("not_found.html")
#         else:
#             user_info = DB.users.find_one({"_id": user_id})
#             if user_info != None:
#                 if user_info["type"] == 1:
#                     return render_template("index/index_admin.html")
#                 else:
#                     return render_template("index/index.html")
#     else:
#         return render_template("not_found.html")
# @model.route('/user/update_date/', methods= ['post'])
# def uodate_data():
#     data = {
#         "name": "234567654",
#         "haha": "",
#         "hehe": "66666"
#     }
#     if data.__len__() == 0:
#         return jsonify({"code": -1, "msg": "编辑失败"})
#     else:
#         for key in data.keys():
#             if data[key].__len__() == 0:
#                 del(data[key])
#     return jsonify(data)


@model.route('/a')
def uodate_data():
    return render_template("upload.html")




