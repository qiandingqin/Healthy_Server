# coding=utf-8
# -*- coding: utf-8 -*-
from flask import Blueprint, request, session, render_template,jsonify,json
from conf.config import users,recipes,DB
from app.controller.common import apiresult,timestamp,item_count,next_start
import bson
from bson.json_util import dumps
import pymongo

model = Blueprint('seller', __name__)

@model.route("/seller/my_clients/", methods= ['post'])
def my_clients():
    """
       @api {POST} /seller/my_clients/ 03. 获取我的客户列表
       @apiGroup S_商家_Seller
       @apiVersion 1.0.0
       @apiParam {int} next_start 分页起始ID 默认值: 0
       @apiPermission 访问授权
       @apiSuccessExample {json} JSON.result 对象
       {
         "users" : [
                "_id": String # 主键，用户ID,其它地方为: user_id
                "name": String # 姓名/昵称
                "diet_timed" : Long #最新饮食日报发布时间，根据时间判断是否已报
                "is_report" : Long #最新食谱发布时间，根据时间判断商家是否配餐
            ]
       }
    """
    code = 0
    try:
        members = users.find({'type': 0, "apply_status": 1, "status": 0}).limit(item_count()).skip(next_start()).sort("timed", pymongo.DESCENDING)
    except:
        code = -1
    data = []
    for mem in members:
        member = {}
        member['_id'] = mem['_id']
        member['name'] = mem['name']
        member['diet_timed'] = mem['diet_timed']
        member['is_report'] = mem['is_report']
        data.append(member)

    us = {"users": data}
    # return jsonify(code=code,result=us,timestamp=timestamp())
    return apiresult(us, code)


@model.route("/seller/recipes/<string:user_id>/", methods=['post'])
def recipes(user_id):
    """
      @api {POST} /seller/recipes/<user_id>/ 04. 商家发布对应会员的食谱
      @apiGroup S_商家_Seller
      @apiVersion 1.0.0
      @apiPermission 访问授权
      @apiParam {str} user_id 用户ID
      @apiParam {str} content 食谱内容
      @apiSuccessExample {json} JSON.result 对象
      {
      }
    """
    if not user_id:
        return "请求参数错误"
    user = users.find_one(filter={"_id": user_id, "type": 0, "apply_status": 1}, projection={"_id": 1})
    if not user:
        return "该用户不存在或还不是您的会员"
    content = request.form.get("content")
    recipe = {
        "_id": bson.objectid.ObjectId().__str__(),
        "user_id": user_id,
        "content": content,
        "timed": timestamp()
    }
    code = 0
    try:
        DB.recipes.insert_one(recipe)
        #修改用户信息的配餐时间
        users.update_one({"_id": user_id, "is_report": timestamp()})
    except:
        code = -1
    return apiresult(None, code)

@model.route( "/seller/apply_clients/", methods = ['get'])
def apply_clients():
    """
      @api {get} /seller/apply_clients/ 05. 获取我的申请用户列表
      @apiGroup S_商家_Seller
      @apiVersion 1.0.0
      @apiPermission 访问授权
      @apiParam {str} next_start 分页起始ID 默认值: null
      @apiSuccessExample {json} JSON.result 对象
      {
        apply_clients:[{
           "_id": String # 主键，用户ID,其它地方为: user_id
           "name": String # 姓名/昵称
           "phone": String #联系方式
        }]
      }
    """
    lists = []
    code = 0
    try:
        list = users.find({"type": 0, "apply_status": 0}).limit(item_count()).skip(next_start()).sort("timed",pymongo.DESCENDING)
        for user in list:
            us = {}
            us['_id'] = user['_id']
            us['name'] = user['name']
            us['phone'] = user['phone']
            lists.append(us)
    except:
        code = -1
    data = {"apply_clients": lists}
    return apiresult(data, code)


@model.route("/seller/apply_clients_info/<string:user_id>/", methods=['get'])
def apply_clients_info(user_id):
    """
       @api {get} /seller/apply_clients_info/<user_id>/ 06. 获取用户详细信息
       @apiGroup S_商家_Seller
       @apiVersion 1.0.0
       @apiPermission 访问授权
       @apiParam {str} user_id 用户ID
       @apiSuccessExample {json} JSON.result 对象
       {
         "_id": String # 主键，用户ID,其它地方为: user_id
         "name": String # 姓名/昵称
         "phone": String #联系方式
         "avatar": String # 头像
         "sex": Int # 性别: [-1=未知/1=男/2=女]
         "apply_weight" : Double #申请减重[单位：kg]
         "estimated_times" : String #预计时间
         "age": Int #年龄
         "height" : Int #身高 [cm]
         "weight" : Int #体重 [kg]
         "sport" : String # 运动
         "assessment" : String # 当前评估
       }
    """
    if not user_id:
        return "请求参数错误"
    data = {}
    code = 0
    try:
        data = users.find_one(filter={"_id": user_id}, projection={"_id": 1, "name": 1, "phone": 1, "avatar": 1, "sex": 1,"apply_weight": 1, "estimated_times": 1, "age": 1, "height": 1,"weight": 1, "assessment": 1, "sport": 1})
    except:
        code = -1
    return apiresult(data, code)


