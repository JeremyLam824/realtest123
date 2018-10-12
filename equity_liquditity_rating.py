import pandas as pd
import cx_Oracle
from WindPy import *
w.start()
def main():
    conn = cx_Oracle.connect('feuser', 'gfjjfeuser', '10.88.101.121:1521/fedb')
    c = conn.cursor()
    y = c.execute("select a.t_date 组合日期,b.fname 组合名称,case when a.w_symbol is null then substr(a.s_symbol,length(a.s_symbol)-3,4)||'.HK' when a.w_symbol is not null then a.w_symbol end 股票代码,a.s_name 股票名称,a.n_amount 持仓数量,a.n_price 股票市值,a.s_subcode_name 分类 from feuser.fact_fund_hlddetail a,feuser.gz_fund_baseinfo b where a.t_date=date'2018-10-9'and b.fcode=a.f_code and a.s_subcode_name like '%股票投资%' and b.fname like '%广发中证传媒ETF%'")
    row = y.fetchall()
    zz = pd.DataFrame(row,columns=['组合日期', '组合名称', '股票代码', '股票名称', '持仓数量', '股票市值', '分类'])
    zz = zz.fillna(0)
    return zz
    c.close()
    conn.close()
if __name__ == '__main__':
    main()

#equityrate函数传入参数a=股票持仓数量，b=市场过去一月内日均成交量
def equityrate(a,b):
    if b is None:
        return 100
    else:
        return a/b

#equityliquditityrating函数传入参数a=分类，b=交易状态,c=变现能力
def equityliquditityrating(a,b,c):
    if '限售' in a:
        return 1
    elif b is not None and '交易' in b:
        if c<0.3:
            return 5
        elif c<1:
            return 4
        elif c<2:
            return 3
        elif c<6:
            return 2
        else:
            return 1
    else:
        return 1

import time
t1=time.time()
zz1=main()
t2=time.time()
t3=t2-t1
print("第一步时间：", t3)
zz2 = pd.DataFrame()
zz3 = pd.DataFrame()
#wmif=wind市场信息，捉取交易状态、区间日均成交量
for symbol in zz1.股票代码:
    ewmif = w.wss(symbol, "trade_status,avg_vol_per", "tradeDate=20181009;unit=1;startDate=20180909;endDate=20181009")
    ewmif.Codes[0]=symbol
    zz3['股票代码'] = ewmif.Codes[0]
    zz3['交易状态'] = ewmif.Data[0]
    zz3['区间日均成交量'] = ewmif.Data[1]
    zz4 = pd.concat([zz2, zz3], ignore_index=True)
    zz2 = zz4
t4 = time.time()
t5 = t4-t2
print("第二步时间：", t5)
equitysheet = pd.merge(zz1, zz2, on='股票代码')
equitysheet['变现能力'] = equitysheet.apply(lambda x: equityrate(x.持仓数量, x.区间日均成交量), axis=1)
equitysheet['流动性打分'] = equitysheet.apply(lambda x: equityliquditityrating(x.分类, x.交易状态, x.变现能力), axis=1)
t6=time.time()
t7=t6-t4
print("第三步时间：", t7)
print(zz1)
print(zz2)
print(equitysheet)
equitysheet.to_excel('equity_jieguo.xlsx')