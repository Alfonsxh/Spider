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
from sqlalchemy import MetaData, Table, Column, String, JSON, Integer
from sqlalchemy.sql import select

from SqlManager.DoubanDbEngine import engine


def __GetMovieInfoTable(meta):
    """
    获取电影信息表，如果数据库中存在，使用autoload的方式加载
    :return: 电影信息表
    """
    try:
        return Table("MovieInfo", meta, autoload=True)
    except sqlalchemy.exc.NoSuchTableError:
        MovieInfoTableTmp = Table("MovieInfo", meta,
                                  Column("id", String(64), primary_key=True, comment="电影ID，唯一标识"),
                                  Column("name", String(256), nullable=False, comment="电影名称"),
                                  Column("url", String(256), nullable=False, comment="电影在豆瓣的链接"),
                                  Column("image", String(512), comment="电影海报"),
                                  Column("director", JSON(), comment="导演列表，人物ID"),
                                  Column("author", JSON(), comment="编剧列表，人物ID"),
                                  Column("actor", JSON(), comment="演员列表， 人物ID"),
                                  Column("country", String(512), comment="制片国家"),
                                  Column("datePublished", String(10), comment="发布日期"),
                                  Column("duration", String(10), comment="电影时长"),
                                  Column("genre", JSON(), comment="电影类型"),
                                  Column("description", String(1024), comment="电影描述"),
                                  Column("rateDetails", JSON(), comment="电影评分详情"),
                                  Column("rateNumber", Integer(), comment="电影评分数量"),
                                  Column("imdb", String(256), comment="imdb链接"))
        MovieInfoTableTmp.create()
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
        logging.error("[sqlerror] MovieInfoTable fetch data error!\n{}".format(traceback.format_exc()))
        return None


def UpdateData(movie_id, movie_name, movie_url, movie_image, movie_director,
               movie_author, movie_actor, movie_country, movie_date_published, movie_genre,
               movie_duration, movie_description, movie_rate_details, movie_rate_number, movie_imdb):
    """
    更新电影信息
    :param movie_id: 电影编号
    :param movie_name: 电影名称
    :param movie_url: 电影豆瓣链接地址
    :param movie_image: 电影海报
    :param movie_director: 导演
    :param movie_author: 编剧
    :param movie_actor: 演员
    :param movie_country: 电影制作国
    :param movie_date_published: 发布日期
    :param movie_genre: 类型
    :param movie_duration: 时长
    :param movie_description: 描述
    :param movie_rate_details: 评分详情
    :param movie_rate_number: 评分数量
    :param movie_imdb: imdb链接
    :return: 成功返回True，失败返回False
    """
    try:
        update = MovieInfoTable.update().values(name=movie_name,
                                                url=movie_url,
                                                image=movie_image,
                                                director=movie_director,
                                                author=movie_author,
                                                actor=movie_actor,
                                                country=movie_country,
                                                datePublished=movie_date_published,
                                                genre=movie_genre,
                                                duration=movie_duration,
                                                description=movie_description,
                                                rateDetails=movie_rate_details,
                                                rateNumber=movie_rate_number,
                                                imdb=movie_imdb). \
            where(MovieInfoTable.c.id == movie_id)

        engine.execute(update)
        return True
    except:
        logging.error("[sqlerror] MovieInfoTable update data error!\n{}".format(traceback.format_exc()))
        return False


def InsertData(movie_id, movie_name, movie_url, movie_image, movie_director,
               movie_author, movie_actor, movie_country, movie_date_published, movie_genre,
               movie_duration, movie_description, movie_rate_details, movie_rate_number, movie_imdb):
    """
    插入电影信息
    :param movie_id: 电影编号
    :param movie_name: 电影名称
    :param movie_url: 电影豆瓣链接地址
    :param movie_image: 电影海报
    :param movie_director: 导演
    :param movie_author: 编剧
    :param movie_actor: 演员
    :param movie_country: 电影制作国
    :param movie_date_published: 发布日期
    :param movie_genre: 类型
    :param movie_duration: 时长
    :param movie_description: 描述
    :param movie_rate_details: 评分详情
    :param movie_rate_number: 评分个数
    :param movie_imdb: imdb链接
    :return: 成功返回True，失败返回False
    """
    try:
        isExist = FetchData(movie_id)
        if isExist:
            return UpdateData(movie_id=movie_id,
                              movie_name=movie_name,
                              movie_url=movie_url,
                              movie_image=movie_image,
                              movie_director=movie_director,
                              movie_author=movie_author,
                              movie_actor=movie_actor,
                              movie_country=movie_country,
                              movie_date_published=movie_date_published,
                              movie_genre=movie_genre,
                              movie_duration=movie_duration,
                              movie_description=movie_description,
                              movie_rate_details=movie_rate_details,
                              movie_rate_number=movie_rate_number,
                              movie_imdb=movie_imdb)

        insert = MovieInfoTable.insert().values(id=movie_id,
                                                name=movie_name,
                                                url=movie_url,
                                                image=movie_image,
                                                director=movie_director,
                                                author=movie_author,
                                                actor=movie_actor,
                                                country=movie_country,
                                                datePublished=movie_date_published,
                                                genre=movie_genre,
                                                duration=movie_duration,
                                                description=movie_description,
                                                rateDetails=movie_rate_details,
                                                rateNumber=movie_rate_number,
                                                imdb=movie_imdb)
        engine.execute(insert)
        return True
    except:
        logging.error("[sqlerror] MovieInfoTable insert error!\n{}".format(traceback.format_exc()))
        return False


if __name__ == '__main__':
    import json

    StartDB()
    # InsertData("1234", "helloworld", "2321", "dsfasd", json.dumps(["lalons"]), json.dumps(["lalons"]), ["lalons"], "CN",
    #            "2018-12-26", json.dumps(["lalons"]), "1H68M", "hellosofd", {6: 0.45, 4: 0.44}, "dsfa")
    data = FetchData("1234")
    actor = data[0].actor
    rate = data[0].aggregateRating
    pass
