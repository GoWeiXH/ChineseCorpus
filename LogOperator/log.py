from LogOperator.logException import *
import time


class Log:

    """
    日志类
    属性：等级
          内容
    方法：to_console()
          to_file()
    """

    def __init__(self, level, content):

        self.level = None
        self.content = content

        # 等级控制
        level_list = {"DEBUG": 1,
                      "INFO": 2,
                      "WARN": 3,
                      "ERROR": 4}
        self.level = str.upper(level)
        if self.level not in level_list.keys():
            raise LevelException(level)

    def __format__(self, content):
        """
        将要显示信息格式化。
        :param content: 内容 str
        :return: 格式化后的内容 str
        """
        msg = "{0} - {1}: {2}".format(self.level, time.ctime(), content['msg'])
        return msg

    def to_console(self):
        """
        将单行日志打印在控制台。
        """
        content = self.__format__(self.content)
        print(content)

    def to_file(self, filename):
        """
        将单行日志写入日志文件。
        """
        content = self.__format__(self.content) + "\n"
        filename = filename + ".log"
        with open(filename, "a") as f:
            f.write(content)

