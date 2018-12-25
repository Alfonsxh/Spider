"""
@author: Alfons
@contact: alfons_xh@163.com
@file: DoubanMoviePersonSqlManager.py
@time: 18-12-25 下午10:58
@version: v1.0 
"""
import logging
import traceback
import sqlalchemy
from sqlalchemy import MetaData, Table, Column, String
from sqlalchemy.sql import select

from .DoubanDbEngine import engine


def __GetPersonInfoTable(meta):
    """
    获取演职人员信息表，如果数据库中存在，使用autoload的方式加载
    :return: 演职人员信息表
    """
    try:
        return Table("PersonInfo", meta, autoload=True)
    except sqlalchemy.exc.NoSuchTableError:
        MovieInfoTableTmp = Table("PersonInfo", meta,
                                  Column(), )
        MovieInfoTableTmp.Creat()
        return MovieInfoTableTmp


# 电影信息表
PersonInfoTable = None
