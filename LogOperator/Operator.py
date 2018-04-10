import datetime
import os


class Operator:

    """
    日志操作类
    """

    def __init__(self):
        self.logName = self.__format(datetime.date.today())
        self.logPath = os.getcwd() + "\logs\\"

    @classmethod
    def __format(cls, date):
        """
        格式化日期，将横线替换为下划线
        :param date: 日期 date
        :return: 日期 str
        """
        date = date.__str__().replace("-", "_")
        return date

    def output(self, log):
        """
        按照等级规则对日志内容进行输出
        DEBUG 只在控制台打印
        :param log: 日志对象 log
        """
        if log.level not in ["DEBUG"]:
            log.to_file(self.logPath, self.logName)
        log.to_console()

    def modify(self):
        """
        修改日志文件名称，将前一日的文件名修改为完成状态
        """
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        last_log_file_path = self.logPath + self.__format(yesterday) + ".log"
        finished_log_file_path = self.logPath + self.__format(yesterday) + "_finished.log"
        os.rename(last_log_file_path, finished_log_file_path)
