// to pdf to print only support windows not ubuntu
//const io = require('socket.io-client')
//const socket = io.connect('http://'+ip+':5000')
const print = require("pdf-to-printer");
const express = require('express')
const app = express()
const homeDir = require('os').homedir()
const {writeFileSync , readFileSync , unlink} = require ("fs");
const PDFDocument = require("pdfkit"); 
XLSX = require('xlsx')
var MySql = require('sync-mysql');
const mysql = require('mysql');
const io = require('socket.io-client')
socket = io.connect('http://localhost:5000')
const process = require('process');
const multer = require('multer')
const path = require('path');




const storage = multer.diskStorage({
  destination: function (req, file, cb) {
      cb(null , homeDir )  
  },

  filename: function (req, file, cb) {
    cb(null, "invoice.pdf")
  }
  
})

const invoiceDataStorage = multer.diskStorage({
  destination: function (req, file, cb) {
      cb(null , homeDir )  
  },

  filename: function (req, file, cb) {
    originalName = file.originalname.split(".")
    fileName1 = "invoiceData"+Math.floor(Math.random()*100) + "." + originalName.slice(-1)
    cb(null, fileName1)
  }
  
})

const files = multer({storage : storage})
const invoiceDataFiles = multer({storage : invoiceDataStorage})

let con = mysql.createConnection({
  host: "localhost",
  port: "3306",
  user: "root",
  password: "#mysqlpassword5",
  multipleStatements : true
});

var connection = new MySql({
  host: "localhost",
  port: "3306",
  user: "root",
  password: "#mysqlpassword5",
  multipleStatements : true
});

