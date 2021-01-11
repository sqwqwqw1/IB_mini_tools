import re
import os
import shutil

check = 源目录
dest = 输出目录

def move(index, dest):
    check = 0
    g2 = os.walk(dest)
    for r1,ds1,fs1 in g2:
            for d in ds1:
                match = d.split('$')[0]
                if index == match:
                    oldpath = os.path.join(r,f)
                    newpath = os.path.join(r1, d, f)
                    shutil.copy(oldpath, newpath)
                    check = 1
    return  check


for r,ds,fs in os.walk(check):
    for f in fs: 
        i = 0
        if '.DS' in f: continue
        dirname = os.path.dirname(os.path.join(r,f)).split('/')[-1] 
        index = re.search('^([0-9\-]*)', dirname).group(1)
        check = move(index, dest)
        while  check == 0:
            index = '-'.join(index.split('-')[:-1])
            check = move(index, dest)
            i = i+1
            if i==4:
                break