from LogOperator.operator import Operator
from LogOperator.log import Log

content = "{class_name} is loaded".format(class_name=__name__)
Operator(Log("INFO", [content])).output()
