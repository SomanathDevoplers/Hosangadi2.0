const http = require('http');
const express = require('express');
const app = express();
const server = http.createServer(app);
const io = require('socket.io')(server)
const homeDir = require('os').homedir()
const clientIo = require('socket.io-client')


const mysql = require('mysql'); 
const { time } = require('console');
const { exit } = require('process');
const { nanoid } = require('nanoid');
const { connect } = require('http2');
var MySql = require('sync-mysql');
const fs = require('fs');
const path = require('path');
var connection = new MySql({
  host: "localhost",
  port: "3306",
  user: "root",
  password: "mysqlpassword5",
  multipleStatements : true
});

  

let con = mysql.createConnection({
  host: "localhost",
  port: "3306",
  user: "root",
  password: "mysqlpassword5",
  multipleStatements : true
});

con.connect()






//server initialization with database connection
//global variables start

let usersLogged = []
let servers = []
let productStocks = {}
const systemOs = "ubuntu"
let purchaseSaving = false
let salesSaving = false
//@change c:// to homDir


let backedUpdata = fs.readFileSync(path.join(homeDir , 'Hosangadi2.0','backend','socket_server','NodeErr.txt'),{encoding:'utf8', flag:'r'});
if (backedUpdata != "{}"){
        backedUpdata = JSON.parse(backedUpdata)
}
fs.writeFileSync(path.join(homeDir , 'Hosangadi2.0','backend','socket_server','NodeErr.txt'),"{}");


let getTime = () => {
    today = new Date()
    h = today.getHours()
    m = today.getMinutes()
    let time = ""
    if(h<10)
        time = "0"+h
    else
        time = h
    if(m<10)
        time+= ":0"+m
    else  
        time =time + ":"+ m
    delete today
    return time
}

function getOldStocks(prodId , dbYear , minYear , stocks , nStocks , max , clientResponse)
{
  
    if(dbYear<minYear)
      {
          clientResponse.send(stocks)
          return 0
      }
    else if(nStocks >= max)
      {
        clientResponse.send(stocks)
        return 0
      }
    else
      {

        sql1 = "SELECT stk_pur_id , stk_prod_qty , stk_cost, stk_sp_nml, stk_sp_htl, stk_sp_spl, stk_sp_ang , acc_name , date_format(pur_date , '%d-%b-%Y') as pur_date   FROM somanath20"+dbYear+".stocks , somanath.accounts , somanath20"+dbYear+".purchases  where stk_prod_id = "+prodId+" and somanath20"+dbYear+".purchases.pur_acc = somanath.accounts.acc_id and somanath20"+dbYear+".stocks.stk_pur_id = somanath20"+dbYear+".purchases.pur_id order by  somanath20"+dbYear+".stocks.insert_time DESC, stk_prod_qty"
        con.query(sql1 , (err1 , res1) =>  {
                for( i = 0 ; i<res1.length  && nStocks < max; i++)
                  {
                      
                      stocks['totQty'] = parseFloat(stocks['totQty'])  + res1[i]['stk_prod_qty']
                      stocks['stocks'].push([ res1[i]['pur_date'] ,  res1[i]['acc_name'] ,  res1[i]['stk_cost'] ,  res1[i]['stk_prod_qty'] ,  res1[i]['stk_sp_nml'],  res1[i]['stk_sp_htl'],  res1[i]['stk_sp_spl'],  res1[i]['stk_sp_ang'], res1[i]['stk_pur_id']] )
                      nStocks += 1
                  }
                
                getOldStocks( prodId, dbYear - 1 , minYear , stocks , nStocks , max , clientResponse)

          })

      }


}

function insertToStocks( stkId ,purId , accId , firmId , dbYear , Time , userName , products , prodId , n , max , clientResponse , sqlStock , editState ,  insertTime , insertId)
{
    if (n >= max)
      {
        clientResponse.sendStatus(200)
        sqlStock = sqlStock.slice(0 , -1)
        con.query(sqlStock , (err , res) => {
            purchaseSaving = false})
        con.commit()
        
        return 0
      }
    else
      {   
          con.query("select distinct(stk_tot_qty) from somanath20"+dbYear+".stocks where stk_prod_id = "+prodId[n] , (errn,resultn) => {

            stk_prod_qty = (parseFloat(products[prodId[n]][3]) - parseFloat(products[prodId[n]][24])).toFixed(3)
            totStk = parseFloat(products[prodId[n]][3]) - parseFloat(products[prodId[n]][24])
            if (resultn.length != 0)
                totStk += parseFloat(resultn[0]['stk_tot_qty'])
            

            totStk = Number(totStk).toFixed(3)

            sqln1 = "update somanath20"+dbYear+".stocks set stk_tot_qty = " + totStk + " where stk_prod_id = "+ prodId[n]
            con.query(sqln1 , (errn1 , resultn1) => {
                      nmlSp = ":" +  products[prodId[n]][6] + ":" +  products[prodId[n]][7] + ":" +  products[prodId[n]][8] + ":" +  products[prodId[n]][9] + ":"
                      htlSp = ":" +  products[prodId[n]][10] + ":" +  products[prodId[n]][11] + ":" +  products[prodId[n]][12] + ":" +  products[prodId[n]][13] + ":"
                      angSp = ":" +  products[prodId[n]][14] + ":" +  products[prodId[n]][15] + ":" +  products[prodId[n]][16] + ":" +  products[prodId[n]][17] + ":"
                      splSp = ":" +  products[prodId[n]][18] + ":" +  products[prodId[n]][19] + ":" +  products[prodId[n]][20] + ":" +  products[prodId[n]][21] + ":"

                      if (editState)
                        sqlStock +="('" + dbYear +"_"+stkId + "' , '"+purId + "'," + prodId[n] + "," + stk_prod_qty + "," +totStk + "," + products[prodId[n]][2] + ",'" + nmlSp + "','" + htlSp + "','" + angSp + "','" + splSp + "'," + products[prodId[n]][22] + "," + accId + "," + firmId + ",'" + insertTime + "',"+ insertId + ",'" + Time+ "',(select user_id from somanath.users where user_name = '"+userName+"')),"
                      else
                        sqlStock +="('" + dbYear +"_"+stkId + "' , '"+purId + "'," + prodId[n] + "," + stk_prod_qty + "," +totStk + "," + products[prodId[n]][2] + ",'" + nmlSp + "','" + htlSp + "','" + angSp + "','" + splSp + "'," + products[prodId[n]][22] + "," + accId + "," + firmId + ",'" + Time+ "',(select user_id from somanath.users where user_name = '"+userName+"'), NULL , NULL),"

                      stkId += 1
                      n+=1
                      if (n<=max)
                        insertToStocks( stkId ,purId , accId , firmId , dbYear , Time , userName , products , prodId , n , max , clientResponse , sqlStock , editState , insertTime , insertId)
 
                           
                      
                })

            
          })
      }
    
}

function purchaseEdit(prodId , balDiff  , stockDiff , prodQty , stocks , clientResponse , n , max, accId,ip ,firmId)
{
    if (n >= max)
      {
        stockDiff.trans = balDiff
        
  
        sql = "SELECT acc_cls_bal_firm"+ firmId +" as acc_cls_bal FROM somanath20"+dbYear+".acc_bal where acc_id ="+accId
        con.query(sql,(err,result)=>{
                acc_cls_bal = result[0].acc_cls_bal - (balDiff[0]-balDiff[1])
                sql = "UPDATE somanath20"+dbYear+".acc_bal SET acc_cls_bal_firm"+ firmId +" = "+acc_cls_bal.toFixed(1) +" where acc_id="+accId
                con.query(sql)
              
            
                  sql2 = "select date_format(insert_time , '%Y-%m-%d %h:%i:%s') as insert_time , insert_id from somanath20"+dbYear+".purchases where pur_id = '"+stocks[0].stk_pur_id+"'"
                  con.query(sql2 , (err1 , result2) => {

                            insertTime = result2[0]['insert_time']
                            insertId = result2[0]['insert_id']

                            sql3 = "DELETE FROM somanath20"+dbYear+".cashflow_purchase where trans_pur ='"+stocks[0].stk_pur_id+"';DELETE FROM somanath20"+dbYear+".stocks where stk_pur_id = '"+stocks[0].stk_pur_id+"';DELETE FROM somanath20"+dbYear+".purchases where pur_id = '"+stocks[0].stk_pur_id+"';"
                            con.query(sql3) 
                          
                            purchaseSaving = false
                            clientResponse.send(stockDiff)
                            delete stockDiff.trans
                            

                            usersLogged.forEach(element => {
                              if(element.ip == ip)
                                      element.purchases.products = stockDiff
                                      element.purchases['insertTime'] = insertTime
                                      element.purchases['insertId'] = insertId
                            });
                            return 0

                })
          })
      }
    else
      {
          con.query("select tax_per from somanath.taxes where tax_id = " + stocks[n].prod_cess , (errn , resultn) =>{


                  spNml = stocks[n].stk_sp_nml.split(":")
                  spNml.pop()
                  spNml.shift()

                  spHtl = stocks[n].stk_sp_htl.split(":")
                  spHtl.pop()
                  spHtl.shift()

                  spSpl = stocks[n].stk_sp_spl.split(":")
                  spSpl.pop()
                  spSpl.shift()

                  spAng = stocks[n].stk_sp_ang.split(":")
                  spAng.pop()
                  spAng.shift()

                  prodStock = stocks[n]

                  cost = parseFloat(prodStock.stk_cost)
                  qty  = parseFloat(prodQty[n])
                  cess = parseFloat(resultn[0]['tax_per'])
                  gst = prodStock.gst

                  totCost = (cost * qty).toFixed(3)
                  totTaxable =( ( cost / (1+(cess+gst)/100)) * qty ).toFixed(3) 

                  
                  stockDiff[prodId[n]] = [ prodStock.prod_name , gst , cost.toFixed(3) ,  qty.toFixed(3) , totTaxable , totCost ,  spNml[0] , spNml[0] , spNml[0] , spNml[0] , spHtl[0] , spHtl[0] , spHtl[0] , spHtl[0] , spSpl[0] , spSpl[0] , spSpl[0] , spSpl[0] , spAng[0] , spAng[0] , spAng[0] , spAng[0] , prodStock.stk_exp , cess   ,stockDiff[prodId[n]][0]]

                  sqln1 = "UPDATE somanath20"+dbYear+".stocks SET stk_tot_qty ="+ (parseFloat(stocks[n].stk_tot_qty)-parseFloat(stocks[n].stk_prod_qty)).toFixed(3) +" where stk_prod_id ="+prodId[n]
                  con.query(sqln1)
                  
                  n+=1
                  if (n<=max)
                    purchaseEdit(prodId , balDiff  , stockDiff , prodQty , stocks , clientResponse , n , max,accId,ip , firmId)
              })
          


          
      }
}

