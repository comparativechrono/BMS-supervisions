/**
 * BMS supervisions – the hand-in.
 *
 * The BMS supervisions site (https://comparativechrono.github.io/BMS-supervisions/) sends the Word document of a
 * piece of supervision work here when a student hands it in. This script checks the hand-in password, saves the
 * document in a folder of your Google Drive (a folder for each supervision), adds a line for it to a Google Sheet,
 * and sends the site a receipt.
 *
 * Setting it up (see README.md, beside this file): paste this file into a new Apps Script project
 * (script.google.com), put the hand-in password in the project's Script properties as PASSWORD, run setup() once,
 * and deploy the project as a web app (Execute as: Me; Who has access: Anyone). The password is kept only in the
 * Script properties: it is never in this file, or on the site.
 *
 * Script properties: PASSWORD (the hand-in password, which you give the students); FOLDER_ID (the folder that the
 * work goes into) and SHEET_ID (the sheet that lists it), which setup() makes if they aren't there.
 */

var VERSION = 1;
var MAX_BYTES = 10 * 1024 * 1024;            // the largest document it takes (a 40-minute essay is about 10 to 30 kB)
var DOCX = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';
var FAILS_ALLOWED = 30;                       // wrong passwords, from anyone, allowed in FAILS_WINDOW seconds;
var FAILS_WINDOW = 600;                       // after that it rests until the window is over
var FOLDER_NAME = 'BMS supervision work – handed in';
var SHEET_NAME = 'BMS supervision work – handed in (list)';
var HEADINGS = ['Handed in', 'Supervision', 'Paper', 'Name', 'Candidate number', 'Words', 'File', 'Link', 'Submitted on the site'];

/** the address of the web app, opened in a browser: says whether the hand-in is set up (and nothing else) */
function doGet() {
  return json_({ ok: true, service: 'BMS supervisions hand-in', version: VERSION, ready: !!prop_('PASSWORD') && !!prop_('FOLDER_ID') });
}

/** a hand-in from the site: a JSON body (sent as text/plain, which needs no CORS preflight) */
function doPost(e) {
  var req;
  try {
    req = JSON.parse((e && e.postData && e.postData.contents) || '{}');
  } catch (err) {
    return json_({ ok: false, error: 'request', message: 'The hand-in could not be read.' });
  }
  try {
    return json_(handIn_(req || {}));
  } catch (err) {
    console.error(err);
    return json_({ ok: false, error: 'server', message: 'The hand-in could not be saved (' + String((err && err.message) || err) + '). Try again in a moment.' });
  }
}

function handIn_(req) {
  var password = prop_('PASSWORD');
  if (!password || !prop_('FOLDER_ID')) {
    return { ok: false, error: 'setup', message: 'The hand-in has not been set up yet. Tell your supervisor.' };
  }
  // (a guard against guessing: after too many wrong passwords from anyone, it rests for a while)
  var cache = CacheService.getScriptCache();
  var fails = Number(cache.get('fails') || 0);
  if (fails >= FAILS_ALLOWED) {
    return { ok: false, error: 'busy', message: 'Too many wrong passwords have been tried. Wait ten minutes, and try again.' };
  }
  if (typeof req.password !== 'string' || !same_(req.password.trim(), password.trim())) {
    cache.put('fails', String(fails + 1), FAILS_WINDOW);
    return { ok: false, error: 'password', message: 'That isn’t the hand-in password.' };
  }
  var f = req.file || {};
  if (typeof f.data !== 'string' || !f.data) return { ok: false, error: 'file', message: 'No document came with the hand-in.' };
  if (f.data.length > Math.ceil(MAX_BYTES / 3) * 4 + 4) return { ok: false, error: 'size', message: 'The document is too big to hand in.' };
  var bytes;
  try {
    bytes = Utilities.base64Decode(f.data);
  } catch (err) {
    return { ok: false, error: 'file', message: 'The document could not be read.' };
  }
  if (bytes.length > MAX_BYTES) return { ok: false, error: 'size', message: 'The document is too big to hand in.' };
  // (a Word document is a zip file, which starts with PK)
  if (bytes.length < 4 || bytes[0] !== 0x50 || bytes[1] !== 0x4b) return { ok: false, error: 'file', message: 'That isn’t a Word document.' };

  var week = Math.max(0, Math.min(99, Math.floor(Number(req.week) || 0)));
  var name = clean_(f.name, 120).replace(/\.docx$/i, '') || 'supervision-work';
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(20000)) return { ok: false, error: 'busy', message: 'The hand-in is busy. Try again in a moment.' };
  try {
    var folder = weekFolder_(week);
    var fileName = unique_(folder, name + '.docx');
    var now = new Date();
    var tz = Session.getScriptTimeZone() || 'Europe/London';
    var when = Utilities.formatDate(now, tz, 'yyyy-MM-dd HH:mm:ss');
    var who = text_(req.name, 80);
    var number = text_(req.number, 20);
    var words = Math.max(0, Math.floor(Number(req.words) || 0));
    var file = folder.createFile(Utilities.newBlob(bytes, DOCX, fileName));
    file.setDescription('Handed in from the BMS supervisions site at ' + when + (who ? ' by ' + who : '') + (number ? ' (' + number + ')' : '') +
      '. ' + text_(req.title, 120) + (words ? ', ' + words + ' words' : '') + '.');
    log_([when, week || '', text_(req.paper, 60), who, number, words || '', fileName, file.getUrl(), text_(req.submitted, 40)]);
    var id = file.getId();
    return { ok: true, receipt: (week ? 'S' + week + '-' : '') + id.slice(-6), file: fileName, folder: folder.getName(), time: now.toISOString() };
  } finally {
    lock.releaseLock();
  }
}

