import os, shutil, re
import pandas as pd
import os  

# 扫描件所在目录
check_folder = os.path.join(os.path.dirname(__file__), '扫描件目录')
# 目录index
check_excel = os.path.join(os.path.dirname(__file__), 'index.xlsx')
# 输出文件夹
export_folder = os.path.join(os.path.dirname(__file__), '重命名后的文件')
if os.path.exists(export_folder) != True:
    os.mkdir(export_folder)

df = pd.read_excel(check_excel,header=None,index_col=0)


for rs,ds,fs in os.walk(check_folder):
    for f in fs:
        if ".DS" in f: continue
        try:
            index = re.findall('[0-9\-]+',f)[0]
        except:
            continue
        try:
            if "标题行" in str(df.loc[index, 3]):
                filename = '{} {}({})'.format(index, df.loc[index, 1], df.loc[index, 3])
            elif ("参见" in str(df.loc[index, 2])) or ("不适用" in str(df.loc[index, 2])):
                filename = '{} {}({})'.format(index, df.loc[index, 1], df.loc[index, 2])
            else:
                filename = '{} {}'.format(index, df.loc[index, 1])
            origin_path = os.path.join(rs, f)
            export_path = '{}.pdf'.format(os.path.join(export_folder, filename))
            shutil.copy(origin_path, export_path)
        except:
            continue