function Invoice(BillNumber, Date, customerName, InvoiceData, BillTotal, old_bal,oldBalData,page, res,gst){
  if(page == 0)
  {
    if( gst === 'True')
    {
      //GST INVOICE
      let doc = new PDFDocument({ size: 'A6', margins: {
        top: 3,
        bottom: 3,
        left: 10,
        right:5
      }
      });
    doc.pipe(res);
    const totItems = Object.keys(InvoiceData)
    enterprices = {}
    stores = {}
    let totalStores = 0
    let totalEnterprices = 0
    for (let i =0 ;i<totItems.length;i++)
    {
      if(InvoiceData[totItems[i]][6].split('_')[0]==="SEM")
        enterprices[totItems[i]] = InvoiceData[totItems[i]]
      else
        stores[totItems[i]] = InvoiceData[totItems[i]]
    }
    let position = 0
    if(Object.keys(stores).length>0)
    {
      const prodName = Object.keys(stores)
       doc
          .fontSize(14)
          .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-Regular.ttf'))
          .text('ಸೋಮನಾಥ ಸ್ಟೋರ್ಸ್', {align: 'center'})
      doc 
          .fontSize(10)
          .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-Regular.ttf'))
          .text('ಮರವಂತೆ - ೫೭೬೨೨೪',105,20 )
      doc
          .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','Work_Sans','static','WorkSans-Regular.ttf'))
          .fontSize(8)
          .text('GST%',100,66)
          .fontSize(11)
          .text('MRP',110, 66,{ width: 50, align: "right" })
          .fontSize(9)
          .text('GST : 29ATBPS7012G1ZN',10,35 )
          .text('Mob  : 9902664717',10,45)
          .text(`Bill No: ${stores[prodName[prodName.length - 1]][6]}`,175,35)
          .text(`${Date}`,190,45)
          .fontSize(10)
          .text(`To    : ${customerName}`,10,55)
      doc
          .moveTo(5, 66)
          .lineTo(295,65)
          .stroke()
          .moveTo(5, 82)
          .lineTo(295,82)
          .stroke();
      doc
          .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-Light.ttf'))
          .fontSize(12)
          .text('ವಿವರಗಳು',30,66 )
          .text('ದರ',145,66,{ width: 50, align: "right" })
          .text('ಪ್ರಮಾಣ',195,66, { width: 50, align: "right" })
          .text('ಮೊತ್ತ',0,66,{ align: "right" })
          .text()
          
          let pageTop = 62
          
          let count = 0
          let maxPage = 385
          let numberOfItems = prodName.length
          let saved = 0
          //Show old Balance
          if(old_bal && numberOfItems > 18) maxPage = 365
          let mrp
          let gstValues = {}
          let arr
          for (let i = 0; i < numberOfItems; i++) {
            count += 1
            position = pageTop + ((count + 1) * 10);//gap between rows 
            if (stores[prodName[i]][0] != 0){
              mrp = (stores[prodName[i]][0]).toFixed(1)
              saved += (stores[prodName[i]][0] - stores[prodName[i]][1])*stores[prodName[i]][2]
            }
            else
              mrp = ''
            if(stores[prodName[i]][4]==''){
              x = position
              doc
                .fontSize(8.5)
                .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','Work_Sans','static','WorkSans-Regular.ttf'))
                .text(prodName[i].slice(0,18),5, x )
                .text(stores[prodName[i]][5]+"%",105,x)
                .text(mrp, 110, x,{ width: 50, align: "right" })
                .text((stores[prodName[i]][1]).toFixed(1), 145, x, { width: 50, align: "right" })
                .text((stores[prodName[i]][2]).toFixed(3) , 195, x, { width: 50, align: "right" })
                .text((stores[prodName[i]][3]).toFixed(2), 0, x, { align: "right" });
                prodTotal = parseFloat(stores[prodName[i]][3])
                totalStores = totalStores+prodTotal
                gstRate = stores[prodName[i]][5]
                arr = gstValues[String(gstRate)]
                try{
                  arr[0]
                }catch{
                  arr = [0,0]
                }
                gstValues[String(gstRate)] = [ arr[0]+(prodTotal/(1+(gstRate/100))) , arr[1]+( prodTotal - ( prodTotal / (1 + (gstRate/100) ) ) ) ]
            }
            else
            {
              doc
              .fontSize(8.5)
              .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-Regular.ttf'))
              .text(stores[prodName[i]][4].slice(0,23),5, position)
              .text(stores[prodName[i]][5]+"%",105,position)
              .text(mrp, 110, position,{ width: 50, align: "right" })
              .text((stores[prodName[i]][1]).toFixed(1), 145, position, { width: 50, align: "right" })
              .text((stores[prodName[i]][2]).toFixed(3) , 195, position, { width: 50, align: "right" })
              .text((stores[prodName[i]][3]).toFixed(2), 0, position, { align: "right" });
              prodTotal = parseFloat(stores[prodName[i]][3])
              totalStores = totalStores+parseFloat(stores[prodName[i]][3])
              gstRate = stores[prodName[i]][5]
              arr = gstValues[String(gstRate)]
              try{
                arr[0]
              }catch{
                arr = [0,0]
              }
              gstValues[String(gstRate)] = [ arr[0]+(prodTotal/(1+(gstRate/100))) , arr[1]+( prodTotal - ( prodTotal / (1 + (gstRate/100) ) ) ) ]
            }

            if(position > maxPage )
              {
                  doc.addPage({size: "A6",margins: {
                      top: 0,
                      bottom: 0,
                      left: 10,
                      right:5
                    }})
                  count = 0
                  pageTop = -15
                  position = 0
              }
          }
      doc
          .moveTo(5, position+15)
          .lineTo(295,position+15)
          .stroke();
      doc
          .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-Regular.ttf'))
          .text(`ಒಟ್ಟು : ₹ ${Math.round(Number(totalStores)).toFixed(2)}`,0,position+20,{ align: "right" })
          doc
          .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','Work_Sans','static','WorkSans-Regular.ttf'))
          .fontSize(8)
          .text('GST%',10,position+35)
          .text('Taxable Amount',40,position+35)
          .text('CGST',130,position+35)
          .text('SGST',180,position+35)
          .text('CESS',230,position+35)
          .text('Total Tax',0,position+35,{ align: "right" })
      gstRate = Object.keys(gstValues)
      x = 35
      totalTaxable = 0
      totalGST = 0
      for(let i=0;i<gstRate.length;i++)
        {
          x +=10 
        doc
          .text(gstRate[i]+"%",13,position+x)
          .text((gstValues[gstRate[i]][0]).toFixed(2),65,position+x)
          .text(((gstValues[gstRate[i]][1])/2).toFixed(2),130,position+x)
          .text(((gstValues[gstRate[i]][1])/2).toFixed(2),180,position+x)
          .text('-',240,position+x)
          .text((gstValues[gstRate[i]][1]).toFixed(2),0,position+x,{ align: "right" })
          totalGST = (gstValues[gstRate[i]][1])/2 + totalGST
          totalTaxable = gstValues[gstRate[i]][0] + totalTaxable
        }
        x +=10
        doc
          .text('Total',13,position+x)
          .text((totalTaxable).toFixed(2),65,position+x)
          .text((totalGST).toFixed(2),130,position+x)
          .text((totalGST).toFixed(2),180,position+x)
          .text('-',240,position+x)
          .text((totalGST*2).toFixed(2),0,position+x,{ align: "right" })

      if(saved>1){
        position = position + 10
        doc 
          .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','Work_Sans','static','WorkSans-Regular.ttf'))
          .text(`You have Saved Rs.${saved.toFixed(2)} on MRP`,{align:"center"})
      }

      doc .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-Regular.ttf'))
          .text("ನಮ್ಮೊಂದಿಗೆ ವ್ಯವಹರಿಸಿದಕ್ಕೆ ಧನ್ಯವಾದಗಳು. ಮತ್ತೆ ಬನ್ನಿ",{align:"center"})
          position = position + 50
    }
    
    if(Object.keys(enterprices).length>0)
    {
      position = 0
      if(Object.keys(stores).length>0){
        doc.addPage({size: "A6",margins: {
          top: 0,
          bottom: 0,
          left: 10,
          right:5
        }})
      }
      const prodName = Object.keys(enterprices)
      doc
          .fontSize(14)
          .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-Regular.ttf'))
          .text('ಸೋಮನಾಥ ಎಂಟರ್ಪ್ರೈಸಸ್', {align: 'center'})
      doc 
          .fontSize(10)
          .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-Regular.ttf'))
          .text('ಮರವಂತೆ - ೫೭೬೨೨೪',105,20 )
      doc
          .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','Work_Sans','static','WorkSans-Regular.ttf'))
          .fontSize(11)
          .text('MRP',110, 66,{ width: 50, align: "right" })
          .fontSize(9)
          .text('GST : 29BHSPS5551A1ZM',10,35 )
          .text('Mob  : 9611029582',10,45)
          .text(`Bill No: ${enterprices[prodName[0]][6]}`,190,35)
          .text(`${Date}`,190,45)
          .fontSize(10)
          .text(`To    : ${customerName}`,10,55)
      doc
          .moveTo(5, 66)
          .lineTo(295,65)
          .stroke()
          .moveTo(5, 82)
          .lineTo(295,82)
          .stroke();
      doc
          .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-Light.ttf'))
          .fontSize(12)
          .text('ವಿವರಗಳು',30,66 )
          .text('ದರ',145,66,{ width: 50, align: "right" })
          .text('ಪ್ರಮಾಣ',195,66, { width: 50, align: "right" })
          .text('ಮೊತ್ತ',0,66,{ align: "right" })
          .text()
          
          let pageTop = 62
          
          let count = 0
          let maxPage = 385
          let numberOfItems = prodName.length
          let saved = 0
          //Show old Balance
          if(old_bal && numberOfItems > 18) maxPage = 365
          let mrp
          for (let i = 0; i < numberOfItems; i++) {
            count += 1
            position = pageTop + ((count + 1) * 10);//gap between rows 
            if (enterprices[prodName[i]][0] != 0){
              mrp = (enterprices[prodName[i]][0]).toFixed(1)
              saved += (enterprices[prodName[i]][0] - enterprices[prodName[i]][1])*enterprices[prodName[i]][2]
            }
            else
              mrp = ''
            if(enterprices[prodName[i]][4]==''){
              x = position
              doc
                .fontSize(8.5)
                .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','Work_Sans','static','WorkSans-Regular.ttf'))
                .text(prodName[i].slice(0,23),5, x )
                .text(mrp, 110, x,{ width: 50, align: "right" })
                .text((enterprices[prodName[i]][1]).toFixed(1), 145, x, { width: 50, align: "right" })
                .text((enterprices[prodName[i]][2]).toFixed(3) , 195, x, { width: 50, align: "right" })
                .text((enterprices[prodName[i]][3]).toFixed(2), 0, x, { align: "right" });
                prodTotal = parseFloat(enterprices[prodName[i]][3])
                totalEnterprices = totalEnterprices+prodTotal
            }
            else{
            doc
            .fontSize(8.5)
            .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-Regular.ttf'))
            .text(enterprices[prodName[i]][4].slice(0,23),5, position)
            .text(mrp, 110, position,{ width: 50, align: "right" })
            .text((enterprices[prodName[i]][1]).toFixed(1), 145, position, { width: 50, align: "right" })
            .text((enterprices[prodName[i]][2]).toFixed(3) , 195, position, { width: 50, align: "right" })
            .text((enterprices[prodName[i]][3]).toFixed(2), 0, position, { align: "right" });
            prodTotal = parseFloat(enterprices[prodName[i]][3])
            totalEnterprices = totalEnterprices+prodTotal
            }
            
            if(position > maxPage )
              {
                  doc.addPage({size: "A6",margins: {
                      top: 0,
                      bottom: 0,
                      left: 10,
                      right:5
                    }})
                  count = 0
                  pageTop = -15
                  position = 0
              }
          }
      doc
          .moveTo(5, position+15)
          .lineTo(295,position+15)
          .stroke();
      doc
          .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-Regular.ttf'))
          .text(`ಒಟ್ಟು : ₹ ${Math.round(Number(totalEnterprices)).toFixed(2)}`,0,position+20,{ align: "right" })

      if(saved>1){
        position = position + 10
        doc
          .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','Work_Sans','static','WorkSans-Regular.ttf'))
          .text(`You have Saved Rs.${saved.toFixed(2)} on MRP`,{align:"center"})
      }
      doc .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-Regular.ttf'))
          .text("ನಮ್ಮೊಂದಿಗೆ ವ್ಯವಹರಿಸಿದಕ್ಕೆ ಧನ್ಯವಾದಗಳು. ಮತ್ತೆ ಬನ್ನಿ",{align:"center"})
          .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','Work_Sans','static','WorkSans-Regular.ttf'))
          .text("Composition tax payer not allowed to collect tax.",{align:"center"})
    }
    if(old_bal === 'True'){
      doc
          .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-Regular.ttf'))
          .text(`ಒಟ್ಟು : ₹ ${Math.round(Number(BillTotal)).toFixed(2)}`,0,position+60,{ align: "right" })
          .text(`ಹಳೆ ಬಾಕಿ : ₹ ${Math.round(Number(oldBalData['old_bal'])).toFixed(2)}`,10,position+60,{ align: "left" })
          .text(`ಜಮಾ      : ₹ ${Math.round(Number(oldBalData['amountPaid'])).toFixed(2)}`,10,position+80,{ align: "left" })
          .text(`ಉಳಿದ ಬಾಕಿ : ₹ ${Math.round(Number(oldBalData['remaining_bal'])).toFixed(2)}`,0,position+80,{ align: "right" })
      }
    doc.end();
    }
  else
    {
      let doc = new PDFDocument({ size: 'A6', margins: {
        top: 3,
        bottom: 3,
        left: 10,
        right:5
      }
      });
    doc.pipe(res);
    doc
        .fontSize(14)
        .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-Regular.ttf'))
        .text('ಸೋಮನಾಥ ಸ್ಟೋರ್ಸ್', {align: 'center'})
    doc 
        .fontSize(10)
        .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-Regular.ttf'))
        .text('ಮರವಂತೆ - ೫೭೬೨೨೪',105,20 )
    doc
        .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','Work_Sans','static','WorkSans-Regular.ttf'))
        .fontSize(11)
        .text('MRP',110, 66,{ width: 50, align: "right" })
        .fontSize(9)
        .text('GST : 29ATBPS7012G1ZN',10,35 )
        .text('Mob  : 9902664717',10,45)
        .text(`Bill No:    ${BillNumber}`,190,35)
        .text(`${Date}`,190,45)
        .fontSize(10)
        .text(`To    : ${customerName}`,10,55)
    doc
        .moveTo(5, 66)
        .lineTo(295,65)
        .stroke()
        .moveTo(5, 82)
        .lineTo(295,82)
        .stroke();
    doc
        .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-Light.ttf'))
        .fontSize(12)
        .text('ವಿವರಗಳು',30,66 )
        .text('ದರ',145,66,{ width: 50, align: "right" })
        .text('ಪ್ರಮಾಣ',195,66, { width: 50, align: "right" })
        .text('ಮೊತ್ತ',0,66,{ align: "right" })
        .text()
        const prodName = Object.keys(InvoiceData)
        let pageTop = 62
        let position = 0
        let count = 0
        let maxPage = 385
        let numberOfItems = prodName.length
        let saved = 0
        //Show old Balance
        if(old_bal && numberOfItems > 18) maxPage = 365
        let mrp
        for (let i = 0; i < numberOfItems; i++) {
          count += 1
          position = pageTop + ((count + 1) * 10);//gap between rows 
          if (InvoiceData[prodName[i]][0] != 0){
            mrp = (InvoiceData[prodName[i]][0]).toFixed(1)
            saved += (InvoiceData[prodName[i]][0] - InvoiceData[prodName[i]][1])*InvoiceData[prodName[i]][2]
          }
          else
            mrp = ''
          if(InvoiceData[prodName[i]][4]==''){
            x = position
            doc
              .fontSize(8.5)
              .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','Work_Sans','static','WorkSans-Regular.ttf'))
              .text(prodName[i].slice(0,23),5, x )
              .text(mrp, 110, x,{ width: 50, align: "right" })
              .text((InvoiceData[prodName[i]][1]).toFixed(1), 145, x, { width: 50, align: "right" })
              .text((InvoiceData[prodName[i]][2]).toFixed(3) , 195, x, { width: 50, align: "right" })
              .text((InvoiceData[prodName[i]][3]).toFixed(2), 0, x, { align: "right" });
          }
          else{
          doc
          .fontSize(8.5)
          .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-Regular.ttf'))
          .text(InvoiceData[prodName[i]][4].slice(0,23),5, position)
          .text(mrp, 110, position,{ width: 50, align: "right" })
          .text((InvoiceData[prodName[i]][1]).toFixed(1), 145, position, { width: 50, align: "right" })
          .text((InvoiceData[prodName[i]][2]).toFixed(3) , 195, position, { width: 50, align: "right" })
          .text((InvoiceData[prodName[i]][3]).toFixed(2), 0, position, { align: "right" });
          }
          
          if(position > maxPage )
            {
                doc.addPage({size: "A6",margins: {
                    top: 0,
                    bottom: 0,
                    left: 10,
                    right:5
                  }})
                count = 0
                pageTop = -15
                position = 0
            }
        }
    doc
        .moveTo(5, position+15)
        .lineTo(295,position+15)
        .stroke();
    doc
        .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-Regular.ttf'))
        .text(`ಒಟ್ಟು : ₹ ${Math.round(Number(BillTotal)).toFixed(2)}`,0,position+20,{ align: "right" })

    if(old_bal === 'True'){
    doc
        .text(`ಹಳೆ ಬಾಕಿ : ₹ ${Math.round(Number(oldBalData['old_bal'])).toFixed(2)}`,10,position+20,{ align: "left" })
        .text(`ಜಮಾ      : ₹ ${Math.round(Number(oldBalData['amountPaid'])).toFixed(2)}`,10,position+40,{ align: "left" })
        .text(`ಉಳಿದ ಬಾಕಿ : ₹ ${Math.round(Number(oldBalData['remaining_bal'])).toFixed(2)}`,0,position+40,{ align: "right" })
    }

    if(saved>1){
      doc 
        .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','Work_Sans','static','WorkSans-Regular.ttf'))
        .text(`You have Saved Rs.${saved.toFixed(2)} on MRP`,{align:"center"})
    }

    doc .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-Regular.ttf'))
        .text("ನಮ್ಮೊಂದಿಗೆ ವ್ಯವಹರಿಸಿದಕ್ಕೆ ಧನ್ಯವಾದಗಳು. ಮತ್ತೆ ಬನ್ನಿ",{align:"center"})
    doc.end();
    }
  }
  else{
    //Thermal Printer Invoice
  const prodName = Object.keys(InvoiceData)
  let numberOfItems = prodName.length
  height = 85+ numberOfItems*20.5+50
    // start pdf document
    let doc = new PDFDocument({ size: [225,height], margins: {
        top: 3,
        bottom: 3,
        left: 10,
        right:5
      }
      });
 
    doc.pipe(res);

    doc 
        .fontSize(14)
        .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-SemiBold.ttf'))
        .text('ಸೋಮನಾಥ  ಸ್ಟೋರ್', {align: 'center'})

    doc 
        .fontSize(10)
        .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-Medium.ttf'))
        .text('ಮರವಂತೆ - ೫೭೬೨೨೪',0,20,{align: 'center'} )
    doc 
        .font('Helvetica')
        .text('MRP',40, 69,{ width: 50, align: "right" })
        .fontSize(9)
        .text('GST : 29ATBPS7012G1ZN',5,35 )
        .text('Mob  : 9902664717',5,45)
        .text(`Bill No:    ${BillNumber}`,0,35,{align: 'right'})
        .text(`${Date}`,0,45,{align: 'right'})
        .fontSize(9)
        .text(`To     : ${customerName}`,5,55)
        
      
    doc
        .moveTo(5, 65)
        .lineTo(295,65)
        .stroke()
        .moveTo(5, 82)
        .lineTo(295,82)
        .stroke();
        
    doc
        .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-Light.ttf'))
        .fontSize(12)
        .text('ವಿವರಗಳು',15,66 )
        .text('ದರ',85,66,{ width: 50, align: "right" })
        .text('ಪ್ರಮಾಣ',135,66, { width: 50, align: "right" })
        .text('ಮೊತ್ತ',0,66,{ align: "right" })
        .text()
        
        let position = 0
        let position1 = 10
        let pageTop = 10
        let count = 1
        //Show old Balance
        if(old_bal && numberOfItems > 18) maxPage = 365
        let mrp
        for (let i = 0; i < numberOfItems; i++) {
          count += 1
          position = pageTop + ((count + 2) * 20);//gap between rows
          position1 =  20 + ((count + 2) * 20)
          if (InvoiceData[prodName[i]][0] != 0)
            mrp = (InvoiceData[prodName[i]][0]).toFixed(1)
          else
            mrp = ''
          doc
          .fontSize(8.5)
          .font("Helvetica")
          .text(prodName[i],5, position)
          .text(mrp, 40, position1,{ width: 50, align: "right" })
          .text((InvoiceData[prodName[i]][1]).toFixed(1), 85, position1, { width: 50, align: "right" })
          .text((InvoiceData[prodName[i]][2]).toFixed(3) , 120, position1, { width: 50, align: "right" })
          .text((InvoiceData[prodName[i]][3]).toFixed(2), 0, position1, { align: "right" });
          
        }
        position += 10
    doc
        .moveTo(5, position+8)
        .lineTo(295,position+8)
        .stroke();
    doc
        .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-Regular.ttf'))
        .text(`ಒಟ್ಟು : ₹ ${Math.round(Number(BillTotal)).toFixed(2)}`,0,position+10,{ align: "right" })

    if(old_bal === 'True'){
    doc
        .text(`ಹಳೆ ಬಾಕಿ : ₹ ${Math.round(Number(oldBalData['old_bal'])).toFixed(2)}`,10,position+10,{ align: "left" })
        .text(`ಜಮಾ      : ₹ ${Math.round(Number(oldBalData['amountPaid'])).toFixed(2)}`,10,position+23,{ align: "left" })
        .text(`ಉಳಿದ ಬಾಕಿ : ₹ ${Math.round(Number(oldBalData['remaining_bal'])).toFixed(2)}`,0,position+23,{ align: "right" })
    }
    doc .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-Regular.ttf'))
        .text("ನಮ್ಮೊಂದಿಗೆ ವ್ಯವಹರಿಸಿದಕ್ಕೆ ಧನ್ಯವಾದಗಳು. ಮತ್ತೆ ಬನ್ನಿ",{align:"center"})
    doc.end();
  }
}

