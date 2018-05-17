# zhidao_keyword
根据百度知道爬取关键字
*********************************
  2018年04月17日
=
###  注意事项:
#####  1、更新了 v1.0版本，最粗糙的版本，只是使用了urllib+lxml的方式获取数据，并且以insert和update的形式，进行数据库数据的插入和更新</br >
#####  2、整个程序，我用的是python3做的，没做兼容python2(因为我不会。。。python2.x _(:з」∠)_)，所以不兼容python2.x，不兼容python2.x</br >
#####  3、程序的编译环境是mac os</br>
    
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
