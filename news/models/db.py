# !usr/bin/env python  
# -*- coding:utf-8 _*-  
""" 
@author:dandan.zheng 
@file: db.py
@time: 2018/03/21 
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@192.168.100.78:3306/51fanli_django'
db = SQLAlchemy(app)

client = MongoClient('mongodb://127.0.0.1', 27017)
mongo_db = client.test


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name


# 文章表
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(80), unique=True)
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    content = db.Column(db.Text)
    category = db.relationship('Category', backref=db.backref('file', lazy='dynamic'))

    def __init__(self, title, created_time=datetime.utcnow(),category=Category(''), content=''):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content

    # 向文章添加标签
    def add_tag(self, tag_name):
        # 为当前文章添加 tag_name 标签存入到 MongoDB
        if tag_name not in self.tags:
            tag_info = {'title': self.title, 'tag_name': tag_name}
            mongo_db.tag.insert_one(tag_info)

    # 移除标签
    def remove_tag(self, tag_name):
        # 从 MongoDB 中删除当前文章的 tag_name 标签
        where = {'title': self.title, 'tag_name': tag_name}
        mongo_db.tag.remove(where)

    # 标签列表
    @property
    def tags(self):
        # 读取 mongodb，返回当前文章的标签列表
        result = []
        where = {'title': self.title}
        for tag in mongo_db.tag.find(where):
            result.append(tag['tag_name'])
        return result

    def __repr__(self):
        return '<File %r>' % self.title


def get_file_data():
    data = []
    for id, title in db.session.query(File.id, File.title):
        file_instance = File(title)
        data.append({'id': id, 'title': title, 'tags': file_instance.tags})
    return data


def get_data_byid(id):
    result = {}
    data = db.session.query(File.id, File.title, File.created_time, File.content).filter_by(id=id)
    for id, title,created_time,content in data:
        result = {'id': id, 'title':title, 'created_time':created_time, 'content':content}
        return result


if __name__ == '__main__':
    # db.create_all()
    # # 增加 MySQL 中的数据
    # java = Category('Java')
    # python = Category('Python')
    # file1 = File('Hello Java', datetime.utcnow(), java, 'File Content - Java is cool!')
    # file2 = File('Hello Python', datetime.utcnow(), python, 'File Content - Python is cool!')
    # db.session.add(java)
    # db.session.add(python)
    # db.session.add(file1)
    # db.session.add(file2)
    # db.session.commit()
    #
    # # 增加 MongoDB 中的数据
    # file1.add_tag('tech')
    # file1.add_tag('java')
    # file1.add_tag('linux')
    # file2.add_tag('tech')
    # file2.add_tag('python')
    #
    # result = file1.tags
    # file1.remove_tag('tech')
    # file1.remove_tag('aa')
    # print(result)
    print(get_file_data())
    for data in get_file_data():
        print(data['id'])







