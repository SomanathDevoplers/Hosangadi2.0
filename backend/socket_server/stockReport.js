// not used anywhere under progress
const express = require('express');
const app = express();
const MySql = require('sync-mysql');
const mysql = require('mysql'); 

const connection = new MySql({
  host: "localhost",
  port: "3306",
  user: "root",
  password: "mysqlpassword5",
  multipleStatements : true
});

  

// let con = mysql.createConnection({
//   host: "localhost",
//   port: "3306",
//   user: "root",
//   password: "mysqlpassword5",
//   multipleStatements : true
// });

// con.connect()
let con = mysql.createPool({
    connectionLimit : 50,
    host: "localhost",
    port: "3306",
    user: "root",
    password: "mysqlpassword5",
    multipleStatements : true,
    debug: false
  });

dict = {}
inwardsTotal = 0
outwardsTotal = 0
n = 5
topSales = []
topProdIds = []
for(i=0;i<n;i++)
{
    topSales.push([0,0])
    topProdIds.push(0)
}

sql = 'SELECT pur_id,pur_prod_id,pur_prod_qty FROM somanath2021.purchases where pur_firm_id = 1 and pur_date >="2022-02-01" and pur_date<="2022-02-28"'
con.query(sql,(err,result)=>{
    console.log(err);
    for(i=0;i<result.length;i++)
    {
        stocks = connection.query("SELECT stk_prod_id,stk_cost,stk_tot_qty FROM somanath2021.stocks where stk_firm_id = 1 and stk_pur_id ='"+ result[i]['pur_id']+"'")
        prodIDs = result[i]['pur_prod_id'].split(':').slice(1,-1)
        qtys = result[i]['pur_prod_qty'].split(':').slice(1,-1)
        for(j=0;j<prodIDs.length;j++)
        {
            qty = parseFloat(qtys[j])
            cp = parseFloat(stocks[j]['stk_cost'])
            inwardsTotal += qty*cp
            if( prodIDs[j] in dict)
            {
                dict[prodIDs[j]] = [dict[prodIDs[j]][0]+(qty*cp), dict[prodIDs[j]][1], 0]
            }
            else
            {
                dict[prodIDs[j]] = [ qty*cp, stocks[j]['stk_tot_qty'],  0]
            }
        }
    }
    sql1= "SELECT sales_prod_id,sales_prod_qty,sales_prod_sp FROM somanath2021.sales where sales_ref regexp 'SSM' and sale_date >= '2022-02-01' and sale_date<= '2022-02-28'"
    con.query(sql1,(err1,result1)=>{
        
        for(i=0;i<result1.length;i++)
        {
            prodIDs = result1[i]['sales_prod_id'].split(':').slice(1,-1)
            qtys = result1[i]['sales_prod_qty'].split(':').slice(1,-1)
            sps = result1[i]['sales_prod_sp'].split(':').slice(1,-1)
            for(j=0;j<prodIDs.length;j++)
            {
                qty = parseFloat(qtys[j])
                sp = parseFloat(sps[j])
                x = sp*qty
                outwardsTotal += x
                if( prodIDs[j] in dict  )
                {
                    dict[prodIDs[j]] = [  dict[prodIDs[j]][0], dict[prodIDs[j]][1], dict[prodIDs[j]][2] + (x) ]
                }
                else
                {
                    dict[prodIDs[j]] = [ 0, 0, x ]
                }
            }
            
        }

        Object.keys(dict).forEach(prodIDs => {
            if(dict[prodIDs][2] > topSales[4][0])
        {
            topSales[4] = [dict[prodIDs][2],parseInt(prodIDs),dict[prodIDs][0],dict[prodIDs][1] ]
            topSales =  topSales.sort(function(a, b){return b[0]-a[0]});
        }
        });
        topSales =  topSales.sort(function(a, b){return a[1]-b[1]});
        prodids = ''
        for (i = 0; i< topSales.length; i++) {
            topSales[i].push(connection.query("SELECT prod_name FROM somanath.products where prod_id ="+topSales[i][1])[0]['prod_name'])
            prodids +=  topSales[i][1] +','
        }
        
        sql3 = 'SELECT distinct(stk_prod_id),stk_tot_qty FROM somanath2021.stocks where stk_prod_id in ('+prodids.slice(0,-1) +') order by stk_prod_id' 
        con.query(sql3,(err3,result3)=>{
            for(i=0;i<result3.length;i++)
            {
               topSales[i] = [  topSales[i][4], result3[i]['stk_tot_qty'], topSales[i][2],topSales[i][0],topSales[i][3] ]
            }
            topSales =  topSales.sort(function(a, b){return b[3]-a[3]});
            console.log(topSales);
        })
    
    })

})

