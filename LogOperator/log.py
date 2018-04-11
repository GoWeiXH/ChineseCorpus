from LogOperator.logException import *
import time


class Log:

    """
    日志类
    """

    def __init__(self, level, content):

        self.level = None
        self.content = content

        # 等级控制
        level_list = ("DEBUG", "INFO", "WARN", "ERROR")
        level = str.upper(level)
        if level not in level_list:
            raise LevelException(level)
        self.level = level

    def __format(self, content):
        """
        将要显示的信息格式化。
        :param content: 内容 str/list
        :return: 格式化后的内容 str
        """
        content = ". ".join([item for item in content])
        msg = "{level} - {datetime}: {content}"
        return msg.format(level=self.level, datetime=time.ctime(), content=content)

    def to_console(self):
        """
        将单行日志打印在控制台。
        """
        content = self.__format(self.content)
        print(content)

    def to_file(self, log_path, filename):
        """
        将单行日志写入日志文件。
        """
        content = self.__format(self.content) + "\n"
        file_path = log_path + filename + ".log"
        with open(file_path, "a") as f:
            f.write(content)
