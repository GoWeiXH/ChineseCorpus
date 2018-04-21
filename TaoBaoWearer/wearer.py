# -*- coding: UTF-8 -*-
from DBOperator.csvOperator import CSVOperator
from bs4 import BeautifulSoup
import toolBox as Box
import requests
import json
import re


class Wearer:

    @staticmethod
    def _get_html(url):
        html = requests.get(url).text
        return html

    def test(self):
        url = "https://s.taobao.com/list?cat=16&q=衬衫"
        html = self._get_html(url).encode("utf-8").decode("unicode-escape")
        Box.save_file("item_list_page.html", html)

    def get_items(self, url):
        bs = BeautifulSoup(self._get_html(url), "html.parser")
        items_data = re.findall("(?<=g_page_config = ).*};", bs.select("script")[7].text)[0][0:-1]
        items_json = json.loads(items_data)

        # mainInfo > traceInfo > traceData > allCategories | auctionNids
        items_data = items_json.get("mainInfo").get("traceInfo").get("traceData")
        items_cate = items_data.get("allCategories")
        items_id = items_data.get("auctionNids")
        # https://detail.tmall.com/item.htm?id=……
        items_list = []
        for item_cate, item_id in zip(items_cate, items_id):
            item_url = "https://detail.tmall.com/item.htm?id=" + item_id
            items_list.append((item_cate, item_id, item_url))

        # todo 断点续爬，auction行信息补全，id去重
        CSVOperator("auction").save_data("auction", items_list)
        return items_list

    def category_clothing(self):
        # 获取类别的html内容
        url = "https://www.taobao.com/markets/nvzhuang/taobaonvzhuang"
        bs = BeautifulSoup(self._get_html(url), "html.parser")
        selector = "#guid-312344 textarea"
        all_cate = bs.select(selector)[0].text.encode()

        # 将内容转换为json格式，提取出一级类别、二级类别及相应链接存储到数据库
        cate_list = []
        base = "https://s.taobao.com/list?cat={first_cate_id}&q={second_cate}"
        first_cate_list = json.loads(all_cate).get("cat_mian")
        for first_cate in first_cate_list:
            second_list = first_cate.get("cat_data")
            for item in second_list:
                first_cate_id = re.findall("(?<=cat=)\d+(?=&)", item.get("cat_url"))[0]
                url = base.format(first_cate_id=first_cate_id, second_cate=item.get("cat_name"))
                cate_list.append((first_cate.get("name"), first_cate_id, item.get("cat_name"), url))

        # 存储类别到数据库并返回数据
        CSVOperator("category").save_data("clothing", cate_list)
        return cate_list

    def category_jewelry(self):
        # 获取类别的html内容
        url = "https://www.taobao.com/market/peishi/zhubao.php"
        bs = BeautifulSoup(self._get_html(url), "html.parser")
        first_selector = "#guid-13993729158900 p"
        second_selector = "#guid-13993729158900 textarea"
        first_cate_list = bs.select(first_selector)
        second_cate_list = bs.select(second_selector)

        # 将内容转换为json格式，提取出一级类别、二级类别及相应链接存储到数据库
        cate_list = []
        base = "https://s.taobao.com/list?cat={first_cate_id}&q={second_cate}"
        for i, first_cate in enumerate(first_cate_list):
            first_cate_name = first_cate.text
            items = json.loads(second_cate_list[i].text).get("custom")
            for item in items:
                first_cate_id = re.findall("(?<=cat=)\d+(?=&)", item.get("cat_url"))[0]
                url = base.format(first_cate_id=first_cate_id, second_cate=item.get("cat_name"))
                cate_list.append((first_cate_name, first_cate_id, item.get("cat_name"), url))

        # 存储类别到数据库并返回数据
        CSVOperator("category").save_data("jewelry", cate_list)
        return cate_list
