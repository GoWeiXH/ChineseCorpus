import datetime
import os


class Operator:

    """
    日志操作类
    """

    def __init__(self, log):
        self.log = log
        self.logName = self.__format(datetime.date.today())
        self.logPath = os.getcwd() + "\logs\\"
        # 判断日志目录是否存在，不存在则创建
        if not os.path.exists(self.logPath):
            os.mkdir(self.logPath)

    @classmethod
    def __format(cls, date):
        """
        格式化日期，将横线替换为下划线
        :param date: 日期 date
        :return: 日期 str
        """
        return date.__str__().replace("-", "_")

    def output(self):
        """
        按照等级规则对日志内容进行输出
        DEBUG 等级只在控制台打印
        """
        if self.log.level not in ["DEBUG"]:
            self.log.to_file(self.logPath, self.logName)
        self.log.to_console()

    @staticmethod
    def modify(self):
        """
        修改日志文件名称，将前一日的日志修改为完成状态
        """
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)

        last_log_file_path = self.logPath + self.__format(yesterday) + ".log"
        finished_log_file_path = self.logPath + self.__format(yesterday) + "_finished.log"

        os.rename(last_log_file_path, finished_log_file_path)
