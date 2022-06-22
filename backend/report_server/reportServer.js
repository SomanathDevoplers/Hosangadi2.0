const path = require('path')
const ip = "localhost"
const io = require('socket.io-client')
const socket = io.connect('http://'+ip+':5000' )
const express = require('express')
const app = express()
const mysql = require('mysql') 
const multer = require('multer')
const fs = require('fs')
const mv = require('mv')
const { Console, dir, log } = require('console')
const { response } = require('express')
const { execPath } = require('process')
const homeDir = require('os').homedir()
const { createWriteStream } = require ("fs");
const PDFDocument = require("pdfkit"); 
var MySql = require('sync-mysql');

let photos = []
let barcodeInUse = []

var connection = new MySql({
  host: "localhost",
  port: "3306",
  user: "root",
  password: "mysqlpassword5",
  multipleStatements : true
});


const con = mysql.createConnection({
  host: "localhost",
  port: "3306",
  user: "root",
  password: "mysqlpassword5",
  multipleStatements : true
});

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
      cb(null , path.join(homeDir , "angadiImages"))   // homedir + slashType +"angadiImages"
  },

  filename: function (req, file, cb) {
    originalName = file.originalname.split(".")
    fileName = "temp"+Math.floor(Math.random()*100) + "." + originalName.slice(-1)
    photos.push(fileName)
    cb(null, fileName)
  }
  
})


con.connect()




const files = multer({storage : storage})

serveDirectory = path.join(homeDir , "angadiImages")
app.use( '/images' , express.static(serveDirectory))


app.get('/onlySql' , (req , res)=>{
  
      sql = req.query.sql
      con.query(sql , (err , result)=>{

        res.send(result)
      })
})




app.post('/firms/save' , files.array('images' , 3) , (req,res) =>{
    let sqlInputs = req.query  
    ID = sqlInputs['firm_id']
    edit = false
    sql = "select firm_name from somanath.firms where (firm_name = '"+sqlInputs.firm_name+"' or firm_suffix = '"+sqlInputs.firm_suffix+"'"
        if (sqlInputs.firm_pan != "")
              sql += " or firm_pan = '"+sqlInputs.firm_pan+"'"
        if (sqlInputs.firm_gst != "")
          sql += " or firm_gstin = '"+sqlInputs.firm_gst+"'"
    sql += ")"
    if(ID != '')
      {
        sql += " and firm_id !="+ ID
        edit = true
      }  
      con.query(sql , (err1 , result1) => {
                            if (result1.length > 0)
                              {
                                   res.sendStatus(201)
                                    photos = []
                              }

                              else
                              {

                                    Time = new Date
                                    Time = Time.getFullYear()+"-"+String(Time.getMonth()+1).padStart(2 , '0')+"-"+String(Time.getDate()).padStart(2 , '0')+" "+String(Time.getHours()).padStart(2 , '0')+":"+String(Time.getMinutes()).padStart(2 , '0')+":"+String(Time.getSeconds()).padStart(2 , '0')
                                    if (!edit)
                                    {
                                                  sql1 = "select max(firm_id) from somanath.firms"
                                                    con.query(sql1 , (err1 , result1)=>{
                                                      if (result1 == null)
                                                        ID = 1
                                                      else
                                                        ID = result1[0]['max(firm_id)']+1 


                                                      photoIndex = 0
                                                      newDirectory =  path.join(homeDir , "angadiImages" , "firms" , String(ID))

                                                      
                                                      fs.mkdirSync(newDirectory , ()=>{})

                                                      newImageName = ""

                                                      if(sqlInputs.firm_qr == "True")
                                                      {
                                                        newImageName = path.join(newDirectory , "qr."+photos[photoIndex].split(".")[1])
                                                        fs.renameSync(path.join(homeDir , "angadiImages" , String(photos[photoIndex])) , newImageName , (err)=>{})          
                                                        photoIndex += 1          
                                                        
                                                      }

                                                    if(sqlInputs.firm_logo == "True")
                                                      {
                                                        newImageName = path.join(newDirectory , "logo."+photos[photoIndex].split(".")[1])
                                                        fs.renameSync(path.join(homeDir , "angadiImages" , String(photos[photoIndex])) , newImageName , (err)=>{})  
                                                        photoIndex += 1
                                                       
                                              
                                                      }

                                                    if(sqlInputs.firm_photo == "True")
                                                      {
                                                        newImageName = path.join(newDirectory , "photo."+photos[photoIndex].split(".")[1])
                                                        fs.renameSync(path.join(homeDir , "angadiImages" , String(photos[photoIndex])) , newImageName , (err)=>{})
                                                       
                                                      }
                                            
                                                      photos = []

                                    
                                                                                                                                                                                                                                                                                                                                                                   
                                                      sql2 = "insert into somanath.firms values("+String(ID)+",'"+sqlInputs.firm_type+"','"+sqlInputs.firm_name+"','"+sqlInputs.firm_suffix+"','"+sqlInputs.firm_email+"','"+sqlInputs.firm_mobile+"','"+sqlInputs.firm_website+"','"+sqlInputs.firm_address+"','"+sqlInputs.firm_gst+"','"+sqlInputs.firm_pan+"','"+sqlInputs.firm_bank+"','"+sqlInputs.firm_acno+"','"+sqlInputs.firm_ifsc+"','"+sqlInputs.firm_upiid+"','"+sqlInputs.firm_qr+"','"+sqlInputs.firm_logo+"','"+sqlInputs.firm_photo+"','"+Time+"',(select user_id from somanath.users where user_name = '"+sqlInputs.user_name+"') , NULL , NULL)" 
                                                      con.query(sql2 , (err2 , result2)=>{
                                                            //con.commit()
                                                            res.sendStatus(200)
                                                        })

                                                })


                                            }
                                    else        
                                            {

                                                      photoIndex = 0
                                                      newDirectory =  path.join(homeDir , "angadiImages" , "firms" , String(ID))

                                                    
                                                      newImageName = ""

                                                      if(sqlInputs.firm_qr == "True")
                                                      {
                                                        newImageName = path.join(newDirectory , "qr."+photos[photoIndex].split(".")[1])
                                                        fs.renameSync(path.join(homeDir , "angadiImages" , String(photos[photoIndex])) , newImageName , (err)=>{})          
                                                        photoIndex += 1          
                                                        
                                                      }

                                                    if(sqlInputs.firm_logo == "True")
                                                      {
                                                        newImageName = path.join(newDirectory , "logo."+photos[photoIndex].split(".")[1])
                                                        fs.renameSync(path.join(homeDir , "angadiImages" , String(photos[photoIndex])) , newImageName , (err)=>{})  
                                                        photoIndex += 1
                                                        
                                              
                                                      }

                                                    if(sqlInputs.firm_photo == "True")
                                                      {
                                                        newImageName = path.join(newDirectory , "photo."+photos[photoIndex].split(".")[1])
                                                        fs.renameSync(path.join(homeDir , "angadiImages" , String(photos[photoIndex])) , newImageName , (err)=>{})
                                                        
                                                      }
                                            
                                                      photos = []



                                                  sql2 = "update somanath.firms set firm_tax = '"+sqlInputs.firm_type+"', firm_name = '"+sqlInputs.firm_name+"', firm_suffix = '"+sqlInputs.firm_suffix+"', firm_email = '"+sqlInputs.firm_email+"', firm_mobile = '"+sqlInputs.firm_mobile+"', firm_website = '"+sqlInputs.firm_website+"', firm_address = '"+sqlInputs.firm_address+"', firm_gstin = '"+sqlInputs.firm_gst+"', firm_pan = '"+sqlInputs.firm_pan+"', firm_bank = '"+sqlInputs.firm_bank+"', firm_accno = '"+sqlInputs.firm_acno+"', firm_ifsc = '"+sqlInputs.firm_ifsc+"', firm_upid = '"+sqlInputs.firm_upiid+"', firm_upiqr = '"+sqlInputs.firm_qr+"', firm_logo = '"+sqlInputs.firm_logo+"', firm_photo = '"+sqlInputs.firm_photo+"', update_time = '"+Time+"', update_id = (select user_id from somanath.users where user_name = '"+sqlInputs.user_name+"') where firm_id = "+String(ID) 
                                                  con.query(sql2 , (err2 , result2)=>{
                                                    con.commit()
                                                    res.sendStatus(200)
                                                })

                                            }
                                    
                              }


          })

})

