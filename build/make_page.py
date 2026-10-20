"""Write the site's pages, from the list in supervisions.py:
  - index.html, the landing page (landing.html): a tile for each supervision;
  - a page for each supervision whose work is ready (supervision-N.html): template.html with the supervision's chapters
    (its module's ALL());
  - workbench.html, the workbench's guide (the tour of chapters.py), which the supervisions that aren't ready open.
It also writes the lists that the tabs read: slides/index.json (the microscope's slide box, from each
slides/*/slide.json), exams/index.json (the papers of Supervision work) and examples/index.json (the diagrams and
circuits), and gives every page the list of the files that a new user finds in their home folder (everything in
../starter: starter/data/x.csv becomes ~/data/x.csv).
Run:  python3 build/make_page.py"""
import html as H
import importlib
import json
import os
import re
import sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from supervisions import COURSE, GUIDE, SITE_TITLE, SUPERVISIONS, SUPERVISOR  # noqa: E402

# the starter files: starter/ of the site → ~/ of the user. Increase STARTERS_VERSION when you add a starter file after
# students have started, so that they receive it (files they already have are left alone).
STARTERS_VERSION = 1
starters = []
for root, dirs, files in os.walk(os.path.join(SITE, 'starter')):
    dirs.sort()
    for f in sorted(files):
        rel = os.path.relpath(os.path.join(root, f), os.path.join(SITE, 'starter')).replace(os.sep, '/')
        if f in ('README.md', '.DS_Store'):
            continue
        starters.append({'p': rel, 's': os.path.getsize(os.path.join(root, f))})


def write_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
        f.write('\n')


def write(path, text):
    # (in one step: several builds can run at once)
    tmp = path + f'.{os.getpid()}.tmp'
    open(tmp, 'w', encoding='utf-8').write(text)
    os.replace(tmp, path)


# the slide box: one entry for each slide folder, in the order of the systems
SYSTEMS = ['Endocrine', 'Cardiovascular', 'Respiratory', 'Urinary', 'Digestive', 'Muscle', 'Nervous', 'Lymphoid', 'Skin',
           'Reproductive', 'Measuring', 'Other']
slides = []
sdir = os.path.join(SITE, 'slides')
if os.path.isdir(sdir):
    for d in sorted(os.listdir(sdir)):
        p = os.path.join(sdir, d, 'slide.json')
        if not os.path.exists(p):
            continue
        s = json.load(open(p, encoding='utf-8'))
        src = s.get('source', {})
        slides.append({
            'id': s['id'], 'title': s['title'], 'system': s.get('system', 'Other'), 'description': s.get('description', ''),
            'stain': s.get('stain', ''), 'width': s['width'], 'height': s['height'], 'mpp': s['mpp'],
            'credit': src.get('credit', ''), 'bytes': s.get('packBytes', 0), 'labels': len(s.get('labels', [])),
            'order': s.get('order', 0)
        })
    slides.sort(key=lambda x: (SYSTEMS.index(x['system']) if x['system'] in SYSTEMS else 99, x['order'], x['title']))
    write_json(os.path.join(sdir, 'index.json'), {'format': 'bms-slides-1', 'systems': SYSTEMS, 'slides': slides})


# the papers of Supervision work: exams/*.json (but index.json)
papers = []
edir = os.path.join(SITE, 'exams')
if os.path.isdir(edir):
    for f in sorted(os.listdir(edir)):
        if not f.endswith('.json') or f == 'index.json':
            continue
        e = json.load(open(os.path.join(edir, f), encoding='utf-8'))
        papers.append({'id': e['id'], 'file': f, 'title': e['title'], 'kind': e.get('kind', 'practice'),
                       'minutes': e.get('minutes'), 'suggestedMinutes': e.get('suggestedMinutes'),
                       'week': e.get('week'), 'required': bool(e.get('required')),
                       'questions': len([q for q in e.get('questions', []) if q.get('type') != 'info']),
                       'description': e.get('description', ''), 'order': e.get('order', 0)})
    papers.sort(key=lambda x: (x['week'] or 0, not x['required'], x['order'], x['title']))
    write_json(os.path.join(edir, 'index.json'), {'format': 'bms-exams-1', 'papers': papers})


# the examples of the Diagrams and Circuits tabs: examples/diagrams/*.flow.json, examples/circuits/*.circuit.json
examples = {}
for kind, folder, ext in (('diagrams', 'diagrams', '.flow.json'), ('circuits', 'circuits', '.circuit.json')):
    d = os.path.join(SITE, 'examples', folder)
    out = []
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            if not f.endswith(ext):
                continue
            e = json.load(open(os.path.join(d, f), encoding='utf-8'))
            out.append({'id': f[:-len(ext)], 'file': folder + '/' + f, 'title': e.get('title', f), 'description': e.get('description', ''),
                        'group': e.get('group', ''), 'order': e.get('order', 0)})
    out.sort(key=lambda x: (x['order'], x['title']))
    examples[kind] = out
if any(examples.values()):
    write_json(os.path.join(SITE, 'examples', 'index.json'), {'format': 'bms-examples-1', **examples})


