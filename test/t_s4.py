"""Supervision 4 (supervision-4.html), as a student would use it: tile 4 on the landing page, the week's papers first in
Supervision work, the two optional exercises, whose steps don't count towards finishing the page (cardiac muscle in the
Microscope, with an intercalated disc and a nucleus labelled; the heart sounds with the ECG in the Recorder, played, and
systole and diastole measured between the marked sounds; the PR and QT intervals of one beat of the 12-lead ECG,
measured with the calipers and recognised by the Recorder; second-degree heart block; Furchgott's experiment in the
Organ bath, on rings of rat aorta with and without the endothelium, with nitroprusside, and acetylcholine at a high
concentration on the rubbed ring; Poiseuille's fourth power), and the work to hand in: the essay, written, submitted
and handed in (through a stand-in for the hand-in script, so that nothing is handed in), with the Word document
checked; the guidance after submitting; the short-answer questions, whose guidance draws a pressure–volume loop; the
revision titles; the landing page's progress and status afterwards; a phone.
Run:  python3 test/t_s4.py   (screenshots in test/out/s4-*.png)"""
import base64
import io
import json
import os
import re
import time
import zipfile

from h import Page, check, done, OUT

E = 'MG.app.exam'
RC = 'MG.app.recorder'
B = 'MG.app.bath'
NAME = 'Ada Lovelace'
PAPER = 's4-essay'
FILE = 'supervision-4-essay-ada-lovelace.docx'
ESSAY = ('Explain how the structural and electrical properties of cardiac muscle enable coordinated, rhythmic pumping '
         'of blood while allowing relaxation between beats.')
TEST_PW = 'the-stand-in-password'   # (the stand-in's: the real password is never in the tests)

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
    P.locator(f'.q[data-q="{qid}"] .mcq label[data-correct]').click()
    time.sleep(0.15)
    fb = p.js(f"() => document.querySelector('.q[data-q=\"{qid}\"] .q-feedback').textContent")
    return answered(qid) and fb.startswith('✓')


def short(qid, text):
    q = P.locator(f'.q[data-q="{qid}"]')
    q.locator('input[type=text]').fill(text)
    q.locator('button:has-text("Check")').click()
    time.sleep(0.2)
    return answered(qid)


def model(qid, text):
    """types an answer to a question and shows its model answer; the model answer's text"""
    P.locator(f'.q[data-q="{qid}"] textarea').fill(text)
    P.locator(f'.q[data-q="{qid}"] button:has-text("Show answer")').click()
    time.sleep(0.2)
    return p.js(f"() => document.querySelector('.q[data-q=\"{qid}\"]').innerText")


def listen():
    p.js("() => { window.__s4ev = []; MG.bus.on('*', (d, t) => { try { window.__s4ev.push([t, JSON.parse(JSON.stringify(d || {}, (k, v) => k === 'st' ? undefined : v))]); } catch (e) {} }); }")


def evs(kind, cond='true'):
    return p.js(f"() => (window.__s4ev || []).filter(e => e[0] === '{kind}' && (d => {cond})(e[1])).map(e => e[1])")


def no_errors(where):
    errs = [e for e in p.errors if 'ResizeObserver' not in e]
    check(not errs, f'no errors in the page ({where}): {errs[:3]}')
    p.errors.clear()


def essay_text(docx_bytes):
    return re.sub(r'<[^>]+>', '', zipfile.ZipFile(io.BytesIO(docx_bytes)).read('word/document.xml').decode('utf-8'))


def rec_open(spec, rid):
    click(f'#s4-beat button[data-rec="{spec}"]')
    p.wait(f"() => {RC} && {RC}.R && {RC}.R.id === '{rid}' && !{RC}._raf", timeout=30000)
    time.sleep(0.4)


