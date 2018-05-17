"""
    项目"百度知道爬虫多线程测试
    时间:2018年05月13日20:26:29
"""

import threading
import time
import random
import requests
import re
import pymysql
from lxml import etree
from queue import Queue
from zhidao_reset01 import config
from IPPool_new_04_16 import Util

class threadCrawl_link_html(threading.Thread):
    def __init__(self, threadName, pageQueue, link_html_Queue, lock):
        super(threadCrawl_link_html, self).__init__()
        self.threadName = threadName
        self.pageQueue = pageQueue
        self.link_html_Queue = link_html_Queue
        self.lock = lock

    def run(self):
        print("开启first请求线程....代号:\t" + self.threadName)
        """
        第一种方法
        while True:
            try:
                page = self.pageQueue.get(False)
                time.sleep(1)
                # print(page)
                self.requests_html(page)
            except:
                if self.pageQueue.empty() == True:
                    print("pageQueue队列为空，结束\t\t\t来自:"+ self.threadName)
                    break
        """
        # 第二种方法
        while not first_Exit:
            try:
                page = self.pageQueue.get(False)
                time.sleep(1)
                # print(page)
                self.requests_html(page)
            except:
                pass
        print("结束first请求线程...代号:\t" + self.threadName)

    def requests_html(self, page):
        """
            作用：得到page，根据page组合url，发送请求，放入队列
        :param :
        :return:
        """
        url = "https://zhidao.baidu.com/search?word=%C4%CF%C4%FE%BB%E1%BC%C6&ie=gbk&site=-1&sites=0&date=0&pn="+ str(page) + "/"
        while True:
            try:
                time.sleep(random.randint(1, 3))
                html = requests.get(url, headers=config.headrs_other, proxies=Util.Get(), timeout=8)
                if html.status_code == 200:
                    html.encoding='gbk'
                    htmlText = html.text
                    self.link_html_Queue.put(htmlText)
                    break
            except:
                print("发送不成功，休息后再次发送请求。。(这里是threadCrawl_link_html线程)" + self.threadName )
                time.sleep(random.randint(1, 3))
                # 上锁，以免多线程混乱计数器
                self.lock.acquire()
                global clear_num
                clear_num += 1
                # 当计数器到达50 的时候重新更新IP池，并且计数器清零
                if clear_num == config.upIPPORT_NUM:
                    print("发送错误已达200次，更新IP池程序启动")
                    Util.Refresh()
                    clear_num = 0
                    print("IP池更新结束，继续运行程序")
                self.lock.release()
                print(clear_num)
        print("循环结束" + self.threadName + "\t\t\t\t当前link_html_Queue为:\t\t" + str(self.link_html_Queue.qsize()))
        # json文件
        # self.print_json(browers_html)
        # self.print_json(json.loads((browers_html)))

class threadParser_return_data1(threading.Thread):
    def __init__(self, threadName, link_html_Queue, second_link_list):
        super(threadParser_return_data1, self).__init__()
        self.threadName = threadName
        self.link_html_Queue = link_html_Queue
        self.second_link_list = second_link_list

    def run(self):
        print("开启"+ self.threadName +"线程")
        while not first_parser_Exit:
            try:
                time.sleep(3)
                html = self.link_html_Queue.get(False)
                self.parser(html)
            except:
                pass
        print("结束"+ self.threadName +"线程")

    def parser(self, html):
        content = etree.HTML(html)
        # 循环取出其中每个link链接，存入url队列，结束
        links_list = []
        re_id = re.compile(r"\d{5,}")
        node_list = content.xpath("//div/div/div/dl")
        for link in node_list:
            link_list = link.xpath('./dt/a[@class="ti"]/@href')[0]
            # 提取链接中的id
            id_list = re_id.findall(link_list)[0]
            # 提取提问日期
            date_list = link.xpath('./dd/span[@class="mr-8"]/text()')[0]
            # 提取提问者
            answerer = link.xpath('./dd/span/a[@target="_blank"]/text()')[0]#提取回答者

            # 将 id 和 link 列表以字典形式存入insert_MYSQL_data队列
            items = {
                "id":id_list,
                "link_list":link_list,
                "date_list":date_list,
                "answerer":answerer
            }
            # print(items)
            # links_list.append(items)
        # 将列表字典放入url队列
        # print(links_list)
            self.second_link_list.put(items)

