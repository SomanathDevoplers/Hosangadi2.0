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
    socketData = socket.handshake.headers
    if(socketData.host[0] == "l")
      socketData.host = socketData.host.replace("localhost","127.0.0.1")
    usersLogged.push({"ip" : socketData['host'] , "userName" : socketData['user_name'] , "userType": socketData['user_type'] , "loggedInAt":getTime()})
    console.log(usersLogged);
    //connection evenrt ends here

    //root window disconnect event
          socket.on('disconnect' , (data)=> {
                  socketData = socket.handshake.headers

                  if(socketData.host[0] == "l")
                      socketData.host = socketData.host.replace("localhost","127.0.0.1")

                  for (user = 0 ; user<usersLogged.length ; user ++)
                      {
                          console.log(usersLogged[user]);
                          if(usersLogged[user].ip == socketData.host)
                            usersLogged.splice(user , 1)
                      }
                    
                  console.log(usersLogged)
          });   
    //root window disconnect event ends here

          


})

app.get('/login' , (req,res) => {                                                                                                          //for user login authentication
  sql = "select user_type from somanath.users where user_name = '"+ req.query.user_name + "' and user_pass = '"+req.query.user_pass+"'"
  responseSent = false
  
  usersLogged.forEach( user => {
      if(user.ip == req.headers.host)
          responseSent = true
          res.sendStatus(101)
          return
    });                                                                                                                                      //checks if same two clients are from same ip
                                                                                                                                           //responds {"NOT FOUND"}
  if(!responseSent)
        con.query(sql, (err , userType)=>{
          res.send(userType)
        });  
                                                                                                                                       //returns null when not found else returns {""}
});



server.listen(5000);