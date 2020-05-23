#-*- coding: utf-8 -*-
# 功能：潜在主题可视化

import pandas as pd
df = pd.read_excel('NewData.xlsx',encoding='utf-8')
X = df[['comment']]
y = df.sentiment

import jieba
def chinese_cut(mytext):   # 建立一个辅助函数，将分词的结果用空格连接
    return " ".join(jieba.cut(mytext))
X['cut_comment'] = X.comment.apply(chinese_cut) # apply将每一行的评论都进行分词
print("分词之后的前5行是：")
print(X.cut_comment[:5]) # 查看前五行，看分词是否成功

def get_stopwords(file):
    with open(file,encoding='utf-8') as f:
        stopwords = f.read()
    stopwords_list = stopwords.split('\n')
    new_stopwords_list = [i for i in stopwords_list] # 把停用词作为列表格式保存
    return new_stopwords_list    # 返回存成列表形式的停用词
stopwords = get_stopwords('stoplist.txt')
print("停用词表后10项为：")
print(stopwords[-10:])

max_df = 0.8 # 定义过于平凡的词的界限
min_df = 3   # 定义过于独特的词的界限
from sklearn.feature_extraction.text import CountVectorizer
vect = CountVectorizer(max_df = max_df, min_df=min_df, token_pattern=u'(?u)\\b[^\\d\\W]\\w+\\b', stop_words=frozenset(stopwords))# 类似于正则表达式
# 使用向量化工具CountVectorizer将评论内容的分词X_train.cut_comment转化为dataframe类型，赋值给transf_matrix
X_train = pd.DataFrame(vect.fit_transform(X.cut_comment).toarray(), columns=vect.get_feature_names())

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_train, y, random_state=1)
print("去除停用词且向量化后训练集的格式：")
print(X_train.head())
print("去除停用词且向量化后训练集的大小：",X_train.shape)

# LDA模型挖掘潜在主题==============================================================================
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np
# 使用batch方法进行学习，比默认online要慢一点，但通常结果比较好
lda = LatentDirichletAllocation(n_topics=5, learning_method="batch", max_iter=25, random_state=0)
document_topics = lda.fit_transform(X_train)   # fit_transform()对数据先拟合fit，然后标准化、归一化
# LatentDirichletAllocation有一个components_属性，其中保存了每个单词对每个主题的重要性
print(lda.components_.shape)  # components_的大小为（n_topics，n_words)
# 对于每个主题（components_的一行），将特征排序
sorting = np.argsort(lda.components_, axis=1)[:,::-1]  # 用[:,::-1]进行反转，为降序
# 从向量器中获取特征名称
feature_names = np.array(vect.get_feature_names())
# 显示5个主题前10个单词=================
import mglearn
# 显示5个主题；每个主题10个单词n_words=10
mglearn.tools.print_topics(topics=range(5), feature_names=feature_names, sorting=sorting, topics_per_chunk=5, n_words=10)

# 可视化================================
import matplotlib.pyplot as plt
topic_names =["{:>2}".format(i) + " ".join(words) for i,words in enumerate(feature_names[sorting[:,:2]])]
# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
xValue,yValue=["topic0","topic1","topic2","topic3","topic4"], list((np.sum(document_topics,axis=0))/1500) # axis=0表示列(每一列求和)；
plt.bar(xValue,yValue,width=0.5)  # 作柱状图；
plt.ylabel("frequency")
for a,b in zip(xValue,yValue): # 打包遍历
    plt.text(a, b, '%s'%round(b,3), ha='center', va='bottom', fontsize=11) # 显示数字(四舍五入，保留3位小数)：顶部、居中、大小11
plt.show()

