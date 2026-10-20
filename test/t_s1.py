"""Supervision 1 (supervision-1.html) and the landing page (index.html), as a student would use them: the eight tiles
(Supervision 1's page, the workbench's guide for the others), the name that every page shares, Supervision work first
among the tabs with this week's papers at the top, the essay to hand in (no time limit, a suggested 40 minutes counted
up, pasting refused, the hand-in box, a Word document with the student's name, and offered again on the paper's first
page), and each chapter's steps ticking as the student does them – the thirst and clock diagrams and their periods, the
finds in Anatomy and the Microscope, the molecules, the R–R interval, the heart-rate data in R (the numbers the model
answers give), the multiple-choice questions of the marking and plagiarism chapters – and the landing page's progress
and essay status afterwards; the layout on a phone.
Handing in goes straight to Google Drive, through the hand-in script (here a stand-in, so nothing is handed in): no
password, a wrong one, no answer, the hand-in busy, then the receipt, and handing it in again. Given the hand-in
password as BMS_HANDIN_PASSWORD, it checks that no file has it.
Run:  python3 test/t_s1.py   (screenshots in test/out/s1-*.png; R is downloaded from the internet)"""
import base64
import io
import json
import os
import re
import time
import zipfile

from h import Page, check, done, OUT

A = 'MG.app.anatomy'
F = 'MG.app.flow'
E = 'MG.app.exam'
RC = 'MG.app.recorder'
NAME = 'Ada Lovelace'

p = Page(width=1500, height=950)
P = p.p


def click(sel):
    P.locator(sel).first.click()


def ticked(tid):
    return bool(p.js(f"() => !!(MG.tutorial && MG.tutorial.state.tasks['{tid}'])"))


def wait_ticked(tid, s=20):
    for _ in range(int(s * 4)):
        if ticked(tid):
            return True
        time.sleep(0.25)
    return False


def answered(qid):
    return bool(p.js(f"() => !!(MG.tutorial.state.answers['{qid}'] || {{}}).done"))


def chapter(cid):
    p.js(f"() => MG.app.showChapter('{cid}', true)")
    time.sleep(0.6)


def mcq_right(qid):
    """chooses the right option of a multiple-choice question; it is marked right, and the question done"""
    P.locator(f'.q[data-q="{qid}"] .mcq label[data-correct]').click()
    time.sleep(0.15)
    fb = p.js(f"() => document.querySelector('.q[data-q=\"{qid}\"] .q-feedback').textContent")
    return answered(qid) and fb.startswith('✓')


def mcq_wrong(qid):
    P.locator(f'.q[data-q="{qid}"] .mcq label:not([data-correct])').first.click()
    time.sleep(0.15)
    fb = p.js(f"() => document.querySelector('.q[data-q=\"{qid}\"] .q-feedback').textContent")
    return not answered(qid) and fb.startswith('✗') and len(fb) > 20


def short(qid, text):
    q = P.locator(f'.q[data-q="{qid}"]')
    q.locator('input[type=text]').fill(text)
    q.locator('button:has-text("Check")').click()
    time.sleep(0.2)
    return answered(qid)


def leave_diagram():
    """the Diagrams tab asks before it leaves a diagram with changes: go on without saving"""
    for _ in range(20):
        if p.js("() => !!document.querySelector('.modal')"):
            click('.modal button:has-text("Go on without saving")')
            time.sleep(0.3)
            return True
        time.sleep(0.1)
    return False


def ev(kind, cond='true'):
    return p.js(f"() => (window.__s1ev || []).filter(e => e[0] === '{kind}' && (d => {cond})(e[1])).length")


def last(kind):
    e = [x for x in p.js("() => window.__s1ev || []") if x[0] == kind]
    return e[-1][1] if e else None


def listen():
    p.js("() => { window.__s1ev = []; MG.bus.on('*', (d, t) => { try { window.__s1ev.push([t, JSON.parse(JSON.stringify(d || {}))]); } catch (e) {} }); }")


def no_errors(where):
    errs = [e for e in p.errors if 'ResizeObserver' not in e]
    check(not errs, f'no errors in the page ({where}): {errs[:3]}')
    p.errors.clear()


# ====================================================================== the landing page, fresh
p.open('index.html')
p.js("() => { localStorage.clear(); sessionStorage.clear(); }")
p.js("() => new Promise((ok) => { const r = indexedDB.deleteDatabase('bmssup-files'); r.onsuccess = r.onerror = r.onblocked = () => ok(); })")
p.open('index.html')
tiles = p.js("""() => [...document.querySelectorAll('.tiles .tile')].map(t => ({ n: t.dataset.sup, href: t.getAttribute('href'), ready: t.classList.contains('ready'),
    kicker: t.querySelector('.tile-kicker').textContent, text: t.innerText }))""")
check([t['n'] for t in tiles] == [str(i) for i in range(1, 9)] and [t['kicker'] for t in tiles] == [f'Supervision {i}' for i in range(1, 9)],
      f'the landing page has eight tiles, Supervision 1 to 8: {[t["kicker"] for t in tiles]}')
check(tiles[0]['href'] == 'supervision-1.html' and tiles[0]['ready'], 'Supervision 1 opens its own page')
check(all(t['href'] == 'workbench.html' and not t['ready'] and 'Coming soon' in t['text'] for t in tiles[1:]), 'Supervisions 2 to 8 are coming soon, and open the workbench and its guide')
t1 = tiles[0]['text']
check('To hand in: an essay on why negative feedback is more common than positive feedback' in t1 and 'Not started yet' in t1 and 'Essay not started yet' in t1, f'tile 1 names the essay to hand in, and nothing is started: {t1[:200]!r}')
check(p.js("() => document.querySelector('[data-student-name-text]').textContent") == 'no name yet', 'there is no name yet')
click('[data-name-btn]')
P.fill('#studentNameIn', NAME)
click('.user-form button[type=submit]')
time.sleep(0.3)
check(p.js("() => document.querySelector('[data-student-name-text]').textContent") == NAME and p.js("() => MG.user.fullName()") == NAME,
      'the name given on the landing page is shown, and kept for every page')
grid = p.js("() => getComputedStyle(document.querySelector('.tiles')).gridTemplateColumns.split(' ').length")
check(grid == 4, f'four tiles to a row on a wide screen ({grid})')
p.shot('s1-landing')
no_errors('the landing page')