app.get('/firms/getFirmList' , (req , res )=>{
  sql = "select firm_id , firm_suffix , firm_name from somanath.firms"
  if(req.query.tax_check == "True")
    sql += " where firm_tax != 'CASH'"
  sql += " order by firm_id"

  con.query(sql , (err , result)=>{
    res.send(result)
  })
})

//firms get selected item
app.get('/firms/getSelectedFirm' , (req,res) => {
    sql = "select * from somanath.firms where firm_id = " + req.query.firm_id

    con.query(sql , (err , result) =>{
      
      res.send(result)
    })    
})
//Done firms!!






//TAXES
app.post('/taxes/save' , (req,res) => {
  let sqlInputs = req.query
  ID = sqlInputs['tax_id']
  edit = false
  sql = "select tax_per from somanath.taxes where tax_per = "+ sqlInputs["tax_per" ] +" and tax_type = '"+ sqlInputs["tax_type" ] +"'" 
  if(ID != '')
      {
        sql += " and tax_id != "+ ID
        edit = true
      } 
  con.query(sql , (err , result)=>{
      if (result.length > 0)
        {
             res.sendStatus(201)
              photos = []
        }

        else
        {
          Time = new Date
          Time = Time.getFullYear()+"-"+String(Time.getMonth()+1).padStart(2 , '0')+"-"+String(Time.getDate()).padStart(2 , '0')+" "+String(Time.getHours()).padStart(2 , '0')+":"+String(Time.getMinutes()).padStart(2 , '0')+":"+String(Time.getSeconds()).padStart(2 , '0')

          if(edit)
            {
                sql1 = "update somanath.taxes set tax_type='"+sqlInputs.tax_type+"',"+"tax_per ='"+sqlInputs.tax_per+"',"+"update_time='"+Time+"',"+"update_id=(select user_id from somanath.users where user_name = '"+sqlInputs.user_name+"') where tax_id ="+ID
                con.query(sql1 , (err1 , result1) => {
                  con.commit()
                  res.sendStatus(200)
                  //#socket call refresh event
                  })

            }
          else
            {
              sql1 = "select max(tax_id) from somanath.taxes"
              con.query(sql1 , (err1 , result1)=>{
                      
                      if (result1 == null)
                        ID = 1
                      else
                        ID = result1[0]['max(tax_id)']+1
                      sql2 =  "insert into somanath.taxes values ("+String(ID)+",'"+sqlInputs.tax_type+"','"+sqlInputs.tax_per+"','"+Time+"',(select user_id from somanath.users where user_name = '"+sqlInputs.user_name+"')"+" , NULL , NULL)"
                      con.query(sql2 , (err2 , result2) => {
                          con.commit()
                          res.sendStatus(200)
                        //#socket call refresh event
                        })     

                })

            }

        }
  })

})

//taxes get selected item
app.get('/taxes/getSelectedTax' , (req,res) => {
  sql = "select * from somanath.taxes where tax_id = " + req.query.tax_id
  con.query(sql , (err , result) =>{
   
    res.send(result)
  })
})

//taxes get all for treeview
app.get('/taxes/getTaxList' , (req , res )=>{

  sql = "SELECT tax_id,tax_type,tax_per FROM somanath.taxes order by tax_id"
  con.query(sql , (err , result)=>{
    res.send(result)
  })
})

//Taxes done!!








