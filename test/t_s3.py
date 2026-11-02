"""Supervision 3 (supervision-3.html), as a student would use it: tile 3 on the landing page, the week's papers first in
Supervision work, the two optional exercises, whose steps don't count towards finishing the page (skeletal muscle in the
Microscope: a label on the perimysium and on a nucleus, three fibres measured at the place the button opens, and the
time Ca2+ would take to diffuse across them, worked out in R; smooth and cardiac muscle; Hill's force–velocity curve and
power in R; the biceps found in Anatomy, the others faded, and the arm as a lever in R; the soleus, the gastrocnemius
and myoglobin), and the work to hand in: the essay, written, submitted and handed in (through a stand-in for the
hand-in script, so that nothing is handed in), with the Word document checked; the guidance after submitting; the
short-answer questions, whose guidance draws the force–velocity graph; the revision titles; the landing page's progress
and status afterwards; a phone.
Run:  python3 test/t_s3.py   (screenshots in test/out/s3-*.png; R is downloaded from the internet)"""
import base64
import io
import json
import os
import re
import time
import zipfile

from h import Page, check, done, OUT

E = 'MG.app.exam'
A = 'MG.app.anatomy'
NAME = 'Ada Lovelace'
PAPER = 's3-essay'
FILE = 'supervision-3-essay-ada-lovelace.docx'
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


def listen():
    p.js("() => { window.__s3ev = []; MG.bus.on('*', (d, t) => { try { window.__s3ev.push([t, JSON.parse(JSON.stringify(d || {}, (k, v) => k === 'st' ? undefined : v))]); } catch (e) {} }); }")


def evs(kind, cond='true'):
    return p.js(f"() => (window.__s3ev || []).filter(e => e[0] === '{kind}' && (d => {cond})(e[1])).map(e => e[1])")


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


def printed(out):
    """the last number R printed after [1]"""
    m = re.findall(r'\[1\] (-?[\d.e+-]+)', out or '')
    return float(m[-1]) if m else None


def essay_text(docx_bytes):
    return re.sub(r'<[^>]+>', '', zipfile.ZipFile(io.BytesIO(docx_bytes)).read('word/document.xml').decode('utf-8'))


# ====================================================================== the landing page: Supervision 3 is ready
p.open('index.html')
p.js("() => { localStorage.clear(); sessionStorage.clear(); }")
p.js("() => new Promise((ok) => { const r = indexedDB.deleteDatabase('bmssup-files'); r.onsuccess = r.onerror = r.onblocked = () => ok(); })")
p.open('index.html')
t3 = p.js("() => { const t = document.querySelector('.tile[data-sup=\"3\"]'); return [t.getAttribute('href'), t.classList.contains('ready'), t.innerText]; }")
check(t3[0] == 'supervision-3.html' and t3[1], f'tile 3 opens Supervision 3’s own page: {t3[:2]}')
check('Muscle and movement' in t3[2] and 'To hand in: an essay on how movements of molecules and cells move whole animals' in t3[2]
      and 'Essay not started yet' in t3[2], f'it names the topic and the essay to hand in, and nothing is started: {t3[2][:300]!r}')
rest = p.js("() => [...document.querySelectorAll('.tile')].slice(3).map(t => t.getAttribute('href') + (t.classList.contains('soon') ? ':soon' : ''))")
check(rest == ['workbench.html:soon'] * 5, f'Supervisions 4 to 8 are still to come: {rest}')
p.js(f"() => MG.user.setFullName('{NAME}')")

