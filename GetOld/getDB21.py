from audioop import reverse
import datetime
from re import I
from time import sleep, time
import mysql.connector
from requests import post
from PIL import Image,ImageTk
conn = mysql.connector.connect(host='localhost', user='root', password='mysqlpassword5') 
c = conn.cursor(buffered=True)
from asyncio.windows_events import NULL
import datetime
from distutils.spawn import spawn
import time

now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")
import os

import shutil


#Make changes so that only date<31st march is selected
#use database backup of 2022-03-31
#Acc_bal
"""
c.execute("select max(acc_id) from somanath.accounts where acc_type = 'SUPP'")
max_acc_id = c.fetchone()[0] 

c.execute("select sup_id , sup_name , sup_bal , opn_bal from somanathstores.supplier_registry")
sup = c.fetchall()

for each in sup:
    c.execute("insert into somanath2021.acc_bal (acc_id, acc_cls_bal_firm1 , acc_opn_bal_firm1) values("+str(each[0]) +","+"{:.2f}".format(each[2])+","+"{:.2f}".format(each[3])+")")



c.execute("select cust_id , cust_name , cust_bal , open_bal from somanathstores.customer_registry")
cust = c.fetchall()

for each in cust:
    c.execute("insert into somanath2021.acc_bal (acc_id, acc_cls_bal_firm1 , acc_opn_bal_firm1) values("+str(each[0] + max_acc_id) +","+"{:.2f}".format(each[2])+","+"{:.2f}".format(each[3])+")")

conn.commit()
"""

#To correct deleted purchases
"""
c.execute("select distinct(pur_id) from somanathstores.purchase_registry order by pur_id;")
id = c.fetchall()
A = []
for each in id:
    A.append(each[0])

    
# using zip
res = []
for m,n in zip(A,A[1:]):
   if n - m > 1:
      for i in range(m+1,n):
         res.append(i)

# Result
print("Missing elements from the list : \n" ,res)
"""
#673 missing 

#1165 is missing from purchase_registry 
#DELETE FROM somanathstores.purchase_cashflow where bill_id= 1165;
#SELECT * FROM somanathstores.stocks where pur_id=1165; Missing good
#SELECT * FROM somanathstores.sales_registry where  pur_id = 1165
#
#6467 6475 6484 6490 6501 6506 bills contain 1165's product
#
#for Bill 6467
#DELETE FROM somanathstores.sales_registry where  pur_id = 1165 and sale_id = 6467;
#UPDATE somanathstores.sales_registry SET amt_paid = 819 where sale_id = 6467;
#SELECT * FROM somanathstores.sales_cashflow where bill_id=6467; SET amt_paid bill_amt to 819;
#UPDATE somanathstores.profits set bill_total = 819 , profit = 95.18 where sale_id = 6467;
#
#for Bill 6475
#DELETE FROM somanathstores.sales_registry where  pur_id = 1165 and sale_id = 6475;
#UPDATE somanathstores.sales_registry SET amt_paid = 180.8 where sale_id = 6475;
#SELECT * FROM somanathstores.sales_cashflow where bill_id=6475;SET amt_paid bill_amt to 180.8
#UPDATE somanathstores.profits set bill_total = 180.8 , profit = 45.52 where sale_id = 6475;
#
#for Bill 6484
#DELETE FROM somanathstores.sales_registry where  pur_id = 1165 and sale_id = 6484;
#UPDATE somanathstores.sales_registry SET amt_paid = 1034.1 where sale_id = 6484;
#SELECT * FROM somanathstores.sales_cashflow where bill_id=6484; #amt_paid bill_amt 1034.1;
#UPDATE somanathstores.profits set bill_total = 1034.1 , profit = 189.39 where sale_id = 6484;
#
#for Bill 6501 #6490 #6490 20*1.2=24  -9.6 profit 50.5 393.51
#DELETE FROM somanathstores.sales_registry where  pur_id = 1165 and sale_id = 6501;
#UPDATE somanathstores.sales_registry SET amt_paid = 1164.51 where sale_id = 6501;
#SELECT * FROM somanathstores.sales_cashflow where bill_id=6501; #amt_paid 1164.51 bill_amt 393.51;
#UPDATE somanathstores.profits set bill_total = 393.51 , profit = 50.5 where sale_id = 6501;
#
#6506 #6506 31*50=1550 -1550 -100 profit 537.12 3650
#DELETE FROM somanathstores.sales_registry where  pur_id = 1165 and sale_id = 6506;
#UPDATE somanathstores.sales_registry SET amt_paid = -1550 where sale_id = 6506;
#SELECT * FROM somanathstores.sales_cashflow where bill_id=6506; #amt_paid -1550 bill_amt 3650;
#SELECT * FROM somanathstores.sales_registry where pur_id = 1165; check again res


