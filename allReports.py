#python file for monthly report
"""
from math import ceil
from reportlab.lib.pagesizes import A6
from reportlab.platypus import SimpleDocTemplate,Table,TableStyle,Spacer,Paragraph
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet
from webbrowser import open as edge
import os

from requests import get
from datetime import timedelta,datetime
#location change for file store
def getData(month,acc_id,acc_name,dbYear,year,nextMonth):
    acc_name = acc_name.title()
    #pass a month one greater
    lastDay = (str(datetime.strptime("20"+str(year)+"-"+nextMonth+"-05",'%Y-%B-%d').replace(day=1) - timedelta(days=1))).split(" ")[0]
    firstDay = lastDay[:-2]+"01"
    
    billYear = dbYear #add a drop down for selecting year 
    
    #to get monthly statement select month from dropdown Enter year in box if entry empty current year
    req1 = get("http://localhost:6000/onlySql", params={"sql" : 'SELECT count(sales_id) as count  FROM somanath20'+str(dbYear)+'.sales where sales_acc =930 and sale_date >= "'+firstDay+'" and sale_date <="'+lastDay+'"' })
    count = req1.json()[0]['count'] 
    if count == 0:
        print("Show msg no sales found for selected month")
        return
    req = get("http://localhost:6000/reports/getMontlyReport" , 
        params = { "acc_id" : acc_id , "limit" : count ,'sdate' :firstDay,'edate' :lastDay,
                    'invNo' : '' ,'db' : billYear }) #billYear+'_'+'1' = inv_no
    #print(type)
    
    values = [] 
    total = 0
    for each in req.json():
        x = req.json()[each]
        total += float(x[0][2])
        if len(str(x[1])) > 27:
            x[1] = x[1][:28]+'\n'+x[1][28:]
        
        values.append([x[1],x[0][0],x[0][1],x[0][2]])
    values.sort(key=lambda x: x[0])
    
    fileName=os.path.expanduser('~')+"\\Desktop\\Invoice\\_MonthlyReports\\"+acc_name+"_"+month+".pdf"
    data = [['Product Name', 'Price', 'Qty', 'Value']]
    for each in values:
        data.append(each)
    
    pdf = SimpleDocTemplate(fileName,pagesize=A6,rightMargin=20*mm, leftMargin=20*mm, topMargin=2*mm, bottomMargin=0)

    table = Table(data)
  
    style = TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.green),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('FONTNAME',(0,0),(-1,0),'Times-Bold'),
        ('ALIGN',(0,0),(-1,0),'LEFT'),
        ('ALIGN',(0,0),(1,-1),'LEFT'),
        ('ALIGN',(1,1),(-1,-1),'RIGHT'),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica'),
        ('FONTSIZE',(0,1),(0,-1),9),
        ('FONTSIZE',(1,1),(-1,-1),7),
        ('FONTSIZE',(0,0),(-1,0),12),
        ('BOTTOMPADDING',(0,0),(-1,0),6),
        ('BACKGROUND',(0,1),(-1,-1),colors.beige),
        ('GRID',(0,0),(-1,-1),1,colors.black),
        ])

    table.setStyle(style)

    rowNumb = len(data)
    for i in range(1, rowNumb):
        ts = TableStyle([('BACKGROUND',(0,i),(-1,i),colors.white)])
        table.setStyle(ts)
    elems = []

    elems.append(Paragraph("<font size=13>Sales Report "+month+"</font>",getSampleStyleSheet()['Title']))
    elems.append(Spacer(0,-10))
    elems.append(table)
    elems.append(Spacer(0,5))
    elems.append(Paragraph("<font size=10>Total Amount: Rs." +str("{:.00f}".format(ceil(total)))+"</font>",getSampleStyleSheet()['Title']))
    elems.append(Spacer(0,-10))
    elems.append(Paragraph("<font size=15><i>"+acc_name+"</i></font>",getSampleStyleSheet()['Title']))
    try:
        pdf.build(elems)
        homedir = os.path.expanduser("~").split('\\')[-1]
        edge(r"C:\\Users\\"+homedir+"\\Desktop\\Invoice\\_MonthlyReports\\"+acc_name+"_"+month+".pdf")
    except FileNotFoundError:
        print('show Error to create a _MonthlyReports file in invoice folder of desktop  ')

month = 'February'
acc_id = 478
acc_name = "HOTEL UDUPI SAVIRUCHI"
dbYear = '21'
nextMonth = 'March'
year = '21' #22 beacuse needed report of feb-2022
getData(month,acc_id,acc_name,dbYear,year,nextMonth)
"""