# ====================================================================== Supervision 3's page
p.open('supervision-3.html')
listen()
chs = p.js("() => [...document.querySelectorAll('.chapter')].map(c => c.id + ':' + c.dataset.num)")
check(chs == ['s3-week:0', 's3-fibres:1', 's3-move:2', 's3-write:3', 's3-more:4'], f'Supervision 3 has its five chapters: {chs}')
check(p.js("() => document.body.dataset.week") == '3', 'the page knows it is week 3')
check(p.js("() => MG.app.currentBench") == 'exam', 'the page opens on Supervision work')
p.wait("() => document.querySelectorAll('.ex-card').length >= 8", timeout=30000)
cards = p.js("() => [...document.querySelectorAll('.ex-card')].filter(c => !c.closest('details')).map(c => c.dataset.paper + ':' + (c.querySelector('.ex-badge') ? c.querySelector('.ex-badge').textContent : ''))")
check(cards[:3] == ['s3-essay:To hand in', 's3-saqs:Optional', 's3-revision:Optional'], f'this week’s papers come first, the essay to hand in at the top: {cards[:3]}')
others = p.js("() => [...document.querySelectorAll('details.ex-others .ex-card')].map(c => c.dataset.paper)")
check(others == ['s1-essay', 's1-saqs', 's1-revision', 's2-work', 's2-revision'], f'the earlier weeks’ papers are kept apart: {others}')
meta = p.js("() => document.querySelector('.ex-card[data-paper=\"s3-essay\"] .ex-cmeta').textContent")
check('No time limit (about 40 minutes suggested)' in meta, f'the essay has no time limit, and suggests 40 minutes: {meta}')
box = p.js("() => document.querySelector('#s3-week .handin-box').innerText")
check('How are movements on the cellular and molecular scale used to produce movement of whole animals?' in box
      and 'hand-in password I give you, and your essay then goes straight into my Google Drive' in box,
      f'This week shows the essay to hand in, and how it is handed in: {box[-170:]!r}')
links = p.js("() => [...document.querySelectorAll('.chapter a[href^=\"supervision-\"]')].map(a => a.getAttribute('href'))")
check(sorted(links) == ['supervision-1.html#s1-marking', 'supervision-2.html#s2-ans'], f'it points back to the marking criteria and to last week’s organ bath: {links}')
check(wait_ticked('w3-name', 5), 'the name given on the landing page ticks w3-name')
counted = p.js("""() => [...document.querySelectorAll('[data-task], .q[data-q]')].filter(x => !x.closest('.optional')).map(x => x.dataset.task || x.dataset.q)""")
check(counted == ['w3-name', 'es3-start', 'es3-write', 'es3-submit', 'es3-send', 'es3-word', 'es3-q-next'],
      f'only the essay counts towards finishing the page, not the optional chapters: {counted}')
p.shot('s3-week')
no_errors('opening Supervision 3')

# ====================================================================== 1 (optional) Muscle fibres
chapter('s3-fibres')
check(p.js("() => MG.app.currentBench") == 'scope', 'the chapter opens the Microscope (not RStudio, which would start downloading R)')
check(p.js("() => !!document.querySelector('#s3-fibres .optional.whole')") and 'Optional, about 15 minutes' in p.js("() => document.querySelector('#s3-fibres').innerText"),
      'it says that it is optional')
click('#s3-fibres button[data-scope="skeletal-muscle@1.6,1.6,2x"]')
p.wait("() => MG.app.scope && MG.app.scope.current() === 'skeletal-muscle'", timeout=30000)
check(wait_ticked('fb-open', 5), 'the skeletal muscle opens at low power (fb-open)')
time.sleep(3)
r = p.js("() => { const b = document.querySelector('.ms-view').getBoundingClientRect(); return [b.x, b.y, b.width, b.height]; }")
x0, y0 = r[0], r[1]
check(r[2] > 500 and r[3] > 700, f'(the view beside the instructions: {r[2]:.0f} × {r[3]:.0f})')


def label(x, y, text):
    click('#s3-fibres button[data-scope-tool="label"]')
    time.sleep(0.3)
    P.mouse.click(x0 + x, y0 + y)
    p.wait("() => document.querySelector('.modal input')", timeout=5000)
    P.fill('.modal input', text)
    P.keyboard.press('Enter')
    time.sleep(0.4)


