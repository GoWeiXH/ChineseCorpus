"""
利用 Sogou 问问的接口获取问答语料库
"""

from urllib.parse import quote_plus
from urllib.request import Request
from urllib import request
from random import choice
import json
import time
import os
import re

from bs4 import BeautifulSoup
import jieba

from utils import get_ips

jieba.setLogLevel('INFO')


class SogouSpider:

    NAME = 'Sogou'

    DATA_PATH = 'corpus/Sogou_QA/'

    VIEWED_FILE = 'corpus/viewed/viewed_sogou.json'

    DOMAIN = 'https://www.sogou.com'

    # 搜索问题的链接
    QUERY_URL = 'https://www.sogou.com/sogou?query={0}&ie=utf8&insite=wenwen.sogou.com'

    # 获取相似问题的链接
    EXTEND_URL = 'https://wenwenfeedapi.sogou.com/sgapi/web/related_search_new?key={0}'

    HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) "
                             "AppleWebKit/600.5.17 (KHTML, like Gecko) "
                             "Version/8.0.5 Safari/600.5.17"}

    def __init__(self, num_query):
        self.num_query = num_query  # 搜索问题数量
        self.query_list = list()  # 待搜索问题列表
        self.current_query = None
        self.index = len(os.listdir(self.DATA_PATH))  # 文件编号
        self.viewed = self.init_viewed()  # 已搜索过的问题集合
        self.all_answer = list()  # 当前缓存中获取的答案列表

    def init_viewed(self):
        """
        初始化 viewed 列表，用以去重
        """
        try:
            with open(self.VIEWED_FILE, 'r', encoding='utf-8') as f:
                viewed = json.load(f).get('viewed')
                viewed = set(viewed)
        except FileNotFoundError:
            print('Viewed set is empty.')
            return set()
        else:
            print(f'Viewed set has {len(viewed)} elements')
            return viewed

    def save_viewed(self):
        """
        保存已经搜索过的问题
        """
        with open(self.VIEWED_FILE, 'w', encoding='utf-8') as f:
            viewed = {'viewed': list(self.viewed)}
            json.dump(viewed, f, ensure_ascii=False)

    def get_html_ori(self, url):
        """
        不使用代理 ip
        """
        req = Request(url, headers=self.HEADERS)
        response = request.urlopen(req, timeout=3)
        html = response.read().decode('utf8')  # 读取后数据为 bytes，需用 utf-8 进行解码
        html = BeautifulSoup(html, 'html.parser')
        return html

    def get_html(self, url):
        """
        访问 url，并转换成 BeautifulSoup 类型
        """
        # time.sleep(0.5)

        ps, ips = get_ips()

        def get_resp():
            index = choice(range(len(ps)))
            try:
                proxy = request.ProxyHandler({ps[index]: ips[index]})
                request.install_opener(request.build_opener(proxy))
                req = Request(url, headers=self.HEADERS)
                response = request.urlopen(req, timeout=3)
            except Exception as e:
                print(e, f'{ps[index]}://{ips[index]}')
                ps.pop(index)
                ips.pop(index)
                return get_resp()

            return response

        resp = get_resp()

        html = resp.read().decode('utf8')  # 读取后数据为 bytes，需用 utf-8 进行解码
        html = BeautifulSoup(html, 'html.parser')
        return html

    def collect_answers(self, query):
        """
        从搜索结果页面中收集答案
        """
        query = quote_plus(query)
        query_url = self.QUERY_URL.format(query)
        html = self.get_html(query_url)
        answer_list = html.select('.vrwrap')
        return answer_list

    def extract_skip_url(self, url):
        """
        从跳转页面中提取出目标 url
        """
        html = self.get_html(url)
        skip_url = html.select('meta')[1].attrs.get('content')
        skip_url = re.findall("URL=\\\'(.+)", skip_url)[0][:-1]
        return skip_url

    def extract_answer(self, answer_list):
        """
        提取问题的最佳答案
        将问题内容、标签、答案内容整合成一条数据
        """

        for answer in answer_list:

            a = answer.select_one('.vrTitle a')

            # 获取跳转链接
            link = self.DOMAIN + a.attrs.get('href')
            url = self.extract_skip_url(link)
            html = self.get_html(url)

            # 获取问题标题与标签
            section = html.select('.main .section')[0]
            title = re.sub(r'[\?？]+', '', section.select_one('#question_title span').text)
            tag = section.select_one('.tags a').text

            # 获取答案相关
            section = html.select('.main .section')[1]
            content = section.select_one('#bestAnswers .replay-info pre')
            if content is None:
                content = section.select_one('.replay-section.answer_item .replay-info pre')
            content = content.text
            content = re.sub(r'\s+', '', content)  # 去除空格字符，包括：\r \n \r\n \t 空格
            content = content.split('。')[0].split('！')[0]
            content = re.sub(r'["“”]', '', content) + '。'

            # 构建成一条答案，并添加至答案结果列表
            answer = {'title': title, 'tag': tag, 'content': content}
            self.all_answer.append(answer)
            print(f"Add '{title}': {url}")

    def save_corpus(self):
        """
        以 json 文件形式存储搜索到的问答语料库
        """
        qa = {'data': self.all_answer}
        filename = f'{self.DATA_PATH}/{self.NAME}_QA_{self.index}.json'  # 利用索引设定文件名
        with open(filename, 'w', encoding='utf8') as f:
            json.dump(qa, f, ensure_ascii=False)  # ensure_ascii=False 表示非 ASCII 存储
            print(f'Saved data: {filename}, query: {self.current_query} length: {len(self.all_answer)}')
            self.index += 1  # 更新文件名称
        self.all_answer = list()  # 保存之后对缓存列表初始化

    def extend_question(self, query):
        """
        根据问题搜索相近问题，做延伸搜索
        """
        query = quote_plus(query)
        extend_url = self.EXTEND_URL.format(query)
        req = Request(extend_url, headers=self.HEADERS)
        resp = request.urlopen(req).read().decode('utf8')
        extend_query_list = json.loads(resp).get('data')
        if extend_query_list is not None:
            self.query_list += extend_query_list  # 将相近问题添加至待搜索问题列表

    def extract_question(self, query):
        words = jieba.lcut_for_search(query)
        self.query_list += words

    def run(self, query):

        self.query_list.append(query)   # 初始化搜索问题

        # 对问题进行延伸
        self.extend_question(query)
        # self.extract_question(query)

        for epoch in range(self.num_query):

            # 对问题进行查重并搜索答案
            query = self.query_list.pop(0)
            if query not in self.viewed:
                self.viewed.add(query)
                self.current_query = query
                print(f'Query --- {query}')
                answers = sgs.collect_answers(query)
                sgs.extract_answer(answers)

            # 当已搜索问题达到一定数量，则保存
            if len(self.all_answer) >= 1000:
                self.save_corpus()

        self.save_viewed()  # 当一次任务结束后，保存已搜索问题


def load_question():
    with open('question_to_learn.txt', 'r', encoding='utf-8') as f:
        questions = list()
        for line in f.readlines():
            questions.append(line.strip())
        return questions


init = '天气'
# sgs = SogouSpider(10000)
sgs = SogouSpider(10)
try:
    for que in load_question():
        sgs.run(que)
except Exception as e:
    print(e)
    sgs.save_viewed()
    sgs.save_corpus()
