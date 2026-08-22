#!/usr/bin/env node
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');
const {
  defaultConfigPath,
  defaultStateDirectory,
  getDatabaseConfig,
  loadRuntimeEnvironment,
  parseBoolean
} = require('./gstRuntimeConfig');
const { sendFailureEmail, sendSuccessEmail, validateMailConfiguration } = require('./gstMailer');
const { ensurePrinterServer, generateAndVerifyReports, stopPrinterServer } = require('./gstReportClient');
const { RunLock, StateStore, WorkflowLogger, sanitize } = require('./gstWorkflowState');

const MONTH_NAMES = [
  'JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE',
  'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER'
];

function parseArguments(argv) {
  const options = { mode: 'manual', force: false, month: null, configPath: null, help: false };
  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === '--scheduled') {
      options.mode = 'scheduled';
    } else if (argument === '--manual') {
      options.mode = 'manual';
    } else if (argument === '--force') {
      options.force = true;
    } else if (argument === '--month') {
      options.month = argv[++index];
      if (!options.month) {
        throw new Error('--month requires a YYYY-MM value');
      }
    } else if (argument === '--config') {
      options.configPath = argv[++index];
      if (!options.configPath) {
        throw new Error('--config requires a file path');
      }
    } else if (argument === '--help' || argument === '-h') {
      options.help = true;
    } else {
      throw new Error(`Unknown argument: ${argument}`);
    }
  }
  if (options.mode === 'scheduled' && options.force) {
    throw new Error('--force is allowed only for an intentional manual retry');
  }
  return options;
}

function formatLocalDate(date) {
  return [
    date.getFullYear(),
    String(date.getMonth() + 1).padStart(2, '0'),
    String(date.getDate()).padStart(2, '0')
  ].join('-');
}

function parseMonthOverride(value) {
  if (!/^\d{4}-(0[1-9]|1[0-2])$/.test(value)) {
    throw new Error('--month must use YYYY-MM, for example 2026-07');
  }
  const [year, month] = value.split('-').map(Number);
  return new Date(year, month - 1, 1);
}

function getReportingPeriod(now = new Date(), monthOverride = null) {
  const currentMonth = new Date(now.getFullYear(), now.getMonth(), 1);
  let reportingMonth;
  if (monthOverride) {
    reportingMonth = parseMonthOverride(monthOverride);
    if (reportingMonth >= currentMonth) {
      throw new Error('The reporting month must be a completed calendar month');
    }
  } else {
    reportingMonth = new Date(now.getFullYear(), now.getMonth() - 1, 1);
  }

  const endExclusive = new Date(reportingMonth.getFullYear(), reportingMonth.getMonth() + 1, 1);
  const lastDay = new Date(endExclusive.getFullYear(), endExclusive.getMonth(), 0);
  const calendarYear = reportingMonth.getFullYear();
  const calendarMonth = reportingMonth.getMonth() + 1;
  const financialYearStart = calendarMonth >= 4 ? calendarYear : calendarYear - 1;
  const quarter = calendarMonth >= 4 && calendarMonth <= 6 ? 1
    : calendarMonth >= 7 && calendarMonth <= 9 ? 2
      : calendarMonth >= 10 ? 3 : 4;
  const monthName = MONTH_NAMES[reportingMonth.getMonth()];
  const titleMonth = monthName[0] + monthName.slice(1).toLowerCase();

  return {
    monthKey: `${calendarYear}-${String(calendarMonth).padStart(2, '0')}`,
    monthName,
    displayName: `${titleMonth} ${calendarYear}`,
    startDate: formatLocalDate(reportingMonth),
    endExclusiveDate: formatLocalDate(endExclusive),
    lastDate: formatLocalDate(lastDay),
    quarter,
    quarterLabel: `Q${quarter}`,
    financialYearStart,
    financialYearTwoDigit: String(financialYearStart).slice(-2),
    financialYearLabel: `${financialYearStart}-${String(financialYearStart + 1).slice(-2)}`,
    schema: `somanath${financialYearStart}`
  };
}

function buildInvoiceRangeSql(schema) {
  if (!/^somanath\d{4}$/.test(schema)) {
    throw new Error(`Invalid financial-year schema: ${schema}`);
  }
  return `WITH ranked_data AS (
    SELECT
        trans_sales,
        insert_time,
        ROW_NUMBER() OVER (ORDER BY insert_time ASC) AS rn_first,
        ROW_NUMBER() OVER (ORDER BY insert_time DESC) AS rn_last
    FROM ${schema}.cashflow_sales
    WHERE trans_sales IS NOT NULL
      AND insert_time >= ?
      AND insert_time < ?
)
SELECT
    MAX(CASE WHEN rn_first = 1 THEN trans_sales END) AS starting_invoice,
    MAX(CASE WHEN rn_last = 1 THEN trans_sales END) AS ending_invoice
FROM ranked_data`;
}

