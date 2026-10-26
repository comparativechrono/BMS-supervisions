"""Supervision 2 (supervision-2.html), as a student would use it: tile 2 on the landing page, the week's papers first in
Supervision work, the two optional exercises (equilibrium potentials and the GHK equation in R, the resting-potential
circuit with its Na+ switch, the Neuron simulation; nicotine, acetylcholine and hexamethonium on the ileum in the Organ
bath), whose steps don't count towards finishing the page, and the work to hand in: the thyroid in the Microscope (the
follicle that the button opens, three labels, the area of the lumen, the photograph), the area in R, and the paper –
the photograph put into part (a) from the workbench's files with Insert picture, part (b) under its 200-word limit, the
two short-answer questions in bullet points – submitted and handed in (through a stand-in for the hand-in script, so
that nothing is handed in), with the Word document checked (the picture, the bullet points, the student's name); the
guidance after submitting; the revision titles; the landing page's progress and status afterwards; a phone.
Run:  python3 test/t_s2.py   (screenshots in test/out/s2-*.png; R is downloaded from the internet)"""
import base64
import io
import json
import os
import re
import time
import zipfile

from h import Page, check, done, OUT

E = 'MG.app.exam'
NAME = 'Ada Lovelace'
PAPER = 's2-work'
FILE = 'supervision-2-work-ada-lovelace.docx'
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


def listen():
    p.js("() => { window.__s2ev = []; MG.bus.on('*', (d, t) => { try { window.__s2ev.push([t, JSON.parse(JSON.stringify(d || {}))]); } catch (e) {} }); }")


def evs(kind, cond='true'):
    return p.js(f"() => (window.__s2ev || []).filter(e => e[0] === '{kind}' && (d => {cond})(e[1])).map(e => e[1])")


def no_errors(where):
    errs = [e for e in p.errors if 'ResizeObserver' not in e]
    check(not errs, f'no errors in the page ({where}): {errs[:3]}')
    p.errors.clear()


def console():
    return p.js("() => { const c = MG.app.rstudio && MG.app.rstudio.cv && MG.app.rstudio.cv.out; return c ? c.textContent : ''; }")


def r_idle():
    return p.js("() => { const R = MG.app.rstudio; return R && R.S ? R.S.state : ''; }")


def run_button(where, code, wait_for=None, timeout=60):
    """clicks the show-me button (in the chapter where) that types code, and presses Enter in the Console; what R printed"""
    before = len(console())
    if not p.js("([w, c]) => { const b = [...document.querySelectorAll(`#${w} button[data-rcon]`)].find(x => x.dataset.rcon === c); if (!b) return false; b.scrollIntoView({block: 'center'}); b.click(); return true; }", [where, code]):
        return None
    time.sleep(0.6)
    P.keyboard.press('Enter')
    for _ in range(timeout * 4):
        time.sleep(0.25)
        out = console()[before:]
        if r_idle() == 'idle' and (wait_for is None or re.search(wait_for, out)):
            return out
    return console()[before:]


def essay_text(docx_bytes):
    return re.sub(r'<[^>]+>', '', zipfile.ZipFile(io.BytesIO(docx_bytes)).read('word/document.xml').decode('utf-8'))


# ====================================================================== the landing page: Supervision 2 is ready
p.open('index.html')
p.js("() => { localStorage.clear(); sessionStorage.clear(); }")
p.js("() => new Promise((ok) => { const r = indexedDB.deleteDatabase('bmssup-files'); r.onsuccess = r.onerror = r.onblocked = () => ok(); })")
p.open('index.html')
t2 = p.js("() => { const t = document.querySelector('.tile[data-sup=\"2\"]'); return [t.getAttribute('href'), t.classList.contains('ready'), t.innerText]; }")
check(t2[0] == 'supervision-2.html' and t2[1], f'tile 2 opens Supervision 2’s own page: {t2[:2]}')
check('Nerves, synapses and the autonomic nervous system' in t2[2] and 'To hand in: a practical question on the thyroid gland, and two short-answer questions' in t2[2]
      and 'Practical and short answers not started yet' in t2[2], f'it names the topic and the work to hand in, and nothing is started: {t2[2][:300]!r}')
