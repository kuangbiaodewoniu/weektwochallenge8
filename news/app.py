# !usr/bin/env python  
# -*- coding:utf-8 _*-  
""" 
@author:dandan.zheng 
@file: app.py 
@time: 2018/03/21 
"""
from flask import Flask, render_template
from models.db import get_file_data, get_data_byid, File

app = Flask(__name__)


@app.route('/')
def index():
    # 显示文章名称的列表
    # 页面中需要显示所有文章的标题（title）列表，此外每个标题都需要使用 `<a href=XXX></a>` 链接到对应的文章内容页面
    datas = get_file_data()
    if not datas:
        return render_template('404.html', error='shiyanlou 404')
    return render_template('index.html', datas=datas)


@app.route('/files/<file_id>')
def file(file_id):
    # file_id 为 File 表中的文章 ID
    # 需要显示 file_id  对应的文章内容、创建时间及类别信息（需要显示类别名称）
    # 如果指定 file_id 的文章不存在，则显示 404 错误页面
    data = get_data_byid(file_id)
    if not data:
        return render_template('404.html', error='shiyanlou 404')
    return render_template('file.html', data=data)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error='shiyanlou 404')


if __name__ == '__main__':
    app.run()






