const fs = require('fs');
const path = require('path');

function secretValues() {
  return Object.entries(process.env)
    .filter(([key, value]) => value && /(PASSWORD|PASS|TOKEN|SECRET|AUTH)/i.test(key))
    .map(([, value]) => String(value))
    .filter((value) => value.length >= 4)
    .sort((a, b) => b.length - a.length);
}

function sanitize(value) {
  let result = String(value ?? '');
  for (const secret of secretValues()) {
    result = result.split(secret).join('[REDACTED]');
  }
  result = result.replace(/(password|token|secret|authorization)(\s*[=:]\s*)[^\s,;]+/gi, '$1$2[REDACTED]');
  return result;
}

class WorkflowLogger {
  constructor(stateDirectory, monthKey) {
    fs.mkdirSync(stateDirectory, { recursive: true });
    this.logPath = path.join(stateDirectory, `gst-monthly-automation-${monthKey}.log`);
  }

  write(level, message, details) {
    const timestamp = new Date().toISOString();
    const suffix = details === undefined ? '' : ` ${sanitize(typeof details === 'string' ? details : JSON.stringify(details))}`;
    const line = `${timestamp} [${level}] ${sanitize(message)}${suffix}`;
    fs.appendFileSync(this.logPath, `${line}\n`, 'utf8');
    if (level === 'ERROR') {
      console.error(line);
    } else {
      console.log(line);
    }
  }

  info(message, details) {
    this.write('INFO', message, details);
  }

  error(message, details) {
    this.write('ERROR', message, details);
  }
}

class StateStore {
  constructor(stateDirectory) {
    fs.mkdirSync(stateDirectory, { recursive: true });
    this.path = path.join(stateDirectory, 'state.json');
  }

  readAll() {
    if (!fs.existsSync(this.path)) {
      return { version: 1, months: {} };
    }
    const parsed = JSON.parse(fs.readFileSync(this.path, 'utf8'));
    parsed.months = parsed.months || {};
    return parsed;
  }

  get(key) {
    return this.readAll().months[key] || null;
  }

  update(key, patch) {
    const state = this.readAll();
    state.months[key] = {
      ...(state.months[key] || {}),
      ...patch,
      updatedAt: new Date().toISOString()
    };
    const temporaryPath = `${this.path}.${process.pid}.tmp`;
    fs.writeFileSync(temporaryPath, `${JSON.stringify(state, null, 2)}\n`, 'utf8');
    fs.renameSync(temporaryPath, this.path);
    return state.months[key];
  }
}

function processExists(pid) {
  if (!Number.isInteger(pid) || pid <= 0) {
    return false;
  }
  try {
    process.kill(pid, 0);
    return true;
  } catch (error) {
    return error.code === 'EPERM';
  }
}

class RunLock {
  constructor(stateDirectory, key) {
    const safeKey = key.replace(/[^A-Za-z0-9_-]/g, '_');
    this.path = path.join(stateDirectory, `${safeKey}.lock`);
    this.handle = null;
  }

  acquire() {
    fs.mkdirSync(path.dirname(this.path), { recursive: true });
    for (let attempt = 0; attempt < 2; attempt += 1) {
      try {
        this.handle = fs.openSync(this.path, 'wx');
        fs.writeFileSync(this.handle, JSON.stringify({ pid: process.pid, startedAt: new Date().toISOString() }));
        return;
      } catch (error) {
        if (error.code !== 'EEXIST') {
          throw error;
        }

        let owner = {};
        try {
          owner = JSON.parse(fs.readFileSync(this.path, 'utf8'));
        } catch (_) {
          // An unreadable lock is handled as stale after the age check below.
        }
        const ageMs = Date.now() - fs.statSync(this.path).mtimeMs;
        if (!processExists(Number(owner.pid)) && ageMs > 5 * 60 * 1000) {
          fs.unlinkSync(this.path);
          continue;
        }
        throw new Error(`Another GST monthly workflow is already running (lock: ${this.path})`);
      }
    }
    throw new Error(`Unable to acquire GST workflow lock: ${this.path}`);
  }

  release() {
    if (this.handle !== null) {
      try {
        fs.closeSync(this.handle);
      } catch (_) {
        // Best effort during shutdown.
      }
      this.handle = null;
    }
    try {
      fs.unlinkSync(this.path);
    } catch (error) {
      if (error.code !== 'ENOENT') {
        throw error;
      }
    }
  }
}

module.exports = { RunLock, StateStore, WorkflowLogger, sanitize };