rest = p.js("() => [...document.querySelectorAll('.tile')].slice(2).map(t => t.getAttribute('href') + (t.classList.contains('soon') ? ':soon' : ''))")
check(rest == ['workbench.html:soon'] * 6, f'Supervisions 3 to 8 are still to come: {rest}')
p.js(f"() => MG.user.setFullName('{NAME}')")

# ====================================================================== Supervision 2's page
p.open('supervision-2.html')
listen()
chs = p.js("() => [...document.querySelectorAll('.chapter')].map(c => c.id + ':' + c.dataset.num)")
check(chs == ['s2-week:0', 's2-ions:1', 's2-ans:2', 's2-thyroid:3', 's2-saq:4', 's2-more:5'], f'Supervision 2 has its six chapters: {chs}')
check(p.js("() => document.body.dataset.week") == '2', 'the page knows it is week 2')
check(p.js("() => MG.app.currentBench") == 'exam', 'the page opens on Supervision work')
p.wait("() => document.querySelectorAll('.ex-card').length >= 6", timeout=30000)
cards = p.js("() => [...document.querySelectorAll('.ex-card')].filter(c => !c.closest('details')).map(c => c.dataset.paper + ':' + (c.querySelector('.ex-badge') ? c.querySelector('.ex-badge').textContent : ''))")
check(cards[:2] == ['s2-work:To hand in', 's2-revision:Optional'], f'this week’s papers come first, the work to hand in at the top: {cards[:2]}')
others = p.js("() => [...document.querySelectorAll('details.ex-others .ex-card')].map(c => c.dataset.paper)")
check(others == ['s1-essay', 's1-saqs', 's1-revision'], f'last week’s papers are kept apart: {others}')
meta = p.js("() => document.querySelector('.ex-card[data-paper=\"s2-work\"] .ex-cmeta').textContent")
check(meta == 'No time limit · 4 questions', f'the work to hand in: no time limit and four questions, with no marks given ({meta})')
box = p.js("() => document.querySelector('#s2-week .handin-box').innerText")
check('practical question on the thyroid gland' in box and 'at least five' in box and 'hand-in password I give you, and your work then goes straight into my Google Drive' in box,
      f'This week shows the work to hand in, and how it is handed in: {box[-170:]!r}')
check(wait_ticked('w2-name', 5), 'the name given on the landing page ticks w2-name')
counted = p.js("""() => [...document.querySelectorAll('[data-task], .q[data-q]')].filter(x => !x.closest('.optional')).map(x => x.dataset.task || x.dataset.q)""")
check(len(counted) == 20 and not any(c.startswith(('io-', 'an-', 'm2-')) for c in counted),
      f'only the work to hand in counts towards finishing the page (20 steps and questions), not the optional chapters: {len(counted)}')
p.shot('s2-week')
no_errors('opening Supervision 2')

# ====================================================================== 1 (optional) Gradients and potentials
chapter('s2-ions')
check(p.js("() => MG.app.currentBench") == 'circuit', 'the chapter opens Circuits (not RStudio, which would start downloading R)')
check(p.js("() => !!document.querySelector('#s2-ions .optional.whole')") and 'Optional, about 15 minutes' in p.js("() => document.querySelector('#s2-ions').innerText"),
      'it says that it is optional')
p.js("() => [...document.querySelectorAll('#s2-ions button[data-rcon]')][0].click()")
for _ in range(400):
    if r_idle() == 'idle':
        break
    time.sleep(0.5)
