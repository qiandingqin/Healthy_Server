#!/usr/bin/env python
# coding=utf-8
# -*- coding: utf-8 -*-


from app import app
from conf import config
from flask import Blueprint, request, session, g, render_template,jsonify, redirect, url_for

app.config.from_object(config)

@app.errorhandler(404)
def not_found(e):
    if "user_id" in session:
        user_id = session["user_id"]
        if user_id == None:
            return render_template("not_found.html")
        else:
            user_info = config.DB.users.find_one({"_id": user_id})
            if user_info != None:
                if user_info["type"] == 1:
                    return render_template("index/index_admin.html")
                else:
                    return render_template("index/index.html")
    else:
        return render_template("not_found.html")

# @app.errorhandler(500)
# def internal_server_error(e):
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888)