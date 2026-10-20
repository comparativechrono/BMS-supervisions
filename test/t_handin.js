/* The hand-in script (handin/Code.gs), run in Node with stand-ins for the Apps Script services that it uses
   (PropertiesService, CacheService, LockService, Utilities, Session, DriveApp, SpreadsheetApp, ContentService): the
   setup, the password and its guard against guessing, the checks on the document, where it is saved and under what
   name (nothing is ever replaced), the sheet, and the replies that the site reads.
   Run:  node test/t_handin.js */
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

let failed = 0;
const check = (ok, what) => {
  console.log((ok ? 'PASS ' : 'FAIL ') + what);
  if (!ok) failed++;
};

/* ---------------- stand-ins for the Apps Script services ---------------- */
function services() {
  const props = {};
  const cache = {};
  let nid = 0;
  const id = (p) => p + String(++nid).padStart(4, '0') + 'xYzAbC';
  const iterator = (list) => {
    let i = 0;
    return { hasNext: () => i < list.length, next: () => list[i++] };
  };
  const files = {};
  function Folder(name, parent) {
    this.id = id('fold');
    this.name = name;
    this.parent = parent;
    this.folders = [];
    this.files = [];
  }
  Folder.prototype.getId = function () { return this.id; };
  Folder.prototype.getName = function () { return this.name; };
  Folder.prototype.getUrl = function () { return 'https://drive.google.com/drive/folders/' + this.id; };
  Folder.prototype.getFoldersByName = function (n) { return iterator(this.folders.filter((f) => f.name === n)); };
  Folder.prototype.getFilesByName = function (n) { return iterator(this.files.filter((f) => f.name === n)); };
  Folder.prototype.createFolder = function (n) {
    const f = new Folder(n, this);
    this.folders.push(f);
    folders[f.id] = f;
    return f;
  };
  Folder.prototype.createFile = function (blob) {
    const f = { id: id('file'), name: blob.name, bytes: blob.bytes, type: blob.type, description: '', folder: this };
    f.getId = () => f.id;
    f.getUrl = () => 'https://drive.google.com/file/d/' + f.id + '/view';
    f.setDescription = (d) => { f.description = d; return f; };
    f.moveTo = (folder) => { folder.files.push(f); return f; };
    this.files.push(f);
    files[f.id] = f;
    return f;
  };
  const root = new Folder('My Drive');
  const folders = {};
  const sheets = {};
  let locked = false;
  const S = {
    PropertiesService: { getScriptProperties: () => ({ getProperty: (k) => (k in props ? props[k] : null), setProperty: (k, v) => { props[k] = String(v); } }) },
    CacheService: { getScriptCache: () => ({ get: (k) => (k in cache ? cache[k] : null), put: (k, v) => { cache[k] = String(v); } }) },
    LockService: { getScriptLock: () => ({ tryLock: () => (locked ? false : (locked = true)), releaseLock: () => { locked = false; } }) },
    Utilities: {
      // (Apps Script's bytes are Java's: signed, -128 to 127)
      base64Decode: (s) => {
        if (!/^[A-Za-z0-9+/]*={0,2}$/.test(s)) throw new Error('Could not decode string.');
        return Array.from(Buffer.from(s, 'base64')).map((b) => (b > 127 ? b - 256 : b));
      },
      newBlob: (bytes, type, name) => ({ bytes, type, name }),
      formatDate: (d) => d.toISOString().replace('T', ' ').slice(0, 19)
    },
    Session: { getScriptTimeZone: () => 'Europe/London' },
    DriveApp: {
      createFolder: (n) => root.createFolder(n),
      getFolderById: (i) => { if (!folders[i]) throw new Error('No item with the given ID could be found.'); return folders[i]; },
      getFileById: (i) => files[i]
    },
    SpreadsheetApp: {
      create: (n) => {
        const rows = [];
        const sh = { appendRow: (r) => rows.push(r), setFrozenRows: () => {} };
        const ss = root.createFile({ name: n, bytes: [], type: 'sheet' });
        root.files.pop();
        sheets[ss.id] = { rows, ss };
        return { getId: () => ss.id, getUrl: () => 'https://docs.google.com/spreadsheets/d/' + ss.id, getSheets: () => [sh] };
      },
      openById: (i) => ({ getSheets: () => [{ appendRow: (r) => sheets[i].rows.push(r) }] })
    },
    ContentService: {
      MimeType: { JSON: 'application/json' },
      createTextOutput: (t) => ({ text: t, mime: 'text/plain', setMimeType(m) { this.mime = m; return this; }, getContent() { return this.text; } })
    },
    console: { log: () => {}, error: () => {} }
  };
  return { S, props, cache, root, folders, sheets, files };
}