function voucher( Date, customerName, oldBalData , res){
  // start pdf document
  let doc = new PDFDocument({ size: 'A6', margins: {
      top: 3,
      bottom: 3,
      left: 10,
      right:5
    }
    });

  

  doc.pipe(res);
  doc 
      .font('Helvetica')
      .fontSize(12)
      .text(`${customerName}`,0,5,{ align: "center" })
      
  doc
      .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-Medium.ttf'))
      .text(`ದಿನಾಂಕ :${Date}`,0,20,{ align: "right" })
      .text(`ಹಳೆ ಬಾಕಿ : ₹ ${Math.round(Number(oldBalData['old_bal'])).toFixed(2)}`,10,20,{ align: "left" })
      .text(`ಜಮಾ      : ₹ ${Math.round(Number(oldBalData['amountPaid'])).toFixed(2)}`,10,40,{ align: "left" })
      .text(`ಉಳಿದ ಬಾಕಿ : ₹ ${Math.round(Number(oldBalData['remaining_bal'])).toFixed(2)}`,0,40,{ align: "right" })
  

 
  doc.end();

}

function dbDataPurchase(firm,dbYear,year,firstDay,lastDay,month,res){
fromDb = {}

sql = "SELECT pur_id, pur_firm_id, pur_inv, pur_prod_id, pur_prod_qty, pur_exp, date_format(pur_date,'%m/%d/%Y') as pur_date,acc_name,acc_gstin FROM somanath20"+dbYear+".purchases,somanath.accounts where acc_id =pur_acc and pur_date>='"+firstDay+"' and pur_date<='"+lastDay+"' and pur_firm_id = "+firm+" order by pur_date"

allPurchases = connection.query(sql)
noOfPurchase = allPurchases.length
if(noOfPurchase>0){
  res.sendStatus(200)
  sqlExmept = "SELECT pur_id,pur_prod_id,pur_prod_qty FROM somanath20"+dbYear+".purchases where pur_firm_id ="+firm+" and pur_date >='"+firstDay+"' and pur_date <='"+lastDay+"';"
  allExmept = connection.query(sqlExmept)
  let exemt = 0
  for(e=0;e<allExmept.length;e++)
  {
    prod_id = allExmept[e]['pur_prod_id'].split(':').slice(1,-1)
    prod_qty = allExmept[e]['pur_prod_qty'].split(':').slice(1,-1)
    f = 0
    for(g=0;g<prod_id.length;g++)
    {
      
      gst = connection.query("SELECT prod_gst FROM somanath.products where prod_id ="+prod_id[g])
      if(gst[0]['prod_gst']==1)
      {
        cost = connection.query("SELECT stk_cost FROM somanath20"+dbYear+".stocks where stk_pur_id = '"+allExmept[e]['pur_id']+"' and stk_prod_id = "+prod_id[g])
        exemt += (parseFloat(cost[0]['stk_cost'])*parseFloat(prod_qty[f]))
      }
      f++
    }
  }
  writeFileSync(path.join(homeDir , 'angadiImages' , 'Exempted_'+month+'.txt'),`Somanath Stores\n Total Inward Supply of Exempt/Nil Rated for the month of ${month} : ${exemt}` );

  for(i=0;i<noOfPurchase;i++)
  {
    fromDb[allPurchases[i].pur_id] = {}
    temp = []
      prodQty = allPurchases[i]['pur_prod_qty'].split(':').slice(1,-1)
      prodId = allPurchases[i]["pur_prod_id"].split(':').slice(1,-1)
      billTotal = 0
      taxableTotal = 0
      for(k=0;k<prodId.length;k++)
      {
        result1 = connection.query("SELECT stk_cost,prod_gst,prod_cess FROM somanath20"+dbYear+".stocks,somanath.products where stk_prod_id = "+prodId[k]+" and stk_prod_id = prod_id   and stk_pur_id = '"+allPurchases[i]["pur_id"]+"';")
        result2 = connection.query("SELECT tax_per FROM somanath.taxes where tax_id in ("+result1[0]["prod_gst"]+","+result1[0]["prod_cess"]+");")
        prodTotal = result1[0]['stk_cost']*parseFloat(prodQty[k])
        billTotal += prodTotal
        taxableTotal += prodTotal/(1+(result2[0]['tax_per']/100))
      }   
      gst = ((billTotal - taxableTotal)/2).toFixed(2)
      fromDb[allPurchases[i].pur_id] = [[allPurchases[i]['acc_gstin'],allPurchases[i]['acc_name'],'B2B','Invoice',allPurchases[i]['pur_inv'],allPurchases[i]['pur_date'],taxableTotal.toFixed(2),'',gst,'']]
  }
  let worksheets = {};

worksheets['Read Me'] = {
  '!ref': 'B1:D30',
  B1: {
    t: 's',
    v: '                Goods and Services Tax - Purchase Register Template V2.0',
    r: '<t xml:space="preserve">                Goods and Services Tax - Purchase Register Template V2.0</t>',
    h: '                Goods and Services Tax - Purchase Register Template V2.0',
    w: '                Goods and Services Tax - Purchase Register Template V2.0'
  },
  B5: {
    t: 's',
    v: 'When should a taxpayer use purchase register template ?',
    r: '<t>When should a taxpayer use purchase register template ?</t>',
    h: 'When should a taxpayer use purchase register template ?',
    w: 'When should a taxpayer use purchase register template ?'
  },
  B6: {
    t: 's',
    v: '1. The excel based Purchase register is designed to help the taxpayer to prepare this purchase register, if the taxpayer intends to match the details of GSTR-2B with the purchase register using the offline tool.\r\n' +
      '2. This template has 2 excel worksheets\r\n' +
      '       Worksheet 1: Read me - Contains introduction and help instructions\r\n' +
      '       Worksheet 2: Purchase register - to prepare the purchase register by providing the relevant details',
    r: '<t>1. The excel based Purchase register is designed to help the taxpayer to prepare this purchase register, if the taxpayer intends to match the details of GSTR-2B with the purchase register using the offline tool.\r\n' +
      '2. This template has 2 excel worksheets\r\n' +
      '       Worksheet 1: Read me - Contains introduction and help instructions\r\n' +
      '       Worksheet 2: Purchase register - to prepare the purchase register by providing the relevant details</t>',
    h: '1. The excel based Purchase register is designed to help the taxpayer to prepare this purchase register, if the taxpayer intends to match the details of GSTR-2B with the purchase register using the offline tool.&#x000d;<br/>2. This template has 2 excel worksheets&#x000d;<br/>       Worksheet 1: Read me - Contains introduction and help instructions&#x000d;<br/>       Worksheet 2: Purchase register - to prepare the purchase register by providing the relevant details',
    w: '1. The excel based Purchase register is designed to help the taxpayer to prepare this purchase register, if the taxpayer intends to match the details of GSTR-2B with the purchase register using the offline tool.\r\n' +
      '2. This template has 2 excel worksheets\r\n' +
      '       Worksheet 1: Read me - Contains introduction and help instructions\r\n' +
      '       Worksheet 2: Purchase register - to prepare the purchase register by providing the relevant details'
  },
  B8: {
    t: 's',
    v: 'Preparing the purchase register',
    r: '<t>Preparing the purchase register</t>',
    h: 'Preparing the purchase register',
    w: 'Preparing the purchase register'
  },
  B9: {
    t: 's',
    v: '1. Please ensure you download the latest version of the New return offline tool from the GST Portal - https://www.gst.gov.in/downloads/offline tools\r\n' +
      '2. From the downloaded zip file, open the purchase register template.\r\n' +
      '3. Enter your GSTIN. It should be of 15 characters.\r\n' +
      '4. Select the applicable Financial Year from the drop-down. It is a mandatory field.\r\n' +
      '5. Select the applicable return period from the drop-down. It is a mandatory field.\r\n' +
      '6. Enter the details of the purchase register file where it is stored on the local machine.\r\n',
    r: '<t xml:space="preserve">1. Please ensure you download the latest version of the New return offline tool from the GST Portal - https://www.gst.gov.in/downloads/offline tools\r\n' +
      '2. From the downloaded zip file, open the purchase register template.\r\n' +
      '3. Enter your GSTIN. It should be of 15 characters.\r\n' +
      '4. Select the applicable Financial Year from the drop-down. It is a mandatory field.\r\n' +
      '5. Select the applicable return period from the drop-down. It is a mandatory field.\r\n' +
      '6. Enter the details of the purchase register file where it is stored on the local machine.\r\n' +
      '</t>',
    h: '1. Please ensure you download the latest version of the New return offline tool from the GST Portal - https://www.gst.gov.in/downloads/offline tools&#x000d;<br/>2. From the downloaded zip file, open the purchase register template.&#x000d;<br/>3. Enter your GSTIN. It should be of 15 characters.&#x000d;<br/>4. Select the applicable Financial Year from the drop-down. It is a mandatory field.&#x000d;<br/>5. Select the applicable return period from the drop-down. It is a mandatory field.&#x000d;<br/>6. Enter the details of the purchase register file where it is stored on the local machine.&#x000d;<br/>',
    w: '1. Please ensure you download the latest version of the New return offline tool from the GST Portal - https://www.gst.gov.in/downloads/offline tools\r\n' +
      '2. From the downloaded zip file, open the purchase register template.\r\n' +
      '3. Enter your GSTIN. It should be of 15 characters.\r\n' +
      '4. Select the applicable Financial Year from the drop-down. It is a mandatory field.\r\n' +
      '5. Select the applicable return period from the drop-down. It is a mandatory field.\r\n' +
      '6. Enter the details of the purchase register file where it is stored on the local machine.\r\n'
  },
  B10: {
    t: 's',
    v: 'Important: Do not tamper with the excel template. This might create an issue at the time of importing the purchase register into the offline tool.',
    r: '<t>Important: Do not tamper with the excel template. This might create an issue at the time of importing the purchase register into the offline tool.</t>',
    h: 'Important: Do not tamper with the excel template. This might create an issue at the time of importing the purchase register into the offline tool.',
    w: 'Important: Do not tamper with the excel template. This might create an issue at the time of importing the purchase register into the offline tool.'
  },
  B12: {
    t: 's',
    v: 'Purchase register import on GST offline tool',
    r: '<t>Purchase register import on GST offline tool</t>',
    h: 'Purchase register import on GST offline tool',
    w: 'Purchase register import on GST offline tool'
  },
  B13: {
    t: 's',
    v: '1. Go to New Return offline tool and navigate to the matching tool.\r\n' +
      `2. Import the purchase register by clicking on "Import Excel/csv' button.\r\n` +
      '3. Imported purchase register would be validated and processed. Upon successful validation and processing, the summary of the purchase register shall be displayed.\r\n' +
      '4. The purchase register successfully validated and processed would be added in the offline tool.\r\n' +
      '5. In case of validation failure of one or more details upon processing; an error file shall be generated. Error handling is detailed in next section.\r\n' +
      '6. Post successful import of purchase register, the taxpayer can view the imported details and can continue to match the GSTR-2B with the purchase register.\r\n' +
      '7. Please note, at one time only one purchase register can be imported.\r\n',
    r: '<t xml:space="preserve">1. Go to New Return offline tool and navigate to the matching tool.\r\n' +
      `2. Import the purchase register by clicking on "Import Excel/csv' button.\r\n` +
      '3. Imported purchase register would be validated and processed. Upon successful validation and processing, the summary of the purchase register shall be displayed.\r\n' +
      '4. The purchase register successfully validated and processed would be added in the offline tool.\r\n' +
      '5. In case of validation failure of one or more details upon processing; an error file shall be generated. Error handling is detailed in next section.\r\n' +
      '6. Post successful import of purchase register, the taxpayer can view the imported details and can continue to match the GSTR-2B with the purchase register.\r\n' +
      '7. Please note, at one time only one purchase register can be imported.\r\n' +
      '</t>',
    h: '1. Go to New Return offline tool and navigate to the matching tool.&#x000d;<br/>2. Import the purchase register by clicking on &quot;Import Excel/csv&apos; button.&#x000d;<br/>3. Imported purchase register would be validated and processed. Upon successful validation and processing, the summary of the purchase register shall be displayed.&#x000d;<br/>4. The purchase register successfully validated and processed would be added in the offline tool.&#x000d;<br/>5. In case of validation failure of one or more details upon processing; an error file shall be generated. Error handling is detailed in next section.&#x000d;<br/>6. Post successful import of purchase register, the taxpayer can view the imported details and can continue to match the GSTR-2B with the purchase register.&#x000d;<br/>7. Please note, at one time only one purchase register can be imported.&#x000d;<br/>',
    w: '1. Go to New Return offline tool and navigate to the matching tool.\r\n' +
      `2. Import the purchase register by clicking on "Import Excel/csv' button.\r\n` +
      '3. Imported purchase register would be validated and processed. Upon successful validation and processing, the summary of the purchase register shall be displayed.\r\n' +
      '4. The purchase register successfully validated and processed would be added in the offline tool.\r\n' +
      '5. In case of validation failure of one or more details upon processing; an error file shall be generated. Error handling is detailed in next section.\r\n' +
      '6. Post successful import of purchase register, the taxpayer can view the imported details and can continue to match the GSTR-2B with the purchase register.\r\n' +
      '7. Please note, at one time only one purchase register can be imported.\r\n'
  },
  B15: {
    t: 's',
    v: 'Error file handling',
    r: '<t>Error file handling</t>',
    h: 'Error file handling',
    w: 'Error file handling'
  },
  B16: {
    t: 's',
    v: '1. In case of validation failure of one or more details upon processing on purchase register, an error file shall be generated.\r\n' +
      "2. The error file can be downloaded by clicking on 'Download Error File'.\r\n" +
      '3. Download the error file and save it on your system.\r\n' +
      "4. Go to the worksheet 'Purchase register' and see the column 'Offline tool validation error' column to see the validation errors.\r\n" +
      '5. Correct the errors.\r\n' +
      "6. Follow steps mentioned in 'Purchase register import GST offline tool' section to re-import the purchase register.",
    r: '<t>1. In case of validation failure of one or more details upon processing on purchase register, an error file shall be generated.\r\n' +
      "2. The error file can be downloaded by clicking on 'Download Error File'.\r\n" +
      '3. Download the error file and save it on your system.\r\n' +
      "4. Go to the worksheet 'Purchase register' and see the column 'Offline tool validation error' column to see the validation errors.\r\n" +
      '5. Correct the errors.\r\n' +
      "6. Follow steps mentioned in 'Purchase register import GST offline tool' section to re-import the purchase register.</t>",
    h: '1. In case of validation failure of one or more details upon processing on purchase register, an error file shall be generated.&#x000d;<br/>2. The error file can be downloaded by clicking on &apos;Download Error File&apos;.&#x000d;<br/>3. Download the error file and save it on your system.&#x000d;<br/>4. Go to the worksheet &apos;Purchase register&apos; and see the column &apos;Offline tool validation error&apos; column to see the validation errors.&#x000d;<br/>5. Correct the errors.&#x000d;<br/>6. Follow steps mentioned in &apos;Purchase register import GST offline tool&apos; section to re-import the purchase register.',
    w: '1. In case of validation failure of one or more details upon processing on purchase register, an error file shall be generated.\r\n' +
      "2. The error file can be downloaded by clicking on 'Download Error File'.\r\n" +
      '3. Download the error file and save it on your system.\r\n' +
      "4. Go to the worksheet 'Purchase register' and see the column 'Offline tool validation error' column to see the validation errors.\r\n" +
      '5. Correct the errors.\r\n' +
      "6. Follow steps mentioned in 'Purchase register import GST offline tool' section to re-import the purchase register."
  },
  B18: {
    t: 's',
    v: 'Purchase Register Data Entry Instructions',
    r: '<t>Purchase Register Data Entry Instructions</t>',
    h: 'Purchase Register Data Entry Instructions',
    w: 'Purchase Register Data Entry Instructions'
  },
  B19: {
    t: 's',
    v: 'Worksheet name',
    r: '<t>Worksheet name</t>',
    h: 'Worksheet name',
    w: 'Worksheet name'
  },
  C19: {
    t: 's',
    v: 'Field Name',
    r: '<t>Field Name</t>',
    h: 'Field Name',
    w: 'Field Name'
  },
  D19: {
    t: 's',
    v: 'Help Instruction',
    r: '<t>Help Instruction</t>',
    h: 'Help Instruction',
    w: 'Help Instruction'
  },
  B20: {
    t: 's',
    v: 'Purchase Register',
    r: '<t>Purchase Register</t>',
    h: 'Purchase Register',
    w: 'Purchase Register'
  },
  C20: {
    t: 's',
    v: 'GSTIN of supplier',
    r: '<t>GSTIN of supplier</t>',
    h: 'GSTIN of supplier',
    w: 'GSTIN of supplier'
  },
  D20: {
    t: 's',
    v: 'Enter the GSTIN of the supplier. The GSTIN should be of 15 characters. e.g. 05AAACP0000AAAA',
    r: '<t>Enter the GSTIN of the supplier. The GSTIN should be of 15 characters. e.g. 05AAACP0000AAAA</t>',
    h: 'Enter the GSTIN of the supplier. The GSTIN should be of 15 characters. e.g. 05AAACP0000AAAA',
    w: 'Enter the GSTIN of the supplier. The GSTIN should be of 15 characters. e.g. 05AAACP0000AAAA'
  },
  C21: {
    t: 's',
    v: 'Trade/Legal name',
    r: '<t>Trade/Legal name</t>',
    h: 'Trade/Legal name',
    w: 'Trade/Legal name'
  },
  D21: {
    t: 's',
    v: 'Enter the Trade/Legal name of the Supplier',
    r: '<t>Enter the Trade/Legal name of the Supplier</t>',
    h: 'Enter the Trade/Legal name of the Supplier',
    w: 'Enter the Trade/Legal name of the Supplier'
  },
  C22: {
    t: 's',
    v: 'Type of inward supplies',
    r: '<t>Type of inward supplies</t>',
    h: 'Type of inward supplies',
    w: 'Type of inward supplies'
  },
  D22: {
    t: 's',
    v: 'Select the type of inward supplies from the dropdown, for example:\r\n' +
      'Supplies from registered persons  - B2B\r\n' +
      'SEZ supplies with payment -  SEZWP\r\n' +
      'SEZ supplies without payment - SEZWOP\r\n' +
      'Deemed Exports - DE',
    r: '<t>Select the type of inward supplies from the dropdown, for example:\r\n' +
      'Supplies from registered persons  - B2B\r\n' +
      'SEZ supplies with payment -  SEZWP\r\n' +
      'SEZ supplies without payment - SEZWOP\r\n' +
      'Deemed Exports - DE</t>',
    h: 'Select the type of inward supplies from the dropdown, for example:&#x000d;<br/>Supplies from registered persons  - B2B&#x000d;<br/>SEZ supplies with payment -  SEZWP&#x000d;<br/>SEZ supplies without payment - SEZWOP&#x000d;<br/>Deemed Exports - DE',
    w: 'Select the type of inward supplies from the dropdown, for example:\r\n' +
      'Supplies from registered persons  - B2B\r\n' +
      'SEZ supplies with payment -  SEZWP\r\n' +
      'SEZ supplies without payment - SEZWOP\r\n' +
      'Deemed Exports - DE'
  },
  C23: {
    t: 's',
    v: 'Document type',
    r: '<t>Document type</t>',
    h: 'Document type',
    w: 'Document type'
  },
  D23: {
    t: 's',
    v: 'Select the document type from the Dropdown:\r\n' +
      'Invoice\r\n' +
      'Debit Note\r\n' +
      'Credit Note',
    r: '<t>Select the document type from the Dropdown:\r\n' +
      'Invoice\r\n' +
      'Debit Note\r\n' +
      'Credit Note</t>',
    h: 'Select the document type from the Dropdown:&#x000d;<br/>Invoice&#x000d;<br/>Debit Note&#x000d;<br/>Credit Note',
    w: 'Select the document type from the Dropdown:\r\n' +
      'Invoice\r\n' +
      'Debit Note\r\n' +
      'Credit Note'
  },
  C24: {
    t: 's',
    v: 'Document number',
    r: '<t>Document number</t>',
    h: 'Document number',
    w: 'Document number'
  },
  D24: {
    t: 's',
    v: 'Enter the Document number. Ensure that the format is alpha-numeric with  allowed special characters of slash(/) and dash(-) .The total number of characters should not be more than 16.',
    r: '<t>Enter the Document number. Ensure that the format is alpha-numeric with  allowed special characters of slash(/) and dash(-) .The total number of characters should not be more than 16.</t>',
    h: 'Enter the Document number. Ensure that the format is alpha-numeric with  allowed special characters of slash(/) and dash(-) .The total number of characters should not be more than 16.',
    w: 'Enter the Document number. Ensure that the format is alpha-numeric with  allowed special characters of slash(/) and dash(-) .The total number of characters should not be more than 16.'
  },
  C25: {
    t: 's',
    v: 'Document date',
    r: '<t>Document date</t>',
    h: 'Document date',
    w: 'Document date'
  },
  D25: {
    t: 's',
    v: 'Enter date of document in DD/MM/YYYY. e.g. 24/07/2019.',
    r: '<t>Enter date of document in DD/MM/YYYY. e.g. 24/07/2019.</t>',
    h: 'Enter date of document in DD/MM/YYYY. e.g. 24/07/2019.',
    w: 'Enter date of document in DD/MM/YYYY. e.g. 24/07/2019.'
  },
  C26: {
    t: 's',
    v: 'Taxable value',
    r: '<t>Taxable value</t>',
    h: 'Taxable value',
    w: 'Taxable value'
  },
  D26: {
    t: 's',
    v: 'Enter the taxable value of the received goods or services. It should not exceed 13 digits and 2 decimals.',
    r: '<t>Enter the taxable value of the received goods or services. It should not exceed 13 digits and 2 decimals.</t>',
    h: 'Enter the taxable value of the received goods or services. It should not exceed 13 digits and 2 decimals.',
    w: 'Enter the taxable value of the received goods or services. It should not exceed 13 digits and 2 decimals.'
  },
  C27: {
    t: 's',
    v: 'Integrated tax',
    r: '<t>Integrated tax</t>',
    h: 'Integrated tax',
    w: 'Integrated tax'
  },
  D27: {
    t: 's',
    v: 'Enter the Integrated tax amount. It should not exceed 13 digits and 2 decimals.',
    r: '<t>Enter the Integrated tax amount. It should not exceed 13 digits and 2 decimals.</t>',
    h: 'Enter the Integrated tax amount. It should not exceed 13 digits and 2 decimals.',
    w: 'Enter the Integrated tax amount. It should not exceed 13 digits and 2 decimals.'
  },
  C28: {
    t: 's',
    v: 'Central tax',
    r: '<t>Central tax</t>',
    h: 'Central tax',
    w: 'Central tax'
  },
  D28: {
    t: 's',
    v: 'Enter the Central tax amount. It should not exceed 13 digits and 2 decimals.',
    r: '<t>Enter the Central tax amount. It should not exceed 13 digits and 2 decimals.</t>',
    h: 'Enter the Central tax amount. It should not exceed 13 digits and 2 decimals.',
    w: 'Enter the Central tax amount. It should not exceed 13 digits and 2 decimals.'
  },
  C29: {
    t: 's',
    v: 'State/UT tax',
    r: '<t>State/UT tax</t>',
    h: 'State/UT tax',
    w: 'State/UT tax'
  },
  D29: {
    t: 's',
    v: 'Enter the State/UT tax amount. It should not exceed 13 digits and 2 decimals.',
    r: '<t>Enter the State/UT tax amount. It should not exceed 13 digits and 2 decimals.</t>',
    h: 'Enter the State/UT tax amount. It should not exceed 13 digits and 2 decimals.',
    w: 'Enter the State/UT tax amount. It should not exceed 13 digits and 2 decimals.'
  },
  C30: { t: 's', v: 'Cess', r: '<t>Cess</t>', h: 'Cess', w: 'Cess' },
  D30: {
    t: 's',
    v: 'Enter the Cess amount. It should not exceed 13 digits and 2 decimals.',
    r: '<t>Enter the Cess amount. It should not exceed 13 digits and 2 decimals.</t>',
    h: 'Enter the Cess amount. It should not exceed 13 digits and 2 decimals.',
    w: 'Enter the Cess amount. It should not exceed 13 digits and 2 decimals.'
  },
  '!margins': {
    left: 0.7,
    right: 0.7,
    top: 0.75,
    bottom: 0.75,
    header: 0.3,
    footer: 0.3
  }
}

worksheets['Purchase Reigster'] = {
  "!ref":"A1:K8",
  "B1":{"t":"s","v":"GSTIN of recipient* : ","r":"<t xml:space=\"preserve\">GSTIN of recipient* : </t>","h":"GSTIN of recipient* : ","w":"GSTIN of recipient* : "},
  "C1":{"t":"s","v":"29ATBPS7012G1ZN","r":"<t>29ATBPS7012G1ZN</t>","h":"29ATBPS7012G1ZN","w":"29ATBPS7012G1ZN"},
  "D1":{"t":"s","v":"Financial year* :","r":"<t>Financial year* :</t>","h":"Financial year* :","w":"Financial year* :"},
  "E1":{"t":"s","v":"2021-22","r":"<t>2021-22</t>","h":"2021-22","w":"2021-22"},"B2":{"t":"s","v":"Trade/Legal name:","r":"<t>Trade/Legal name:</t>","h":"Trade/Legal name:","w":"Trade/Legal name:"},
  "C2":{"t":"s","v":"GANAPATHY KRISHNARAYA SHENOY","r":"<t>GANAPATHY KRISHNARAYA SHENOY</t>","h":"GANAPATHY KRISHNARAYA SHENOY","w":"GANAPATHY KRISHNARAYA SHENOY"},
  "D2":{"t":"s","v":"Tax period* : ","r":"<t xml:space=\"preserve\">Tax period* : </t>","h":"Tax period* : ","w":"Tax period* : "},
  "E2":{"t":"s","v":"February","r":"<t>February</t>","h":"February","w":"February"},
  "F2":{"t":"s","v":"                  Please Note: Fields marked with * (red asterisk) are mandatory fields and need to be filled up","r":"<t xml:space=\"preserve\">                  Please Note: Fields marked with * (red asterisk) are mandatory fields and need to be filled up</t>","h":"                  Please Note: Fields marked with * (red asterisk) are mandatory fields and need to be filled up","w":"                  Please Note: Fields marked with * (red asterisk) are mandatory fields and need to be filled up"},
  "A5":{"t":"s","v":"GSTIN of supplier *","r":"<t>GSTIN of supplier *</t>","h":"GSTIN of supplier *","w":"GSTIN of supplier *"},
  "B5":{"t":"s","v":"Trade/Legal name","r":"<t>Trade/Legal name</t>","h":"Trade/Legal name","w":"Trade/Legal name"},
  "C5":{"t":"s","v":"Type of inward supplies *","r":"<t>Type of inward supplies *</t>","h":"Type of inward supplies *","w":"Type of inward supplies *"},
  "D5":{"t":"s","v":"Document type *","r":"<t>Document type *</t>","h":"Document type *","w":"Document type *"},
  "E5":{"t":"s","v":"Document number *","r":"<t>Document number *</t>","h":"Document number *","w":"Document number *"},
  "F5":{"t":"s","v":"Document date *","r":"<t>Document date *</t>","h":"Document date *","w":"Document date *"},
  "G5":{"t":"s","v":"Taxable value (₹) *","r":"<t>Taxable value (₹) *</t>","h":"Taxable value (₹) *","w":"Taxable value (₹) *"},
  "H5":{"t":"s","v":"Integrated tax (₹) ","r":"<t xml:space=\"preserve\">Integrated tax (₹) </t>","h":"Integrated tax (₹) ","w":"Integrated tax (₹) "},
  "I5":{"t":"s","v":"Central tax (₹) ","r":"<t xml:space=\"preserve\">Central tax (₹) </t>","h":"Central tax (₹) ","w":"Central tax (₹) "},
  "J5":{"t":"s","v":"State/ UT tax (₹) ","r":"<t xml:space=\"preserve\">State/ UT tax (₹) </t>","h":"State/ UT tax (₹) ","w":"State/ UT tax (₹) "},
  "K5":{"t":"s","v":"Cess (₹) ","r":"<t xml:space=\"preserve\">Cess (₹) </t>","h":"Cess (₹) ","w":"Cess (₹) "},
}

i = 6
date1 = new Date("12/30/1899");
Object.keys(fromDb).forEach(element => {
  GSTIN = String(fromDb[element][0][0])
  TradeName = String(fromDb[element][0][1])
  TypeOfSupply = String(fromDb[element][0][2])
  DocType = String(fromDb[element][0][3])
  DocNum = String(fromDb[element][0][4])
  xDate = String(fromDb[element][0][5])
  TaxableValue = String(fromDb[element][0][6])
  GST = String(fromDb[element][0][8])
  worksheets['Purchase Reigster']["A"+i] = {"t":"s","v":GSTIN,"r":"<t>"+fromDb[element][0][0]+"</t>","h":GSTIN,"w":GSTIN}
  worksheets['Purchase Reigster']["B"+i] = {"t":"s","v":TradeName,"r":"<t>"+fromDb[element][0][1]+"</t>","h":TradeName,"w":TradeName}
  worksheets['Purchase Reigster']["C"+i] = {"t":"s","v":TypeOfSupply,"r":"<t>"+fromDb[element][0][2]+"</t>","h":TypeOfSupply,"w":TypeOfSupply},
  worksheets['Purchase Reigster']["D"+i] = {"t":"s","v":DocType,"r":"<t>"+fromDb[element][0][3]+"</t>","h":DocType,"w":DocType},
  worksheets['Purchase Reigster']["E"+i] = {t: 's',v: DocNum,r: "<t>"+fromDb[element][0][4]+"</t>",h: DocNum,w: DocNum}
  date2 = new Date(xDate);
  Difference_In_Days = (date2.getTime() - date1.getTime())/ (1000 * 3600 * 24);
  worksheets['Purchase Reigster']["F"+i] = {"t":"n","v":parseInt(Difference_In_Days.toFixed(0)),"w":xDate},
  worksheets['Purchase Reigster']["G"+i] = {"t":"n","v":fromDb[element][0][6],"w":TaxableValue},
  worksheets['Purchase Reigster']["H"+i] = {"t":"n","v":0,"w":"0.00"}, //IGST
  worksheets['Purchase Reigster']["I"+i] = {"t":"n","v":fromDb[element][0][8],"w":GST},
  worksheets['Purchase Reigster']["J"+i] = {"t":"n","v":fromDb[element][0][8],"w":GST},
  worksheets['Purchase Reigster']["K"+i] = {"t":"n","v":0,"w":"0"}
  i++
});
worksheets['Purchase Reigster']["E1"] = {"t":"s","v":String(year),"r":"<t>"+year+"</t>","h":String(year),"w":String(year)}
worksheets['Purchase Reigster']["E2"] = {"t":"s","v":String(month),"r":"<t>"+month+"</t>","h":String(month),"w":String(month)}
worksheets['Purchase Reigster']["!ref"] = String("A1:K"+(i-1))
worksheets['Purchase Reigster']["!margins"] = {"left":0.7,"right":0.7,"top":0.75,"bottom":0.75,"header":0.3,"footer":0.3}
const newBook = XLSX.utils.book_new();
XLSX.utils.book_append_sheet(newBook, worksheets['Read Me'], "Read Me");
XLSX.utils.book_append_sheet(newBook, worksheets['Purchase Reigster'], "Purchase Reigster");
XLSX.writeFileSync(newBook,path.join(homeDir , 'angadiImages' , "Purchase_"+month+".xlsx"));

socket.emit("reportFinished" , "Purchase Report" , "Purchase_"+month+".xlsx Exempted_"+month+".txt")

}
else{
  res.sendStatus(201)

}
}

