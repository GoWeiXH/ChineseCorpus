# -*- coding: UTF-8 -*-
import json
import os


def match_string(a_str, b_str):
    """
    比较两个字符串是否一致
    :param a_str: 一个字符串（str）
    :param b_str: 另一个字符串（str）
    :return: 一致则返回True，不一致则返回False（bool）
    """
    return a_str == b_str


def save_file(name, data):
    """
    在当前文件目录存储文件
    :param name: 文件名称
    :param data: 要存储数据
    """
    base_path = "\\".join([os.getcwd(), "file", name.split(".")[1]])
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    file_path = base_path + "\\" + name
    with open(file_path, "w") as f:
        f.write(data)


def load_json(name):
    """
    读取son文件
    :param name:
    :return:返回json格式
    """
    base_path = "\\".join([os.getcwd(), "file", "json", name])
    with open(base_path, "r", encoding="utf-8") as f:
        return json.load(f)