//Category
app.post('/cat/save' , files.array('images', 1) ,(req,res) => {
  let sqlInputs = req.query
  ID = sqlInputs['cat_id']
  edit = false
  sql = "select cat_name from somanath.categories where cat_name = '"+sqlInputs['cat_name']+"'"
  if(ID != '')
    {
      edit = true
      sql += " and cat_id != "+ ID
    }
    con.query(sql , (err , result)=>{
            if (result.length > 0)
              {
                  res.sendStatus(201)
                    photos = []
              }

              else
              {
                Time = new Date
                Time = Time.getFullYear()+"-"+String(Time.getMonth()+1).padStart(2 , '0')+"-"+String(Time.getDate()).padStart(2 , '0')+" "+String(Time.getHours()).padStart(2 , '0')+":"+String(Time.getMinutes()).padStart(2 , '0')+":"+String(Time.getSeconds()).padStart(2 , '0')
                if(edit)
                    {
                              newDirectory =  path.join(homeDir , "angadiImages" , "categories" , String(ID))
                              

                              if(sqlInputs.cat_image == "True")
                              {
                                newImageName = path.join(newDirectory , "photo."+photos[0].split(".")[1])
                                fs.renameSync(path.join(homeDir , "angadiImages" , String(photos[0])) , newImageName , (err)=>{})
                              }
                    
                              photos = []



                            sql1 = "update somanath.categories set cat_name = '"+sqlInputs.cat_name+"', cat_image = '"+sqlInputs.cat_image+"', update_time = '"+Time+"', update_id = (select user_id from somanath.users where user_name = '"+sqlInputs.user_name+"') where cat_id = "+String(ID) 
                            con.query(sql1 , (err1 , result1)=>{
                              con.commit()
                              res.sendStatus(200)
                          })



                    }
                  else
                    {
                      sql1 = "select max(cat_id) from somanath.categories"
                      con.query(sql1 , (err1 , result1)=>{
                              if (result1 == null)
                                ID = 1
                              else
                                ID = result1[0]['max(cat_id)']+1

                                photoIndex = 0
                                newDirectory =  path.join(homeDir , "angadiImages" , "categories" , String(ID))            
                                fs.mkdirSync(newDirectory , ()=>{})
                                

                                if(sqlInputs.cat_image == "True")
                              {
                                newImageName = path.join(newDirectory , "photo."+photos[0].split(".")[1])
                                fs.renameSync(path.join(homeDir , "angadiImages" , String(photos[0])) , newImageName , (err)=>{})
                                
                              }
                    
                              photos = []

                              sql2 =  "insert into somanath.categories values ("+String(ID)+",'"+sqlInputs.cat_name+"','"+sqlInputs.cat_image+"','"+Time+"',(select user_id from somanath.users where user_name = '"+sqlInputs.user_name+"')"+" , NULL , NULL)"
                              con.query(sql2 , (err2 , result2) => {
                                  con.commit()
                                  res.sendStatus(200)
                                //#socket call refresh event
                                }) 
                                                      
                              
                      })

                    }

              }
      })

})


//cat get all for treeview
app.get('/cat/getCatList' , (req , res )=>{
  sql = "SELECT cat_id,cat_name FROM somanath.categories order by cat_name"
  con.query(sql , (err , result)=>{
    res.send(result)
  })
})

//cat get selected item
app.get('/cat/getSelectedCat' , (req,res) => {
  sql = "select * from somanath.categories where cat_id = " + req.query.cat_id
  con.query(sql , (err , result) =>{
   
    res.send(result)
  })
})

//edit save cat

//category done!!!













