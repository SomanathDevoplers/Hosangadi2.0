const path = require('path');

module.exports = {
  apps: [
    { name: 'hosangadi-socket', script: 'socketServer.js', cwd: path.join(__dirname, 'socket_server') },
    { name: 'hosangadi-product', script: 'productServer.js', cwd: path.join(__dirname, 'product_server') },
    { name: 'hosangadi-report', script: 'reportServer.js', cwd: path.join(__dirname, 'report_server') },
    { name: 'hosangadi-printer', script: 'printerServer.js', cwd: path.join(__dirname, 'printer_server') },
    { name: 'hosangadi-barcode', script: 'barcodeServer.js', cwd: path.join(__dirname, 'barcode_server') }
  ]
};