function getSalesStocks(stocks , n , max , clientResponse)
{

    if (n>=max)
      {
          clientResponse.send(stocks)
      }
    else  
      {
        
        dbYear = stocks[n]['stk_pur_id'].split("_")[0]

          sql1 = "select firm_suffix from somanath.firms where firm_id = " + stocks[n]['stk_firm_id']
          con.query(sql1 , (err1 , result1) =>{
                    stocks[n]['firm_suffix'] = result1[0]['firm_suffix']

                    sql2 = "select acc_name from somanath.accounts where acc_id = " + stocks[n]['stk_sup_id']
                    con.query(sql2, (err2 , result2) =>{

                            
                              stocks[n]['acc_name'] = result2[0]['acc_name']

                              sql3 = "select date_format(pur_date , '%d-%m-%Y') as pur_date from somanath20"+dbYear+".purchases where pur_id = '" + stocks[n]['stk_pur_id'] +"'"
                              con.query(sql3 , (err3 , result3) =>{
                                              if(result3.length>0){
                                                stocks[n]['pur_date'] = result3[0]['pur_date']
                                                
                                              }
                                              n+=1
                                                getSalesStocks(stocks , n , max , clientResponse)
                                              
                                                                                                  
                                    })

                        })

              })

      }
}


function checkStockAvailable  (products , dbYear){
    
  available = {}
  nonAvailable = {}
  withStkId = {}
  sql1 = "select distinct(stk_prod_id), stk_tot_qty from somanath20"+dbYear+".stocks where stk_prod_id in ("
  sqlCheck = sql1
  Object.keys(products).forEach(element =>{ 
              Object.keys(products[element]).forEach(stk =>{

                      if (stk == 'stkId')
                          sql1 += element + ","
                      else 
                        { 
                          if(! withStkId.hasOwnProperty(element))
                              withStkId[element] = {}
                          withStkId[element][stk] = products[element][stk]
                        }

              })
                 
    })


    if (sql1 != sqlCheck)
      {
          sql1 = sql1.slice(0 , -1)
          sql1 += ')'

          result = connection.query(sql1);

          result.forEach(stk =>{

                  if (products[stk.stk_prod_id].stkId[1] <= stk.stk_tot_qty )
                    {
                        available[stk.stk_prod_id] = {}
                        if(products[stk.stk_prod_id].stkId.length == 11)
                          products[stk.stk_prod_id].stkId.push(stk.stk_tot_qty)
                        available[stk.stk_prod_id].stkId = products[stk.stk_prod_id].stkId
                    }
                  else
                    {
                        nonAvailable[stk.stk_prod_id] = {}
                        products[stk.stk_prod_id].stkId.push(stk.stk_tot_qty)
                        nonAvailable[stk.stk_prod_id].stkId = products[stk.stk_prod_id].stkId
                        
                    }

            })

         
      }
    

    Object.keys(withStkId).forEach(element =>{
         
          Object.keys(withStkId[element]).forEach(stk =>{


                    sql2 = "select stk_prod_qty,stk_tot_qty,stk_pur_id,stk_firm_id,stk_cost from somanath20"+dbYear+".stocks where stk_id = '" + stk + "'"
                    result2 = connection.query(sql2);
                    
                    if (withStkId[element][stk][1] <= result2[0]['stk_prod_qty'])
                      {
                          if(! available.hasOwnProperty(element))
                              available[element] = {}
                          if(withStkId[element][stk].length == 11)
                          {
                            withStkId[element][stk].push(result2[0]['stk_prod_qty'])
                            withStkId[element][stk].push(result2[0]['stk_tot_qty'])
                            withStkId[element][stk].push(result2[0]['stk_pur_id'])
                            withStkId[element][stk].push(result2[0]['stk_firm_id'])
                            withStkId[element][stk].push(result2[0]['stk_cost'])
                          }
                          
                          available[element][stk] = withStkId[element][stk]
                      }
                    else
                      {
                        if(! nonAvailable.hasOwnProperty(element))
                          nonAvailable[element] = {}
                        withStkId[element][stk].push(result2[0]['stk_prod_qty'])
                        nonAvailable[element][stk] = withStkId[element][stk] 
                        

                      }
                })
        })

    return [available , nonAvailable]

}

//global variables end
io.on('connection', function (socket) {
    //connection event starts 
    //adds data to usersLogged when login is approved
    
    clientIp = socket.handshake.address

    
    //all the params passed pushed to usersLogged
    socketData = socket.handshake.headers

    if ( socketData['user-agent'] ==  "node-XMLHttpRequest" )
        servers.push({"id" : socket.id })
    else
      {
        
        newUser = {"id" : socket.id , "ip" : clientIp , "userName" : socketData['user_name'] , "userType": socketData['user_type'] , "loggedInAt":getTime() , "purchases" : {} , "sales" : {}}
        if (backedUpdata != "{}")
        {
          backedupuser = backedUpdata[clientIp]
          newUser.sales = backedupuser.sales
          newUser.purchases = backedupuser.purchases
          delete backedUpdata[clientIp]
          if (backedUpdata.length == 0)
              backedUpdata = "{}"
        }

        usersLogged.push(newUser)
        
      }
    
    

    //connection event ends 

    //root window disconnect event
          socket.on('disconnect' , (data)=> {
                  socketData = socket.handshake.headers
                  for (user = 0 ; user<usersLogged.length ; user ++)
                      {   
                          if(usersLogged[user].ip == socket.handshake.address)
                            usersLogged.splice(user , 1)
                      }
                    
          });   
  

    //server refreshes
          socket.on('refresh' , ()=> {
                socket.broadcast.emit("refreshProductServer")
          })



    //
          socket.on('purchaseError' , () => {
          }) 

          socket.on('sendError' , (data) =>{
              socket.broadcast.emit('error' , data)
          })




})






app.get('/login' , (req,res) => {                                                                                                          //for user login authentication
  sql = "select user_type from somanath.users where user_name = '"+ req.query.user_name + "' and user_pass = '"+req.query.user_pass+"'"
  responseSent = false
  

  usersLogged.forEach( user => {
    if(user.ip == req.socket.remoteAddress)
       {
          responseSent = true
          res.sendStatus(101)
       }
    if(!responseSent && user.userName == req.query.user_name)
       {
          responseSent = true
          res.sendStatus(102)
       }
          
    });                                                                                                                                     //checks if same two clients are from same ip or from same user name
                                                                                                                                           //responds {"NOT FOUND"}
  if(!responseSent)
        con.query(sql, (err , userType)=>{
          res.send(userType)
        });  

    
                                                                                                                                       //returns null when not found else returns {""}
});

//purchase entry routes
app.get('/purchases/addEditPurDetails' , (req , res) => {

  ip = req.socket.remoteAddress
  purDetails = req.query
  
  
  sql = "select pur_id from somanath20" + purDetails.year + ".purchases where pur_acc = (select acc_id from somanath.accounts where acc_name = '"+ purDetails.sup_name +"') and pur_inv = '" + purDetails.inv_no + "'"
  
  con.query(sql , (err , result) =>{

      found = false
      found_ip = ""
      
      if (result.length != 0)
          res.sendStatus(202)
      
      else
        {    
            usersLogged.forEach(element => {

                        if (element.purchases.supName == purDetails.sup_name && element.purchases.invNo ==  purDetails.inv_no)
                        {
                           found = true
                           found_ip = element.ip
                        }
            });

      
            if (found && found_ip != ip)
            {
                res.sendStatus(201) 
            }
            else
              {

                 
                  usersLogged.forEach(element => {
                    
                      if(element.ip == ip)
                          {   
                              
                              element.purchases.purDate = purDetails.date
                              element.purchases.invNo =  purDetails.inv_no
                              element.purchases.taxMethod =  purDetails.tax_method
                              element.purchases.firmName = purDetails.firm_name 
                              element.purchases.supName = purDetails.sup_name
                             
                              if (purDetails.editState == 'False') 
                                {
                                  element.purchases.purId = "new"
                                   
                                  if (purDetails.productsAdded == 'False')  
                                    element.purchases.products = {}
                                  
                                }
                             
                          }
                        
                  });
                  
                  res.sendStatus(200)
              }
        }
  })

})