function dbDataSales(firm,dbYear,firstDay,lastDay,month,res){
  sql = "SELECT gst_value, cess_value,sales_prod_qty, sales_prod_sp FROM somanath20"+dbYear+".sales LEFT JOIN somanath20"+dbYear+".sales_sp ON somanath20"+dbYear+".sales.sales_ref = somanath20"+dbYear+".sales_sp.sales_ref  where sale_date>='"+firstDay+"' and sale_date<='"+lastDay+"' and  somanath20"+dbYear+".sales.sales_ref regexp '"+firm+"' order by sale_date"
  con.query(sql,(err,sales)=>{
    if(sales.length>0)
        {
              res.sendStatus(200)
              total = {0:[0,0],5:[0,0],12:[0,0],18:[0,0],28:[0,0]}
              Object.keys(sales).forEach(bill => 
                  {
                      gst = sales[bill]['gst_value'].split(':').slice(1,-1)
                      cess = sales[bill]['cess_value'].split(':').slice(1,-1)
                      qty = sales[bill]['sales_prod_qty'].split(':').slice(1,-1)
                      sp = sales[bill]['sales_prod_sp'].split(':').slice(1,-1)
                      for(i=0;i<sp.length;i++)
                        {
                              total[parseInt(gst[i])][0] +=  parseFloat(sp[i]) * parseFloat(qty[i])
                              if(parseInt(cess[i]) != 0)
                                total[parseInt(gst[i])][1] +=   ( ( parseFloat(sp[i]) * parseFloat(qty[i]) ) / ( 1 + ( (parseInt(gst[i])/100) ) ) ) * ( parseInt(cess[i]) /100)
                              
                        }
                  });
              total[0][0] = total[0][0].toFixed(2)
              total[5][0] = (total[5][0]/1.05).toFixed(2)
              total[12][0] = (total[12][0]/1.12).toFixed(2)
              total[18][0] = (total[18][0]/1.18).toFixed(2)
              total[28][0] = (total[28][0]/1.28).toFixed(2)
              total[0][1] = total[0][1].toFixed(2)
              total[5][1] = total[5][1].toFixed(2)
              total[12][1] = total[12][1].toFixed(2)
              total[18][1] = total[18][1].toFixed(2)
              total[28][1] = total[28][1].toFixed(2)
              //location
              const workbook = XLSX.readFile(path.join(homeDir,'Hosangadi2.0','backend','printer_server','GSTR1_Excel_Workbook_Template_V1.81.xlsx'));

          SheetNames = ['Help Instruction', 'b2b','b2ba','b2cl','b2cla','b2cs','b2csa','cdnr','cdnra','cdnur','cdnura','exp','expa','at','ata','atadj','atadja','exemp','hsn','docs','master']

          workbook.Sheets['exemp']= {
            '!ref': 'A1:D10',
            A1: {
              t: 's',
              v: 'Summary For Nil rated, exempted and non GST outward supplies (8)',
              r: '<t>Summary For Nil rated, exempted and non GST outward supplies (8)</t>',
              h: 'Summary For Nil rated, exempted and non GST outward supplies (8)',
              w: 'Summary For Nil rated, exempted and non GST outward supplies (8)'
            },
            D1: {
              t: 's',
              v: 'HELP',
              r: '<t>HELP</t>',
              h: 'HELP',
              w: 'HELP',
              l: {
                ref: 'D1',
                location: 'EXEMP',
                display: 'HELP',
                Target: '#EXEMP',
                Rel: [Object]
              }
            },
            B2: {
              t: 's',
              v: 'Total Nil Rated Supplies',
              r: '<t>Total Nil Rated Supplies</t>',
              h: 'Total Nil Rated Supplies',
              w: 'Total Nil Rated Supplies'
            },
            C2: {
              t: 's',
              v: 'Total Exempted Supplies',
              r: '<t>Total Exempted Supplies</t>',
              h: 'Total Exempted Supplies',
              w: 'Total Exempted Supplies'
            },
            D2: {
              t: 's',
              v: 'Total Non-GST Supplies',
              r: '<t>Total Non-GST Supplies</t>',
              h: 'Total Non-GST Supplies',
              w: 'Total Non-GST Supplies'
            },
            B3: { t: 'n', v: 0, f: 'SUM(B5:B8)', w: '0' },
            C3: { t: 'n', v: 0, f: 'SUM(C5:C8)', w: '0.00' },
            D3: { t: 'n', v: 0, f: 'SUM(D5:D8)', w: '0.00' },
            A4: {
              t: 's',
              v: 'Description',
              r: '<t>Description</t>',
              h: 'Description',
              w: 'Description'
            },
            B4: {
              t: 's',
              v: 'Nil Rated Supplies',
              r: '<t>Nil Rated Supplies</t>',
              h: 'Nil Rated Supplies',
              w: 'Nil Rated Supplies'
            },
            C4: {
              t: 's',
              v: 'Exempted(other than nil rated/non GST supply)',
              r: '<t>Exempted(other than nil rated/non GST supply)</t>',
              h: 'Exempted(other than nil rated/non GST supply)',
              w: 'Exempted(other than nil rated/non GST supply)'
            },
            D4: {
              t: 's',
              v: 'Non-GST Supplies',
              r: '<t>Non-GST Supplies</t>',
              h: 'Non-GST Supplies',
              w: 'Non-GST Supplies'
            },
            A5: {
              t: 's',
              v: 'Inter-State supplies to registered persons',
              r: '<t>Inter-State supplies to registered persons</t>',
              h: 'Inter-State supplies to registered persons',
              w: 'Inter-State supplies to registered persons'
            },
            A6: {
              t: 's',
              v: 'Intra-State supplies to registered persons',
              r: '<t>Intra-State supplies to registered persons</t>',
              h: 'Intra-State supplies to registered persons',
              w: 'Intra-State supplies to registered persons'
            },
            A7: {
              t: 's',
              v: 'Inter-State supplies to unregistered persons',
              r: '<t>Inter-State supplies to unregistered persons</t>',
              h: 'Inter-State supplies to unregistered persons',
              w: 'Inter-State supplies to unregistered persons'
            },
            A8: {
              t: 's',
              v: 'Intra-State supplies to unregistered persons',
              r: '<t>Intra-State supplies to unregistered persons</t>',
              h: 'Intra-State supplies to unregistered persons',
              w: 'Intra-State supplies to unregistered persons'
            },
            B8: { t: 'n', v: 0, w: '0' },
            '!margins': {
              left: 0.7,
              right: 0.7,
              top: 0.75,
              bottom: 0.75,
              header: 0.3,
              footer: 0.3
            }
          }

          workbook.Sheets['exemp']['B3'] = { t: 'n', v: parseFloat(total['0'][0]), f: 'SUM(B5:B8)', w: total['0'][0] }
          workbook.Sheets['exemp']['B8'] = { t: 'n', v: parseFloat(total['0'][0]), w: total['0'][0] }


          ttlTaxable = (parseFloat(total['0'][0]) + parseFloat(total['5'][0]) + parseFloat(total['12'][0]) + parseFloat(total['18'][0]) + parseFloat(total['28'][0])).toFixed(2)
          ttlCess = (parseFloat(total['0'][1]) + parseFloat(total['5'][1]) + parseFloat(total['12'][1]) + parseFloat(total['18'][1]) + parseFloat(total['28'][1])).toFixed(2)

          workbook.Sheets['b2cs'] =  
          {
            '!ref': 'A1:G8',
            A1: {
              t: 's',
              v: 'Summary For B2CS(7)',
              r: '<t>Summary For B2CS(7)</t>',
              h: 'Summary For B2CS(7)',
              w: 'Summary For B2CS(7)'
            },
            G1: {
              t: 's',
              v: 'HELP',
              r: '<t>HELP</t>',
              h: 'HELP',
              w: 'HELP',
              l: {
                ref: 'G1',
                location: 'B2CS',
                display: 'HELP',
                Target: '#B2CS',
                Rel: [Object]
              }
            },
            E2: {
              t: 's',
              v: 'Total Taxable  Value',
              r: '<t>Total Taxable  Value</t>',
              h: 'Total Taxable  Value',
              w: 'Total Taxable  Value'
            },
            F2: {
              t: 's',
              v: 'Total Cess',
              r: '<t>Total Cess</t>',
              h: 'Total Cess',
              w: 'Total Cess'
            },
            E3: { t: 'n', v: parseFloat(ttlTaxable), f: 'SUM(E5:E8)', w: ttlTaxable },
            F3: { t: 'n', v: parseFloat(ttlCess), f: 'SUM(F5:F8)', w: ttlCess },
            A4: { t: 's', v: 'Type', r: '<t>Type</t>', h: 'Type', w: 'Type' },
            B4: {
              t: 's',
              v: 'Place Of Supply',
              r: '<t>Place Of Supply</t>',
              h: 'Place Of Supply',
              w: 'Place Of Supply'
            },
            C4: {
              t: 's',
              v: 'Applicable % of Tax Rate',
              r: '<t>Applicable % of Tax Rate</t>',
              h: 'Applicable % of Tax Rate',
              w: 'Applicable % of Tax Rate'
            },
            D4: { t: 's', v: 'Rate', r: '<t>Rate</t>', h: 'Rate', w: 'Rate' },
            E4: {
              t: 's',
              v: 'Taxable Value',
              r: '<t>Taxable Value</t>',
              h: 'Taxable Value',
              w: 'Taxable Value'
            },
            F4: {
              t: 's',
              v: 'Cess Amount',
              r: '<t>Cess Amount</t>',
              h: 'Cess Amount',
              w: 'Cess Amount'
            },
            G4: {
              t: 's',
              v: 'E-Commerce GSTIN',
              r: '<t>E-Commerce GSTIN</t>',
              h: 'E-Commerce GSTIN',
              w: 'E-Commerce GSTIN'
            },
          }
          
          i = 5
            Object.keys(total).slice(1).forEach( gst => {
              if (parseFloat(total[gst][0]) > 0)
              {
                
                workbook.Sheets['b2cs']["A"+i] = { t: 's', v: 'OE', r: '<t>OE</t>', h: 'OE', w: 'OE' },
                workbook.Sheets['b2cs']["B"+i] = { t: 's', v: '29-Karnataka',r: '<t>29-Karnataka</t>',h: '29-Karnataka',w: '29-Karnataka'},
                workbook.Sheets['b2cs']["D"+i] = { t: 'n', v: parseFloat(gst), w: gst },
                workbook.Sheets['b2cs']["E"+i] = { t: 'n', v: parseFloat(total[gst][0]), w: total[gst][0] }
                
                if(parseFloat(total[gst][1]) >  0)
                {
                  workbook.Sheets['b2cs']["F"+i] = { t: 'n', v: parseFloat(total[gst][1]), w: total[gst][1] }
                
                }
              }
            i++
          });

          workbook.Sheets['b2cs']["!margins"] = {left: 0.7,right: 0.7,top: 0.75,bottom: 0.75,header: 0.3,footer: 0.3}

          const newBook = XLSX.utils.book_new();
          SheetNames.forEach( SheetName => {
            XLSX.utils.book_append_sheet(newBook, workbook.Sheets[SheetName], SheetName);
          });

          XLSX.writeFileSync(newBook,path.join(homeDir , 'angadiImages' , "GSTR1_"+month+".xlsx"))
          socket.emit("reportFinished" , "Sales Report" , "GSTR1_"+month+".xlsx")
        }

    else
      {
          res.sendStatus(201)
      }
  })
}

