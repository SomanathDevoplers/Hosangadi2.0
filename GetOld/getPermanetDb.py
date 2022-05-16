from cmath import log
import datetime
from time import sleep, time
import mysql.connector
from requests import post
from PIL import Image,ImageTk
conn = mysql.connector.connect(host='localhost', user='root', password='#mysqlpassword5') 
c = conn.cursor(buffered=True)
from asyncio.windows_events import NULL
import datetime
from distutils.spawn import spawn
import time

now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")
import os

import shutil
#change now to some time before 2021 seconds increasing
#update somanath.products SET insert_time = '2021-01-01 00:00:00'
#Make changes so that only date<31st march is selected
#TAXES MANUAL ENTRY

#category_registry
"""
c.execute("select cat_name from may.category_registry order by cat_id")
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
    req = post("http://192.168.0.100:6000/cat/save" , params = parameters , files = files)

conn.commit()

"""

#category_registry

#cess_registry,gdt_registry direct entry first add gst then cess



#CATEGORY ENDS

#Accounts run supplier first change cash to cash sales in cutomer registry
"""
c.execute("select sup_name, sup_address , sup_phone , sup_email , sup_gst  from may.supplier_registry")
cust = c.fetchall()
for each in cust:
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
                "db_year" : '21'

                }
    files = []
    req = post("http://192.168.0.100:6000/accounts/save" , params = parameters , files = files)
"""
#UPDATE somanath.accounts set insert_time = '2021-01-01 00:00:00' ;
#for cashfllow and ther report checks insert time for min db selection



#Check for distinct cust_name first
#change cash to cash sales
"""
c.execute("select cust_name, cust_address , cust_phone , cust_email , cust_type  from may.customer_registry")
cust = c.fetchall()
i=0
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
        ctype = "NML"
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
                "acc_gstin" : "CASH",
                "acc_accno" : "" ,
                "acc_ifsc" :  "",
                "acc_cus_type" :  ctype,
                "acc_img" : False ,
                "db_year" : '21'
                }
    
    files = []

    req = post("http://192.168.0.100:6000/accounts/save" , params = parameters , files = files)

"""

#ACCOUNTS ENDS




#Products Entry

"""
c.execute("select prod_name,prod_bar, prod_bar_1, prod_bar_2 , cat_id , sup_id_1, sup_id_2, sup_id_3, gst_id , cess_id , prod_minqty, prod_hsn , prod_mrp ,prod_unit, prod_unit_1, prod_unit_2, prod_unit_3 ,  prod_name_k , prod_id , sup_id_4 , sup_id_5 from may.product_registry order by prod_id")
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
        

    c.execute("select gst_per from may.gst_registry where gst_id = "+str(each[8]))
    gst = c.fetchone()[0]

    c.execute("select cess_per from may.cess_registry where cess_id = "+str(each[9]))
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
            "img_high" : False , 
            "img_low" : False

        }

    #c:\\users\\vijay alla c:\\users\\User  use homedir method
    #prod_id, prod_bar, prod_name, prod_cat, prod_hsn, prod_shelf, prod_name_kan, prod_name_eng, prod_min_qty, prod_expiry, prod_mrp, prod_mrp_old, prod_sup, prod_gst, prod_cess, prod_unit_type, nml_unit, htl_unit, spl_unit, ang_unit, prod_hide, prod_desc, high_img, low_img, insert_time, insert_id, update_time, update_id

    path = os.path.join(os.path.expanduser('~')+"\\angadiImages\\products" , str(each[-3]))
    os.mkdir(path)


   

    #prod_id, prod_bar, prod_name, prod_cat, prod_hsn, prod_shelf, prod_name_eng, prod_min_qty, prod_expiry, prod_mrp, prod_mrp_old, prod_sup, prod_gst, prod_cess, prod_unit_type, nml_unit, htl_unit, spl_unit, ang_unit, prod_hide, prod_desc, kan_img, high_img, low_img, insert_time, insert_id, update_time, update_id
    sql2 = "insert into somanath.products values ("+ str(each[-3])   +",'" + parameters['prod_bar'] + "','"+ parameters['prod_name'] + "','"+ parameters['prod_cat'] + "','" + str(parameters['prod_hsn']) + "','" + parameters['prod_shelf'] +"','','" +parameters['prod_name_eng'] + "'," + str(parameters['prod_min_qty']) + "," + str(parameters['prod_expiry']) + "," + str(parameters['prod_mrp']) + "," + str(parameters['prod_mrp_old']) + ",'" + parameters['prod_sup'] + "', (select tax_id from somanath.taxes where tax_type = 0 and tax_per = " + str(parameters['prod_gst']) + ") , (select tax_id from somanath.taxes where tax_type = 1 and tax_per = " + str(parameters['prod_cess']) + "),'" + parameters['prod_unit_type'] +"','" + parameters['nml_unit'] + "','"   + parameters['htl_unit'] + "','"  + parameters['spl_unit'] + "','"  + parameters['ang_unit'] + "','False','" + parameters['prod_desc'] +"','"+  str(parameters['img_high']) + "','" + str(parameters['img_low']) +"','" + now + "',(select user_id from somanath.users where user_name = '"+parameters['user_name']+"') , NULL , NULL)"
    c.execute(sql2)

conn.commit()
"""