check(r_idle() == 'idle', f'R starts in RStudio ({r_idle()})')
out = run_button('s2-ions', '58 * log10(2.25 / 140)', r'-104\.0')
check(out and '-104.0488' in out and wait_ticked('io-ek', 5), f'E(K) for frog muscle is −104 mV, as the model answer says: {(out or "").strip()[-40:]!r}')
out = run_button('s2-ions', '58 * log10(120 / 10)', r'62\.59')
check(out and '62.59251' in out and wait_ticked('io-ena', 5), f'and E(Na) +62.6 mV: {(out or "").strip()[-40:]!r}')
run_button('s2-ions', 'ghk <- function(r) 58 * log10((2.25 + r * 120) / (140 + r * 10))')
out = run_button('s2-ions', 'ghk(c(0.001, 0.01, 0.05, 0.1))', r'-57\.7')
nums = [round(float(x), 1) for x in re.findall(r'-\d+\.\d+', out or '')]
check(nums[-4:] == [-102.7, -93.3, -71.4, -57.7] and wait_ticked('io-ghk', 5), f'the GHK equation gives the numbers of the model answer: {nums[-4:]}')
check(mcq_right('io-q-ratio'), 'io-q-ratio: P(K) is about 70 times P(Na) in frog muscle')
P.locator('.q[data-q="io-q-e"] textarea').fill('E(K) -104 mV, E(Na) +63 mV; the potential moves towards E(Na).')
# the circuit
click('#s2-ions button[data-circuit="example:resting-potential"]')
p.wait("() => MG.app.circuit && MG.app.circuit.doc && /resting/i.test(MG.app.circuit.doc.title)", timeout=30000)
click('#s2-ions button[data-circuit-run]')
check(wait_ticked('io-open', 10), 'running the resting-potential circuit ticks io-open')
meter = lambda: p.js("() => [...document.querySelectorAll('.ci-meter, .meter, [data-meter]')].map(e => e.textContent).join(' ')")
for _ in range(60):
    if '-70.4 mV' in meter():
        break
    time.sleep(0.5)
check('-70.4 mV' in meter(), f'the membrane settles at −70.4 mV, as the step says: {meter()!r}')
p.js("() => { const c = MG.app.circuit; c.toggleSwitch(c.doc.elements.find(e => e.id === 'S1')); }")
for _ in range(60):
    if '46.5 mV' in meter():
        break
    time.sleep(0.5)
check('46.5 mV' in meter() and wait_ticked('io-switch', 5), f'with the Na⁺ switch closed it swings to +46.5 mV, short of E(Na), as the model answer says: {meter()!r}')
p.shot('s2-circuit')
# the Neuron simulation
click('#s2-ions button[data-sim="neuron"]')
p.wait("() => { const S = MG.app.sims; try { return !!(S && S.cur && S.cur.id === 'neuron' && S._screensOf(S.cur.sim)[0]); } catch (e) { return false; } }", timeout=60000)
time.sleep(3)
NM = "(() => { const S = MG.app.sims; const s = S._screensOf(S.cur.sim)[0]; return (s.model || s._model).model; })()"
p.js(f"() => {NM}.initiateStimulusPulse()")
check(wait_ticked('io-sim', 10), 'stimulating the neuron ticks io-sim')
p.js(f"() => {{ {NM}.potentialChartVisibleProperty.value = true; }}")
check(wait_ticked('io-chart', 10), 'showing the potential chart ticks io-chart')
lock = p.js(f"() => {NM}.stimulusLockoutProperty.value")
check(lock is True, 'just after a stimulus the simulation won’t take another (its refractory period), as the step says')
check(mcq_right('io-q-lock'), 'io-q-lock: the sodium channels are inactivated')
p.shot('s2-neuron')
no_errors('the optional exercise on potentials')

# ====================================================================== 2 (optional) Where does nicotine act?
chapter('s2-ans')
check(p.js("() => MG.app.currentBench") == 'bath', 'the chapter opens the Organ bath')


def bath(cmd, wait=0.8):
    click(f'#s2-ans button[data-bath-do="{cmd}"]')
    time.sleep(wait)


click('#s2-ans button[data-bath="ileum?seed=3"]')
check(wait_ticked('an-setup', 20), 'a fresh ileum is set up (an-setup)')
bath('speed 20')
for cmd in ('add acetylcholine 1e-7', 'plateau', 'wash'):
    bath(cmd, 2.5 if cmd == 'plateau' else 0.8)
check(wait_ticked('an-ach', 10), 'the response to acetylcholine ticks an-ach')
for cmd in ('add nicotine 1e-5', 'plateau', 'wash'):
    bath(cmd, 2.5 if cmd == 'plateau' else 0.8)
check(wait_ticked('an-nic', 10), 'the response to nicotine ticks an-nic')
check(mcq_right('an-q-nic'), 'an-q-nic: nicotine acts on the ganglia')
bath('antagonist hexamethonium 1e-4')
bath('wait 600', 3)
check(wait_ticked('an-hexa', 10), 'ten minutes in hexamethonium ticks an-hexa')
for cmd in ('add nicotine 1e-5', 'plateau', 'wash', 'add acetylcholine 1e-7', 'plateau', 'wash'):
    bath(cmd, 2.5 if cmd == 'plateau' else 0.8)
