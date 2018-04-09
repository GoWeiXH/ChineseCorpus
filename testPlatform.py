from toolBox import toolBox
from DBOperator import csvDB
import random
import csv
import sys


def run04():
    db = csvDB.CSVOperator("CSVdatabase")
    db.read_data("test")


def run03():
    db = csvDB.CSVOperator("CSVdatabase")
    d = (("b", "b1") for _ in range(10))
    db.append_data("test_", d)


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

