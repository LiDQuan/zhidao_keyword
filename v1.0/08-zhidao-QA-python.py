import urllib.request
from urllib import request
import random
import ssl
from lxml import etree
import re
import pymysql
import json
import IPProxyPool
import time
from IPPool_new_04_16 import Util

"""开始使用代理"""
# Util.Refresh()#启动ip池
proxy = Util.Get()  # 调用IP池接口
proxy_support = urllib.request.ProxyHandler({'http': proxy})
opener = urllib.request.build_opener(proxy_support)
urllib.request.install_opener(opener)
"""结束代理调用"""


class zhidao(object):

    def loadPage(self, url):
        """
            作用：根据url发送请求，获取服务器响应文件
            url：需要爬去的url地址
        :return:
        """

        #请求头列表
        headers_list = [
            {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1"},
            {"User-Agent":"Mozilla/5.0 (Macintosh;Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"},
            {"User_Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"},
            {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko"},
            {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0"}
        ]



        headers = random.choice(headers_list)#随机拿取请求头发送请求
        context = ssl._create_unverified_context()#创建一个证书ssl以便访问网站
        times = random.randint(2,7) #设置延迟，反爬虫
        time.sleep(times)
        requests = urllib.request.Request(url, headers = headers)#构建请求
        respones = urllib.request.urlopen(requests, context = context, timeout = 1000).read().decode("gbk")#解析网站xml
        content = etree.HTML(respones)#解析为html DOM模型


        # 第一种方法
        """
        # #进行匹配，返回列表集合，取出每个帖子里面的a标签，也就是每个帖子的链接
        # xpath_a = "//div/div/div/dl/dt/a[@class="ti"]/@href"
        # #匹配列表中的time时间
        # xpath_time = "//div/div/div/dl/dd/span[@class='mr-8']/text()"
        # 调用etree的xpath语法
        # link_list = content.xpath(xpath_a)
        """

        # 第二种方法

        node_list = content.xpath("//div/div/div/dl")   #返回所有节点的子节点

        re_id = re.compile(r"\d{5,}")  #调用正则表达式提取id


        for link in node_list:
            links = link.xpath('./dt/a[@class="ti"]/@href')[0] #提取链接
            date = link.xpath('./dd/span[@class="mr-8"]/text()')[0]#提取提问日期
            answerer = link.xpath('./dd/span/a[@target="_blank"]/text()')[0]#提取回答者
            id_list = re_id.findall(links)[0]
            items = {
                "links" : links,
                "date" : date,
                "id" : id_list,
                "answer" : answerer
            }

            self.write_insterData(id_list, links, date, answerer)#先将id、链接、提问日期插入mysql数据库
            # print(items)
            i = random.randint(2,7)#设置延迟
            time.sleep(i)
            self.loadQA(items["links"], items["id"]) #提取超链接中的浏览数，问题，普通答案和最佳答案

    def loadQA(self, link_list, id_list):
        """
            作用：取出每个链接里面的问题和答案、以及浏览次数
            link_list: 每个页面标题的超链接
            id_list: 每个url之中的id
        :return:
        """
        #请求头列表
        headers_list = [
            {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1"},
            {"User-Agent":"Mozilla/5.0 (Macintosh;Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"},
            {"User_Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"},
            {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko"},
            {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0"}
        ]
        #随机选择请求头，组合请求头
        headerTemp = random.choice(headers_list)
        headerTemp["Referer"] = "https://zhidao.baidu.com/question/" + str(id_list) + ".html"
        headers = headerTemp

        #创建证书认证
        context = ssl._create_unverified_context()

        #组合字符串
        browes_url = "http://zhidao.baidu.com/api/qbpv?q=" + str(id_list)

        requestsUrl = request.Request(link_list, headers = headers)#构建请求
        requestsBrowse = request.Request(browes_url, headers = headers)#构建请求返回浏览数


        #延迟随机数执行
        i = random.randint(2,5)
        time.sleep(i)
        respones = urllib.request.urlopen(requestsUrl, context = context).read().decode("gbk")#返回网页代码
        respones_browes = urllib.request.urlopen(requestsBrowse, context = context).read().decode("gbk")#返回浏览数

        #获取用户评论数(最佳答案)
        re_common_temp = re.compile(r'threadId:"(\d{4,})"') # 使用正则进行匹配
        re_common_num = re_common_temp.findall(respones)[0] # 返回该问题的threadId，用于拼接url

        
        common_url = "http://zhidao.baidu.com//api/comment?method=get_reply_count&app=qb&thread_id=" + str(re_common_num)
        requestCommon = urllib.request.Request(common_url, headers = headers)#构建请求
        respones_Common = urllib.request.urlopen(requestCommon, context=context).read().decode("gbk")#查看返回值


        # 测试返回值,用户评论数
        # print((json.loads(respones_Common))["res"][0]["total_count"])

        content = etree.HTML(respones)#解析为html DOm模型
        questions = content.xpath('//div/div//h1[@accuse="qTitle"]/span/text()')#抓取问题
        questions_add = content.xpath('//div/div//div[@accuse="qContent"]/span/text()')#抓取问题补充
        comment_best = content.xpath('//div/div/pre[@accuse="aContent"]/text()')#抓取最佳答案
        # comment_best_num = content.xpath('//div/section/article//div/span[@alog-action="qb-comment-btnbestbox"]/em/text()')#抓取最佳答案
        comment_common = content.xpath('//div/div/div[@accuse="aContent"]/span/text()')#抓取普通答案



        #测试抓取信息
        items = {
            "浏览次数" : json.loads((respones_browes)),
            "问题" : questions,
            "问题补充": questions_add,
            "最佳答案" : comment_best,
            "最佳答案评论数": (json.loads(respones_Common))["res"][0]["total_count"],
            "普通答案" : comment_common,
        }

        #更新数据库
        self.update_sql(
            id_list,
            items["浏览次数"],
            items["问题"],
            items["问题补充"],
            items["最佳答案"],
            items["最佳答案评论数"],
            items["普通答案"]
        )

        #测试写入文件
        # self.update_sql_write(id_list, items["浏览次数"], items["问题"], items["问题补充"], items["最佳答案"], items["最佳答案评论数"], items["普通答案"])
        """
        print(items)
        """

        #旧版返回所有节点
        """ 旧版
        # #返回所有节点
        # node_list = content.xpath("//div/div")
        #
        # #进行提取
        # for link in node_list:
        #     #抓取问题,只提取第一个
        #     question_list = link.xpath('.//h1[@accuse="qTitle"]/span/text()')[0]
        #     #抓取最佳答案
        #     commentBest_list = link.xpath('./pre[@accuse="aContent"]/text()')[0]
        #     #抓取普通答案
        #     commentCommon_list = link.xpath('./div[@accuse="aContent"]/span/text()')[0]
        #
        #     items = {
        #         "问题" : question_list,
        #         "最佳答案" : commentBest_list,
        #         "普通答案" : commentCommon_list
        #     }
        #
        #     print(items)
        """

    def update_sql(self, id_list, respones_browes, questions, questions_add, comment_best, respones_Common, comment_common):
        """
            作用：将获取到的浏览数(respones_browes)，问题(questions)，问题补充(questions_add), 最佳答案(comment_best), 最佳答案评论数(respones_Common), 普通答案(comment_common)以更新的形式存入数据库，以id_list为主键
        """
        conn = pymysql.connect(host = 'localhost', port = 3306, db = 'python4', user = 'root', passwd = '123456', charset = 'utf8')
        cursors = conn.cursor()
        try:
            #开始执行sql语句
            sql = """update zhidao_new
                     set browse_num=%s, questions=%s, questions_add=%s, comment_best=%s, comment_best_num=%s, comment_common=%s
                     where id = %s"""
            cursors.execute(
                sql,
                [
                    respones_browes,
                    questions,
                    str(questions_add),
                    str(comment_best),
                    str(respones_Common),
                    str(comment_common),
                    id_list
                ]
            )
            print("更新成功！！！")
            # print(sql%(respones_browes, questions, questions_add, comment_best, respones_Common, comment_common, id_list))
        except Exception as e:
            print("最佳回答字符错误=。=，跳过该错误")
        conn.commit()
        cursors.close()
        conn.close()

    # def update_sql_write(self, *args, **kwargs):
    #     """
    #         作用：测试write写入流
    #     """
    #     with open('/Users/li/Desktop/2018test.txt','a+') as f:
    #         f.write('浏览次数:%s,问题:%s,问题补充:%s,最佳答案:%s,最佳问题答案补充:%s,普通答案:%s,id:%s[==================================空格君===============================]'%(respones_browes, questions, questions_add, comment_best, respones_Common, comment_common,id_list))

    def write_insterData(self, id_list, link_list, date_list,answerer_list):
        """
            作用：将id、链接、日期插入数据库
        :param id:url的id，作为主键存入数据库
        :param links:url链接列表
        :param date_list:百度知道问题提问时间
        :return:
        """

        #创建connection对象,将数据库连接信息存入
        conn = pymysql.connect(host = 'localhost', port = 3306, db = 'python4', user = 'root', passwd = '123456', charset = 'utf8' )
        cursors = conn.cursor()
        # cursors.execute("set sql_mode=''")
        try:
            cursors.execute("insert into zhidao_new(id, answerer, link_list, date_list) VALUE ('%s', '%s', '%s', '%s')"%(id_list, answerer_list, link_list, date_list))
            print("数据插入成功!!!")
        except Exception as e:
            print("id重复，继续执行!!")
        conn.commit()
        cursors.close()
        conn.close()

    def zhidaoSpider(self):
        """
            作用：百度知道调度器，选择爬去的页数,组合url
        :param begin_Page:开始页数
        :param end_Page:结束页数
        """
        begin_num = int(input("请输入开始爬取的页数\n"))
        end_num = int(input("请输入结束爬取的页数\n"))
        for temp in range(begin_num,end_num+1):
            temp = temp*10
            url ="https://zhidao.baidu.com/search?word=%C4%CF%C4%FE%BB%E1%BC%C6%C5%E0%D1%B5&ie=gbk&site=-1&sites=0&date=4&pn=" + str(temp)
            self.loadPage(url)




if __name__ == "__main__":
    zd = zhidao()
    zd.zhidaoSpider()#开始正式运行
    # url = "https://zhidao.baidu.com/search?word=%C4%CF%C4%FE%BB%E1%BC%C6%C5%E0%D1%B5&ie=gbk&site=-1&sites=0&date=4&pn=20"
    # zd.loadPage(url)



    # '''启动程序'''
    # url = "https://zhidao.baidu.com/search?word=%BB%E1%BC%C6%C5%E0%D1%B5&pn=10"
    # zd.loadPage(url)

    #单独测试爬取页面信息
    # zd.loadQA("https://zhidao.baidu.com/question/403657760.html?fr=iks&word=python&ie=gbk",403657760)

    #测试调用代理
    # a = Util.Get()
    #更新ip和扩充ip池，
    # Util.Refresh()
    # print(a)
    # '''开始测试代理程序'''
    # url = "http://www.whatismyip.com.tw"
    # headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0"}
    # context = ssl._create_unverified_context()
    # request = urllib.request.Request(url, headers = headers)
    # respones = urllib.request.urlopen(request, context=context, timeout=1000).read().decode('gbk')
    # print(request)