def calipers(lane, ta, tb):
    """drags the calipers on a channel of the Recorder from ta to tb (s); the rec:measure it sends"""
    n = len(evs('rec:measure'))
    y = p.js(f"(l) => {RC}._clientY(l)", lane)
    xa, xb = p.js(f"(b) => [{RC}._clientX(b[0]), {RC}._clientX(b[1])]", [ta, tb])
    m = P.mouse
    m.move(xa, y)
    m.down()
    for k in range(1, 9):
        m.move(xa + (xb - xa) * k / 8, y)
    m.up()
    time.sleep(0.4)
    got = evs('rec:measure')
    return got[-1] if len(got) > n else None


def bath_do(task, cmd):
    """clicks the show-me button of a step of the Organ bath chapter"""
    click(f'#s4-endo li[data-task="{task}"] button[data-bath-do="{cmd}"]')
    time.sleep(0.4)


# ====================================================================== the landing page: Supervision 4 is ready
p.open('index.html')
p.js("() => { localStorage.clear(); sessionStorage.clear(); }")
p.js("() => new Promise((ok) => { const r = indexedDB.deleteDatabase('bmssup-files'); r.onsuccess = r.onerror = r.onblocked = () => ok(); })")
p.open('index.html')
t4 = p.js("() => { const t = document.querySelector('.tile[data-sup=\"4\"]'); return [t.getAttribute('href'), t.classList.contains('ready'), t.innerText]; }")
check(t4[0] == 'supervision-4.html' and t4[1], f'tile 4 opens Supervision 4’s own page: {t4[:2]}')
check('The heart and the circulation' in t4[2] and 'To hand in: an essay on how cardiac muscle makes the heart a rhythmic pump' in t4[2]
      and 'Essay not started yet' in t4[2], f'it names the topic and the essay to hand in, and nothing is started: {t4[2][:300]!r}')
rest = p.js("() => [...document.querySelectorAll('.tile')].slice(4).map(t => t.getAttribute('href') + (t.classList.contains('soon') ? ':soon' : ''))")
check(rest == ['workbench.html:soon'] * 4, f'Supervisions 5 to 8 are still to come: {rest}')
p.js(f"() => MG.user.setFullName('{NAME}')")

# ====================================================================== Supervision 4's page
p.open('supervision-4.html')
listen()
chs = p.js("() => [...document.querySelectorAll('.chapter')].map(c => c.id + ':' + c.dataset.num)")
check(chs == ['s4-week:0', 's4-beat:1', 's4-endo:2', 's4-write:3', 's4-more:4'], f'Supervision 4 has its five chapters: {chs}')
check(p.js("() => document.body.dataset.week") == '4', 'the page knows it is week 4')
check(p.js("() => MG.app.currentBench") == 'exam', 'the page opens on Supervision work')
p.wait("() => document.querySelectorAll('.ex-card').length >= 11", timeout=30000)
cards = p.js("() => [...document.querySelectorAll('.ex-card')].filter(c => !c.closest('details')).map(c => c.dataset.paper + ':' + (c.querySelector('.ex-badge') ? c.querySelector('.ex-badge').textContent : ''))")
check(cards[:3] == ['s4-essay:To hand in', 's4-saqs:Optional', 's4-revision:Optional'], f'this week’s papers come first, the essay to hand in at the top: {cards[:3]}')
others = p.js("() => [...document.querySelectorAll('details.ex-others .ex-card')].map(c => c.dataset.paper)")
check(others == ['s1-essay', 's1-saqs', 's1-revision', 's2-work', 's2-revision', 's3-essay', 's3-saqs', 's3-revision'],
      f'the earlier weeks’ papers are kept apart: {others}')
meta = p.js("() => document.querySelector('.ex-card[data-paper=\"s4-essay\"] .ex-cmeta').textContent")
check('No time limit (about 40 minutes suggested)' in meta, f'the essay has no time limit, and suggests 40 minutes: {meta}')
box = p.js("() => document.querySelector('#s4-week .handin-box').innerText")
check(ESSAY in box and 'hand-in password I give you, and your essay then goes straight into my Google Drive' in box,
      f'This week shows the essay to hand in, and how it is handed in: {box[-170:]!r}')