class Ids(HTMLParser):
    """the steps (data-task) and questions (data-q) of the chapters, and whether each is in an optional part"""
    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.tasks, self.questions = [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        optional = 'optional' in (a.get('class') or '').split() or (self.stack and self.stack[-1][1])
        if 'data-task' in a:
            self.tasks.append((a['data-task'], bool(optional)))
        if 'data-q' in a:
            self.questions.append((a['data-q'], bool(optional)))
        if tag not in self.VOID:
            self.stack.append((tag, bool(optional)))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break


STARTERS_JS = ('<script>window.BMS_STARTERS = ' + json.dumps(starters, separators=(',', ':')) +
               f';\nwindow.BMS_STARTERS_VERSION = {STARTERS_VERSION};</script>')
shell = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
bad = False
registry = []
built = {}


def build_page(pg, week):
    """one page of the workbench: the template, with the chapters of pg['module']"""
    global bad
    mod = importlib.import_module(pg['module'])
    chapters = mod.ALL()
    body = '\n'.join(chapters).replace(' hidden>', '>', 1)  # (the first chapter is visible when the page loads)
    p = Ids()
    p.feed(body)
    for what, ids in (('task', [t for t, _ in p.tasks]), ('question', [q for q, _ in p.questions]), ('heading', re.findall(r'<h2 id="([^"]+)"', body))):
        dup = sorted({x for x in ids if ids.count(x) > 1})
        if dup:
            print(f'{pg["page"]}: {what}s used twice: {dup}')
            bad = True
    page = shell
    a = page.index('<!--CHAPTERS-->') + len('<!--CHAPTERS-->')
    b = page.index('<!--/CHAPTERS-->')
    page = page[:a] + '\n' + body + page[b:]
    page_js = '<script>window.BMS_PAGE = ' + json.dumps({'week': week, 'page': pg['page'], 'title': pg['title']}, ensure_ascii=False) + ';</script>'
    for k, v in {
        '{{PAGE_TITLE}}': H.escape(f'{pg["title"]} – {SITE_TITLE}'),
        '{{DESCRIPTION}}': H.escape(pg['description']),
        '{{DATA_PAGE}}': pg['data_page'],
        '{{TITLE}}': H.escape(pg['title']),
        '{{SUBTITLE}}': H.escape(pg['subtitle']),
        '{{WEEK}}': str(week),
        '{{PAGE_SCRIPT}}': page_js,
        '<!--STARTERS-->': STARTERS_JS,
    }.items():
        page = page.replace(k, v)
    left = re.findall(r'\{\{[A-Z_]+\}\}', page)
    if left:
        print(pg['page'], 'has placeholders left:', left)
        bad = True
    write(os.path.join(SITE, pg['page']), page)
    tasks = [t for t, opt in p.tasks if not opt]
    questions = [q for q, opt in p.questions if not opt]
    print(f'{pg["page"]}: {len(chapters)} chapters, {len(p.tasks)} steps and {len(p.questions)} questions '
          f'({len(tasks)} and {len(questions)} count towards finishing it), {len(body)} bytes of chapters')
    return {'page': pg['page'], 'dataPage': pg['data_page'], 'tasks': tasks, 'questions': questions}


# the workbench's guide, and each supervision that is ready
guide = build_page(GUIDE, 0)
for sv in SUPERVISIONS:
    if sv['status'] == 'ready':
        r = build_page(sv, sv['n'])
        r.update({'n': sv['n'], 'paper': sv.get('handin_paper')})
        registry.append(r)

# the landing page
land = open(os.path.join(HERE, 'landing.html'), encoding='utf-8').read()
tiles = []
for sv in SUPERVISIONS:
    n = sv['n']
    if sv['status'] == 'ready':
        tiles.append(f'''<a class="tile ready" href="{sv['page']}" data-sup="{n}">
  <span class="tile-n" aria-hidden="true">{n}</span>
  <span class="tile-kicker">Supervision {n}</span>
  <span class="tile-topic">{H.escape(sv['topic'])}</span>
  <span class="tile-text">{H.escape(sv['card'])}</span>
  <span class="tile-handin" title="{H.escape(sv['handin'])}"><b>To hand in:</b> {H.escape(sv.get('handin_short') or 'an essay, “' + sv['handin'] + '”')}</span>
  <span class="tile-time">{H.escape(sv['time'])}</span>
  <span class="tile-progress" aria-live="polite"><span class="tp-bar"><i></i></span><span class="tp-text">Not started yet</span></span>
  <span class="tile-essay" aria-live="polite"></span>
  <span class="tile-go">Open Supervision {n} <span aria-hidden="true">→</span></span>
</a>''')
    else:
        tiles.append(f'''<a class="tile soon" href="{sv['page']}" data-sup="{n}">
  <span class="tile-n" aria-hidden="true">{n}</span>
  <span class="tile-kicker">Supervision {n}</span>
  <span class="tile-topic">Coming soon</span>
  <span class="tile-text">I’ll put the work for this supervision here nearer the time. Until then, this tile opens the workbench and its guide.</span>
  <span class="tile-go">Open the workbench <span aria-hidden="true">→</span></span>
</a>''')
REG = '<script>window.BMS_SUPERVISIONS = ' + json.dumps(registry, ensure_ascii=False, separators=(',', ':')) + ';</script>'
for k, v in {'{{TILES}}': '\n'.join(tiles), '{{REGISTRY}}': REG, '{{SITE_TITLE}}': H.escape(SITE_TITLE),
             '{{COURSE}}': H.escape(COURSE), '{{SUPERVISOR}}': H.escape(SUPERVISOR), '{{GUIDE}}': GUIDE['page']}.items():
    land = land.replace(k, v)
left = re.findall(r'\{\{[A-Z_]+\}\}', land)
if left:
    print('index.html has placeholders left:', left)
    bad = True
write(os.path.join(SITE, 'index.html'), land)
print(f'index.html: {len(SUPERVISIONS)} tiles; {len(starters)} starter files; {len(slides)} slides; {len(papers)} papers; '
      f'{sum(len(v) for v in examples.values())} examples')
sys.exit(1 if bad else 0)