# ====================================================================== Supervision 1's page
p.open('supervision-1.html')
listen()
# the essay is handed in through the hand-in script, in Tim Hearn's Google account (config.js: handIn.script)
SCRIPT = p.js("() => MG.config.handIn.script") or ''
check(bool(re.match(r'https://script\.google\.com/macros/s/[\w-]+/exec$', SCRIPT)), f'the site hands in to the hand-in script, a web app of Apps Script ({SCRIPT[:48]}…)')
check('dropbox' not in p.js("() => document.body.textContent + JSON.stringify(MG.config)").lower(), 'nothing on the page, or in its settings, mentions Dropbox')
chs = p.js("() => [...document.querySelectorAll('.chapter')].map(c => c.id + ':' + c.dataset.num)")
check(chs == ['s1-week:0', 's1-clock:1', 's1-where:2', 's1-heart:3', 's1-marking:4', 's1-plag:5', 's1-write:6', 's1-more:7'], f'Supervision 1 has its eight chapters: {chs}')
check(p.js("() => document.body.dataset.week") == '1' and p.js("() => window.BMS_PAGE && window.BMS_PAGE.week") == 1, 'the page knows it is week 1')
tabs = p.js("() => [...document.querySelectorAll('.wb-tab[data-wb]')].map(t => t.dataset.wb + ':' + t.innerText.trim())")
check(tabs[0] == 'exam:Supervision work', f'the first tab is Supervision work: {tabs[:2]}')
check(p.js("() => MG.app.currentBench") == 'exam', 'the page opens on Supervision work')
p.wait("() => document.querySelectorAll('.ex-card').length >= 6", timeout=30000)
cards = p.js("() => [...document.querySelectorAll('.ex-card')].map(c => c.dataset.paper + ':' + (c.querySelector('.ex-badge') ? c.querySelector('.ex-badge').textContent : ''))")
check(cards[:3] == ['s1-essay:To hand in', 's1-saqs:Optional', 's1-revision:Optional'], f'this week’s papers come first, the essay to hand in at the top: {cards[:3]}')
meta = p.js("() => document.querySelector('.ex-card[data-paper=\"s1-essay\"] .ex-cmeta').textContent")
check('No time limit (about 40 minutes suggested)' in meta, f'the essay has no time limit, and suggests 40 minutes: {meta}')
check(p.js("() => document.querySelector('.ex-card[data-paper=\"s1-revision\"] .ex-cmeta').textContent").find('marks') < 0, 'the revision titles carry no marks')
check(wait_ticked('wk-name', 5), 'the name given on the landing page ticks wk-name')
box = p.js("() => document.querySelector('#s1-week .handin-box').innerText")
check('Discuss, with examples' in box and '40 minutes' in box and 'type the hand-in password that Tim Hearn gives you, and it goes straight to his Google Drive' in box,
      f'This week shows the essay to hand in, the 40 minutes, and how it is handed in to Tim Hearn: {box[-160:]!r}')
p.shot('s1-week')
no_errors('opening Supervision 1')

# ====================================================================== 1 A clock made of feedback
chapter('s1-clock')
check(p.js("() => MG.app.currentBench") == 'flow', 'the clock chapter opens the Diagrams tab')
click('#s1-clock button[data-flow="example:thirst"]')
p.wait(f"() => {F} && {F}.D && /^Thirst/.test({F}.D.title)", timeout=30000)
check(wait_ticked('ck-th-open', 5), 'the thirst diagram opens and ticks ck-th-open')
click('#s1-clock button[data-flow-run]')
check(wait_ticked('ck-th-run', 10), 'running it ticks ck-th-run')
lo = p.js(f"() => Math.min(...{F}.result.series.osm)")
hi = p.js(f"() => Math.max(...{F}.result.series.osm)")
check(abs(hi - 308.7) < 0.5 and abs(lo - 290.8) < 0.5, f'osmolarity rises to about 309 and overshoots to about 291 mOsm/L, as the model answer says ({hi:.1f}, {lo:.1f})')
check(not ticked('ck-th-ff'), 'ck-th-ff waits for the feed-forward arrow')
# unblock the feed-forward arrow as a student would: right-click it, and choose Unblock this arrow
pt = p.js("""() => { const path = document.querySelector('.fl-edge[data-edge="e-ff"] .fl-line'); const q = path.getPointAtLength(path.getTotalLength() / 2), m = path.getScreenCTM();
    return [q.x * m.a + q.y * m.c + m.e, q.x * m.b + q.y * m.d + m.f]; }""")
P.mouse.click(pt[0], pt[1], button='right')
time.sleep(0.3)
click('.popmenu button:has-text("Unblock this arrow")')
time.sleep(0.2)
check(p.js(f"() => !{F}.edge('e-ff').blocked"), 'the menu unblocks the feed-forward arrow')
p.js(f"() => {F}.run()")
check(wait_ticked('ck-th-ff', 10), 'running it again with feed-forward ticks ck-th-ff')
lo2 = p.js(f"() => Math.min(...{F}.result.series.osm)")
check(abs(lo2 - 298.3) < 0.5, f'with feed-forward the overshoot almost goes (the lowest point is {lo2:.1f} mOsm/L)')
msg = p.js(f"() => {F}.runPanel.innerText")
check('Changes start at' not in msg, f'the run message does not speak of changes starting, for an arrow blocked from the start: {msg[:120]!r}')
p.shot('s1-thirst')
click('#s1-clock button[data-flow="example:clock"]')
check(leave_diagram(), 'leaving the changed thirst diagram asks first (and the instructions say so)')
p.wait(f"() => {F}.D && /clock/i.test({F}.D.title)", timeout=30000)
check(wait_ticked('ck-open', 5), 'the clock opens and ticks ck-open')
click('#s1-clock button[data-flow-run]')
check(wait_ticked('ck-run', 10), 'running it ticks ck-run')
r = last('flow:run')
check(r['oscillates'] and abs(r['period'] - 24.6) < 0.2 and r['oscillation'] == 'steady', f'the clock in the cave oscillates steadily, with a period of about 24.6 h: {r["period"]} h, {r["oscillation"]}')
msg = p.js(f"() => {F}.runPanel.innerText")
check(re.search(r'period of 24\.\d h', msg) is not None, f'the message under the diagram gives the period: {msg[:160]!r}')
check(short('ck-q-period', str(r['period'])), 'the period, typed in, is right (ck-q-period)')
p.shot('s1-clock')
for delay, tid, lo_, hi_ in ((2, 'ck-short', 19.5, 21.5), (6, 'ck-long', 28, 30)):
    p.js(f"() => {{ {F}.setEdge('back', {{ delay: {delay} }}); {F}.run(); }}")
    ok = wait_ticked(tid, 10)
    per = last('flow:run')['period']
    check(ok and lo_ < per < hi_, f'a delay of {delay} h on the way back into the nucleus gives a period of {per} h, and ticks {tid}')