label(300, 300, 'Perimysium')
check(wait_ticked('fb-peri', 5) and not ticked('fb-nuc'), 'labelling the perimysium ticks fb-peri (and not the nucleus’s step)')
check(not ticked('fb-across'), '(2× isn’t the magnification for the fibres: fb-across waits)')
click('#s3-fibres button[data-scope="skeletal-muscle@0.642,3.113,10x"]')
time.sleep(5)
check(wait_ticked('fb-across', 5) and p.js("() => Math.round(MG.app.scope.mag())") == 10, 'show me goes to fibres cut across, at 10× (fb-across)')
label(150, 130, 'Nucleus')
check(wait_ticked('fb-nuc', 5), 'labelling a nucleus ticks fb-nuc')
# the three fibres' narrowest widths, at the place the button opens (found by measuring the slide's own image: each line
# crosses one fibre at its narrowest, from edge to edge)
LINES = [((103, 120), (150, 159)), ((383, 366), (420, 418)), ((236, 301), (289, 355))]
click('#s3-fibres button[data-scope-tool="measure:fibre width"]')
time.sleep(0.3)
for (ax, ay), (bx, by) in LINES:
    P.mouse.move(x0 + ax, y0 + ay)
    P.mouse.down()
    for s in range(1, 11):
        P.mouse.move(x0 + ax + (bx - ax) * s / 10, y0 + ay + (by - ay) * s / 10, steps=1)
    P.mouse.up()
    time.sleep(0.4)
ms = p.js("() => MG.app.scope.st.measures.filter(m => m.slide === 'skeletal-muscle').map(m => [m.kind, m.label, m.value, m.unit])")
widths = [m[2] for m in ms]
check(len(ms) == 3 and all(m[:2] == ['length', 'fibre width'] and m[3] == 'µm' for m in ms) and all(55 < w < 85 for w in widths),
      f'three fibres, measured at their narrowest, are 60 to 80 µm across, as the model answer says: {widths}')
check(wait_ticked('fb-width', 5), 'the third measurement ticks fb-width')
p.shot('s3-fibres-measured')
check(mcq_right('fb-q-band'), 'fb-q-band: the A band stays the same length')
# R
p.js("() => [...document.querySelectorAll('#s3-fibres button[data-rcon]')][0].click()")
for _ in range(400):
    if r_idle() == 'idle':
        break
    time.sleep(0.5)
check(r_idle() == 'idle', f'R starts in RStudio ({r_idle()})')
out = run_button('s3-fibres', 'm <- read.csv("~/microscope/measurements.csv")')
check(out is not None and wait_ticked('fb-read', 5), 'reading the measurements ticks fb-read')
run_button('s3-fibres', 'w <- subset(m, slide == "skeletal-muscle" & kind == "length")$value')
out = run_button('s3-fibres', 'mean(w)', r'\[1\]')
mean_w = printed(out)
check(mean_w and abs(mean_w - sum(widths) / 3) < 0.01 and wait_ticked('fb-w', 5), f'R finds the mean width of the three fibres, {mean_w} µm (fb-w)')
run_button('s3-fibres', 'x <- mean(w) / 2')
t = printed(run_button('s3-fibres', 'x^2 / (2 * 800)', r'\[1\]'))
check(t and abs(t - (mean_w / 2) ** 2 / 1600) < 1e-3 and 0.6 < t < 0.8 and wait_ticked('fb-t', 5),
      f'Ca²⁺ would take about 0.7 s to diffuse from the surface to the middle, as the model answer says: {t} s (fb-t)')
t1 = printed(run_button('s3-fibres', '1^2 / (2 * 800)', r'\[1\]'))
check(t1 == 0.000625 and wait_ticked('fb-t1', 5), f'and 0.6 ms over 1 µm: {t1} s (fb-t1)')
# if you have time: smooth and cardiac muscle
click('#s3-fibres button[data-scope="smooth-muscle@2.471,2.273,10x"]')
p.wait("() => MG.app.scope.current() === 'smooth-muscle'", timeout=30000)
check(wait_ticked('fb-smooth', 5), 'the smooth muscle opens (fb-smooth)')
ts = printed(run_button('s3-fibres', '2.5^2 / (2 * 800)', r'\[1\]'))
check(ts == 0.00390625 and wait_ticked('fb-smooth-t', 5), f'Ca²⁺ crosses half a smooth muscle cell in about 4 ms, as the model answer says: {ts} s')
click('#s3-fibres button[data-scope="heart@2.2,1.46,40x"]')
p.wait("() => MG.app.scope.current() === 'heart'", timeout=30000)
check(wait_ticked('fb-heart', 5), 'the heart opens (fb-heart)')
P.locator('.q[data-q="fb-q-tt"] textarea').fill('About 0.7 s from the surface, but only 0.6 ms over 1 µm from the SR: diffusion is far too slow over long distances.')
P.locator('.q[data-q="fb-q-tt"] button:has-text("Show answer")').click()
check('33² / 1600 gives about 0.7 s' in p.js("() => document.querySelector('.q[data-q=\"fb-q-tt\"]').innerText"), 'the model answer can be shown once the question has been tried')
no_errors('the optional exercise on muscle fibres')

