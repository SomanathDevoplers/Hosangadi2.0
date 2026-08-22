const fs = require('fs');
const http = require('http');
const os = require('os');
const path = require('path');
const { execFile, spawn } = require('child_process');

class NoDataError extends Error {
  constructor(message) {
    super(message);
    this.name = 'NoDataError';
    this.code = 'GST_NO_DATA';
  }
}

function request({ hostname = '127.0.0.1', port = 7000, pathname, params = {}, timeoutMs = 30000 }) {
  const query = new URLSearchParams(params).toString();
  const requestPath = query ? `${pathname}?${query}` : pathname;
  return new Promise((resolve, reject) => {
    const req = http.get({ hostname, port, path: requestPath, timeout: timeoutMs }, (res) => {
      const chunks = [];
      res.on('data', (chunk) => chunks.push(chunk));
      res.on('end', () => resolve({
        statusCode: res.statusCode,
        body: Buffer.concat(chunks).toString('utf8')
      }));
    });
    req.on('timeout', () => req.destroy(new Error(`HTTP request timed out after ${timeoutMs} ms`)));
    req.on('error', reject);
  });
}

async function waitForHealth({ timeoutMs = 30000 }) {
  const deadline = Date.now() + timeoutMs;
  let lastError;
  while (Date.now() < deadline) {
    try {
      const response = await request({ pathname: '/health', timeoutMs: 3000 });
      if (response.statusCode === 200 && response.body.includes('printer_server')) {
        return;
      }
      lastError = new Error(`Unexpected printer server health response: HTTP ${response.statusCode}`);
    } catch (error) {
      lastError = error;
    }
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }
  throw new Error(`Printer server was unavailable after ${timeoutMs} ms: ${lastError ? lastError.message : 'unknown error'}`);
}

async function ensurePrinterServer({ logger }) {
  try {
    await waitForHealth({ timeoutMs: 3000 });
    logger.info('Using the already-running printer server on port 7000');
    return { child: null, startedByWorkflow: false };
  } catch (_) {
    logger.info('Printer server is not running; starting it for this workflow');
  }

  const serverPath = path.join(__dirname, 'printerServer.js');
  const logDescriptor = logger.logPath ? fs.openSync(logger.logPath, 'a') : null;
  const child = spawn(process.execPath, [serverPath], {
    cwd: __dirname,
    env: process.env,
    windowsHide: true,
    stdio: ['ignore', logDescriptor === null ? 'ignore' : logDescriptor, logDescriptor === null ? 'ignore' : logDescriptor]
  });
  if (logDescriptor !== null) {
    fs.closeSync(logDescriptor);
  }

  try {
    await Promise.race([
      waitForHealth({ timeoutMs: 30000 }),
      new Promise((_, reject) => child.once('exit', (code, signal) => {
        reject(new Error(`Printer server exited before completion (code=${code}, signal=${signal || 'none'})`));
      }))
    ]);
    return { child, startedByWorkflow: true };
  } catch (error) {
    await terminateChildProcessTree(child);
    throw error;
  }
}

function terminateChildProcessTree(child) {
  if (!child || child.killed || child.exitCode !== null) {
    return Promise.resolve();
  }
  if (process.platform !== 'win32') {
    child.kill('SIGTERM');
    return Promise.resolve();
  }
  return new Promise((resolve) => {
    execFile(
      'taskkill.exe',
      ['/PID', String(child.pid), '/T', '/F'],
      { windowsHide: true },
      (error) => {
        if (error && child.exitCode === null && !child.killed) {
          child.kill();
        }
        resolve()
      }
    );
  });
}

async function stopPrinterServer(server, logger) {
  if (!server || !server.startedByWorkflow || !server.child || server.child.killed || server.child.exitCode !== null) {
    return;
  }
  logger.info('Stopping the printer server started by this workflow');
  const exitPromise = new Promise((resolve) => server.child.once('exit', resolve));
  await terminateChildProcessTree(server.child);
  await Promise.race([
    exitPromise,
    new Promise((resolve) => setTimeout(resolve, 5000))
  ]);
}

function snapshot(filePath) {
  try {
    const stat = fs.statSync(filePath);
    return { exists: true, mtimeMs: stat.mtimeMs, size: stat.size };
  } catch (error) {
    if (error.code === 'ENOENT') {
      return { exists: false, mtimeMs: 0, size: 0 };
    }
    throw error;
  }
}