links = p.js("() => [...document.querySelectorAll('.chapter a[href^=\"supervision-\"]')].map(a => a.getAttribute('href'))")
check(links == ['supervision-1.html#s1-marking'], f'it points back to the marking criteria: {links}')
check(wait_ticked('w4-name', 5), 'the name given on the landing page ticks w4-name')
counted = p.js("""() => [...document.querySelectorAll('[data-task], .q[data-q]')].filter(x => !x.closest('.optional')).map(x => x.dataset.task || x.dataset.q)""")
check(counted == ['w4-name', 'es4-start', 'es4-write', 'es4-submit', 'es4-send', 'es4-word', 'es4-q-next'],
      f'only the essay counts towards finishing the page, not the optional chapters: {counted}')
p.shot('s4-week')
no_errors('opening Supervision 4')

# ====================================================================== 1 (optional) The heartbeat
chapter('s4-beat')
check(p.js("() => MG.app.currentBench") == 'scope', 'the chapter opens the Microscope')
check(p.js("() => !!document.querySelector('#s4-beat .optional.whole')") and 'Optional, about 15 minutes' in p.js("() => document.querySelector('#s4-beat').innerText"),
      'it says that it is optional')
click('#s4-beat button[data-scope="heart@1.779,2.273,20x"]')
p.wait("() => MG.app.scope && MG.app.scope.current() === 'heart'", timeout=30000)
check(wait_ticked('hb-open', 5) and p.js("() => Math.round(MG.app.scope.mag())") == 20, 'the heart opens at 20×, at cardiac muscle cut lengthways (hb-open)')
time.sleep(3)
r = p.js("() => { const b = document.querySelector('.ms-view').getBoundingClientRect(); return [b.x, b.y, b.width, b.height]; }")
x0, y0 = r[0], r[1]


def label(x, y, text):
    click('#s4-beat button[data-scope-tool="label"]')
    time.sleep(0.3)
    P.mouse.click(x0 + x, y0 + y)
    p.wait("() => document.querySelector('.modal input')", timeout=5000)
    P.fill('.modal input', text)
    P.keyboard.press('Enter')
    time.sleep(0.4)


label(240, 130, 'Intercalated disc')
check(wait_ticked('hb-disc', 5) and not ticked('hb-nuc'), 'labelling an intercalated disc ticks hb-disc (and not the nucleus’s step)')
label(330, 300, 'Nucleus')
check(wait_ticked('hb-nuc', 5), 'labelling a nucleus ticks hb-nuc')
p.shot('s4-heart')
txt = model('hb-q-discs', 'Gap junctions let the action potential spread, desmosomes hold the cells together.')
check('functional syncytium' in txt, 'the model answer can be shown once the question has been tried')
# the heart sounds
rec_open('heart-sounds@0.4,2.4', 'heart-sounds')
check(wait_ticked('hb-snd', 5) and p.js(f"() => {RC}._lanes().map(L => L.short)") == ['PCG', 'ECG'], 'the heart sounds open, with the ECG (hb-snd)')
ev = p.js(f"() => {RC}.R.events.map(e => [e.label, e.t])")
s1 = [t for l, t in ev if l == 'S1']
s2 = [t for l, t in ev if l == 'S2']
check(len(s1) > 30 and len(s2) > 30, f'the sounds are marked S1 and S2 ({len(s1)} and {len(s2)})')
click('#s4-beat button[data-rec-tool="listen"]')
click('#s4-beat button[data-rec-tool="play"]')
check(wait_ticked('hb-listen', 5), 'playing the heart sounds ticks hb-listen')
time.sleep(1)
p.js(f"() => {RC}.tool('stop')")
rec_open('heart-sounds@0.4,2.4', 'heart-sounds')
click('#s4-beat button[data-rec-tool="calipers"]')
time.sleep(0.3)
a1 = [t for t in s1 if 0.5 < t < 0.8][0]
a2 = [t for t in s2 if a1 < t < a1 + 0.5][0]
a3 = [t for t in s1 if a2 < t < a2 + 0.8][0]
m = calipers('PCG', a1, a2)
check(m and m['signal'] == 'pcg' and abs(m['dt'] - (a2 - a1)) < 0.02 and wait_ticked('hb-sys', 5),
      f'systole, from S1 to S2, measured on the heart sounds: {m and m["dt"]} s (hb-sys)')
