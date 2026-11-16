"""Supervision 5 (supervision-5.html), as a student would use it: tile 5 on the landing page, the week's papers first in
Supervision work, the two optional exercises, whose steps don't count towards finishing the page (in the Recorder, the
R–R interval at the start and the end of ten minutes of cycling, and one beat of blood pressure before and after
standing up, with the mean the calipers measure against the one-third rule; in the Circuits tab, Guyton's model of the
circulation run through rest, exercise and a haemorrhage, with every number the model answers give), and the work to
hand in: the three questions on using equations, the essay written with a formula put in with the Σ tool, submitted
and handed in (through a stand-in for the hand-in script, so that nothing is handed in), with the Word document
checked; the guidance after submitting, with its figure of Guyton's curves; the short-answer questions and the
revision titles; the landing page's progress and status afterwards; a phone.
Run:  python3 test/t_s5.py   (screenshots in test/out/s5-*.png)"""
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
CI = 'MG.app.circuit'
NAME = 'Ada Lovelace'
PAPER = 's5-essay'
FILE = 'supervision-5-essay-ada-lovelace.docx'
ESSAY = ('Describe the cardiovascular responses during sustained exercise. What limits maximal exercise performance '
         'under these conditions?')
TEST_PW = 'the-stand-in-password'   # (the stand-in's: the real password is never in the tests)
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
    p.js("() => { window.__s5ev = []; MG.bus.on('*', (d, t) => { try { window.__s5ev.push([t, JSON.parse(JSON.stringify(d || {}, (k, v) => k === 'st' ? undefined : v))]); } catch (e) {} }); }")


def evs(kind, cond='true'):
    return p.js(f"() => (window.__s5ev || []).filter(e => e[0] === '{kind}' && (d => {cond})(e[1])).map(e => e[1])")


def no_errors(where):
    errs = [e for e in p.errors if 'ResizeObserver' not in e]
    check(not errs, f'no errors in the page ({where}): {errs[:3]}')
    p.errors.clear()


def essay_text(docx_bytes):
    return re.sub(r'<[^>]+>', '', zipfile.ZipFile(io.BytesIO(docx_bytes)).read('word/document.xml').decode('utf-8'))


def rec_open(spec, rid):
    click(f'#s5-rec button[data-rec="{spec}"]')
    p.wait(f"() => {RC} && {RC}.R && {RC}.R.id === '{rid}' && !{RC}._raf", timeout=30000)
    time.sleep(0.4)


def calipers(lane, ta, tb):
    """drags the calipers on a channel of the Recorder from ta to tb (s); the rec:measure it sends, with the minimum,
    maximum and mean that the bar above the traces shows"""
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
    if len(got) <= n:
        return None
    st = p.js(f"() => {{ const m = {RC}.measurement(); return m && m.stats; }}")
    return dict(got[-1], stats=st)


def meters():
    """the latest reading of each meter of the circuit, by its label"""
    last = {}
    for e in evs('circuit:measure'):
        last[e['label']] = e['value']
    return last


def el(i):
    return f"{CI}.doc.elements.find(e => e.id === '{i}')"


def settle(label, test, s=8):
    """waits until a meter's reading passes a test"""
    for _ in range(int(s * 4)):
        v = meters().get(label)
        if v is not None and test(v):
            return v
        time.sleep(0.25)
    return meters().get(label)


# ====================================================================== the landing page: Supervision 5 is ready
p.open('index.html')
p.js("() => { localStorage.clear(); sessionStorage.clear(); }")
p.js("() => new Promise((ok) => { const r = indexedDB.deleteDatabase('bmssup-files'); r.onsuccess = r.onerror = r.onblocked = () => ok(); })")
p.open('index.html')
t5 = p.js("() => { const t = document.querySelector('.tile[data-sup=\"5\"]'); return [t.getAttribute('href'), t.classList.contains('ready'), t.innerText]; }")
check(t5[0] == 'supervision-5.html' and t5[1], f'tile 5 opens Supervision 5’s own page: {t5[:2]}')
check('Cardiac output, blood pressure and exercise' in t5[2] and 'To hand in: an essay on the circulation in sustained exercise, and what limits it' in t5[2]
      and 'Essay not started yet' in t5[2], f'it names the topic and the essay to hand in, and nothing is started: {t5[2][:300]!r}')