p.js(f"() => {{ {F}.setEdge('back', {{ delay: 4 }}); }}")
# knock out the proteins from the menu of the box
# (the last run's animation redraws the boxes: let it finish first, as a student would)
p.wait(f"() => {F}.stopBtn.hidden", timeout=20000)
time.sleep(0.3)
nb = p.js("() => { const r = document.querySelector('.fl-node[data-node=\"protein\"]').getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; }")
P.mouse.click(nb[0], nb[1], button='right')
time.sleep(0.3)
click('.popmenu button:has-text("Knock it out")')
p.js(f"() => {F}.run()")
check(wait_ticked('ck-ko', 10) and not last('flow:run')['oscillates'], 'knocking out the PER and CRY proteins stops the clock, and ticks ck-ko')
check(mcq_wrong('ck-q-per') and mcq_right('ck-q-per'), 'ck-q-per: a wrong answer says why; the right one (knocking out the proteins) is marked right')
p.js(f"() => {{ {F}.intervene('protein', null); {F}.setEdge('entrain', {{ blocked: false }}); {F}.run(); }}")
check(wait_ticked('ck-light', 10), 'out of the cave, with light, ticks ck-light')
per = last('flow:run')['period']
check(abs(per - 24.0) < 0.2, f'light entrains the clock to 24 h ({per} h)')
# (if you have time) 24 h in the cave; positive feedback
p.js(f"() => {{ {F}.setEdge('entrain', {{ blocked: true }}); {F}.setEdge('back', {{ delay: 3.7 }}); {F}.run(); }}")
check(wait_ticked('ck-24', 10), f'a total delay of 7.7 h gives 24 h in the cave ({last("flow:run")["period"]} h), and ticks ck-24')
click('#s1-clock button[data-flow="example:positive-feedback-clotting"]')
leave_diagram()
check(wait_ticked('ck-pos', 10), 'the blood-clotting example opens (ck-pos)')
no_errors('the clock chapter')

# ====================================================================== 2 Where is the clock?
chapter('s1-where')
check(p.js("() => MG.app.currentBench") == 'anatomy', 'the chapter opens the Anatomy tab')


def idle():
    p.wait(f"() => {A} && {A}.index && !Object.values({A}.files).some(f => f.state === 'loading') && !{A}._camAnim && !{A}._raf", timeout=120000)
    time.sleep(0.3)


def click_on(sid):
    pt = p.js(f"(id) => {A}.testPoint(id)", sid)
    if not pt:
        return False
    P.mouse.click(pt['x'], pt['y'])
    time.sleep(0.5)
    return True


idle()
click('#s1-where button[data-anat="endocrine+labels"]')
idle()
check(wait_ticked('wh-glands', 5), 'the endocrine glands, with labels, tick wh-glands')
click_on('neurohypophysis')
ok = click_on('hypothalamus')
check(ok and wait_ticked('wh-hypo', 5), 'clicking on the hypothalamus ticks wh-hypo')
click('#s1-where button[data-anat-find="pineal-gland"]')
idle()
ok = click_on('pineal-gland')
check(ok and wait_ticked('wh-pineal', 5), 'finding the pineal gland ticks wh-pineal')
click('#s1-where button[data-anat-find="suprarenal-gland"]')
idle()
ok = click_on('suprarenal-gland-right')
check(ok and wait_ticked('wh-adrenal', 5), 'finding a suprarenal gland ticks wh-adrenal')
click('#s1-where button[data-anat-find="optic-chiasm"]')
idle()
check(p.js(f"() => !!{A}.on.brain"), 'finding the optic chiasm shows the brain')
P.locator('.an-view').focus()
P.keyboard.press('6')
idle()
ok = click_on('optic-chiasm-left') or click_on('optic-chiasm-right')
check(ok and wait_ticked('wh-chiasm', 5), 'from below, a click on the optic chiasm ticks wh-chiasm')
p.shot('s1-chiasm')
click('#s1-where button[data-anat="brain+endocrine:hypothalamus+section:sagittal@0.5@left"]')
idle()
check(wait_ticked('wh-cut', 5), 'the sagittal section ticks wh-cut')
vis = p.js(f"() => ['hypothalamus', 'adenohypophysis', 'pineal-gland'].map(id => !!{A}.testPoint(id))")
check(all(vis), f'in the cut, the hypothalamus, the pituitary and the pineal gland can be seen and clicked: {vis}')
p.shot('s1-section')
no_errors('the anatomy of the clock')


def find_click(slide, key):
    p.js(f"""() => {{ const S = MG.app.scope, L = S.slide.info.labels.find(l => (l.key || l.id) === '{key}'); S._goTo(L, 10); }}""")
    time.sleep(1.5)
    pt = p.js(f"""() => {{ const S = MG.app.scope, L = S.slide.info.labels.find(l => (l.key || l.id) === '{key}');
        const s = S._screen(L.x, L.y), r = S.view.getBoundingClientRect(); return {{x: r.left + s.x, y: r.top + s.y}}; }}""")
    P.mouse.click(pt['x'], pt['y'])
    time.sleep(0.4)


click('#s1-where button[data-scope="pituitary-gland"]')
p.wait("() => MG.app.scope && MG.app.scope.current() === 'pituitary-gland'", timeout=30000)
check(wait_ticked('wh-pit', 5), 'the pituitary slide opens (wh-pit)')
click('#s1-where button[data-scope-find="pituitary-gland:posterior"]')
time.sleep(0.5)
find_click('pituitary-gland', 'posterior')
check(wait_ticked('wh-post', 5), 'finding the posterior pituitary ticks wh-post')
click('#s1-where button[data-scope="adrenal-gland"]')
p.wait("() => MG.app.scope.current() === 'adrenal-gland'", timeout=30000)
check(wait_ticked('wh-adr', 5), 'the adrenal slide opens (wh-adr)')
for key, tid in (('zona-fasciculata', 'wh-zf'), ('medulla', 'wh-med')):
    click(f'#s1-where button[data-scope-find="adrenal-gland:{key}"]')
    time.sleep(0.5)
    find_click('adrenal-gland', key)
    check(wait_ticked(tid, 5), f'finding the {key.replace("-", " ")} ticks {tid}')
