const path = require('path');
const { getEmailAddresses, getSmtpConfig } = require('./gstRuntimeConfig');
const { sanitize } = require('./gstWorkflowState');

function validateMailConfiguration() {
  const smtp = getSmtpConfig();
  if (!smtp.password || /^REPLACE_/i.test(smtp.password)) {
    throw new Error('GST_SMTP_PASSWORD is not configured with a Gmail App Password');
  }
  return smtp;
}

function createTransport() {
  const smtp = validateMailConfiguration();
  // Loaded lazily so date/state tests can run before dependencies are installed.
  const nodemailer = require('nodemailer');
  return nodemailer.createTransport({
    host: smtp.host,
    port: smtp.port,
    secure: smtp.secure,
    auth: { user: smtp.user, pass: smtp.password },
    connectionTimeout: 30000,
    greetingTimeout: 30000,
    socketTimeout: 60000
  });
}

async function sendSuccessEmail({ period, invoiceRange, attachments, logger, messageId }) {
  const addresses = getEmailAddresses();
  const subject = `GST Returns - SOMANATH STORES - ${period.displayName}`;
  const transporter = createTransport();
  const result = await transporter.sendMail({
    from: addresses.from,
    to: addresses.to,
    cc: addresses.cc,
    subject,
    messageId,
    text: [
      `GST Returns for SOMANATH STORES for ${period.displayName}.`,
      '',
      `Invoice Number ${invoiceRange.startingInvoice} - ${invoiceRange.endingInvoice}`,
      '',
      'Please find the GST return files attached.'
    ].join('\n'),
    attachments: attachments.map((filePath) => ({
      filename: path.basename(filePath),
      path: filePath
    }))
  });
  logger.info('Auditor email accepted by SMTP', { messageId: result.messageId, response: result.response });
  return result;
}

async function sendFailureEmail({ period, stage, error, logger, auditorEmailMayHaveBeenSent = false }) {
  const addresses = getEmailAddresses();
  const transporter = createTransport();
  const timestamp = new Date().toISOString();
  const details = sanitize(error && error.stack ? error.stack : error);
  const result = await transporter.sendMail({
    from: addresses.from,
    to: addresses.errorTo,
    subject: `[FAILED] GST Monthly Automation - SOMANATH STORES - ${period.displayName}`,
    text: [
      auditorEmailMayHaveBeenSent
        ? 'The GST monthly automation failed during or after auditor email delivery. Delivery may have occurred; review the mailbox before using --force.'
        : 'The GST monthly automation failed. No auditor email was sent by this failed run.',
      '',
      `Timestamp: ${timestamp}`,
      `Reporting month: ${period.displayName}`,
      `Workflow stage: ${stage}`,
      `Error: ${sanitize(error && error.message ? error.message : error)}`,
      '',
      'Details:',
      details
    ].join('\n')
  });
  logger.info('Failure notification email accepted by SMTP', { messageId: result.messageId, response: result.response });
  return result;
}

module.exports = { sendFailureEmail, sendSuccessEmail, validateMailConfiguration };