#Changes in report server for monthly report#onlySql is needed
#replace +452 with '' after correct import of sales
"""
//reports

function filterDataMontlhyReport( sales, clientResponse){
  let dictionary = {}
  let temp_dict_value = []

  for(var i = 0; i < sales.length; i++) {
    let temp_prod_id  = sales[i].sales_prod_id.split(":").slice(1,-1)
    let temp_sp       = sales[i].sales_prod_sp.split(":").slice(1,-1)
    let temp_qty      = sales[i].sales_prod_qty.split(":").slice(1,-1)
    
        for(var j = 0; j < temp_prod_id.length ; j++ ) {
          total_l = parseFloat(temp_sp[j])*parseFloat(temp_qty[j])
          try{
            temp_dict_value = dictionary[temp_prod_id[j]]
            qty_l = parseFloat(temp_dict_value[1]) + parseFloat(temp_qty[j])
            final_total = parseFloat(temp_dict_value[2]) + total_l
            dictionary[temp_prod_id[j]] = [(final_total/qty_l).toFixed(2),qty_l.toFixed(3),final_total.toFixed(2)]
          }
          catch(error1){
            dictionary[temp_prod_id[j]] = [parseFloat(temp_sp[j]).toFixed(2), parseFloat(temp_qty[j]).toFixed(3), total_l.toFixed(2)]
          }
        }
    
  }

  const prod_id_keys = Object.keys(dictionary);
  
  let count = 0 
  let k = 0
  for(k=0 ;k < prod_id_keys.length; k++){
    sql_only = "SELECT prod_name FROM somanath.products where prod_id = "+prod_id_keys[k]
    con.query(sql_only,(err1,result)=>{
      dictionary[prod_id_keys[count].toString()] = [dictionary[prod_id_keys[count].toString()] ,result[0]['prod_name']]
      count++
      if (count == k){clientResponse.send(dictionary);return}
    })
  }

}

function getoneMonthBills(  dbYear , mindbYear , acc_id , bills , nBill , max ,sqlwhere, clientResponse )
{
    
    if( dbYear < mindbYear )
      { 
        
        if( nBill == 0)
        {
          clientResponse.send("[]")
          return
        } 
        else{
          filterDataMontlhyReport( bills , clientResponse )
          return
        }
        
      }
    else if(nBill >= max)
     {
      filterDataMontlhyReport( bills , clientResponse )
      return
      }
    else
      {
        
        sql = "SELECT sales_prod_id,sales_prod_qty,sales_prod_sp,date_format(sale_date,'%d-%b-%y') as date  FROM somanath20"+dbYear+".sales where sales_acc ="+(parseInt(acc_id)+452)+ sqlwhere
        con.query(sql , (err , res) =>  {
                res.forEach(element => {

                  if(nBill < max){
                    bills.push(element)
                    nBill++
                  }
                });
                getoneMonthBills( dbYear-1 , mindbYear , acc_id , bills , nBill , max ,sqlwhere, clientResponse )

          })

      }


} 

app.get('/reports/getMontlyReport' ,  (req,res) => {
  accId = req.query.acc_id
  sqlmin = "SELECT date_format(insert_time,'%y') as year,date_format(insert_time,'%m') as month FROM somanath.accounts  where acc_id ="+accId
  con.query(sqlmin,(err,result)=>{
    y = parseInt(result[0].year)
    m = parseInt(result[0].month)
    if (y < 23 & m < 4){
      minYear = 21
    }
    else if (m < 4) minYear = y-1
    else minYear = y
    
    startDate = req.query.sdate
    endDate = req.query.edate
    noBills = req.query.limit
    
    year = parseInt(startDate.slice(2,4))
    month = parseInt(startDate.slice(3,5))

    if (year < 23 & month < 4)minYear = 21
    else if (month < 4) minYear = year-1
    else minYear = year

    sqlwhere = " and sale_date >= '"+startDate+"' and sale_date <='"+endDate+"'"

    getoneMonthBills(  req.query.db , minYear , accId , [] , 0 , noBills , sqlwhere , res)


  })

})


//reports

"""

from requests import get

from datetime import date, timedelta,datetime


#pass a month one greate
lastDay = (str(datetime.strptime("2022-March-05",'%Y-%B-%d').replace(day=1) - timedelta(days=1))).split(" ")[0]
firstDay = lastDay[:-2]+"01"

#if hotel set limit to 30 else 10 
billYear = '22' #add a drop down for selecting year 
# any of the parameter is null then send ''

#to get monthly statement select month from dropdown Enter year in box if entry empty current year

req = get("http://localhost:6000/reports/getCustomersales" , 
    params = { "acc_id" : 561 , "limit" : 1 ,'sdate' :firstDay,'edate' :firstDay,
                'invNo' : '' ,'db' : 22 }) #billYear+'_'+'1'



array_of_items = []

for each in req.json():
    x = req.json()[each]
    array_of_items.append([x[-1],x[-2],x[0][1],x[0][0],x[0][2]])
