"""Supervision 1's data and diagrams: the 24 hours of heart rate in starter/data/heart-rate-24h.csv (from the MIT-BIH
Normal Sinus Rhythm Database), and the two diagrams of the Diagrams tab that its chapters use, run with the workbench's
own simulator (MG.flowSim): the circadian clock (examples/diagrams/clock.flow.json), which must oscillate by itself
with a period of a little more than 24 h, lock onto 24 h when light reaches it, change its period with its delays and
stop when a box is knocked out; and thirst (examples/diagrams/thirst.flow.json), where feed-forward must remove most
of the overshoot of a delayed negative feedback loop.
Run:  python3 test/t_s1_data.py   (screenshots in test/out/s1-*.png)"""
import csv
import json
import os
import statistics as st
import time
from h import Page, check, done, SITE

# ---------------------------------------------------------------- the heart-rate data
path = os.path.join(SITE, 'starter', 'data', 'heart-rate-24h.csv')
rows = list(csv.DictReader(open(path, encoding='utf-8')))
check(list(rows[0].keys()) == ['subject', 'sex', 'age', 'hour', 'time', 'hr', 'n_beats'], f'heart-rate-24h.csv has its seven columns: {list(rows[0].keys())}')
subjects = sorted({r['subject'] for r in rows})
check(len(subjects) == 18 and len(rows) == 18 * 24, f'18 people × 24 hours ({len(subjects)} people, {len(rows)} rows)')
ok_hours = all(sorted(int(r['hour']) for r in rows if r['subject'] == s) == list(range(24)) for s in subjects)
check(ok_hours, 'each person has each clock hour, 0 to 23, once, in order')
check(all(r['time'] == f'{int(r["hour"]):02d}:00' for r in rows), 'time is the hour as a time ("08:00")')
check(all(r['sex'] in ('F', 'M') and 18 <= int(r['age']) <= 60 for r in rows), 'sex is F or M, and the ages are adults’')
hrs = [float(r['hr']) for r in rows if r['hr'] != 'NA']
na = [r for r in rows if r['hr'] == 'NA']
check(all(35 <= x <= 160 for x in hrs), f'every heart rate is possible ({min(hrs)}–{max(hrs)} beats/min)')
check(len(na) <= 60, f'few hours are NA ({len(na)})')
check(all(int(r['n_beats']) > 1000 for r in rows if r['hr'] != 'NA'), 'every hour with a heart rate rests on more than 1000 beats')
check(all(r['n_beats'].isdigit() for r in rows), 'n_beats is a whole number everywhere')
day = [float(r['hr']) for r in rows if r['hr'] != 'NA' and 8 <= int(r['hour']) < 20]
night = [float(r['hr']) for r in rows if r['hr'] != 'NA' and int(r['hour']) < 6]
diff = st.mean(day) - st.mean(night)
check(10 <= diff <= 25, f'the heart rate is lower at night: day {st.mean(day):.1f}, night {st.mean(night):.1f} beats/min ({diff:.1f} lower)')
lower = 0
for s in subjects:
    d = [float(r['hr']) for r in rows if r['subject'] == s and r['hr'] != 'NA' and 8 <= int(r['hour']) < 20]
    n = [float(r['hr']) for r in rows if r['subject'] == s and r['hr'] != 'NA' and int(r['hour']) < 6]
    lower += st.mean(d) > st.mean(n)
check(lower == 18, f'every one of the 18 has a lower heart rate at night ({lower})')
means = {h: st.mean([float(r['hr']) for r in rows if int(r['hour']) == h and r['hr'] != 'NA']) for h in range(24)}
trough = min(means, key=means.get)
check(2 <= trough <= 6, f'the mean is lowest in the small hours ({trough:02d}:00, {means[trough]:.1f} beats/min)')
check(all(sum(1 for r in rows if int(r['hour']) == h and r['hr'] != 'NA') >= 6 for h in range(24)), 'every hour has a heart rate for at least 6 people')
check(os.path.getsize(path) < 30000, f'the file is small ({os.path.getsize(path)} bytes)')
check(os.path.exists(os.path.join(SITE, 'starter', 'data', 'README.md')), 'starter/data/README.md describes it')

