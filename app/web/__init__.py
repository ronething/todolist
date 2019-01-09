# -*- coding:utf-8 _*-  
""" 
@author: ronething 
@file: __init__.py.py 
@time: 2019/01/09
@github: github.com/ronething 

Less is more.
"""

from flask import Blueprint

web = Blueprint("web", __name__)

# views 不能放在 web blueprint 前面 否则会报错
import app.web.views