app.get('/purchases/cancelPurchase' , (req , res) => {

    ip = req.socket.remoteAddress

    usersLogged.forEach(element => {

          if (element.ip == ip )
          {
            element.purchases = {}
          }
    });
    res.sendStatus(200)


})

app.get('/getOldStocks' ,  (req , res )=>{

  dbYear = parseInt(req.query['year'])
  prodId = req.query['prod_id']
  max =  parseInt(req.query['max'])
  stocks = {}

  nStocks = 0
  totalQty = 0
  n = 1
  con.query("select prod_mrp , prod_mrp_old ,  date_format(insert_time, ('%y')) as minDate from somanath.products where prod_id = " + prodId , (err , result) =>{

    stocks['prodMrp1'] = result[0]['prod_mrp']
    stocks['prodMrp2'] = result[0]['prod_mrp_old']
    stocks['totQty'] = 0
    stocks['stocks'] = []
    minYear = result[0]['minDate']

    sql2 = "SELECT count(stk_prod_id) as max FROM somanath20"+dbYear+".stocks where stk_prod_qty >0 and stk_prod_id = " + prodId
    con.query(sql2 , (err2 , result2) =>{

            newMax = result2[0].max
         

            if(newMax > max)
                max = newMax
                
            if(dbYear >= minYear)
            {
                
              n =  getOldStocks(prodId , dbYear , minYear , stocks , nStocks , max , res);
            }
          if(n)
              res.send(stocks)

    })


    
    
  })
  
})

app.get('/purchases/addPurchaseProduct' , (req , res) =>{
  ip = req.socket.remoteAddress
  productData = req.query.value
  usersLogged.forEach(element => {

        if (element.ip == ip ) 
        {
          prodId = String(productData[24])
          
          newArray = productData.slice(1,24)
          newArray.push(productData[25])
          newArray.push(productData[26])
          
          element.purchases.products[prodId] = newArray
        }
  });
  res.sendStatus(200)

 
})

app.get('/purchases/removePurchaseProduct' , (req , res) =>{
  ip = req.socket.remoteAddress
  prodId = req.query.prod_id

  
  usersLogged.forEach(element => {

        if (element.ip == ip )
        {
          
          delete element.purchases.products[prodId]
         
        }
  });
  res.sendStatus(200)
})

app.get('/purchases/save'  , (req , res) =>{

    if (purchaseSaving)
      {
        res.sendStatus(201)
      }
    else
      {
        purchaseSaving = true
        ip = req.socket.remoteAddress
        editState = false
        if (req.query.edit_state == 'True')
            editState = true


        dbYear = req.query.db_year
        purInv = req.query.pur_inv
        purExp = req.query.pur_exp
        amtPaid = req.query.amt_paid 
        purBal = req.query.pur_bal
        
        grandTotal = req.query.grand_total
        payMeth = req.query.pay_meth
        if (payMeth == 'UPI/NEFT')
          payMeth = 'BANK'
        userName = req.query.user_name

        Time = new Date
        Time = Time.getFullYear()+"-"+String(Time.getMonth()+1).padStart(2 , '0')+"-"+String(Time.getDate()).padStart(2 , '0')+" "+String(Time.getHours()).padStart(2 , '0')+":"+String(Time.getMinutes()).padStart(2 , '0')+":"+String(Time.getSeconds()).padStart(2 , '0')


        usersLogged.forEach((element)=>{
            if (element.ip == ip)
            {
               purDetails = element.purchases  
               element.purchases = {}
            }
        })
        
        sql = "select firm_id from somanath.firms where firm_name = '"+purDetails.firmName+"'"
        con.query(sql , (err , result) =>{
                  firmId = result[0]['firm_id']
                  sql1 = "select acc_id from somanath.accounts where acc_name = '"+purDetails.supName+"'"
                  con.query(sql1 , (err1 , result1)=>{

                            accId = result1[0]['acc_id']
                            sql2 = "select purchases , cashflow_purchase as cashflow , stocks , acc_cls_bal_firm"+firmId+" as acc_cls_bal from somanath20"+dbYear+".max_id , somanath20"+dbYear+".acc_bal where acc_bal.acc_id = " + accId
                            con.query(sql2 , (err2 , result2) => {

                                      maxPurId = parseInt(result2[0]['purchases'])+1
                                    //correct +1


                                      //@shiva
                                      if(editState){
                                        x = req.query.pur_id.split("_")
                                        maxPurId = x.pop()
                                      }
                                      
                                      maxCashID = parseInt(result2[0]['cashflow'])+1
                                      maxStockId = parseInt(result2[0]['stocks'])+1
                                      accBal = parseFloat(result2[0]['acc_cls_bal'])
                                      accBal += parseFloat(purBal)

                                      prodId = ":"
                                      prodQty = ":"
                                      
                                      sqlProdHideUpdate = " update somanath.products set prod_hide = 'False' where prod_id in (" 

                                      Object.keys(purDetails.products).forEach(element =>{ 
                                        sqlProdHideUpdate += element + "," 
                                        prodId += element +":"
                                        prodQty += purDetails.products[element][3] + ":" 
                                      })
                                      
                                      sqlProdHideUpdate = sqlProdHideUpdate.slice(0 , -1) + ")"
                                      

                                      purDate = purDetails.purDate.split("-")
                                      purDate = purDate[2] + "-" + purDate[1] + "-" + purDate[0]
                                      
                                      if (editState)
                                        {
                                            sql3 = "insert into somanath20"+dbYear+".purchases values ('" + dbYear+"_"+ maxPurId + "'," + accId + "," + firmId + ",'" + purInv + "','" + prodId + "','" + prodQty + "'," + purExp +" , '" + purDate + "','"+  purDetails.taxMethod.split("-")[0].toUpperCase() + "','"+ purDetails.insertTime + "',"+ purDetails.insertId + ",'" + Time +"',(select user_id from somanath.users where user_name = '"+userName+"'));" 
                                            sql4 = "update somanath20"+dbYear+".acc_bal set acc_cls_bal_firm"+ firmId +" = "+accBal+" where acc_id = " + accId + ";"
                                            sql5 = "insert into somanath20"+dbYear+".cashflow_purchase values ('"+ dbYear + "_" + maxCashID + "'," + accId + ","+firmId+",'"+dbYear+"_"+ maxPurId + "' , " + grandTotal + "," + amtPaid + ", '" + payMeth + "','" + purDate + "','"+ purDetails.insertTime + "',"+ purDetails.insertId + ",'" + Time +"',(select user_id from somanath.users where user_name = '"+userName+"'));" 

                                        }
                                      else
                                        {
                                            sql3 = "insert into somanath20"+dbYear+".purchases values ('" + dbYear+"_"+ maxPurId + "'," + accId + "," + firmId + ",'" + purInv + "','" + prodId + "','" + prodQty + "'," + purExp +" , '" + purDate + "','"+  purDetails.taxMethod.split("-")[0].toUpperCase() + "','"+ Time +"',(select user_id from somanath.users where user_name = '"+userName+"')"+" , NULL , NULL);" 
                                            sql4 = "update somanath20"+dbYear+".acc_bal set acc_cls_bal_firm"+ firmId +" = "+accBal+" where acc_id = " + accId + ";"
                                            sql5 = "insert into somanath20"+dbYear+".cashflow_purchase values ('"+ dbYear + "_" + maxCashID + "'," + accId +","+firmId+ ",'"+dbYear+"_"+ maxPurId + "' , " + grandTotal + "," + amtPaid + " , '" + payMeth + "','" + purDate + "','"+ Time +"',(select user_id from somanath.users where user_name = '"+userName+"')"+" , NULL , NULL);" 
                                        }

                                      maxStkId = Number(maxStockId) + Number(Object.keys(purDetails.products).length) -1

                                      sql6 = "update somanath20" + dbYear + ".max_id set purchases = " + maxPurId + " , cashflow_purchase = " + maxCashID + " , stocks = " + maxStkId + ";"
                                      
                                      sqlStock =  "insert into somanath20"+dbYear+".stocks values "
                                      con.query(sql3 + sql4 + sql5 + sql6 + sqlProdHideUpdate , (err3, result3) =>{
                                        insertToStocks(maxStockId , dbYear+"_"+ maxPurId , accId , firmId , dbYear , Time , userName, purDetails.products , Object.keys(purDetails.products) , 0 , Object.keys(purDetails.products).length , res , sqlStock , editState , purDetails.insertTime , purDetails.insertId) 
                                      })
                                      
                                })

                      })

            })

      }

})

