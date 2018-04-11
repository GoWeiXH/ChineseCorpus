from DBOperator.dbException import *
from collections import Iterator
import csv
import os


class CSVOperator:
    """
    操作CSV数据库的类
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        单例模式创建 CSVOperator
        :param args:
        :param kwargs:
        :return:
        """
        if not cls._instance:
            cls._instance = super(CSVOperator, cls).__new__(cls)
        return cls._instance

    def __init__(self, database_name):
        self.databaseName = None
        self.databasePath = None

        # 设定数据库名称
        self.databaseName = "\\" + database_name
        # 判断数据库文件夹是否存在
        # 如果不存在则创建
        _base_path = os.getcwd() + "\\database"
        self.databasePath = _base_path + self.databaseName + "\\"
        result = os.path.exists(self.databasePath)
        if not result:
            os.makedirs(self.databasePath)

    def save_data(self, filename, data):
        """
        存储数据，以.csv文件形式存储。
        :param filename: 文件名称，无需.csv后缀
        :param data: 可迭代对象
        """
        complete_path = self.databasePath + filename + ".csv"
        with open(complete_path, "a", newline="") as f:
            # 判断data是否为可迭代对象，否则抛出异常
            if not isinstance(data, Iterator):
                raise ClassErrorException("variable data")
            csv_writer = csv.writer(f)
            csv_writer.writerows(data)

    def read_data(self, filename):
        """
        读取数据并返回。
        :param filename: 文件名称，无需.csv后缀
        :return: 可迭代对象 reader
        """
        complete_path = self.databasePath + filename + ".csv"
        # 判断要读取的文件是否存在，不存在则抛出异常
        if not os.path.exists(complete_path):
            raise FileNotFoundError(complete_path)
        with open(complete_path, "r") as f:
            rows = csv.reader(f)
            return rows
