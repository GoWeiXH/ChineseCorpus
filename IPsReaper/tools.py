# -*- coding: utf-8 -*-
class Tools:
    """
    此类包含了一些处理工具（方法）
    """

    @staticmethod
    def print_dict(dict_data):
        """
        将传入的字典对象进行格式化打印
        :param dict_data: 字典数据
        """
        for key, value in dict_data.items():
            print("{0}: {1}".format(key, value))

    @staticmethod
    def print_format(str_data):
        """
        将传入的字符串进行格式化打印
        :param str_data: 字符串数据
        """
        print("-"*20 + str_data + "-"*20)

    @staticmethod
    def strip(str_data):
        """
        删除 str中的 ['\n','\r' ,'\t',' ']
        :param str_data:旧字符串
        :return:删除后的字符串
        """
        # todo update in re
        if str_data is not None:
            new_str = str_data.replace("\n", "").replace(" ", "").replace("\r", "").replace("\t", "")
            return new_str
        else:
            return None

    @staticmethod
    def count_ip(abs_path):
        """
        统计此次任务最终保存的ip数量，并打印
        :param abs_path: 存储 ips_ok.txt 的绝对路径
        """
        ok_txt = len(open(abs_path+"\\"+"ips_ok.txt", "rt").readlines())
        print("The number of available ip is {0}".format(ok_txt))
