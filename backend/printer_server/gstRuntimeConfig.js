const fs = require('fs');
const os = require('os');
const path = require('path');

const DEFAULT_DB_CONFIG = Object.freeze({
  host: 'localhost',
  port: 3306,
  user: 'root',
  password: 'mysqlpassword5'
});

function defaultStateDirectory() {
  const base = process.env.LOCALAPPDATA || path.join(os.homedir(), 'AppData', 'Local');
  return path.join(base, 'Hosangadi', 'gst-monthly-automation');
}

function defaultConfigPath() {
  return path.join(__dirname, '.env');
}

function unquote(value) {
  if (value.length >= 2) {
    const first = value[0];
    const last = value[value.length - 1];
    if ((first === '"' && last === '"') || (first === "'" && last === "'")) {
      return value.slice(1, -1);
    }
  }
  return value;
}

function parseEnvironmentFile(contents) {
  const values = {};
  for (const originalLine of contents.split(/\r?\n/)) {
    const line = originalLine.trim();
    if (!line || line.startsWith('#')) {
      continue;
    }

    const separator = line.indexOf('=');
    if (separator <= 0) {
      continue;
    }

    const key = line.slice(0, separator).trim();
    const value = unquote(line.slice(separator + 1).trim());
    if (/^[A-Z_][A-Z0-9_]*$/i.test(key)) {
      values[key] = value;
    }
  }
  return values;
}

function loadRuntimeEnvironment(explicitPath) {
  const configPath = explicitPath || process.env.GST_MONTHLY_AUTOMATION_CONFIG || defaultConfigPath();
  if (!fs.existsSync(configPath)) {
    return { configPath, loaded: false };
  }

  const values = parseEnvironmentFile(fs.readFileSync(configPath, 'utf8'));
  for (const [key, value] of Object.entries(values)) {
    if (process.env[key] === undefined) {
      process.env[key] = value;
    }
  }
  return { configPath, loaded: true };
}

function parseBoolean(value, defaultValue = false) {
  if (value === undefined || value === null || value === '') {
    return defaultValue;
  }
  return /^(1|true|yes|on)$/i.test(String(value).trim());
}

function parsePositiveInteger(value, defaultValue, name) {
  if (value === undefined || value === null || value === '') {
    return defaultValue;
  }
  const parsed = Number(value);
  if (!Number.isInteger(parsed) || parsed <= 0) {
    throw new Error(`${name} must be a positive integer`);
  }
  return parsed;
}

function getDatabaseConfig() {
  return {
    host: process.env.GST_DB_HOST || DEFAULT_DB_CONFIG.host,
    port: parsePositiveInteger(process.env.GST_DB_PORT, DEFAULT_DB_CONFIG.port, 'GST_DB_PORT'),
    user: process.env.GST_DB_USER || DEFAULT_DB_CONFIG.user,
    password: process.env.GST_DB_PASSWORD || DEFAULT_DB_CONFIG.password,
    connectTimeout: parsePositiveInteger(process.env.GST_DB_CONNECT_TIMEOUT_MS, 15000, 'GST_DB_CONNECT_TIMEOUT_MS'),
    multipleStatements: false
  };
}

function getSmtpConfig() {
  const port = parsePositiveInteger(process.env.GST_SMTP_PORT, 465, 'GST_SMTP_PORT');
  return {
    host: process.env.GST_SMTP_HOST || 'smtp.gmail.com',
    port,
    secure: parseBoolean(process.env.GST_SMTP_SECURE, port === 465),
    user: process.env.GST_SMTP_USER || 'somanathstoresmaravanthe@gmail.com',
    password: process.env.GST_SMTP_PASSWORD || ''
  };
}

function getEmailAddresses() {
  return {
    from: process.env.GST_EMAIL_FROM || 'somanathstoresmaravanthe@gmail.com',
    to: process.env.GST_EMAIL_TO || 'jathindra_co@yahoo.com',
    cc: process.env.GST_EMAIL_CC || 'vshivanand2@gmail.com',
    errorTo: process.env.GST_ERROR_EMAIL_TO || 'vshivanand2@gmail.com'
  };
}

module.exports = {
  DEFAULT_DB_CONFIG,
  defaultConfigPath,
  defaultStateDirectory,
  getDatabaseConfig,
  getEmailAddresses,
  getSmtpConfig,
  loadRuntimeEnvironment,
  parseBoolean,
  parseEnvironmentFile,
  parsePositiveInteger
};