app.get('/purchases/edit' , (req , res) =>{

      if (purchaseSaving)
        {
            res.sendStatus(201)
        }
      else
        {
              purDetails = req.query
              
              accId = purDetails['pur_acc']
              purId = purDetails['pur_id']
              dbYear = parseInt(purDetails['pur_id'].split("_")[0])
              ip = req.socket.remoteAddress
              //con.query("SELECT acc_cls_bal FROM somanath20"+dbYear+".acc_bal where acc_id = "+accId , (err1 , result1) =>{
                            

                            sql2 = "SELECT * from somanath20"+dbYear+".cashflow_purchase where trans_pur = '" + purId + "'"
                            con.query(sql2 , (err2 , result2) =>{
                                        
                                        firmId = result2[0]['trans_firm_id']

                                        balDiff = [parseFloat(result2[0]['trans_amt']).toFixed(2) , parseFloat(result2[0]['amt_paid']).toFixed(2) , result2[0]['trans_mode']]

                                        sql3 = "SELECT stk_id, stk_pur_id, stk_prod_id, stk_prod_qty, stk_tot_qty, stk_cost, stk_sp_nml, stk_sp_htl, stk_sp_spl, stk_sp_ang, stk_exp, stk_sup_id, stk_firm_id , prod_name , prod_cess , tax_per as gst   from somanath20"+dbYear+".stocks , somanath.products , somanath.taxes where stk_pur_id = '"+purId+"' and stk_prod_id = prod_id and prod_gst = tax_id  order by stk_prod_id"
                                        con.query(sql3 , (err3 , result3) => {
                                              prodId = purDetails['pur_prod_id'].split(':')
                                              prodId.shift()
                                              prodId.pop()
                                              prodQty = purDetails['pur_prod_qty'].split(':')
                                              prodQty.shift()
                                              prodQty.pop()
                                              stockDiff ={} 
                                              for(i = 0; i< prodId.length ; i++ ){
                                                stockDiff[prodId[i]] = prodQty[i]
                                              }
                                              let j = 0

                                              Object.keys(stockDiff).forEach( prodId => {
                                                stockDiff[prodId] = [ (parseFloat(stockDiff[prodId]) - parseFloat(result3[j].stk_prod_qty)).toFixed(3)]
                                                j++
                                              });
                                              
                                              

                                              usersLogged.forEach(element => {
                                                if(element.ip == ip)
                                                    {
                                                        element.purchases.purId =  purId
                                                        element.purchases.purDate = purDetails.pur_date
                                                        element.purchases.invNo =  purDetails.pur_inv

                                                        if (purDetails.tax_method == "OUT")
                                                            taxMethod = "Out-Of-State"
                                                        else  
                                                            taxMethod = "In-State"

                                                        element.purchases.taxMethod =  taxMethod
                                                        element.purchases.firmName = purDetails.pur_firm_name
                                                        element.purchases.supName = purDetails.pur_acc_name   
                                                        element.purchases.products = {}
                                                    }
                                                     
                                                  
                                              });

                                              
                                              purchaseEdit( Object.keys(stockDiff) , balDiff , stockDiff , prodQty , result3 , res , 0 , Object.keys(stockDiff).length, accId , ip , firmId)


                                              //res.sendStatus(200)
                                        })

                                })

              // })
              
        }

})

//purchase entry routes done


//sales enrty route

app.get('/sales/addEditNewSalesDetails' , (req , res) =>{
 
  ip = req.socket.remoteAddress
  salesDetails = req.query
  usersLogged.forEach(element => {
    if(element.ip == ip)
        {
          saleId = salesDetails.sale_id 
          if (saleId == '')
            saleId = String(nanoid())
          newSaleObject = {
                'saleDate' : salesDetails.sale_date , 
                'custName' : salesDetails.cust_name , 
                'products' : {}
          }

          element.sales[saleId] = newSaleObject

    }
})

res.send({'saleId' : saleId})




})

app.get('/sales/getSalesStocks' , (req , res) =>{

  prodId = req.query.prod_id
  dbYear = req.query.year
  spType = req.query.spType



  sql = "SELECT stk_id,stk_prod_qty,stk_tot_qty,stk_cost,stk_pur_id , stk_firm_id , stk_sup_id, stk_sp_"+spType+",prod_name , prod_mrp , prod_mrp_old  , prod_unit_type , "+spType+"_unit , prod_gst , prod_cess FROM somanath20"+dbYear+".stocks , somanath.products where stk_prod_id = "+prodId+"  and stk_prod_qty > 0 and somanath.products.prod_id = somanath20"+dbYear+".stocks.stk_prod_id  order  by somanath20"+dbYear+".stocks.insert_time ;"

  con.query(sql , (err , result) => {
      getSalesStocks(result , 0 , result.length , res)
  })



})

app.get('/sales/addSalesProduct' , (req , res) =>{
  ip = req.socket.remoteAddress
  saleId = req.query.sale_id
  productData = req.query.product
  usersLogged.forEach(element => {

        if (element.ip == ip ) 
        {
            prodId = productData[13]
            stkId = productData[12]
            

            //adding to globalstocks
            if (stkId != "")
            {
                  if(productStocks.hasOwnProperty(prodId))
                      {
                          if(productStocks[prodId].hasOwnProperty(stkId))
                              {
                                stk = (parseFloat(productStocks[prodId][stkId]) + parseFloat(productData[2])).toFixed(3)
                                productStocks[prodId][stkId] = stk
                              }
                          else
                              {   

                                  productStocks[prodId][stkId] = productData[2]
                              }
                          
                      }
                  else
                      {
                          productStocks[prodId] = {}
                          productStocks[prodId][stkId] = productData[2]
                          
                      }
            }
            
            
            newArray = productData.slice(1,12)
            
            if (stkId != '')
            {
              
                if(element.sales[saleId].products.hasOwnProperty(prodId))
                {
                    element.sales[saleId].products[prodId][stkId] = newArray
                }
                else
                {
                    element.sales[saleId].products[prodId] = {}
                    element.sales[saleId].products[prodId][stkId] = newArray
                }
          
            }
            else
            {
              element.sales[saleId].products[prodId] = {}
              element.sales[saleId].products[prodId]['stkId'] = newArray
            }
            
        }
  });
  res.sendStatus(200)
  
})

app.get('/sales/removeSalesProduct' , (req , res) =>{
  
          ip = req.socket.remoteAddress
          saleId = req.query.sale_id
          dbYear = req.query.db_year
          newProduct = req.query.newBill
          prodId = req.query.product[13]
          stkId = req.query.product[12] 
          if(stkId === '')
            {
              stkId = 'stkId'
            }

          usersLogged.forEach(element => {

                if (element.ip == ip ) 
                {
                    delete element.sales[saleId].products[prodId][stkId]
                    if(Object.keys(element.sales[saleId].products[prodId]).length === 0)
                          delete element.sales[saleId].products[prodId]

                    if (newProduct == 'True')
                    {
                      if (stkId != 'stkId' && Object.keys(productStocks).length > 0 )
                      {

                        if(productStocks[prodId].hasOwnProperty(stkId))
                          {
                            stk = (parseFloat(productStocks[prodId][stkId]) - parseFloat(req.query.product[2])).toFixed(3)
                            productStocks[prodId][stkId] = stk
                            if(stk === '0.000')
                                {
                                    delete productStocks[prodId][stkId]
                                    if (Object.keys(productStocks[prodId]).length ===0)
                                      delete productStocks[prodId]
                                                                          
                                }
                          } 
                  
                      }
                    }
                    else
                      { 
                          qty = req.query.product[2]
                          sql = "update somanath20"+dbYear+".stocks set stk_prod_qty = stk_prod_qty +" + qty + " where stk_id = '"+stkId+"';"
                          sql += "update somanath20"+dbYear+".stocks set stk_tot_qty = stk_tot_qty +" + qty + " where stk_prod_id = '"+prodId+"'"
                          con.query(sql)
                      }
                  

                    
                }
          })

          res.sendStatus(200)
})

app.get('/getGlobalStocks' , (req , res) =>{

  if (productStocks.hasOwnProperty(req.query.prod_id))
      res.send(productStocks[req.query.prod_id])
  else
      res.send({})

})

app.get('/sales/cancelSales' , (req , res) => {

  ip = req.socket.remoteAddress
  saleId = req.query.sale_id
  usersLogged.forEach(element => {

        if (element.ip == ip )
        { 
              delete element.sales[saleId]
    
        }
        


  });
  res.sendStatus(200)


})

