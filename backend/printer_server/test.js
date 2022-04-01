/*
    doc.lineJoin('bevel')
   .rect(0, 0, 107, 42.5)
   .stroke();
    doc 
        .fontSize(8)
        .text('MRP :',0,6.5,)
        .font('C:\\Users\\vijay\\Desktop\\Hosangadi2.0\\backend\\report_server\\Languages\\NotoFont\\static\\NotoSerifKannada-SemiBold.ttf')
        .text('₹1354.2',25,5)
        .text('ದರ : ₹1300.0',55,5)

        .font('C:\\Users\\vijay\\Desktop\\Hosangadi2.0\\backend\\report_server\\Languages\\Barcode\\LibreBarcode128-Regular.ttf')
        .fontSize(21)
        .text('S00120',30,20)
        doc.lineJoin('bevel')
        .rect(120, 0, 107, 42.5)
        .stroke();
         doc 
             .fontSize(8)
             .font('Helvetica')
             .text('MRP :',120,6.5,)
             .font('C:\\Users\\vijay\\Desktop\\Hosangadi2.0\\backend\\report_server\\Languages\\NotoFont\\static\\NotoSerifKannada-SemiBold.ttf')
             .text('₹1354.2',145,5)
             .text('ದರ : ₹1300.0',175,5)
*/
/*
             const { toBuffer } = require("bwip-js");
             const PDFDocument = require("pdfkit");
             const { createWriteStream } = require ("fs");
             
             toBuffer({
                bcid: "code128",
                text: "S00120",
              },(err,png)=>{
                  //barcode_50_25(png)
                  //barcode_38_15(png)
                  voucher_label()
              })
              
             function barcode_38_15(image){
                const count = 3
                let doc = new PDFDocument({ size: [107.5, 42.5], margins: {
                    top: 0,
                    bottom: 0,
                    left: 2,
                    right: 2
                  }
                  });
                  
                doc.pipe(createWriteStream('C:\\Users\\vijay\\Desktop\\Hosangadi2.0\\barcode.pdf'));
                for(i = 0; i<count;i++)
                {
                    console.log(i);
                    doc.image(image, 5, 20,{width: 90, height: 20,align : 'center'})
                    .fontSize(8)
                    .text('  MRP : 1231.5', 0, 2,{align: 'right'})
                    .text('Price : 1201.5', 0, 10,{align: 'right'})
                    .text('1234567890123'.slice(0,12),2,2,{align: 'left'})
                    .text('ABO',2,10,{align: 'left'})
                    if(i<count-1)
                    {doc.addPage({ size: [107.5, 42.5], margins: {
                    top: 0,
                    bottom: 0,
                    left: 2,
                    right: 2
                  }
                  });}
                  

                }  
                
                
                doc.end();
              
              }
              
              function barcode_50_25(image){
                const count = 1
                let doc = new PDFDocument({ size: [140, 70], margins: {
                    top: 0,
                    bottom: 0,
                    left: 2,
                    right: 2
                  }
                  });
                  
                doc.pipe(createWriteStream('C:\\Users\\vijay\\Desktop\\Hosangadi2.0\\barcode.pdf'));
                for(i = 0; i<count;i++)
                {
                doc
                    .fontSize(16)
                    .font('Helvetica')
                    .text('MS Freshnol'.slice(0,17),0,2,{align: 'center'})
                    .fontSize(12)
                    .text('MRP: ',17,47)
                    .font('C:\\Users\\vijay\\Desktop\\Hosangadi2.0\\backend\\report_server\\Languages\\NotoFont\\static\\NotoSerifKannada-Regular.ttf')
                    .text('ದರ   :', 20,25,{align: 'left'})
                    .fontSize(22)
                    .text('136', 20, 18,{align: 'center'})
                    .fontSize(18)
                    .text('140', 60, 40,{align: 'left',strike : true})
                    .font('C:\\Users\\vijay\\Desktop\\Hosangadi2.0\\backend\\report_server\\Languages\\NotoFont\\static\\NotoSerifKannada-ExtraLight.ttf')
                    .fontSize(14)
                    .text('₹',50, 25)
                    .text('₹',50, 43)
                    
                    if(i<count-1)
                    {
                        doc.addPage({ size: [144, 72], margins: {
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
             
              function voucher_label(){
                let doc = new PDFDocument({ size: [107.5, 42.5], margins: {
                    top: 0,
                    bottom: 0,
                    left: 2,
                    right: 2
                  }
                  })
                doc.pipe(createWriteStream('C:\\Users\\vijay\\Desktop\\Hosangadi2.0\\barcode.pdf'));
                  
                doc 
                .font('Helvetica')
                .fontSize(10)
                .text(`Raju`,0,5,{ align: "left" })
            try{
              doc
                .font('C:\\Users\\vijay\\Desktop\\Hosangadi2.0\\backend\\report_server\\Languages\\NotoFont\\static\\NotoSerifKannada-Medium.ttf')
                .fontSize(9)
                .text(`ಹಳೆ ಬಾಕಿ : ₹ 1255.2`,0,10,{ align: "right" })
                .text(`ಜಮಾ    : ₹ 15420.2`,0,18,{ align: "right" })
                .text(`ಉಳಿದ ಬಾಕಿ : ₹ 6541.3`,0,27,{ align: "right" })
            }
            catch(err){
              console.log(err);
            }
            
          
           
            doc.end();
              }
*/


   










