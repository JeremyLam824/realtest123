import pandas as pd
import cx_Oracle
def main():
    conn = cx_Oracle.connect('feuser', 'gfjjfeuser', '10.88.101.121:1521/fedb')
    c=conn.cursor()
    x=c.execute("select * from feuser.fact_trade_info where f_code='003037'and t_date between date'2018-8-1'and date'2018-9-10'and s_type='B'")
    row=x.fetchall()
    zz=pd.DataFrame(row)
    return zz
    c.close()
    conn.close()
if __name__ == '__main__':
    main()
zz1=main()
print(zz1)