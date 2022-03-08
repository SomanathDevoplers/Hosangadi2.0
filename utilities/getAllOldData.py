import datetime
import mysql.connector
from numpy import insert 
from requests import post
from PIL import Image,ImageTk
conn = mysql.connector.connect(host='localhost', user='root', password='mysqlpassword5') 
c = conn.cursor(buffered=True)



#permanaent data base only once for all
"""
c.execute("select cust_name, cust_address , cust_phone , cust_email , cust_type  from new_schema.customer_registry order by cust_name")
cust = c.fetchall()

for each in cust:

    cust_name = each[0]
    #cust_name = cust_name.replace("." , "")
    #cust_name = cust_name.replace("*" , "")
    #cust_name = cust_name.replace("+" , "")
    #cust_name = cust_name.replace("-" , "")
    #cust_name = cust_name.replace("!" , "")
    #cust_name = cust_name.replace("@" , "")
    #cust_name = cust_name.replace("#" , "")
    #cust_name = cust_name.replace("$" , "")
    #cust_name = cust_name.replace("%" , "")
    #cust_name = cust_name.replace("^" , "")
    #cust_name = cust_name.replace("&" , "")
    #cust_name = cust_name.replace("(" , "")
    ###cust_name = cust_name.replace(")" , "")
    #cust_name = cust_name.replace("_" , "")
    #cust_name = cust_name.replace("=" , "")
    #cust_name = cust_name.replace("{" , "")
    #cust_name = cust_name.replace("}" , "")
    #cust_name = cust_name.replace("[" , "")
    #cust_name = cust_name.replace("]" , "")
    #cust_name = cust_name.replace("\\" , "")
    #cust_name = cust_name.replace("|" , "")
    #cust_name = cust_name.replace(";" , "")
    #cust_name = cust_name.replace(":" , "")
    #cust_name = cust_name.replace("\"" , "")
    #cust_name = cust_name.replace("'" , "")
    #cust_name = cust_name.replace("<" , "")
    #cust_name = cust_name.replace(">" , "")
    #cust_name = cust_name.replace("?" , "")
    #cust_name = cust_name.replace("," , "")
    #cust_name = cust_name.replace("/" , "")
    

    

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



c.execute("select sup_name, sup_address , sup_phone , sup_email , sup_gst  from new_schema.supplier_registry order by sup_name")
cust = c.fetchall()
for each in cust:
    sup_name = each[0]
    #sup_name = each[0]
    #sup_name = sup_name.replace("." , "")
    #sup_name = sup_name.replace("*" , "")
    #sup_name = sup_name.replace("+" , "")
    #sup_name = sup_name.replace("-" , "")
    #sup_name = sup_name.replace("!" , "")
    #sup_name = sup_name.replace("@" , "")
    #up_name = sup_name.replace("#" , "")
    ##up_name = sup_name.replace("$" , "")
    #up_name = sup_name.replace("%" , "")
    #sup_name = sup_name.replace("^" , "")
    #sup_name = sup_name.replace("&" , "")
    #sup_name = sup_name.replace("(" , "")
    #sup_name = sup_name.replace(")" , "")
    #sup_name = sup_name.replace("_" , "")
    #sup_name = sup_name.replace("=" , "")
    #sup_name = sup_name.replace("{" , "")
    #sup_name = sup_name.replace("}" , "")
    #sup_name = sup_name.replace("[" , "")
    #sup_name = sup_name.replace("]" , "")
    #sup_name = sup_name.replace("\\" , "")
    #sup_name = sup_name.replace("|" , "")
    #sup_name = sup_name.replace(";" , "")
    #sup_name = sup_name.replace(":" , "")
    #sup_name = sup_name.replace("\"" , "")
    #sup_name = sup_name.replace("'" , "")
    ##sup_name = sup_name.replace("<" , "")
    #sup_name = sup_name.replace(">" , "")
    #sup_name = sup_name.replace("?" , "")
    #sup_name = sup_name.replace("," , "")
    #sup_name = sup_name.replace("/" , "")



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






c.execute("select cat_name from new_schema.category_registry order by cat_name")
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

c.execute("select prod_name,prod_bar, prod_bar_1, prod_bar_2 , cat_id , sup_id_1, sup_id_2, sup_id_3, gst_id , cess_id , prod_minqty, prod_hsn , prod_mrp ,prod_unit, prod_unit_1, prod_unit_2, prod_unit_3 ,  prod_name_k , prod_id , sup_id_4 , sup_id_5 from new_schema.product_registry order by prod_name")
a = c.fetchall()
i = 1
for each in a:
    prod_name = each[0]
    

    i+=1
    print(i)

    prod_bar = ":"
    if each[1] != "" and each[1] != None:
        prod_bar += each[1] + ":"
    if each[2] != "" and each[2] != None:
        prod_bar += each[2] + ":"
    if each[3] != "" and each[3] != None:
        prod_bar += each[3] + ":"

    if prod_bar == ":":
        prod_bar = "" 
    
    
    try:
        c.execute("select cat_id from somanath.categories where cat_name = (select cat_name from new_schema.category_registry where cat_id = "+str(each[4])+")")
        cat = c.fetchone()[0]
    except:
        print(each[4] , each[-1])
        

    c.execute("select gst_per from new_schema.gst_registry where gst_id = "+str(each[8]))
    gst = c.fetchone()[0]
    c.execute("select cess_per from new_schema.cess_registry where cess_id = "+str(each[9]))
    cess = c.fetchone()[0]

    sup = ":"
    if each[5] != None and each[5] != "":
        sql = "select acc_id from somanath.accounts where acc_name = (select sup_name from new_schema.supplier_registry where sup_id = "+str(each[5])+")"
        c.execute(sql)
        sup1 = c.fetchone()
        if sup1 != None:
            sup += str(sup1[0])+ ":"

    if each[6] != None and each[6] != "":
        sql = "select acc_id from somanath.accounts where acc_name = (select sup_name from new_schema.supplier_registry where sup_id = "+str(each[6])+")"
        c.execute(sql)
        sup1 = c.fetchone()
        if sup1 != None:
            sup += str(sup1[0])+ ":"
    
    if each[7] != None and each[7] != "":
        sql = "select acc_id from somanath.accounts where acc_name = (select sup_name from new_schema.supplier_registry where sup_id = "+str(each[7])+")"
        c.execute(sql)
        sup1 = c.fetchone()
        if sup1 != None:
            sup += str(sup1[0])+ ":"
        
    if sup == ":" and each[-2] != None and each[-2] != "":
        sql = "select acc_id from somanath.accounts where acc_name = (select sup_name from new_schema.supplier_registry where sup_id = "+str(each[-2])+")"
        c.execute(sql)
        sup1 = c.fetchone()
        if sup1 != None:
            sup += str(sup1[0])+ ":"

    if sup == ":" and each[-1] != None and each[-1] != "":
        sql = "select acc_id from somanath.accounts where acc_name = (select sup_name from new_schema.supplier_registry where sup_id = "+str(each[-1])+")"
        c.execute(sql)
        sup1 = c.fetchone()
        if sup1 != None:
            sup += str(sup1[0])+ ":"
    r = ""
    print(sup)
    if sup == ":":
        print(each[-3])
        input(r)



    nml = ":"+str(each[14])+":"+str(each[15])+":"+str(each[16])+":"+str(each[16])+":"  
    
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

    files = []

    if each[17]:
        parameters['img_kan'] = "True"
        kan = "C:\\Users\\vijay\\Desktop\\Kan_name\\"+str(each[18])+".png"
        files.append(('images', (kan, open(kan, 'rb'), 'images/png')))
        

    req = post("http://localhost:6000/products/save" , params = parameters , files = files)



#permanent data base ends here





#purchase , cashflow , stocks ends here




#sales , cashflow


#open bal_insert
c.execute("select cust_id , cust_name , open_bal from new_schema.customer_registry order by cust_name")
cust = c.fetchall()
cust_2 = []
for each in cust:
    cust_name = each[1]
    if cust_name == "CASH":
        cust_name = "CASH CASH"
    c.execute("select acc_id from somanath.accounts where acc_name = '"+cust_name+"'")
    cust_2.append([ each[0] , c.fetchone()[0] , each[2] , each[1] ])
    
for each in cust_2:
    print(each)
    try:
        c.execute("insert into somanath2021.acc_bal (acc_id, acc_opn_bal) values("+str(each[1]) +","+"{:.2f}".format(each[2])+")")
    except mysql.connector.errors.IntegrityError:
        print(each , "here")



c.execute("select sup_id , sup_name , opn_bal from new_schema.supplier_registry order by sup_name")
sup = c.fetchall()
sup_2 = []
for each in sup:
    c.execute("select acc_id from somanath.accounts where acc_name = '"+each[1]+"'")
    sup_2.append([ each[0] , c.fetchone()[0] , each[2] , each[1] ])
    

for each in sup_2:
    print(each)
    c.execute("insert into somanath2021.acc_bal (acc_id, acc_opn_bal) values("+str(each[1]) +","+"{:.2f}".format(each[2])+")")
#open_bal ens here

"""


