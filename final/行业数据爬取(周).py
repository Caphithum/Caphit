import json
import os
import pandas as pd
import requests

session = requests.session()

def pd_unit(newArr):
    result = format(float(newArr) / 10000, '.2f')
    return result



def getLinesData():
    # beg和end可以调整数据区间
    params = "secid=90.BK0474&ut=fa5fd1943c7b386f172d6893dbfba10b&"\
            "fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&"\
             "fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&"\
             "klt=102&"\
             "fqt=1&"\
             "beg=20180101&"\
             "end=20181231&"\
             "smplmt=755&"\
             "lmt=1000000&"
    res = session.get("http://22.push2his.eastmoney.com/api/qt/stock/kline/get", params=params)
    data = json.loads(res.text)
    return data["data"]["klines"]



def main():
    cur_dir = os.path.dirname(__file__)
    res = pd.DataFrame(columns=('日期', '开盘', '收盘', '最高', '最低', '涨跌幅', '涨跌额', '成交量', '成交额', '振幅', '换手率'))
    # 计数
    count = 1
    for item in getLinesData():
        newArr = item.split(',')
        count = count + 1
        # 行业 地区 概念
        res.loc[count] = [newArr[0], newArr[1], newArr[2], newArr[3], newArr[4], newArr[8], newArr[9], newArr[5], newArr[6], newArr[7], newArr[10]]
        # 日期: newArr[0]
        # 开盘newArr[1] 收盘newArr[2] 最高newArr[3] 最低newArr[4] 涨跌幅newArr[8]+'%' 涨跌额newArr[9] 成交量pd_unit(newArr[5]) 成交额pd_unit(newArr[6]) 振幅newArr[7]+'%'  换手率newArr[10]+'%'

    res.to_excel(os.path.join(cur_dir, "通信服务2018" + ".xlsx"))


if __name__ == '__main__':
    main()