#update somanath2021.max_id SET stocks =0 , cashflow_sales=0, cashflow_purchase =0;

"""
sql = 'select distinct(pur_id), sup_id from somanathstores.purchase_registry where pur_date <"2022-04-01" order by pur_id'
c.execute(sql)
pur_id1 = c.fetchall()
pur_id = []

for each in pur_id1:
    pur_id.append((each[0],each[1], each[1]))

i = 1
j = 1
sec = 0
for each in pur_id:
    c.execute("select * from somanathstores.purchase_registry where pur_id = "+str(each[0]))
    pur = c.fetchall()

    id = "21_" + str(pur[0][0])
    inv = pur[0][3]
    exp = "{:.2f}".format(pur[0][7])
    paid = "{:.2f}".format(pur[0][6])

    date2 = str(pur[0][1])
    
    insert_time = date2 + " 00:00:"+"{:02.0f}".format(sec)
    sec+=1
    if sec==60:
        sec = 0
    
    prod_id = ":"
    prod_cp = ":"
    prod_qty_pur = ":"

    stk_sql = "insert into somanath2021.stocks ( stk_id , stk_pur_id, stk_prod_id, stk_prod_qty, stk_tot_qty, stk_cost, stk_sp_nml, stk_sp_htl, stk_sp_spl, stk_sp_ang, stk_exp, stk_sup_id,stk_firm_id, insert_time, insert_id) values"

    sql = "select cash from somanathstores.supplier_registry where sup_id = "+str(each[2])
    c.execute(sql)
    pur_firm_id = c.fetchone()[0]+1
    sup_id_for_stocks = str(each[2])
    for row in pur:
        p_id = row[4]
        prod_id += str(p_id)+":"

        c.execute("select cost_price , sell_price_1 , sell_price_2 , sell_price_3 , tot_qty , pro_hotel , pro_family , pro_special , prod_qty  from somanathstores.stocks where prod_id = "+str(row[4])+" and pur_id = "+str(pur[0][0]))
        stk = c.fetchone()
        prod_cp += str("{:.2f}".format(stk[0]))+":"
        prod_qty_pur += str("{:.2f}".format(row[5]))+":"
        prod_qty_stk = "{:.2f}".format(stk[8])

        

        nml = ":"+"{:.2f}".format(stk[1])+":"+"{:.2f}".format(stk[2])+":"+"{:.2f}".format(stk[3])+":"+"{:.2f}".format(stk[3])+":"

        htl = nml
        if stk[5] >0:
            sp_htl = "{:.2f}".format(stk[0] + (stk[0] * stk[5]/100))  
            htl = ":"+sp_htl+":"+sp_htl+":"+sp_htl+":"+sp_htl+":"

        spl = nml
        if stk[6] > 0:
            sp_spl = "{:.2f}".format(stk[0] + (stk[0] * stk[6]/100))  
            spl = ":"+sp_spl+":"+sp_spl+":"+sp_spl+":"+sp_spl+":"

        ang = nml
        if stk[7] > 0:
            sp_ang = "{:.2f}".format(stk[0] + (stk[0] * stk[7]/100))  
            ang = ":"+sp_ang+":"+sp_ang+":"+sp_ang+":"+sp_ang+":"
        
        stk_id = "21_"+str(j)
        stk_sql +=  "('"+str(stk_id)+"','"+str(id)+"',"+str(p_id)+","+prod_qty_stk+","+"{:.2f}".format(stk[4])+","+"{:.2f}".format(stk[0]) + ",'"+nml + "','"+htl + "','"+spl+"','"+ang+"',0,"+sup_id_for_stocks+","+str(pur_firm_id)+",'"+insert_time+"',1),"
        j+=1

        

    stk_sql = stk_sql[0:-1]

    sql = "insert into somanath2021.purchases (pur_id, pur_acc, pur_firm_id, pur_inv, pur_prod_id, pur_prod_qty, pur_exp, pur_date, insert_time, insert_id) values('"+str(id)+"',"+str(each[1])+","+str(pur_firm_id)+",'"+str(inv)+"','"+str(prod_id)+"','"+prod_qty_pur+"',"+str(exp)+",'"+date2+"','"+insert_time+"',1)"
    c.execute(sql)

    trans_id = id
    
    c.execute(stk_sql)
    i+=1

    print("pur_id" , id)

    max_purchase = pur[0][0]
    max_cashflow = i - 1
    max_stocks = j-1
print("Write These Down",max_purchase,max_stocks,max_cashflow)
#Write These Down 2347 19726 2344
conn.commit()
"""

