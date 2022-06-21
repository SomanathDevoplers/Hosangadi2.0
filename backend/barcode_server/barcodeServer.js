
const print = require("pdf-to-printer");
const express = require('express')
const app = express()

const homeDir = require('os').homedir()
const { createWriteStream ,writeFileSync} = require ("fs");
const PDFDocument = require("pdfkit"); 
const { toBuffer } = require("bwip-js");


function barcode_50_25(image,name,mrp,cp,sp,count,slno){

    let doc = new PDFDocument({ size: [141.7, 70.8], margins: {
        top: 0,
        bottom: 0,
        left: 2,
        right: 2
      }
      });
    doc.pipe(createWriteStream(homeDir + '\\Desktop\\Invoices\\barcode\\'+slno+'.pdf'));
    for(i = 0; i<count;i++)
    {   
        if(parseFloat(mrp)>99){
          mrp = mrp.split('.')[0]
          sp =sp.split('.')[0]
        }
        sp+=" "
        x = ''
        y='center'
        if(parseFloat(mrp)>parseFloat(sp)){
          x = ` MRP:${"Rs"}${mrp}`
          y='right'
        }
        
        doc.image(image, 26, 33,{width: 90, height: 20,align : 'center'})
          .fontSize(10)
          .text(`${cp}`, 0, 56,{align: 'center'})
          .text(`Price:${"Rs"}${sp}`, 0, 20,{align: y})
          .text(`${name}`.slice(0,20),4,8,{align: 'center'})
          .text(x,0,20,{align: 'left'})
          if(i<count-1)
          {
            doc.addPage({
                        size: [141.7, 70.8], 
                        margins: 
                        {
                          top: 0,
                          bottom: 0,
                          left: 2,
                          right: 2
                        }
                      });
          }
        }
    doc.end();
  }



app.get('/Barcode', (req,res) =>{
    toBuffer({bcid: "code128",text: req.query.barcode.split(':')[1],},
            (err,png)=>{
            barcode_50_25(png,req.query.name,req.query.mrp,req.query.cp,req.query.sp,req.query.count,req.query.slno)
            print.print(homeDir + '\\Desktop\\Invoices\\barcode\\'+req.query.slno+'.pdf', {printer: "BarcodePrinter",orientation :"landscape"}).then(res.sendStatus(200))
        })
      })



app.listen(8000);