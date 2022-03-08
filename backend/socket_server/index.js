const http = require('http');
const express = require('express');
const app = express();
const server = http.createServer(app);
const io = require('socket.io')(server)
const mysql = require('mysql'); 
const { time } = require('console');
const { exit } = require('process');

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
const systemOs = "ubuntu"
let purchaseSaving = false

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

        sql1 = "SELECT stk_pur_id , stk_prod_qty , stk_cost, stk_sp_nml, stk_sp_htl, stk_sp_spl, stk_sp_ang , acc_name , date_format(pur_date , '%d-%m-%Y') as pur_date   FROM somanath20"+dbYear+".stocks , somanath.accounts , somanath20"+dbYear+".purchases  where stk_prod_id = "+prodId+" and somanath20"+dbYear+".purchases.pur_acc = somanath.accounts.acc_id and somanath20"+dbYear+".stocks.stk_pur_id = somanath20"+dbYear+".purchases.pur_id order by  somanath20"+dbYear+".stocks.insert_time DESC, stk_prod_qty"
        con.query(sql1 , (err1 , res1) =>  {
                
                for( i = 0 ; i<res1.length  && nStocks < max; i++)
                  {
                      
                      stocks['totQty'] = parseFloat(stocks['totQty'])  + res1[i]['stk_prod_qty']
                      stocks['stocks'].push([ res1[i]['pur_date'] ,  res1[i]['acc_name'] ,  res1[i]['stk_cost'] ,  res1[i]['stk_prod_qty'] ,  res1[i]['stk_sp_nml'],  res1[i]['stk_sp_htl'],  res1[i]['stk_sp_spl'],  res1[i]['stk_sp_ang']])
                      nStocks += 1
                  }
                
                getOldStocks( prodId, dbYear - 1 , minYear , stocks , nStocks , max , clientResponse)

          })

      }


}

function insertToStocks( stkId ,purId , accId , firmId , dbYear , Time , userName , products , prodId , n , max , clientResponse , sqlStock)
{
    if (n >= max)
      {
        clientResponse.sendStatus(200)
        sqlStock = sqlStock.slice(0 , -1)
        con.query(sqlStock , (err , res) => purchaseSaving = false)
        
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

                      sqlStock +="('" + dbYear +"_"+stkId + "' , '"+purId + "'," + prodId[n] + "," + stk_prod_qty + "," +totStk + "," + products[prodId[n]][2] + ",'" + nmlSp + "','" + htlSp + "','" + angSp + "','" + splSp + "'," + products[prodId[n]][22] + "," + accId + "," + firmId + ",'" +   + "',(select user_id from somanath.users where user_name = '"+userName+"')"+" , NULL , NULL),"
                      stkId += 1
                      n+=1
                      if (n<=max)
                        insertToStocks( stkId ,purId , accId , firmId , dbYear , Time , userName , products , prodId , n , max , clientResponse , sqlStock)

                           
                      
                })

            
          })
      }
    
}

function purchaseEdit(prodId , balDiff  , stockDiff , prodQty , stocks , clientResponse , n , max, accId,ip )
{
    if (n >= max)
      {
        stockDiff.trans = balDiff
        
        

        sql = "SELECT acc_cls_bal FROM somanath20"+dbYear+".acc_bal where acc_id ="+accId
        con.query(sql,(err,result)=>{
          acc_cls_bal = result[0].acc_cls_bal - (balDiff[0]-balDiff[1])
          sql = "UPDATE somanath20"+dbYear+".acc_bal SET acc_cls_bal ="+acc_cls_bal.toFixed(1) +" where acc_id="+accId
          con.query(sql)
        })
       
        sql = "DELETE FROM somanath20"+dbYear+".cashflow where trans_pur ='"+stocks[0].stk_pur_id+"';DELETE FROM somanath20"+dbYear+".stocks where stk_pur_id = '"+stocks[0].stk_pur_id+"';DELETE FROM somanath20"+dbYear+".purchases where pur_id = '"+stocks[0].stk_pur_id+"';"
        con.query(sql) 
       
        
        purchaseSaving = false
        clientResponse.send(stockDiff)
        delete stockDiff.trans
        

        usersLogged.forEach(element => {
          if(element.ip == ip)
                  element.purchases.products = stockDiff
        });
        console.log("purchaseEdit :\n",usersLogged);

        return 0
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

                  sqln1 = "UPDATE somanath2022.stocks SET stk_tot_qty ="+ (parseFloat(stocks[n].stk_tot_qty)-parseFloat(stocks[n].stk_prod_qty)).toFixed(3) +" where stk_prod_id ="+prodId[n]
                  con.query(sqln1)
                  
                  n+=1
                  if (n<=max)
                    purchaseEdit(prodId , balDiff  , stockDiff , prodQty , stocks , clientResponse , n , max,accId,ip)
              })
          


          
      }
}