#get missing bill
"""
c.execute("select distinct(sale_id)  from somanathstores.sales_registry order by sale_id")
id = c.fetchall()
A = []
for each in id:
    A.append(each[0])

    
# using zip
res = []
for m,n in zip(A,A[1:]):
   if n - m > 1:
      for i in range(m+1,n):
         res.append(i)
print("Missing elements from the list : \n" ,res)
"""

#DELETE FROM somanathstores.sales_cashflow where bill_id = 10916 or bill_id = 6991 or bill_id = 6346 or bill_id = 3517 ;
# [3517, 6346, 6991, 10916]


#sales,sales_SP clean up
"""
c.execute("SELECT distinct(cust_id),sale_id FROM somanathstores.sales_registry order by sale_id;")
id = c.fetchall()

A = []
for each in id:
    A.append([each[0],each[1]])
sale_id = A[0][1]
cust_id = A[0][0]
for each in A[1:]: 
    sale_id_l = each [1]
    #cust_id_l = each [0]
    if sale_id == sale_id_l:
        print(sale_id)
    else:
        sale_id = sale_id_l
"""
#984 3777
#DELETE FROM somanathstores.sales_registry where sale_id = 984 and cust_id = 1;
#DELETE FROM somanathstores.sales_registry where sale_id = 3777 and cust_id = 1;
#AFTER EVERYTHING CHECK CUST BALABNCE OF NAGAYA BILLAVA BAGGODI, santhosh kharvi sealand MANE IN CASHFLOW AND ACC_BALANCE
#SELECT * FROM somanathstores.sales_cashflow where bill_id= 3777 ;# trans_id, trans_date, cust_id, bill_id, amt_paid, bill_amt '4151', '2021-03-03', '27', '3777', '175', '175'


