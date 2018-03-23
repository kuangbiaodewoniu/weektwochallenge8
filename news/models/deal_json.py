# !usr/bin/env python  
# -*- coding:utf-8 _*-  
""" 
@author:dandan.zheng 
@file: deal_json.py 
@time: 2018/03/22 
"""
import os,json

# pwd = os.getcwd()
# news_dir = os.path.abspath(os.path.dirname(pwd)+os.path.sep+"files")


# 从文件中获取json数据
def get_data(json_file):
    try:
        with open(json_file) as re:
            data = json.load(re)
            return data
    except:
        return []


# 取标题
def get_title(data):
    return data.get('title')


# 获取文件
def get_files(dir):
    files = []
    for file_name in os.listdir(dir):
        file = os.path.join(dir, file_name)
        files.append(file)
    return files