function queryPool(pool, sql, parameters) {
  return new Promise((resolve, reject) => {
    pool.query(sql, parameters, (error, rows) => {
      if (error) {
        reject(error);
      } else {
        resolve(rows);
      }
    });
  });
}

async function getInvoiceRange(period, logger) {
  const mysql = require('mysql');
  const pool = mysql.createPool({
    connectionLimit: 2,
    ...getDatabaseConfig()
  });
  try {
    logger.info('Querying the monthly invoice range', {
      schema: period.schema,
      start: period.startDate,
      endExclusive: period.endExclusiveDate,
      field: 'insert_time',
      invoiceField: 'trans_sales'
    });
    const rows = await queryPool(
      pool,
      buildInvoiceRangeSql(period.schema),
      [period.startDate, period.endExclusiveDate]
    );
    const row = rows && rows[0];
    if (!row || !row.starting_invoice || !row.ending_invoice) {
      const error = new Error(`No invoice range exists for ${period.displayName}`);
      error.code = 'GST_NO_DATA';
      throw error;
    }
    return {
      startingInvoice: String(row.starting_invoice),
      endingInvoice: String(row.ending_invoice)
    };
  } finally {
    await new Promise((resolve) => pool.end(() => resolve()));
  }
}

function resolveDesktopDirectory() {
  if (process.env.GST_DESKTOP_DIRECTORY) {
    return process.env.GST_DESKTOP_DIRECTORY;
  }
  if (process.platform === 'win32') {
    try {
      return execFileSync(
        'powershell.exe',
        ['-NoProfile', '-NonInteractive', '-Command', '[Environment]::GetFolderPath("Desktop")'],
        { encoding: 'utf8', windowsHide: true }
      ).trim();
    } catch (_) {
      // Fall through to the portable home-directory fallback.
    }
  }
  return path.join(os.homedir(), 'Desktop');
}

function desktopErrorFilename(now = new Date()) {
  const timestamp = [
    now.getFullYear(), '-',
    String(now.getMonth() + 1).padStart(2, '0'), '-',
    String(now.getDate()).padStart(2, '0'), '_',
    String(now.getHours()).padStart(2, '0'), '-',
    String(now.getMinutes()).padStart(2, '0'), '-',
    String(now.getSeconds()).padStart(2, '0')
  ].join('');
  return `GST_Automation_Error_${timestamp}.txt`;
}

function writeDesktopError({ period, stage, error }) {
  const desktop = resolveDesktopDirectory();
  fs.mkdirSync(desktop, { recursive: true });
  const outputPath = path.join(desktop, desktopErrorFilename());
  const details = sanitize(error && error.stack ? error.stack : error);
  fs.writeFileSync(outputPath, [
    `Timestamp: ${new Date().toISOString()}`,
    `Reporting month: ${period.displayName}`,
    `Failed workflow stage: ${stage}`,
    `Error message: ${sanitize(error && error.message ? error.message : error)}`,
    '',
    'Details:',
    details,
    ''
  ].join('\n'), 'utf8');
  return outputPath;
}

function printHelp() {
  console.log(`Usage: node gstMonthlyWorkflow.js [options]

Options:
  --scheduled          Scheduled mode; obey GST_MONTHLY_AUTOMATION_ENABLED
  --manual             Manual mode (default); allowed even when scheduling is disabled
  --month YYYY-MM      Manually process a specific completed month
  --force              Intentionally resend a month with sent/uncertain email state
  --config PATH        Load environment values from PATH
  --help               Show this help

Default config path:
  ${defaultConfigPath()}`);
}