function load(env) {
  const code = fs.readFileSync(path.join(__dirname, '..', 'handin', 'Code.gs'), 'utf8');
  const ctx = vm.createContext(Object.assign({}, env.S));
  vm.runInContext(code, ctx, { filename: 'Code.gs' });
  return ctx;
}
const reply = (out) => {
  check(out && out.mime === 'application/json', '(the reply is JSON)');
  return JSON.parse(out.getContent());
};
const post = (G, body) => reply(G.doPost({ postData: { contents: typeof body === 'string' ? body : JSON.stringify(body), type: 'text/plain' } }));

// a small Word document (a zip file: PK…), as the site sends it
const docx = Buffer.concat([Buffer.from('PK\u0003\u0004'), Buffer.alloc(3000, 7)]).toString('base64');
const hand = (over) => Object.assign({ v: 1, password: 'right horse battery', paper: 's1-essay', week: 1, title: 'Supervision 1 essay', name: 'Ada Lovelace',
  number: 'B4827', words: 912, submitted: '2026-10-20T16:13:03.189Z', file: { name: 'supervision-1-essay-ada-lovelace.docx', type: 'docx', data: docx } }, over || {});

/* ---------------- before it is set up ---------------- */
let env = services();
let G = load(env);
let r = reply(G.doGet());
check(r.ok === true && r.ready === false && r.service === 'BMS supervisions hand-in', `before setup, the address says it isn't ready: ${JSON.stringify(r)}`);
r = post(G, hand());
check(r.ok === false && r.error === 'setup', `a hand-in before setup is refused, and says why: ${r.message}`);

/* ---------------- setup ---------------- */
G.setup();
check(!!env.props.FOLDER_ID && !!env.props.SHEET_ID, 'setup() makes the folder and the sheet, and keeps their ids');
const root = env.folders[env.props.FOLDER_ID];
check(root && root.name === 'BMS supervision work – handed in', `the folder is called ${root && root.name}`);
check(env.sheets[env.props.SHEET_ID].rows[0].join('|') === 'Handed in|Supervision|Paper|Name|Candidate number|Words|File|Link|Submitted on the site', 'the sheet has its headings');
const before = { f: env.props.FOLDER_ID, s: env.props.SHEET_ID };
G.setup();
check(env.props.FOLDER_ID === before.f && env.props.SHEET_ID === before.s && env.root.folders.length === 1, 'running setup() again changes nothing');
r = post(G, hand());
check(r.ok === false && r.error === 'setup', 'without a password, it still refuses');
env.props.PASSWORD = 'right horse battery';
r = reply(G.doGet());
check(r.ok && r.ready === true && !('password' in r) && !JSON.stringify(r).includes('horse'), 'with the password set it is ready, and the address never shows the password');

/* ---------------- the password ---------------- */
r = post(G, hand({ password: 'wrong' }));
check(r.ok === false && r.error === 'password' && env.cache.fails === '1', `a wrong password is refused (and counted): ${r.message}`);
r = post(G, hand({ password: undefined }));
check(r.ok === false && r.error === 'password', 'so is none at all');
check(root.folders.length === 0, 'and nothing is saved');
r = post(G, hand({ password: '  right horse battery ' }));
check(r.ok === true, 'spaces typed around the password don’t matter');