//products
app.post('/products/save' , files.array('images' , 3) ,  (req,res) =>{
  let sqlInputs = req.query  
  ID = sqlInputs['prod_id']
  edit = false
  
  sql = "select prod_name from somanath.products where (prod_name = '"+sqlInputs.prod_name+"'"
  
  barcode = sqlInputs['prod_bar'].split(":")
  barcode.forEach(element => {
      if(element != "")
        {
          sql += " and prod_bar regexp ':"+element+":'"
        }
  });

  
  sql += ")"
  if(ID != '')
    {
      sql += " and prod_id !="+ ID
      edit = true
    }  
    
    con.query(sql , (err1 , result1) => {
                          
                          if (result1.length > 0)
                            {
                                 res.sendStatus(201)
                                  photos = []
                            }

                            else
                            {

                                  Time = new Date
                                  Time = Time.getFullYear()+"-"+String(Time.getMonth()+1).padStart(2 , '0')+"-"+String(Time.getDate()).padStart(2 , '0')+" "+String(Time.getHours()).padStart(2 , '0')+":"+String(Time.getMinutes()).padStart(2 , '0')+":"+String(Time.getSeconds()).padStart(2 , '0')

                                  if (!edit)
                                  {
                                                sql1 = "select max(prod_id) from somanath.products"
                                                  con.query(sql1 , (err1 , result1)=>{
                                                    
                                                    if (result1 == null)
                                                      ID = 1
                                                    else
                                                      ID = result1[0]['max(prod_id)']+1 


                                                
                                                      photoIndex = 0
                                                      newDirectory =  path.join(homeDir , "angadiImages" , "products" , String(ID))

                                                      
                                                      fs.mkdirSync(newDirectory , ()=>{})

                                                      newImageName = ""

                                                    

                                                    if(sqlInputs.img_high == "True")
                                                      {
                                                        newImageName = path.join(newDirectory , "high."+photos[photoIndex].split(".")[1])
                                                        fs.renameSync(path.join(homeDir , "angadiImages" , String(photos[photoIndex])) , newImageName , (err)=>{})  
                                                        photoIndex += 1
                                                       
                                              
                                                      }

                                                    if(sqlInputs.img_low == "True")
                                                      {
                                                        newImageName = path.join(newDirectory , "low."+photos[photoIndex].split(".")[1])
                                                        fs.renameSync(path.join(homeDir , "angadiImages" , String(photos[photoIndex])) , newImageName , (err)=>{})
                                                       
                                                      }
                                            
                                                      photos = []

                                    
                                                      sql2 = "insert into somanath.products values (" + String(ID) + ",'" + sqlInputs.prod_bar + "','"+ sqlInputs.prod_name + "','"+ sqlInputs.prod_cat + "','" + sqlInputs.prod_hsn + "','" + sqlInputs.prod_shelf + "','" + sqlInputs.prod_name_kan + "','" +sqlInputs.prod_name_eng + "'," + sqlInputs.prod_min_qty + "," + sqlInputs.prod_expiry + "," + sqlInputs.prod_mrp + "," + sqlInputs.prod_mrp_old + ",'" + sqlInputs.prod_sup + "', (select tax_id from somanath.taxes where tax_type = 0 and tax_per = " + sqlInputs.prod_gst + ") , (select tax_id from somanath.taxes where tax_type = 1 and tax_per = " + sqlInputs.prod_cess + "),'" + sqlInputs.prod_unit_type +"','" + sqlInputs.nml_unit + "','"   + sqlInputs.htl_unit + "','"  + sqlInputs.spl_unit + "','"  + sqlInputs.ang_unit + "','False','" + sqlInputs.prod_desc + "','" + sqlInputs.img_high + "','" + sqlInputs.img_low +"','" + Time + "',(select user_id from somanath.users where user_name = '"+sqlInputs.user_name+"') , NULL , NULL)"
                                                      
                                                      con.query(sql2,  (err2 , result2)=>{                                                          
                                                          con.commit()                                                      
                                                          res.sendStatus(200)
                                                          socket.emit("refresh")
                                                       })

                                              })


                                          }
                                  else        
                                          {

                                                    
                                            photoIndex = 0
                                            newDirectory =  path.join(homeDir , "angadiImages" , "products" , String(ID))

                                            
                                            //fs.mkdirSync(newDirectory , ()=>{})

                                            newImageName = ""

                                          

                                          if(sqlInputs.img_high == "True")
                                            {
                                              newImageName = path.join(newDirectory , "high."+photos[photoIndex].split(".")[1])
                                              fs.renameSync(path.join(homeDir , "angadiImages" , String(photos[photoIndex])) , newImageName , (err)=>{})  
                                              photoIndex += 1
                                             
                                    
                                            }

                                          if(sqlInputs.img_low == "True")
                                            {
                                              newImageName = path.join(newDirectory , "low."+photos[photoIndex].split(".")[1])
                                              fs.renameSync(path.join(homeDir , "angadiImages" , String(photos[photoIndex])) , newImageName , (err)=>{})
                                             
                                            }
                                  
                                            photos = []

                                            sql2 = "update somanath.products set prod_bar = '" + sqlInputs.prod_bar + "', prod_name = '"+ sqlInputs.prod_name + "', prod_cat = '"+ sqlInputs.prod_cat + "', prod_hsn = '" + sqlInputs.prod_hsn + "', prod_shelf = '" + sqlInputs.prod_shelf +"', prod_name_kan = '" + sqlInputs.prod_name_kan + "',  prod_name_eng = '" +sqlInputs.prod_name_eng + "', prod_min_qty = " + sqlInputs.prod_min_qty + ", prod_expiry = " + sqlInputs.prod_expiry + ", prod_mrp = " + sqlInputs.prod_mrp + ", prod_mrp_old = " + sqlInputs.prod_mrp_old + ", prod_sup = '" + sqlInputs.prod_sup + "',  prod_gst =  (select tax_id from somanath.taxes where tax_type = 0 and tax_per = " + sqlInputs.prod_gst + ") , prod_cess = (select tax_id from somanath.taxes where tax_type = 1 and tax_per = " + sqlInputs.prod_cess + "), prod_unit_type = '" + sqlInputs.prod_unit_type +"', nml_unit = '" + sqlInputs.nml_unit + "', htl_unit = '"   + sqlInputs.htl_unit + "', spl_unit = '"  + sqlInputs.spl_unit + "',  ang_unit =  '"  + sqlInputs.ang_unit + "', prod_hide = '"+sqlInputs.prod_hide+"',prod_desc = '" + sqlInputs.prod_desc + "', high_img = '" + sqlInputs.img_high + "', low_img = '" + sqlInputs.img_low +"',update_time = '" + Time + "',update_id = (select user_id from somanath.users where user_name = '"+sqlInputs.user_name+"')  where prod_id = "+ ID
                                            con.query(sql2 , (err2 , result2)=>{
                                                  con.commit()                          
                                                  res.sendStatus(200)
                                                  socket.emit("refresh")
                                              })

                                          }
                                  
                            }


        })

})

app.get('/products/getProductList' , (req , res )=>{
  sql = req.query.sql
    con.query(sql ,(err , result)=>{
      res.send(result)
    })
})

app.get('/products/getSelectedProduct' , (req,res) => {
  sql = "select * from somanath.products where prod_id = " + req.query.prod_id

  con.query(sql , (err , result) =>{
    res.send(result)
  })    
})

app.post('/barcodes' , (req,res)=>{
  type = req.query['type']
  barcode = req.query['barcode']
  barcodeInUse.sort(function(a, b){return a-b});

  sql = "select max_prod_bar from somanath.data"
  con.query(sql , (err,result) =>{
    maxBar = result[0]['max_prod_bar']
    
    if (type == 'get')
      {
          if (barcodeInUse.length > 0)
              {
                bar = parseInt(barcodeInUse[barcodeInUse.length-1])+1
                res.send(String(bar))
                exist = false
                barcodeInUse.forEach(element =>{
                    if(element == bar)
                      exist = true
                })
                
                if(!exist)
                  barcodeInUse.push(bar)
              }
          else
              {
                bar = parseInt(maxBar)+1
                res.send(String(bar))
                exist = false
                barcodeInUse.forEach(element =>{
                    if(element == bar)
                      exist = true
                })
                
                if(!exist)
                  barcodeInUse.push(bar)
                
              }
      }

    if(type == 'update')
      {
        exist = false
        bar =  parseInt(req.query['barcode'])
        barcodeInUse.forEach(element =>{
            if(element == bar)
              exist = true
        })
        if(!exist)
          barcodeInUse.push(bar)
        res.sendStatus(200)
      }


    if(type == 'save')
      {
        barcodeInUse = barcodeInUse.filter(function(f) { return f != parseInt(barcode) })
        max = true
        barcodeInUse.forEach(element => {
            if(barcode < element)
              max = false
        });

    
          
            
            sql1 = "update somanath.data set max_prod_bar = " + String(barcode)
            con.query(sql1)
            if(max)
                barcodeInUse.push(parseInt(barcode))

            res.sendStatus(200)
              
          
          
        
      }
    
  })



})

//products done!!





//employs

