import functools

import pymysql
import jieba
import json

#读取停用列表
def get_stopword_list(file):
    with open(file,'r',encoding='utf-8') as f:
        stopword_list = [word.strip('\n') for word in f.readlines()]
    return stopword_list

#分词 然后清除停用词语
def clean_stopword(str,stopword_list):
    result = []
    word_list = jieba.lcut(str)  #分词后返回一个列表 jieba.cut() 返回的是一个迭代器
    for w in word_list:
        if w not in stopword_list:
            result.append(w)
    return result
stopword_file = r"C:\Users\Daitu\gitProjects\wechat-report\bin\stop_words2.txt"
stopword_list = get_stopword_list(stopword_file)  #获得停用词表

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    db='wechat',
    charset='utf8mb4',
    port=3306)

cur = conn.cursor()

cur.execute("select * from log")

r = cur.fetchall()
result = {}

# 获得最长的一句话
max_item = None
for item in r:
    content = item[3]
    if (max_item is None or len(content) > len(max_item[3])) and content.find('http') == -1:
        max_item = item
print(max_item)

# # 进行分词
word_arr = []
for item in r:
    content = item[3]
    word_arr = word_arr + clean_stopword(content,stopword_list)
word_count_map = {}
for word in word_arr:
    if word in word_count_map:
        word_count_map[word] = word_count_map[word] + 1
    else:
        word_count_map[word] = 1
word_count_arr = []
for word in word_count_map:
    o = {
        'word': word,
        'count': word_count_map[word]
    }
    word_count_arr.append(o)
    with open("result.txt","a+",encoding="utf-8") as f2:
        f2.write(f"{word}\t{word_count_map[word]}\n")

def custom_sort(x, y):
    if x['count'] > y['count']:
        return -1
    if x['count'] < y['count']:
        return 1
    return 0


result['word'] = sorted(word_count_arr, key=functools.cmp_to_key(custom_sort))

with open("result.json", "w", encoding="utf-8") as f:
    f.write(
        json.dumps(result, ensure_ascii=False)
    )
