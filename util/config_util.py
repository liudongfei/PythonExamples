# -*- coding: utf-8 -*-
# @Time    : 2020/8/13 下午7:25
# @Author  : Mat
from configparser import ConfigParser
import configparser


class ConfigUtil:
    """
    配置文件工具类
    """
    @staticmethod
    def get_conf(file):
        if isinstance(file, str):
            conf = configparser.RawConfigParser()
            conf.read(file)
            return conf

    @staticmethod
    def read_conf_value(file, section, key):
        """
        从配置文件中获取指定配置项的值
        :param file: 配置文件
        :param section: 配置项段落
        :param key: 配置项的key
        :return: 配置项对应的值
        """
        if file or section or key:
            if isinstance(file, str):
                conf = configparser.RawConfigParser()
                conf.read(file)
            elif isinstance(file, ConfigParser):
                conf = file
            else:
                return None
            sections = conf.sections()
            if section not in sections:
                return None
            return conf[section][key]

    @staticmethod
    def read_conf_lvalue(file, section, key):
        """
        从配置文件中获取指定配置项的值
        :param file: 配置文件
        :param section: 配置项段落
        :param key: 配置项的key
        :return: 配置项对应的值
        """
        if file or section or key:
            if isinstance(file, str):
                conf = configparser.RawConfigParser()
                conf.read(file)
            elif isinstance(file, ConfigParser):
                conf = file
            else:
                return None
            sections = conf.sections()
            if section not in sections:
                return None
            return [val for val in conf[section][key].split(',')]

    @staticmethod
    def read_conf_values(file, section):
        """
        从配置文件中获取指定的配置段落
        :param file: 配置文件
        :param section: 配置项段落
        :return: 段落中的配置项字典
        """
        if file or section:
            if isinstance(file, str):
                conf = configparser.RawConfigParser()
                conf.read(file)
            elif isinstance(file, ConfigParser):
                conf = file
            else:
                return None
            sections = conf.sections()
            if section not in sections:
                return None
            values_dict = {}
            for (k, v) in conf.items(section):
                values_dict[k] = v
            return values_dict

    @staticmethod
    def write_conf_value(file, section, key, val):
        """
        添加指定的配置项到配置文件
        :param file: 配置文件路径
        :param section: 配置项段落
        :param key: 配置项的键
        :param val: 配置项的值
        :return: None
        """
        if file or section or key or val:
            conf = ConfigParser()
            conf.add_section(section)
            conf.set(section, key, val)
            conf.write(open(file, 'w'))

    @staticmethod
    def write_conf_values(file, section, dict_kvs):
        """
        添加多个配置项到配置文件中。
        :param file: 配置文件路径
        :param section: 配置项段落
        :param dict_kvs: 配置项内容字典
        :return: None
        """
        if file or section or dict_kvs:
            conf = ConfigParser()
            conf.add_section(section)
            for (k, v) in dict_kvs:
                conf.set(section, k, v)
            conf.write(open(file, 'w'))


if __name__ == '__main__':
    print(ConfigUtil.read_conf_lvalue('../conf/db_config_inner.ini', 'kafka', 'bootstrap_servers'))