array_of_items.sort(key=lambda x: x[0])

#array_of_items = [[1, 'HASI MENASU', '0.250', '60.000', '21-Nov-20'], [1, 'ONION S', '1.000', '65.000', '21-Nov-20'], [2, 'SUGAR', '1.000', '38.000', '17-Nov-20'], [4, 'DAZZY ENDOR 2RS', 71, '2.000', '25-Nov-20'], [5, 'MENASU .', '0.250', '320.000', '25-Nov-20'], [6, 'MOONG MAHARAJA GOLD', '0.500', '100.000', '18-Nov-20'], [6, 'HURULI KALU', 2, '45.000', '21-Nov-20'], [9, 'RAVA B', '1.000', '32.000', '18-Nov-20'], [11, 'DEVAGIRI 250G', '1.000', '65.000', '20-Nov-20'], [18, 'RAJ NJOY HALDI CHANDAN 5*100G', '1.000', '73.000', '17-Nov-20'], [26, 'GIL PRESTO 20RS 3+1N', '0.250', '80.000', '25-Nov-20'], [28, 'ULLAS 12RS', 2, '10.000', '25-Nov-20'], [41, 'NANDINI CURD 200G', 4, '13.000', '25-Nov-20'], [41, 'NANDINI MILK 500ML', 4, '22.000', '25-Nov-20']]
y = 0
sorted_array = []
category_array = []


x = array_of_items[0][0]
for each in array_of_items:
    y = each[0]
    if x == y: category_array.append( each[1:] )
    else: 
        category_array.sort(key=lambda x: x[0][0])
        sorted_array.append(category_array)
        category_array = []
        category_array.append( each[1:] )
        x = each[0]
    y = x
category_array.sort(key=lambda x: x[0][0])
sorted_array.append(category_array)    

for each in sorted_array:
    for x in each:
        print(x)
        print('\n')
    




#cashFlow Sales and Purchase
"""
req = get("http://localhost:6000/reports/getCashflow" , 
        params = { "acc_id" : 172 , "limit" : 10 ,'sdate' :'2022-02-20','edate' :'',
                    'invNo' : '' ,'db' : 21 , 'pur_sale': "trans_pur" }) #billYear+'_'+'1' if salecashflow pur_sale : 'trans_sales' else 'trans_pur'

for each in req.json():
    print(each)
    print('\n')
"""

