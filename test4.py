import pandas as pd
import cx_Oracle
from WindPy import *
w.start()
def main():
    conn = cx_Oracle.connect('feuser', 'gfjjfeuser', '10.88.101.121:1521/fedb')
    c=conn.cursor()
    x=c.execute("select f_code,w_symbol,S_NAME,n_amount,n_price,N_interest from feuser.fact_fund_hlddetail where t_date=date'2018-9-10'and s_subcode_name='债券投资'and f_code='000037'and n_amount!=0")
    row=x.fetchall()
    zz=pd.DataFrame(row,columns=['组合代码', '债券代码','债券简称','持仓数量','持仓净价','应计利息'])
    return zz
    c.close()
    conn.close()
if __name__ == '__main__':
    main()

def marketname(a):
    if '.IB'in a:
        return '银行间'
    elif '.SH'in a:
        return '上交所'
    else:
        return '深交所'

def windmarkettype(a):
    wmt=w.wss(a,"windl1type,amount,latestissurercreditrating")
    df = pd.DataFrame(wmt.Data)
    df1=df.T
    return df1

def bondliqu(a):
    if '国债' in a:
        return 5
    elif '同业存单' in a:
        return 5
    elif '短期融资券' in a:
        return 3
    elif '金融债' in a:
        return 4
    else:
        return 1

import time
t1=time.time()
zz1=main()
t2=time.time()
t3=t2-t1
print("第一步时间：",t3)
zz1['市场名称']=zz1.apply(lambda x: marketname(x.债券代码), axis = 1)
t4=time.time()
t5=t4-t2
print("第二步时间：",t5)
zz1['wind一级分类', '最新债项评级', '最新主体评级']=zz1.apply(lambda x: windmarkettype(x.债券代码), axis = 1)
t6=time.time()
t7=t6-t4
print("第三步时间：",t7)
t8=time.time()
t9=t8-t6
print("第四步时间：",t9)
print(zz1)