app.get('/sales/save' , (req , res) =>{

      if(salesSaving)
            res.sendStatus(201)
      else
      {
            salesSaving = true 
            saleId = req.query.sale_id
            dbYear = req.query.year
            accId = req.query.cust_id
            userName = req.query.user_name
            saleDate1 = req.query.sale_date

            ip = req.socket.remoteAddress

            usersLogged.forEach((element)=>{
              if (element.ip == ip)
              {
                 salesDetails = element.sales[saleId]  
              }
          })
          toCheckStockAvailable = salesDetails.products
          editDirectSave = {}
          if(saleId.length<15)
          {
            insertTime = salesDetails.insert_time
            insertId = salesDetails.insert_id
            salesIds = salesDetails.sales_ids
            toCheckStockAvailable = {}
          } 
          
          prodIdBackend = Object.keys(salesDetails.products)
          for(i = 0; i < prodIdBackend.length ; i++ )
          {
            stkIdBackend =  Object.keys(salesDetails.products[prodIdBackend[i]]);
            for(j = 0; j< stkIdBackend.length ; j++ ){
              if(salesDetails.products[prodIdBackend[i]][stkIdBackend[j]][0] === 'E' )
              {
                if(prodIdBackend[i] in editDirectSave )
                {
                  editDirectSave[prodIdBackend[i]][stkIdBackend[j]] = salesDetails.products[prodIdBackend[i]][stkIdBackend[j]]
                }
                else
                {
                  editDirectSave[prodIdBackend[i]] = {}
                  editDirectSave[prodIdBackend[i]][stkIdBackend[j]] = salesDetails.products[prodIdBackend[i]][stkIdBackend[j]]
                }
              }
              else
              {
                if(prodIdBackend[i] in toCheckStockAvailable ){
                  toCheckStockAvailable[prodIdBackend[i]][stkIdBackend[j]] = salesDetails.products[prodIdBackend[i]][stkIdBackend[j]]
                }else{
                  toCheckStockAvailable[prodIdBackend[i]] = {}
                  toCheckStockAvailable[prodIdBackend[i]][stkIdBackend[j]] = salesDetails.products[prodIdBackend[i]][stkIdBackend[j]]
                }
              }
            }
          } 
          

          availList = checkStockAvailable(  toCheckStockAvailable ,  dbYear)
          
          
          available = availList[0]
          nonAvailable = availList[1] 

          salesSaveData = {
                           '1' : {'sales_prod_id' : ':', 'sales_pur_id' : ':', 'sales_prod_qty' : ':', 'sales_prod_sp' : ':', 'cost_price' : ':', 'units' : '::', 'sp_list' : '::', 'gst_value' : ':', 'cess_value' : ':', 'sales_profit' : 0, 'prod_name' : ':','firm_total' : 0},
                           '2' : {'sales_prod_id' : ':', 'sales_pur_id' : ':', 'sales_prod_qty' : ':', 'sales_prod_sp' : ':', 'cost_price' : ':', 'units' : '::', 'sp_list' : '::', 'gst_value' : ':', 'cess_value' : ':', 'sales_profit' : 0, 'prod_name' : ':','firm_total' : 0},
                           '3' : {'sales_prod_id' : ':', 'sales_pur_id' : ':', 'sales_prod_qty' : ':', 'sales_prod_sp' : ':', 'cost_price' : ':', 'units' : '::', 'sp_list' : '::', 'gst_value' : ':', 'cess_value' : ':', 'sales_profit' : 0, 'prod_name' : ':','firm_total' : 0}
                          }

                        

          if((Object.keys(nonAvailable).length > 0))
              {      
                    salesSaving = false
                    res.status(320).send(nonAvailable)

              } 
          else
              {     
                SqlFinal = ''
                Object.keys(available).forEach(element => 
                {
                    stkId = Object.keys(available[element])
                    if( stkId[0] == 'stkId')
                    {
                          result = connection.query("select stk_id , stk_prod_qty , stk_pur_id, stk_firm_id, stk_cost from somanath20" + dbYear + ".stocks where stk_prod_id = " + element + " and stk_prod_qty > 0 order by insert_time")

                          reducedQty = available[element]['stkId'][1]
                          for ( i = 0 ; i<result.length ; i++)
                                { 
                                      units = ''
                                      available[element]['stkId'][5].slice(2,-2).split("', '").forEach(element => {
                                        units +=  parseFloat(element).toFixed(3) + ':'
                                      });
                                      spList = ''
                                      available[element]['stkId'][6].slice(2,-2).split("', '").forEach(element => {
                                        spList +=  parseFloat(element).toFixed(3) + ':'
                                      });

                                      if( i == 0 )
                                          {
                                                sql = "update somanath20" + dbYear + ".stocks set stk_tot_qty = " + (available[element]['stkId'][11] - reducedQty).toFixed(3) + " where stk_prod_id = " + element +';'
                                                SqlFinal +=  sql
                                          }
                                          temp = salesSaveData[result[i]['stk_firm_id']]
                                          temp.sales_prod_id += element +':'
                                          temp.prod_name += available[element]['stkId'][0]+':'
                                          temp.sales_pur_id += result[i]['stk_pur_id'] +':'
                                          temp.sales_prod_sp += available[element]['stkId'][2] +':'
                                          temp.cost_price += result[i]['stk_cost'] +':'
                                          temp.units += units +':'
                                          temp.sp_list += spList +':'
                                          temp.gst_value += available[element]['stkId'][9]+':'
                                          temp.cess_value += available[element]['stkId'][10]+':'
                                          

                                      if(reducedQty <= result[i]['stk_prod_qty'])
                                          {
                                                sql1 = "update somanath20" + dbYear + ".stocks set stk_prod_qty = " + (result[i]['stk_prod_qty'] - reducedQty).toFixed(3) + " where stk_id = '" +  result[i]['stk_id'] + "';"
                                                SqlFinal += sql1
                                                temp.sales_prod_qty += reducedQty +':'
                                                temp.firm_total += (parseFloat(available[element]['stkId'][2])*parseFloat(reducedQty))
                                                temp.sales_profit =  ( parseFloat(temp.sales_profit) + ( ( parseFloat(available[element]['stkId'][2]) - parseFloat(result[i]['stk_cost']) ) * parseFloat(reducedQty) ) ).toFixed(2)
                                                break;
                                          }
                                      else
                                          {
                                                sql1 = "update somanath20" + dbYear + ".stocks set stk_prod_qty = 0 where stk_id = '" +  result[i]['stk_id'] + "';"
                                                reducedQty -= result[i]['stk_prod_qty']
                                                SqlFinal += sql1
                                                temp.sales_prod_qty += result[i]['stk_prod_qty'] +':'
                                                temp.firm_total += (parseFloat(available[element]['stkId'][2])*parseFloat(result[i]['stk_prod_qty']))
                                                temp.sales_profit =  ( parseFloat(temp.sales_profit) + ( ( parseFloat(available[element]['stkId'][2]) - parseFloat(result[i]['stk_cost']) ) * parseFloat(result[i]['stk_prod_qty']) ) ).toFixed(2)
                                                
                                                
                                          }
                                      

                                }

                    }
                    else
                    {      
                        totStkInput = 0
                        stkIdprod = 0 
                        
                        stkId.forEach(item => 
                          {
                            temp1 = available[element][item]
                            stkIdprod = item
                            totStkInput += parseFloat(temp1[1])
                            stkQty = temp1[11] - parseFloat(temp1[1])
                            units = ''
                            temp1[5].slice(2,-2).split("', '").forEach(element => {
                              units +=  parseFloat(element).toFixed(3) + ':'
                            });
                            spList = ''
                            temp1[6].slice(2,-2).split("', '").forEach(element => {
                              spList +=  parseFloat(element).toFixed(3) + ':'
                            });
                            temp = salesSaveData[temp1[14]]
                            temp.prod_name += temp1[0]+':'
                            temp.sales_prod_id += element +':'
                            temp.sales_pur_id += temp1[13] +':'
                            temp.sales_prod_sp += temp1[2] +':'
                            temp.cost_price += temp1[15] +':'
                            temp.units += units +':'
                            temp.sp_list += spList +':'
                            temp.sales_prod_qty += temp1[1] +':'
                            temp.gst_value += temp1[9]+':'
                            temp.cess_value += temp1[10]+':'
                            temp.firm_total += (parseFloat(temp1[2])*parseFloat(temp1[1]))
                            temp.sales_profit =  ( parseFloat(temp.sales_profit) + ( ( parseFloat(temp1[2]) - parseFloat(temp1[15]) ) * parseFloat( temp1[1]) ) ).toFixed(2)
                            sql2   = "update somanath20"+dbYear+".stocks set stk_prod_qty = " + Number(stkQty).toFixed(3) + " where stk_id = '" + item + "';" 
                            
                            SqlFinal += sql2
                        });

                        stkTotQty = available[element][stkIdprod][12] - totStkInput
                        sqltot = "update somanath20" + dbYear + ".stocks set stk_tot_qty = " + Number(stkTotQty).toFixed(3) + " where stk_prod_id = " + element + ";" 
                        SqlFinal += sqltot
                    }
                });

                if(Object.keys(editDirectSave).length>0)
                {
                  
                  Object.keys(editDirectSave).forEach(element=>{
                    
                    stkIdprod = 0 
                    stkId = Object.keys(editDirectSave[element])
                    stkId.forEach(item => 
                      {
                        temp1 = editDirectSave[element][item].slice(1,)
                        stkIdprod = item
                        stkQty = temp1[11] - parseFloat(temp1[1])
                        units = ''
                        temp1[5].slice(2,-2).split("','").forEach(element => {
                          units +=  parseFloat(element).toFixed(3) + ':'
                        });
                        spList = ''
                        temp1[6].slice(2,-2).split("','").forEach(element => {
                          spList +=  parseFloat(element).toFixed(3) + ':'
                        });
                        temp = salesSaveData[temp1[14]]
                        temp.prod_name += temp1[0]+':'
                        temp.sales_prod_id += element +':'
                        temp.sales_pur_id += temp1[13] +':'
                        temp.sales_prod_sp += temp1[2] +':'
                        temp.cost_price += temp1[15] +':'
                        temp.units += units +':'
                        temp.sp_list += spList +':'
                        temp.sales_prod_qty += temp1[1] +':' 
                        temp.gst_value += temp1[9]+':'
                        temp.cess_value += temp1[10]+':'
                        temp.firm_total += (parseFloat(temp1[2])*parseFloat(temp1[1]))
                        temp.sales_profit =  ( parseFloat(temp.sales_profit) + ( ( parseFloat(temp1[2]) - parseFloat(temp1[15]) ) * parseFloat( temp1[1]) ) ).toFixed(2)
                      
                    });

                    

                  });
                
                }

                if(saleId.length < 15)
                {//editSave
                Time = new Date
                Time = Time.getFullYear()+"-"+String(Time.getMonth()+1).padStart(2 , '0')+"-"+String(Time.getDate()).padStart(2 , '0')+" "+String(Time.getHours()).padStart(2 , '0')+":"+String(Time.getMinutes()).padStart(2 , '0')+":"+String(Time.getSeconds()).padStart(2 , '0')
                
                sql3 = "insert into somanath20" + dbYear + ".sales values "
                sql4 = "insert into somanath20" + dbYear + ".sales_sp values "

                saleDate = saleDate1.split("-")

                saleDate = saleDate[2] + "-" + saleDate[1] + "-" + saleDate[0]
                
                if (salesSaveData['1'].sales_prod_id != ":")
                  {
                    
                    temp = salesSaveData['1']
                    sql3 += "('"+  salesIds[0] + "' , '" + salesIds[1] +"' , " + accId + ",'" + temp.sales_prod_id +"','"  + temp.sales_pur_id +"','" + temp.sales_prod_qty +"','" + temp.sales_prod_sp +"','" + saleDate + "',0,'" + insertTime + "',"+insertId +",'"+ Time + "',(select user_id from somanath.users where user_name = '" + userName +"')),"
                    sql4 += "('"+  salesIds[0] + "' , '" + salesIds[1] +"' , '" + temp.sales_prod_id +"','"  + temp.cost_price +"','" + temp.units +"','" + temp.sp_list +"','" + temp.gst_value +"','" + temp.cess_value +"'," + temp.sales_profit +"),"
                  }

                if (salesSaveData['2'].sales_prod_id != ":")
                  {
                    
                    temp = salesSaveData['2']
                    sql3 += "('"+  salesIds[0] + "' , '" + salesIds[2] +"' , " + accId + ",'" + temp.sales_prod_id +"','"  + temp.sales_pur_id +"','" + temp.sales_prod_qty +"','" + temp.sales_prod_sp +"','" + saleDate + "',0,'" + insertTime + "',"+insertId +",'"+ Time + "',(select user_id from somanath.users where user_name = '" + userName +"')),"
                    sql4 += "('"+  salesIds[0] + "' , '" + salesIds[2] +"' , '" + temp.sales_prod_id +"','"  + temp.cost_price +"','" + temp.units +"','" + temp.sp_list +"','" + temp.gst_value +"','" + temp.cess_value +"'," + temp.sales_profit +"),"
                  }

                if (salesSaveData['3'].sales_prod_id != ":")
                  {
                    
                    temp = salesSaveData['3']
                    sql3 += "('"+  salesIds[0] + "' , '" + salesIds[3] +"' , " + accId + ",'" + temp.sales_prod_id +"','"  + temp.sales_pur_id +"','" + temp.sales_prod_qty +"','" + temp.sales_prod_sp +"','" + saleDate + "',0,'" + insertTime + "',"+insertId +",'"+ Time + "',(select user_id from somanath.users where user_name = '" + userName +"')),"
                    sql4 += "('"+  salesIds[0] + "' , '" + salesIds[3] +"' , '" + temp.sales_prod_id +"','"  + temp.cost_price +"','" + temp.units +"','" + temp.sp_list +"','" + temp.gst_value +"','" + temp.cess_value +"'," + temp.sales_profit +"),"
                  }
                  BillNumber = salesIds[0].slice(3,)
                  toSendfirmIds =[]
                  for(i=1;i<salesIds.length-1;i++)
                  {
                    if(salesIds[i] != '')
                    {
                      toSendfirmIds.push([i,salesIds[i]])
                    }
                  }
                    
                  SqlFinal +="DELETE FROM somanath20"+ dbYear +".sales where sales_id ='"+ salesIds[0] +"';DELETE FROM somanath20"+ dbYear +".sales_sp where sales_id = '"+ salesIds[0] +"';"+sql3.slice(0, -1)+';'+sql4.slice(0, -1)
                }  
                else
                {//NewState
                Time = new Date
                Time = Time.getFullYear()+"-"+String(Time.getMonth()+1).padStart(2 , '0')+"-"+String(Time.getDate()).padStart(2 , '0')+" "+String(Time.getHours()).padStart(2 , '0')+":"+String(Time.getMinutes()).padStart(2 , '0')+":"+String(Time.getSeconds()).padStart(2 , '0')
                
                maxIds = connection.query("SELECT sales+1 as sales, firm1+1 as firm1, firm2+1 as firm2, firm3+1 as firm3 FROM somanath20"+dbYear+".max_id ")
                sql3 = "insert into somanath20" + dbYear + ".sales values "
                sql4 = "insert into somanath20" + dbYear + ".sales_sp values "

                saleDate = saleDate1.split("-")

                saleDate = saleDate[2] + "-" + saleDate[1] + "-" + saleDate[0]
                
                maxIdUpdate = []

                if (salesSaveData['1'].sales_prod_id != ":")
                  {
                    maxIdUpdate.push(1)
                    temp = salesSaveData['1']
                    sql3 += "('" + dbYear + "_" + maxIds[0]['sales'] + "' , 'SSM_" + maxIds[0]['firm1'] +"' , " + accId + ",'" + temp.sales_prod_id +"','"  + temp.sales_pur_id +"','" + temp.sales_prod_qty +"','" + temp.sales_prod_sp +"','" + saleDate + "',0,'" + Time + "',(select user_id from somanath.users where user_name = '" + userName +"') , NULL , NULL),"
                    sql4 += "('" + dbYear + "_" + maxIds[0]['sales'] + "' , 'SSM_" + maxIds[0]['firm1'] +"','" + temp.sales_prod_id +"','"  + temp.cost_price +"','" + temp.units +"','" + temp.sp_list +"','" + temp.gst_value +"','" + temp.cess_value +"'," + temp.sales_profit +"),"
                  }
                if (salesSaveData['2'].sales_prod_id != ":")
                  {
                    maxIdUpdate.push(2)
                    temp = salesSaveData['2']
                    sql3 += "('" + dbYear + "_" + maxIds[0]['sales'] + "' , 'SCM_" + maxIds[0]['firm2'] +"' , " + accId + ",'" + temp.sales_prod_id +"','"  + temp.sales_pur_id +"','" + temp.sales_prod_qty +"','" + temp.sales_prod_sp +"','" + saleDate + "',0,'" + Time + "',(select user_id from somanath.users where user_name = '" + userName +"') , NULL , NULL),"
                    sql4 += "('" + dbYear + "_" + maxIds[0]['sales'] + "' , 'SCM_" + maxIds[0]['firm2'] +"','" + temp.sales_prod_id +"','"  + temp.cost_price +"','" + temp.units +"','" + temp.sp_list +"','" + temp.gst_value +"','" + temp.cess_value +"'," + temp.sales_profit +"),"
                  }
                if (salesSaveData['3'].sales_prod_id != ":")
                  {
                    maxIdUpdate.push(3)
                    temp = salesSaveData['3']
                    sql3 += "('" + dbYear + "_" + maxIds[0]['sales'] + "' , 'SEM_" + maxIds[0]['firm3'] +"' , " + accId + ",'" + temp.sales_prod_id +"','"  + temp.sales_pur_id +"','" + temp.sales_prod_qty +"','" + temp.sales_prod_sp +"','" + saleDate + "',0,'" + Time + "',(select user_id from somanath.users where user_name = '" + userName +"') , NULL , NULL),"
                    sql4 += "('" + dbYear + "_" + maxIds[0]['sales'] + "' , 'SEM_" + maxIds[0]['firm3'] +"','" + temp.sales_prod_id +"','"  + temp.cost_price +"','" + temp.units +"','" + temp.sp_list +"','" + temp.gst_value +"','" + temp.cess_value +"'," + temp.sales_profit +"),"
                  }

                //firm1 = , firm2 = , firm3 = 
                
                firmIds = ''
                toSendfirmIds =[]

                
                  maxIdUpdate.forEach(firmNumber => {
                    fNumber = String(":firm"+firmNumber).split(':')
                    firmIds += 'firm'+firmNumber+ " = "+maxIds[0][fNumber[1]]+','
                    toSendfirmIds.push([firmNumber,maxIds[0][fNumber[1]]])
                  });
  
                  sqlMax = "update somanath20" + dbYear + ".max_id set sales = "+maxIds[0]['sales']+","+firmIds.slice(0, -1)+';'
                  SqlFinal += sql3.slice(0, -1)+';'+sql4.slice(0, -1)+';'+sqlMax
                  BillNumber = maxIds[0]['sales'] 
                }

                res.status(200).send({'salesSaveData':salesSaveData,'BillNumber':BillNumber,'firmBillNumber':toSendfirmIds }) 
                con.query(SqlFinal)
                salesSaving = false
                //console.timeEnd("t1")

                    
              }
              
           
      }
})

