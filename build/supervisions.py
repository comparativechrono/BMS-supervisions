"""The pages of the BMS supervisions site, for build/make_page.py.

index.html is the landing page: a tile for each supervision. A supervision whose work is ready has a page of its own
(supervision-N.html), made from build/template.html with the chapters of its module (build/s1.py for Supervision 1:
ALL() lists them) and its papers in exams/ (those with "week": N). A supervision that isn't ready yet opens the
workbench's guide (workbench.html: the chapters of build/chapters.py, the tour of the workbench).

To add a supervision's work: write its module of chapters (like s1.py), its papers (exams/sN-*.json, with
"week": N), and change its entry below (page, module, status 'ready', the texts of its tile); then run
python3 build/make_page.py."""

import os
import re

SITE_TITLE = 'BMS supervisions'
COURSE = 'NST IA Biomedical Sciences'
SUPERVISOR = 'Tim Hearn'

# the workbench's guide: the tour of the tabs (build/chapters.py), for the supervisions that have no page yet
GUIDE = {
    'page': 'workbench.html', 'data_page': 'workbench', 'week': 0, 'module': 'chapters',
    'title': 'The workbench guide', 'subtitle': 'How each tab of the workbench works',
    'description': 'The BMS supervisions’ workbench: a guide to each of its tabs – the microscope, 3D anatomy and molecules, '
                   'real recordings, the organ bath, diagrams and circuits that run, simulations, supervision work written as '
                   'in the online exam, and R. Everything runs in your web browser.',
}

SUPERVISIONS = [
    {
        'n': 1, 'status': 'ready', 'page': 'supervision-1.html', 'data_page': 'supervision-1', 'module': 's1',
        'title': 'Supervision 1', 'topic': 'Feedback, hormones and the hypothalamus',
        'subtitle': 'Supervision 1: feedback, hormones and the hypothalamus – through the body’s clock',
        'description': 'Supervision 1 of NST IA Biomedical Sciences: homeostasis and feedback, moving things around, '
                       'hormones, the hypothalamus and pituitary, and the adrenal gland, seen through the body’s daily clock. '
                       'An essay to hand in, written as in the online exam, and short exercises in the workbench.',
        'card': 'Homeostasis and feedback, hormones, the hypothalamus and pituitary, and the adrenal gland – seen through '
                'the body’s daily clock.',
        'handin': 'Discuss, with examples, why negative feedback mechanisms are more common than positive feedback '
                  'mechanisms in animal physiology.',
        'handin_short': 'an essay on why negative feedback is more common than positive feedback',
        'handin_paper': 's1-essay',
        'time': 'Essay: about 40 minutes · exercises: about an hour',
    },
] + [
    {'n': n, 'status': 'soon', 'page': GUIDE['page'], 'title': f'Supervision {n}', 'topic': '', 'card': '', 'time': ''}
    for n in range(2, 9)
]


def _hand_in():
    """the hand-in settings of assets/js/config.js (handIn): the chapters say how to hand in by what is set up there –
    the hand-in script (straight to Google Drive) when its address is set, else the Dropbox file request.
    BMS_HANDIN_SCRIPT, when it is set (even to nothing), takes the place of the script's address: the tests use it to
    build the pages for the other way of handing in (with BMS_PAGES_OUT: see make_page.py)."""
    t = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'js', 'config.js'), encoding='utf-8').read()
    m = re.search(r"handIn:\s*\{(.*?)\n\s*\}", t, re.S)
    block = m.group(1) if m else ''

    def get(key):
        v = re.search(key + r":\s*'([^']*)'", block)
        return v.group(1) if v else ''
    script = os.environ['BMS_HANDIN_SCRIPT'] if 'BMS_HANDIN_SCRIPT' in os.environ else get('script')
    return {'script': script, 'dropbox': get('dropbox'), 'to': get('to') or SUPERVISOR}


HAND_IN = _hand_in()
