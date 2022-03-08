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
const { homedir } = require('os');
const { Console, dir, log } = require('console')
const { response } = require('express')
const { execPath } = require('process')
const homeDir = require('os').homedir()
let photos = []
let barcodeInUse = []

 


const con = mysql.createConnection({
  host: "localhost",
  port: "3306",
  user: "root",
  password: "mysqlpassword5"
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
    console.log(photos);
  }
  
})


con.connect()



const files = multer({storage : storage})

serveDirectory = path.join(homeDir , "angadiImages")
app.use( '/images' , express.static(serveDirectory))


app.get('/onlySql' , (req , res)=>{

      sql = req.query.sql

      con.query(sql , (err , result)=>{
        console.log(err);
        console.log(result);
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
      console.log(sql);
      con.query(sql , (err1 , result1) => {
                            console.log(err1 , result1);
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
                                                      console.log(result1);
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
                                                      console.log(sql2);
                                                      con.query(sql2 , (err2 , result2)=>{
                                                            console.log(err2);
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
                                                  console.log(sql2);
                                                  con.query(sql2 , (err2 , result2)=>{
                                                    console.log(err2);
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
  console.log(req.query);
  let sqlInputs = req.query
  ID = sqlInputs['tax_id']
  edit = false
  sql = "select tax_per from somanath.taxes where tax_per = "+ sqlInputs["tax_per" ] +" and tax_type = '"+ sqlInputs["tax_type" ] +"'" 
  if(ID != '')
      {
        sql += " and tax_id != "+ ID
        edit = true
      } 
  console.log(sql);
  con.query(sql , (err , result)=>{
      console.log(err , result);
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
  console.log(sqlInputs);
  ID = sqlInputs['cat_id']
  edit = false
  sql = "select cat_name from somanath.categories where cat_name = '"+sqlInputs['cat_name']+"'"
  if(ID != '')
    {
      edit = true
      sql += " and cat_id != "+ ID
    }
    con.query(sql , (err , result)=>{
            console.log(err , result);
            if (result.length > 0)
              {
                  res.sendStatus(201)
                    photos = []
              }

              else
              {
                Time = new Date
                Time = Time.getFullYear()+"-"+String(Time.getMonth()+1).padStart(2 , '0')+"-"+String(Time.getDate()).padStart(2 , '0')+" "+String(Time.getHours()).padStart(2 , '0')+":"+String(Time.getMinutes()).padStart(2 , '0')+":"+String(Time.getSeconds()).padStart(2 , '0')
                console.log(edit);
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
                            console.log(sql1);
                            con.query(sql1 , (err1 , result1)=>{
                              console.log(err1);
                              con.commit()
                              res.sendStatus(200)
                          })



                    }
                  else
                    {
                      sql1 = "select max(cat_id) from somanath.categories"
                      con.query(sql1 , (err1 , result1)=>{
                              console.log(err1);
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
                                console.log(sql2 , err2);
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

                                                      if(sqlInputs.img_kan == "True")
                                                      {
                                                        newImageName = path.join(newDirectory , "kan."+photos[photoIndex].split(".")[1])
                                                        fs.renameSync(path.join(homeDir , "angadiImages" , String(photos[photoIndex])) , newImageName , (err)=>{})          
                                                        photoIndex += 1          
                                                        
                                                      }

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

                                    
                                                      sql2 = "insert into somanath.products values (" + String(ID) + ",'" + sqlInputs.prod_bar + "','"+ sqlInputs.prod_name + "','"+ sqlInputs.prod_cat + "','" + sqlInputs.prod_hsn + "','" + sqlInputs.prod_shelf + "','" +sqlInputs.prod_name_eng + "'," + sqlInputs.prod_min_qty + "," + sqlInputs.prod_expiry + "," + sqlInputs.prod_mrp + "," + sqlInputs.prod_mrp_old + ",'" + sqlInputs.prod_sup + "', (select tax_id from somanath.taxes where tax_type = 0 and tax_per = " + sqlInputs.prod_gst + ") , (select tax_id from somanath.taxes where tax_type = 1 and tax_per = " + sqlInputs.prod_cess + "),'" + sqlInputs.prod_unit_type +"','" + sqlInputs.nml_unit + "','"   + sqlInputs.htl_unit + "','"  + sqlInputs.spl_unit + "','"  + sqlInputs.ang_unit + "','False','" + sqlInputs.prod_desc + "','" + sqlInputs.img_kan + "','" + sqlInputs.img_high + "','" + sqlInputs.img_low +"','" + Time + "',(select user_id from somanath.users where user_name = '"+sqlInputs.user_name+"') , NULL , NULL)"
                                                      
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

                                            if(sqlInputs.img_kan == "True")
                                            {
                                              newImageName = path.join(newDirectory , "kan."+photos[photoIndex].split(".")[1])
                                              fs.renameSync(path.join(homeDir , "angadiImages" , String(photos[photoIndex])) , newImageName , (err)=>{})          
                                              photoIndex += 1          
                                              
                                            }

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

                                            sql2 = "update somanath.products set prod_bar = '" + sqlInputs.prod_bar + "', prod_name = '"+ sqlInputs.prod_name + "', prod_cat = '"+ sqlInputs.prod_cat + "', prod_hsn = '" + sqlInputs.prod_hsn + "', prod_shelf = '" + sqlInputs.prod_shelf + "',  prod_name_eng = '" +sqlInputs.prod_name_eng + "', prod_min_qty = " + sqlInputs.prod_min_qty + ", prod_expiry = " + sqlInputs.prod_expiry + ", prod_mrp = " + sqlInputs.prod_mrp + ", prod_mrp_old = " + sqlInputs.prod_mrp_old + ", prod_sup = '" + sqlInputs.prod_sup + "',  prod_gst =  (select tax_id from somanath.taxes where tax_type = 0 and tax_per = " + sqlInputs.prod_gst + ") , prod_cess = (select tax_id from somanath.taxes where tax_type = 1 and tax_per = " + sqlInputs.prod_cess + "), prod_unit_type = '" + sqlInputs.prod_unit_type +"', nml_unit = '" + sqlInputs.nml_unit + "', htl_unit = '"   + sqlInputs.htl_unit + "', spl_unit = '"  + sqlInputs.spl_unit + "',  ang_unit =  '"  + sqlInputs.ang_unit + "', prod_hide = '"+sqlInputs.prod_hide+"',prod_desc = '" + sqlInputs.prod_desc + "', kan_img = '" + sqlInputs.img_kan + "', high_img = '" + sqlInputs.img_high + "', low_img = '" + sqlInputs.img_low +"',update_time = '" + Time + "',update_id = (select user_id from somanath.users where user_name = '"+sqlInputs.user_name+"')  where prod_id = "+ ID
                                            console.log(sql2);
                                            con.query(sql2 , (err2 , result2)=>{
                                                  console.log(err2);
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
      console.log(err)
      res.send(result)
    })
})

app.get('/products/getSelectedProduct' , (req,res) => {
  sql = "select * from somanath.products where prod_id = " + req.query.prod_id

  con.query(sql , (err , result) =>{
    res.send(result)
    console.log(result);
  })    
})

app.post('/barcodes' , (req,res)=>{
  type = req.query['type']
  barcode = req.query['barcode']
  barcodeInUse.sort(function(a, b){return a-b});
  console.log(barcodeInUse);
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
                console.log(exist , barcodeInUse)
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
                console.log(exist , barcodeInUse)
                
              }
              console.log("get : " , barcodeInUse);
      }

    if(type == 'update')
      {
        exist = false
        bar =  parseInt(req.query['barcode'])
        barcodeInUse.forEach(element =>{
            if(element == bar)
              exist = true
        })
        console.log(exist , barcodeInUse)
        if(!exist)
          barcodeInUse.push(bar)
        console.log(barcodeInUse);
        res.sendStatus(200)
        console.log("update : " , barcodeInUse);
      }


    if(type == 'save')
      {
        barcodeInUse = barcodeInUse.filter(function(f) { return f != parseInt(barcode) })
        console.log(barcodeInUse);       
        max = true
        barcodeInUse.forEach(element => {
            if(barcode < element)
              max = false
        });

    
          
            
            sql1 = "update somanath.data set max_prod_bar = " + String(barcode)
            con.query(sql1 , (err1 , result1) => {
              if(max)
                {
                  barcodeInUse.push(parseInt(barcode))
                }

              res.sendStatus(200)
              console.log("save : " , barcodeInUse);
            })
          
      
      }
    
  })
})

//products done!!





//employs

app.post('/employs/save' , files.array('images', 1),(req,res) => {
  let sqlInputs = req.query
  console.log(sqlInputs);
  ID = sqlInputs['emp_id']
  edit = false
  sql = "select emp_name from somanath.employs where emp_name = '"+sqlInputs['emp_name']+"'"
  if(ID != '')
    {
      edit = true
      sql += " and emp_id != "+ ID
    }
    
    

          con.query(sql , (err , result)=>{
            console.log(err , result);
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
                            console.log(sql1);
                            con.query(sql1 , (err1 , result1)=>{
                              console.log(err1);
                              con.commit()
                              res.sendStatus(200)
                          })



                    }
                  else
                    {
                      sql1 = "select max(emp_id) from somanath.employs"
                      con.query(sql1 , (err1 , result1)=>{
                              console.log(err1);
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
                                console.log(sql2 , err2);
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
    console.log(result);
  })    
})


//employs Done!!









//accounts
app.post('/accounts/save' , files.array('images' , 3) , (req,res) =>{
  let sqlInputs = req.query  
  ID = sqlInputs['acc_id']
  edit = false
  sql = "select acc_name from somanath.accounts where (acc_name = '"+sqlInputs.acc_name+"'"
      if (sqlInputs.acc_gstin != "")
        sql += " or acc_gstin = '"+sqlInputs.acc_gstin+"'"
  sql += ")"
  if(ID != '')
    {
      sql += " and acc_id !="+ ID
      edit = true
    }  
    console.log(sql);
    con.query(sql , (err1 , result1) => {
                          console.log(err1 , result1);
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
                                                    console.log(result1);
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

                                  
                                                                                                                                                                                                      //acc_id, acc_type, acc_name, acc_email, acc_add, acc_mob1, acc_mob2, acc_gstin, acc_accno, acc_ifsc, acc_cus_type, acc_img, insert_time, insert_id, update_time, update_id
                                                    sql2 = "insert into somanath.accounts values (" + String(ID) + ",'" + sqlInputs.acc_type + "','"+ sqlInputs.acc_name + "','"+ sqlInputs.acc_email + "','" + sqlInputs.acc_add + "','" + sqlInputs.acc_mob1+ "','" + sqlInputs.acc_mob2+ "','" + sqlInputs.acc_gstin+ "','" + sqlInputs.acc_accno+ "','" + sqlInputs.acc_ifsc+ "','" + sqlInputs.acc_cus_type + "','" +sqlInputs.acc_img+"','" + Time + "',(select user_id from somanath.users where user_name = '"+sqlInputs.user_name+"'),NULL,NULL)"
                                                    console.log(sql2);
                                                    con.query(sql2 , (err2 , result2)=>{
                                                          console.log(err2);
                                                          con.commit()
                                                          res.sendStatus(200)
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
                                                console.log(sql2);
                                                con.query(sql2 , (err2 , result2)=>{
                                                  console.log(err2);
                                                  con.commit()
                                                  res.sendStatus(200)
                                              })

                                          }
                                  
                            }


        })

})

app.get('/accounts/getAccList' , (req , res )=>{
  
  sql = req.query['sql']
  console.log(req.query['tax_check'])
  if (req.query['tax_check'] == "True")
    sql = "SELECT acc_id,acc_name,acc_type FROM somanath.accounts where acc_id not in (select acc_id from somanath.accounts where acc_type = 'SUPP' and acc_gstin = '') order by acc_type , acc_name"
  

  
  console.log(sql);
  

  con.query(sql , (err , result)=>{
    res.send(result)
  })
})

app.get('/accounts/getSelectedAcc' , (req,res) => {
  sql = "select * from somanath.accounts where acc_id = " + req.query.acc_id

  con.query(sql , (err , result) =>{

    res.send(result)
    console.log(result);
  })    
})


app.listen(6000)
