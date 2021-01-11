import os, shutil
import pandas as pd

# 拆分的PDF所在目录
folder = os.path.join(os.path.dirname(__file__), '拆分的PDF')
# 目录Excel
excel = os.path.join(os.path.dirname(__file__), 'index.xlsx')
df = pd.read_excel(excel,header=None)
# 偏移量，也就是说从Excel的第几条开始读取文件名
offset = 2
# 输出文件夹
dest = os.path.join(os.path.dirname(__file__), "重命名的文件")
if os.path.exists(dest) != True:
    os.mkdir(dest)

path_list = []
g = os.walk(folder)
# 获取文件列表
for r, d, f in g:
    for filename in f:
        oldpath = os.path.join(r, filename)
        if ".DS" not in oldpath:
            path_list.append(oldpath)
# 按最后修改时间排序
path_list = sorted(path_list, key=lambda x: os.path.getmtime(os.path.join(r, x)))
# 从Excel读取文件名并重命名
for i in range(len(path_list)):
    j = i + offset
    if ("不适用" in str(df.iloc[j,2])) or ("参见" in str(df.iloc[j,2])):
        newpath = os.path.join(dest, '{} {}({}).pdf'.format(df.iloc[j,0], df.iloc[j,1], df.iloc[j,2]))
        # print(path_list[i], newpath)
        shutil.copy(path_list[i], newpath)
    else:
        newpath = os.path.join(dest, '{} {}.pdf'.format(df.iloc[j,0], df.iloc[j,1]))
        # print(path_list[i], newpath)
        shutil.copy(path_list[i], newpath)