//global variables end
io.on('connection', function (socket) {
    //connection event starts here
    //adds data to usersLogged when login is approved
    
    clientIp = socket.handshake.address

    
    //all the params passed pushed to usersLogged
    socketData = socket.handshake.headers
    
    
    

    if ( socketData['user-agent'] ==  "node-XMLHttpRequest" )
        servers.push({"id" : socket.id })
    else
        usersLogged.push({"id" : socket.id , "ip" : clientIp , "userName" : socketData['user_name'] , "userType": socketData['user_type'] , "loggedInAt":getTime() , "purchases" : {} , "sales" : []})
    
    
    console.log("connection event starts here",usersLogged);

    //connection event ends here

    //root window disconnect event
          socket.on('disconnect' , (data)=> {
                  socketData = socket.handshake.headers
                  for (user = 0 ; user<usersLogged.length ; user ++)
                      {   
                          if(usersLogged[user].ip == socket.handshake.address)
                            usersLogged.splice(user , 1)
                      }
                    
          });   
    //root window disconnect event ends here
    //server refreshes
          socket.on('refresh' , ()=> {
                socket.broadcast.emit("refreshProducts")
          })
    //server refresh ends here


    //
          socket.on('purchaseError' , () => {
            console.log(usersLogged);
            console.log("purchaseError");
          }) 


    //      


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
    
    if(dbYear >= minYear)
      {
          
        n =  getOldStocks(prodId , dbYear , minYear , stocks , nStocks , max , res);
      }
    if(n)
        res.send(stocks)
    
  })
  
})


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
                        
                          console.log("addEditPurDetails :\n",usersLogged[0]);
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
    console.log("cancelPurchase\n",usersLogged);
    res.sendStatus(200)


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
          console.log("Products Added :\n " , element.purchases);
        }
  });
  res.send(usersLogged)

 
})

app.get('/purchases/removePurchaseProduct' , (req , res) =>{
  ip = req.socket.remoteAddress
  prodId = req.query.prod_id

  
  usersLogged.forEach(element => {

        if (element.ip == ip )
        {
          
          delete element.purchases.products[prodId]
         
          console.log("After delete : \n" , element.purchases);
        }
  });
  res.send(usersLogged)
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
                            sql2 = "select purchases , cashflow , stocks , acc_cls_bal from somanath20"+dbYear+".max_id , somanath20"+dbYear+".acc_bal where acc_bal.acc_id = " + accId
                            con.query(sql2 , (err2 , result2) => {
                                      maxPurId = parseInt(result2[0]['purchases'])+1
                                      //@shiva
                                      if(req.query.edit_state == 'True'){
                                        x = req.query.pur_id.split("_")
                                        maxPurId = x.pop()
                                      }
                                      
                                      maxCashID = parseInt(result2[0]['cashflow'])+1
                                      maxStockId = parseInt(result2[0]['stocks'])+1
                                      accBal = parseFloat(result2[0]['acc_cls_bal'])
                                      accBal += parseFloat(purBal)

                                      prodId = ":"
                                      prodQty = ":"

                                      Object.keys(purDetails.products).forEach(element =>{ 
                                        prodId += element +":"
                                        prodQty += purDetails.products[element][3] + ":" 
                                      })
                                      
                                      purDate = purDetails.purDate.split("-")
                                      purDate = purDate[2] + "-" + purDate[1] + "-" + purDate[0]
                                      

                                      sql3 = "insert into somanath20"+dbYear+".purchases values ('" + dbYear+"_"+ maxPurId + "'," + accId + "," + firmId + ",'" + purInv + "','" + prodId + "','" + prodQty + "'," + purExp +" , '" + purDate + "','"+  purDetails.taxMethod.split("-")[0].toUpperCase() + "','"+ Time +"',(select user_id from somanath.users where user_name = '"+userName+"')"+" , NULL , NULL);" 
                                      
                                      sql4 = "update somanath20"+dbYear+".acc_bal set acc_cls_bal = "+accBal+" where acc_id = " + accId + ";"
                                     
                                      sql5 = "insert into somanath20"+dbYear+".cashflow values ('"+ dbYear + "_" + maxCashID + "'," + accId + ", NULL, '"+dbYear+"_"+ maxPurId + "' , " + grandTotal + "," + amtPaid + ", 'DEB' , '" + payMeth + "','" + purDate + "','"+ Time +"',(select user_id from somanath.users where user_name = '"+userName+"')"+" , NULL , NULL);" 
                                      

                                      maxStkId = Number(maxStockId) + Number(Object.keys(purDetails.products).length)

                                      sql6 = "update somanath20" + dbYear + ".max_id set purchases = " + maxPurId + " , cashflow = " + maxCashID + " , stocks = " + maxStkId + ";"
                                      
                                      sqlStock =  "insert into somanath20"+dbYear+".stocks values "
                                      con.query(sql3 + sql4 + sql5 + sql6 , (err3, result3) =>{
                                        
                                        insertToStocks(maxStockId , dbYear+"_"+ maxPurId , accId , firmId , dbYear , Time , userName, purDetails.products , Object.keys(purDetails.products) , 0 , Object.keys(purDetails.products).length , res , sqlStock)
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
              con.query("SELECT acc_cls_bal FROM somanath20"+dbYear+".acc_bal where acc_id = "+accId , (err1 , result1) =>{
                            

                            sql2 = "SELECT * from somanath20"+dbYear+".cashflow where trans_pur = '" + purId + "'"
                            con.query(sql2 , (err2 , result2) =>{
                                        
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

                                              
                                              purchaseEdit( Object.keys(stockDiff) , balDiff , stockDiff , prodQty , result3 , res , 0 , Object.keys(stockDiff).length, accId , ip )


                                              //res.sendStatus(200)
                                        })

                                })

                    })
              
        }

})

//purchase entry routes done



server.listen(5000);