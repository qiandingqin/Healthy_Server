#!/usr/bin/env python
# coding=utf-8
# -*- coding: utf-8 -*-


from app import app
from conf import config

app.config.from_object(config)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888)