app.post('/employs/save' , files.array('images', 1),(req,res) => {
  let sqlInputs = req.query
  ID = sqlInputs['emp_id']
  edit = false
  sql = "select emp_name from somanath.employs where emp_name = '"+sqlInputs['emp_name']+"'"
  if(ID != '')
    {
      edit = true
      sql += " and emp_id != "+ ID
    }
    
    

          con.query(sql , (err , result)=>{
            if (result.length > 0)
              {
                  res.sendStatus(201)
                    photos = []
              }

              else
              {
                Time = new Date
                Time = Time.getFullYear()+"-"+String(Time.getMonth()+1).padStart(2 , '0')+"-"+String(Time.getDate()).padStart(2 , '0')+" "+String(Time.getHours()).padStart(2 , '0')+":"+String(Time.getMinutes()).padStart(2 , '0')+":"+String(Time.getSeconds()).padStart(2 , '0')
            
                if(edit)
                    {
                              newDirectory =  path.join(homeDir , "angadiImages" , "employs" , String(ID))
                              

                              if(sqlInputs.emp_img == "True")
                              {
                                newImageName = path.join(newDirectory , "photo."+photos[0].split(".")[1])
                                fs.renameSync(path.join(homeDir , "angadiImages" , String(photos[0])) , newImageName , (err)=>{})
                              }
                    
                              photos = []


                            //emp_id, emp_name, emp_address, emp_phone,emp_accno, emp_ifsc, emp_img, insert_time, insert_id, update_time, update_id
                            sql1 = "update somanath.employs set emp_name = '"+sqlInputs.emp_name+"',emp_address = '"+sqlInputs.emp_add+"',emp_phone = '"+sqlInputs.emp_mob+"',emp_accno = '"+sqlInputs.emp_acno+"',emp_ifsc = '"+sqlInputs.emp_ifsc+"', emp_img = '"+sqlInputs.emp_img+"', update_time = '"+Time+"', update_id = (select user_id from somanath.users where user_name = '"+sqlInputs.user_name+"') where emp_id = "+String(ID) 
                            con.query(sql1 , (err1 , result1)=>{
                              con.commit()
                              res.sendStatus(200)
                          })



                    }
                  else
                    {
                      sql1 = "select max(emp_id) from somanath.employs"
                      con.query(sql1 , (err1 , result1)=>{
                              if (result1 == null)
                                ID = 1
                              else
                                ID = result1[0]['max(emp_id)']+1

                                photoIndex = 0
                                newDirectory =  path.join(homeDir , "angadiImages" , "employs" , String(ID))            
                                fs.mkdirSync(newDirectory , ()=>{})
                                

                                if(sqlInputs.emp_img == "True")
                              {
                                newImageName = path.join(newDirectory , "photo."+photos[0].split(".")[1])
                                fs.renameSync(path.join(homeDir , "angadiImages" , String(photos[0])) , newImageName , (err)=>{})
                                
                              }
                    
                              photos = []
                              //                                                                                                                                            emp_id, emp_name, emp_address, emp_phone, emp_accno, emp_ifsc, emp_img, insert_time, insert_id, update_time, update_id                                                                                             
                              sql2 =  "insert into somanath.employs values ("+String(ID)+",'"+sqlInputs.emp_name+"','"+sqlInputs.emp_add+"','"+sqlInputs.emp_mob+"','"+sqlInputs.emp_acno+"','"+sqlInputs.emp_ifsc+"','"+sqlInputs.emp_img+"','"+Time+"',(select user_id from somanath.users where user_name = '"+sqlInputs.user_name+"')"+" , NULL , NULL)"
                              con.query(sql2 , (err2 , result2) => {
                                  con.commit()
                                  res.sendStatus(200)
                                //#socket call refresh event
                                }) 
                                                      
                              
                      })

                    }

              }
      })



        

})

app.get('/employs/getEmpList' , (req , res )=>{
  sql = "SELECT emp_id,emp_name FROM somanath.employs order by emp_name"
  con.query(sql , (err , result)=>{
    res.send(result)
  })
})

app.get('/employs/getSelectedEmp' , (req,res) => {
  sql = "select * from somanath.employs where emp_id = " + req.query.emp_id

  con.query(sql , (err , result) =>{
    res.send(result)
  })    
})


//employs Done!!