rest = p.js("() => [...document.querySelectorAll('.tile')].slice(5).map(t => t.getAttribute('href') + (t.classList.contains('soon') ? ':soon' : ''))")
check(rest == ['workbench.html:soon'] * 3, f'Supervisions 6 to 8 are still to come: {rest}')
p.js(f"() => MG.user.setFullName('{NAME}')")

# ====================================================================== Supervision 5's page
p.open('supervision-5.html')
listen()
chs = p.js("() => [...document.querySelectorAll('.chapter')].map(c => c.id + ':' + c.dataset.num)")
check(chs == ['s5-week:0', 's5-rec:1', 's5-model:2', 's5-write:3', 's5-more:4'], f'Supervision 5 has its five chapters: {chs}')
check(p.js("() => document.body.dataset.week") == '5', 'the page knows it is week 5')
check(p.js("() => MG.app.currentBench") == 'exam', 'the page opens on Supervision work')
p.wait("() => document.querySelectorAll('.ex-card').length >= 14", timeout=30000)
cards = p.js("() => [...document.querySelectorAll('.ex-card')].filter(c => !c.closest('details')).map(c => c.dataset.paper + ':' + (c.querySelector('.ex-badge') ? c.querySelector('.ex-badge').textContent : ''))")
check(cards[:3] == ['s5-essay:To hand in', 's5-saqs:Optional', 's5-revision:Optional'], f'this week’s papers come first, the essay to hand in at the top: {cards[:3]}')
others = p.js("() => [...document.querySelectorAll('details.ex-others .ex-card')].map(c => c.dataset.paper)")
check(others == ['s1-essay', 's1-saqs', 's1-revision', 's2-work', 's2-revision', 's3-essay', 's3-saqs', 's3-revision',
                 's4-essay', 's4-saqs', 's4-revision'], f'the earlier weeks’ papers are kept apart: {others}')
meta = p.js("() => document.querySelector('.ex-card[data-paper=\"s5-essay\"] .ex-cmeta').textContent")
check('No time limit (about 40 minutes suggested)' in meta, f'the essay has no time limit, and suggests 40 minutes: {meta}')
box = p.js("() => document.querySelector('#s5-week .handin-box').innerText")
check(ESSAY in box and 'equations' in box and 'hand-in password I give you, and your essay then goes straight into my Google Drive' in box,
      f'This week shows the essay to hand in, that it needs equations, and how it is handed in: {box[-200:]!r}')
links = p.js("() => [...document.querySelectorAll('.chapter a[href^=\"supervision-\"]')].map(a => a.getAttribute('href'))")
check(links == ['supervision-1.html#s1-marking'], f'it points back to the marking criteria: {links}')
check(wait_ticked('w5-name', 5), 'the name given on the landing page ticks w5-name')
counted = p.js("""() => [...document.querySelectorAll('[data-task], .q[data-q]')].filter(x => !x.closest('.optional')).map(x => x.dataset.task || x.dataset.q)""")
check(counted == ['w5-name', 'es5-q-hr', 'es5-q-veno', 'es5-q-pump', 'es5-start', 'es5-write', 'es5-submit', 'es5-send', 'es5-word', 'es5-q-next'],
      f'only the essay and its questions on equations count towards finishing the page, not the optional chapters: {counted}')
p.shot('s5-week')
no_errors('opening Supervision 5')

# ====================================================================== 1 (optional) Exercise and standing up
chapter('s5-rec')
check(p.js("() => MG.app.currentBench") == 'recorder', 'the chapter opens the Recorder')
check(p.js("() => !!document.querySelector('#s5-rec .optional.whole')") and 'Optional, about 15 minutes' in p.js("() => document.querySelector('#s5-rec').innerText"),
      'it says that it is optional')
