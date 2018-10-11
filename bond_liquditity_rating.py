import pandas as pd
import cx_Oracle
from WindPy import *
w.start()
def main():
    conn = cx_Oracle.connect('feuser', 'gfjjfeuser', '10.88.101.121:1521/fedb')
    c=conn.cursor()
    x=c.execute("select a.t_date 组合日期,b.fname 组合名称,a.w_symbol 债券代码,a.s_name 债券名称,a.n_amount 债券数量,a.n_price 债券净价,(a.n_price+NVL(a.n_interest，0）) 债券全价 from feuser.fact_fund_hlddetail a,feuser.gz_fund_baseinfo b where a.t_date=date'2018-10-9'and a.s_subcode_name like '%债券投资%'and b.fcode=a.f_code and a.n_amount!=0 and b.fname like '%招商%'and a.w_symbol is not null")
    row=x.fetchall()
    zz=pd.DataFrame(row,columns=['组合日期', '组合名称', '债券代码','债券简称','持仓数量','债券净价','债券全价'])
    zz=zz.fillna(0)
    return zz
    c.close()
    conn.close()
if __name__ == '__main__':
    main()

#compoundrating函数传入参数a=债项评级、b=主体评级、c=wind一级分类，若wind一级分类为短期融资券，则取主体评级；若债项评级为空则取主体评级，
def compoundrating(a,b,c):
    if '短期融资券' in c:
        return b
    elif a is None:
        return b
    else:
        return a

#bondliquditityrating函数传入参数a=综合评级, b=wind一级分类, c=wind二级分类, d=剩余期限天, e=发行方式
def bondliquditityrating(a, b,c, d, e):
    if '国债' in c or '地方政府债' in c or '央行票据' in c or '政策银行债' in c or '政府支持机构债' in c:
        return 5
    elif '短期融资券' in b or '同业存单' in b:
        if a=="AAA":
           return 5
        elif d<=7:
            return 4
        else:
            return 3
    elif '定向工具' in c or '私募债' in c or '资产支持证券' in b:
        return 1
    elif '可交换债' in c or '可转债' in c:
        if '私募' in e:
            return 1
        else:
            return 4
    else:
        if d<=7:
            return 4
        elif '私募' in e:
            return 1
        else:
            return 3

import time
t1=time.time()
zz1=main()
t2=time.time()
t3=t2-t1
print("第一步时间：", t3)
zz2 = pd.DataFrame()
zz3 = pd.DataFrame()
#wmif=wind市场信息，捉取wind债券一级分类、wind债券二级分类、最新债项评级、最新主题评级、最新
for symbol in zz1.债券代码:
    wmif = w.wss(symbol, "windl1type,windl2type,amount,latestissurercreditrating,day,issue_issuemethod", "tradeDate=20181009")
    wmif.Codes[0]=symbol
    zz3['债券代码'] = wmif.Codes[0]
    zz3['wind一级分类'] = wmif.Data[0]
    zz3['wind二级分类'] = wmif.Data[1]
    zz3['债项评级'] = wmif.Data[2]
    zz3['主体评级'] = wmif.Data[3]
    zz3['剩余期限天'] = wmif.Data[4]
    zz3['发行方式'] = wmif.Data[5]
    zz4 = pd.concat([zz2, zz3], ignore_index=True)
    zz2=zz4
t4=time.time()
t5=t4-t2
print("第二步时间：", t5)
zz2['综合评级'] = zz2.apply(lambda x: compoundrating(x.债项评级, x.主体评级, x.wind一级分类), axis=1)
zz2['流动性打分'] = zz2.apply(lambda x: bondliquditityrating(x.综合评级, x.wind一级分类, x.wind二级分类, x.剩余期限天, x.发行方式), axis=1)
t6=time.time()
t7=t6-t4
print("第三步时间：", t7)
bondsheet = pd.merge(zz1, zz2, on='债券代码')
print(zz1)
print(zz2)
print(bondsheet)
bondsheet.to_excel('jieguo1.xlsx')