app.get('/sales/edit',(req,res)=>{
  responseSent = false
  BillNumber = req.query.billNo

  usersLogged.forEach(element =>{

      if(element.sales.hasOwnProperty(BillNumber))
        {
          res.sendStatus(201)
          responseSent = true
        } 

  })

  if (!responseSent)
  {

                ip = req.socket.remoteAddress
                userName = req.query.user
                dbYear = req.query.dbYear
                saleDate = req.query.sale_date
                custName = req.query.cust_name
                sql = "SELECT sales_ref,sales_prod_id, sales_pur_id, sales_prod_qty, sales_prod_sp,  discount, date_format(insert_time,'%Y-%m-%d %H:%i:%S') as insert_time , insert_id FROM somanath20"+dbYear+".sales where sales_id='"+BillNumber+"'"
                con.query(sql,(err,result)=>{
                  sql1 = "SELECT sales_ref, cost_price, units, sp_list, gst_value, cess_value FROM somanath20"+dbYear+".sales_sp where sales_id='"+BillNumber+"'"
                  userIndex = 0
                  index = 0
                  saleIds = [BillNumber,'','','']
                  for(k = 0 ; k < result.length ; k++)
                  { 
                    //@
                    sale_ref = result[k]['sales_ref'].split('_').slice(0,-1)
                    if(sale_ref[0] === 'SSM'){ saleIds[1] = result[k]['sales_ref'] }
                    else if(sale_ref[0] === 'SCM'){ saleIds[2] = result[k]['sales_ref'] }
                    else{ saleIds[3] = result[k]['sales_ref'] }
                  }
                  usersLogged.forEach((element)=>{
                        
                        if (element.ip == ip)
                              { 
                                newSaleObject = {
                                  'saleDate' : saleDate , 
                                  'custName' : custName , 
                                  'insert_time' : result[0]['insert_time'], 
                                  'insert_id' : result[0]['insert_id'],
                                   'sales_ids' : saleIds,
                                  'products' : {}
                                }
                                element.sales[BillNumber] = newSaleObject
                                userIndex = index
                              }
                              index++
                    })
                  let values = []
                  //let products = {}
                  let Total = 0
                  let TotalHsn = 0 
                  let i =0 
                  let slNO  = 1
                  con.query(sql1,(err,result1)=>{
                    for(k = 0 ;k<result1.length;k++){
                    prodId = result[k]["sales_prod_id"].split(':').slice(1,-1)
                    qty = result[k]["sales_prod_qty"].split(':').slice(1,-1)
                    sp = result[k]["sales_prod_sp"].split(':').slice(1,-1)
                    prodUnits = result1[k]["units"].split('::').slice(1,-1)
                    prodSpList = result1[k]["sp_list"].split('::').slice(1,-1)
                    prodCp = result1[k]["cost_price"].split(':').slice(1,-1)
                    prodGst = result1[k]["gst_value"].split(':').slice(1,-1)
                    prodCess = result1[k]["cess_value"].split(':').slice(1,-1)
                    
                    i = 0
                    result[k]["sales_pur_id"].split(':').slice(1,-1).forEach(purchaseId=>{
                      sql2 = "SELECT stk_id,prod_name  FROM somanath20"+dbYear+".stocks,somanath.products where stk_pur_id = '"+purchaseId+"' and stk_prod_id ="+prodId[i]+" and stk_prod_id = prod_id;"
                      result3 = connection.query(sql2)
                      prodTotal = parseFloat(qty[i])*parseFloat(sp[i])
                      Total += prodTotal
                      prodTotalHsn = ( parseFloat(sp[i])-parseFloat(prodCp[i]) ) * parseFloat(qty[i])
                      TotalHsn +=  prodTotalHsn
                      
                      backEndUnits = "["
                      backEndSpList = "["
                      units = prodUnits[i].split(':')
                      spList = prodSpList[i].split(':')

                      units.forEach(u => backEndUnits += "'" + u + "'" + "," )
                      backEndUnits = backEndUnits.slice(0 , -1) + "]"
                      
                      spList.forEach(sp => backEndSpList += "'" + sp + "'" + "," )
                      backEndSpList = backEndSpList.slice(0 , -1) + "]"

                      values.push([slNO,result3[0]['prod_name'],qty[i],sp[i],(prodTotal).toFixed(2),(prodTotalHsn).toFixed(2),units,spList,prodCp[[i]],qty[i],prodGst[i],prodCess[i],result3[0]['stk_id'],prodId[i]])
                      sale_ref = result[k]['sales_ref'].split('_').slice(0,-1)
                      let firmId = 1
                      if(sale_ref[0] === 'SSM'){ firmId = 1}
                      else if(sale_ref[0] === 'SCM'){ firmId = 2}
                      else {firmId = 3}
                      //@ added E
                      backEndValues= ['E', result3[0]['prod_name'] ,  String(qty[i]), String(sp[i]), String((prodTotal).toFixed(2)), String((prodTotalHsn).toFixed(2)) , backEndUnits , backEndSpList,String(prodCp[[i]]), String(qty[i]), String(prodGst[i]), String(prodCess[i]),0,0,purchaseId,firmId,parseFloat(prodCp[i])]
                      slNO++
                      if(! usersLogged[userIndex].sales[BillNumber].products.hasOwnProperty(prodId[i]))
                          usersLogged[userIndex].sales[BillNumber].products[prodId[i]] = {}
                      usersLogged[userIndex].sales[BillNumber].products[prodId[i]][result3[0]['stk_id']] = backEndValues
                      i++
                    })

                    }
                    


                    

                    data = {'values':values,'slNO':slNO,'total':Total.toFixed(2),'total_hsn':TotalHsn.toFixed(2),'insert_time':result[0]['insert_time'],'insert_id':result[0]['insert_id']}
                    res.send(data)



                  })
                })
  }
  
})