rec_open('exercise@10,16', 'exercise')
check(wait_ticked('ex-open', 5) and p.js(f"() => {RC}._lanes().map(L => L.short)") == ['ECG', 'HR'], 'the cycling opens, with its heart rate (ex-open)')
click('#s5-rec button[data-rec-tool="calipers"]')
time.sleep(0.3)
beats = p.js(f"() => {RC}.R.beats.t")
b = [t for t in beats if 11 < t < 15][:2]
m = calipers('ECG', b[0], b[1])
check(m and m['interval'] == 'R-R' and wait_ticked('ex-start', 5), f'an R–R interval near the start is recognised: {m and (m["interval"], m["dt"], m["rate"])} (ex-start)')
check(m and abs(m['dt'] - 0.71) < 0.02 and 80 < m['rate'] < 88, f'about 0.71 s, about 84 a minute, as the model answer says: {m and (m["dt"], m["rate"])}')
rec_open('exercise@575,581', 'exercise')
click('#s5-rec button[data-rec-tool="calipers"]')
time.sleep(0.3)
b = [t for t in beats if 576 < t < 580][:2]
m = calipers('ECG', b[0], b[1])
check(m and m['interval'] == 'R-R' and wait_ticked('ex-end', 5) and abs(m['dt'] - 0.46) < 0.015 and 126 < m['rate'] < 134,
      f'and one near the end, about 0.46 s, about 130 a minute: {m and (m["dt"], m["rate"])} (ex-end)')
txt = model('ex-q-rate', 'The rate rose; in exercise venous return rises too, so the extra beats have blood to pump.')
check('about 84 beats a minute' in txt and 'about 130' in txt, 'the model answer gives the two rates that were measured')
p.shot('s5-cycling')
rec_open('bp-standing@25,75', 'bp-standing')
check(wait_ticked('st-open', 5) and p.js(f"() => {RC}._lanes().map(L => L.short)") == ['BP', 'ECG', 'HR'], 'standing up opens, with blood pressure, ECG and heart rate (st-open)')
stand = p.js(f"() => {RC}.R.events.filter(e => /Stands up/.test(e.text || e.label || '')).map(e => e.t)")
check(stand and abs(stand[0] - 41.06) < 0.05, f'(a flag marks the moment he stands up: {stand})')
click('#s5-rec button[data-rec-tool="calipers"]')
time.sleep(0.3)
m = calipers('BP', 32.85, 33.64)
st = m and m['stats']
check(m and m['signal'] == 'bp' and wait_ticked('st-before', 5), f'one beat of the blood pressure before he stands is measured (st-before): {m and (m["from"], m["to"])}')
check(st and abs(st['max'] - 97) < 2 and abs(st['min'] - 53) < 2 and abs(st['mean'] - 65) < 1.5,
      f'about 97/53 mmHg with a mean of about 65, as the model answer says: {st}')
est = st['min'] + (st['max'] - st['min']) / 3
check(abs(est - 68) < 1.5 and 2 < est - st['mean'] < 4, f'the one-third rule gives about 68 mmHg, about 3 mmHg above the measured mean: {est:.1f}')
m = calipers('BP', 45.38, 45.99)
st = m and m['stats']
check(m and wait_ticked('st-low', 5) and st and abs(st['max'] - 84) < 2 and abs(st['min'] - 38) < 2 and abs(st['mean'] - 51) < 1.5,
      f'and one at the lowest pressure, about 84/38 with a mean of about 51 (st-low): {st}')
hr = p.js(f"() => {RC}.R.hr.map(x => [x.t, x.v])")
before = [v for t, v in hr if 30 < t < 40]
after = [v for t, v in hr if 41 < t < 56]
check(abs(sum(before) / len(before) - 77) < 3 and abs(max(after) - 105) < 4,
      f'his heart rate rises from about 77 to about 105 a minute, as the model answer says: {sum(before) / len(before):.1f}, {max(after):.1f}')
txt = model('st-q-map', 'About 53 + 44/3 = 68, a little above the measured mean of 65.')
check('97/53 mmHg' in txt and 'MAP ≈ 53 + 44/3 ≈ 68 mmHg' in txt and 'a mean of about 65 mmHg' in txt, 'the model answer works the estimate through')
txt = model('st-q-baro', 'CO fell as blood pooled in the legs; the baroreflex raised the heart rate and TPR.')
check('from about 65 to about 51 mmHg' in txt and 'from about 77 to about 105' in txt, 'the model answer gives the fall in pressure and the rise in heart rate')
p.shot('s5-standing')
no_errors('the optional exercise in the Recorder')

