
import mysql.connector
conn = mysql.connector.connect(host='localhost', user='root', password='mysqlpassword5') 
c = conn.cursor(buffered=True)
import datetime

oldDbYear = 22
newDbYear = 23

now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")

c.execute("SELECT * from somanath20"+str(oldDbYear)+".stocks where stk_prod_qty>0")
sup = c.fetchall()
i=1
for each in sup:
    stk_id = str(newDbYear) + "_" + str(i)
    sql = "insert into somanath20"+str(newDbYear)+".stocks values ('"+stk_id+"','" + str(each[1]) +"',"+str(each[2])+","+ str(each[3]) +"," + str(each[4]) +","+ str(each[5])+",'"+str(each[6])+"','"+str(each[7])+"','"+str(each[8])+"','"+str(each[9])+"',"+str(each[10])+","+str(each[11])+","+str(each[12])+",'"+str(each[13])+"',"+str(each[14])+",NULL,NULL)"
    c.execute(sql)
    i+=1
    print(i)

sql = "insert into somanath20"+str(newDbYear)+".max_id VALUES (0,0,"+str(i-1)+",0,0,0,0,0)"
c.execute(sql)
conn.commit()