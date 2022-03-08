from asyncio.windows_events import NULL
import datetime
from distutils.spawn import spawn
import mysql.connector
from numpy import insert 
from requests import post
from PIL import Image,ImageTk
conn = mysql.connector.connect(host='localhost', user='root', password='mysqlpassword5') 
c = conn.cursor(buffered=True)
import time
now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")
import os

import shutil
max_acc_id = 107
max_purchase = 0
max_sales = 0
max_stocks = 0 
max_cashflow = 0
max_firm1 = 0
max_firm2 = 0
max_firm3 = 0



"""

c.execute("select cat_name from new_schema.category_registry order by cat_id")
cat = c.fetchall()

for each in cat:
    parameters = {
                    'cat_id': "",
                    'cat_name' : each[0],
                    'user_name': "ADMIN",
                    'cat_image':False 
                }
    files = []
    print(each)
    req = post("http://localhost:6000/cat/save" , params = parameters , files = files)


conn.commit()

c.execute("select sup_name, sup_address , sup_phone , sup_email , sup_gst  from new_schema.supplier_registry order by sup_id")
supp = c.fetchall()
for each in supp:
    sup_name = each[0]
    sup_name = each[0]
    sup_name = sup_name.replace("." , "")
    sup_name = sup_name.replace("*" , "")
    sup_name = sup_name.replace("+" , "")
    sup_name = sup_name.replace("-" , "")
    sup_name = sup_name.replace("!" , "")
    sup_name = sup_name.replace("@" , "")
    sup_name = sup_name.replace("#" , "")
    sup_name = sup_name.replace("$" , "")
    sup_name = sup_name.replace("%" , "")
    sup_name = sup_name.replace("^" , "")
    sup_name = sup_name.replace("&" , "")
    sup_name = sup_name.replace("(" , "")
    sup_name = sup_name.replace(")" , "")
    sup_name = sup_name.replace("_" , "")
    sup_name = sup_name.replace("=" , "")
    sup_name = sup_name.replace("{" , "")
    sup_name = sup_name.replace("}" , "")
    sup_name = sup_name.replace("[" , "")
    sup_name = sup_name.replace("]" , "")
    sup_name = sup_name.replace("\\" , "")
    sup_name = sup_name.replace("|" , "")
    sup_name = sup_name.replace(";" , "")
    sup_name = sup_name.replace(":" , "")
    sup_name = sup_name.replace("\"" , "")
    sup_name = sup_name.replace("'" , "")
    sup_name = sup_name.replace("<" , "")
    sup_name = sup_name.replace(">" , "")
    sup_name = sup_name.replace("?" , "")
    sup_name = sup_name.replace("," , "")
    sup_name = sup_name.replace("/" , "")



    parameters = {
                "acc_id" : "" ,
                "user_name" : "ADMIN" ,
                "acc_type" : "SUPP" ,
                "acc_name" : each[0] , 
                "acc_email":each[3] , 
                "acc_add" : each[1] ,
                "acc_mob1" : each[2] ,
                "acc_mob2" : "" ,
                "acc_gstin" : each[4],
                "acc_accno" : "" ,
                "acc_ifsc" :  "",
                "acc_cus_type" :  "",
                "acc_img" : False , 

                }
    files = []
    print(each)
    req = post("http://localhost:6000/accounts/save" , params = parameters , files = files)

c.execute("select max(acc_id) from somanath.accounts")
max_acc_id = c.fetchone()[0] 

c.execute("select cust_name, cust_address , cust_phone , cust_email , cust_type  from new_schema.customer_registry order by cust_id")
cust = c.fetchall()

for each in cust:
    cust_name = each[0]
    cust_name = cust_name.replace("." , "")
    cust_name = cust_name.replace("*" , "")
    cust_name = cust_name.replace("+" , "")
    cust_name = cust_name.replace("-" , "")
    cust_name = cust_name.replace("!" , "")
    cust_name = cust_name.replace("@" , "")
    cust_name = cust_name.replace("#" , "")
    cust_name = cust_name.replace("$" , "")
    cust_name = cust_name.replace("%" , "")
    cust_name = cust_name.replace("^" , "")
    cust_name = cust_name.replace("&" , "")
    cust_name = cust_name.replace("(" , "")
    cust_name = cust_name.replace(")" , "")
    cust_name = cust_name.replace("_" , "")
    cust_name = cust_name.replace("=" , "")
    cust_name = cust_name.replace("{" , "")
    cust_name = cust_name.replace("}" , "")
    cust_name = cust_name.replace("[" , "")
    cust_name = cust_name.replace("]" , "")
    cust_name = cust_name.replace("\\" , "")
    cust_name = cust_name.replace("|" , "")
    cust_name = cust_name.replace(";" , "")
    cust_name = cust_name.replace(":" , "")
    cust_name = cust_name.replace("\"" , "")
    cust_name = cust_name.replace("'" , "")
    cust_name = cust_name.replace("<" , "")
    cust_name = cust_name.replace(">" , "")
    cust_name = cust_name.replace("?" , "")
    cust_name = cust_name.replace("," , "")
    cust_name = cust_name.replace("/" , "")
    

    

    if each[4] == 0:
        ctype = "NRM"
    if each[4] == 1:
        ctype = "HTL"
    if each[4] == 2:
        ctype = "SPL"
    if each[4] == 3:
        ctype = "ANG"

    parameters = {
                "acc_id" : "" ,
                "user_name" : "ADMIN" ,
                "acc_type" : "CUST" ,
                "acc_name" :cust_name , 
                "acc_email":each[3] , 
                "acc_add" : each[1] ,
                "acc_mob1" : each[2] ,
                "acc_mob2" : "" ,
                "acc_gstin" : "",
                "acc_accno" : "" ,
                "acc_ifsc" :  "",
                "acc_cus_type" :  ctype,
                "acc_img" : False , 

                }
    files = []
    print(each)
    req = post("http://localhost:6000/accounts/save" , params = parameters , files = files)




conn.commit()





c.execute("select prod_name,prod_bar, prod_bar_1, prod_bar_2 , cat_id , sup_id_1, sup_id_2, sup_id_3, gst_id , cess_id , prod_minqty, prod_hsn , prod_mrp ,prod_unit, prod_unit_1, prod_unit_2, prod_unit_3 ,  prod_name_k , prod_id , sup_id_4 , sup_id_5 from new_schema.product_registry order by prod_id")
a = c.fetchall()

for each in a:
    prod_name = each[0]

    print(each[-3])
    

    prod_bar = ":"
    if each[1] != "" and each[1] != None and each[1] != 'NULL':
        prod_bar += each[1] + ":"
    if each[2] != "" and each[2] != None and each[2] != 'NULL':
        prod_bar += each[2] + ":"
    if each[3] != "" and each[3] != None and each[3] != 'NULL':
        prod_bar += each[3] + ":"

    if prod_bar == ":":
        prod_bar = "" 
    
    

    cat  = each[4]
        

    c.execute("select gst_per from new_schema.gst_registry where gst_id = "+str(each[8]))
    gst = c.fetchone()[0]

    c.execute("select cess_per from new_schema.cess_registry where cess_id = "+str(each[9]))
    cess = c.fetchone()[0]

    sup = ":"
    if each[5] != None and each[5] != "":
        sup += str(each[5])+ ":"

    if each[6] != None and each[6] != "":
         sup += str(each[6])+ ":"
    
    if each[7] != None and each[7] != "":
        sup += str(each[7])+ ":"
        
    if sup == ":" and each[19] != None and each[19] != "":
         sup += str(each[19])+ ":"

    if sup == ":" and each[20] != None and each[20] != "":
         sup += str(each[20])+ ":"

    



    nml = ":"+"{:.3f}".format(each[14])+":"+"{:.3f}".format(each[15])+":"+"{:.3f}".format(each[16])+":"+"{:.3f}".format(each[16])+":"  
    
    hsn = ""
    if each[11]!="" and each[11]!=None and each[11]!="NULL":
        hsn = each[11]

    qty = each[10]
    if qty != None:
        qty = "{:.2f}".format(qty)
    else:
        qty = "0.00"
    mrp = each[12]
    if mrp != None:
        mrp = "{:.2f}".format(mrp)
    else:
        mrp = "0.00"

    parameters = {
            "prod_id"   : "",
            "user_name" :  "ADMIN" ,
            "prod_bar"  :  prod_bar , 
            "prod_name" : prod_name , 
            "prod_cat"  : ":"+str(cat)+":" ,
            "prod_hsn"  : hsn , 
            "prod_shelf": "",
            "prod_name_eng" : each[0] , 
            "prod_min_qty" :  qty,
            "prod_expiry" : 0 ,
            "prod_mrp"  : mrp , 
            "prod_mrp_old" :  mrp, 
            "prod_sup"  : sup ,
            "prod_gst"  : gst ,
            "prod_cess" : cess,
            "prod_unit_type": each[13],
            "nml_unit"  : nml,
            "htl_unit"  : nml,
            "ang_unit"  : nml,
            "spl_unit"  : nml,
            "prod_desc" : "" ,
            "img_kan"   : False , 
            "img_high" : False , 
            "img_low" : False

        }

    
    path = os.path.join("C:\\Users\\vijay\\angadiImages\\products" , str(each[-3]))
    os.mkdir(path)


    if each[17]:
        parameters['img_kan'] = "True"
        kan = "C:\\Users\\vijay\\Desktop\\Kan_name\\"+str(each[18])+".png"
        shutil.copy(kan , path)

    #prod_id, prod_bar, prod_name, prod_cat, prod_hsn, prod_shelf, prod_name_eng, prod_min_qty, prod_expiry, prod_mrp, prod_mrp_old, prod_sup, prod_gst, prod_cess, prod_unit_type, nml_unit, htl_unit, spl_unit, ang_unit, prod_hide, prod_desc, kan_img, high_img, low_img, insert_time, insert_id, update_time, update_id
    sql2 = "insert into somanath.products values ("+ str(each[-3])   +",'" + parameters['prod_bar'] + "','"+ parameters['prod_name'] + "','"+ parameters['prod_cat'] + "','" + str(parameters['prod_hsn']) + "','" + parameters['prod_shelf'] + "','" +parameters['prod_name_eng'] + "'," + str(parameters['prod_min_qty']) + "," + str(parameters['prod_expiry']) + "," + str(parameters['prod_mrp']) + "," + str(parameters['prod_mrp_old']) + ",'" + parameters['prod_sup'] + "', (select tax_id from somanath.taxes where tax_type = 0 and tax_per = " + str(parameters['prod_gst']) + ") , (select tax_id from somanath.taxes where tax_type = 1 and tax_per = " + str(parameters['prod_cess']) + "),'" + parameters['prod_unit_type'] +"','" + parameters['nml_unit'] + "','"   + parameters['htl_unit'] + "','"  + parameters['spl_unit'] + "','"  + parameters['ang_unit'] + "','False','" + parameters['prod_desc'] + "','" + str(parameters['img_kan']) + "','" + str(parameters['img_high']) + "','" + str(parameters['img_low']) +"','" + now + "',(select user_id from somanath.users where user_name = '"+parameters['user_name']+"') , NULL , NULL)"
    c.execute(sql2)

conn.commit()

#permanent db ends 


c.execute("select sup_id , sup_name , sup_bal , opn_bal from new_schema.supplier_registry")
sup = c.fetchall()

for each in sup:
    c.execute("insert into somanath2021.acc_bal (acc_id, acc_cls_bal , acc_opn_bal) values("+str(each[0]) +","+"{:.2f}".format(each[2])+","+"{:.2f}".format(each[3])+")")



c.execute("select cust_id , cust_name , cust_bal , open_bal from new_schema.customer_registry")
cust = c.fetchall()

for each in cust:
    c.execute("insert into somanath2021.acc_bal (acc_id, acc_cls_bal , acc_opn_bal) values("+str(each[0] + max_acc_id) +","+"{:.2f}".format(each[2])+","+"{:.2f}".format(each[3])+")")



"""