# ====================================================================== 2 (optional) From muscle to movement
chapter('s3-move')
check(p.js("() => MG.app.currentBench") == 'rstudio', 'the chapter opens RStudio')
check(p.js("() => !!document.querySelector('#s3-move .optional.whole')"), 'it is optional')
run_button('s3-move', 'hill <- function(f) 0.25 * (1 - f) / (f + 0.25)')
run_button('s3-move', 'f <- seq(0, 1, by = 0.01)')
run_button('s3-move', 'v <- hill(f)')
check(wait_ticked('mo-hill', 5), 'Hill’s equation, made into a function, ticks mo-hill')
plots = len(evs('rstudio:plot'))
run_button('s3-move', 'plot(f, v, type = "l", xlab = "Force (fraction of the isometric force)", ylab = "Velocity (fraction of the maximum)")')
p.wait(f"() => (window.__s3ev || []).filter(e => e[0] === 'rstudio:plot').length > {plots}", timeout=30000)
check(wait_ticked('mo-plotv', 5), 'the force–velocity curve is plotted (mo-plotv)')
p.shot('s3-force-velocity')
run_button('s3-move', 'p <- f * v')
run_button('s3-move', 'plot(f, p, type = "l", xlab = "Force (fraction of the isometric force)", ylab = "Power")')
check(wait_ticked('mo-plotp', 5), 'and the power (mo-plotp)')
fmax = printed(run_button('s3-move', 'f[which.max(p)]', r'\[1\]'))
check(fmax == 0.31 and wait_ticked('mo-max', 5), f'the power is greatest at 0.31 of the isometric force, as the model answer says: {fmax}')
ratio = printed(run_button('s3-move', 'hill(0.05) / hill(0.5)', r'\[1\]'))
check(ratio == 4.75 and wait_ticked('mo-ratio', 5), f'50 g takes 4.75 times as long to lift as 5 g, as the model answer says: {ratio}')
check(short('mo-q-max', '0.31') and short('mo-q-50g', '4.75'), 'the two numbers, typed in, are right (mo-q-max, mo-q-50g)')
# the arm as a lever


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


click('#s3-move button[data-anat-find="long-head-of-biceps-brachii"]')
p.wait(f"() => MG.app.currentBench === 'anatomy' && {A} && {A}.index", timeout=60000)
idle()
check(p.js(f"() => !!{A}.on.muscles"), 'finding the biceps shows the muscles')
ok = click_on('long-head-of-biceps-brachii-right') or click_on('long-head-of-biceps-brachii-left')
check(ok and wait_ticked('mo-bic', 5), 'a click on the long head of the biceps ticks mo-bic')
fade = p.js("() => { const b = [...document.querySelectorAll('.an-acts button')].find(x => /Fade the others/.test(x.textContent)); if (!b) return false; b.click(); return true; }")
check(fade and wait_ticked('mo-fade', 5), 'the panel about it has Fade the others, which ticks mo-fade')
time.sleep(1)
p.shot('s3-biceps')
gain = printed(run_button('s3-move', '35 / 4', r'\[1\]'))
force = printed(run_button('s3-move', '5 * 9.81 * 35 / 4', r'\[1\]'))
check(gain == 8.75 and force == 429.1875 and wait_ticked('mo-arm', 5), f'the hand moves 8.75 times as far as the biceps shortens, which pulls with about 430 N, as the model answer says: {gain}, {force}')
# if you have time: the soleus, the gastrocnemius and myoglobin
click('#s3-move button[data-anat-find="soleus-muscle"]')
p.wait(f"() => MG.app.currentBench === 'anatomy' && {A}.findTask", timeout=30000)
idle()
p.js(f"() => {A}.setView('posterior')")
idle()
ok = click_on('soleus-muscle-right') or click_on('soleus-muscle-left')
if not ok:
    # (the soleus lies under the gastrocnemius: Show me brings it into view)
    p.js(f"() => {A}._findShow()")
    idle()
    ok = click_on('soleus-muscle-right') or click_on('soleus-muscle-left')
