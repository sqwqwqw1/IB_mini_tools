import os,re
import shutil
import pandas as pd


# 原文件目录
origin = 
# 目标根目录
dest = 

def move(index, dest):
    check = 0
    g2 = os.walk(dest)
    for r2, d2, f2 in g2:
        for d in d2:
            match = d.split('$')[0]
            if index == match:
                oldpath = os.path.join(r1,f)
                newpath = os.path.join(r2,d, f)
                shutil.move(oldpath,newpath)
                check = 1
    return check


g = os.walk(origin)
for r1, d1, f1 in g:
    for f in f1:
        i = 0
        index = re.search('^([0-9\-]*)', f).group(1)
        check = move(index, dest)
        while check==0 and i<2:
            index = '-'.join(index.split('-')[:-1])
            i += 1
            check = move(index, dest)