check(mcq_right('wh-q-zone'), 'wh-q-zone: the zona fasciculata makes cortisol')
for btn, tid, name in (('melatonin', 'wh-mel', 'Melatonin'), ('cortisol', 'wh-cort', 'Cortisol')):
    click(f'#s1-where button[data-viewer^="clear; molecule {btn}"]')
    check(wait_ticked(tid, 30), f'{name} opens in Molecules and ticks {tid}')
p.shot('s1-cortisol')
check(mcq_right('wh-q-lipid'), 'wh-q-lipid: a steroid acts on receptors inside the cell')
check(mcq_right('wh-q-conn'), 'wh-q-conn (if you have time): aldosterone, from the zona glomerulosa')
no_errors('the microscope and the molecules')

# ====================================================================== 3 Your heart's daily rhythm
chapter('s1-heart')
check(p.js("() => MG.app.currentBench") == 'recorder', 'the chapter opens the Recorder')
click('#s1-heart button[data-rec="ecg-normal@2,6"]')
p.wait(f"() => {RC} && {RC}.R && {RC}.R.id === 'ecg-normal' && !{RC}._raf", timeout=30000)
check(wait_ticked('ht-open', 5), 'the ECG opens and ticks ht-open')
click('#s1-heart button[data-rec-tool="calipers"]')
time.sleep(0.3)
beats = p.js(f"() => {RC}.R.beats.t.filter((t) => t > 2.2 && t < 5.8)")
y = p.js(f"() => {RC}._clientY('II')")
xa, xb = p.js(f"(b) => [{RC}._clientX(b[0]), {RC}._clientX(b[1])]", beats)
m = P.mouse
m.move(xa, y)
m.down()
for k in range(1, 9):
    m.move(xa + (xb - xa) * k / 8, y)
m.up()
time.sleep(0.3)
check(wait_ticked('ht-cal', 5), f'an R–R interval measured with the calipers ticks ht-cal ({last("rec:measure")["dt"]:.3f} s)')
check(short('ht-q-rr', '75'), 'ht-q-rr: an R–R interval of 0.8 s is 75 beats per minute')
p.shot('s1-rr')

# R: each button types its line into the Console, and the student presses Enter
click('#s1-heart button[data-rcon]')
for _ in range(400):
    st = p.js("() => { const R = MG.app.rstudio; return R && R.S ? R.S.state : ''; }")
    if st == 'idle':
        break
    time.sleep(0.5)
check(st == 'idle', f'R starts in RStudio ({st})')


def console():
    """the output of RStudio's Console"""
    return p.js("() => { const c = MG.app.rstudio && MG.app.rstudio.cv && MG.app.rstudio.cv.out; return c ? c.textContent : ''; }")


def run_button(code, wait_for=None, timeout=60):
    """clicks the show-me button that types code, and presses Enter in the Console; returns what R printed"""
    before = len(console())
    b = P.locator('#s1-heart button[data-rcon]').filter(has=None)
    sel = p.js("(c) => { const b = [...document.querySelectorAll('#s1-heart button[data-rcon]')].find(x => x.dataset.rcon === c); if (!b) return false; b.scrollIntoView({block: 'center'}); return true; }", code)
    if not sel:
        return None
    p.js("(c) => [...document.querySelectorAll('#s1-heart button[data-rcon]')].find(x => x.dataset.rcon === c).click()", code)
    time.sleep(0.6)
    P.keyboard.press('Enter')
    for _ in range(timeout * 4):
        time.sleep(0.25)
        busy = p.js("() => MG.app.rstudio && MG.app.rstudio.S && MG.app.rstudio.S.state")
        out = console()[before:]
        if busy == 'idle' and (wait_for is None or re.search(wait_for, out)):
            return out
    return console()[before:]


R_READ = 'heart <- read.csv("~/data/heart-rate-24h.csv")'
# (the first button was clicked above, to start R: its line is waiting in the Console)
P.keyboard.press('Enter')
time.sleep(1.5)
check(wait_ticked('ht-read', 20), 'reading the file ticks ht-read')
out = run_button('head(heart)', r'n_beats')
check(out and 'subject' in out and 'n_beats' in out and '16265' in out, f'head(heart) shows the columns: {(out or "")[:200]!r}')
check(ticked('ht-head'), 'ht-head ticks')
out = run_button('summary(heart$hr)', r"NA's")
check(out and re.search(r"45\.5", out) and re.search(r"116\.7", out) and re.search(r"NA'?s\s+50\b", out.replace('\n', ' ')), f'summary() gives the range, 45.5 to 116.7, and 50 NAs: {(out or "")[:300]!r}')
check(ticked('ht-sum'), 'ht-sum ticks')
run_button('one <- subset(heart, subject == 16786)')
n0 = p.js("() => MG.app.rstudio.plots.length")
run_button('plot(one$hour, one$hr, type = "b", xlab = "Hour of the day", ylab = "Heart rate (beats/min)")')
for _ in range(40):
    if p.js("() => MG.app.rstudio.plots.length") > n0:
        break
    time.sleep(0.25)