check(wait_ticked('an-nic2', 10) and wait_ticked('an-ach2', 10), 'the responses in hexamethonium tick an-nic2 and an-ach2')
rs = {(r['drug'], 'hex' if 'hexamethonium' in r['condition'] else 'control'): r['pct'] for r in evs('bath:response')}
check(85 < rs.get(('nicotine', 'control'), 0) <= 100 and 5 < rs.get(('nicotine', 'hex'), 100) < 20 and rs.get(('acetylcholine', 'hex'), 0) > 90,
      f'hexamethonium all but abolishes the response to nicotine and leaves acetylcholine’s, as the model answer says: {rs}')
p.shot('s2-bath')
no_errors('the optional exercise in the organ bath')

# ====================================================================== 3 The practical question
chapter('s2-thyroid')
check(p.js("() => MG.app.currentBench") == 'scope', 'the chapter opens the Microscope')
qtext = p.js("() => document.querySelector('#s2-thyroid .handin-box').innerText")
check('label a thyroid follicle, its lumen and a thyroid follicular cell' in qtext and 'no more than 200 words' in qtext, 'the chapter starts with the question itself')
click('#s2-thyroid button[data-scope="thyroid-gland@1.8,1.6,2x"]')
p.wait("() => MG.app.scope && MG.app.scope.current() === 'thyroid-gland'", timeout=30000)
check(wait_ticked('th-open', 5), 'the thyroid slide opens at low power (th-open)')
check(not ticked('th-find'), '(2× isn’t the magnification for a follicle: th-find waits)')
click('#s2-thyroid button[data-scope="thyroid-gland@2.05,0.83,20x"]')
time.sleep(4)
check(wait_ticked('th-find', 5) and p.js("() => Math.round(MG.app.scope.mag())") == 20, 'show me one goes to a follicle at 20× (th-find)')
r = p.js("() => { const b = document.querySelector('.ms-view').getBoundingClientRect(); return [b.x, b.y, b.width, b.height]; }")
x0, y0 = r[0], r[1]
check(r[2] > 500 and r[3] > 700, f'(the view beside the instructions: {r[2]:.0f} × {r[3]:.0f})')


def label(x, y, text):
    click('#s2-thyroid button[data-scope-tool="label"]')
    time.sleep(0.3)
    P.mouse.click(x0 + x, y0 + y)
    p.wait("() => document.querySelector('.modal input')", timeout=5000)
    P.fill('.modal input', text)
    P.keyboard.press('Enter')
    time.sleep(0.4)


label(420, 200, 'Thyroid follicle')
check(wait_ticked('th-lab-f', 5) and not ticked('th-lab-c'), 'labelling the follicle ticks th-lab-f (and not the cell’s step)')
label(298, 300, 'Lumen (colloid)')
check(wait_ticked('th-lab-l', 5), 'labelling the lumen ticks th-lab-l')
label(200, 470, 'Follicular cell')
check(wait_ticked('th-lab-c', 5), 'labelling a follicular cell ticks th-lab-c')
click('#s2-thyroid button[data-scope-tool="area:lumen"]')
time.sleep(0.3)
pts = [(250, 222), (300, 212), (350, 225), (385, 262), (402, 320), (408, 385), (405, 450), (392, 505), (360, 535), (320, 545), (285, 535),
       (255, 505), (230, 465), (205, 415), (190, 360), (192, 300), (210, 255), (230, 232)]
for (x, y) in pts:
    P.mouse.click(x0 + x, y0 + y)
    time.sleep(0.12)
P.mouse.click(x0 + pts[0][0], y0 + pts[0][1])
time.sleep(0.6)
ms = p.js("() => MG.app.scope.st.measures.filter(m => m.slide === 'thyroid-gland').map(m => [m.kind, m.label, m.value, m.unit])")
check(len(ms) == 1 and ms[0][:2] == ['area', 'lumen'] and 10000 < ms[0][2] < 18000 and ms[0][3] == 'µm²' and wait_ticked('th-area', 5),
      f'the lumen of the follicle, traced to the cells, is about 13,000 to 14,000 µm², as the model answer says (th-area): {ms}')