app.get('/sales/voucher',(req,res)=>{
    editState = req.query.editState
    dbYear = req.query.dbYear
    //'dbYear','bank','cash','name','billDate','user_name'
    ////'billNo':'','firm1':'','firm2':'','firm3':'', : '','editState' : ''
    
    billNo = dbYear+"_"+req.query.billNo
    firm1_frontend = req.query.firm1
    firm2_frontend = req.query.firm2
    firm3_frontend = req.query.firm3
    if(req.query.billNo === '')
    { 
      //@ Need to check NULL
      billNo = 'NULL'
      firm1_frontend = 0
      firm2_frontend = 0
      firm3_frontend = 0
    }
  if(editState === 'True')
  {
    result = connection.query("SELECT date_format(insert_time,'%Y-%m-%d %H:%i:%S') as insert_time,insert_id FROM somanath20"+dbYear+".cashflow_sales where trans_sales ='"+billNo+"'")
    insertTime = result[0]['insert_time']
    insertId = result[0]['insert_id']
  } 

  sql = "SELECT acc_id FROM somanath.accounts where acc_name='"+req.query.name+"'"
  
  Time = new Date
  Time = Time.getFullYear()+"-"+String(Time.getMonth()+1).padStart(2 , '0')+"-"+String(Time.getDate()).padStart(2 , '0')+" "+String(Time.getHours()).padStart(2 , '0')+":"+String(Time.getMinutes()).padStart(2 , '0')+":"+String(Time.getSeconds()).padStart(2 , '0')
  con.query(sql,(err,result)=>{
    sql1 = "SELECT acc_cls_bal_firm1,acc_cls_bal_firm2,acc_cls_bal_firm3 FROM somanath20"+dbYear+".acc_bal where acc_id ="+result[0]['acc_id']
    con.query(sql1,(err1,result1)=>{
      firm1_bal = parseFloat((parseFloat(result1[0]['acc_cls_bal_firm1']) + parseFloat(firm1_frontend)).toFixed(2))
      firm2_bal = parseFloat((parseFloat(result1[0]['acc_cls_bal_firm2']) + parseFloat(firm2_frontend)).toFixed(2))
      firm3_bal = parseFloat((parseFloat(result1[0]['acc_cls_bal_firm3']) + parseFloat(firm3_frontend)).toFixed(2))
      
      old_bal = parseFloat(result1[0]['acc_cls_bal_firm1']) + parseFloat(result1[0]['acc_cls_bal_firm2']) + parseFloat(result1[0]['acc_cls_bal_firm3'])
      bill_amt = parseFloat(firm1_frontend)+parseFloat(firm2_frontend)+parseFloat(firm3_frontend) 
      
      bank = parseFloat(req.query.bank)
      cash = parseFloat(req.query.cash)
      
      amountPaid = parseFloat((bank+cash).toFixed(2))
      
      remaining_bal = old_bal + bill_amt - amountPaid

      oldBal = {
                'old_bal' : old_bal,
                'bill_amt' : bill_amt,
                'amountPaid' : amountPaid,
                'remaining_bal' : remaining_bal
              }

      firm1 = firm1_bal
      firm2 = firm2_bal
      firm3 = firm3_bal
      
      firm3_bank = 0
      firm2_bank = 0
      firm1_bank = 0
      
      firm3_cash = 0
      firm2_cash = 0
      firm1_cash = 0
      
      
      
      if(amountPaid>0)
      {
        if(amountPaid>=firm3_bal){
          if(bank<=firm3_bal)
          {
              firm3_bank = bank
              bank = 0
              
          }
          else if(bank>0)
          {
              bank -= firm3_bal
              firm3_bank = firm3_bal
          }
          amountPaid -= firm3_bal
          firm3_bal -= firm3_bank
        }
        else{
            if(bank<=firm3_bal)
            {
            firm3_bank = bank
            bank = 0 
            }
            else  if (bank>0)
            {
                bank -= firm3_bal
                firm3_bank = firm3_bal
            }
            firm3_bal -= firm3_bank
            amountPaid = 0
        }
  
        if(amountPaid>=firm2_bal){
          if(bank<=firm2_bal)
          {
              firm2_bank = bank
              bank = 0
              
          }
          else if(bank>0)
          {
              bank -= firm2_bal
              firm2_bank = firm2_bal
          }
          amountPaid -= firm2_bal
          firm2_bal -= firm2_bank
        }
        else{
            if(bank<=firm2_bal)
            {
            firm2_bank = bank
            bank = 0 
            }
            else  if (bank>0)
            {
                bank -= firm2_bal
                firm2_bank = firm2_bal
            }
            firm2_bal -= firm2_bank
            amountPaid = 0
        }
        if(amountPaid>=firm1_bal){
          if(bank<=firm1_bal)
          {
              firm1_bank = bank
              bank = 0
              
          }
          else if(bank>0)
          {
              bank -= firm1_bal
              firm1_bank = firm1_bal
          }
          amountPaid -= firm1_bal
          firm1_bal -= firm1_bank
        }
        else{
            if(bank<=firm1_bal)
            {
            firm1_bank = bank
            bank = 0 
            }
            else  if (bank>0)
            {
                bank -= firm1_bal
                firm1_bank = firm1_bal
            }
            firm1_bal -= firm1_bank
            amountPaid = 0
        }
        if(amountPaid>=firm3_bal){
        if(cash<=firm3_bal)
        {
        firm3_cash = cash
        cash = 0
  
        }
        else if(cash>0)
        {
        cash -= firm3_bal
        firm3_cash = firm3_bal
        }
        amountPaid -= firm3_bal
        firm3_bal -= firm3_cash
        }
        else{
        if(cash<=firm3_bal)
        {
        firm3_cash = cash
        cash = 0 
        }
        else  if (cash>0)
        {
          cash -= firm3_bal
          firm3_cash = firm3_bal
        }
        firm3_bal -= firm3_cash
        amountPaid = 0
        }
        if(amountPaid>=firm2_bal){
          if(cash<=firm2_bal)
          {
              firm2_cash = cash
              cash = 0
              
          }
          else if(cash>0)
          {
              cash -= firm2_bal
              firm2_cash = firm2_bal
          }
          amountPaid -= firm2_bal
          firm2_bal -= firm2_cash
        }
        else{
            if(cash<=firm2_bal)
            {
            firm2_cash = cash
            cash = 0 
            }
            else  if (cash>0)
            {
                cash -= firm2_bal
                firm2_cash = firm2_bal
            }
            firm2_bal -= firm2_cash
            amountPaid = 0
        }
        if(amountPaid>=firm1_bal){
          if(cash<=firm1_bal)
          {
              firm1_cash = cash
              cash = 0
              
          }
          else if(cash>0)
          {
              cash -= firm1_bal
              firm1_cash = firm1_bal
          }
          amountPaid -= firm1_bal
          firm1_bal -= firm1_cash
        }
        else{
            if(cash<=firm1_bal)
            {
            firm1_cash = cash
            cash = 0 
            }
            else  if (cash>0)
            {
                cash -= firm1_bal
                firm1_cash = firm1_bal
            }
            firm1_bal -= firm1_cash
            amountPaid = 0
        }
        if(cash>0 )
        {
          firm1_bal -= cash
          firm1_cash += cash
          cash = 0
        }
        if(bank>0 )
        {
          firm1_bal -= bank
          firm1_bank += bank
          bank = 0
        }
      }
      else
      {
        firm1_bal -= cash
        firm1_cash = cash
      }

      //trans_id, trans_acc, trans_sales, trans_amt_firm1, amt_paid_firm1_cash, amt_paid_firm1_bank, trans_amt_firm2, amt_paid_firm2_cash, amt_paid_firm2_bank, trans_amt_firm3, amt_paid_firm3_cash, amt_paid_firm3_bank, trans_date, insert_time, insert_id, update_time, update_id
      

      sql2 = `SELECT cashflow_sales+1 as trans_id FROM somanath20${dbYear}.max_id;`
      con.query(sql2,(err2,result2)=>{
        date = req.query.billDate.split("-") 
        date = `${date[2]}-${date[1]}-${date[0]}`
        bankName = 1
        if(editState === 'True')
        {
          sql3 = `UPDATE somanath20${dbYear}.cashflow_sales SET  trans_acc =${result[0]['acc_id']}  , trans_amt_firm1 = ${firm1_frontend}, amt_paid_firm1_cash =${firm1_cash} , amt_paid_firm1_bank =${firm1_bank} , trans_amt_firm2 =${firm2_frontend} , amt_paid_firm2_cash =${firm2_cash} , amt_paid_firm2_bank =${firm2_bank} , trans_amt_firm3=${firm3_frontend} , amt_paid_firm3_cash=${firm3_cash} , amt_paid_firm3_bank=${firm3_bank}, bank_firm = ${bankName} , trans_date = '${date}', insert_time ='${insertTime}' , insert_id =${insertId} , update_time = '${Time}', update_id =(select user_id from somanath.users where user_name = '${req.query.user_name}') where trans_sales='${billNo}';`
        }
        else
        {
          sql3 = `insert into somanath20${dbYear}.cashflow_sales values ('${dbYear}_${result2[0]['trans_id']}',${result[0]['acc_id']},'${billNo}',${firm1_frontend},${firm1_cash},${firm1_bank},${firm2_frontend},${firm2_cash},${firm2_bank},${firm3_frontend},${firm3_cash},${firm3_bank},${bankName},'${date}','${Time}',(select user_id from somanath.users where user_name = '${req.query.user_name}'),NULL,NULL);`
          sql5 = `UPDATE somanath20${dbYear}.max_id set cashflow_sales =${result2[0]['trans_id']}`
          con.query(sql5)
        }
        con.query(sql3)
        sql4 = `UPDATE somanath20${dbYear}.acc_bal set acc_cls_bal_firm1 =${firm1_bal.toFixed(2)} ,acc_cls_bal_firm2=${firm2_bal.toFixed(2)},acc_cls_bal_firm3=${firm3_bal.toFixed(2)} where acc_id = ${result[0]['acc_id']}`
        con.query(sql4)
        res.send(oldBal)
      })
      
    })
  })

})

