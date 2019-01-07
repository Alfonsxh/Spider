"""
@author: Alfons
@contact: alfons_xh@163.com
@file: DoubanMovieLinksSqlManager.py
@time: 18-12-23 下午9:23
@version: v1.0 
"""
import logging
import traceback
import sqlalchemy
from sqlalchemy import MetaData, Table, Column, String
from sqlalchemy.sql import select

from SqlManager.DoubanDbEngine import engine


def __GetMovieLinksTable(meta):
    """
    获取电影链接表，如果数据库中存在，使用autoload的方式加载
    :return: 电影链接表
    """
    try:
        return Table("MovieLink", meta, autoload=True)
    except sqlalchemy.exc.NoSuchTableError:
        MovieLinksTableTmp = Table("MovieLink", meta,
                                   Column("id", String(64), primary_key=True, comment="movie's id"),
                                   Column("title", String(256), comment="movie's name"),
                                   Column("url", String(2048), comment="movie's link url")
                                   )
        MovieLinksTableTmp.create()
        return MovieLinksTableTmp


# 电影链接信息表
MovieLinksTable = None


# ------------------------------------- 外部调用接口 -------------------------------------------
def StartDB():
    """
    激活数据库
    :return:
    """
    global MovieLinksTable

    meta = MetaData(bind=engine)
    MovieLinksTable = __GetMovieLinksTable(meta)


def FetchData(movie_id):
    """
    根据电影编号查找电影链接信息
    :param movie_id: 电影ID
    :return: 成功返回电影信息，失败返回None
    """
    try:
        fetch = select([MovieLinksTable]). \
            where(MovieLinksTable.c.id == movie_id)
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
        update = MovieLinksTable.update().values(title=movie_title, url=movie_url). \
            where(MovieLinksTable.c.id == movie_id)

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

        insert = MovieLinksTable.insert().values(id=movie_id, title=movie_title, url=movie_url)
        engine.execute(insert)
        return True
    except:
        logging.error("[sqlerror] MovieLinksTable insert error!\n{}".format(traceback.format_exc()))
        return False


def GetAllMovie():
    """
    获取表中所有电影的id
    :return: 所有电影的id
    """
    try:
        fetch = select([MovieLinksTable])
        return engine.execute(fetch).fetchall()
    except:
        logging.error("[sqlerror] MovieLinksTable get all movie id error!\n{}".format(traceback.format_exc()))
        return None


if __name__ == '__main__':
    # movieid = "123456"
    # movietitle = "非常好看2"
    # movieurl = "http://baidu.com"
    # print(InsertData(movieid, movietitle, movieurl))
    StartDB()
    all_id = GetAllMovie()
    for i in all_id:
        print(i.id, i.title, i.url)
    pass