# ---------------------------------------------------------------- the diagrams, run with the workbench's simulator
SIM = """<!doctype html><html><head><meta charset="utf-8"></head><body data-page="s1sim">
<script src="assets/js/config.js"></script><script src="assets/js/core.js"></script><script src="assets/js/flow.js"></script>
<script>window.MG_READY = !!(window.MG && MG.flowSim);</script></body></html>"""
p = Page(extra={'s1sim.html': (SIM, 'text/html')})
p.open('s1sim.html')
RUN = """async ([file, change]) => {
  const D = await (await fetch('examples/diagrams/' + file + '.flow.json')).json();
  const apply = (o) => {
    for (const [k, v] of Object.entries(o.nodes || {})) Object.assign(D.nodes.find((n) => n.id === k), v);
    for (const [k, v] of Object.entries(o.edges || {})) Object.assign(D.edges.find((e) => e.id === k), v);
    if (o.duration) D.sim.duration = o.duration;
  };
  apply(change || {});
  const r = MG.flowSim.simulate(D);
  const out = { osc: r.oscillating.map((o) => [o.id, o.trend]), runaway: r.runaway, series: {} };
  const t = r.times;
  for (const id of Object.keys(r.series)) {
    const s = r.series[id];
    let lo = Infinity, hi = -Infinity; for (const y of s) { lo = Math.min(lo, y); hi = Math.max(hi, y); }
    const ext = hi - lo > 1e-9 ? MG.flowSim.turningPoints(s, 0.03 * (hi - lo)) : [];
    const peaks = ext.filter((e) => e.type === 'max').map((e) => t[e.i]);
    // the last 40%: what is left of the rhythm
    const k = Math.floor(s.length * 0.6); let lo2 = Infinity, hi2 = -Infinity;
    for (let q = k; q < s.length; q++) { lo2 = Math.min(lo2, s[q]); hi2 = Math.max(hi2, s[q]); }
    out.series[id] = { lo, hi, last: s[s.length - 1], peaks, tailRange: hi2 - lo2, argmin: t[s.indexOf(lo)] };
  }
  return out;
}"""


def run(file, change=None):
    return p.js(RUN, [file, change or {}])


def period(peaks, after):
    pk = [x for x in peaks if x >= after]
    return (pk[-1] - pk[0]) / (len(pk) - 1) if len(pk) >= 2 else None


r = run('clock')
g = r['series']['genes']
per = period(g['peaks'], 30)
trend = dict(r['osc']).get('genes')
check(trend == 'steady', f'the clock, as given, oscillates by itself, steadily ({r["osc"]})')
check(per is not None and 24.3 <= per <= 25.0, f'its free-running period is a little longer than 24 h ({per and round(per, 2)} h)')
check(len(g['peaks']) >= 4 and not r['runaway'], f'about five cycles in the run ({len(g["peaks"])} peaks), and nothing runs away')
r = run('clock', {'edges': {'entrain': {'blocked': False}}, 'duration': 240})
per_l = period(r['series']['genes']['peaks'], 120)
check(per_l is not None and abs(per_l - 24) < 0.1, f'with the light’s arrow unblocked, it locks onto 24 h ({per_l and round(per_l, 2)} h)')
r = run('clock', {'edges': {'entrain': {'blocked': False}}, 'duration': 240})
pk = [x % 24 for x in r['series']['genes']['peaks'] if x >= 120]
check(max(pk) - min(pk) < 0.5, f'… at the same time of day each day (peaks at {[round(x, 1) for x in pk]} h)')
table = {}
for d in (2, 3, 4, 5, 6, 8):
    r = run('clock', {'edges': {'back': {'delay': d}}, 'duration': 200})
    table[d] = period(r['series']['genes']['peaks'], 60)