/** run this once, from the editor: it makes the folder and the sheet (if they aren't there), and checks the password */
function setup() {
  var p = PropertiesService.getScriptProperties();
  var folder;
  if (p.getProperty('FOLDER_ID')) {
    folder = DriveApp.getFolderById(p.getProperty('FOLDER_ID'));
    console.log('The work goes into the folder ' + folder.getName() + ': ' + folder.getUrl());
  } else {
    folder = DriveApp.createFolder(FOLDER_NAME);
    p.setProperty('FOLDER_ID', folder.getId());
    console.log('Made the folder that the work goes into: ' + folder.getUrl());
  }
  if (!p.getProperty('SHEET_ID')) {
    var ss = SpreadsheetApp.create(SHEET_NAME);
    var sheet = ss.getSheets()[0];
    sheet.appendRow(HEADINGS);
    sheet.setFrozenRows(1);
    DriveApp.getFileById(ss.getId()).moveTo(folder);
    p.setProperty('SHEET_ID', ss.getId());
    console.log('Made the sheet that lists it: ' + ss.getUrl());
  }
  console.log(p.getProperty('PASSWORD') ? 'The password is set. Now deploy the project as a web app (see README.md).'
    : 'Now set the password: Project Settings → Script properties → Add script property → PASSWORD.');
}

// ---------------------------------------------------------------------------------------------------------------------
function weekFolder_(week) {
  var root = DriveApp.getFolderById(prop_('FOLDER_ID'));
  var name = week ? 'Supervision ' + week : 'Other work';
  var it = root.getFoldersByName(name);
  return it.hasNext() ? it.next() : root.createFolder(name);
}

/** a file name that isn't in the folder yet: "name.docx", then "name (2).docx"… (nothing is ever replaced) */
function unique_(folder, fileName) {
  if (!folder.getFilesByName(fileName).hasNext()) return fileName;
  var base = fileName.replace(/\.docx$/i, '');
  for (var n = 2; n < 1000; n++) {
    var candidate = base + ' (' + n + ').docx';
    if (!folder.getFilesByName(candidate).hasNext()) return candidate;
  }
  return base + ' (' + new Date().getTime() + ').docx';
}

function log_(row) {
  var id = prop_('SHEET_ID');
  if (!id) return;
  try {
    SpreadsheetApp.openById(id).getSheets()[0].appendRow(row);
  } catch (err) {
    console.error('The sheet could not be written: ' + err);
  }
}

/** a file name: no characters that Drive or a computer would object to */
function clean_(s, max) {
  return String(s == null ? '' : s).replace(/[\u0000-\u001f\u007f\\\/:*?"<>|]/g, ' ').replace(/\s+/g, ' ').trim().slice(0, max || 120);
}

/** text for the sheet and the file's description: one line, not too long */
function text_(s, max) {
  return String(s == null ? '' : s).replace(/[\u0000-\u001f\u007f]/g, ' ').replace(/\s+/g, ' ').trim().slice(0, max || 120);
}

/** compares two strings in the same time whatever they hold */
function same_(a, b) {
  var d = a.length ^ b.length;
  for (var i = 0; i < Math.max(a.length, b.length); i++) d |= (a.charCodeAt(i) || 0) ^ (b.charCodeAt(i) || 0);
  return d === 0;
}

function prop_(key) {
  return PropertiesService.getScriptProperties().getProperty(key);
}

function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}