m2 = calipers('PCG', a2, a3)
check(m2 and abs(m2['dt'] - (a3 - a2)) < 0.02 and wait_ticked('hb-dia', 5), f'and diastole, from S2 to the next S1: {m2 and m2["dt"]} s (hb-dia)')
check(0.2 < m['dt'] < 0.32 and 0.45 < m2['dt'] < 0.6, f'diastole is about twice as long as systole at rest, as the model answer says ({m["dt"]:.3f} and {m2["dt"]:.3f} s)')
txt = model('hb-q-sounds', 'S1 is the AV valves closing as the ventricles contract after the QRS; S2 is the semilunar valves closing.')
check('about 0.26 s and diastole about 0.53 s' in txt, 'the model answer gives the recording’s systole and diastole')
p.shot('s4-heart-sounds')
# the ECG's intervals, in one beat of lead II
rec_open('ecg-12lead@1.1,2.1:II', 'ecg-12lead')
check(wait_ticked('hb-12', 5) and p.js(f"() => {RC}._lanes().map(L => L.short)") == ['II'], 'one beat of lead II of the 12-lead ECG opens (hb-12)')
click('#s4-beat button[data-rec-tool="calipers"]')
time.sleep(0.3)
R = p.js(f"() => {RC}.R.beats.t.filter(t => t > 1.1 && t < 2.1)")
check(len(R) == 1 and abs(R[0] - 1.406) < 0.01, f'(one R wave in view, at {R})')
m = calipers('II', 1.195, 1.375)
check(m and m['interval'] == 'PR' and abs(m['dt'] - 0.18) < 0.01 and wait_ticked('hb-pr', 5), f'the PR interval, from the start of the P wave to the start of the QRS, is recognised: {m and (m["interval"], m["dt"])} (hb-pr)')
m = calipers('II', 1.375, 1.73)
check(m and m['interval'] == 'QT' and abs(m['dt'] - 0.355) < 0.01 and wait_ticked('hb-qt', 5), f'and the QT interval, from the start of the QRS to the end of the T wave: {m and (m["interval"], m["dt"])} (hb-qt)')
p.shot('s4-ecg-qt')
txt = model('hb-q-qt', 'About a hundred times longer than in skeletal muscle, so the heart cannot be tetanised.')
check('about 0.36 s' in txt and 'tetanised' in txt, 'the model answer gives the QT that was measured')
rec_open('ecg-block@8,20', 'ecg-block')
check(wait_ticked('hb-block', 5), 'the heart block opens (hb-block)')
no_errors('the optional exercise on the heartbeat')

