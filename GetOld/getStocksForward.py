import datetime
from distutils.log import error
from time import sleep, time
import mysql.connector
from requests import post
conn = mysql.connector.connect(host='localhost', user='root', password='mysqlpassword5') 
c = conn.cursor(buffered=True)
import datetime
import time

now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")

                     #0         1           2                  3         4        5             6         7         8              9       10          11          12          13                      
c.execute("SELECT prod_id, prod_qty, cost_price, sell_price_1, sell_price_2, sell_price_3, tot_qty, pur_id, cash, pro_hotel, pro_family, pro_special FROM may.stocks where prod_qty > 0 ")
sup = c.fetchall()
i=1
sec =0
min =0
for each in sup:
    c.execute("select distinct(sup_id) , pur_date from may.purchase_registry where pur_id = " + str(each[7]))
    pur = c.fetchone()
    print(pur)

    insert_time = str(pur[1]) + " 00:"+"{:02.0f}".format(min)+":"+"{:02.0f}".format(sec)
    sec+=1
    if sec==60:
        sec = 0
        min+=1
        if min == 60:
            min = 0

    

    

    if each[7] >2347:
        pur_id = '22_' + str (each[7] - 2347)
    else:
        pur_id = '21_' + str(each[7])
    
    sp_nml = ":" + "{:.3f}".format(round(each[3],3)) + ":" + "{:.3f}".format(round(each[4],3)) + ":" + "{:.3f}".format(round(each[5],3)) + ":" + "{:.3f}".format(round(each[5],3)) + ":"

    htl_price = "{:.3f}".format(round(each[3],3))
    if each[9] >0 :
        htl_price = "{:.3f}".format(round((1+(each[9]/100)) * each[2],3))
    spl_price = htl_price
    if each[10] >0 :
        spl_price = "{:.3f}".format(round((1+(each[10]/100)) * each[2],3))
    ang_price = spl_price
    if each[11] >0 :
        ang_price = "{:.3f}".format(round((1+(each[11]/100)) * each[2],3))

    sp_htl = ":" + htl_price + ":" + htl_price + ":" + htl_price + ":" + htl_price + ":"
    sp_spl = ":" + spl_price + ":" + spl_price + ":" + spl_price + ":" + spl_price + ":"
    sp_ang = ":" + ang_price + ":" + ang_price + ":" + ang_price + ":" + ang_price + ":"

    sql = "insert into somanath2022.stocks values('"+'22_'+str(i)+"','"+pur_id+"',"+str(each[0])+","+"{:.3f}".format(round(each[1],3))+","+"{:.3f}".format(round(each[6],3))+","+"{:.3f}".format(round(each[2],3))+",'"+sp_nml+"','"+sp_htl+"','"+sp_spl+"','"+sp_ang+"',0,"+str(pur[0])+","+str(each[8]+1)+",'" + insert_time+"',1,NULL,NULL)"

    c.execute(sql)
    i+=1
    print(i)
conn.commit()

#22_3530 max_stocks id