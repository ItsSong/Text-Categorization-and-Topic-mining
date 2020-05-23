#-*- coding: utf-8 -*-
# 功能：提取正面和负面情感的评论内容

import pandas as pd
# 获取评论数据，将1星和2星存储为负面评论；4星和5星存储为正面评论============
data = pd.read_csv('data.csv', encoding = 'gbk')
dataPos = data.loc[data[u'star'].isin(['4','5'])][u'comment']
dataNeg = data.loc[data[u'star'].isin(['1','2'])][u'comment']
# 存储正面及负面评论
dataPos.to_csv('DataPositive.txt', index = False, header = False, encoding = 'utf-8')
dataNeg.to_csv('DataNegative.txt', index = False, header = False, encoding = 'utf-8')