class threadCrawl_secontHtml(threading.Thread):
    def __init__(self, threadName, second_link_list, second_htmlQueue, lock2):
        super(threadCrawl_secontHtml, self).__init__()
        self.threadName = threadName
        self.second_link_list = second_link_list
        self.second_htmlQueue = second_htmlQueue
        self.lock2 = lock2


    def run(self):
        print("开启" + self.threadName + "线程")
        while not second_Exit:
            try:
                html_items = self.second_link_list.get(False)
                print(html_items)
                print("*"*80)
                # for i in html_items:
                    # print("ojbk"*10)
                    # print(i)
                self.requests_url(html_items["link_list"], html_items["id"], html_items["date_list"], html_items["answerer"])
            except:
                pass
        print("关闭" + self.threadName + "线程")

    def requests_url(self, url, id_, date_list, answerer):
        # print("123321")
        while True:
            # try:
            # items = {}
            items_list = []
            try:
                time.sleep(random.randint(1, 3))
                # print(url)
                html = requests.get(url, headers=config.headrs_other, proxies=Util.Get(), timeout=8)
                # print("发送成功")
                if html.status_code == 200:
                    html.encoding='gbk'
                    htmlText = html.text
                    items = {
                        "id":id_,
                        "html":htmlText,
                        "date_list":date_list,
                        "answerer":answerer
                    }
                    # print(items)
                    # items_list.append(items)
                    self.second_htmlQueue.put(items)
                    print("当前second_html队列中有:\t\t\t\t" + str(self.second_htmlQueue.qsize()))
                    break
                # print("跳过if")
            except:
                print("发送不成功，休息后再次发送请求。。(这里是threadCrawl_secontHtml线程)" + self.threadName )
                time.sleep(random.randint(1, 3))
                # 上锁，以免多线程混乱计数器
                self.lock2.acquire()
                global clear_num
                clear_num += 1
                # 当计数器到达50 的时候重新更新IP池，并且计数器清零
                if clear_num == config.upIPPORT_NUM:
                    print("发送错误已达200次，更新IP池程序启动")
                    Util.Refresh()
                    clear_num = 0
                    print("IP池更新结束，继续运行程序")
                self.lock2.release()
                print(clear_num)

class threadParser_return_data2(threading.Thread):
    def __init__(self, threadName, second_htmlQueue, inset_dataQueue):
        super(threadParser_return_data2, self).__init__()
        self.threadName = threadName
        self.second_htmlQueue = second_htmlQueue
        self.inset_dataQueue = inset_dataQueue

    def run(self):
        print("开启" + self.threadName + "线程")
        # print("这里是解析线程:second_htmlQueue未被取，现在目前为:\t\t\t" + str(self.second_htmlQueue.qsize()))
        while not second_parser_Exit:
            try:
                dict_ = self.second_htmlQueue.get(False)
                # print("这里是解析线程:second_htmlQueue被取了一个，现在目前为:\t\t\t" + str(self.second_htmlQueue.qsize()))
                # for temp in dict_:
                    # print(temp)
                self.parsert(dict_["html"], dict_["id"], dict_["date_list"], dict_["answerer"])
            except:
                pass
        print("关闭" + self.threadName + "线程")

    def parsert(self, html, id_, date_list, answerer):
        # print("这里是\t\t\t" + self.threadName)
        # print(html)
        # print(id_)
        # 从second_htmlQueue队列中get次级页面的源码，并且解析，提取出所有的关键词，以字典的形式存入dataQueue队列
        print("进入解析")
        # print(html)
        content = etree.HTML(html)
        # print(content)
        questions = content.xpath('//div/div//h1[@accuse="qTitle"]/span/text()')  # 抓取问题
        questions_add = content.xpath('//div/div//div[@accuse="qContent"]/span/text()')  # 抓取问题补充
        comment_best = content.xpath('//div/div/pre[@accuse="aContent"]/text()')  # 抓取最佳答案
        # comment_best = comment_best.replace("\u3000", "")
        comment_common = content.xpath('//div/div/div[@accuse="aContent"]/span/text()') # 抓取普通答案
        items = {
            "id":id_,
            "answerer":answerer,
            "date_list":date_list,
            "questions":questions,
            "questions_add":questions_add,
            "comment_best":comment_best,
            "comment_common":comment_common
        }
        print(items)
        self.inset_dataQueue.put(items)

class threadInsert_Mysql(threading.Thread):
    def __init__(self, threadName, inset_dataQueue, lock3):
    # def __init__(self, threadName, lock3):
        super(threadInsert_Mysql, self).__init__()
        self.threadName = threadName
        self.inset_dataQueue = inset_dataQueue
        # self.itmes = config.test_items
        self.lock3 = lock3

    def run(self):
        print("启动"+ self.threadName + "线程")
        time.sleep(random.randint(1,2))
        conn = config.conn
        cursor = conn.cursor()
        while not insert_Exit:
            try:
                data_items = self.inset_dataQueue.get(False)
                # sql = "insert into zhidao_formal_a(id, answerer, date_list, questions, questions_add, comment_best, comment_common)VALUE (%s, %s, %s, %s, %s, %s, %s)"
                # print(sql)
                self.lock3.acquire()
                time.sleep(0.15)
                cursor.execute("""INSERT IGNORE INTO zHidao_formal_a(id, answerer, date_list, questions, questions_add, comment_best, comment_common)VALUE ("%s", "%s", "%s", "%s", "%s", "%s", "%s")"""%(data_items["id"], data_items["answerer"], data_items["date_list"], data_items["questions"], data_items["questions_add"], data_items["comment_best"], data_items["comment_common"]))
                conn.commit()
                self.lock3.release()
                print("插入成功")
            except SyntaxError:
                # print("插入失败")
                print("id重复，插入错误")

        print("结束"+ self.threadName + "线程")
        cursor.close()
        conn.close()



