#-*- coding: utf-8 -*-
# 功能：分别对正面和负面评论内容进行分词
import pandas as pd
import jieba
data1 = pd.read_csv('ComDataNegCleaned.txt', encoding = 'utf-8', header = None)  # 读取负面情感评论
data2 = pd.read_csv('ComDataPosCleaned.txt', encoding = 'utf-8', header = None)  # 读取正面情感评论
mycut = lambda s: ' '.join(jieba.cut(s)) #自定义简单分词函数
data1 = data1[0].apply(mycut) #通过“广播”形式分词，加快速度
data2 = data2[0].apply(mycut)
# 存储
data1.to_csv('JieBaCommentNegative.txt', index = False, header = False, encoding = 'utf-8')
data2.to_csv('JieBaCommentPositive.txt', index = False, header = False, encoding = 'utf-8')