check(wait_ticked('ht-one', 10), 'her day is plotted, and ht-one ticks')
run_button('avg <- aggregate(hr ~ hour, data = heart, FUN = mean)')
out = run_button('avg', r'23\s+70\.0')
check(out and re.search(r'^\s*6\s+5\s+64\.3', out, re.M) and re.search(r'23\s+70\.0', out), f'avg holds the mean of each hour (05:00: 64.4, 23:00: 70.0): {(out or "")[:160]!r}')
check(ticked('ht-agg'), 'ht-agg ticks')
run_button('plot(avg$hour, avg$hr, type = "b", xlab = "Hour of the day", ylab = "Mean heart rate (beats/min)")')
check(wait_ticked('ht-plot', 10), 'the means are plotted (ht-plot)')
p.shot('s1-r-plot')
out = run_button('avg$hour[which.min(avg$hr)]', r'\[1\]')
check(out and re.search(r'\[1\]\s+5\b', out), f'the lowest mean is at hour 5: {(out or "").strip()!r}')
check(ticked('ht-min') and short('ht-q-low', '5'), 'ht-min ticks, and ht-q-low takes 5')
run_button('day <- mean(heart$hr[heart$hour >= 8 & heart$hour < 20], na.rm = TRUE)')
run_button('night <- mean(heart$hr[heart$hour < 6], na.rm = TRUE)')
out = run_button('day - night', r'\[1\]')
check(out and re.search(r'\[1\]\s+16\.9', out), f'the heart rate is 16.9 beats per minute lower at night: {(out or "").strip()!r}')
check(ticked('ht-day') and ticked('ht-night') and ticked('ht-diff'), 'ht-day, ht-night and ht-diff tick')
check(not short('ht-q-diff', '82.5') and short('ht-q-diff', '16.9'), 'ht-q-diff takes 16.9 (and not the day’s mean)')
check(mcq_right('ht-q-mask'), 'ht-q-mask: masking – the rhythm alone doesn’t show the clock')
# (if you have time) the cosinor
run_button('boxplot(hr ~ hour, data = heart, xlab = "Hour of the day", ylab = "Heart rate (beats/min)")')
run_button('fit <- lm(hr ~ cos(2 * pi * hour / 24) + sin(2 * pi * hour / 24), data = heart)')
run_button('b <- unname(coef(fit))')
out = run_button('c(mesor = b[1], amplitude = sqrt(b[2]^2 + b[3]^2), peak = (atan2(b[3], b[2]) * 12 / pi) %% 24)', r'peak')
nums = re.findall(r'-?\d+\.\d+', (out or '').split('peak', 1)[-1])
check(len(nums) >= 3 and abs(float(nums[0]) - 75.26) < 0.05 and abs(float(nums[1]) - 10.09) < 0.05 and abs(float(nums[2]) - 14.65) < 0.05,
      f'the cosinor: mesor 75.3, amplitude 10.1, peak at 14.7 h, as the model answer says: {nums[:3]}')
run_button('plot(avg$hour, avg$hr, type = "b", xlab = "Hour of the day", ylab = "Mean heart rate (beats/min)")')
out = run_button('curve(b[1] + b[2] * cos(2 * pi * x / 24) + b[3] * sin(2 * pi * x / 24), add = TRUE, col = "red")')
check('Error' not in (out or ''), 'the curve is drawn over the means, without errors')
check(ticked('ht-cos') and ticked('ht-curve'), 'ht-cos and ht-curve tick')
p.shot('s1-cosinor')
check('Error' not in console(), 'none of the R typed for the student gives an error')
no_errors('the heart chapter')

# ====================================================================== 4 How essays are marked
chapter('s1-marking')
check(p.js("() => document.querySelectorAll('#s1-marking .crit').length") == 6, 'the six core criteria are set out')
check(p.js("() => document.querySelectorAll('#s1-marking .sample-essay:not(details .sample-essay) p').length") == 5, 'the example essay has five numbered paragraphs')
for i in range(1, 7):
    check(mcq_right(f'mk-q{i}'), f'mk-q{i}: the right comment from the feedback form is marked right')
check(p.js("() => document.querySelectorAll('#s1-marking details.better .sample-essay p').length") == 5 and
      p.js("() => document.querySelectorAll('#s1-marking details.better .ctag').length") == 10, 'the better version has its five paragraphs, each with what it does')

# ====================================================================== 5 Plagiarism
chapter('s1-plag')
for i in range(1, 5):
    right = p.js(f"() => [...document.querySelectorAll('.q[data-q=\"pl-q{i}\"] .mcq label')].findIndex(l => l.hasAttribute('data-correct'))")
    check(right == i - 1 and mcq_right(f'pl-q{i}'), f'pl-q{i}: version {i} is “{["copied phrases", "copied sentence structure", "copied paragraph structure", "acceptable"][i - 1]}”')
check(mcq_right('pl-q-quote'), 'pl-q-quote: quotation marks and a reference')
check('Kohler' in p.js("() => document.querySelector('#s1-plag .passage.orig').innerText"), 'the original passage and its source are shown')
p.shot('s1-plag')
no_errors('marking and plagiarism')

# ====================================================================== 6 Write your essay
chapter('s1-write')
click('#s1-write button[data-exam="s1-essay"]')
p.wait("() => document.querySelector('.ex-startcard h2') && document.querySelector('.ex-startcard h2').textContent === 'Supervision 1 essay'", timeout=30000)
check(wait_ticked('es-open', 5), 'opening the essay ticks es-open')
sc = p.js("() => document.querySelector('.ex-startcard').textContent")
check('No time limit. We suggest about 40 minutes' in sc and 'To hand in' in sc and 'Tim Hearn' in sc and 'Supervision 1 · to hand in' in sc,
      f'its first page: no time limit, 40 minutes suggested, and how to hand it in: {sc[:240]!r}')
check('Why like this?' in sc and 'online exam' in sc, 'and why it is written as in the exam')
p.shot('s1-essay-start')
click('.ex-startacts .btn.primary')
p.wait("() => document.querySelector('.ex-area')", timeout=30000)
check(not p.js("() => !!document.querySelector('.modal')"), 'with a name already given, Start doesn’t ask for one')
check(wait_ticked('es-start', 5), 'starting the essay ticks es-start')
tm = p.js("() => document.querySelector('.ex-timer').textContent")
check(tm == '0 of about 40 minutes', f'the clock counts up towards the suggested 40 minutes: {tm!r}')
PASTE = """(t) => { const A = document.querySelector('.ex-area'); A.focus(); const dt = new DataTransfer(); dt.setData('text/plain', t);
    A.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true })); }"""
p.js(PASTE, 'Few laboratory creatures have had such a spectacularly successful and productive history as Drosophila.')
time.sleep(0.3)
check('Few laboratory' not in p.js("() => document.querySelector('.ex-area').textContent") and wait_ticked('es-paste', 5),
      'text copied from elsewhere won’t paste into the essay, and es-paste ticks')
para = ('Negative feedback opposes a change in a regulated variable and so keeps the internal environment stable, which cells need '
        'because their enzymes and channels work only within narrow limits of temperature, osmolarity and pH. ')
