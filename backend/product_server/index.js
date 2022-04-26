const ip = "localhost"
const io = require('socket.io-client')
const socket = io.connect('http://'+ip+':5000')
const express = require('express')
const app = express()
const mysql = require('mysql') 

let prod_list_show = []
let prod_list_all = []

let custList = []

 

con = mysql.createConnection({
    host: "localhost",
    port: "3306",
    user: "root",
    password: "mysqlpassword5"
});

con.connect()



socket.on("refreshProductServer" , ()=>{

  prod_list_show = []
  con.query("select  prod_id, prod_bar , prod_name from somanath.products where prod_hide = 'False' order by prod_name" , (err , result) =>{
      result.forEach(element => {
        prod_list_show.push(element['prod_name'])
      })
  });


  prod_list_all = []
  con.query("select  prod_id, prod_bar , prod_name from somanath.products order by prod_name" , (err , result) =>{
      result.forEach(element => {
          prod_list_all.push(element['prod_name'])
      })
  });

  custList = []
  con.query("select  acc_name from somanath.accounts where acc_type = 'CUST' order by acc_name" , (err , result) => {
    result.forEach(element => {
      custList.push(element['acc_name'])
    })
  })

console.log("refreshed!!");
});


con.query("select  prod_name from somanath.products where prod_hide = 'False' order by prod_name" , (err , result) =>{
    result.forEach(element => {
        prod_list_show.push(element['prod_name'])
    });
    //console.log(prod_list_show);
})

con.query("select  prod_name from somanath.products order by prod_name" , (err , result) =>{
  result.forEach(element => {
      prod_list_all.push(element['prod_name'])
  })
  //console.log(prod_list_show);
});

con.query("select  acc_name from somanath.accounts where acc_type = 'CUST' order by acc_name" , (err , result) => {
      result.forEach(element => {
        custList.push(element['acc_name'])
    })
})


app.get('/onlySql' , (req , res)=>{

  sql = req.query.sql
  con.query(sql , (err , result)=>{
    console.log(err);
    res.send(result)
  })
})

app.get('/getNameAll' , (req,res) => {
  prod_name = req.query['prod_name']
  matched_products = []
  prod_list_all.forEach(element => {
        matched = element.match(prod_name)
        if (matched != null) 
            matched_products.push(element)
  })
  res.send(matched_products)
  //console.log("matched : " , matched_products);
})

app.get('/getNameFew' , (req,res) => {
  prod_name = req.query['prod_name']
  matched_products = []
  prod_list_show.forEach(element => {
        matched = element.match(prod_name)
        if (matched != null) 
            matched_products.push(element)
  })
  res.send(matched_products)
  //console.log("matched : " , matched_products);
})

app.get('/getProdByBar' , (req , res )=>{
    sql = "select prod_id, prod_bar, prod_name, prod_gst, prod_cess, nml_unit, htl_unit, spl_unit, ang_unit from somanath.products where prod_bar regexp '"+req.query['prod_bar']+"'"
    con.query(sql , (err , result)=>{
      res.send(result)
    })
})

  app.get('/getProdByName' , (req , res )=>{
    sql = "select prod_id, prod_bar, prod_name, prod_gst, prod_cess, nml_unit, htl_unit, spl_unit, ang_unit from somanath.products where prod_name =  '"+req.query['prod_name']+"'"
    con.query(sql , (err , result)=>{
      res.send(result)
    })
})


app.get('/getCustName' , (req , res) => {
  custName = req.query['cust_name']
  matched_products = []
  custList.forEach(element => {
        matched = element.match(custName)
        if (matched != null) 
            matched_products.push(element)
  })
  res.send(matched_products)
})



process.on('uncaughtException', (error) => {
  console.log("here",error.message);
  socket.emit('sendError' ,"\n"+String(error.stack))
  process.exit(1)
});

process.on('unhandledRejection', (error, promise)  => {
  console.log('Alert!----------------- ERROR : ',  error);
  socket.emit('sendError' , error)
  process.exit(1); // Exit your app 
})

function myCustomErrorHandler(err, req, res, next) {
  console.log(err.stack);
  socket.emit('sendError' ,req.path+"\n"+String(err.stack))
  process.exit(1);

}

app.use(myCustomErrorHandler);




app.listen(4000)