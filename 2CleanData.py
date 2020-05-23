#-*- coding: utf-8 -*-
# 功能：提取评论文本，并去重

# 第一步:提取评论文本==================================================
import pandas as pd
# 获取评论数据
data = pd.read_excel('NewData.xlsx', encoding = 'utf-8')
data = data[[u'comment']]
# 提取评论数据保存至txt中
data.to_csv('comment.txt', index = False, header = False, encoding = 'utf-8')

# 第二步：去重=========================================================
# 读取txt文本数据
data1 = pd.read_csv('comment.txt', encoding = 'utf-8', header = None)
# 定义文本去重、且去重之后存储至新的文件中的函数
def cleanData(data,filename):
    l1 = len(data)   # 统计未去重前的数据量
    data = pd.DataFrame(data[0].unique())
    l2 = len(data)   # 统计去重后的数据量
    data.to_csv(filename, index=False, header=False, encoding='utf-8')
    print(u'删除了%s条评论!' %(l1 - l2))
cleanData(data1,'cleanData.txt')# 去重后存储至cleanData.txt