/* ---------------- a hand-in ---------------- */
env = services();
G = load(env);
G.setup();
env.props.PASSWORD = 'right horse battery';
r = post(G, hand());
const f1 = env.folders[env.props.FOLDER_ID].folders[0];
check(r.ok === true && f1 && f1.name === 'Supervision 1' && f1.files.length === 1, `the right password saves the document, in a folder for the supervision: ${JSON.stringify(r)}`);
const saved = f1.files[0];
check(saved.name === 'supervision-1-essay-ada-lovelace.docx' && saved.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', `under its own name, as a Word document (${saved.name})`);
check(Buffer.from(saved.bytes.map((b) => (b < 0 ? b + 256 : b))).toString('base64') === docx, 'byte for byte as it was sent');
check(/Ada Lovelace/.test(saved.description) && /B4827/.test(saved.description) && /912 words/.test(saved.description), `its description says whose it is: ${saved.description}`);
check(r.receipt === 'S1-' + saved.id.slice(-6) && r.file === saved.name && r.folder === 'Supervision 1' && !isNaN(Date.parse(r.time)), `the reply is a receipt: ${r.receipt}, ${r.file}, ${r.folder}`);
const row = env.sheets[env.props.SHEET_ID].rows[1];
check(row && row[1] === 1 && row[2] === 's1-essay' && row[3] === 'Ada Lovelace' && row[4] === 'B4827' && row[5] === 912 && row[6] === saved.name && row[7] === saved.getUrl() && row[8] === '2026-10-20T16:13:03.189Z',
  `the sheet gets a line for it: ${JSON.stringify(row)}`);
r = post(G, hand());
check(r.ok && f1.files.length === 2 && f1.files[1].name === 'supervision-1-essay-ada-lovelace (2).docx', `handing in again keeps both: ${f1.files.map((f) => f.name)}`);
r = post(G, hand());
check(f1.files[2].name === 'supervision-1-essay-ada-lovelace (3).docx', 'and a third time');
r = post(G, hand({ week: 2, paper: 's2-essay', file: { name: 'supervision-2-essay-ada-lovelace.docx', data: docx } }));
check(r.ok && env.folders[env.props.FOLDER_ID].folders.map((f) => f.name).join() === 'Supervision 1,Supervision 2', 'another supervision’s work goes in a folder of its own');
r = post(G, hand({ week: 0 }));
check(r.ok && r.folder === 'Other work' && r.receipt.indexOf('S') !== 0, 'work with no supervision goes in Other work');

/* ---------------- what it refuses ---------------- */
r = post(G, hand({ file: {} }));
check(!r.ok && r.error === 'file', `no document: ${r.message}`);
r = post(G, hand({ file: { name: 'x.docx', data: Buffer.from('not a word document').toString('base64') } }));
check(!r.ok && r.error === 'file', `something that isn't a Word document: ${r.message}`);
r = post(G, hand({ file: { name: 'x.docx', data: '%%% not base64 %%%' } }));
check(!r.ok && r.error === 'file', `a document that can't be read: ${r.message}`);
r = post(G, hand({ file: { name: 'x.docx', data: 'A'.repeat(14 * 1024 * 1024) } }));
check(!r.ok && r.error === 'size', `a document that is too big: ${r.message}`);
r = post(G, 'this is not JSON');
check(!r.ok && r.error === 'request', `a request that isn't JSON: ${r.message}`);
r = post(G, hand({ name: 'Ada\u0000 <Lovelace>\n', file: { name: '../../etc/pass:wd?.docx', data: docx } }));
const odd = env.folders[env.props.FOLDER_ID].folders[0].files.slice(-1)[0];
check(r.ok && !/[\\/:*?"<>|\u0000-\u001f]/.test(odd.name) && /\.docx$/.test(odd.name), `a file name is made safe: ${odd.name}`);
check(env.sheets[env.props.SHEET_ID].rows.slice(-1)[0][3] === 'Ada <Lovelace>', 'and so is the name in the sheet (one line, no control characters)');

/* ---------------- guessing ---------------- */
env.cache.fails = '0';
for (let i = 0; i < 30; i++) post(G, hand({ password: 'guess ' + i }));
r = post(G, hand());
check(!r.ok && r.error === 'busy', `after 30 wrong passwords it rests, even for the right one: ${r.message}`);
delete env.cache.fails;
r = post(G, hand());
check(r.ok, 'and works again when the ten minutes are over');

/* ---------------- one at a time ---------------- */
const lock = env.S.LockService.getScriptLock();
lock.tryLock();
r = post(G, hand());
check(!r.ok && r.error === 'busy', 'while another hand-in is being saved, it says to try again');
lock.releaseLock();
check(post(G, hand()).ok, 'and then it works');

/* ---------------- an error while saving ---------------- */
const orig = env.S.DriveApp.getFolderById;
env.S.DriveApp.getFolderById = () => { throw new Error('Drive is down'); };
G = load(env);
r = post(G, hand());
check(!r.ok && r.error === 'server' && /Drive is down/.test(r.message), `an error while saving is reported: ${r.message}`);
env.S.DriveApp.getFolderById = orig;
const lockAfter = env.S.LockService.getScriptLock();
check(lockAfter.tryLock() === true, 'and the lock is released after it');

console.log(`\n${failed ? failed + ' FAILED' : 'ALL PASSED'}`);
process.exit(failed ? 1 : 0);