function orderList(list,res)
{
  singlePage = true
  if(parseInt(list[0][3])>5)
      {
        singlePage = false
      }

  let doc = new PDFDocument({ size: 'A6', margins: {
    top: 3,
    bottom: 3,
    left: 10,
    right:5
  }
  });

doc.pipe(res);
if(singlePage)
  {
    doc .fontSize(12)
    .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-SemiBold.ttf'))
    .text('ಸೋಮನಾಥ  ಸ್ಟೋರ್', {align: 'center'})
    }
let position = 0
let count = 0
let numberOfItems = list.length
let j = 0;
for (i = 0  ;i < numberOfItems; i++){
  if(parseInt(list[i][3])>5)
  {
    j = i
    break
  }
  
    count += 1
    position = 10 + count*10;//gap between rows 
    doc
    .fontSize(8.5)
    .font("Helvetica")
    .text(list[i][0],5, position)
    .text(list[i][1],145, position, { width: 50, align: "right" })
    .text(list[i][2],195, position, { width: 100, align: "center" })

    if(count == 39 ) 
      {
          doc.addPage({size: "A6",margins: {
              top: 0,
              bottom: 0,
              left: 10,
              right:5
            }})
            doc
            .fontSize(12)
            .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-SemiBold.ttf'))
            .text('ಸೋಮನಾಥ  ಸ್ಟೋರ್', {align: 'center'})
          count = 0
      }
  

}
 if(singlePage){
  doc.addPage({size: "A6",margins: {
    top: 0,
    bottom: 0,
    left: 10,
    right:5
  }})
 }
      count = 0
      doc
      .fontSize(12)
      .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-SemiBold.ttf'))
      .text('ಸೋಮನಾಥ  ಎಂಟರ್ಪ್ರೈಸ್', {align: 'center'})
      
      
      for(j ; j<numberOfItems ; j++)
      {
      count += 1
      position = 10 + count*10;//gap between rows 
      doc
      .fontSize(8.5)
      .font("Helvetica")
      .text(list[j][0],5, position)
      .text(list[j][1],145, position, { width: 50, align: "right" })
      .text(list[j][2],195, position, { width: 100, align: "center" })

      if(count == 39 ) 
        {
            doc.addPage({size: "A6",margins: {
                top: 0,
                bottom: 0,
                left: 10,
                right:5
              }})
              doc
              .fontSize(12)
              .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-SemiBold.ttf'))
              .text('ಸೋಮನಾಥ  ಎಂಟರ್ಪ್ರೈಸ್', {align: 'center'})
            count = 0
        }
      }    
doc.end();
}

