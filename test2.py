import pandas as pd
import cx_Oracle
def main():
    conn = cx_Oracle.connect('feuser', 'gfjjfeuser', '10.88.101.121:1521/fedb')
    c=conn.cursor()
    x=c.execute("with dateframe as (select c.fname,p.* from feuser.fact_fund_hlddetail p,feuser.gz_fund_baseinfo c where p.t_date=date'2018-9-12' and c.fname like '%四零三%'and p.s_subcode_name like '%资产支持证券%'and p.f_code=c.fcode order by p.s_subcode_name),dateframe1 as (select d.fname,c.* from feuser.fact_fund_hldtotal c,feuser.gz_fund_baseinfo d where d.fcode=c.f_code and c.t_date=date'2018-9-12'and d.fname like '%四零三%'and c.s_subcode='701A') select sum(t1.n_price) as ABS估值净价,avg(t2.n_price) as ABS利息,sum(t1.n_price)+avg(t2.n_price) as ABS估值全价,avg(t3.n_price) as 组合净资产,(sum(t1.n_price)+avg(t2.n_price))/avg(t3.n_price) as ABS占净值比例 from (select * from dateframe where s_subcode='1104') t1,(select * from dateframe where s_subcode='120410') t2,dateframe1 t3")
    row=x.fetchall()
    zz=pd.DataFrame(row,columns=['ABS估值净价', 'ABS利息','ABS估值全价','组合净资产','ABS占净值比例'])
    return zz
    c.close()
    conn.close()
if __name__ == '__main__':
    main()
zz1=main()
print(zz1)


