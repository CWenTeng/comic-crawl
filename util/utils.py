import execjs
import json
import random
import re
import time
import traceback
from os.path import join

import config
import requests

from util.logUtil import download_log

# 格式化
def formatting(t):
    t = t.replace("|", " ") \
        .replace("?", " ") \
        .replace("*", " ") \
        .replace(":", " ") \
        .replace('[', '(') \
        .replace(']', ')') \
        .replace('<', '(') \
        .replace('>', ')') \
        .replace('「', ' ') \
        .replace('\\', ' ') \
        .replace('/', ' ') \
        .replace('"', ' ') \
        .replace('）', ')') \
        .replace('#', ' ') \
        .replace('（', '(')
    t = ' '.join(t.split('_'))
    t = '_'.join(t.split())
    return t


"""
js js代码段
funcName 执行入口函数名
args 入参
"""
def runJs(js, funcName, *args):
    ctx = execjs.compile(js)
    return ctx.call(funcName,*args)
