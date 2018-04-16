from DBOperator.csvOperator import CSVOperator
from bs4 import BeautifulSoup
import requests
import json


class Wearer:

    @staticmethod
    def _get_response(url, method="get"):
        response = requests.request(method, url).content
        return response

    def category_clothing(self):
        # 获取类别的html内容
        url = "https://www.taobao.com/markets/nvzhuang/taobaonvzhuang"
        bs = BeautifulSoup(self._get_response(url), "html.parser")
        selector = "#guid-312344 textarea"
        all_cate = bs.select(selector)[0].text.encode()

        # 将内容转换为json格式，提取出一级类别、二级类别及相应链接存储到数据库
        data = []
        first_cate_list = json.loads(all_cate).get("cat_mian")
        for first_cate in first_cate_list:
            second_list = first_cate.get("cat_data")
            for item in second_list:
                data.append((first_cate.get("name"), item.get("cat_name"), item.get("cat_url")))

        # 存储类别到数据库并返回数据
        CSVOperator("category").save_data("clothing", data)
        return data

    def category_jewelry(self):
        # 获取类别的html内容
        url = "https://www.taobao.com/market/peishi/zhubao.php"
        bs = BeautifulSoup(self._get_response(url), "html.parser")
        first_selector = "#guid-13993729158900 p"
        second_selector = "#guid-13993729158900 textarea"
        first_cate_list = bs.select(first_selector)
        second_cate_list = bs.select(second_selector)

        # 将内容转换为json格式，提取出一级类别、二级类别及相应链接存储到数据库
        data = []
        for i, first_cate in enumerate(first_cate_list):
            first_cate_name = first_cate.text
            items = json.loads(second_cate_list[i].text).get("custom")
            for item in items:
                data.append((first_cate_name, item.get("cat_name"), "https:"+item.get("cat_url")))

        # 存储类别到数据库并返回数据
        CSVOperator("category").save_data("jewelry", data)
        return data
