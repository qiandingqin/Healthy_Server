# coding=utf-8
# -*- coding: utf-8 -*-
from flask import Blueprint, request, session, g, render_template
model = Blueprint('user', __name__)

@model.route("/oauth/<string:open_id>/",methods=['post'])
def oauth(open_id):
    """
       @api {POST} /user/oauth/<open_id>/ 01. 用户-第三方账号登录
       @apiGroup U_用户_USER
       @apiVersion 1.0.0

       @apiPermission 访问授权

       @apiParam {str} open_id 第三方唯一ID
       @apiParam {str} token 第三方授权TOKEN
       @apiParam {long} expire 失效时间
       @apiParam {str} name 第三方昵称
       @apiParam {str} avatar 第三方头像
       @apiParam {int} sex 第三方性别

       @apiSuccessExample {json} JSON.result 对象
       {

       }
      """

@model.route("/today_recipes/")
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

@model.route("/dietetic_daily_list/")
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


@model.route("/create/dietetic_daily/",methods=['post'])
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

@model.route("/get/dietetic_daily_info/<string:diet_id>/")
def dietetic_daily_info(diet_id):
    """
       @api {GET} /user/get/dietetic_daily/<diet_id>/ 05. 我的-发布饮食日报详细信息
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

@model.route("/get/comprehensive_daily/")
def comprehensive_daily():
    """
       @api {GET} /user/get/comprehensive_daily/ 06. 我的-获取综合日报列表信息
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
                "today_weight": Double # 今日体重
                "arrange_weight" : Double # 变化体重 [单位：kg]
                "timed": Long # 创建时间
             }]
             "timed": Long # 创建时间
       }
    """
    return  "sdfasdf"


@model.route('/get/comprehensive_info/<string:comprehensive_id>/')
def comprehensive_info(comprehensive_id):
    """
        @api {GET} /user/get/comprehensive_info/<comprehensive_id>/ 07. 获取综合日报详细信息
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

@model.route('/obesity_test/',methods=['post'])
def obesity_test():
    """
       @api {POST} /user/obesity_test/ 08. 肥胖测试
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

@model.route('/apply_free_consultation/',methods=['post'])
def apply_free_consultation():
    """
       @api {POST} /user/apply_free_consultation/ 09. 申请免费咨询
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

@model.route('/files_upload/',methods=['post'])
def files_upload():
    """
       @api {POST} /user/files_upload/ 10. 文件上传接口
       @apiGroup U_用户_USER
       @apiVersion 1.0.0
       @apiPermission 访问授权
       @apiSuccessExample {json} JSON.result 对象
       {
       }
    """