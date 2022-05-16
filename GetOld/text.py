#
import mysql.connector
conn = mysql.connector.connect(host='localhost', user='root', password='#mysqlpassword5') 
c = conn.cursor(buffered=True)

c.execute("SELECT trans_id,trans_sales FROM somanath2022.cashflow_sales where trans_sales is not null;")
all = c.fetchall()
for each in all:
    trans_sales = "22_"+str(int(each[1].split('_')[1])-18158)
    #print("update somanath2022.cashflow_sales set trans_sales ='"+trans_sales+"' where trans_id='"+each[0]+"'")
    c.execute("update somanath2022.cashflow_sales set trans_sales ='"+trans_sales+"' where trans_id='"+each[0]+"'")
conn.commit()