print('    period by the delay of "back into the nucleus":', {k: v and round(v, 1) for k, v in table.items()})
check(all(table[a] < table[b] for a, b in ((2, 3), (3, 4), (4, 5), (5, 6), (6, 8))), 'a longer delay makes a longer period, and a shorter one a shorter period')
check(table[2] < 21 and table[6] > 28, f'short delays give a period like perS’s (~19–20 h: {table[2]:.1f} h), long ones like perL’s (~28–29 h: {table[6]:.1f} h)')
for d in (2, 6):
    r = run('clock', {'edges': {'made': {'delay': d}}, 'duration': 200})
    pd = period(r['series']['genes']['peaks'], 60)
    check(abs(pd - table[d]) < 0.2, f'the delay of "made into protein" works the same way ({d} h: {pd:.1f} h)')
r = run('clock', {'nodes': {'protein': {'knocked': True}}})
check(r['series']['genes']['tailRange'] < 0.01 and not r['osc'], f'knocking out the proteins (per⁰, from the start) leaves no rhythm: the genes stay switched on ({r["series"]["genes"]["last"]:.2f}; oscillating: {r["osc"]})')
r = run('clock', {'nodes': {'bmal': {'knocked': True}}})
check(r['series']['genes']['tailRange'] < 0.01 and abs(r['series']['genes']['last']) < 0.01 and not r['osc'], 'knocking out CLOCK and BMAL1 leaves no rhythm either, with the genes switched off')

r = run('thirst')
o = r['series']['osm']
r2 = run('thirst', {'edges': {'e-ff': {'blocked': False}}})
o2 = r2['series']['osm']
print(f'    thirst: peak {o["hi"]:.1f} mOsm/L; with negative feedback alone it falls to {o["lo"]:.1f} (at {o["argmin"]:.0f} min), with feed-forward to {o2["lo"]:.1f}')
check(307 <= o['hi'] <= 311, f'sweating raises osmolarity to about 310 mOsm/L ({o["hi"]:.1f})')
check(o['lo'] < 293, f'with negative feedback alone, the person over-drinks: osmolarity overshoots to {o["lo"]:.1f} mOsm/L')
check(o2['lo'] > 297, f'with the feed-forward arrow unblocked, most of the overshoot goes ({o2["lo"]:.1f} mOsm/L)')
check((300 - o2['lo']) < 0.25 * (300 - o['lo']), 'feed-forward removes more than three quarters of the overshoot')
check(abs(o['last'] - 300) < 0.5 and abs(o2['last'] - 300) < 0.5, 'osmolarity comes back to its set point in both')
d1, d2 = r['series']['drink'], r2['series']['drink']
check(d2['hi'] <= d1['hi'] + 1e-6, 'with feed-forward, drinking stops sooner (its peak is no higher)')
check(not p.errors, 'no page errors: ' + '; '.join(p.errors[:2]))
p.close()

# ---------------------------------------------------------------- the diagrams in the Diagrams tab (screenshots)
p = Page(width=1500, height=950)
p.open()
p.js("() => MG.app.showWorkbench('flow')")
p.wait("() => MG.app.flow && MG.app.flow.open", timeout=30000)
for name, change in (('clock', None), ('clock-light', 'entrain'), ('thirst', None), ('thirst-ff', 'e-ff')):
    ex = name.split('-')[0]
    p.js(f"() => MG.app.flow.open('example:{ex}', {{ force: true }})")
    time.sleep(0.8)
    if change:
        p.js(f"() => {{ MG.app.flow.setEdge('{change}', {{ blocked: false }}, 'blocked'); MG.app.flow.run(); }}")
    else:
        p.js("() => MG.app.flow.run()")
    time.sleep(1.5)
    p.shot(f's1-{name}')
check(not p.errors, 'the diagrams open and run in the Diagrams tab without errors: ' + '; '.join(p.errors[:2]))
p.close()
done()
