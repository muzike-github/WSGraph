"""
   bitcoinotc.csv源文件中权值有负数[-10,10]，将其全部转换为正数
   将权重列全部加20,将权重控制在[10,30]
   如果只+10可能会出现权值为0的情况，算法准确度会出现问题
"""

import pandas as pd
filename = "dataset/soc-sign-bitcoinotc.csv"
df = pd.read_csv(filename)
df.columns = ['node1', 'node2', 'weight', 'extra']
df['weight'] = df['weight'] + 15
df_new = df.drop('extra', axis=1)
df_new.to_csv('dataset/bitcoinData.csv',header=None,index=None)
print(df_new)