#sales,sales_SP ,
"""
c.execute("select max(acc_id) from somanath.accounts where acc_type = 'SUPP'")
max_acc_id = c.fetchone()[0] 
q1 = 1
#while(q1<value) value is next 1000 place of max sale_id
cash = 0 #max_firm2+1
gst  = 0  #max_firm1+1

while(q1 < 19000):#search which is max bill_id in sales_registry
    
    q2 = q1+500
    sql = "select distinct(sale_id), cust_id , disc , sale_date  from somanathstores.sales_registry where sale_id >= "+str(q1) +" and sale_id<= "+str(q2) + " order by sale_id"
    q1 = q2+1
    c.execute(sql)
    sale_id = c.fetchall()

    
    sql = "insert into somanath2021.sales(sales_id ,  sales_ref , sales_acc , sales_prod_id, sales_pur_id, sales_prod_qty, sales_prod_sp, sale_date, discount, insert_time, insert_id)values"
    sql_sp = "insert into somanath2021.sales_sp(sales_id, sales_ref, prod_id, cost_price, units, sp_list, gst_value , cess_value, sales_profit) values "
    sec =  0
    for each in sale_id:
        sale_id = "21_"+str(each[0])
        cust_id = each[1]
        disc = "{:.2f}".format(each[2])
        date = str(each[3])
    
        
        c.execute("select  prod_id , cp , sp , prod_qty , pur_id , prod_unit_stocks , SP_list , cess , gst , cash from somanathstores.sales_registry where sale_id = "+str(each[0]))
        prods = c.fetchall()
        
        prod_id_gst = ":"
        prod_id_cash  = ":"
        prod_qty_gst = ":"
        prod_qty_cash = ":"
        pur_id_gst = ":"
        pur_id_cash = ":"
        prod_sp_gst = ":"
        prod_sp_cash = ":"
        prod_cp_gst = ":"
        prod_profit_gst = 0
        prod_profit_cash = 0
        prod_cp_cash = ":"
        prod_units_gst = "::"
        prod_units_cash = "::"
        prod_sp_list_cash = "::"
        prod_sp_list_gst = "::"
        prod_gst_gst = ":"
        prod_gst_cash = ":"
        prod_cess_gst = ":"
        prod_cess_cash = ":"
        



        
        for row in prods:
            prod_firm = row[9]  + 1

            units = row[5][1:-1].split(',')
            a=0
            
            
            for i in units:
                units[a] = "{:.3f}".format(float(i))
                a+=1
            units.sort()
            try:
                units.append(units[2])
            except IndexError:
                units = [0,0,0,0]
            
            
           

            sp_list = row[6][1:-1].split(',')
            a=0
            for i in sp_list:
                sp_list[a] = "{:.2f}".format(float(i))
                a+=1
            sp_list.sort(reverse = True)
            try:
                sp_list.append(sp_list[2])
            except IndexError:
                sp_list = [sp_list[0],sp_list[0],sp_list[0],sp_list[0]]

            

            

            if prod_firm == 1:
                prod_id_gst += str(row[0]) + ":"
                prod_qty_gst +=  "{:.3f}".format(row[3]) + ":"
                pur_id_gst += "21_"+str(row[4]) + ":"
                prod_sp_gst += "{:.3f}".format(row[2]) + ":"
                prod_profit_gst += (row[2]-row[1]) * row[3]
                prod_cp_gst +=  "{:.3f}".format(row[1]) + ":" 
                prod_gst_gst += str(row[8])+":"
                prod_cess_gst += str(row[7])+":"
                for i in units:
                    prod_units_gst += str(i) + ":"
                prod_units_gst += ":"
                for i in sp_list:
                    prod_sp_list_gst += str(i) + ":"
                prod_sp_list_gst += ":"
            else:
                prod_id_cash += str(row[0]) + ":"
                prod_qty_cash +=  "{:.3f}".format(row[3]) + ":"
                pur_id_cash += "21_"+str(row[4]) + ":"
                prod_sp_cash += "{:.3f}".format(row[2]) + ":"
                prod_profit_cash += (row[2]-row[1]) * row[3]
                prod_cp_cash += "{:.3f}".format(row[1]) + ":"
                prod_gst_cash += str(row[8])+":"
                prod_cess_cash += str(row[7])+":"
                for i in units:
                    prod_units_cash += str(i) + ":"
                prod_units_cash += ":"
                for i in sp_list:
                    prod_sp_list_cash += str(i) + ":"
                prod_sp_list_cash += ":"
        #sales_id,sales_ref, prod_id, cost_price, units, sp_list, gst_value, cess_value
            insert_time = date + " 00:00:"+"{:02.0f}".format(sec)
            sec+=1
            if sec==60:
                sec = 0

        if prod_id_gst != ":":
            gst += 1
            sql_sp += " ('"+sale_id+"','SSM_"+str(gst)+"','"+prod_id_gst+"','"+ prod_cp_gst+"','"+prod_units_gst+"','"+prod_sp_list_gst+"','"+prod_gst_gst+"','"+prod_cess_gst+"',"+'{:.3f}'.format(prod_profit_gst)+"),"
            sql += " ('"+sale_id+"','SSM_"+str(gst)+"',"+str(cust_id+max_acc_id)+",'"+prod_id_gst+"','"+pur_id_gst+"','"+prod_qty_gst+"','"+prod_sp_gst+"','"+date+"',"+str(disc)+",'"+str(insert_time)+"',1"+"),"
            
        if prod_id_cash != ":":
            cash += 1
            sql_sp += " ('"+sale_id+"','SCM_"+str(cash)+"','"+prod_id_cash+"','"+prod_cp_cash+"','"+prod_units_cash+"','"+prod_sp_list_cash+"','"+prod_gst_cash+"','"+prod_cess_cash+"',"+'{:.3f}'.format(prod_profit_cash)+"),"
            sql += " ('"+sale_id+"','SCM_"+str(cash)+"',"+str(cust_id+max_acc_id)+",'"+prod_id_cash+"','"+pur_id_cash+"','"+prod_qty_cash+"','"+prod_sp_cash+"','"+date+"',"+str(disc)+",'"+str(insert_time)+"',1"+"),"    
        

        print(sale_id)
        
        max_sales = sale_id
        max_firm1 = gst
        max_firm2 = cash
        
    #21_17625
    #Write These Down 21_17625 24 22
    #print(sql[0:-1])
    c.execute(sql[0:-1])
    c.execute(sql_sp[0:-1])
    conn.commit()
    
    

print("Write These Down",max_sales,max_firm1,max_firm2)


"""





