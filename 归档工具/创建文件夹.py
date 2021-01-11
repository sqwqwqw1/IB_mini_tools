import os
import pandas as pd

# 目录excel
index_excel = os.path.join(os.path.dirname(__file__), 'index.xlsx')
# 文件夹目录
root = os.path.join(os.path.dirname(__file__), '目录文件夹')
if os.path.exists(root) != True:
    os.mkdir(root)

# 读取excel目录
df = pd.read_excel(index_excel)
df.columns = ['index', 'title', 'notes']
df = df.fillna(' ')

# 建立文件目录
for i in range(len(df)):
    dirname = '{} {}'.format(df.iloc[i,0], df.iloc[i,1])
    if "部分" in dirname:
        dest = os.path.join(root, dirname)
        if os.path.exists(dest) != True:
            os.mkdir(dest)
        continue
    if len(df.iloc[i,0].split('-')) == 1:
        path = os.path.join(dest, dirname)
    elif len(df.iloc[i,0].split('-')) > len(df.iloc[i-1,0].split('-')):
        path = os.path.join(path, dirname)
    elif len(df.iloc[i,0].split('-')) == len(df.iloc[i-1,0].split('-')):
        path = '/'.join(path.split('/')[:-1])
        path = os.path.join(path, dirname)
    else:
        path = '/'.join(path.split('/')[:-2])
        path = os.path.join(path, dirname)
    if os.path.exists(path) != True:
        # print(path)
        os.mkdir(path)