# ====================================================================== 2 (optional) Furchgott's experiment
chapter('s4-endo')
check(p.js("() => MG.app.currentBench") == 'bath', 'the chapter opens the Organ bath')
check(p.js("() => !!document.querySelector('#s4-endo .optional.whole')"), 'it is optional')
click('#s4-endo button[data-bath="aorta?seed=1"]')
p.wait(f"() => {B} && {B}.exp && {B}.exp.type === 'aorta' && {B}.exp.opts.endothelium !== false && {B}.exp.seed == 1", timeout=60000)
check(wait_ticked('fu-ring', 5) and p.js(f"() => {B}.speeds.aorta") == 20, 'a ring of aorta with its endothelium is set up, its clock at 20 times (fu-ring)')
bath_do('fu-pe', 'add phenylephrine 1e-6')
bath_do('fu-pe', 'plateau')
check(wait_ticked('fu-pe', 5), 'phenylephrine contracts it (fu-pe)')
bath_do('fu-ach', 'add acetylcholine 1e-6')
bath_do('fu-pe', 'plateau')
check(not ticked('fu-ach'), '(the relaxation is read when the bath is washed)')
bath_do('fu-ach', 'wash')
rel = evs('bath:response', "d.drug === 'acetylcholine'")
check(wait_ticked('fu-ach', 5) and rel and 75 < rel[-1]['pct'] < 90, f'with its endothelium, acetylcholine relaxes most of the tone, as the model answer says (about 83%): {rel and rel[-1]["pct"]}% (fu-ach)')
pe = evs('bath:response', "d.drug === 'phenylephrine'")
check(pe and pe[-1]['response'] > 1, f'(phenylephrine’s contraction was {pe and pe[-1]["response"]} g)')
p.shot('s4-aorta')
click('#s4-endo button[data-bath="aorta?endothelium=off&seed=1"]')
p.wait(f"() => {B}.exp.opts.endothelium === false", timeout=30000)
check(wait_ticked('fu-rub', 5), 'a ring with its endothelium rubbed off is set up (fu-rub)')
bath_do('fu-snp', 'add phenylephrine 1e-6')
bath_do('fu-pe', 'plateau')
bath_do('fu-snp', 'add acetylcholine 1e-6')
bath_do('fu-pe', 'plateau')
bath_do('fu-snp', 'add nitroprusside 1e-6')
check(wait_ticked('fu-snp', 5), 'nitroprusside is added (fu-snp)')
rel = evs('bath:response', "d.drug === 'acetylcholine'")
check(rel and rel[-1]['pct'] < 10, f'without its endothelium, acetylcholine hardly relaxes it, as the model answer says (about 2%): {rel[-1]["pct"]}%')
bath_do('fu-pe', 'plateau')
bath_do('fu-wash', 'wash')
snp = evs('bath:response', "d.drug === 'nitroprusside'")
check(wait_ticked('fu-wash', 5) and snp and snp[-1]['pct'] > 95, f'but nitroprusside relaxes it completely: {snp and snp[-1]["pct"]}% (fu-wash)')
txt = model('fu-q-endo', 'The endothelium makes NO when acetylcholine acts on it.')
check('about 83%' in txt and 'about 2%' in txt, 'the model answer gives the two rings’ numbers')
check(mcq_right('fu-q-sild'), 'fu-q-sild: sildenafil inhibits PDE5')
bath_do('fu-high', 'plateau')
before = p.js(f"() => {B}.exp.recent(3)")
bath_do('fu-high', 'add acetylcholine 1e-4')
bath_do('fu-pe', 'plateau')
after = p.js(f"() => {B}.exp.recent(3)")
check(wait_ticked('fu-high', 5) and 0.4 < after - before < 0.7, f'at 10⁻⁴ M, acetylcholine contracts the rubbed ring by about half a gram, as the model answer says ({after - before:.2f} g) (fu-high)')
check(short('fu-q-r4', '0.5'), 'a 16% constriction leaves half the flow (fu-q-r4)')
p.shot('s4-aorta-rubbed')
no_errors('the optional exercise on the endothelium')

# ====================================================================== 3 Write your essay
chapter('s4-write')
check(p.js("() => MG.app.currentBench") == 'exam', 'the chapter opens Supervision work')
click('#s4-write button[data-exam="s4-essay"]')
p.wait("() => document.querySelector('.ex-startcard h2') && document.querySelector('.ex-startcard h2').textContent === 'Supervision 4 essay'", timeout=30000)
sc = p.js("() => document.querySelector('.ex-startcard').textContent")
check('No time limit, but we suggest about 40 minutes' in sc and 'Supervision 4 · to hand in' in sc and 'Tim Hearn' in sc,
      f'its first page: no time limit, 40 minutes suggested, and how to hand it in: {sc[:240]!r}')