//Invoice
app.post('/sales/invoice', invoiceDataFiles.single('upload_file') ,  (req,res) =>{
  fileLocation = path.join(homeDir , req.file.filename)
  invoiceData = readFileSync(fileLocation,{encoding:'utf8', flag:'r'});
  unlink(fileLocation , (err)=>{})
  invoiceData = JSON.parse(invoiceData)
  oldBalData = JSON.parse(req.query.oldBalData)
  Invoice(req.query.billNo, req.query.Date, req.query.customerName,invoiceData , req.query.billTotal,req.query.oldBal,oldBalData,req.query.page,res,req.query.gst)
})

app.get('/sales/voucherPrint', (req,res) =>{
  oldBalData = JSON.parse(req.query.oldBalData)
  voucher(req.query.Date,req.query.customerName,oldBalData , res)
})

app.get('/sales/checkKannada', (req,res) =>{
  let doc = new PDFDocument();
  try{
    doc 
      .font(path.join(homeDir,'Hosangadi2.0','backend','report_server','Languages','NotoFont','static','NotoSerifKannada-Medium.ttf'))
      .text(req.query.kannada,10,10)
      doc.end()
      res.sendStatus(200)
    }catch(err){
    res.sendStatus(201)
  }

  
})

app.get('/PurchaseReport',(req,res)=>{
  dbDataPurchase(req.query.firm,req.query.dbYear,req.query.year,req.query.firstDay,req.query.lastDay,req.query.month,res)
});

