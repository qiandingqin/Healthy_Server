# coding=utf-8
# -*- coding: utf-8 -*-
from flask import Flask, session, redirect, url_for
from functools import wraps
from app.controller.common import abort, apiresult

def requery_auth(func):
    @wraps(func)
    def auth(*args, **kwargs):
        if "ticket" in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('index.index'))
    return auth

def requires_login(func):
    '''
    登录授权
    :param func:
    :return:
    '''
    @wraps(func)
    def authod(*args, **kwargs):
        if "user_id" in session:
            user_id = session["user_id"]
            if user_id and len(user_id) > 6:
             return func(*args, **kwargs)

        # abort(-10000, "登录无效, 无法访问")
        return apiresult({"message": "登录无效, 无法访问"}, code=-1)
    return authod