p.js("""(t) => { const A = document.querySelector('.ex-area'); A.focus(); document.execCommand('insertText', false, t); }""", (para * 9).strip())
time.sleep(1.6)
check(wait_ticked('es-write', 5), f'writing more than 300 words ticks es-write ({p.js("() => document.querySelector(\'.ex-wc\').textContent")})')
# the suggested time: the clock counts the time spent writing (here, a long session squeezed into a moment)
p.js(f"() => {{ {E}.att.activeMs = 40 * 60000 + 1000; {E}._tickNow(); }}")
time.sleep(0.3)
tm = p.js("() => document.querySelector('.ex-timer').textContent")
check(tm == '40 minutes (about 40 suggested)' and ev('exam:suggested', "d.paper === 's1-essay' && d.minutes === 40") == 1, f'at 40 minutes the clock says so, and nothing is locked: {tm!r}')
check(p.js("() => document.querySelector('.ex-area').getAttribute('contenteditable')") == 'true', 'the essay can still be written after 40 minutes')
p.shot('s1-essay-writing')
click('.ex-tile.review')
p.wait("() => document.querySelector('.ex-submit')", timeout=10000)
click('.ex-submit')
time.sleep(0.2)
mt = p.js("() => document.querySelector('.modal') ? document.querySelector('.modal').innerText : ''")
check('Then you hand it in, from the page that follows: it goes straight to Tim Hearn’s Google Drive.' in mt, f'Submit asks first, and says how it will then be handed in: {mt[-120:]!r}')
click('.modal button:has-text("Submit now")')
p.wait("() => document.querySelector('.ex-receipt')", timeout=10000)
check(wait_ticked('es-submit', 5), 'submitting ticks es-submit')
# ---------------------------------------------------------------- handing it in
# Straight to Tim Hearn's Google Drive, through the hand-in script (config.js: handIn.script – handin/Code.gs, a web
# app of Google Apps Script). Here the script is a stand-in, so that the tests never hand anything in.
TEST_PW = 'the-stand-in-password'   # (the stand-in's: the real password is never in the tests)
# (the real password is given to students, and must never be in the site: given as BMS_HANDIN_PASSWORD, every file is
# searched for it; it is not written here)
PW = os.environ.get('BMS_HANDIN_PASSWORD')
if PW:
    ROOT = os.path.dirname(os.path.dirname(OUT))
    found = []
    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in ('.git', 'out', '__pycache__', 'slides', 'anatomy', 'sims', 'recordings', 'molecules')]
        for f in files:
            try:
                if PW in open(os.path.join(dirpath, f), encoding='utf-8', errors='ignore').read():
                    found.append(os.path.relpath(os.path.join(dirpath, f), ROOT))
            except OSError:
                pass
    check(not found, f'the hand-in password is in none of the site’s files: {found}')
FILE = 'supervision-1-essay-ada-lovelace.docx'
RX = '.ex-receipt .ex-hi'
STILL = 'If it still won’t go, download a copy (below), and send it to Tim Hearn another way.'


def state():
    return p.js("() => MG.siteStore.get('paper:s1-essay')") or {}


def modal_text():
    return p.js("() => document.querySelector('.modal') ? document.querySelector('.modal').innerText : ''")


def pill():
    """the essay's line in the list of papers"""
    p.js(f"() => {E}.home()")
    p.wait("() => document.querySelector('.ex-card[data-paper=\"s1-essay\"] .ex-pill')", timeout=10000)
    return p.js("() => document.querySelector('.ex-card[data-paper=\"s1-essay\"] .ex-pill').textContent")


def essay_text(docx_bytes):
    return re.sub(r'<[^>]+>', '', zipfile.ZipFile(io.BytesIO(docx_bytes)).read('word/document.xml').decode('utf-8'))


class Script:
    """the hand-in script, as a stand-in: it keeps what it is sent, and answers as handin/Code.gs does – or, when it is
    told to (.next), doesn't answer ('network'), is busy ('busy') or sends back something that isn't its answer
    ('garbled')"""
    def __init__(self, url):
        self.url = url
        self.calls = []     # (method, url) of every request
        self.posts = []     # (headers, the hand-in) of each one that reached it
        self.replies = []
        self.files = []
        self.next = None

    def __call__(self, route):
        req = route.request
        self.calls.append((req.method, req.url))
        how, self.next = self.next, None
        if how == 'network':
            return route.abort('internetdisconnected')
        cors = {'Access-Control-Allow-Origin': '*'}
        if req.method != 'POST' or req.url != self.url:
            return route.fulfill(status=404, headers=cors, body='')
        if how == 'garbled':
            return route.fulfill(status=502, headers=dict(cors, **{'Content-Type': 'text/html'}), body='<html><body>Bad gateway</body></html>')
        d = json.loads(req.post_data)
        self.posts.append((req.headers, d))
        if how == 'busy':
            r = {'ok': False, 'error': 'busy', 'message': 'The hand-in is busy. Try again in a moment.'}
        elif d.get('password') != TEST_PW:
            r = {'ok': False, 'error': 'password', 'message': 'That isn’t the hand-in password.'}
        else:
            name, n = d['file']['name'], 1
            while name in self.files:
                n += 1
                name = d['file']['name'][:-5] + f' ({n}).docx'
            self.files.append(name)
            r = {'ok': True, 'receipt': f"S{d['week']}-Xy7Q{len(self.files):02d}", 'file': name, 'folder': f"Supervision {d['week']}",
                 'time': time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())}
        self.replies.append(r)
        route.fulfill(status=200, headers=dict(cors, **{'Content-Type': 'application/json; charset=utf-8'}), body=json.dumps(r))