click('.ex-startacts .btn.primary')
p.wait("() => document.querySelector('.ex-area')", timeout=30000)
check(wait_ticked('es4-start', 5), 'starting the essay ticks es4-start')
PARA = ('Cardiac muscle cells are joined end to end by intercalated discs, whose gap junctions let the action potential '
        'spread from cell to cell, so that each ventricle contracts as a functional syncytium, and the long plateau of '
        'the action potential keeps the cells refractory until they have begun to relax. ')
p.js("(t) => { const A = document.querySelector('.ex-area'); A.focus(); document.execCommand('insertText', false, t); }", (PARA * 7).strip())
time.sleep(1.6)
check(wait_ticked('es4-write', 5), f'writing more than 300 words ticks es4-write ({p.js("() => document.querySelector(\'.ex-wc\').textContent")})')
click('.ex-tile.review')
p.wait("() => document.querySelector('.ex-submit')", timeout=10000)
click('.ex-submit')
time.sleep(0.2)
click('.modal button:has-text("Submit now")')
p.wait("() => document.querySelector('.ex-receipt')", timeout=10000)
check(wait_ticked('es4-submit', 5), 'submitting ticks es4-submit')

# ---------------------------------------------------------------- handing it in (to a stand-in for the hand-in script)
SCRIPT = p.js("() => MG.config.handIn.script")
RX = '.ex-receipt .ex-hi'
posts, replies = [], []


def stand_in(route):
    req = route.request
    cors = {'Access-Control-Allow-Origin': '*'}
    if req.method != 'POST' or req.url != SCRIPT:
        return route.fulfill(status=404, headers=cors, body='')
    d = json.loads(req.post_data)
    posts.append(d)
    if d.get('password') != TEST_PW:
        r = {'ok': False, 'error': 'password', 'message': 'That isn’t the hand-in password.'}
    else:
        r = {'ok': True, 'receipt': f"S{d['week']}-Hb4K{len(posts):02d}", 'file': d['file']['name'], 'folder': f"Supervision {d['week']}",
             'time': time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())}
    replies.append(r)
    route.fulfill(status=200, headers=dict(cors, **{'Content-Type': 'application/json; charset=utf-8'}), body=json.dumps(r))


p.ctx.route('https://script.google.com/**', stand_in)
p.ctx.route('https://script.googleusercontent.com/**', lambda r: r.abort())


def send(pw):
    P.fill(f'{RX} .ex-hi-pw', pw)
    p.js(f"() => {{ document.querySelector('{RX} .ex-hi-msg').textContent = ''; }}")
    click(f'{RX} .ex-hi-go')
    p.wait(f"""() => {{ const g = document.querySelector('{RX} .ex-hi-go'), m = document.querySelector('{RX} .ex-hi-msg');
        return !g || (!g.disabled && m && m.textContent && !/^Sending/.test(m.textContent)); }}""", timeout=20000)
    return p.js(f"() => document.querySelector('{RX} .ex-hi-msg') ? document.querySelector('{RX} .ex-hi-msg').textContent : ''")


msg = send('a wrong password')
check(msg == 'That isn’t the right hand-in password. Check it with Tim Hearn and try again.' and not ticked('es4-send'), f'a wrong password is refused: {msg!r}')
send(TEST_PW)
p.wait(f"() => document.querySelector('{RX}.handed')", timeout=20000)
d, R = posts[-1], replies[-1]
check(R.get('ok') and d.get('paper') == PAPER and d.get('week') == 4 and d.get('title') == 'Supervision 4 essay' and d.get('name') == NAME and d.get('words', 0) > 300,
      f'the right password hands in the essay, week 4, with the student’s name: { {k: v for k, v in d.items() if k not in ("file", "password")} }')