//accounts
app.post('/accounts/save' , files.array('images' , 3) , (req,res) =>{
  let sqlInputs = req.query  
  ID = sqlInputs['acc_id']
  edit = false
  sql = "select acc_name from somanath.accounts where (acc_name = '"+sqlInputs.acc_name+"'"

  if (sqlInputs.acc_gstin != "CASH")
    sql += " or acc_gstin = '"+sqlInputs.acc_gstin+"'"
  sql += ")"

  

  if(ID != '')
    {
      sql += " and acc_id !="+ ID
      edit = true
    }  
    con.query(sql , (err1 , result1) => {
                          if (result1.length > 0)
                            {
                                 res.sendStatus(201)
                                  photos = []
                            }

                            else
                            {

                                  Time = new Date
                                  Time = Time.getFullYear()+"-"+String(Time.getMonth()+1).padStart(2 , '0')+"-"+String(Time.getDate()).padStart(2 , '0')+" "+String(Time.getHours()).padStart(2 , '0')+":"+String(Time.getMinutes()).padStart(2 , '0')+":"+String(Time.getSeconds()).padStart(2 , '0')

                                  if (!edit)
                                  {
                                                sql1 = "select max(acc_id) from somanath.accounts"
                                                  con.query(sql1 , (err1 , result1)=>{
                                                    if (result1 == null)
                                                      ID = 1
                                                    else
                                                      ID = result1[0]['max(acc_id)']+1 


                                                
                                                    newDirectory =  path.join(homeDir , "angadiImages" , "accounts" , String(ID))

                                                    
                                                    fs.mkdirSync(newDirectory , ()=>{})

                                                    newImageName = ""

                                                    if(sqlInputs.acc_img == "True")
                                                    {
                                                      newImageName = path.join(newDirectory , "photo."+photos[0].split(".")[1])
                                                      fs.renameSync(path.join(homeDir , "angadiImages" , String(photos[0])) , newImageName , (err)=>{})          
                                                      
                                                    }

                                                  
                                          
                                                    photos = []

                                                    //acc_id, acc_opn_bal_firm1, acc_opn_bal_firm2, acc_opn_bal_firm3, acc_cls_bal_firm1, acc_cls_bal_firm2, acc_cls_bal_firm3
                                                                                                                                                                                                      //acc_id, acc_type, acc_name, acc_email, acc_add, acc_mob1, acc_mob2, acc_gstin, acc_accno, acc_ifsc, acc_cus_type, acc_img, insert_time, insert_id, update_time, update_id
                                                    sql2 = "insert into somanath.accounts values (" + String(ID) + ",'" + sqlInputs.acc_type + "','"+ sqlInputs.acc_name + "','"+ sqlInputs.acc_email + "','" + sqlInputs.acc_add + "','" + sqlInputs.acc_mob1+ "','" + sqlInputs.acc_mob2+ "','" + sqlInputs.acc_gstin+ "','" + sqlInputs.acc_accno+ "','" + sqlInputs.acc_ifsc+ "','" + sqlInputs.acc_cus_type + "','" +sqlInputs.acc_img+"','" + Time + "',(select user_id from somanath.users where user_name = '"+sqlInputs.user_name+"'),NULL,NULL);"
                                                    sql2 += "insert into somanath20"+sqlInputs.db_year+".acc_bal values("+String(ID)+",0.00,0.00,0.00,0.00,0.00,0.00)"
                                                    con.query(sql2 , (err2 , result2)=>{
                                                          con.commit()
                                                          res.sendStatus(200)
                                                          socket.emit("refresh")
                                                      })
                                              })
                                          }
                                  else        
                                          {
                                                    newDirectory =  path.join(homeDir , "angadiImages" , "accounts" , String(ID))
                                                    newImageName = ""
                                                  if(sqlInputs.acc_img == "True")
                                                    {
                                                      newImageName = path.join(newDirectory , "photo."+photos[0].split(".")[1])
                                                      fs.renameSync(path.join(homeDir , "angadiImages" , String(photos[0])) , newImageName , (err)=>{})
                                                    }
                                                    photos = []
                                                sql2 = "update somanath.accounts set acc_type = '"+sqlInputs.acc_type+"', acc_name = '"+sqlInputs.acc_name+"', acc_email = '"+sqlInputs.acc_email+"', acc_add = '"+sqlInputs.acc_add+"', acc_mob1 = '"+sqlInputs.acc_mob1+"', acc_mob2 = '"+sqlInputs.acc_mob2+"',acc_gstin = '"+sqlInputs.acc_gstin+"', acc_accno = '"+sqlInputs.acc_accno+"', acc_ifsc = '"+sqlInputs.acc_ifsc+"', acc_cus_type = '"+sqlInputs.acc_cus_type+"', acc_img = '"+sqlInputs.acc_img+"', update_time = '"+Time+"', update_id = (select user_id from somanath.users where user_name = '"+sqlInputs.user_name+"') where acc_id = "+String(ID) 
                                                con.query(sql2 , (err2 , result2)=>{
                                                  con.commit()
                                                  res.sendStatus(200)
                                                  socket.emit("refresh")
                                              })

                                          }
                                  
                            }


        })

})

app.get('/accounts/getAccList' , (req , res )=>{
  
  sql = req.query['sql']
  if (req.query['tax_check'] == "True")
    sql = "SELECT acc_id,acc_name,acc_type FROM somanath.accounts where acc_id not in (select acc_id from somanath.accounts where acc_type = 'SUPP' and acc_gstin = '') order by acc_type , acc_name"
  

  
  

  con.query(sql , (err , result)=>{
    res.send(result)
  })
})

app.get('/accounts/getSelectedAcc' , (req,res) => {
  sql = "select * from somanath.accounts where acc_id = " + req.query.acc_id

  con.query(sql , (err , result) =>{

    res.send(result)
  })    
})



