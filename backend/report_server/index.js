const io = require('socket.io-client');
const socket = io.connect('http://192.168.1.35:5000');
const app = require('express')()
const mysql = require('mysql'); 
const file = require('multer')()
const con = mysql.createConnection({
  host: "localhost",
  port: "3306",
  user: "root",
  password: "mysqlpassword5"
});
//server initialization with database connection
//global variables declaration
const systemOs = "ubuntu"
//gloabl variables declaration end
console.log(systemOs);

app.post('/firms/newSave' , file.array(),(req,res) => {
      
      res.sendStatus(200)
      console.log(req);
});


app.listen(6000)

