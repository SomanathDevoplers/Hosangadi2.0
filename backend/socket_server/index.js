const http = require('http');
const express = require('express');
const app = express();
const server = http.createServer(app);
const io = require('socket.io')(server)
const mysql = require('mysql'); 
const { time } = require('console');
const { exit } = require('process');

const con = mysql.createConnection({
  host: "localhost",
  port: "3306",
  user: "root",
  password: "mysqlpassword5"
});

con.connect()


//server initialization with database connection
//global variables start

let usersLogged = []
let sbOpened = {}
let pbOpened = {}
const systemOs = "ubuntu"

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


//global variables end
   


io.on('connection', function (socket) {
    //connection event starts here
    //adds data to usersLogged when login is approved

    
    
    clientIp = socket.handshake.address

    console.log()
    //all the params passed pushed to usersLogged
    socketData = socket.handshake.headers
    usersLogged.push({"ip" : clientIp , "userName" : socketData['user_name'] , "userType": socketData['user_type'] , "loggedInAt":getTime()})

    console.log(usersLogged);
    //connection evenrt ends here

    //root window disconnect event
          socket.on('disconnect' , (data)=> {
                  socketData = socket.handshake.headers

                  

                  for (user = 0 ; user<usersLogged.length ; user ++)
                      {
                          console.log(usersLogged[user]);
                          if(usersLogged[user].ip == socket.handshake.address)
                            usersLogged.splice(user , 1)
                      }
                    
          });   
    //root window disconnect event ends here

          


})

app.get('/login' , (req,res) => {                                                                                                          //for user login authentication
  sql = "select user_type from somanath.users where user_name = '"+ req.query.user_name + "' and user_pass = '"+req.query.user_pass+"'"
  responseSent = false
  
  console.log(req.query.user_name);

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



server.listen(5000);