def handin(script):
    """hands in the essay just submitted, from its receipt, straight to the hand-in script (a stand-in): with no
    password, a wrong one, no answer, the hand-in busy and an answer that isn't its own – each said, with what to do –
    then the right password, and the receipt. Then, on the paper's first page, it is handed in again: a second copy."""
    S = Script(script)
    p.ctx.route('https://script.google.com/**', S)
    p.ctx.route('https://script.googleusercontent.com/**', lambda r: r.abort())
    hb = p.js(f"() => document.querySelector('{RX}') ? document.querySelector('{RX}').innerText : ''")
    check('Now hand it in' in hb and 'Your essay goes straight from here to Tim Hearn’s Google Drive. Type the hand-in password that Tim Hearn gave you, and press Hand it in.' in hb,
          f'the receipt hands the essay in from here, with the hand-in password: {hb[:220]!r}')
    hint = p.js("() => document.querySelector('.ex-receipt p.hint').textContent")
    check('When you hand it in, its Word document goes to Tim Hearn’s Google Drive, and nowhere else.' in hint, f'and says where it goes: {hint!r}')
    check('Dropbox' not in p.js("() => document.querySelector('.ex-receipt').textContent"), 'and doesn’t mention Dropbox')
    box = p.js(f"() => {{ const i = document.querySelector('{RX} .ex-hi-pw'); return [i.type, i.getAttribute('autocomplete'), i.value, !!i.closest('form')]; }}")
    check(box == ['password', 'off', '', True], f'the password goes in a password box, which the browser doesn’t fill in: {box}')
    words = int(re.search(r'(\d+) words', p.js("() => document.querySelector('.ex-receipt').innerText")).group(1))

    def send(pw=None, how=None, enter=False):
        """types the password (unless None), and hands it in; what the page then says"""
        if pw is not None:
            P.fill(f'{RX} .ex-hi-pw', pw)
        S.next = how
        p.js(f"() => {{ document.querySelector('{RX} .ex-hi-msg').textContent = ''; }}")
        if enter:
            P.press(f'{RX} .ex-hi-pw', 'Enter')
        else:
            click(f'{RX} .ex-hi-go')
        p.wait(f"""() => {{ const g = document.querySelector('{RX} .ex-hi-go'), m = document.querySelector('{RX} .ex-hi-msg');
            return !g || (!g.disabled && m && m.textContent && !/^Sending/.test(m.textContent)); }}""", timeout=20000)
        return p.js(f"() => document.querySelector('{RX} .ex-hi-msg') ? document.querySelector('{RX} .ex-hi-msg').textContent : ''")

    msg = send('')
    check(msg == 'Type the hand-in password that Tim Hearn gave you.' and not S.calls, f'with no password, it asks for one, and sends nothing: {msg!r}')
    msg = send('a wrong password')
    check(msg == 'That isn’t the hand-in password. Check it with Tim Hearn, and try again.' and len(S.posts) == 1, f'a wrong password is refused by the hand-in: {msg!r}')
    check(ev('exam:handin', "d.paper === 's1-essay' && d.step === 'failed' && d.error === 'password'") == 1 and not ticked('es-send') and not state().get('handedIn'),
          'and the essay isn’t handed in: es-send waits')
    msg = send(TEST_PW, 'network')
    check(msg == 'Your essay couldn’t be sent: Tim Hearn’s Google Drive didn’t answer. Check that you are online, and try again. ' + STILL,
          f'when the hand-in doesn’t answer, it says so, and what to do: {msg!r}')
    msg = send(None, 'busy')
    check(msg == 'The hand-in is busy. Try again in a moment. ' + STILL, f'the hand-in’s own messages are passed on: {msg!r}')
    msg = send(None, 'garbled')
    check(msg == 'The hand-in sent back an answer that couldn’t be read (502). Try again in a moment. ' + STILL, f'and an answer that isn’t the hand-in’s is caught: {msg!r}')
    check(not state().get('handedIn') and not ticked('es-send') and len(S.replies) == 2, 'none of them hands it in')
    # on a phone (where the workbench opens over the instructions), the password and the button fit
    P.set_viewport_size({'width': 390, 'height': 844})
    p.js("() => document.body.classList.add('bench-open')")
    time.sleep(0.6)
    P.locator(f'{RX} .ex-hi-pw').scroll_into_view_if_needed()
    fit = p.js(f"""() => {{ const b = document.querySelector('{RX}'), i = b.querySelector('.ex-hi-pw'), g = b.querySelector('.ex-hi-go');
        return [b.scrollWidth <= b.clientWidth + 1, Math.round(i.getBoundingClientRect().width), g.getBoundingClientRect().right <= innerWidth + 1]; }}""")
    check(fit[0] and fit[1] >= 150 and fit[2], f'on a phone, the password box and the button fit: {fit}')
    p.shot('s1-handin-phone')
    p.js("() => document.body.classList.remove('bench-open')")
    P.set_viewport_size({'width': 1500, 'height': 950})
    time.sleep(0.4)
    # the right password (pressing Enter)
    send(TEST_PW, enter=True)
    p.wait(f"() => document.querySelector('{RX}.handed')", timeout=20000)
    hdr, d = S.posts[-1]
    R = S.replies[-1]
    check(len(S.posts) == 3 and R.get('ok') and all(m == 'POST' and u == script for m, u in S.calls), f'it is sent to the hand-in script, as a POST: {S.calls[-1][0]}')
    ct = hdr.get('content-type', '')
    check(ct.startswith('text/plain'), f'as text, which needs no preflight: {ct}')
    check(d.get('v') == 1 and d.get('password') == TEST_PW and d.get('paper') == 's1-essay' and d.get('week') == 1 and d.get('title') == 'Supervision 1 essay'
          and d.get('name') == NAME and d.get('words') == words and d.get('submitted') and d.get('site') == p.base + 'supervision-1.html',
          f'with the password, the paper, the student and the number of words: { {k: v for k, v in d.items() if k not in ("file", "password")} }')
    f = d.get('file') or {}
    raw = base64.b64decode(f.get('data') or '')
    check(f.get('name') == FILE and f.get('type') == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' and raw[:2] == b'PK',
          f'and the Word document, named after the essay and the student: {f.get("name")}, {len(raw)} bytes')
    doc = essay_text(raw)
    check(NAME in doc and 'Discuss, with examples, why negative feedback' in doc and 'Negative feedback opposes a change' in doc,
          'the Word document has the student’s name, the title and the essay')
    time.sleep(0.3)
    done_text = p.js(f"() => document.querySelector('{RX}').innerText")
    check('Handed in to Tim Hearn' in done_text and 'Received by Tim Hearn’s Google Drive at' in done_text and f'receipt {R["receipt"]}' in done_text
          and FILE in done_text and 'in the folder Supervision 1' in done_text, f'the receipt says it has arrived, and where it was saved: {done_text[:240]!r}')
    check(wait_ticked('es-send', 5) and ev('exam:handin', f"d.paper === 's1-essay' && d.step === 'confirmed' && d.receipt === '{R['receipt']}'") == 1,
          'handing it in ticks es-send')
    st = state()
    check(st.get('handedIn') == R['time'] and st.get('receipt') == R['receipt'] and st.get('file') == FILE and st.get('folder') == 'Supervision 1'
          and all(st.get(k) for k in ('started', 'submitted')), f'the site remembers it, with the receipt: {st}')
    kept = p.js("""async () => { const E = MG.app.exam; let t = JSON.stringify(Object.assign({}, localStorage)) + JSON.stringify(Object.assign({}, sessionStorage));
        for (const f of E._attemptFiles()) t += await E.fs.readText(f); return t; }""")
    check(len(kept) > 1000 and TEST_PW not in kept and 'a wrong password' not in kept, 'the password is kept nowhere: not in the browser’s storage, nor with the essay')
    p.shot('s1-essay-receipt')
    with P.expect_download() as dl:
        click(f'{RX} button:has-text("Download your copy")')
    check(dl.value.suggested_filename == FILE and wait_ticked('es-word', 5), 'Download your copy downloads the Word document, and ticks es-word')
    path = os.path.join(OUT, 's1-essay.docx')
    dl.value.save_as(path)
    mine = essay_text(open(path, 'rb').read())
    check(NAME in mine and 'Negative feedback opposes a change' in mine, 'the copy has the student’s name and the essay')
    # the paper's first page: handed in, with the receipt; and handing it in again, which sends a second copy
    p.js(f"() => {E}.openPaper('s1-essay')")
    p.wait("() => document.querySelector('.ex-startacts') && /You submitted this at/.test(document.querySelector('.ex-startacts').innerText)", timeout=10000)
    sa = p.js("() => document.querySelector('.ex-startacts').innerText")
    acts = p.js("() => [...document.querySelectorAll('.ex-startacts .btn')].map(b => b.textContent)")
    check('Handed in to Tim Hearn' in sa and f'receipt {R["receipt"]}' in sa and acts == ['Download your copy', 'See what you submitted', 'Start a new attempt'],
          f'the paper’s first page says it is handed in, with the receipt: {acts}')
    click('.ex-startacts button:has-text("Hand it in again")')
    time.sleep(0.2)
    mt = modal_text()
    check('second copy' in mt and 'the first one is kept' in mt, f'handing it in again says that it sends a second copy: {mt[:160]!r}')
    click('.modal button:has-text("Keep it as it is")')
    time.sleep(0.2)
    check(state().get('handedIn') == R['time'], 'Keep it as it is keeps it handed in')
    click('.ex-startacts button:has-text("Hand it in again")')
    time.sleep(0.2)
    click('.modal button:has-text("Hand it in again")')
    time.sleep(0.3)
    st = state()
    check(not st.get('handedIn') and not st.get('receipt') and p.js("() => !!document.querySelector('.ex-startacts .ex-hi-pw')"), 'Hand it in again asks for the password again')
    pl = pill()
    check(pl == 'Submitted · not handed in yet', f'and the list of papers says it is to hand in: {pl}')
    p.js(f"() => {E}.openPaper('s1-essay')")
    p.wait("() => document.querySelector('.ex-startacts .ex-hi-pw')", timeout=10000)
    P.fill('.ex-startacts .ex-hi-pw', TEST_PW)
    click('.ex-startacts .ex-hi-go')
    p.wait("() => document.querySelector('.ex-startacts .ex-hi.handed')", timeout=20000)
    R2 = S.replies[-1]
    sa = p.js("() => document.querySelector('.ex-startacts').innerText")
    check(R2.get('ok') and R2['receipt'] != R['receipt'] and f'receipt {R2["receipt"]}' in sa and 'supervision-1-essay-ada-lovelace (2).docx' in sa,
          f'handed in again: a second copy, with a receipt of its own: {sa[:200]!r}')
    pl = pill()
    check(pl.startswith('Handed in'), f'and the list of papers says it is handed in: {pl}')