app.get('/SalesReport',(req,res)=>{
  dbDataSales(req.query.firm,req.query.dbYear,req.query.firstDay,req.query.lastDay,req.query.month,res)
});

app.get('/orderList',(req,res)=>{
  list = JSON.parse(req.query.values)
  orderList(list,res)
})

app.get('/onlySql' , (req , res)=>{

  sql = req.query.sql
  con.query(sql , (err , result)=>{
    res.send(result)
  })
})

app.get('/billOnly',(req, res)=>{

  dbYear = req.query.dbYear
  billNumber = req.query.billNumber
  sql = "SELECT  acc_name , sales_prod_id , sales_prod_qty , sales_prod_sp , date_format(sale_date,'%d-%m-%Y') as Date  , discount, acc_cls_bal_firm1 + acc_cls_bal_firm2 + acc_cls_bal_firm3 as remaining_bal,trans_amt_firm1+trans_amt_firm2+trans_amt_firm3 as bill_amt,amt_paid_firm1_cash+amt_paid_firm2_cash+amt_paid_firm3_cash+amt_paid_firm1_bank+amt_paid_firm2_bank+amt_paid_firm3_bank as amountPaid"
  sql += " FROM somanath20"+dbYear+".sales, somanath.accounts, somanath20"+dbYear+".acc_bal, somanath20"+dbYear+".cashflow_sales where somanath20"+dbYear+".sales.sales_id = '"+dbYear+"_"+billNumber+"'" 
  sql += " and somanath20"+dbYear+".sales.sales_acc = somanath.accounts.acc_id  and somanath20"+dbYear+".acc_bal.acc_id = somanath20"+dbYear+".sales.sales_acc and somanath20"+dbYear+".cashflow_sales.trans_sales = somanath20"+dbYear+".sales.sales_id;"
  con.query(sql,(err,result)=>{
    if(result.length==0){
      res.sendStatus(201)
    }
    else{
      prodName = []
      prodQty = []
      prodSp = []
      result1 = {}
      j=0
      Object.keys(result).forEach(element => {
        Qty = result[element]['sales_prod_qty'].split(':').slice(1,-1)
        Sp = result[element]['sales_prod_sp'].split(':').slice(1,-1)
        i = 0
        prod = result[element]['sales_prod_id'].split(':').slice(1,-1)
        prod.forEach(id => {
          prodQty.push(Qty[i])
          prodSp.push(Sp[i])
          prodDeatils = connection.query("SELECT prod_name,prod_mrp,prod_id,prod_name_kan FROM somanath.products where prod_id ="+id)
          result1[j] = prodDeatils
          i+=1
          j+=1
        });
      });
      invoiceData = {}
      i = 0
      grandTotal = 0
      Object.keys(result1).forEach(element => {
        each = result1[element][0]
        if(each['prod_name'] in invoiceData){
          x = invoiceData[each['prod_name']]
          tot = parseFloat(prodQty[i])*parseFloat(prodSp[i]) + x[3]
          qty = x[2] + parseFloat(prodQty[i])
          sp = parseFloat((tot/qty).toFixed(2))
          grandTotal += tot
          invoiceData[each['prod_name']] = [x[0],sp,qty,tot,x[4]]
        }
        else{
          MRP = parseFloat(each['prod_mrp'])
          if ( MRP <= parseFloat(prodSp[i]) )
              MRP = 0
          tot = parseFloat(prodQty[i])*parseFloat(prodSp[i])
          grandTotal += tot
          invoiceData[each['prod_name']] = [ MRP , parseFloat(prodSp[i]) , parseFloat(prodQty[i]) , tot,each['prod_name_kan'] ]
        }
        i += 1
      });
      voucher ={
        'old_bal' : parseFloat(result[0]['remaining_bal'])  - ( grandTotal - parseFloat(result[0]['amountPaid']) ),
        'amountPaid': result[0]['amountPaid'],
        'remaining_bal': result[0]['remaining_bal']
      }
      Invoice(billNumber, result[0]['Date'], result[0]['acc_name'],invoiceData , grandTotal,'True',voucher,0,res,req.query.gst)
    }
  })
})

