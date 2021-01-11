import os
import re
import pandas as pd 

# 扫描件在的目录
check_dir = os.path.join(os.path.dirname(__file__), '扫描件目录')
# 目录Excel
index_excel = os.path.join(os.path.dirname(__file__), 'index.xlsx')
# 输出文件目录
export_excel = os.path.join(os.path.dirname(__file__), '核对目录.xlsx')

# 获取已有文件的索引
oklist = []
g = os.walk(check_dir)
for rs,ds,fs in g:
     for f in fs:
        try:
            index = re.findall('[0-9\-]+', f)[0] 
            oklist.append(index) 
        except:
            continue

df = pd.read_excel(index_excel, header=None)
df['扫描件'] = 0
for i in range(len(df)): 
    if df.iloc[i,0] in oklist: 
        df.loc[1,'扫描件'] = "已有扫描件"
df.to_excel(export_excel,index=False)