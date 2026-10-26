"""The pages of the BMS supervisions site, for build/make_page.py.

index.html is the landing page: a tile for each supervision. A supervision whose work is ready has a page of its own
(supervision-N.html), made from build/template.html with the chapters of its module (build/s1.py for Supervision 1:
ALL() lists them) and its papers in exams/ (those with "week": N). A supervision that isn't ready yet opens the
workbench's guide (workbench.html: the chapters of build/chapters.py, the tour of the workbench).

To add a supervision's work: write its module of chapters (like s1.py), its papers (exams/sN-*.json, with
"week": N), and change its entry below (page, module, status 'ready', the texts of its tile, and handin_noun, the
work to hand in as the tile's status names it: 'Essay', say); then run python3 build/make_page.py."""

SITE_TITLE = 'BMS supervisions'
COURSE = 'NST IA Biomedical Sciences'
SUPERVISOR = 'Tim Hearn'

# the workbench's guide: the tour of the tabs (build/chapters.py), for the supervisions that have no page yet
GUIDE = {
    'page': 'workbench.html', 'data_page': 'workbench', 'week': 0, 'module': 'chapters',
    'title': 'The workbench guide', 'subtitle': 'How each tab of the workbench works',
    'description': 'A guide to each tab of the BMS supervisions workbench: the microscope, 3D anatomy and molecules, real '
                   'recordings, the organ bath, diagrams and circuits you can run, simulations, supervision work written as in '
                   'the online exam, and R. Everything runs in your web browser.',
}

SUPERVISIONS = [
    {
        'n': 1, 'status': 'ready', 'page': 'supervision-1.html', 'data_page': 'supervision-1', 'module': 's1',
        'title': 'Supervision 1', 'topic': 'Feedback, hormones and the hypothalamus',
        'subtitle': 'Supervision 1: feedback, hormones and the hypothalamus, through the body’s clock',
        'description': 'Supervision 1 of NST IA Biomedical Sciences covers homeostasis and feedback, moving things around, '
                       'hormones, the hypothalamus and pituitary, and the adrenal gland, all seen through the body’s daily '
                       'clock. There’s an essay to hand in, written as in the online exam, and short exercises in the workbench.',
        'card': 'Homeostasis and feedback, hormones, the hypothalamus and pituitary, and the adrenal gland, all seen '
                'through the body’s daily clock.',
        'handin': 'Discuss, with examples, why negative feedback mechanisms are more common than positive feedback '
                  'mechanisms in animal physiology.',
        'handin_short': 'an essay on why negative feedback is more common than positive feedback',
        'handin_paper': 's1-essay',
        'handin_noun': 'Essay',
        'time': 'About 40 minutes for the essay, and an hour for the exercises',
    },
    {
        'n': 2, 'status': 'ready', 'page': 'supervision-2.html', 'data_page': 'supervision-2', 'module': 's2',
        'title': 'Supervision 2', 'topic': 'Nerves, synapses and the autonomic nervous system',
        'subtitle': 'Supervision 2: nerves, synapses and the autonomic nervous system',
        'description': 'Supervision 2 of NST IA Biomedical Sciences covers electrochemical gradients, action potentials, '
                       'synapses and the autonomic nervous system. There’s a practical question on the thyroid gland and two '
                       'short-answer questions to hand in, and optional exercises in the workbench.',
        'card': 'Electrochemical gradients and resting potentials, the action potential, synapses and the '
                'neuromuscular junction, and the autonomic nervous system.',
        'handin': 'A practical question on the thyroid gland, and two short-answer questions.',
        'handin_short': 'a practical question on the thyroid gland, and two short-answer questions',
        'handin_paper': 's2-work',
        'handin_noun': 'Practical and short answers',
        'time': 'About an hour for the work to hand in, and half an hour for the optional exercises',
    },
] + [
    {'n': n, 'status': 'soon', 'page': GUIDE['page'], 'title': f'Supervision {n}', 'topic': '', 'card': '', 'time': ''}
    for n in range(3, 9)
]
