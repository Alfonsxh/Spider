"""
@author: Alfons
@contact: alfons_xh@163.com
@file: ConfigManager.py
@time: 18-12-23 下午9:34
@version: v1.0 
"""
import os
import sys
import configparser
import traceback

ConfigPath = "/home/alfons/.Spiders/Douban/Spider.conf"


class ConfigManager:
    def __init__(self, config_path=ConfigPath):
        self.mysql_host = None
        self.mysql_port = None
        self.mysql_user = None
        self.mysql_password = None

        self.dbname_douban_movie = None

        self.login_username = None
        self.login_password = None

        self.__ReadConfig(config_path)

    def __ReadConfig(self, config_path):
        try:
            if not os.path.isfile(config_path):
                sys.exit()

            reader = configparser.ConfigParser()
            reader.read(config_path)

            self.__GetMysqlBaseInfo(reader)
            self.__GetDbName(reader)
            self.__GetLoginInfo(reader)
        except:
            sys.stderr.write("[*] Read config error!\n{}".format(traceback.format_exc()))
            sys.exit()

    def __GetMysqlBaseInfo(self, reader: configparser.ConfigParser):
        self.mysql_host = reader.get("Mysql", "host")
        self.mysql_port = reader.getint("Mysql", "port")
        self.mysql_user = reader.get("Mysql", "user")
        self.mysql_password = reader.get("Mysql", "password")

    def __GetDbName(self, reader):
        self.dbname_douban_movie = reader.get("dbname", "Douban")

    def __GetLoginInfo(self, reader):
        self.login_username = reader.get("login", "username")
        self.login_password = reader.get("login", "password")


ConfigManagerInstance = ConfigManager()

if __name__ == '__main__':
    print(ConfigManagerInstance.mysql_host)
    print(ConfigManagerInstance.mysql_port)
    print(ConfigManagerInstance.mysql_user)
    print(ConfigManagerInstance.mysql_password)