//sales entry routes done



process.on('uncaughtException', (error) => {

  backupData = {}
  usersLogged.forEach(element =>{
      backupData[element.ip] = element
  })
  fs.writeFileSync(path.join(homeDir,'Hosangadi2.0','backend','socket_server','NodeErr.txt'),JSON.stringify(backupData));
  //connection.query("update somanath.data set userslogged = '" + JSON.stringify(backupData) + "'");

  io.sockets.emit('sendError' ,"\n"+String(error.stack))
  process.exit(1)  
});

process.on('unhandledRejection', (error, promise)  => {
  backupData = {}
  usersLogged.forEach(element =>{
      backupData[element.ip] = element
  })
  fs.writeFileSync(path.join(homeDir,'Hosangadi2.0','backend','socket_server','NodeErr.txt'),JSON.stringify(backupData));
  io.sockets.emit('sendError' , error)
  process.exit(1); // Exit your app 
})


function myCustomErrorHandler(err, req, res, next) {
  backupData = {}
  usersLogged.forEach(element =>{
      backupData[element.ip] = element
  })
  fs.writeFileSync(path.join(homeDir,'Hosangadi2.0','backend','socket_server','NodeErr.txt'),JSON.stringify(backupData));
  io.sockets.emit('sendError' ,req.path+"\n"+String(err.stack))
  process.exit(1);
}
app.use(myCustomErrorHandler);



server.listen(5000);                                                                                                                           