async function runWorkflow(options, now = new Date()) {
  const configResult = loadRuntimeEnvironment(options.configPath);
  const period = getReportingPeriod(now, options.month);
  const stateDirectory = process.env.GST_AUTOMATION_STATE_DIR || defaultStateDirectory();
  const logger = new WorkflowLogger(stateDirectory, period.monthKey);
  const stateStore = new StateStore(stateDirectory);
  const stateKey = `SOMANATH_STORES:${period.monthKey}`;
  const lock = new RunLock(stateDirectory, stateKey);
  let printerServer = null;
  let stage = 'initialization';
  let lockAcquired = false;

  logger.info('GST monthly workflow invoked', {
    mode: options.mode,
    reportingMonth: period.displayName,
    quarter: period.quarterLabel,
    financialYear: period.financialYearLabel,
    configFile: configResult.loaded ? configResult.configPath : 'not found; process environment/defaults used'
  });

  if (options.mode === 'scheduled' && !parseBoolean(process.env.GST_MONTHLY_AUTOMATION_ENABLED, false)) {
    logger.info('Scheduled workflow is disabled by GST_MONTHLY_AUTOMATION_ENABLED; no work performed');
    return { status: 'disabled', period, logPath: logger.logPath };
  }

  try {
    stage = 'idempotency_lock';
    lock.acquire();
    lockAcquired = true;

    const existing = stateStore.get(stateKey);
    if (existing && existing.status === 'email_sent' && !options.force) {
      logger.info('Auditor email was already sent for this month; duplicate run skipped');
      return { status: 'already_sent', period, logPath: logger.logPath };
    }
    if (existing && existing.status === 'email_sending' && !options.force) {
      stage = 'auditor_email_delivery_uncertain';
      throw new Error('A previous run stopped while sending the auditor email. Review delivery, then use --force only if an intentional resend is required.');
    }

    stateStore.update(stateKey, {
      status: 'running',
      mode: options.mode,
      reportingMonth: period.displayName,
      startedAt: new Date().toISOString(),
      forced: options.force
    });

    stage = 'printer_server_startup';
    printerServer = await ensurePrinterServer({ logger });

    const setStage = (nextStage) => {
      stage = nextStage;
      stateStore.update(stateKey, { status: 'running', stage });
    };
    const attachments = await generateAndVerifyReports({ period, logger, setStage });

    stage = 'invoice_range_query';
    stateStore.update(stateKey, { status: 'reports_ready', stage, attachments });
    const invoiceRange = await getInvoiceRange(period, logger);
    logger.info('Invoice range retrieved', invoiceRange);

    stage = 'email_construction';
    validateMailConfiguration();

    stage = 'auditor_email_delivery';
    const deterministicMessageId = `<gst-somanath-stores-${period.monthKey}@somanathstoresmaravanthe.gmail.com>`;
    stateStore.update(stateKey, {
      status: 'email_sending',
      stage,
      invoiceRange,
      attachments,
      messageId: deterministicMessageId
    });
    const mailResult = await sendSuccessEmail({
      period,
      invoiceRange,
      attachments,
      logger,
      messageId: deterministicMessageId
    });

    stage = 'record_success';
    stateStore.update(stateKey, {
      status: 'email_sent',
      stage: 'complete',
      completedAt: new Date().toISOString(),
      smtpMessageId: mailResult.messageId,
      smtpResponse: sanitize(mailResult.response || '')
    });
    logger.info('GST monthly workflow completed successfully');
    return { status: 'success', period, invoiceRange, attachments, logPath: logger.logPath };
  } catch (error) {
    const auditorEmailMayHaveBeenSent = stage === 'auditor_email_delivery'
      || stage === 'auditor_email_delivery_uncertain'
      || stage === 'record_success';
    logger.error(`GST monthly workflow failed during ${stage}`, error && error.stack ? error.stack : error);
    if (!auditorEmailMayHaveBeenSent) {
      try {
        stateStore.update(stateKey, {
          status: 'failed',
          stage,
          failedAt: new Date().toISOString(),
          error: sanitize(error && error.message ? error.message : error)
        });
      } catch (stateError) {
        logger.error('Failed to record workflow failure state', stateError);
      }
    }

    try {
      await sendFailureEmail({ period, stage, error, logger, auditorEmailMayHaveBeenSent });
    } catch (notificationError) {
      logger.error('Failure notification email could not be sent', notificationError && notificationError.stack ? notificationError.stack : notificationError);
      try {
        const combinedError = new Error(`${error.message}\n\nFailure notification error: ${notificationError.message}`);
        combinedError.stack = `${error && error.stack ? error.stack : error}\n\nFailure notification error:\n${notificationError && notificationError.stack ? notificationError.stack : notificationError}`;
        const fallbackPath = writeDesktopError({
          period,
          stage,
          error: combinedError
        });
        logger.error('Desktop fallback error file created', fallbackPath);
      } catch (fallbackError) {
        logger.error('Desktop fallback error file could not be created', fallbackError);
      }
    }
    error.workflowStage = stage;
    throw error;
  } finally {
    try {
      await stopPrinterServer(printerServer, logger);
    } catch (stopError) {
      logger.error('Could not stop workflow-started printer server cleanly', stopError);
    }
    if (lockAcquired) {
      try {
        lock.release();
      } catch (lockError) {
        logger.error('Could not release workflow lock cleanly', lockError);
      }
    }
  }
}

async function main() {
  try {
    const options = parseArguments(process.argv.slice(2));
    if (options.help) {
      printHelp();
      return;
    }
    const result = await runWorkflow(options);
    if (result.status === 'success') {
      console.log(`SUCCESS: GST workflow completed for ${result.period.displayName}`);
    } else if (result.status === 'already_sent') {
      console.log(`SKIPPED: Auditor email was already sent for ${result.period.displayName}`);
    } else if (result.status === 'disabled') {
      console.log('SKIPPED: Scheduled GST automation is disabled');
    }
  } catch (error) {
    console.error(`FAILED: ${sanitize(error && error.message ? error.message : error)}`);
    process.exitCode = 1;
  }
}

if (require.main === module) {
  main();
}

module.exports = {
  buildInvoiceRangeSql,
  desktopErrorFilename,
  formatLocalDate,
  getInvoiceRange,
  getReportingPeriod,
  parseArguments,
  parseMonthOverride,
  resolveDesktopDirectory,
  runWorkflow,
  writeDesktopError
};
