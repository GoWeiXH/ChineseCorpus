from DBOperator import csvOperator
from LogOperator.log import Log
import toolBox
import random
import csv
import sys


def run05():
    logger = Log("info", "test_log")
    logger.to_file({"msg": "testing1"})
    logger.to_file({"msg": "testing2"})
    logger.to_console({"msg": "testing1"})
    logger.to_console({"msg": "testing2"})


def run04():
    db = csvOperator.CSVOperator("CSVDatabase")
    db.read_data("test")


def run03():
    db = csvOperator.CSVOperator("CSVDatabase")
    d = (("b", "b1") for _ in range(10))
    db.save_data("test_", d)


def run02():
    with open("data.csv", "r") as f:
        csv_reader = csv.reader(f)
        print(sys.getsizeof(csv_reader))
        for row in csv_reader:
            print(row)


def run01():
    with open("data.csv", "w", newline="") as f:
        csv_writer = csv.writer(f)
        key_lib = ['a', 'b', 'c', 'd']
        count = 1000000
        for _ in range(count):
            csv_writer.writerow((random.choice(key_lib), str(random.randint(10, 50))))


def run00():
    result = toolBox.match_string("a", "b")
    return result


run05()