first_Exit = False
first_parser_Exit = False
second_Exit = False
second_parser_Exit = False
insert_Exit = False
clear_num = 0
def main():
    # 创建锁
    lock = threading.Lock()
    lock2 = threading.Lock()
    lock3 = threading.Lock()

    # 创建队列
    pageQueue = Queue()
    link_html_Queue = Queue()
    second_link_list = Queue()
    second_htmlQueue = Queue()
    inset_dataQueue = Queue()


    for i in range(1, 30):
        i = i *10
        pageQueue.put(i)
        print(pageQueue.qsize())

    first_crwal = ["列表爬虫1号", "列表爬虫2号", "列表爬虫3号", "列表爬虫4号"]
    first_swith = []
    for threadName in first_crwal:
        thread = threadCrawl_link_html(threadName, pageQueue, link_html_Queue, lock)
        thread.start()
        first_swith.append(thread)

    first_parser = ["解析初代1号", "解析初代2号"]#, "解析初代3号", "解析初代4号", "解析初代5号", "解析初代6号", "解析初代7号", "解析初代8号"]
    first_parser_swich = []
    for threadName in first_parser:
        thread = threadParser_return_data1(threadName, link_html_Queue, second_link_list)
        thread.start()
        first_parser_swich.append(thread)


    second_crwal = ["链接爬虫1号", "链接爬虫2号","链接爬虫3号","链接爬虫4号","链接爬虫5号","链接爬虫6号","链接爬虫7号","链接爬虫8号","链接爬虫9号","链接爬虫10号"]
    second_swith = []
    for threadName in second_crwal:
        thread = threadCrawl_secontHtml(threadName, second_link_list, second_htmlQueue, lock2)
        thread.start()
        second_swith.append(thread)


    second_parser = ["解析二代1号", "解析二代2号", "解析二代3号", "解析二代4号"]#, "解析二代5号", "解析二代6号", "解析二代7号", "解析二代8号", "解析二代9号", "解析二代10号"]
    second_parser_swith = []
    for threadName in second_parser:
        thread = threadParser_return_data2(threadName, second_htmlQueue, inset_dataQueue)
        thread.start()
        second_parser_swith.append(thread)

    # a = threadInsert_Mysql("测试存储", inset_dataQueue, lock3)
    # a.start()
    # insert_list = ["存储1号", "存储1号",]
    # insert_list_swith = []
    # for threadName in insert_list:
    #     thread = threadInsert_Mysql(threadName, inset_dataQueue, lock3)
    #     thread.start()
    #     insert_list_swith.append(thread)
    """
    第一种方法：
    for thread in first_swith:
        thread.join()
        print("1.1")

    while not link_html_Queue.empty():
        pass

    for thread in first_parser_swich:
        thread.join()
        print("1.2")
    """
    # 第二种方法
    # 等待pageQueue为空，采集线程退出循环
    while not pageQueue.empty():
        pass

    global first_Exit
    first_Exit = True

    print("pageQueue为空")

    for thread in first_swith:
        thread.join()
        print("1.1 over")

    while not link_html_Queue.empty():
        pass

    global first_parser_Exit
    first_parser_Exit = True

    for thread in first_parser_swich:
        thread.join()
        print("1.2 over")

    while not second_link_list.empty():
        pass

    global second_Exit
    second_Exit = True

    for thread in second_swith:
        thread.join()
        print("2.1 over")

    while not second_htmlQueue.empty():
        pass

    global second_parser_Exit
    second_parser_Exit = True

    for thread in second_parser_swith:
        thread.join()
        print("2.2 over")

    a = threadInsert_Mysql("测试存储", inset_dataQueue, lock3)
    a.start()
    a.join()
    print("3 over")

    # while not inset_dataQueue.empty():
    #     pass
    #
    # global insert_Exit
    # insert_Exit = True
    #
    # for thread in insert_list_swith:
    #     thread.join()
    #     print("3 over")


    print("程序结束，谢谢使用！！！！！")


if __name__ == "__main__":
    # Util.Refresh()
    main()
    # lock3 = threading.Lock()
    # thread = threadInsert_Mysql("1号", lock3)
    # thread.start()
    # thread.join()
    # print("结束")