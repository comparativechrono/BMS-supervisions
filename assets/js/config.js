/* =====================================================================
   Settings for the BMS supervisions (built on the BMS workbench).
   You can change these settings by editing this file and uploading it
   again; nothing else needs to change.
   ===================================================================== */
window.MG_CONFIG = {
  /* (the title and subtitle of each page are written by build/make_page.py, from build/supervisions.py) */
  courseTitle: null,
  courseSubtitle: null,

  /* The prefix for everything the pages save in the browser (files, answers, essays and settings). All the pages of
     this site share it, so a student's files and essays are the same on every supervision's page. It is not the BMS
     workbench's (bmswb), so that the two sites keep their files apart although GitHub Pages serves them from the same
     address. */
  storePrefix: 'bmssup',
  hostname: 'workbench',

  /* Model answers are shown with a "Show answer" button under each question. Set this to false to hide
     them (they are still in the page's source code, and adding ?answers to the address shows them). */
  showModelAnswers: true,

  /* The microscope. slideBase is the folder (or the web address of a folder) that holds the slides: index.json lists
     them and each slide is a folder of its own (see build/slides/README.md). Another web site can hold them, as long as
     it allows requests from this page (CORS) and answers range requests, as GitHub Pages does. */
  slideBase: 'slides/',
  /* The objectives on the microscope, and the size of the slide's pixels that each one shows at one screen pixel:
     20x shows a slide scanned at 20x (about 0.5 micrometres per pixel) pixel for pixel. */
  objectives: [1, 2, 4, 10, 20, 40],
  micronsPerScreenPixelAt20x: 0.5,

  /* Supervision work. The papers are in exams/ (exams/index.json lists them). spellcheckDefault: whether the browser's
     spelling checker is on when a student starts a paper (it is usually off in real exams; students can switch it).
     autosaveSeconds: how often an answer that is being typed is saved. */
  examBase: 'exams/',
  spellcheckDefault: false,
  autosaveSeconds: 5,

  /* Where students hand in the work they submit in Supervision work (a paper with "handIn": true uses this; a paper
     can name its own). The hand-in password is given to the students by their supervisor: it is not on this site, and
     it must never be put here.
     script: the address of the hand-in script (handin/Code.gs), published as a Google Apps Script web app from the
       supervisor's Google account (handin/README.md says how). The site sends the Word document to it, with the
       password that the student types; it checks the password, saves the document in the supervisor's Google Drive
       and sends back a receipt.
     to: who the work goes to; password: whether students need a password. */
  handIn: {
    to: 'Tim Hearn',
    password: true,
    script: 'https://script.google.com/macros/s/AKfycbxeCW2Orw3iCkQb5IPVtyGfB2-l6TTvGRRt5FUnKY6lpnpShigUe0NB2SNPQGypBrwB/exec'
  },

  /* The examples of the Diagrams and Circuits tabs. */
  examplesBase: 'examples/',

  /* The Recorder's recordings (recordings/index.json lists them; see build/recordings/README.md). Another web site can
     hold them, as long as it allows requests from this page (CORS). */
  recordingBase: 'recordings/',

  /* R in the browser (webR). RStudio downloads R from here (about 30 MB, kept by the browser after the first
     download), and R packages from the webR repository when install.packages() asks for them. */
  webrBase: 'https://webr.r-wasm.org/v0.6.0/',
  rRepos: ['https://repo.r-wasm.org'],

  /* The Molecules tab: what the boxes suggest. */
  pdbExample: '4HHB',
  afExample: 'UniProt e.g. P69905',

  /* How many megabytes of files the workbench can keep in the browser before it warns the user. */
  storageWarnMB: 1500
};
