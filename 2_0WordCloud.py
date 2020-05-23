#!/usr/bin/env python
#-*- coding = utf-8 -*-
# 功能：将文本数据处理成分词形式，并展现词频和词云

import jieba
import wordcloud
# 第一步：读取数据=================================
f = open('cleanData.txt','r',encoding="utf-8")
t = f.read()
f.close()

# 第二步：分词，并展现词云=========================
def wordCloud(t,outfilename):
    ls = jieba.lcut(t)       # 将文本数据处理成分词形式，以列表形式返回
    txt = " ".join(ls)       # 将ls元素用空格分开
    # 设置词云展现的格式：字体微软雅黑；宽1000，高700；背景色白色
    w = wordcloud.WordCloud(font_path="msyh.ttc",width=1000,height=700,background_color="white")
    w.generate(txt)         # 加载词云文本
    w.to_file(outfilename)  # 以图片格式输出词云文件
wordCloud(t,"comment.png")

# 第三步：词频统计=================================
def count(ls):
    counts = {}
    for word in ls:
        if len(word) == 1:
            continue
        else:
            counts[word] = counts.get(word,0) + 1   #计数
    items = list(counts.items())
    items.sort(key = lambda x:x[1], reverse=True)
    for i in range(15):
        word,count = items[i]
        print("{0:<10}{1:>5}".format(word,count))
ls = jieba.lcut(t)
print("评价内容词频统计：")
count(ls)