#purchase , cashflow , stocks
sql = "select distinct(pur_id), sup_id from new_schema.purchase_registry order by pur_id"
c.execute(sql)
pur_id1 = c.fetchall()
pur_id = []

for each in pur_id1:    
    sql = "select acc_id from somanath.accounts where acc_type = 'SUPP' and acc_id = "+str(each[1])
    c.execute(sql)
    pur_id.append((each[0],c.fetchone()[0] , each[1]))



i = 1
j = 1
for each in pur_id:
    c.execute("select * from new_schema.purchase_registry where pur_id = "+str(each[0]))
    pur = c.fetchall()

    id = "21_" + str(pur[0][0])
    inv = pur[0][3]
    exp = "{:.2f}".format(pur[0][7])
    paid = "{:.2f}".format(pur[0][6])

    date2 = str(pur[0][1])

    insert_time = date2 + " 00:00:00"

    prod_id = ":"
    prod_cp = ":"
    prod_qty_pur = ":"
    
    stk_sql = "insert into somanath2021.stocks ( stk_id , stk_pur_id, stk_prod_id, stk_prod_qty, stk_tot_qty, stk_cost, stk_sp_nml, stk_sp_htl, stk_sp_spl, stk_sp_ang, stk_exp, stk_firm_id, insert_time, insert_id) values"

    sql = "select cash from new_schema.supplier_registry where sup_id = "+str(each[2])
    c.execute(sql)
    pur_firm_id = c.fetchone()[0]+1
    
    for row in pur:
        p_id = row[4]
        prod_id += str(p_id)+":"

        c.execute("select cost_price , sell_price_1 , sell_price_2 , sell_price_3 , tot_qty , pro_hotel , pro_family , pro_special , prod_qty  from new_schema.stocks where prod_id = "+str(row[4])+" and pur_id = "+str(pur[0][0]))
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
        stk_sql +=  "('"+str(stk_id)+"','"+str(id)+"',"+str(p_id)+","+prod_qty_stk+","+"{:.2f}".format(stk[4])+","+"{:.2f}".format(stk[0]) + ",'"+nml + "','"+htl + "','"+spl+"','"+ang+"',0,"+str(pur_firm_id)+",'"+insert_time+"',1),"
        j+=1

        

    stk_sql = stk_sql[0:-1]

    
    
    

    sql = "insert into somanath2021.purchases (pur_id, pur_acc, pur_firm_id, pur_inv, pur_prod_id, pur_prod_qty, pur_exp, pur_date, insert_time, insert_id) values('"+str(id)+"',"+str(each[1])+","+str(pur_firm_id)+",'"+str(inv)+"','"+str(prod_id)+"','"+prod_qty_pur+"',"+str(exp)+",'"+date2+"','"+insert_time+"',1)"
    c.execute(sql)

    trans_id = "21_"+str(i)
    sql = "insert into somanath2021.cashflow (trans_id, trans_acc,  trans_pur, trans_amt, trans_type, trans_mode, trans_date, insert_time, insert_id) values('"+trans_id+"',"+str(each[1])+",'"+id+"',"+ paid+ ",'DEB', 'CASH' , '"+date2+"','"+insert_time+"',1)"
    c.execute(sql)

    c.execute(stk_sql)
    i+=1

    print("pur_id" , i)

    max_purchase = pur[0][0]
    max_cashflow = i - 1
    max_stocks = j-1