check(ok and wait_ticked('mo-soleus', 5), 'finding the soleus ticks mo-soleus')
click('#s3-move button[data-anat-find="medial-head-of-gastrocnemius|lateral-head-of-gastrocnemius"]')
idle()
ok = any(click_on(f'{h}-head-of-gastrocnemius-{s}') for h in ('medial', 'lateral') for s in ('right', 'left'))
check(ok and wait_ticked('mo-gastro', 5), 'finding the gastrocnemius ticks mo-gastro')
click('#s3-move button[data-pdb="1MBN"]')
check(wait_ticked('mo-mb', 60), 'myoglobin opens in Molecules (mo-mb)')
no_errors('the optional exercise on movement')

# ====================================================================== 3 Write your essay
chapter('s3-write')
check(p.js("() => MG.app.currentBench") == 'exam', 'the chapter opens Supervision work')
click('#s3-write button[data-exam="s3-essay"]')
p.wait("() => document.querySelector('.ex-startcard h2') && document.querySelector('.ex-startcard h2').textContent === 'Supervision 3 essay'", timeout=30000)
sc = p.js("() => document.querySelector('.ex-startcard').textContent")
check('No time limit, but we suggest about 40 minutes' in sc and 'Supervision 3 · to hand in' in sc and 'Tim Hearn' in sc,
      f'its first page: no time limit, 40 minutes suggested, and how to hand it in: {sc[:240]!r}')
click('.ex-startacts .btn.primary')
p.wait("() => document.querySelector('.ex-area')", timeout=30000)
check(wait_ticked('es3-start', 5), 'starting the essay ticks es3-start')
check(p.js("() => document.querySelector('.ex-timer').textContent") == '0 of about 40 minutes', 'the clock counts up towards the suggested 40 minutes')
PARA = ('A single myosin head moves an actin filament about ten nanometres in each cross-bridge cycle, but thousands of '
        'sarcomeres in series add their shortening, and myofibrils in parallel add their force, so that a whole muscle can '
        'move a limb through tens of centimetres. ')
p.js("(t) => { const A = document.querySelector('.ex-area'); A.focus(); document.execCommand('insertText', false, t); }", (PARA * 8).strip())
time.sleep(1.6)
check(wait_ticked('es3-write', 5), f'writing more than 300 words ticks es3-write ({p.js("() => document.querySelector(\'.ex-wc\').textContent")})')
click('.ex-tile.review')
p.wait("() => document.querySelector('.ex-submit')", timeout=10000)
click('.ex-submit')
time.sleep(0.2)
mt = p.js("() => document.querySelector('.modal') ? document.querySelector('.modal').innerText : ''")
check('Then you hand it in on the next page' in mt, f'Submit asks first, and says it is handed in next: {mt[-120:]!r}')
click('.modal button:has-text("Submit now")')
p.wait("() => document.querySelector('.ex-receipt')", timeout=10000)
check(wait_ticked('es3-submit', 5), 'submitting ticks es3-submit')

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
        r = {'ok': True, 'receipt': f"S{d['week']}-Mv7Q{len(posts):02d}", 'file': d['file']['name'], 'folder': f"Supervision {d['week']}",
             'time': time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())}
    replies.append(r)
    route.fulfill(status=200, headers=dict(cors, **{'Content-Type': 'application/json; charset=utf-8'}), body=json.dumps(r))


p.ctx.route('https://script.google.com/**', stand_in)
p.ctx.route('https://script.googleusercontent.com/**', lambda r: r.abort())
lede = p.js(f"() => document.querySelector('{RX} .ex-hi-lede').innerText")
check(lede == 'Your essay goes straight from here to Tim Hearn’s Google Drive. Type in the hand-in password you were given, then press Hand it in.',
      f'the receipt hands the essay in from here: {lede!r}')


