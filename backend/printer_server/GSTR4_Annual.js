// used for testing only
const homeDir = require('os').homedir()
XLSX = require('xlsx')
var MySql = require('sync-mysql');

var connection = new MySql({
    host: "localhost",
    port: "3306",
    user: "root",
    password: "mysqlpassword5",
    multipleStatements : true
  
});

let data = {}
let dataCess = {}
sql = "SELECT pur_id,pur_acc,pur_prod_id,pur_prod_qty FROM somanath2022.purchases where pur_firm_id = 3 and pur_date >= '2022-04-01' and pur_date<='2023-03-31'"
purchase =connection.query(sql)
try{
    purchase1 =connection.query("SELECT pur_id,pur_acc,pur_prod_id,pur_prod_qty FROM somanath2023.purchases where pur_firm_id = 3 and and pur_date >= '2022-04-01' and pur_date<='2023-03-31'")
    purchase = purchase.concat(purchase1)
}
catch{

}
for(i=0;i<purchase.length;i++){
    rateWise = {}
    rateWiseCess = {}
    a = data[purchase[i]['pur_acc']]
    if (typeof a !== 'undefined'){
        prodId = purchase[i]['pur_prod_id'].split(":").slice(1,-1)
        prodQty = purchase[i]['pur_prod_qty'].split(":").slice(1,-1)
        for(j=0;j<prodId.length;j++){
            cp  = connection.query("SELECT stk_cost FROM somanath2022.stocks where stk_pur_id='"+purchase[i]['pur_id']+"'and stk_prod_id ="+prodId[j])[0]['stk_cost']
            gstCessId = connection.query("SELECT prod_gst,prod_cess FROM somanath.products where prod_id ="+prodId[j])[0]
            gst = connection.query("SELECT tax_per FROM somanath.taxes where tax_id ="+gstCessId['prod_gst'])[0]['tax_per']
            cess = connection.query("SELECT tax_per FROM somanath.taxes where tax_id ="+gstCessId['prod_cess'])[0]['tax_per']
            totalValue = cp * prodQty[j]
            rateWise = a
            let y = rateWise[gst]
            if (typeof y !== 'undefined'){
                if(cess>0){
                    totalValue = (totalValue/(1+((gst+cess)/100)))*(1+(gst/100))
                }
                totalValue = totalValue + y
                rateWise[gst] = totalValue
                data[purchase[i]['pur_acc']] = rateWise
            }
            else{
                if(cess>0){
                    totalValue = (totalValue/(1+((gst+cess)/100)))*(1+(gst/100))
                }
                rateWise[gst]=totalValue
                data[purchase[i]['pur_acc']] = rateWise
            }
            if(cess>0){
                let c = rateWiseCess[cess]
                if (typeof c !== 'undefined'){
                    rateWiseCess[cess] =(cp * prodQty[j])/(1+((gst+cess)/100)) +c
                    dataCess[purchase[i]['pur_acc']] = rateWiseCess
                }
                else{
                    rateWiseCess[cess]=(cp * prodQty[j])/(1+((gst+cess)/100))
                    dataCess[purchase[i]['pur_acc']] = rateWiseCess
                }
            }
        }
        
    }
    else{
        prodId = purchase[i]['pur_prod_id'].split(":").slice(1,-1)
        prodQty = purchase[i]['pur_prod_qty'].split(":").slice(1,-1)
        for(j=0;j<prodId.length;j++){
            cp  = connection.query("SELECT stk_cost FROM somanath2022.stocks where stk_pur_id='"+purchase[i]['pur_id']+"'and stk_prod_id ="+prodId[j])[0]['stk_cost']
            gstCessId = connection.query("SELECT prod_gst,prod_cess FROM somanath.products where prod_id ="+prodId[j])[0]
            gst = connection.query("SELECT tax_per FROM somanath.taxes where tax_id ="+gstCessId['prod_gst'])[0]['tax_per']
            cess = connection.query("SELECT tax_per FROM somanath.taxes where tax_id ="+gstCessId['prod_cess'])[0]['tax_per']
            totalValue = cp * prodQty[j]
            let y = rateWise[gst]
            if (typeof y !== 'undefined'){
                if(cess>0){
                    totalValue = (totalValue/(1+((gst+cess)/100)))*(1+(gst/100))
                }
                totalValue = totalValue + y
                rateWise[gst] = totalValue
                data[purchase[i]['pur_acc']] = rateWise
            }
            else{
                if(cess>0){
                    totalValue = (totalValue/(1+((gst+cess)/100)))*(1+(gst/100))
                }
                rateWise[gst]=totalValue
                data[purchase[i]['pur_acc']] = rateWise
            }
            if(cess>0){
                let c = rateWiseCess[cess]
                if (typeof c !== 'undefined'){
                    rateWiseCess[cess] = (cp * prodQty[j])/(1+((gst+cess)/100))+c
                    dataCess[purchase[i]['pur_acc']] = rateWiseCess
                }
                else{
                    rateWiseCess[cess]=(cp * prodQty[j])/(1+((gst+cess)/100))
                    dataCess[purchase[i]['pur_acc']] = rateWiseCess
                }
            }
        }
    }
}


