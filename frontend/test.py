from requests import get

sql = "SELECT pur_id, pur_acc, pur_firm_id, pur_inv, pur_prod_id, pur_prod_qty, pur_exp, date_format(pur_date,'%d-%m-%Y'), tax_method, insert_time, insert_id FROM somanath20"+self.year+".purchases where pur_id = '"+ self.year +"_"+pur_id +"'"


req = get("http://"+self.ip+":5000/purchases/edit" , params = { "purchase" : resp[0]}) 