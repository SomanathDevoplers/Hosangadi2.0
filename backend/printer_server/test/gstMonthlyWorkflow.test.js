'use strict';

const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const test = require('node:test');
const {
  buildInvoiceRangeSql,
  desktopErrorFilename,
  getReportingPeriod,
  parseArguments,
  runWorkflow
} = require('../gstMonthlyWorkflow');
const { parseEnvironmentFile } = require('../gstRuntimeConfig');
const { RunLock, StateStore } = require('../gstWorkflowState');

test('August run processes July in the same financial-year schema', () => {
  const period = getReportingPeriod(new Date(2026, 7, 22, 10, 0, 0));
  assert.equal(period.monthKey, '2026-07');
  assert.equal(period.displayName, 'July 2026');
  assert.equal(period.startDate, '2026-07-01');
  assert.equal(period.endExclusiveDate, '2026-08-01');
  assert.equal(period.lastDate, '2026-07-31');
  assert.equal(period.quarter, 2);
  assert.equal(period.financialYearLabel, '2026-27');
  assert.equal(period.financialYearTwoDigit, '26');
  assert.equal(period.schema, 'somanath2026');
});

test('January run processes December of the prior calendar year', () => {
  const period = getReportingPeriod(new Date(2027, 0, 7, 10, 0, 0));
  assert.equal(period.monthKey, '2026-12');
  assert.equal(period.displayName, 'December 2026');
  assert.equal(period.quarter, 3);
  assert.equal(period.schema, 'somanath2026');
});

test('January through March belong to the financial year starting the prior year', () => {
  const period = getReportingPeriod(new Date(2027, 3, 1), '2027-03');
  assert.equal(period.quarter, 4);
  assert.equal(period.financialYearLabel, '2026-27');
  assert.equal(period.schema, 'somanath2026');
});

test('manual override rejects current or future months', () => {
  assert.throws(
    () => getReportingPeriod(new Date(2026, 7, 22), '2026-08'),
    /completed calendar month/
  );
});

test('invoice query preserves insert_time and trans_sales semantics', () => {
  const sql = buildInvoiceRangeSql('somanath2026');
  assert.match(sql, /FROM somanath2026\.cashflow_sales/);
  assert.match(sql, /trans_sales IS NOT NULL/);
  assert.match(sql, /insert_time >= \?/);
  assert.match(sql, /insert_time < \?/);
  assert.match(sql, /ORDER BY insert_time ASC/);
  assert.match(sql, /ORDER BY insert_time DESC/);
  assert.throws(() => buildInvoiceRangeSql('somanath2026; DROP DATABASE somanath'), /Invalid/);
});

test('scheduled execution cannot force an auditor resend', () => {
  assert.throws(() => parseArguments(['--scheduled', '--force']), /manual retry/);
  assert.deepEqual(parseArguments(['--manual', '--month', '2026-07']), {
    mode: 'manual',
    force: false,
    month: '2026-07',
    configPath: null,
    help: false
  });
});

test('environment file parser handles comments, whitespace and quoted values', () => {
  const parsed = parseEnvironmentFile([
    '# comment',
    'GST_MONTHLY_AUTOMATION_ENABLED = true',
    'GST_SMTP_PASSWORD="abcd efgh"',
    'INVALID LINE'
  ].join('\n'));
  assert.equal(parsed.GST_MONTHLY_AUTOMATION_ENABLED, 'true');
  assert.equal(parsed.GST_SMTP_PASSWORD, 'abcd efgh');
});

test('state updates are persisted and a concurrent run lock is rejected', () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'gst-workflow-test-'));
  try {
    const store = new StateStore(directory);
    store.update('SOMANATH_STORES:2026-07', { status: 'running' });
    assert.equal(store.get('SOMANATH_STORES:2026-07').status, 'running');
    store.update('SOMANATH_STORES:2026-07', { status: 'reports_ready' });
    assert.equal(store.get('SOMANATH_STORES:2026-07').status, 'reports_ready');

    const first = new RunLock(directory, 'SOMANATH_STORES:2026-07');
    const second = new RunLock(directory, 'SOMANATH_STORES:2026-07');
    first.acquire();
    assert.throws(() => second.acquire(), /already running/);
    first.release();
    second.acquire();
    second.release();
  } finally {
    fs.rmSync(directory, { recursive: true, force: true });
  }
});

test('desktop fallback filename uses the requested stable format', () => {
  const name = desktopErrorFilename(new Date(2026, 6, 8, 9, 4, 3));
  assert.equal(name, 'GST_Automation_Error_2026-07-08_09-04-03.txt');
});

test('uncertain auditor delivery is not changed to retryable failed state', async () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'gst-uncertain-test-'));
  const oldValues = {
    state: process.env.GST_AUTOMATION_STATE_DIR,
    desktop: process.env.GST_DESKTOP_DIRECTORY,
    smtpPassword: process.env.GST_SMTP_PASSWORD
  };
  const oldConsoleLog = console.log;
  const oldConsoleError = console.error;
  process.env.GST_AUTOMATION_STATE_DIR = directory;
  process.env.GST_DESKTOP_DIRECTORY = path.join(directory, 'Desktop');
  process.env.GST_SMTP_PASSWORD = '';
  console.log = () => {};
  console.error = () => {};
  try {
    const store = new StateStore(directory);
    const key = 'SOMANATH_STORES:2026-07';
    store.update(key, { status: 'email_sending' });

    await assert.rejects(
      () => runWorkflow({ mode: 'manual', force: false, month: '2026-07', configPath: path.join(directory, 'missing.env') }, new Date(2026, 7, 22)),
      /Review delivery/
    );
    assert.equal(store.get(key).status, 'email_sending');
    const fallbackFiles = fs.readdirSync(path.join(directory, 'Desktop'));
    assert.equal(fallbackFiles.length, 1);
    assert.match(fallbackFiles[0], /^GST_Automation_Error_/);
  } finally {
    if (oldValues.state === undefined) delete process.env.GST_AUTOMATION_STATE_DIR;
    else process.env.GST_AUTOMATION_STATE_DIR = oldValues.state;
    if (oldValues.desktop === undefined) delete process.env.GST_DESKTOP_DIRECTORY;
    else process.env.GST_DESKTOP_DIRECTORY = oldValues.desktop;
    if (oldValues.smtpPassword === undefined) delete process.env.GST_SMTP_PASSWORD;
    else process.env.GST_SMTP_PASSWORD = oldValues.smtpPassword;
    console.log = oldConsoleLog;
    console.error = oldConsoleError;
    fs.rmSync(directory, { recursive: true, force: true });
  }
});
