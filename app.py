#!/usr/bin/env python
# coding=utf-8
# -*- coding: utf-8 -*-


from app import app
from conf import config

app.config.from_object(config)
if __name__ == '__main__':
    app.run(host="www.zhl.com", port=8888)