AREA = ms[0][2]
click('#s2-thyroid button[data-scope-tool="capture"]')
check(wait_ticked('th-photo', 15), 'taking the photograph ticks th-photo')
PHOTO = evs('scope:capture')[-1]['path']
check(PHOTO == '/home/user/microscope/pictures/thyroid-gland-20x-1.png', f'the photograph is saved in the microscope’s pictures: {PHOTO}')
p.shot('s2-thyroid-photo')
# R
out = run_button('s2-thyroid', 'm <- read.csv("~/microscope/measurements.csv")')
check(out is not None and wait_ticked('th-read', 5), 'reading the measurements ticks th-read')
run_button('s2-thyroid', 'lumen <- subset(m, slide == "thyroid-gland" & kind == "area")')
out = run_button('s2-thyroid', 'lumen[, c("label", "value", "unit", "objective")]', r'um2')
check(out and 'lumen' in out and f'{AREA}' in out and '20x' in out and wait_ticked('th-sub', 5), f'R shows the lumen’s area, in µm², at 20× (th-sub): {(out or "").strip()[-80:]!r}')
run_button('s2-thyroid', 'area <- tail(lumen$value, 1)')
out = run_button('s2-thyroid', 'area / 1e6', r'\[1\]')
mm2 = float(re.findall(r'\[1\] ([\d.e-]+)', out)[-1])
out = run_button('s2-thyroid', '2 * sqrt(area / pi)', r'\[1\]')
diam = float(re.findall(r'\[1\] ([\d.e-]+)', out)[-1])
check(abs(mm2 - AREA / 1e6) < 1e-6 and 120 < diam < 150 and wait_ticked('th-last', 5),
      f'and works it out in mm² ({mm2}) and as the diameter of a circle of the same area ({diam:.0f} µm), as the model answer says (th-last)')
P.locator('.q[data-q="th-q-area"] textarea').fill(f'About {AREA:,.0f} µm², or {mm2:.3f} mm².')
time.sleep(0.6)
check(answered('th-q-area'), 'th-q-area is answered')
no_errors('the microscope and R')

# ---------------------------------------------------------------- the paper: part (a), with the photograph
click('#s2-thyroid button[data-exam="s2-work"]')
p.wait("() => document.querySelector('.ex-startcard h2') && document.querySelector('.ex-startcard h2').textContent === 'Supervision 2 work'", timeout=30000)
sc = p.js("() => document.querySelector('.ex-startcard').innerText")
check('SUPERVISION 2 · TO HAND IN' in sc.upper() and 'No time limit' in sc and 'chapter 3' in sc and 'To hand in' in sc and 'Tim Hearn’s Google Drive' in sc,
      f'its first page: to hand in, no time limit, the steps in chapter 3 first, and where it goes: {sc[:200]!r}')
click('.ex-startacts .btn.primary')
p.wait("() => document.querySelector('.ex-area')", timeout=30000)
check(wait_ticked('th-paper', 5), 'starting the paper ticks th-paper')
res = p.js("() => [...document.querySelectorAll('.ex-resbtn')].map(b => b.textContent.trim())")
check('Thyroid gland' in res and 'Calculator' in res, f'the slide and the calculator are among the resources at the top: {res}')
qt = p.js("() => document.querySelector('.ex-q') ? document.querySelector('.ex-q').innerText : ''")
check('(a)' in qt and 'Insert picture' in qt, f'question 1 is part (a): {qt[:80]!r}')
# Insert picture: the workbench's pictures first, the newest at the top, and the computer's chooser on offer
click('.ex-tb [data-cmd="picture"]')
p.wait("() => document.querySelector('.modal .ex-picgrid')", timeout=5000)
items = p.js("() => [...document.querySelectorAll('.modal .ex-picitem')].map(b => b.getAttribute('aria-label'))")
check(items and items[0] == 'thyroid-gland-20x-1.png, in ~/microscope/pictures', f'Insert picture offers the photograph from the workbench’s files: {items}')
p.wait("() => { const i = document.querySelector('.modal .ex-picitem img'); return i && i.complete && i.naturalWidth > 0; }", timeout=5000)
check(p.js("() => !!document.querySelector('.modal button.btn')") and 'From your computer' in p.js("() => document.querySelector('.modal').innerText"),
      'with a thumbnail, and a button for a picture from the computer')
