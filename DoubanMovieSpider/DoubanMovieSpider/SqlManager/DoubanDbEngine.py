"""
@author: Alfons
@contact: alfons_xh@163.com
@file: DoubanDbEngine.py
@time: 18-12-25 下午10:42
@version: v1.0 
"""
from sqlalchemy import create_engine
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


engine = __GetEngine()
