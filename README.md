# film_sipder
1、为保证数据库的安装，bt_spider.py脚本中，我把自己的MySQL的数据库ip地址以及用户的登录密码给换成'****'，请根据自己的mysql的信息，进行配置

2、爬取bt之家的高清的电影信息可以保存为两种方式，分别为csv和MySQL两种，默认的会使用保存到与脚本相同目录下的csv文件，查找电影下载bt种子只做了MySQL的端的优化，如需要，请自行修改代码，以支持csv文件的查找

3、使用脚本前，请先创建数据库以及创建数据表，创建方法如下：

   
    create database bt;
  
    create table films (id int primary key auto_increment,film varchar(250),bt_name varchar(250),bt_url varchar(250));
  
    grant all privileges on bt.* to '授权用户'@'授权主机ip地址' identified by '密码';

4、以上操作都执行完毕以后，需要先爬取bt之家的bt种子资源信息到MySQL端或者csv文件中，以后可以每隔几天，适当需改爬虫代码，爬取最新的bt种子信息

5、保存bt种子的形式(mysql或csv)的设置，以及要爬取高清电影的也是，请在bt_spider.py中main函数端中设置，save_type为保存bt信息的类型可以选择为mysql或者csv(默认格式为mysql)文件,爬取的最大页数可以在range()中设置

6、bt种子信息更新完毕以后，可以使用film.py脚本进行电影或者bt种子的搜索，还可以把远程的mysql端的数据同步到本地的csv文件

7、使用film.py脚本查找电影的方法
  
    python3 film.py search '老炮'

8、使用film.py脚本下载bt种子的方法(默认会把所有匹配到的结果都下载到本地的torrent目录,查找方法是模糊查找，如果需要精确查找，请注意自己查找关键字)
  
    python3 film.py download '变形金刚'

9、myql端的数据同步到本地，以csv文件存储的方法
  
    python3 film.py sync_db