# ====================================================================== 2 (optional) Exercise in a model of the circulation
chapter('s5-model')
check(p.js("() => MG.app.currentBench") == 'circuit', 'the chapter opens the Circuits tab')
check(p.js("() => !!document.querySelector('#s5-model .optional.whole')"), 'it is optional')
idx = json.load(open(os.path.join(SITE, 'examples', 'index.json'), encoding='utf-8'))
ex = [c for c in idx['circuits'] if c['id'] == 'exercise-circulation']
check(ex and ex[0]['group'] == 'Physiology', 'the model is among the Circuits tab’s examples, with the physiology ones')
click('#s5-model button[data-circuit="example:exercise-circulation"]')
p.wait(f"() => {CI} && {CI}.doc && /Guyton/.test({CI}.doc.title)", timeout=30000)
check(p.js(f"() => {CI}.doc.mode") == 'physiology', 'it opens in physiology mode')
click('#s5-model button[data-circuit-run]')
check(wait_ticked('md-open', 10), 'running it ticks md-open')
abp = settle('ABP', lambda v: abs(v - 93) < 0.5)
mt = meters()
check(abs(mt.get('Venous return', 0) - 83.3) < 0.1 and abs(mt.get('Cardiac output', 0) - 83.3) < 0.1 and abs(mt.get('RAP', 9)) < 0.1
      and abs(abp - 93) < 0.5 and abs(mt.get('MSFP', 0) - 7) < 0.01,
      f'at rest, venous return = cardiac output = 83.3 mL/s, RAP 0 and ABP 93 mmHg, as the step says: {mt}')
p.js(f"() => {CI}.toggleSwitch({el('S2')})")
check(wait_ticked('md-muscle', 5), 'closing Exercising muscles ticks md-muscle')
abp = settle('ABP', lambda v: v < 25)
check(abs(abp - 18.6) < 0.2, f'ABP falls to a fifth, about 19 mmHg, as the model answer says: {abp}')
p.js(f"() => {CI}.setProp({el('I1')}, 'value', 417)")
check(wait_ticked('md-heart', 5), 'setting the heart to 417 mL/s ticks md-heart')
rap = settle('RAP', lambda v: v < -20)
abp = settle('ABP', lambda v: v > 90)
check(abs(rap + 28) < 0.2 and abs(abp - 93) < 0.5, f'the heart alone restores ABP, but RAP falls to about −28 mmHg: {rap}, {abp}')
txt = model('md-q-heart', 'RAP went very negative: the veins would collapse.')
check('about 19 mmHg' in txt and 'about −28 mmHg' in txt and '(7 + 28) / 0.084 = 417 mL/s' in txt, 'the model answer has the model’s numbers')
p.js(f"() => {CI}.setProp({el('V1')}, 'value', 17.5)")
check(wait_ticked('md-veno', 5), 'raising MSFP to 17.5 mmHg ticks md-veno')
rap = settle('RAP', lambda v: v > -20)
check(abs(rap + 17.5) < 0.2, f'RAP is still about −17.5 mmHg: {rap}')
p.js(f"() => {CI}.toggleSwitch({el('S1')})")
check(wait_ticked('md-pump', 5), 'closing Muscle pump ticks md-pump')
rap = settle('RAP', lambda v: abs(v) < 0.2)
mt = meters()
check(abs(rap) < 0.2 and abs(mt['ABP'] - 93) < 0.5 and abs(mt['Venous return'] - 417) < 0.5,
      f'with MSFP 2.5-fold and RvR halved, 417 mL/s returns with RAP at 0 and ABP 93, as the model answer says: {mt}')
p.shot('s5-model-exercise')
txt = model('md-q-vr', 'MSFP up 2.5-fold and RvR halved: venous return five-fold, RAP 0.')
check('RAP is back to about 0 mmHg and ABP to 93 mmHg' in txt and '2.5 × 2 = 5-fold' in txt, 'the model answer works through the venous return equation')
check(mcq_right('md-q-max'), 'md-q-max: MSFP and RvR set the highest cardiac output')
# a haemorrhage
p.js(f"() => {{ {CI}.toggleSwitch({el('S1')}); {CI}.toggleSwitch({el('S2')}); }}")
p.js(f"() => {CI}.setProp({el('I1')}, 'value', 83.3)")
p.js(f"() => {CI}.setProp({el('V1')}, 'value', 3.5)")
check(wait_ticked('md-bleed', 5), 'setting MSFP to 3.5 mmHg ticks md-bleed (optional)')
rap = settle('RAP', lambda v: v < -3)
check(abs(rap + 3.5) < 0.1, f'with the heart still at 83.3 mL/s, RAP falls to −3.5 mmHg: {rap}')
p.js(f"() => {CI}.setProp({el('I1')}, 'value', 41.7)")
rap = settle('RAP', lambda v: abs(v) < 0.1)
abp = settle('ABP', lambda v: v < 50)
check(abs(rap) < 0.1 and abs(abp - 46.5) < 0.2, f'41.7 mL/s (2.5 L/min) brings RAP back to 0, and ABP is 46.5 mmHg, as the model answer says: {rap}, {abp}')
check(short('md-q-bleed', '2.5'), 'md-q-bleed: 2.5 litres a minute')
no_errors('the optional exercise in the Circuits tab')