@model.route('/seller/create_apply/<string:user_id>/', methods=['POST'])
def create_apply(user_id):
    """
      @api {POST} /seller/create_apply/<user_id>/ 07. 操作用户申请
      @apiGroup S_商家_Seller
      @apiVersion 1.0.0
      @apiPermission 访问授权
      @apiParam {str} user_id 用户ID
      @apiParam {bool} is_agree 是否同意[true=是/false=否]
      @apiSuccessExample {json} JSON.result 对象
      {
      }
    """
    if not user_id:
        return "请求参数错误"
    user = users.find_one(filter={"_id": user_id},projetction={"_id":1});
    code = 0
    if not user:
        return "该用户不存在"
    elif user["apply_status"] == 1:
        return "该用户已是你的会员，请不要重复操作"
    try:
        users.update_one({"_id": user_id}, {"$set": {"apply_status": 1}})
    except:
        code = -1
    return apiresult(None, code)

@model.route('/seller/user_recipes/<string:user_id>/')
def user_recipes(user_id):
    """
       @api {GET} /seller/user_recipes/<user_id>/ 08. 获取用户食谱列表
       @apiGroup S_商家_Seller
       @apiVersion 1.0.0
       @apiPermission 访问授权
       @apiParam {str} user_id 用户ID
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

    if not user_id:
        return "请求参数错误"
    code = 0
    lists = []
    try:
        lists = DB.recipes.find(filter={"user_id": user_id}, projection={"_id": 1, "content": 1, "timed": 1}).limit(item_count()).skip(next_start()).sort("timed", pymongo.DESCENDING)
    except:
        code = -1
    list = []
    for rec in lists:
        reci = {}
        reci['_id'] = rec['_id']
        reci['content'] = rec['content']
        reci['timed'] = rec['timed']
        list.append(reci)
    return apiresult({"today_recipes": list}, code)

@model.route('/seller/sell_dietetic_daily/<string:user_id>/')
def sell_dietetic_daily(user_id):
    """
       @api {GET} /seller/sell_dietetic_daily/<user_id>/ 09. 获取用户饮食日报列表
       @apiGroup S_商家_Seller
       @apiVersion 1.0.0
       @apiPermission 访问授权
       @apiParam {str} user_id 用户ID
       @apiParam {int} next_start 分页起始ID 默认值: null
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
    if not user_id:
        return "请求参数错误"
    code = 0
    lists = []
    try:
        lists = DB.dietetic_daily.find(filter={"user_id": user_id}, projection={"_id": 1, "timed": 1}).limit(item_count()).skip(next_start()).sort("timed", pymongo.DESCENDING)
    except:
        code = -1
    list = []
    for rec in lists:
        reci = {}
        reci['_id'] = rec['_id']
        reci['timed'] = rec['timed']
        list.append(reci)
    return apiresult({"dietetic_daily": list}, code)


@model.route('/seller/sell_comprehensive_daily/<string:user_id>/')
def sell_comprehensive_daily(user_id):
    """
       @api {GET} /seller/sell_comprehensive_daily/<user_id>/ 10. 获取用户综合日报列表信息
       @apiGroup S_商家_Seller
       @apiVersion 1.0.0
       @apiPermission 访问授权
       @apiParam {str} next_start 分页起始ID 默认值: null
       @apiSuccessExample {json} JSON.result 对象
       {
            "local_weight" : Double # 原始体重 [单位：kg]
            "arrange_weight" : Double # 变化体重 [单位：kg，备注：结果小于0瘦了，大于0胖了]
            "today_weight" : Double # 今日体重 [单位：kg]
             "comprehensive" : [{
                "weight": Double # 今日体重
                "arrange_weight" : Double # 变化体重 [单位：kg]
                "timed": Long # 创建时间
             }]
       }
    """
    if not user_id:
        return "请求参数不能为空"
    lists = []
    code = 0
    result = {}
    try:
        list = DB.comprehensive_daily.find(filter={"user_id": user_id}, projection={"weight": 1, "timed": 1, "_id": 1}).limit(item_count()).skip(next_start()).sort("timed", pymongo.DESCENDING)
        user = users.find_one(filter={"_id": user_id}, projection={"_id": 1, "weight": 1, "local_weight": 1})
        for comprehen in list:
            com = {}
            com['_id'] = comprehen['_id']
            com['weight'] = comprehen['weight']
            if comprehen['weight'] and user['weight']:
                com['arrange_weight'] = comprehen['weight'] - user['weight']
            else:
                com['arrange_weight'] = float(0)
            com['timed'] = comprehen['timed']
            lists.append(com)
        arrange_weight = float(0)
        if user:
            if ("weight" in user) and ("local_weight" in user):
                arrange_weight = user['local_weight'] - user['weight']
                result = {"local_weight": user['local_weight'], "arrange_weight": arrange_weight, "today_weight": user['weight'], "comprehensive": lists}
            result = {"local_weight": float(0), "arrange_weight": arrange_weight, "today_weight": user['weight'], "comprehensive": lists}
        else:
            result = {"local_weight": float(0), "arrange_weight": arrange_weight, "today_weight": float(0), "comprehensive": lists}
    except:
        code = -1

    return apiresult(result, code)