app.get('/cmp08',(req,res)=>{
  reportFileName = ""
  sql = "SELECT sales_prod_sp,sales_prod_qty FROM somanath20"+req.query.dbYear+".sales where sales_ref regexp 'SEM' and sale_date>='"+req.query.firstDay+"' and sale_date<='"+req.query.lastDay+"';"//sales_ref regexp 'SCM' and 
  con.query(sql,(err,result)=>{
    totalSales = 0
    if(result.length==0){
      res.sendStatus(201)
    }
    else{
      res.sendStatus(200)
      Object.keys(result).forEach(element => {
        sp = result[element].sales_prod_sp.split(':').slice(1,-1)
        i = 0
        result[element].sales_prod_qty.split(':').slice(1,-1).forEach(qty => {
          totalSales += qty*sp[i]
          i++
        });
      });
      reportFileName = writeFileSync(path.join(homeDir , 'angadiImages' , 'cmp08.txt'),`Somanath Enterprices\nQuarter     : ${req.query.quarter}\nTotal Sales : ${totalSales.toFixed(2)}` );
      socket.emit("reportFinished" , "Sales CMP" , 'cmp08.txt')
    }
    
  })
 
})

app.get('/gstr04' , (req , res)=>{

res.sendStatus(200)

dbYear = req.query.dbYear
endYear = parseInt(dbYear) + 1

let data = {}
let dataCess = {}

sql = "SELECT pur_id,pur_acc,pur_prod_id,pur_prod_qty FROM somanath20"+dbYear+".purchases where pur_firm_id = 3 and pur_date >= '20"+dbYear+"-04-01' and pur_date<='20"+endYear+"-03-31'"
purchase =connection.query(sql)
try{
    purchase1 =connection.query("SELECT pur_id,pur_acc,pur_prod_id,pur_prod_qty FROM somanath20"+endYear+".purchases where pur_firm_id = 3 and and pur_date >= '20"+dbYear+"-04-01' and pur_date<='20"+endYear+"-03-31'")
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

reportFileName = path.join(homeDir , 'angadiImages' , "NGSTR04.xlsx")
const newBook = XLSX.utils.book_new();
XLSX.utils.book_append_sheet(newBook, worksheets['Sheet1'], "Sheet1");
XLSX.writeFileSync(newBook,reportFileName);

socket.emit("reportFinished" , "GSTR04" , "NGSTR04.xlsx")


})

app.post('/PrintInvoice' , files.single('file') ,(req,res) =>{
    let printOptions = {}
    if(req.query.range != '')
      {
        printOptions.range =  req.query.range
        
      }
    else
    if(req.query.even_odd != '-1')
      {

        if (req.query.even_odd == '0')
          printOptions.subset = 'odd'
        else
          printOptions.subset = 'even'

        
      }
    


    print.print(path.join(homeDir , "invoice.pdf") , printOptions )
      

    res.sendStatus(200)
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


app.listen(7000);
