#-*- coding: utf-8 -*-
# 通过LDA模型挖掘潜在主题

# 获取正负面评论数据====================
import pandas as pd
data = pd.read_csv('data.csv', encoding = 'gbk')
dataPos = data.loc[data[u'star'].isin(['4','5'])][u'comment']
dataNeg = data.loc[data[u'star'].isin(['1','2'])][u'comment']
# 存储正面及负面评论
dataPos.to_csv('DataPositive.txt', index = False, header = False, encoding = 'utf-8')
dataNeg.to_csv('DataNegative.txt', index = False, header = False, encoding = 'utf-8')

# 处理负面情感的数据=====================
import pandas as pd
DataNegative = pd.read_csv('DataNegative.txt', encoding = 'utf-8', header = None)
# 文本去重、且去重之后存储至新的文件
def cleanData(data,filename):
    l1 = len(data)   # 统计未去重前的数据量
    data = pd.DataFrame(data[0].unique())
    l2 = len(data)   # 统计去重后的数据量
    data.to_csv(filename, index=False, header=False, encoding='utf-8')
    print(u'删除了%s条评论!' %(l1 - l2))
cleanData(DataNegative,'DataNegCleaned.txt')

# 处理正面情感的数据=====================
import pandas as pd
DataPositive = pd.read_csv('DataPositive.txt', encoding = 'utf-8', header = None)
# 文本去重、且去重之后存储至新的文件
def cleanData(data,filename):
    l1 = len(data)   # 统计未去重前的数据量
    data = pd.DataFrame(data[0].unique())
    l2 = len(data)   # 统计去重后的数据量
    data.to_csv(filename, index=False, header=False, encoding='utf-8')
    print(u'删除了%s条评论!' %(l1 - l2))
cleanData(DataPositive ,'DataPosCleaned.txt')

# 分别对正面和负面评论内容进行分词=======
import pandas as pd
import jieba
data1 = pd.read_csv('DataNegCleaned.txt', encoding = 'utf-8', header = None)  # 读取负面情感评论
data2 = pd.read_csv('DataPosCleaned.txt', encoding = 'utf-8', header = None)  # 读取正面情感评论
mycut = lambda s: ' '.join(jieba.cut(s)) #自定义简单分词函数
data1 = data1[0].apply(mycut) #通过“广播”形式分词，加快速度
data2 = data2[0].apply(mycut)
# 存储
data1.to_csv('JieBaCommentNegative.txt', index = False, header = False, encoding = 'utf-8')
data2.to_csv('JieBaCommentPositive.txt', index = False, header = False, encoding = 'utf-8')

# 读数据==================================
import pandas as pd
neg = pd.read_csv('JieBaCommentNegative.txt', encoding = 'utf-8', header = None)
pos = pd.read_csv('JieBaCommentPositive.txt', encoding = 'utf-8', header = None)
stop = pd.read_csv('stoplist.txt', encoding = 'utf-8', header = None, sep = 'tipdm',engine='python')
#sep设置分割词，由于csv默认以半角逗号为分割词，而该词恰好在停用词表中，因此会导致读取出错
#所以解决办法是手动设置一个不存在的分割词，如tipdm
stop = [' ', ''] + list(stop[0]) #Pandas自动过滤了空格符，这里手动添加
neg[1] = neg[0].apply(lambda s: s.split(' ')) #定义一个分割函数，然后用apply广播
neg[2] = neg[1].apply(lambda x: [i for i in x if i not in stop]) #逐词判断是否停用词
pos[1] = pos[0].apply(lambda s: s.split(' '))
pos[2] = pos[1].apply(lambda x: [i for i in x if i not in stop])

# 主题挖掘==================================
from gensim import corpora, models
#负面主题分析
neg_dict = corpora.Dictionary(neg[2]) #建立词典
neg_corpus = [neg_dict.doc2bow(i) for i in neg[2]] #建立语料库
neg_lda = models.LdaModel(neg_corpus, num_topics = 2, id2word = neg_dict) #LDA模型训练
print('负面主题:======================================')
print(neg_lda.show_topics())#输出每个主题

print('正面主题:======================================')
#正面主题分析
pos_dict = corpora.Dictionary(pos[2])
pos_corpus = [pos_dict.doc2bow(i) for i in pos[2]]
pos_lda = models.LdaModel(pos_corpus, num_topics = 2, id2word = pos_dict)
print(pos_lda.show_topics())