let worksheets = {}
worksheets['Sheet1'] = {
    '!ref': 'A1:L1',
    A1: {
      t: 's',
      v: 'GSTIN of supplier *',
      h: 'GSTIN of supplier *',
      w: 'GSTIN of supplier *'
    },
    B1: {
      t: 's',
      v: 'Place of supply *',
      h: 'Place of supply *',
      w: 'Place of supply *'
    },
    C1: {
      t: 's',
      v: 'Supply type *',
      h: 'Supply type *',
      w: 'Supply type *'
    },
    D1: {
      t: 's',
      v: 'Taxable value (₹) *',
      h: 'Taxable value (₹) *',
      w: 'Taxable value (₹) *'
    },
    E1: { t: 's', v: 'Rate*', h: 'Rate*', w: 'Rate*' },
    F1: {
      t: 's',
      v: 'Integrated tax (₹)',
      h: 'Integrated tax (₹)',
      w: 'Integrated tax (₹)'
    },
    G1: {
      t: 's',
      v: 'Central tax (₹)',
      h: 'Central tax (₹)',
      w: 'Central tax (₹)'
    },
    H1: {
      t: 's',
      v: 'State/UT tax (₹)',
      h: 'State/UT tax (₹)',
      w: 'State/UT tax (₹)'
    },
    I1: { t: 's', v: 'Cess (₹)', h: 'Cess (₹)', w: 'Cess (₹)' },
    J1: { t: 's', v: 'Action*', h: 'Action*', w: 'Action*' },
    L1: { t: 's', v: 'Suplier Name', h: 'Suplier Name', w: 'Suplier Name' }
}
let rows = 1
Object.keys(data).forEach(supId => {

    supInfo = connection.query("SELECT acc_name,acc_gstin FROM somanath.accounts where acc_id = "+supId)
    Object.keys(data[supId]).forEach(rates=>{
        rows++
        Taxable = data[supId][rates]/(1+(rates/100))
        tax = (data[supId][rates] - Taxable )/2
        let Cess = 0
        if(rates==28){
            q = dataCess[supId]
            if (typeof q !== 'undefined'){
                Object.keys(q).forEach(cessrates=>{
                    Cess = Cess +(q[cessrates]*((1+(cessrates/100))-1))
                })
            }
        }
        worksheets['Sheet1']['A'+rows] = { t: 's', v: supInfo[0]["acc_gstin"], h: supInfo[0]["acc_gstin"], w: supInfo[0]["acc_gstin"]}
        worksheets['Sheet1']['B'+rows] = { t: 's', v: '29-Karnataka', h: '29-Karnataka', w: '29-Karnataka'}
        worksheets['Sheet1']['C'+rows] = { t: 's', v: 'Intra-State', h: 'Intra-State', w: 'Intra-State'}
        worksheets['Sheet1']['D'+rows] = { t: 's', v: Taxable.toFixed(2), h: Taxable.toFixed(2), w: Taxable.toFixed(2)}
        worksheets['Sheet1']['E'+rows] = { t: 's', v: rates, h: rates, w: rates }
        worksheets['Sheet1']['F'+rows] = { t: 's', v: 0, h: 0, w: 0}
        worksheets['Sheet1']['G'+rows] = { t: 's', v: tax.toFixed(2), h: tax.toFixed(2), w: tax.toFixed(2)}
        worksheets['Sheet1']['H'+rows] = { t: 's', v: tax.toFixed(2), h: tax.toFixed(2), w: tax.toFixed(2)}
        worksheets['Sheet1']['I'+rows] =  { t: 's', v: Cess.toFixed(2), h: Cess.toFixed(2), w: Cess.toFixed(2) },
        worksheets['Sheet1']['J'+rows] = { t: 's', v: 'Add', h: 'Add', w: 'Add' }
        worksheets['Sheet1']['L'+rows] = { t: 's', v: supInfo[0]['acc_name'], h: supInfo[0]['acc_name'], w: supInfo[0]['acc_name'] }
        worksheets['Sheet1']['!ref']   = 'A1:L'+rows
    })
     
});

const newBook = XLSX.utils.book_new();
XLSX.utils.book_append_sheet(newBook, worksheets['Sheet1'], "Sheet1");
XLSX.writeFileSync(newBook,"NGSTR4.xlsx");
