/* =====================================================================
   The landing page (index.html): for each supervision whose work is
   ready, how far the student has got (what that supervision's page saved
   in this browser: its ticks and answers) and what they have done with
   the essay to hand in (MG.siteStore 'paper:<id>', kept by Supervision
   work); and the student's name, which goes on the work they hand in.
   ===================================================================== */
(function () {
  'use strict';
  const MG = window.MG;
  const { h, esc, bus, toast, siteStore } = MG;
  const CFG = MG.config || {};
  const SUPS = window.BMS_SUPERVISIONS || [];
  const $ = (s, r) => (r || document).querySelector(s);
  const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  const day = (iso) => {
    const d = new Date(iso);
    return isNaN(d) ? '' : `${d.getDate()} ${MONTHS[d.getMonth()]}`;
  };

  /** what a supervision's page saved: its ticks and answers */
  function saved(dataPage) {
    try {
      const v = window.localStorage.getItem((CFG.storePrefix || 'bmssup') + ':' + dataPage + ':progress');
      return (v && JSON.parse(v)) || { tasks: {}, answers: {} };
    } catch (e) {
      return { tasks: {}, answers: {} };
    }
  }
  function showSup(tile) {
    const n = +tile.dataset.sup;
    const s = SUPS.find((x) => x.n === n);
    if (!s) return;
    const st = saved(s.dataPage);
    const tasks = st.tasks || {}, answers = st.answers || {};
    let done = 0;
    s.tasks.forEach((t) => tasks[t] && done++);
    s.questions.forEach((q) => answers[q] && answers[q].done && done++);
    const total = s.tasks.length + s.questions.length;
    const pct = total ? Math.round((done / total) * 100) : 0;
    const started = Object.keys(tasks).length > 0 || Object.keys(answers).length > 0;
    $('.tp-bar > i', tile).style.width = pct + '%';
    $('.tp-text', tile).textContent = !started ? 'Not started yet' : pct === 100 ? 'All the exercises done' : `${done} of ${total} steps and questions done`;
    tile.classList.toggle('done', total > 0 && done === total);
    // the essay to hand in
    const e = $('.tile-essay', tile);
    const r = s.paper ? siteStore.get('paper:' + s.paper, null) : null;
    if (!e || !s.paper) return;
    e.className = 'tile-essay';
    if (r && r.downloaded) {
      e.textContent = `✓ Essay submitted and downloaded (${day(r.downloaded)}): remember to send it in`;
      e.classList.add('ok');
    } else if (r && r.submitted) {
      e.textContent = `Essay submitted (${day(r.submitted)}): now download it as a Word document and send it in`;
      e.classList.add('todo');
    } else if (r && r.started) {
      e.textContent = 'Essay started, not yet submitted';
      e.classList.add('todo');
    } else e.textContent = 'Essay not started yet';
  }

  function showName() {
    const n = MG.user.fullName();
    const t = $('[data-student-name-text]'), b = $('[data-name-btn]');
    if (t) {
      t.textContent = n || 'no name yet';
      t.classList.toggle('none', !n);
    }
    if (b) b.textContent = n ? 'Change' : 'Add your name';
  }
  function nameDialog() {
    const cur = MG.user.fullName();
    const m = MG.modal('Your name', '');
    const input = h('input.prompt-input#studentNameIn', { type: 'text', value: cur, placeholder: 'For example, Ada Lovelace', maxlength: String(MG.user.MAX), spellcheck: 'false', autocomplete: 'name' });
    const save = h('button.btn.primary', { type: 'submit' }, 'Save');
    const cancel = h('button.btn', { type: 'button' }, 'Cancel');
    const form = h('form.user-form',
      h('p', 'Your name goes on the essays and answers you download and hand in, so that your supervisor knows whose work it is. It is kept in this browser only, and every supervision’s page uses it.'),
      h('label.user-label', { for: 'studentNameIn' }, 'Your name'), input,
      h('div.prompt-actions', h('span.grow'), cancel, save));
    m.box.querySelector('.modal-b').appendChild(form);
    form.addEventListener('submit', (ev) => {
      ev.preventDefault();
      const v = MG.user.setFullName(input.value);
      MG.user.set(v ? MG.user.suggest(v) || MG.user.DEFAULT : MG.user.DEFAULT);
      m.close();
      toast(v ? `Saved: your work will show the name <b>${esc(v)}</b>.` : 'Your name has been removed.', 'ok', 3000);
      showName();
    });
    cancel.addEventListener('click', () => m.close());
    setTimeout(() => input.focus(), 30);
  }

  function refresh() {
    showName();
    document.querySelectorAll('.tile.ready[data-sup]').forEach(showSup);
  }
  function init() {
    const b = $('[data-name-btn]');
    if (b) b.addEventListener('click', nameDialog);
    bus.on('user:name', refresh);
    // (a supervision's page in another tab of this browser saved something; or the student came back to this page)
    window.addEventListener('storage', refresh);
    window.addEventListener('pageshow', refresh);
    refresh();
    window.MG_READY = true;
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