# ====================================================================== 3 Write your essay
chapter('s5-write')
check(p.js("() => MG.app.currentBench") == 'exam', 'the chapter opens Supervision work')
txt = p.js("() => document.querySelector('#s5-write').innerText")
check('Using equations in your essay' in txt and 'One equation, quoted and used' in txt and 'VR = \\frac{MSFP - RAP}{RvR}' in txt,
      'it shows how to use equations, with a worked example, and how to type one with the Σ tool')
check(mcq_right('es5-q-hr') and mcq_right('es5-q-veno') and mcq_right('es5-q-pump'), 'the three slips are put right (es5-q-hr, es5-q-veno, es5-q-pump)')
tex = p.js("() => [MG.ExamTeX.check('VR = \\\\frac{MSFP - RAP}{RvR}'), MG.ExamTeX.text('VR = \\\\frac{MSFP - RAP}{RvR}')]")
check(tex[0] is None and 'MSFP' in tex[1] and 'RvR' in tex[1], f'the formula the page suggests is one the Σ tool accepts: {tex}')
click('#s5-write button[data-exam="s5-essay"]')
p.wait("() => document.querySelector('.ex-startcard h2') && document.querySelector('.ex-startcard h2').textContent === 'Supervision 5 essay'", timeout=30000)
sc = p.js("() => document.querySelector('.ex-startcard').textContent")
check('No time limit, but we suggest about 40 minutes' in sc and 'Supervision 5 · to hand in' in sc and 'Tim Hearn' in sc and 'formula tool' in sc,
      f'its first page: no time limit, 40 minutes suggested, how to type equations, and how to hand it in: {sc[:240]!r}')
click('.ex-startacts .btn.primary')
p.wait("() => document.querySelector('.ex-area')", timeout=30000)
check(wait_ticked('es5-start', 5), 'starting the essay ticks es5-start')
PARA = ('In sustained exercise the dilated arterioles of the working muscles lower TPR to about a fifth of its resting '
        'value, so by ABP = CO × TPR the cardiac output must rise about five-fold; venoconstriction raises MSFP and the '
        'muscle pump lowers RvR, so venous return rises to match. ')
p.js("(t) => { const A = document.querySelector('.ex-area'); A.focus(); document.execCommand('insertText', false, t); }", (PARA * 7).strip() + ' Venous return is ')
click('.ex-tb [data-cmd="formula"]')
P.fill('.ex-ftex', 'VR = \\frac{MSFP - RAP}{RvR}')
time.sleep(0.15)
click('.ex-formula-dlg .btn.primary')
time.sleep(0.3)
check(p.js("() => [...document.querySelectorAll('.ex-area .ex-formula')].map(f => f.getAttribute('data-tex'))") == ['VR = \\frac{MSFP - RAP}{RvR}'],
      'the venous return equation goes in with the formula tool')
