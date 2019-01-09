# -*- coding:utf-8 _*-  
""" 
@author: ronething 
@file: manage.py 
@time: 2019/01/09
@github: github.com/ronething 

Less is more.
"""

from app import app

if __name__ == '__main__':
    app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"])
