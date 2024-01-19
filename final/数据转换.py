import pandas as pd
from decimal import Decimal
import os

hy = '通信服务'

folder_path = f"C:\Users\houzy\Desktop\finalhomework\数据\行业数据(周)\\{hy}"

# 使用os.listdir()函数获取文件夹下的所有文件名
file_names = os.listdir(folder_path)

arr = []
# 打印所有文件名
for file_name in file_names:
    arr.append(file_name)

res = pd.DataFrame(columns=("股票代码", "股票简称", "日期","开盘", "收盘", "最高", "最低", "涨跌幅(%)", "涨跌额", "成交量", "成交额", "振幅(%)", "换手率(%)", "行业"))
kp=0
sp=0
zg=0
zd=0
# 涨跌幅
zdf = 0
zde=0
# 成交量
cjl=0
# 成交额
cje = 0
zf=0
# 换手率
hsl = 0
count = 1
cur_dir = os.path.dirname(__file__)
for name in arr:
    df = pd.read_excel(f'C:\Users\houzy\Desktop\finalhomework\数据\行业数据(周)\{hy}\{name}', sheet_name=0, index_col=0,
                           dtype={'股票代码': 'str', '日期': 'str'})
    for j in range(2018, 2023):
        for i in range(2, df['日期'].size + 2):
            if int(df['日期'].str.split('-')[i][0]) == j:
                kp = df['开盘'][i] * 1000 + kp
                sp = df['收盘'][i] * 1000 + sp
                zg = df['最高'][i] * 1000 + zg
                zd = df['最低'][i] * 1000 + zd
                zdf = df['涨跌幅(%)'][i]*1000+zdf
                zde = df['涨跌额'][i] * 1000 + zde
                cjl = df['成交量'][i] * 1000 + cjl
                cje = df['成交额'][i] * 1000 + cje
                zf = df['振幅(%)'][i] * 1000 + zf
                hsl = df['换手率(%)'][i] * 1000 + hsl
        if kp != 0:
            count = count + 1
            res.loc[count] = [df['股票代码'][2], df['股票简称'][2], j, kp/1000, sp/1000, zg/1000, zd/1000, zdf/1000, zde/1000, cjl/1000, cje/1000, zf/1000, hsl/1000, df['行业'][2]]
        # print(str(j)+"-"+str(z), str(Decimal(zdf/100).quantize(Decimal("0.00")))+'%', Decimal(csl/100).quantize(Decimal("0.00")), Decimal(cje/100).quantize(Decimal("0.00")),str(Decimal(hsl/100).quantize(Decimal("0.00")))+'%')
        kp = 0
        sp = 0
        zg = 0
        zd = 0
        # 涨跌幅
        zdf = 0
        zde = 0
        # 成交量
        cjl = 0
        # 成交额
        cje = 0
        zf = 0
        # 换手率
        hsl = 0
    print("处理了一个")
res.to_excel(os.path.join(cur_dir, f"{hy}.xlsx"))
