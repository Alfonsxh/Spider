"""
@author: Alfons
@contact: alfons_xh@163.com
@file: DoubanMovieInfoSqlManager.py
@time: 18-12-25 下午9:49
@version: v1.0 
"""
import logging
import traceback
import sqlalchemy
from sqlalchemy import MetaData, Table, Column, String
from sqlalchemy.sql import select

from .DoubanDbEngine import engine


def __GetMovieInfoTable(meta):
    """
    获取电影信息表，如果数据库中存在，使用autoload的方式加载
    :return: 电影信息表
    """
    try:
        return Table("MovieInfo", meta, autoload=True)
    except sqlalchemy.exc.NoSuchTableError:
        MovieInfoTableTmp = Table("MovieInfo", meta,
                                  Column(), )
        MovieInfoTableTmp.Creat()
        return MovieInfoTableTmp


# 电影信息表
MovieInfoTable = None


# ------------------------------------- 外部调用接口 -------------------------------------------
def StartDB():
    """
    激活数据库
    :return:
    """
    global MovieInfoTable

    meta = MetaData(bind=engine)
    MovieInfoTable = __GetMovieInfoTable(meta)


def FetchData(movie_id):
    """
    根据电影编号查找电影链接信息
    :param movie_id: 电影ID
    :return: 成功返回电影信息，失败返回None
    """
    try:
        fetch = select([MovieInfoTable]). \
            where(MovieInfoTable.c.id == movie_id)
        return engine.execute(fetch).fetchall()
    except:
        logging.error("[sqlerror] MovieLinksTable fetch data error!\n{}".format(traceback.format_exc()))
        return None


def UpdateData(movie_id, movie_title, movie_url):
    """
    更新电影信息
    :param movie_id: 电影编号
    :param movie_title: 电影名称
    :param movie_url: 电影链接地址
    :return: 成功返回True，失败返回False
    """
    try:
        update = MovieInfoTable.update().values(title=movie_title, url=movie_url). \
            where(MovieInfoTable.c.id == movie_id)

        engine.execute(update)
        return True
    except:
        logging.error("[sqlerror] MovieLinksTable update data error!\n{}".format(traceback.format_exc()))
        return False


def InsertData(movie_id, movie_title, movie_url):
    """
    插入电影信息
    :param movie_id: 电影编号
    :param movie_title: 电影名称
    :param movie_url: 电影链接地址
    :return: 成功返回True，失败返回False
    """
    try:
        isExist = FetchData(movie_id)
        if isExist:
            return UpdateData(movie_id, movie_title, movie_url)

        insert = MovieInfoTable.insert().values(id=movie_id, title=movie_title, url=movie_url)
        engine.execute(insert)
        return True
    except:
        logging.error("[sqlerror] MovieLinksTable insert error!\n{}".format(traceback.format_exc()))
        return False
