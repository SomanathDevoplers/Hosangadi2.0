const systemOs = "ubuntu"
const io = require('socket.io-client')
const socket = io.connect('http://192.168.1.35:5000')
const app = require('express')()
const mysql = require('mysql') 
const multer = require('multer')
const fs = require('fs')
const mv = require('mv')
const { homedir } = require('os');
const homeDir = require('os').homedir()
let photos = []
const con = mysql.createConnection({
  host: "localhost",
  port: "3306",
  user: "root",
  password: "mysqlpassword5"
});

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
      cb(null , homedir + "\\angadiImages")
  },

  filename: function (req, file, cb) {
    fileName = Math.floor(Math.random()*100) +  file.originalname
    photos.push(fileName)
    cb(null, fileName)
  }
  
})

const files = multer({storage : storage})

//server initialization with database connection
//global variables declaration

//gloabl variables declaration end




app.post('/firms/newSave' , files.array('images', 3),(req,res) => {
      
      let sqlInputs = req.query

      let sql = "select max(firm_id) from somanath.firms"
      
      con.query(sql , (err , result)=>{
        if (result == null)
          maxId = 1
        else
          maxId = result[0]['max(firm_id)']+1

      console.log(homeDir + "\\angadiImages\\firms\\" + maxId  , homeDir + "\\angadiImages\\" + photos[0] , homeDir + "\\angadiImages\\firms\\" + maxId + );
      //fs.mkdir(homeDir + "\\angadiImages\\firms\\" + maxId , ()=>{})

      //if(sqlInputs['firm_qr'])
      //    mv(homeDir + "\\angadiImages\\" + photos[0] , homeDir + "\\angadiImages\\firms\\" + maxId  , ()=>{})


      res.sendStatus(200)
      console.log("response sent");

      })    
});


app.listen(6000)

