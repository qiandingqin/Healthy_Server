# coding=utf-8
# -*- coding: utf-8 -*-
from flask import Blueprint
model = Blueprint('seller', __name__)

@model.route("/login/",methods=['POST'])
def login():
    """
      @api {POST} /seller/login/ 01. 商家-登录
      @apiGroup S_商家_Seller
      @apiVersion 1.0.0

      @apiPermission 访问授权

      @apiParam {str} account 手机号码
      @apiParam {str} [password] 密码
      @apiSuccessExample {json} JSON.result 对象
      {

      }
    """

@model.route("/mine/logout/",methods=['POST'])
def logout():
    """
      @api {POST} /seller/mine/logout/ 02. 商家-退出登录
      @apiGroup S_商家_Seller
      @apiVersion 1.0.0

      @apiPermission 用户登录
      @apiSuccessExample {json} JSON.result 对象
      {

      }
    """

@model.route("/my_clients/",methods=['POST'])
def my_clients():
    """
       @api {POST} /seller/my_clients/ 03. 获取我的客户列表
       @apiGroup S_商家_Seller
       @apiVersion 1.0.0
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


@model.route("/recipes/<string:user_id>/",methods=['POST'])
def recipes():
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

@model.route("/apply_clients/",methods=['POST'])
def apply_clients():
    """
      @api {POST} /seller/apply_clients/ 05. 获取我的申请用户列表
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

@model.route("/apply_clients_info/<string:user_id>/",methods=['POST'])
def apply_clients_info(user_id):
    """
       @api {POST} /seller/apply_clients_info/<user_id>/ 06. 获取用户详细信息
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


@model.route('/create_apply/<string:user_id>/',methods=['POST'])
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

@model.route('/user_recipes/<string:user_id>/')
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

@model.route('/dietetic_daily/<string:user_id>/')
def dietetic_daily(user_id):
    """
       @api {GET} /seller/dietetic_daily/<user_id>/ 09. 获取用户饮食日报列表
       @apiGroup S_商家_Seller
       @apiVersion 1.0.0
       @apiPermission 访问授权
       @apiParam {str} user_id 用户ID
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

@model.route('/comprehensive_daily/<string:user_id>/')
def comprehensive_daily(user_id):
    """
       @api {GET} /seller/comprehensive_daily/<user_id>/ 10. 获取用户综合日报列表信息
       @apiGroup U_用户_USER
       @apiVersion 1.0.0
       @apiPermission 访问授权
       @apiParam {str} user_id 用户ID
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