#cashflow purchase # 673 pur_id is missing so cashflow is also deleted
#trans_id, trans_acc, trans_firm_id, trans_pur, trans_amt, amt_paid, trans_mode, trans_date, insert_time, insert_id,
"""
c.execute("SELECT trans_date,sup_id,bill_id,bill_total,amt_paid FROM somanathstores.purchase_cashflow order by trans_date")
all_pc = c.fetchall()
i=1
sec = 0 
for each in all_pc:
    if (each[2] == None) | (each[2] == 673):
        firm_id = '1'
    else:
        c.execute("SELECT cash FROM somanathstores.stocks where pur_id ="+str(each[2]))
        try:
            cash_gst = c.fetchone()[0]
        except TypeError:
            print("SELECT cash FROM somanathstores.stocks where pur_id ="+str(each[2]))
            quit()
        if cash_gst == 0:
            firm_id = '1'
        else:
            firm_id = '2'
    trans_id = '21_'+str(i)
    i+=1
    if each[2] == None:
        id = "NULL"
    else:
        id = "'"+'21_'+str(each[2])+"'"
    if each[-2] == None:
        bill_tot = "NULL"
    else:
        bill_tot=str(each[-2])
    print(trans_id)
    date2 = str(each[0])
    
    insert_time = date2 + " 00:00:"+"{:02.0f}".format(sec)
    sec+=1
    if sec==60:
        sec = 0
    sql = "insert into somanath2021.cashflow_purchase (trans_id, trans_acc,trans_firm_id, trans_pur, trans_amt, amt_paid, trans_mode, trans_date, insert_time, insert_id) values('"+trans_id+"',"+str(each[1])+","+firm_id+","+id+","+ bill_tot+" ,"+str(each[-1])+", 'CASH' , '"+date2+"','"+insert_time+"',1)"
    c.execute(sql)
conn.commit()
"""

#cashflow sales
#trans_id, trans_acc, trans_sales, trans_amt_firm1, amt_paid_firm1_cash, amt_paid_firm1_bank, trans_amt_firm2, amt_paid_firm2_cash, amt_paid_firm2_bank, trans_amt_firm3, amt_paid_firm3_cash, amt_paid_firm3_bank, trans_date, insert_time, insert_id,
#  not available on 13/3/2022
"""
sec = 0
c.execute("SELECT max(acc_id) FROM somanath.accounts where acc_type = 'SUPP';")
max_sup_id = c.fetchone()[0]
c.execute("SELECT trans_date,cust_id, bill_id,bill_amt, amt_paid  FROM somanathstores.sales_cashflow order by trans_date")
all_pc = c.fetchall()
i=1

for each in all_pc:
    cash_items = []
    gst_items = []
    if each[2] != None:
        c.execute("SELECT prod_qty,sp  FROM somanathstores.sales_registry where sale_id ="+str(each[2])+" and cash = 1;")
        cash_items = c.fetchall()

        c.execute("SELECT prod_qty,sp  FROM somanathstores.sales_registry where sale_id ="+str(each[2])+" and cash = 0;")
        gst_items = c.fetchall()

    trans_amt_firm1 = 0

    for x in gst_items:
        trans_amt_firm1 += x[0]*x[1]
    trans_amt_firm1 = round(trans_amt_firm1,2)
    trans_amt_firm2 = 0
    for y in cash_items:
        trans_amt_firm2 += y[0]*y[1]
    trans_amt_firm2 = round(trans_amt_firm2,2)

    if each[-1] == 0:
        amt_paid_firm1_cash = 0
        amt_paid_firm2_cash = 0
    elif each[-1] < 0:
        amt_paid_firm1_cash = each[-1]
        amt_paid_firm2_cash = 0
    elif each[-1] >= trans_amt_firm2 :
        amt_paid_firm2_cash = trans_amt_firm2
        amt_paid_firm1_cash = each[-1] - trans_amt_firm2
    else:
        amt_paid_firm2_cash = each[-1]
        amt_paid_firm1_cash = 0
    
    trans_id = '21_'+str(i)
    sales_id = '21_'+str(each[2])
    i+=1
    if each[2] == None:
        id = "NULL"
    else:
        id = "'"+sales_id+"'"
    if each[-2] == None:
        bill_tot = "NULL"
    else:
        bill_tot=str(each[-2])
    print(trans_id)
    date2 = str(each[0])
    insert_time = date2 + " 00:00:"+"{:02.0f}".format(sec)
    sec+=1
    if sec==60:
        sec = 0
    sql = "insert into somanath2021.cashflow_sales (trans_id, trans_acc, trans_sales, trans_amt_firm1, amt_paid_firm1_cash,trans_amt_firm2,amt_paid_firm2_cash, trans_date, insert_time, insert_id) values('"+trans_id+"',"+str(each[1]+max_sup_id)+","+id+","+'{:.2f}'.format(trans_amt_firm1)+","+'{:.2f}'.format(round(amt_paid_firm1_cash,2))+","+'{:.2f}'.format(trans_amt_firm2)+","+'{:.2f}'.format(round(amt_paid_firm2_cash,2))+",'"+date2+"','"+insert_time+"',1)"
    c.execute(sql)
conn.commit()
"""