"""
function filterData( sales, clientResponse){
  let dictionary = {}
  let temp_dict_value = []

  for(var i = 0; i < sales.length; i++) {
    let temp_prod_id  = sales[i].sales_prod_id.split(":").slice(1,-1)
    let temp_sp       = sales[i].sales_prod_sp.split(":").slice(1,-1)
    let temp_qty      = sales[i].sales_prod_qty.split(":").slice(1,-1)
    let temp_date     = sales[i]["date_format(sale_date,'%d-%b-%y')"]
    
        for(var j = 0; j< temp_prod_id.length; j++){
          try{
            temp_dict_value = dictionary[temp_prod_id[j]]
            dictionary[temp_prod_id[j]] = [temp_sp[j],parseFloat(temp_dict_value[1])+parseFloat(temp_qty[j]),temp_date]
          }
          catch(error1){
            
            dictionary[temp_prod_id[j]] = [temp_sp[j],temp_qty[j],temp_date]
            
          }
        }
    
  }

  const prod_id_keys = Object.keys(dictionary);
  
  let count = 0
  let k = 0

  for(k=0 ;k < prod_id_keys.length; k++){
    sql_only = "SELECT prod_name,prod_cat FROM somanath.products where prod_id = "+prod_id_keys[k]
    con.query(sql_only,(err1,result)=>{
      dictionary[prod_id_keys[count].toString()] = [dictionary[prod_id_keys[count].toString()] ,result[0]['prod_name'],result[0]['prod_cat'].split(":")[1] ]
      count++
      if (count == k){clientResponse.send(dictionary);return}
    })
  }

}

function getOldBill(  dbYear , mindbYear , acc_id , bills , nBill , max ,sqlwhere, clientResponse )
{
    
    if( dbYear < mindbYear )
      { 
        
        if( nBill == 0)
        {
          
          clientResponse.send("[]")
          return
        }
        else{
          filterData( bills , clientResponse )
          return
        }
        
      }
    else if(nBill >= max)
      {
        filterData( bills , clientResponse )
        return
      }
    else
      {

        sql = "SELECT sales_prod_id,sales_prod_qty,sales_prod_sp,date_format(sale_date,'%d-%b-%y')  FROM somanath20"+dbYear+".sales where sales_acc ="+acc_id+ sqlwhere
        console.log(sql);
        con.query(sql , (err , res) =>  {
               
                res.forEach(element => {

                  if(nBill < max){
                    bills.push(element)
                    nBill++
                  }
                });
                
                getOldBill( dbYear-1 , mindbYear , acc_id , bills , nBill , max ,sqlwhere, clientResponse )

          })

      }


}

function getOldtrans(  dbYear , mindbYear  , bills , nBill , max ,sqlwhere,salePur, clientResponse )
{
    
    if( dbYear < mindbYear )
      { 
        
        if( nBill == 0)
        {
          clientResponse.send("[]")
          return
        }
        else{
          clientResponse.send(bills)
          return
        }
        
      }
    else if(nBill >= max)
      {
        clientResponse.send(bills)
        return 
      }
    else
      {

        sql = "SELECT "+salePur+",trans_amt,amt_paid,trans_mode,date_format(trans_date,'%d-%b-%y') as transdate FROM somanath20"+dbYear+".cashflow where "+ sqlwhere
        console.log(sql);
        con.query(sql , (err , res) =>  {
               
                res.forEach(element => {

                  if(nBill < max){
                    bills.push(element) 
                    nBill++
                  }
                });
                
                getOldtrans( dbYear-1 , mindbYear  , bills , nBill , max ,sqlwhere,salePur, clientResponse )

          })

      }


}

app.get('/reports/getCustomersales' ,  (req,res) => {
  minYear = 21
  accId = req.query.acc_id
  
  sqlmin = "SELECT date_format(insert_time,'%y') as year,date_format(insert_time,'%m') as month FROM somanath.accounts  where acc_id ="+109
  con.query(sqlmin,(err,result)=>{
    y = parseInt(result[0].year)
    m = parseInt(result[0].month)
    
    if (y < 23 & m < 4){
      minYear = 21
    }
    else if (m < 4) minYear = y-1
    else minYear = y
    
    startDate = req.query.sdate
  endDate = req.query.edate
  noBills = req.query.limit
  invNo   = req.query.invNo
  if (invNo.length > 0){ 
    sqlwhere = " and sales_id = '"+invNo+"'"
    noBills = 1
    }
  else if ( startDate != '' | endDate != '') {
    year = parseInt(startDate.slice(2,4))
    month = parseInt(startDate.slice(3,5))
      if (year < 23 & month < 4){
        minYear = 21
      }
      else if (month < 4) minYear = year-1
      else minYear = year
     if ( startDate == '') sqlwhere = " and sale_date <='"+endDate+"' order by sale_date DESC"
     else if (endDate == '') sqlwhere = " and sale_date >= '"+startDate+"' order by sale_date DESC"
     else sqlwhere = " and sale_date >= '"+startDate+"' and sale_date <='"+endDate+"' order by sale_date DESC"
  }
  else {sqlwhere = ' order by sale_date DESC limit '+ noBills}
  getOldBill(  req.query.db , minYear , accId , [] , 0 , noBills , sqlwhere , res)


  })
  
  
      
  
    
})

app.get('/reports/getCashflow' ,  (req,res) => {
  minYear = 21
  accId = req.query.acc_id
  salePur = req.query.pur_sale
  sqlmin = "SELECT date_format(insert_time,'%y') as year,date_format(insert_time,'%m') as month FROM somanath.accounts  where acc_id ="+accId
  
  con.query(sqlmin,(err,result)=>{
    y = parseInt(result[0].year)
    m = parseInt(result[0].month)
    
    if (y < 23 & m < 4){
      minYear = 21
    }
    else if (m < 4) minYear = y-1
    else minYear = y
    startDate = req.query.sdate

  endDate = req.query.edate
  noBills = req.query.limit
  invNo   = req.query.invNo

  if (invNo.length > 0){ 
    sqlwhere = salePur+" = '"+invNo+"'"
    noBills = 1
    }
  else if ( startDate != '' | endDate != '') {
    year = parseInt(startDate.slice(2,4))
    month = parseInt(startDate.slice(3,5))
      if (year < 23 & month < 4){
        minYear = 21
      }
      else if (month < 4) minYear = year-1
      else minYear = year
     if ( startDate == '') sqlwhere = "trans_acc = "+accId+" and trans_date <='"+endDate+"' order by trans_date DESC"
     else if (endDate == '') sqlwhere = "trans_acc = "+accId+" and trans_date >= '"+startDate+"' order by trans_date DESC"
     else sqlwhere = "trans_acc = "+accId+" and trans_date >= '"+startDate+"' and trans_date <='"+endDate+"' order by trans_date DESC"
  }
  else { sqlwhere = 'trans_acc = '+accId+' order by trans_date DESC limit '+ noBills }
  getOldtrans(  req.query.db , minYear  , [] , 0 , noBills , sqlwhere ,salePur, res)

  })
  
})

//reports
"""