#Entry of missig prod_id Product
"""
c.execute("SELECT prod_id FROM may.product_registry order by prod_id;")
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
i = 0 
for each in res:
    i+=1
    prod_name = "Edit New"+str(i)

    
    

    
    prod_bar = ":REPLACE"+str(i)+":" 
    
    

    cat  = 44
        

    
    gst = 1

    
    cess = 6

    sup = ":42:"
    

    



    nml = ":1:1:1:1:"  
    
    hsn = ""


    qty = 0
    
    mrp = "0.00"
    

    parameters = {
            "prod_id"   : "",
            "user_name" :  "ADMIN" ,
            "prod_bar"  :  prod_bar , 
            "prod_name" : prod_name , 
            "prod_cat"  : ":"+str(cat)+":" ,
            "prod_hsn"  : hsn , 
            "prod_shelf": "",
            "prod_name_eng" : "" , 
            "prod_min_qty" :  qty,
            "prod_expiry" : 0 ,
            "prod_mrp"  : mrp , 
            "prod_mrp_old" :  mrp, 
            "prod_sup"  : sup ,
            "prod_gst"  : gst ,
            "prod_cess" : cess,
            "prod_unit_type": 'N',
            "nml_unit"  : nml,
            "htl_unit"  : nml,
            "ang_unit"  : nml,
            "spl_unit"  : nml,
            "prod_desc" : "" ,
            "img_high" : False , 
            "img_low" : False
        }

    #c:\\users\\vijay alla c:\\users\\User  use homedir method
    #check if file created for missing prod_id
    path = os.path.join(os.path.expanduser('~')+"\\angadiImages\\products" , str(each))
    os.mkdir(path)

    #prod_id, prod_bar, prod_name, prod_cat, prod_hsn, prod_shelf, prod_name_eng, prod_min_qty, prod_expiry, prod_mrp, prod_mrp_old, prod_sup, prod_gst, prod_cess, prod_unit_type, nml_unit, htl_unit, spl_unit, ang_unit, prod_hide, prod_desc, kan_img, high_img, low_img, insert_time, insert_id, update_time, update_id
    sql2 = "insert into somanath.products values ("+ str(each)   +",'" + parameters['prod_bar'] + "','"+ parameters['prod_name'] + "','"+ parameters['prod_cat'] + "','" + str(parameters['prod_hsn']) + "','" + parameters['prod_shelf'] + "','','" +parameters['prod_name_eng'] + "'," + str(parameters['prod_min_qty']) + "," + str(parameters['prod_expiry']) + "," + str(parameters['prod_mrp']) + "," + str(parameters['prod_mrp_old']) + ",'" + parameters['prod_sup'] + "', (select tax_id from somanath.taxes where tax_type = 0 and tax_per = " + str(parameters['prod_gst']) + ") , (select tax_id from somanath.taxes where tax_type = 1 and tax_per = " + str(parameters['prod_cess']) + "),'" + parameters['prod_unit_type'] +"','" + parameters['nml_unit'] + "','"   + parameters['htl_unit'] + "','"  + parameters['spl_unit'] + "','"  + parameters['ang_unit'] + "','False','" + parameters['prod_desc'] + "','" + str(parameters['img_high']) + "','" + str(parameters['img_low']) +"','" + now + "',(select user_id from somanath.users where user_name = '"+parameters['user_name']+"') , NULL , NULL)"
    c.execute(sql2)

conn.commit()

"""
#PRODUCTS ENDS