time.sleep(1.6)
check(wait_ticked('es5-write', 5), f'writing more than 300 words ticks es5-write ({p.js("() => document.querySelector(\'.ex-wc\').textContent")})')
click('.ex-tile.review')
p.wait("() => document.querySelector('.ex-submit')", timeout=10000)
click('.ex-submit')
time.sleep(0.2)
click('.modal button:has-text("Submit now")')
p.wait("() => document.querySelector('.ex-receipt')", timeout=10000)
check(wait_ticked('es5-submit', 5), 'submitting ticks es5-submit')

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
        r = {'ok': True, 'receipt': f"S{d['week']}-Hb5K{len(posts):02d}", 'file': d['file']['name'], 'folder': f"Supervision {d['week']}",
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
check(msg == 'That isn’t the right hand-in password. Check it with Tim Hearn and try again.' and not ticked('es5-send'), f'a wrong password is refused: {msg!r}')
send(TEST_PW)
p.wait(f"() => document.querySelector('{RX}.handed')", timeout=20000)
d, R = posts[-1], replies[-1]
check(R.get('ok') and d.get('paper') == PAPER and d.get('week') == 5 and d.get('title') == 'Supervision 5 essay' and d.get('name') == NAME and d.get('words', 0) > 300,
      f'the right password hands in the essay, week 5, with the student’s name: { {k: v for k, v in d.items() if k not in ("file", "password")} }')
raw = base64.b64decode((d.get('file') or {}).get('data') or '')
check((d.get('file') or {}).get('name') == FILE and raw[:2] == b'PK', f'as a Word document named after the paper and the student: {(d.get("file") or {}).get("name")}')
doc = essay_text(raw)
check(NAME in doc and ESSAY in doc and 'venoconstriction raises MSFP' in doc, 'the Word document has the student’s name, the title and the essay')
check('RvR' in doc.split('Venous return is')[-1], f'and the formula: {doc.split("Venous return is")[-1][:60]!r}')
check(wait_ticked('es5-send', 5) and 'in the folder Supervision 5' in p.js(f"() => document.querySelector('{RX}').innerText"),
      'it arrives in the folder for Supervision 5, and es5-send ticks')
with P.expect_download() as dl:
    click(f'{RX} button:has-text("Download your copy")')
check(dl.value.suggested_filename == FILE and wait_ticked('es5-word', 5), 'Download your copy downloads the Word document, and ticks es5-word')
dl.value.save_as(os.path.join(OUT, 's5-essay.docx'))
p.shot('s5-receipt')
# the guidance, after submitting
click('.ex-receipt button:has-text("Review my answers")')
p.wait("() => document.querySelector('.ex-review')", timeout=10000)
rv = p.js("() => document.querySelector('.ex-review').innerText")
check(all(k in rv for k in ('functional hyperaemia', 'five-fold', '2.5 × 2 = 5', 'Fick principle', 'two legs', 'reset', 'Using the equations', 'Against the core criteria')),
      'Review my answers shows the guidance, carried by the equations, on the responses and the limits')
svg = p.js("() => { const s = document.querySelector('.ex-review svg'); if (!s) return null; const b = s.getBoundingClientRect(); return {lines: s.querySelectorAll('polyline').length, w: b.width, h: b.height, text: s.textContent}; }")
check(svg and svg['lines'] == 4 and svg['w'] > 250 and svg['h'] > 150 and all(k in svg['text'] for k in ('MSFP 7', 'MSFP 17.5', 'A', 'C', 'D', 'cardiac function', 'venous return')),
      f'and draws Guyton’s curves at rest and in exercise: {svg and {k: v for k, v in svg.items() if k != "text"}}')
p.shot('s5-essay-review')
P.locator('.q[data-q="es5-q-next"] textarea').fill('I quoted ABP = CO × TPR but never used VR = (MSFP − RAP) / RvR to explain why the heart alone cannot raise CO.')
time.sleep(0.6)
check(answered('es5-q-next'), 'es5-q-next is answered')
no_errors('the essay and handing it in')

# ====================================================================== 4 More practice
chapter('s5-more')
saqs = p.js("() => [...document.querySelectorAll('#s5-more ol.titles')[0].querySelectorAll('li')].map(l => l.textContent)")
revs = p.js("() => [...document.querySelectorAll('#s5-more ol.titles')[1].querySelectorAll('li')].map(l => l.textContent)")
check(len(saqs) == 3 and len(revs) == 2, f'the three short-answer questions and the two revision titles are listed: {len(saqs)}, {len(revs)}')
check(saqs[0] == 'Explain why increasing heart rate alone does not greatly increase cardiac output.' and saqs[1].startswith('A healthy person has an arterial blood pressure of 120/80 mmHg')
      and revs[0] == '“The heart is necessary for cardiac output, but it does not normally limit it.” Discuss.' and revs[1].startswith('Why is arterial blood pressure the principal controlled variable'),
      'in the handouts’ own words')
click('#s5-more button[data-exam="s5-saqs"]')
p.wait("() => document.querySelector('.ex-startcard h2') && /short-answer/.test(document.querySelector('.ex-startcard h2').textContent)", timeout=10000)
sc = p.js("() => document.querySelector('.ex-startcard').innerText")
check('supervision 5 · optional' in sc.lower() and 'Only the essay needs to be handed in' in sc and 'equation as its frame' in sc, f'the short-answer questions are optional: {sc[:120]!r}')
click('.ex-startacts .btn.primary')
p.wait("() => document.querySelector('.ex-area')", timeout=30000)
qt = p.js("() => document.querySelector('.ex-q').innerText")
check('increasing heart rate alone' in qt, f'question 1 is on heart rate and cardiac output: {qt[:80]!r}')
click('.ex-tb [data-cmd="ul"]')
for i, t in enumerate(['CO = HR × SV, but CO must equal VR = (MSFP − RAP) / RvR.', 'RAP is already close to zero.',
                       'The veins collapse if RAP falls below zero, so SV falls as HR rises.', 'Guyton’s pump experiment.',
                       'Pacing alone does not raise CO, but an arteriovenous fistula does.']):
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
check(wait_ticked('m5-saq', 5), 'submitting the short-answer questions ticks m5-saq (optional)')
click('.ex-receipt button:has-text("Review my answers")')
p.wait("() => document.querySelector('.ex-review')", timeout=10000)
rv = p.js("() => document.querySelector('.ex-review').innerText")
check(all(k in rv for k in ('Cowley and Guyton', '120 − 80 = 40 mmHg', '80 + 40/3 ≈ 93 mmHg', 'diving reflex', 'flow × concentration')),
      'and their guidance covers the three questions')
p.shot('s5-saq-review')
click('.ex-revbar button:has-text("Back")')
time.sleep(0.5)
p.js(f"() => {E}.home()")
time.sleep(0.5)
click('#s5-more button[data-exam="s5-revision"]')
p.wait("() => document.querySelector('.ex-startcard h2') && document.querySelector('.ex-startcard h2').textContent === 'Essay titles for revision'", timeout=10000)
sc = p.js("() => document.querySelector('.ex-startcard').innerText")
check('supervision 5 · optional' in sc.lower() and 'Only the Supervision 5 essay needs to be handed in' in sc, f'the revision titles are optional: {sc[:120]!r}')
no_errors('more practice')

# ====================================================================== progress, and the landing page afterwards
undone = p.js("""() => { const s = MG.tutorial.state; const t = [...document.querySelectorAll('[data-task]')].filter(li => !li.closest('.optional') && !s.tasks[li.dataset.task]).map(li => li.dataset.task);
    const q = [...document.querySelectorAll('.q[data-q]')].filter(x => !x.closest('.optional') && !(s.answers[x.dataset.q] || {}).done).map(x => x.dataset.q); return t.concat(q); }""")
check(undone == [], f'everything that counts is done: {undone}')
prog = p.js("() => document.querySelector('.progress-label').textContent")
check(prog.startswith('100%'), f'the page says it is finished: {prog}')
p.open('index.html')
tile = p.js("() => document.querySelector('.tile[data-sup=\"5\"]').innerText")
check('10 of 10' in tile or 'All the exercises done' in tile, f'tile 5 shows the work done: {tile[-200:]!r}')
check('✓ Essay handed in' in tile, f'and that the essay has been handed in: {tile[-120:]!r}')
p.shot('s5-landing-after')
no_errors('the landing page afterwards')
p.close()

# ====================================================================== a phone
ph = Page(width=390, height=844, mobile=True)
ph.open('supervision-5.html')
time.sleep(1.5)
w = ph.js("() => [document.documentElement.scrollWidth, window.innerWidth]")
check(w[0] <= w[1], f'Supervision 5 fits a phone: {w}')
for cid in ('s5-week', 's5-rec', 's5-model', 's5-write'):
    ph.js(f"() => MG.app.showChapter('{cid}', true)")
    time.sleep(0.6)
    over = ph.js(f"() => [...document.querySelectorAll('#{cid} .handin-box, #{cid} .activity, #{cid} .callout, #{cid} .q')].filter(e => e.scrollWidth > e.clientWidth + 1).length")
    check(over == 0, f'{cid} fits the phone’s width ({over} overflow)')
ph.shot('s5-phone')
ph.close()
done()
