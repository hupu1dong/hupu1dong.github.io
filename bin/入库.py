import pymysql
import re
from pymysql.converters import escape_string

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    db='wechat',
    charset='utf8mb4',
    port=3306)

cur = conn.cursor()

with open(r"C:\Users\Daitu\Documents\张冠一\慕祁宝贝.txt", encoding='utf-8') as f:
    lines = f.readlines()
    filter_lines = []
    reg = "^.*\s\(.+\):"

    for line in lines:
        # 去除转发的聊天记录 简单过滤
        if (line.startswith('张冠一') or line.startswith('慕祁宝贝') or line.startswith('章鱼小丸子')) and re.match(reg, line):
            filter_lines.append(line.strip())

for line in filter_lines:
    s1 = line.find(" ")
    s2 = line.find("):")
    name = line[:s1]
    time = line[s1 + 2:s2]
    content = line[s2 + 2:]
    print(line)
    insert_sql = f"insert into log(user,datetime,content) values ('{name}','{time}' ,'{pymysql.converters.escape_string(content)}')"
    cur.execute(insert_sql)
conn.commit()
