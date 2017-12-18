#!/usr/bin/env python
# coding=utf-8
# -*- coding: utf-8 -*-


from app import app
from conf import config
from flask import Blueprint, request, session,render_template




app.config.from_object(config)

@app.errorhandler(404)
def not_found():
    user_id = session["user_id"]
    if user_id == None:
        pass



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888)