p.shot('s2-insert-picture')
with P.expect_file_chooser() as fc:
    click('.modal button:has-text("From your computer")')
fc.value.set_files([])
time.sleep(0.3)
check(not p.js("() => !!document.querySelector('.modal')"), 'From your computer… closes the list and opens the computer’s chooser')
click('.ex-tb [data-cmd="picture"]')
p.wait("() => document.querySelector('.modal .ex-picitem')", timeout=5000)
click('.modal .ex-picitem')
p.wait("() => document.querySelectorAll('.ex-area img.ex-image').length === 1", timeout=20000)
check(wait_ticked('th-pic', 5) and len(evs('exam:picture', f"d.paper === '{PAPER}' && d.q === 'thyroid-a' && d.source === 'files' && d.n === 1")) == 1,
      'choosing it puts it in the answer, and ticks th-pic (exam:picture, from the files)')
im = p.js("() => { const i = document.querySelector('.ex-area img.ex-image'); return [i.naturalWidth, i.naturalHeight, i.alt]; }")
check(im[0] > 400 and im[1] > 500, f'the photograph is the microscope’s, at its own size: {im}')
CAP = f'Figure 1. A thyroid follicle at 20×. The lumen has an area of {AREA:,.0f} µm² ({mm2:.3f} mm²). I chose 20× because the whole follicle fits in the view and the follicular cells can still be told apart.'
P.keyboard.type(CAP)
time.sleep(0.8)
# part (b): no more than 200 words
click('.ex-fab.next')
p.wait("() => document.querySelector('.ex-q') && /\\(b\\)/.test(document.querySelector('.ex-q').innerText)", timeout=5000)
B = ('The follicular cells take up iodide from the blood through a sodium iodide symporter, and make thyroglobulin, which they secrete into the lumen. '
     'At the apical surface thyroid peroxidase iodinates its tyrosines, and couples them to make T4 and T3, which are stored in the colloid of the lumen. ')
p.js("(t) => { const A = document.querySelector('.ex-area'); A.focus(); document.execCommand('insertText', false, t); }", (B * 3).strip())
time.sleep(1.6)
wc = p.js("() => document.querySelector('.ex-wc').textContent")
check(re.fullmatch(r'Words: \d+/200', wc) and not p.js("() => document.querySelector('.ex-wc').classList.contains('over')") and wait_ticked('th-b', 5),
      f'part (b) counts its words against the limit of 200, and ticks th-b: {wc}')
no_errors('the practical question')

# ====================================================================== 4 Short-answer questions, and handing in
chapter('s2-saq')
check(p.js("() => document.querySelectorAll('#s2-saq ol.titles li').length") == 2 and 'POSITIVELY' in p.js("() => document.querySelector('#s2-saq ol.titles').innerText"),
      'the two short-answer questions are listed, as set')


def bullets(points):
    """a bulleted list, from the toolbar, a point at a time"""
    click('.ex-tb [data-cmd="ul"]')
    for i, t in enumerate(points):
        P.keyboard.type(t)
        if i < len(points) - 1:
            P.keyboard.press('Enter')
    time.sleep(1.6)


click('.ex-fab.next')
p.wait("() => /POSITIVELY/.test(document.querySelector('.ex-q').innerText)", timeout=5000)
EK = ['K+ is about 140 mM inside the cell and 2 to 5 mM outside.', 'At rest the membrane is permeable mainly to K+, through leak channels.',
      'K+ diffuses out, leaving unpaired negative charges (anions) behind.', 'The inside becomes negative, which pulls K+ back in.',
      'At EK the electrical and chemical forces balance: by the Nernst equation, 58 log(2.25/140) = -104 mV.']
