#-*- coding: utf-8 -*-
# 功能：（1）词向量化操作(带分词、剔除停用词)；（2）训练及预测

# 定义特征和目标=============================
import pandas as pd
df = pd.read_excel('NewData.xlsx',encoding='utf-8')
X = df[['comment']]
y = df.sentiment

# 分词========================================
import jieba
def chinese_cut(mytext):   # 建立一个辅助函数，将分词的结果用空格连接
    return " ".join(jieba.cut(mytext))
X['cut_comment'] = X.comment.apply(chinese_cut) # apply将每一行的评论都进行分词
print("分词之后的前5行是：")
print(X.cut_comment[:5]) # 查看前五行，看分词是否成功


# 词向量化操作，在这个过程中剔除掉停用词======
# 定义停用词格式
def get_stopwords(file):
    with open(file,encoding='utf-8') as f:
        stopwords = f.read()
    stopwords_list = stopwords.split('\n')
    new_stopwords_list = [i for i in stopwords_list] # 把停用词作为列表格式保存
    return new_stopwords_list    # 返回存成列表形式的停用词
stopwords = get_stopwords('stoplist.txt')

# 向量化
max_df = 0.8 # 定义过于平凡的词的界限
min_df = 3   # 定义过于独特的词的界限
from sklearn.feature_extraction.text import CountVectorizer
vect = CountVectorizer(max_df = max_df, min_df=min_df, token_pattern=u'(?u)\\b[^\\d\\W]\\w+\\b', stop_words=frozenset(stopwords))# 类似于正则表达式
# 使用向量化工具CountVectorizer将评论内容的分词X_train.cut_comment转化为dataframe类型，重新赋值给X_new
X_new = pd.DataFrame(vect.fit_transform(X.cut_comment).toarray(), columns=vect.get_feature_names())
print(X_new.head())
print(X_new.shape)

# 划分训练集和测试集======================
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_new, y, random_state=1)
print("X_train.shape：",X_train.shape)
print("y_train.shape：",y_train.shape)
print("X_test.shape：",X_test.shape)
print("y_test.shape：",y_test.shape)

# 训练=====================================
from sklearn.naive_bayes import MultinomialNB
nb = MultinomialNB()
from sklearn.cross_validation import cross_val_score
accu1 = cross_val_score(nb, X_train, y_train, cv=10, scoring='accuracy').mean()
print('Accuracy:',accu1)

# 预测=====================================
nb.fit(X_train, y_train)
y_predict = nb.predict(X_test)
print(y_predict)
# 查看预测的准确率
from sklearn import metrics  # 引入测量工具集
accu2 = metrics.accuracy_score(y_test, y_predict)
print('Predicting Accuracy:',accu2)
# 查看混淆矩阵
print(metrics.confusion_matrix(y_test, y_predict))