//Reports
app.get('/salesData' , (req,res) => {
  dictCashSales ={'0': [0,0,0] , '5': [0,0,0] , '12': [0,0,0] , '18': [0,0,0] , '28': [0,0,0] }
  dictGstSales = {'0': [0,0,0] , '5': [0,0,0] , '12': [0,0,0] , '18': [0,0,0] , '28': [0,0,0] }
  //#12#0.10714285714#18#0.15254237288#5#0.04761904761#28#0.21875


  sql = "SELECT somanath2021.sales_sp.sales_ref,sales_prod_sp,cost_price,sales_prod_qty,gst_value FROM somanath2021.sales inner join somanath2021.sales_sp on somanath2021.sales_sp.sales_ref =somanath2021.sales.sales_ref where somanath2021.sales.sale_date >=  '"+req.query.sdate+"' and sale_date <=  '"+req.query.edate+"';"
  
  con.query(sql , (err , result) =>{
    result.forEach(element => {
      sp = element.sales_prod_sp.split(':').slice(1,-1)
      cp = element.cost_price.split(':').slice(1,-1)
      qty = element.sales_prod_qty.split(':').slice(1,-1)
      gst = element.gst_value.split(':').slice(1,-1)
      
      if(element.sales_ref.split('_').shift() === 'SCM')
        {
          index = 0
          gst.forEach(gstRate =>{
            
            sp_l = parseFloat(sp[index])
            cp_l = parseFloat(cp[index])
            qty_l = parseFloat(qty[index])
            profit = ( sp_l - cp_l ) * qty_l
            switch(gstRate){
              case '0':
                dictCashSales['0'][0] +=  sp_l * qty_l
                dictCashSales['0'][1] +=  profit
                break
              case '5':
                dictCashSales['5'][0] +=  sp_l * qty_l
                dictCashSales['5'][1] +=  profit
                dictCashSales['5'][2] +=  profit * 0.04761904761
                break
              case '12':
                dictCashSales['12'][0] +=  sp_l * qty_l
                dictCashSales['12'][1] +=  profit
                dictCashSales['12'][2] +=  profit * 0.10714285714
                break
              case '18':
                dictCashSales['18'][0] +=  sp_l * qty_l
                dictCashSales['18'][1] +=  profit
                dictCashSales['18'][2] +=  profit * 0.15254237288
                break
              case '28':
                dictCashSales['28'][0] +=  sp_l * qty_l
                dictCashSales['28'][1] +=  profit
                dictCashSales['28'][2] +=  profit * 0.21875
                break
            }
            index++
          })
        }
      else  
        {
          index = 0
          gst.forEach(gstRate =>{
            sp_l = parseFloat(sp[index])
            cp_l = parseFloat(cp[index])
            qty_l = parseFloat(qty[index])
            profit = ( sp_l - cp_l ) * qty_l
            switch(gstRate){
              case '0':
                dictGstSales['0'][0] +=  sp_l * qty_l
                dictGstSales['0'][1] +=  profit 
                break
              case '5':
                dictGstSales['5'][0] +=  sp_l * qty_l
                dictGstSales['5'][1] +=  profit
                dictGstSales['5'][2] +=  profit * 0.04761904761
                break
              case '12':
                dictGstSales['12'][0] +=  sp_l * qty_l
                dictGstSales['12'][1] +=  profit
                dictGstSales['12'][2] +=  profit * 0.10714285714
                break
              case '18':
                dictGstSales['18'][0] +=  sp_l * qty_l
                dictGstSales['18'][1] +=  profit
                dictGstSales['18'][2] +=  profit * 0.15254237288
                break
              case '28':
                dictGstSales['28'][0] +=  sp_l * qty_l
                dictGstSales['28'][1] +=  profit
                dictGstSales['28'][2] +=  profit * 0.21875
                break
            }
            index++
          })
        }
    });
    
    totalCashSales = 0
    totalGstSales = 0
    totalProfit = 0
    totalRegularProfit = 0
    totalCompProfit = 0
    totalSalesRegularCash = 0 //that is gstrate 5 or 0
    totalSalesRegularGst = 0 //that is gstrate 5 or 0
    totalSalesCompostionCash = 0 
    totalSalesCompostionGst = 0
    netGstPayableRegular = 0
    netGstPayableCompo = 0
    Object.keys(dictCashSales).forEach(element => {
        totalCashSales += dictCashSales[element][0]
        totalGstSales += dictGstSales[element][0]
       
        if (element === '5' | element === '0') 
          {
            totalSalesRegularCash += dictCashSales[element][0]
            totalSalesRegularGst += dictGstSales[element][0]
            netGstPayableRegular += dictCashSales[element][2] + dictGstSales[element][2]
            totalRegularProfit += dictCashSales[element][1] + dictGstSales[element][1]
          }  
        else 
          {
            totalSalesCompostionCash += dictCashSales[element][0]
            totalSalesCompostionGst += dictGstSales[element][0]
            netGstPayableCompo += dictCashSales[element][2] + dictGstSales[element][2]
            totalCompProfit += dictCashSales[element][1] + dictGstSales[element][1]

          }
        dictCashSales[element][0] = dictCashSales[element][0].toFixed(2)
        dictCashSales[element][1] = dictCashSales[element][1].toFixed(2)
        dictCashSales[element][2] = dictCashSales[element][2].toFixed(2)
        dictGstSales[element][0] = dictGstSales[element][0].toFixed(2)
        dictGstSales[element][1] = dictGstSales[element][1].toFixed(2)
        dictGstSales[element][2] = dictGstSales[element][2].toFixed(2)
        

  });

  //'CASH':dictCashSales,'GST':dictGstSales 
    sales = { 'totalSales' : (totalGstSales+totalCashSales).toFixed(2) , 'totalGstSales' : totalGstSales.toFixed(2) , 'totalCashSales': totalCashSales.toFixed(2) }
    profit = {'totalProfit' : (totalCompProfit+totalRegularProfit).toFixed(2) , 'totalCompProfit' : totalCompProfit.toFixed(2) , 'totalRegularProfit': totalRegularProfit.toFixed(2)}
    regComp = {'regular' : (totalSalesRegularGst+totalSalesRegularCash).toFixed(2) ,'netGstPayableRegular':netGstPayableRegular , 'comp': (totalSalesCompostionGst+totalSalesCompostionCash).toFixed(2) ,'netGstPayableCompo':netGstPayableCompo }
    allData = { 'totalSales': sales , 'totalProfit' : profit ,'regComp' : regComp  }
    res.send(allData)
  })    
})//reports



function getOldtrans(  dbYear , mindbYear  , bills , nBill , max ,sqlwhere, clientResponse , accId)
{
    
    if( dbYear < mindbYear )
      { 
        
        if( nBill == 0)
        {
          clientResponse.send("[]")
          return
        }
        else
        {

          bills.push(accId)
          bills.push(dbYear+1)
          clientResponse.send(bills)
          return
        }
        
      }
    else if(nBill >= max)
      {
        bills.push(accId)
        bills.push(dbYear)
        clientResponse.send(bills)
        return 
      }
    else
      {

        sql = "SELECT date_format(trans_date,'%d-%b-%y') as transdate, trans_sales , trans_amt_firm1+trans_amt_firm2+trans_amt_firm3 as trans_amt , amt_paid_firm1_cash+amt_paid_firm2_cash+amt_paid_firm3_cash+amt_paid_firm1_bank+amt_paid_firm2_bank+amt_paid_firm3_bank as amt_paid,(trans_amt_firm1+trans_amt_firm2+trans_amt_firm3)-(amt_paid_firm1_cash+amt_paid_firm2_cash+amt_paid_firm3_cash+amt_paid_firm1_bank+amt_paid_firm2_bank+amt_paid_firm3_bank) as bal , trans_id FROM somanath20"+dbYear+".cashflow_sales where "+ sqlwhere
        con.query(sql , (err , res) =>  {

                res.forEach(element => {

                  if(nBill < max){
                    bills.push(element) 
                    nBill++
                  }
                });
                
                getOldtrans( dbYear-1 , mindbYear  , bills , nBill , max , sqlwhere, clientResponse , accId )

          })

      }


}

