from DBOperator.csvOperator import CSVOperator
from bs4 import BeautifulSoup
import toolBox as Box
import requests


class Wearer:

    @staticmethod
    def _get_response(url, method="get"):
        response = requests.request(method, url).content
        return response

    def category_clothing(self):
        # 获取类别的html内容并存储为json文件
        url = "https://www.taobao.com/markets/nvzhuang/taobaonvzhuang"
        response = self._get_response(url)
        bs = BeautifulSoup(response, "html.parser")
        selector = "#guid-312344 textarea"
        ul = bs.select(selector)[0].text.encode()
        Box.save_file("clothing.json", ul)

        # 加载json格式的类别内容，提取出一级类别、二级类别及相应链接存储到数据库
        db_op = CSVOperator("clothing_category")
        json_content = Box.load_json("clothing.json")
        first_category_list = json_content.get("cat_mian")
        data = []
        for first_cate in first_category_list:
            second_list = first_cate.get("cat_data")
            for second_cate in second_list:
                item = (first_cate.get("name"), second_cate["cat_name"], second_cate["cat_url"])
                data.append(item)

        db_op.save_data("clothing_category", data)

    def cat_jewelry(self):
        url = "https://www.taobao.com/market/peishi/zhubao.php"
        response = self._get_response(url)
        pass