raw = base64.b64decode((d.get('file') or {}).get('data') or '')
check((d.get('file') or {}).get('name') == FILE and raw[:2] == b'PK', f'as a Word document named after the paper and the student: {(d.get("file") or {}).get("name")}')
doc = essay_text(raw)
check(NAME in doc and ESSAY in doc and 'functional syncytium' in doc, 'the Word document has the student’s name, the title and the essay')
check(wait_ticked('es4-send', 5) and 'in the folder Supervision 4' in p.js(f"() => document.querySelector('{RX}').innerText"),
      'it arrives in the folder for Supervision 4, and es4-send ticks')
with P.expect_download() as dl:
    click(f'{RX} button:has-text("Download your copy")')
check(dl.value.suggested_filename == FILE and wait_ticked('es4-word', 5), 'Download your copy downloads the Word document, and ticks es4-word')
dl.value.save_as(os.path.join(OUT, 's4-essay.docx'))
p.shot('s4-receipt')
# the guidance, after submitting
click('.ex-receipt button:has-text("Review my answers")')
p.wait("() => document.querySelector('.ex-review')", timeout=10000)
rv = p.js("() => document.querySelector('.ex-review').innerText")
check(all(k in rv for k in ('functional syncytium', 'calcium-induced calcium release', 'refractory period', 'Frank–Starling', 'Against the core criteria')),
      'Review my answers shows the guidance, on coordination, rhythm and relaxation')
P.locator('.q[data-q="es4-q-next"] textarea').fill('I said almost nothing about relaxation, and should have explained SERCA and the exchanger.')
time.sleep(0.6)
check(answered('es4-q-next'), 'es4-q-next is answered')
no_errors('the essay and handing it in')

# ====================================================================== 4 More practice
chapter('s4-more')
saqs = p.js("() => [...document.querySelectorAll('#s4-more ol.titles')[0].querySelectorAll('li')].map(l => l.textContent)")
revs = p.js("() => [...document.querySelectorAll('#s4-more ol.titles')[1].querySelectorAll('li')].map(l => l.textContent)")
check(len(saqs) == 3 and len(revs) == 2, f'the three short-answer questions and the two revision titles are listed: {len(saqs)}, {len(revs)}')
check(saqs[0].startswith('A left ventricle has an EDV of 120 mL') and saqs[2] == 'Explain how the endothelium can cause vasodilatation of arterioles.'
      and revs[0].startswith('Discuss the factors that govern') and revs[1].startswith('Arteriolar resistance must meet'),
      'in the handouts’ own words')
click('#s4-more button[data-exam="s4-saqs"]')
p.wait("() => document.querySelector('.ex-startcard h2') && /short-answer/.test(document.querySelector('.ex-startcard h2').textContent)", timeout=10000)
sc = p.js("() => document.querySelector('.ex-startcard').innerText")
check('supervision 4 · optional' in sc.lower() and 'Only the essay needs to be handed in' in sc, f'the short-answer questions are optional: {sc[:120]!r}')
click('.ex-startacts .btn.primary')
p.wait("() => document.querySelector('.ex-area')", timeout=30000)
qt = p.js("() => document.querySelector('.ex-q').innerText")
check('EDV of 120 mL' in qt and 'Insert drawing' in qt, f'question 1 asks for the loop, drawn with Insert drawing: {qt[:80]!r}')
click('.ex-tb [data-cmd="ul"]')
for i, t in enumerate(['The loop runs anticlockwise: filling, isovolumetric contraction, ejection, isovolumetric relaxation.',
                       'The mitral valve closes at 120 mL (S1); the aortic valve opens.', 'The aortic valve closes at 50 mL (S2); the mitral valve opens.',
                       'Both valves are closed in the two isovolumetric phases.', 'Stroke volume = 120 − 50 = 70 mL.']):
    P.keyboard.type(t)
    if i < 4:
        P.keyboard.press('Enter')