"""

#sales ,
q1 = 1
while(q1<=17000):
    
    q2 = q1+99
    sql = "select distinct(sale_id), cust_id , disc , sale_date  from new_schema.sales_registry where sale_id >= "+str(q1) +" and sale_id<= "+str(q2) + " order by sale_id"
    q1 = q2+1
    c.execute(sql)
    sale_id = c.fetchall()

    cash = 0
    gst = 0

    sql = "insert into somanath2021.sales(sales_id ,  sales_ref , sales_acc , sales_prod_id, sales_pur_id, sales_prod_qty, sales_prod_sp, sale_date, freight, discount, insert_time, insert_id)values"
    sql_sp = "insert into somanath2021.sales_sp(sales_id, prod_id, cost_price, units, sp_list, gst_value , cess_value) values "

    for each in sale_id:
        sale_id = "21_"+str(each[0])
        cust_id = each[1]
        disc = "{:.2f}".format(each[2])
        date = str(each[3])
    
        
        c.execute("select  prod_id , cp , sp , prod_qty , pur_id , prod_unit_stocks , SP_list , cess , gst , cash from new_schema.sales_registry where sale_id = "+str(each[0]))
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
        prod_cp_cash = ":"
        prod_units_gst = "::"
        prod_units_cash = ":"
        prod_sp_list_cash = ":"
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
                units[a] = float(i)
                a+=1
            units.sort()

            temp_units = units
            units = []
            for all in temp_units:
                units.append("{:.3f}".format(all))




            sp_list = row[6][1:-1].split(',')
            a=0
            for i in sp_list:
                sp_list[a] = float(i)
                a+=1
            sp_list.sort()

            temp_sp = sp_list
            sp_list = []
            for all in temp_sp:
                sp_list.append("{:.2f}".format(all))


            

            if prod_firm == 1:
                prod_id_gst += str(row[0]) + ":"
                prod_qty_gst +=  "{:.3f}".format(row[3]) + ":"
                pur_id_gst += "21_"+str(row[4]) + ":"
                prod_sp_gst += "{:.3f}".format(row[2]) + ":"
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
                prod_cp_cash += "{:.3f}".format(row[1]) + ":"
                prod_gst_cash += str(row[8])+":"
                prod_cess_cash += str(row[7])+":"
                for i in units:
                    prod_units_cash += str(i) + ":"
                prod_units_cash += ":"
                for i in sp_list:
                    prod_sp_list_cash += str(i) + ":"
                prod_sp_list_cash += ":"
        
        sql_sp += "('"+sale_id+"','"+prod_id_gst+prod_id_cash[1:]+"','"+ prod_cp_gst+prod_cp_cash[1:]+"','"+prod_units_gst+prod_units_cash[1:-1]+"','"+prod_sp_list_gst+prod_sp_list_cash[1:-1]+"','"+prod_gst_gst+prod_gst_cash[1:]+"','"+prod_cess_gst+prod_cess_cash[1:]+"'),"

        if prod_id_gst != ":":
            gst += 1
            sql += "('"+sale_id+"','SSM_"+str(gst)+"',"+str(cust_id+max_acc_id)+",'"+prod_id_gst+"','"+pur_id_gst+"','"+prod_qty_gst+"','"+prod_sp_gst+"','"+date+"',0.00,"+str(disc)+",'"+str(now)+"',1"+"),"
            

        if prod_id_cash != ":":
            cash += 1
            sql += "('"+sale_id+"','SCM_"+str(cash)+"',"+str(cust_id+max_acc_id)+",'"+prod_id_cash+"','"+pur_id_cash+"','"+prod_qty_cash+"','"+prod_sp_cash+"','"+date+"',0.00,"+disc+",'"+now+"',1"+"),"    

        
        

        print("sale_id" , sale_id)
        max_sales = sale_id
        max_firm1 = gst
        max_firm2 = cash
    
    

    c.execute(sql[0:-1])
    c.execute(sql_sp[0:-1])
    conn.commit()


#SALES_CASHFLOW TRANSFER
sql = 'SELECT * FROM new_schema.sales_cashflow'
c.execute(sql)
sale_cashflow = c.fetchall()

sql = 'INSERT into somanath2021.cashflow (trans_id, trans_acc, trans_sales, trans_amt, amt_paid, trans_type, trans_mode, trans_date, insert_time, insert_id) values '
x=""
i=0
for each in sale_cashflow:
   
    if each[3] != None:
        bill_id = "'21_"+str(each[3])+"'"
        amt_paid = str(each[5])
    else:
        bill_id = "NULL"
        amt_paid = "NULL"
    x += "('21_"+str(each[0]+2152)+"',"+str(each[2]+max_acc_id) +","+bill_id+","+amt_paid+ ","+str(each[4])+","+"'CRD','CASH','"+str(each[1])+"','"+str(each[1])+" 00:00:00"+"',"+str(1)+"),"
    
sql += x[:-1]
c.execute(sql)







"""


print(max_purchase , max_sales , max_stocks , max_cashflow ,max_firm1 ,max_firm2 , max_firm3)







conn.commit()
    