P.locator('.ex-area').click()
bullets(EK)
html = p.js(f"() => {E}.ed.getHTML()")
check(html.count('<li>') == 5 and '<ul>' in html and wait_ticked('sq-ek', 5), f'the first short answer is five bullet points (sq-ek): {html.count("<li>")} points')
click('.ex-fab.next')
p.wait("() => /voltage-gated sodium channel/.test(document.querySelector('.ex-q').innerText)", timeout=5000)
NAV = ['(a) The selectivity filter is a ring of four residues, DEKA, from the P-loops of the four domains.', '(a) It fits a partly hydrated Na+ ion, and passes Na+ about 12 times more than K+.',
       '(b) The S4 segments carry positive charges and act as voltage sensors.', '(b) Depolarization moves them outwards, which opens the gate at the inner end of the pore.',
       '(b) The IFM motif between domains III and IV then blocks the pore: inactivation.']
P.locator('.ex-area').click()
bullets(NAV)
check(wait_ticked('sq-nav', 5), 'the second short answer, in bullet points too, ticks sq-nav')
p.shot('s2-saq-writing')
click('.ex-tile.review')
p.wait("() => document.querySelector('.ex-submit')", timeout=10000)
sub = p.js("() => document.querySelector('.ex-subhead').innerText")
check('You have attempted all questions in this test.' in sub, f'all four parts are answered: {sub[:80]!r}')
click('.ex-submit')
time.sleep(0.2)
mt = p.js("() => document.querySelector('.modal') ? document.querySelector('.modal').innerText : ''")
check('can’t change your answers' in mt and 'Then you hand it in on the next page' in mt, f'Submit asks first: {mt[:160]!r}')
click('.modal button:has-text("Submit now")')
p.wait("() => document.querySelector('.ex-receipt')", timeout=10000)
check(wait_ticked('sq-submit', 5), 'submitting ticks sq-submit')

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
        r = {'ok': True, 'receipt': f"S{d['week']}-Kp3Z{len(posts):02d}", 'file': d['file']['name'], 'folder': f"Supervision {d['week']}",
             'time': time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())}
    replies.append(r)
    route.fulfill(status=200, headers=dict(cors, **{'Content-Type': 'application/json; charset=utf-8'}), body=json.dumps(r))


p.ctx.route('https://script.google.com/**', stand_in)
p.ctx.route('https://script.googleusercontent.com/**', lambda r: r.abort())
lede = p.js(f"() => document.querySelector('{RX} .ex-hi-lede').innerText")
check(lede == 'Your work goes straight from here to Tim Hearn’s Google Drive. Type in the hand-in password you were given, then press Hand it in.',
      f'the receipt hands the work in from here, and calls it work, not an essay: {lede!r}')


def send(pw):
    P.fill(f'{RX} .ex-hi-pw', pw)
    p.js(f"() => {{ document.querySelector('{RX} .ex-hi-msg').textContent = ''; }}")
    click(f'{RX} .ex-hi-go')
    p.wait(f"""() => {{ const g = document.querySelector('{RX} .ex-hi-go'), m = document.querySelector('{RX} .ex-hi-msg');
        return !g || (!g.disabled && m && m.textContent && !/^Sending/.test(m.textContent)); }}""", timeout=20000)
    return p.js(f"() => document.querySelector('{RX} .ex-hi-msg') ? document.querySelector('{RX} .ex-hi-msg').textContent : ''")


msg = send('a wrong password')
check(msg == 'That isn’t the right hand-in password. Check it with Tim Hearn and try again.' and not ticked('sq-send'), f'a wrong password is refused: {msg!r}')
send(TEST_PW)
p.wait(f"() => document.querySelector('{RX}.handed')", timeout=20000)
d, R = posts[-1], replies[-1]
check(R.get('ok') and d.get('paper') == PAPER and d.get('week') == 2 and d.get('title') == 'Supervision 2 work' and d.get('name') == NAME and d.get('words', 0) > 150,
      f'the right password hands in the paper, week 2, with the student’s name: { {k: v for k, v in d.items() if k not in ("file", "password")} }')
raw = base64.b64decode((d.get('file') or {}).get('data') or '')
check((d.get('file') or {}).get('name') == FILE and raw[:2] == b'PK', f'as a Word document named after the paper and the student: {(d.get("file") or {}).get("name")}')
z = zipfile.ZipFile(io.BytesIO(raw))
xml = z.read('word/document.xml').decode('utf-8')
doc = essay_text(raw)
media = [n for n in z.namelist() if n.startswith('word/media/image')]
check(NAME in doc and 'thyroid follicular cell' in doc and 'POSITIVELY charged potassium ions' in doc and 'voltage-gated sodium channel' in doc,
      'the Word document has the student’s name and all four questions')
