"""
@author: Alfons
@contact: alfons_xh@163.com
@file: DoubanMovieLinksSqlManager.py
@time: 18-12-23 下午9:23
@version: v1.0 
"""
import traceback
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, String
from sqlalchemy.sql import select

from ConfigManager.ConfigManager import ConfigManagerInstance as ConfigManager


def __GetEngine():
    """
    获取引擎函数
    :return: 数据库存在则返回引擎，不存在先创建，再返回
    """
    try:
        engineTmp = create_engine("mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}?charset=utf8".format(user=ConfigManager.mysql_user,
                                                                                                                 password=ConfigManager.mysql_password,
                                                                                                                 host=ConfigManager.mysql_host,
                                                                                                                 port=ConfigManager.mysql_port,
                                                                                                                 dbname=ConfigManager.dbname_douban_movie),
                                  encoding='utf-8', echo=False)
        engineTmp.connect()
        return engineTmp
    except:
        engineTmp = create_engine("mysql+pymysql://{user}:{password}@{host}:{port}".format(user=ConfigManager.mysql_user,
                                                                                           password=ConfigManager.mysql_password,
                                                                                           host=ConfigManager.mysql_host,
                                                                                           port=ConfigManager.mysql_port),
                                  encoding='utf-8', echo=False)
        engineTmp.execute("CREATE DATABASE IF NOT EXISTS {dbname} CHARACTER SET utf8 COLLATE utf8_general_ci;".format(dbname=ConfigManager.dbname_douban_movie))
        return __GetEngine()


engine = None  # 引擎
meta = None


def __GetMovieLinksTable():
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
    global engine
    global meta
    global MovieLinksTable

    engine = __GetEngine()
    meta = MetaData(bind=engine)

    MovieLinksTable = __GetMovieLinksTable()


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
        print("[*] MovieLinksTable fetch data error!\n{}".format(traceback.format_exc()))
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
        print("[*] MovieLinksTable update data error!\n{}".format(traceback.format_exc()))
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
        print("[*] MovieLinksTable insert error!\n{}".format(traceback.format_exc()))
        return False


if __name__ == '__main__':
    movie_id = "123456"
    movie_title = "非常好看2"
    movie_url = "http://baidu.com"
    print(InsertData(movie_id, movie_title, movie_url))