handin(SCRIPT)
P.locator('.q[data-q="es-q-next"] textarea').fill('Take a clearer position in the introduction.')
time.sleep(0.6)
check(answered('es-q-next'), 'es-q-next is answered')
no_errors('the essay')

# ====================================================================== 7 More practice
chapter('s1-more')
check(p.js("() => document.querySelectorAll('#s1-more ol.titles li').length") == 9, 'the five SAQs and the four revision titles are listed')
click('#s1-more button[data-exam="s1-saqs"]')
p.wait("() => document.querySelector('.ex-startcard h2') && /short-answer/.test(document.querySelector('.ex-startcard h2').textContent)", timeout=10000)
sc = p.js("() => document.querySelector('.ex-startcard').textContent")
check('Supervision 1 · optional' in sc and 'No time limit' in sc and 'not to hand in' in sc, f'the SAQs are optional practice, with no time limit: {sc[:160]!r}')

# ====================================================================== progress, and the landing page afterwards
prog = p.js("() => document.querySelector('.progress-label').textContent")
pct = int(prog.split('%')[0])
check(pct >= 90, f'nearly everything counted is done: {prog}')
undone = p.js("""() => { const s = MG.tutorial.state; const t = [...document.querySelectorAll('[data-task]')].filter(li => !li.closest('.optional') && !s.tasks[li.dataset.task]).map(li => li.dataset.task);
    const q = [...document.querySelectorAll('.q[data-q]')].filter(x => !x.closest('.optional') && !(s.answers[x.dataset.q] || {}).done).map(x => x.dataset.q); return t.concat(q); }""")
check(set(undone) <= {'ck-q-thirst', 'ck-q-light', 'wh-q-light', 'wh-q-pit', 'ht-q-one'}, f'what is left is the written answers this test didn’t type: {undone}')
p.open('index.html')
tile = p.js("() => document.querySelector('.tile[data-sup=\"1\"]').innerText")
m_ = re.search(r'(\d+) of (\d+) steps and questions done', tile)
check(m_ and int(m_.group(2)) == 67 and int(m_.group(1)) >= 60, f'the tile shows how far the student has got: {m_.group(0) if m_ else tile[:200]!r}')
check('✓ Essay handed in' in tile, f'and that the essay has been handed in: {tile[-120:]!r}')
check('dropbox' not in p.js("() => document.body.textContent").lower(), 'the landing page doesn’t mention Dropbox')
p.shot('s1-landing-after')
no_errors('the landing page afterwards')
p.close()

# ====================================================================== a phone
ph = Page(width=390, height=844, mobile=True)
ph.open('index.html')
w = ph.js("() => [document.documentElement.scrollWidth, window.innerWidth]")
check(w[0] <= w[1], f'the landing page fits a phone, with no sideways scrolling: {w}')
cols = ph.js("() => getComputedStyle(document.querySelector('.tiles')).gridTemplateColumns.split(' ').length")
check(cols == 1, f'one tile to a row on a phone ({cols})')
ph.shot('s1-phone-landing')
ph.open('supervision-1.html')
time.sleep(1.5)
w = ph.js("() => [document.documentElement.scrollWidth, window.innerWidth]")
check(w[0] <= w[1], f'Supervision 1 fits a phone: {w}')
ph.js("() => MG.app.showChapter('s1-marking', true)")
time.sleep(0.8)
over = ph.js("() => [...document.querySelectorAll('#s1-marking .crit, #s1-marking .sample-essay, #s1-week .handin-box')].filter(e => e.scrollWidth > e.clientWidth + 1).length")
check(over == 0, f'the criteria and the essay fit the phone’s width ({over} overflow)')
ph.shot('s1-phone-marking')
ph.close()
done()