check(len(media) == 1 and f'{AREA:,.0f} µm²' in doc and 'Figure 1. A thyroid follicle at 20×' in doc, f'and the labelled photograph, with its caption and the area: {media}')
check(xml.count('<w:numPr>') >= 10 and 'DEKA' in doc and 'pulls K+ back in' in doc, f'and the short answers as bullet points ({xml.count("<w:numPr>")} list paragraphs)')
check(wait_ticked('sq-send', 5) and 'in the folder Supervision 2' in p.js(f"() => document.querySelector('{RX}').innerText"),
      'it arrives in the folder for Supervision 2, and sq-send ticks')
with P.expect_download() as dl:
    click(f'{RX} button:has-text("Download your copy")')
check(dl.value.suggested_filename == FILE and wait_ticked('sq-word', 5), 'Download your copy downloads the Word document, and ticks sq-word')
dl.value.save_as(os.path.join(OUT, 's2-work.docx'))
p.shot('s2-receipt')
# the guidance, after submitting
click('.ex-receipt button:has-text("Review my answers")')
p.wait("() => document.querySelector('.ex-review')", timeout=10000)
rv = p.js("() => document.querySelector('.ex-review').innerText")
check(all(k in rv for k in ('13,000 µm²', 'symporter (NIS)', 'Nernst equation', 'DEKA', 'IFM')), 'Review my answers shows the guidance for all four parts')
P.locator('.q[data-q="th-q-area"]').count()
no_errors('the paper and handing it in')

# ====================================================================== 5 More practice
chapter('s2-more')
check(p.js("() => document.querySelectorAll('#s2-more ol.titles li').length") == 3, 'the three revision titles are listed')
click('#s2-more button[data-exam="s2-revision"]')
p.wait("() => document.querySelector('.ex-startcard h2') && document.querySelector('.ex-startcard h2').textContent === 'Essay titles for revision'", timeout=10000)
sc = p.js("() => document.querySelector('.ex-startcard').innerText")
check('supervision 2 · optional' in sc.lower() and 'Only the practical question and the two short-answer questions need to be handed in' in sc, f'the revision titles are optional: {sc[:120]!r}')
no_errors('more practice')

# ====================================================================== progress, and the landing page afterwards
undone = p.js("""() => { const s = MG.tutorial.state; const t = [...document.querySelectorAll('[data-task]')].filter(li => !li.closest('.optional') && !s.tasks[li.dataset.task]).map(li => li.dataset.task);
    const q = [...document.querySelectorAll('.q[data-q]')].filter(x => !x.closest('.optional') && !(s.answers[x.dataset.q] || {}).done).map(x => x.dataset.q); return t.concat(q); }""")
check(undone == [], f'everything that counts is done: {undone}')
prog = p.js("() => document.querySelector('.progress-label').textContent")
check(prog.startswith('100%'), f'the page says it is finished: {prog}')
p.open('index.html')
tile = p.js("() => document.querySelector('.tile[data-sup=\"2\"]').innerText")
check('20 of 20' in tile or 'All the exercises done' in tile, f'tile 2 shows the work done: {tile[-200:]!r}')
check('✓ Practical and short answers handed in' in tile, f'and that it has been handed in: {tile[-120:]!r}')
p.shot('s2-landing-after')
no_errors('the landing page afterwards')
p.close()

# ====================================================================== a phone
ph = Page(width=390, height=844, mobile=True)
ph.open('supervision-2.html')
time.sleep(1.5)
w = ph.js("() => [document.documentElement.scrollWidth, window.innerWidth]")
check(w[0] <= w[1], f'Supervision 2 fits a phone: {w}')
for cid in ('s2-week', 's2-thyroid', 's2-saq'):
    ph.js(f"() => MG.app.showChapter('{cid}', true)")
    time.sleep(0.6)
    over = ph.js(f"() => [...document.querySelectorAll('#{cid} .handin-box, #{cid} .activity, #{cid} .callout')].filter(e => e.scrollWidth > e.clientWidth + 1).length")
    check(over == 0, f'{cid} fits the phone’s width ({over} overflow)')
ph.shot('s2-phone')
ph.close()
done()