app.get('/reports/getCashflowSales' ,  (req,res) => {
  minYear = 21
  accName = req.query.acc_name
  sqlmin = "SELECT date_format(insert_time,'%y') as year,date_format(insert_time,'%m') as month , acc_id FROM somanath.accounts where acc_name = '"+accName+"'"
  
  con.query(sqlmin,(err,result)=>{
    y = parseInt(result[0].year)
    m = parseInt(result[0].month)
    accId = result[0].acc_id
    if (y < 23 & m < 4){
      minYear = 21
    }
    else if (m < 4) minYear = y-1
    else minYear = y
    startDate = req.query.sdate

  endDate = req.query.edate
  noBills = req.query.limit

  
  if ( startDate != '' | endDate != '') {
    year = parseInt(startDate.slice(2,4))
    month = parseInt(startDate.slice(3,5))
      if (year < 23 & month < 4){
        minYear = 21
      }
      else if (month < 4) minYear = year-1
      else minYear = year
     if ( startDate == '') sqlwhere = "trans_acc = "+accId+" and trans_date <='"+endDate+"' order by insert_time DESC"
     else if (endDate == '') sqlwhere = "trans_acc = "+accId+" and trans_date >= '"+startDate+"' order by insert_time DESC"
     else sqlwhere = "trans_acc = "+accId+" and trans_date >= '"+startDate+"' and trans_date <='"+endDate+"' order by insert_time DESC"
  }
  else { sqlwhere = 'trans_acc = '+accId+' order by insert_time DESC limit '+ noBills }
    getOldtrans(  req.query.db , minYear  , [] , 0 , noBills , sqlwhere , res , accId )

  })
  


})

function filterData( sales, clientResponse){
  let dictionary = {}
  let temp_dict_value = []

  for(var i = 0; i < sales.length; i++) {
    let temp_prod_id  = sales[i].sales_prod_id.split(":").slice(1,-1)
    let temp_sp       = sales[i].sales_prod_sp.split(":").slice(1,-1)
    let temp_qty      = sales[i].sales_prod_qty.split(":").slice(1,-1)
    let temp_date     = sales[i]["date"]
    
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
        
        if( nBill == 0 & bills.length == 0)
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

        sql = "SELECT sales_id,sales_prod_id,sales_prod_qty,sales_prod_sp,date_format(sale_date,'%d-%b-%y') as date FROM somanath20"+dbYear+".sales where sales_acc ="+acc_id+ sqlwhere

        con.query(sql , (err , res) =>  {
          if (res.length>0)
          {
            saleId = res[0]['sales_id']
          }
                  
                res.forEach(element => {
                  if(saleId != element['sales_id'])
                      {
                        nBill++
                        saleId = element['sales_id']
                      }
                  if(nBill < max){
                    bills.push(element)
                  }
                });
                getOldBill( dbYear-1 , mindbYear , acc_id , bills , nBill , max ,sqlwhere, clientResponse )

          })

      }

}

app.get('/reports/getCustomersales' ,  (req,res) => {
  minYear = 21
  accName = req.query.acc_name
  dbYear = req.query.db
  invNo = req.query.invNo
  responseSent = false
  if (invNo != "")
    {
        accName = connection.query( "select acc_name from somanath.accounts where acc_id = (select sales_acc from somanath20"+dbYear+".sales where sales_id = '"+dbYear + "_"+invNo+"' limit 1)")
        if (accName.length == 0)
          {
            res.sendStatus(201)
            responseSent = true
          }
        else  
        {

          accName = accName[0]['acc_name']
        }
    }

  if (!responseSent)
  {
          
          sqlmin = "SELECT date_format(insert_time,'%y') as year,date_format(insert_time,'%m') as month ,acc_id FROM somanath.accounts  where acc_name = '"+accName+"'"
          con.query(sqlmin,(err,result)=>{
            y = parseInt(result[0].year)
            m = parseInt(result[0].month)
            accId = result[0].acc_id
            if (y < 23 & m < 4){
              minYear = 21
            }
            else if (m < 4) minYear = y-1 
            else minYear = y
            
          startDate = req.query.sdate
          endDate = req.query.edate
          nBill = req.query.limit
          if(nBill == '')nBill = 100
          if (invNo.length > 0)
          { 
            sqlwhere = " and sales_id = '"+dbYear + "_" +invNo+"'"
          }
          else if ( startDate != '' | endDate != '') 
          {
            year = parseInt(startDate.slice(2,4))
            month = parseInt(startDate.slice(3,5))
            if (year < 23 & month < 4)
              {
                minYear = 21
            }
            else if (month < 4) minYear = year-1
            else minYear = year

            if ( startDate == '') sqlwhere = " and sale_date <='"+endDate+"' order by sale_date DESC"
            else if (endDate == '') sqlwhere = " and sale_date >= '"+startDate+"' order by sale_date DESC"
            else sqlwhere = " and sale_date >= '"+startDate+"' and sale_date <='"+endDate+"' order by sale_date DESC"
          }

          else {sqlwhere = ' order by sale_date DESC LIMIT '+ (nBill*3).toFixed(0) }
          getOldBill(  req.query.db , minYear , accId , [] , 0 , nBill , sqlwhere , res)


          })
  }
  
})

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
        
        sql = "SELECT sales_prod_id,sales_prod_qty,sales_prod_sp,date_format(sale_date,'%d-%b-%y') as date  FROM somanath20"+dbYear+".sales where sales_acc ="+(parseInt(acc_id))+ sqlwhere
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

function getOldtransPur(  dbYear , mindbYear  , bills , nBill , max ,sqlwhere, clientResponse )
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

        sql = "SELECT trans_pur,trans_amt,amt_paid,trans_mode,date_format(trans_date,'%d-%b-%y') as transdate FROM somanath20"+dbYear+".cashflow_purchase where "+ sqlwhere
        con.query(sql , (err , res) =>  {
               
                res.forEach(element => {

                  if(nBill < max){
                    bills.push(element) 
                    nBill++
                  }
                });
                
                getOldtransPur( dbYear-1 , mindbYear  , bills , nBill , max ,sqlwhere, clientResponse )

          })

      }


}



app.get('/reports/getCashflowPurchase' ,  (req,res) => {
  minYear = 21
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
  getOldtransPur(  req.query.db , minYear  , [] , 0 , noBills , sqlwhere , res)

  })
  
})

process.on('uncaughtException', (error) => {
  socket.emit('sendError' ,"\n"+String(error.stack))
  process.exit(1)
});

process.on('unhandledRejection', (error, promise)  => {
  socket.emit('sendError' , error)
  process.exit(1); // Exit your app 
})

function myCustomErrorHandler(err, req, res, next) {
  socket.emit('sendError' ,req.path+"\n"+String(err.stack))
  process.exit(1);
}
app.use(myCustomErrorHandler);

app.listen(6000) 