def send(pw):
    P.fill(f'{RX} .ex-hi-pw', pw)
    p.js(f"() => {{ document.querySelector('{RX} .ex-hi-msg').textContent = ''; }}")
    click(f'{RX} .ex-hi-go')
    p.wait(f"""() => {{ const g = document.querySelector('{RX} .ex-hi-go'), m = document.querySelector('{RX} .ex-hi-msg');
        return !g || (!g.disabled && m && m.textContent && !/^Sending/.test(m.textContent)); }}""", timeout=20000)
    return p.js(f"() => document.querySelector('{RX} .ex-hi-msg') ? document.querySelector('{RX} .ex-hi-msg').textContent : ''")


msg = send('a wrong password')
check(msg == 'That isn’t the right hand-in password. Check it with Tim Hearn and try again.' and not ticked('es3-send'), f'a wrong password is refused: {msg!r}')
send(TEST_PW)
p.wait(f"() => document.querySelector('{RX}.handed')", timeout=20000)
d, R = posts[-1], replies[-1]
check(R.get('ok') and d.get('paper') == PAPER and d.get('week') == 3 and d.get('title') == 'Supervision 3 essay' and d.get('name') == NAME and d.get('words', 0) > 300,
      f'the right password hands in the essay, week 3, with the student’s name: { {k: v for k, v in d.items() if k not in ("file", "password")} }')
raw = base64.b64decode((d.get('file') or {}).get('data') or '')
check((d.get('file') or {}).get('name') == FILE and raw[:2] == b'PK', f'as a Word document named after the paper and the student: {(d.get("file") or {}).get("name")}')
doc = essay_text(raw)
check(NAME in doc and 'How are movements on the cellular and molecular scale used to produce movement of whole animals?' in doc and 'ten nanometres' in doc,
      'the Word document has the student’s name, the title and the essay')
check(wait_ticked('es3-send', 5) and 'in the folder Supervision 3' in p.js(f"() => document.querySelector('{RX}').innerText"),
      'it arrives in the folder for Supervision 3, and es3-send ticks')
with P.expect_download() as dl:
    click(f'{RX} button:has-text("Download your copy")')
check(dl.value.suggested_filename == FILE and wait_ticked('es3-word', 5), 'Download your copy downloads the Word document, and ticks es3-word')
dl.value.save_as(os.path.join(OUT, 's3-essay.docx'))
p.shot('s3-receipt')
# the guidance, after submitting
click('.ex-receipt button:has-text("Review my answers")')
p.wait("() => document.querySelector('.ex-review')", timeout=10000)
rv = p.js("() => document.querySelector('.ex-review').innerText")
check(all(k in rv for k in ('sliding filament theory', 'size principle', 'T-tubules matter', 'dynein', 'Against the core criteria')),
      'Review my answers shows the guidance, from the motor to whole animals')
P.locator('.q[data-q="es3-q-next"] textarea').fill('I rushed the levers and the whole animal at the end, and never said how the sarcomeres add up.')
time.sleep(0.6)
check(answered('es3-q-next'), 'es3-q-next is answered')
no_errors('the essay and handing it in')

# ====================================================================== 4 More practice
chapter('s3-more')
saqs = p.js("() => [...document.querySelectorAll('#s3-more ol.titles')[0].querySelectorAll('li')].map(l => l.textContent)")
revs = p.js("() => [...document.querySelectorAll('#s3-more ol.titles')[1].querySelectorAll('li')].map(l => l.textContent)")
check(len(saqs) == 3 and len(revs) == 3, f'the three short-answer questions and the three revision titles are listed: {len(saqs)}, {len(revs)}')
check('Duchenne’s muscular dystrophy' in saqs[1] and revs[1].startswith('Explain how the molecular organisation') and revs[0].endswith('skeletal muscle?'),
      'with the typos of the handouts put right')
