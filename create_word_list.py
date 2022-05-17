"""
使用dict.txt完成(dict.txt中每一行即是一个单词记录:单词　　解释)
创建一个数据库  dict  utf8格式
create database dict charset=utf8;
在该数据库下创建数据表  words -> id  word  mean
"""
import re
import pymysql

args = {
    "host": "localhost",  # 本地访问数据库
    "port": 3306,
    "user": "root",  # 根据自己的数据库用户更改
    "password": "123456",  # 输入对应用户的登录密码
    "database": "dict",  # 如果使用其他数据库,自行更改
    "charset": "utf8"
}
# 打开数据库和游标
db = pymysql.connect(**args)
cur = db.cursor()
# 打开当前目录下的dict.txt文件
file = open('dict.txt')
for line in file:  # 按行读取dict.txt
    if not line:  # 如果读取完文件,跳出循环
        break
    try:
        # 使用正则表达式切割出每行的单词
        word_target = re.search("(\w+.\w+)|(\w+\s\s)", line).group()
        # 将每行中的单词部分用空格替代得到单词解释
        # 但该单词解释样式不规范,解释的前面有很多空格
        mean_temp = line.replace(word_target, ' ')
        # 将临时单词解释前面的空格去除
        mean_target = re.findall('\S.*', mean_temp)
        # 如果单词的解释为空,则将单词的解释赋予none
        if mean_target == []:
            mean_target = "none"
        # 将上面得到的单词与单词的解释写入words数据表
        sql = "insert into word (word,mean) values(%s,%s)"
        cur.execute(sql, [word_target, mean_target])
        db.commit()
    except Exception as e:  # 若出现异常则回滚
        print(e)
        db.rollback()
# 关闭数据库和游标
cur.close()
db.close()
