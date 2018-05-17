import time
import requests
import threading
from zhidao_reset01 import config
from IPPool_new_04_16 import Util
import random
from queue import Queue

# TEXT_Exit = False
class ThreadUpBrower_get_id(threading.Thread):
    def __init__(self, threadName, idQueue, threadQueue):
        super(ThreadUpBrower_get_id, self).__init__()
        self.threadName = threadName
        self.datalist = []
        # self.lock = lock
        self.idQueue = idQueue
        self.threadQueue = threadQueue


    def run(self):
        print("启动"+ self.threadName + "。。。")
        print("将id和threadId从数据库中提出。。。。")
        self.get_id_Mysql()
        time.sleep(0.5)
        print("操作完成。。。")
        print("结束"+ self.threadName + "！！！")


    def get_id_Mysql(self):
        """
            作用:从数据库中获取id和threadId
        :return:
        """
        conn = config.conn
        cursor = conn.cursor()
        # cursor2 = conn.cursor()
        try:
            sql = "select id from zhidao_formal_a"
            # sql2 = "select threadId from zhidao_formal_a"
            cursor.execute(sql)
            # cursor2.execute(sql2)
            id_list = cursor.fetchall()
            # thread_list = cursor2.fetchall()
            print("将提取的id，放入队列...")
            for i in id_list:
                time.sleep(0.01)
                self.idQueue.put(i[0])
                print("目前提取id数量：" + str(self.idQueue.qsize()))
            # for i in thread_list:
            #     time.sleep(0.05)
            #     self.threadQueue.put(i[0])
            #     print("目前提取threadId数量：" + str(self.threadQueue.qsize()))
        except SystemExit as e:
            print("无法提取数据。。。。")
        conn.commit()
        # cursor.close()
        # conn.close()


class ThreadUpBrower_return_data(threading.Thread):
    def __init__(self, threadName, idQueue, lock, dataQueue):
        super(ThreadUpBrower_return_data, self).__init__()
        self.threadName = threadName
        self.lock = lock
        self.idQueue = idQueue
        self.dataQueue = dataQueue

    def run(self):
        print("启动"+ self.threadName + "。。。")
        while True:
            try:
                id = self.idQueue.get(False)
                time.sleep(1)
                self.requests_url(id)
            except:
                if self.idQueue.empty() == True:
                    print("idQueue队列为空，结束\t\t\t来自:"+ self.threadName)
                    break
        # self.lock2.acquire()
        # self.update_Mysql(1180301324979251139,20)
        # self.lock2.release()

        print("结束"+ self.threadName + "！！！")

    def requests_url(self, id_list):
        """
            作用：根据id发送请求，返回浏览数
        :param id:
        :return:
        """
        url = "http://zhidao.baidu.com/api/qbpv?q=" + str(id_list)
        headers = config.headrs_other
        headers["Referer"] = "https://zhidao.baidu.com/question/" + str(id_list) + ".html"
        time.sleep(random.randint(1,3))
        items = {}
        """
            说明：
            1、随机休眠1-3秒后，发送请求，如果返回响应码为200，则将返回问题浏览数传入下一个函数写入
            2、如果请求发送超时，则使用try捕获，并且再次休眠1-3秒，然后发送请求
            3、并且如果发送请求超时次数达到60次，则启动IP池更新api，自动去网上抓取免费代理
            4、只有获取浏览数返回值之后，线程才能跳出循环，进入下一个步奏。
        """
        while True:
            try:
                time.sleep(random.randint(1, 3))
                browers_html = requests.get(url, headers=headers, proxies=Util.Get(), timeout = 8)
                if browers_html.status_code == 200:
                    browers_num = browers_html.text
                    #将返回的浏览次数和id一起传入更新函数
                    items = {
                        "id_list":id_list,
                        "browers":browers_num
                    }
                    self.dataQueue.put(items)
                    # print(items)
                    # print(browers_num)
                    break
            except:
                pass
            print("发送不成功，休息后再次发送请求。。" + self.threadName + "操作中。。。。(出现问题的id是  " + id_list + "  )")
            time.sleep(random.randint(1, 3))
            # 上锁，以免多线程混乱计数器
            self.lock.acquire()
            global count_num
            count_num += 1
            self.lock.release()
            # 当计数器到达50 的时候重新更新IP池，并且计数器清零
            if count_num == 60:
                print("开始更新ip池")
                Util.Refresh()
                count_num = 0
                print("IP池更新结束，继续运行程序")
            print(count_num)
        print("循环结束" + self.threadName)
        # json文件
        # self.print_json(browers_html)
        # self.print_json(json.loads((browers_html)))


class ThreadSave(threading.Thread):
    def __init__(self, threadName, dataQueue, lock2):
        super(ThreadSave,self).__init__()
        self.threadName = threadName
        self.lock2 = lock2
        self.dataQueue = dataQueue


    def run(self):
        print("启动\t" + self.threadName)
        conn = config.conn
        cursor = conn.cursor()
        sql = """UPDATE zhidao_formal_a
                     SET browse_num=%s
                     WHERE id = %s
                    """
        for i in range(self.dataQueue.qsize()):
            items = self.dataQueue.get(False)
            try:
                time.sleep(0.5)
                cursor.execute(sql, [items["browers"], items["id_list"]])
                conn.commit()
                print("更新成功 =-=\t\t来自能干的:\t" + self.threadName)
            except:
                pass
        cursor.close()
        conn.close()
        print("结束\t" + self.threadName)

TEXT_Exit = False
count_num = 0
def main():
    lock = threading.Lock()
    lock2 = threading.Lock()
    # Util.Refresh()
    idQueue = Queue()
    threadQueue = Queue()
    dataQueue = Queue()
    a1 = ThreadUpBrower_get_id("1号提取id线程", idQueue, threadQueue)
    a1.start()
    a1.join()
    print("<==id提取完毕，接下来启动线程补全获得浏览数==>")

    requests_url_list = ["补全\更新线程1号","补全\更新线程2号","补全\更新线程3号","补全\更新线程4号","补全\更新线程5号","补全\更新线程6号","补全\更新线程7号","补全\更新线程8号","补全\更新线程9号","补全\更新线程10号"]
    requests_list = []
    for threadName in requests_url_list:
        thread = ThreadUpBrower_return_data(threadName, idQueue, lock, dataQueue)
        thread.start()
        requests_list.append(thread)

    for temp_join in requests_list:
        temp_join.join()

    threadsave1 = ThreadSave("存储线程1号", dataQueue, lock2)
    threadsave1.start()

    while not dataQueue.empty():
        pass

    global TEXT_Exit
    TEXT_Exit = True

    threadsave1.join()
    print("储存线程全部结束=。=")

    # 开始发送请求的线程
    # Util.Refresh()
    print("主线程结束")


if __name__ == "__main__":
    main()
    # Util.Refresh()