click('#s3-more button[data-exam="s3-saqs"]')
p.wait("() => document.querySelector('.ex-startcard h2') && /short-answer/.test(document.querySelector('.ex-startcard h2').textContent)", timeout=10000)
sc = p.js("() => document.querySelector('.ex-startcard').innerText")
check('supervision 3 · optional' in sc.lower() and 'Only the essay needs to be handed in' in sc, f'the short-answer questions are optional: {sc[:120]!r}')
click('.ex-startacts .btn.primary')
p.wait("() => document.querySelector('.ex-area')", timeout=30000)
qt = p.js("() => document.querySelector('.ex-q').innerText")
check('50 g mass' in qt and 'Insert drawing' in qt, f'question 1 asks for the graph, drawn with Insert drawing: {qt[:80]!r}')
click('.ex-tb [data-cmd="ul"]')
for i, t in enumerate(['Velocity falls as the load rises, along a hyperbola (Hill).', 'More cross-bridges must be attached to bear a heavier load.',
                       'At the isometric force, velocity is zero.', 'Power is force times velocity.', 'Power is greatest at about a third of the isometric force.']):
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
check(wait_ticked('m3-saq', 5), 'submitting the short-answer questions ticks m3-saq (optional)')
click('.ex-receipt button:has-text("Review my answers")')
p.wait("() => document.querySelector('.ex-review')", timeout=10000)
svg = p.js("() => { const s = document.querySelector('.ex-review svg'); if (!s) return null; const b = s.getBoundingClientRect(); return {lines: s.querySelectorAll('polyline').length, w: b.width, h: b.height, text: s.textContent}; }")
check(svg and svg['lines'] == 2 and svg['w'] > 200 and svg['h'] > 100 and 'power' in svg['text'],
      f'the guidance for question 1 draws the force–velocity and power curves: {svg}')
rv = p.js("() => document.querySelector('.ex-review').innerText")
check(all(k in rv for k in ('Gowers’ sign', 'dantrolene', 'pyridostigmine', 'latch bridges', 'calmodulin')), 'and covers the diseases and the two kinds of muscle')
p.shot('s3-saq-review')
click('.ex-revbar button:has-text("Back")')
time.sleep(0.5)
p.js(f"() => {E}.home()")
time.sleep(0.5)
click('#s3-more button[data-exam="s3-revision"]')
p.wait("() => document.querySelector('.ex-startcard h2') && document.querySelector('.ex-startcard h2').textContent === 'Essay titles for revision'", timeout=10000)
sc = p.js("() => document.querySelector('.ex-startcard').innerText")
check('supervision 3 · optional' in sc.lower() and 'Only the Supervision 3 essay needs to be handed in' in sc, f'the revision titles are optional: {sc[:120]!r}')
no_errors('more practice')

# ====================================================================== progress, and the landing page afterwards
undone = p.js("""() => { const s = MG.tutorial.state; const t = [...document.querySelectorAll('[data-task]')].filter(li => !li.closest('.optional') && !s.tasks[li.dataset.task]).map(li => li.dataset.task);
    const q = [...document.querySelectorAll('.q[data-q]')].filter(x => !x.closest('.optional') && !(s.answers[x.dataset.q] || {}).done).map(x => x.dataset.q); return t.concat(q); }""")
check(undone == [], f'everything that counts is done: {undone}')
prog = p.js("() => document.querySelector('.progress-label').textContent")
check(prog.startswith('100%'), f'the page says it is finished: {prog}')
p.open('index.html')
tile = p.js("() => document.querySelector('.tile[data-sup=\"3\"]').innerText")
check('7 of 7' in tile or 'All the exercises done' in tile, f'tile 3 shows the work done: {tile[-200:]!r}')
check('✓ Essay handed in' in tile, f'and that the essay has been handed in: {tile[-120:]!r}')
p.shot('s3-landing-after')
no_errors('the landing page afterwards')
p.close()

# ====================================================================== a phone
ph = Page(width=390, height=844, mobile=True)
ph.open('supervision-3.html')
time.sleep(1.5)
w = ph.js("() => [document.documentElement.scrollWidth, window.innerWidth]")
check(w[0] <= w[1], f'Supervision 3 fits a phone: {w}')
for cid in ('s3-week', 's3-fibres', 's3-move', 's3-write'):
    ph.js(f"() => MG.app.showChapter('{cid}', true)")
    time.sleep(0.6)
    over = ph.js(f"() => [...document.querySelectorAll('#{cid} .handin-box, #{cid} .activity, #{cid} .callout')].filter(e => e.scrollWidth > e.clientWidth + 1).length")
    check(over == 0, f'{cid} fits the phone’s width ({over} overflow)')
ph.shot('s3-phone')
ph.close()
done()