"""sql = "select distinct(sale_id) , cust_id from new_schema.sales_registry where sale_date < '2021-04-01' order by sale_id"
c.execute(sql)
sale_id1 = c.fetchall()
sale_id = []
for each in sale_id1:    
    sql = "select acc_id from somanath.accounts where acc_type = 'CUST' and acc_name = (select cust_name from new_schema.customer_registry where cust_id ="+str(each[1])+")"
    c.execute(sql)
    sale_id.append([each[0],c.fetchone()[0] , each[1]])
    


#cp, sp, prod_qty, prod_id, pur_id, cust_id, disc, amt_paid, sale_date, prod_unit_stocks, SP_list, cash, cess
i = 0
for each in sale_id:
    c.execute("select cp, sp, prod_qty, prod_id, pur_id, cust_id, disc, amt_paid, sale_date, prod_unit_stocks, SP_list from new_schema.sales_registry where sale_id = "+str(each[0]))
    sales = c.fetchall()

    prod_id = ":"
    prod_cp = ":"
    prod_qty = ":"
    stk_id = ":"
    sale_id = "21_"+str(i)
    
    #sales_id, sales_acc, sales_ref, sales_prod_id, sales_stk_id, sales_prod_qty, sales_prod_sp, sales_old_sp, sales_firm, sale_date, freight, discount, insert_time, insert_id, update_time, update_id
    for row in sales:
        
        pur_id = "21_"+str(row[4])

        c.execute("select prod_id from somanath.products where prod_name = (select prod_name from new_schema.product_registry where prod_id ="+str(row[3])+")")
        p_id = c.fetchone()[0]
        prod_id += str(p_id)+":"

        sql = "select stk_id from somanath2021.stocks where stk_prod_id = "+str(p_id)+" and stk_pur_id = '"+pur_id+"'"
        c.execute(sql)
        
        st_id = c.fetchone()[0]
        
        stk_id += st_id+":"


        
    quit()"""




#sales , cashflow ends here 
#2021 ends here



conn.commit()
#update prod_nae , acc_name , remove special chars
conn.close()