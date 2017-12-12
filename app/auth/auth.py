# coding=utf-8
# -*- coding: utf-8 -*-
from flask import Flask, session, redirect, url_for
from functools import wraps

def requery_auth(func):
    @wraps(func)
    def auth(*args, **kwargs):
        if "ticket" in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('index.index'))
    return auth