async function waitForFreshStableFile(filePath, before, startedAt, timeoutMs) {
  const deadline = Date.now() + timeoutMs;
  let previousSize = -1;
  let stableCount = 0;
  while (Date.now() < deadline) {
    const current = snapshot(filePath);
    const changed = current.exists && (
      !before.exists ||
      current.mtimeMs > before.mtimeMs ||
      current.size !== before.size
    );
    const belongsToRun = current.mtimeMs >= startedAt - 2000;
    if (changed && belongsToRun && current.size > 0) {
      if (current.size === previousSize) {
        stableCount += 1;
      } else {
        stableCount = 0;
      }
      previousSize = current.size;
      if (stableCount >= 1) {
        return current;
      }
    }
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }
  throw new Error(`Generated report did not appear or stabilize within ${timeoutMs} ms: ${filePath}`);
}

function verifyTextReport(filePath, monthName) {
  const contents = fs.readFileSync(filePath, 'utf8');
  if (!contents.trim()) {
    throw new Error(`Generated Exempted report is empty: ${filePath}`);
  }
  if (!contents.toUpperCase().includes(monthName)) {
    throw new Error(`Generated Exempted report does not identify ${monthName}: ${filePath}`);
  }
}

function verifyWorkbook(filePath, requiredSheets) {
  const XLSX = require('xlsx');
  const workbook = XLSX.readFile(filePath, { bookSheets: true });
  for (const sheet of requiredSheets) {
    if (!workbook.SheetNames.includes(sheet)) {
      throw new Error(`Generated workbook ${path.basename(filePath)} is missing worksheet ${sheet}`);
    }
  }
}

async function generateReport({ pathname, params, files, logger, noDataMessage }) {
  const timeoutMs = Number(process.env.GST_REPORT_TIMEOUT_MS || 15 * 60 * 1000);
  const startedAt = Date.now();
  const before = new Map(files.map((filePath) => [filePath, snapshot(filePath)]));
  const response = await request({ pathname, params, timeoutMs });
  if (response.statusCode === 201) {
    throw new NoDataError(noDataMessage);
  }
  if (response.statusCode !== 200) {
    throw new Error(`${pathname} failed with HTTP ${response.statusCode}: ${response.body}`);
  }

  for (const filePath of files) {
    await waitForFreshStableFile(filePath, before.get(filePath), startedAt, timeoutMs);
    logger.info('Fresh report file generated', { file: filePath, size: fs.statSync(filePath).size });
  }
}

async function generateAndVerifyReports({ period, logger, setStage = () => {} }) {
  const outputDirectory = path.join(os.homedir(), 'angadiImages');
  fs.mkdirSync(outputDirectory, { recursive: true });

  const exempted = path.join(outputDirectory, `Exempted_${period.monthName}.txt`);
  const purchase = path.join(outputDirectory, `Purchase_${period.monthName}.xlsx`);
  const sales = path.join(outputDirectory, `GSTR1_${period.monthName}.xlsx`);

  setStage('purchase_report_generation');
  logger.info('Starting Purchase and Exempted report generation');
  await generateReport({
    pathname: '/PurchaseReport',
    params: {
      firm: '1',
      dbYear: period.financialYearTwoDigit,
      year: period.financialYearLabel,
      firstDay: period.startDate,
      lastDay: period.lastDate,
      month: period.monthName
    },
    files: [purchase, exempted],
    logger,
    noDataMessage: `No purchase data exists for SOMANATH STORES for ${period.displayName}`
  });
  verifyWorkbook(purchase, ['Read Me', 'Purchase Reigster']);
  verifyTextReport(exempted, period.monthName);
  logger.info('Purchase and Exempted reports verified');

  setStage('sales_gstr1_report_generation');
  logger.info('Starting Sales/GSTR1 report generation');
  await generateReport({
    pathname: '/SalesReport',
    params: {
      firm: 'SSM',
      dbYear: period.financialYearTwoDigit,
      firstDay: period.startDate,
      lastDay: period.lastDate,
      month: period.monthName
    },
    files: [sales],
    logger,
    noDataMessage: `No sales data exists for SOMANATH STORES for ${period.displayName}`
  });
  verifyWorkbook(sales, ['Help Instruction', 'b2cs', 'exemp', 'hsn', 'docs']);
  logger.info('Sales/GSTR1 report verified');

  return [exempted, purchase, sales];
}

module.exports = {
  NoDataError,
  ensurePrinterServer,
  generateAndVerifyReports,
  request,
  snapshot,
  stopPrinterServer,
  terminateChildProcessTree,
  verifyTextReport,
  verifyWorkbook,
  waitForFreshStableFile
};
