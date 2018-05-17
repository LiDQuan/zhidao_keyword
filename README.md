# zhidao_keyword
根据百度知道爬取关键字
*********************************
  2018年05月17日
=
###  更新内容：
#####  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1、重构了 v1.0版本，将代码重新编写，更新为 v2.0版本
#####  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2、采用了多线程的方式爬取，解析
#####  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3、由于技术问题，我将写入和更新分开，运行顺序先运行reconstruct_thread.py 进行数据爬取，再运行reconstruct_program_update_indexId.py 补充完整内容
#####  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4、依旧采用mysql数据库，在config中可以自行配置mysql数据库
#####  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;5、以后可能会试着使用scrapy来做这个项目。。。据说scrapy效率很高，而且自带很多库类
#####  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;6、至于用到哪些库，看reconstruct_thread.py 中的import即可，欢迎自行百度。。。

*********************************
  2018年04月17日
=
###  注意事项:
#####  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1、更新了 v1.0版本，最粗糙的版本，只是使用了urllib+lxml的方式获取数据，并且以insert和update的形式，进行数据库数据的插入和更新</br >
#####  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2、整个程序，我用的是python3做的，没做兼容python2(因为我不会。。。python2.x _(:з」∠)_)，所以不兼容python2.x，不兼容python2.x</br >
#####  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3、程序的编译环境是mac os</br>
    
###  使用方法:
#####  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1、使用了网上的IP池项目(感谢大神。。原谅我已经不记得哪个大神写的了，项目名称是 IPProxy)，该项目使用的是轻数据库sqlite，要在项目根目录新建一个sqlite的数据库，
#####  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;数据库名称:“PROXIES.db”,
#####  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;表名:“IPPORT”,
#####  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;列(只有一列,不要设置为主键):IP_PORT
####   &nbsp;&nbsp;&nbsp;&nbsp;调用方法：(具体详细见IPPool中的readme)
#####  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;import IPPoll
#####  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Util.Refresh() # 更新数据库，包括爬取，检验，删除等操作
#####  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Util.Get()  # 从数据库中随机抽取一个ip进行使用
#####  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2、数据库我用的是mysql，所以，需要安装pymysql等依赖还需要(lxml, re, json, time, ssl(不知道为什么我的mac居然需要ssl才能发送请求))
#####  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3、直接运行 08-zhidao-QA-python.py 即可