time.sleep(1.6)
click('.ex-tile.review')
p.wait("() => document.querySelector('.ex-submit')", timeout=10000)
click('.ex-submit')
time.sleep(0.2)
click('.modal button:has-text("Submit now")')
p.wait("() => document.querySelector('.ex-receipt')", timeout=10000)
check(wait_ticked('m4-saq', 5), 'submitting the short-answer questions ticks m4-saq (optional)')
click('.ex-receipt button:has-text("Review my answers")')
p.wait("() => document.querySelector('.ex-review')", timeout=10000)
svg = p.js("() => { const s = document.querySelector('.ex-review svg'); if (!s) return null; const b = s.getBoundingClientRect(); return {lines: s.querySelectorAll('polyline').length, w: b.width, h: b.height, text: s.textContent}; }")
check(svg and svg['lines'] == 2 and svg['w'] > 250 and svg['h'] > 150 and all(k in svg['text'] for k in ('S1', 'S2', 'both valves', '70 mL')),
      f'the guidance for question 1 draws the pressure–volume loop: {svg and {k: v for k, v in svg.items() if k != "text"}}')
rv = p.js("() => document.querySelector('.ex-review').innerText")
check(all(k in rv for k in ('glycocalyx', 'reflection coefficient', 'guanylyl cyclase', 'sildenafil', 'stroke work')), 'and covers the Starling forces and the endothelium')
p.shot('s4-saq-review')
click('.ex-revbar button:has-text("Back")')
time.sleep(0.5)
p.js(f"() => {E}.home()")
time.sleep(0.5)
click('#s4-more button[data-exam="s4-revision"]')
p.wait("() => document.querySelector('.ex-startcard h2') && document.querySelector('.ex-startcard h2').textContent === 'Essay titles for revision'", timeout=10000)
sc = p.js("() => document.querySelector('.ex-startcard').innerText")
check('supervision 4 · optional' in sc.lower() and 'Only the Supervision 4 essay needs to be handed in' in sc, f'the revision titles are optional: {sc[:120]!r}')
no_errors('more practice')

# ====================================================================== progress, and the landing page afterwards
undone = p.js("""() => { const s = MG.tutorial.state; const t = [...document.querySelectorAll('[data-task]')].filter(li => !li.closest('.optional') && !s.tasks[li.dataset.task]).map(li => li.dataset.task);
    const q = [...document.querySelectorAll('.q[data-q]')].filter(x => !x.closest('.optional') && !(s.answers[x.dataset.q] || {}).done).map(x => x.dataset.q); return t.concat(q); }""")
check(undone == [], f'everything that counts is done: {undone}')
prog = p.js("() => document.querySelector('.progress-label').textContent")
check(prog.startswith('100%'), f'the page says it is finished: {prog}')
p.open('index.html')
tile = p.js("() => document.querySelector('.tile[data-sup=\"4\"]').innerText")
check('7 of 7' in tile or 'All the exercises done' in tile, f'tile 4 shows the work done: {tile[-200:]!r}')
check('✓ Essay handed in' in tile, f'and that the essay has been handed in: {tile[-120:]!r}')
p.shot('s4-landing-after')
no_errors('the landing page afterwards')
p.close()

# ====================================================================== a phone
ph = Page(width=390, height=844, mobile=True)
ph.open('supervision-4.html')
time.sleep(1.5)
w = ph.js("() => [document.documentElement.scrollWidth, window.innerWidth]")
check(w[0] <= w[1], f'Supervision 4 fits a phone: {w}')
for cid in ('s4-week', 's4-beat', 's4-endo', 's4-write'):
    ph.js(f"() => MG.app.showChapter('{cid}', true)")
    time.sleep(0.6)
    over = ph.js(f"() => [...document.querySelectorAll('#{cid} .handin-box, #{cid} .activity, #{cid} .callout')].filter(e => e.scrollWidth > e.clientWidth + 1).length")
    check(over == 0, f'{cid} fits the phone’s width ({over} overflow)')
ph.shot('s4-phone')
ph.close()
done()
