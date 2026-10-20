"""The chapters of Supervision 1 (supervision-1.html): feedback, hormones and the hypothalamus, seen through the body's
daily clock.

The essay to hand in is in Supervision work (exams/s1-essay.json), with the optional short-answer questions
(s1-saqs.json) and the essay titles for revision (s1-revision.json). The chapters: what to do this week; three short
exercises, about an hour in all (a clock made of negative feedback and the thirst loop, in Diagrams; where the clock and
the glands it drives are, in Anatomy, the Microscope and Molecules; the heart's daily rhythm, in the Recorder and R, from
starter/data/heart-rate-24h.csv); how essays are marked, against the six core criteria, with an example essay; the
University's plagiarism exercise, and why Supervision work won't paste; writing the essay and handing it in; and more
practice. ALL() puts them in order.

The lecture notes are Prof. Matthew Mason's: nothing here is copied from them. The core criteria are those of
Assessment Plus (a HEFCE-funded project), as on the essay feedback form; the plagiarism exercise is the University's
(Kohler, 1994)."""
from lib import *

ESSAY = ('Discuss, with examples, why negative feedback mechanisms are more common than positive feedback mechanisms in '
         'animal physiology.')
SUPERVISOR = 'Tim Hearn'
PLUM = '#8a1c4a'


def handin_box(buttons=True):
    """the essay to hand in, as the first thing the student sees"""
    b = (f'<p class="hb-acts">{goto("s1-write", "how to write it and hand it in")} {exam("s1-essay", "open the essay")}</p>'
         if buttons else '')
    return f'''<div class="handin-box">
  <div class="hb-k">To hand in this week</div>
  <p class="hb-title">“{ESSAY}”</p>
  <ul>
    <li>An essay, written in <b>Supervision work</b> – the first tab of the workbench – as you will write essays in the online exam: typed, in one sitting, without notes and with nothing pasted in.</li>
    <li>There is no time limit, but aim for about <b>40 minutes</b>.</li>
    <li>When you have submitted it, <b>hand it in</b> from the same page, before your supervision: you download it as a Word document and upload that to <b>{SUPERVISOR}</b>’s Dropbox, with the password he gives you.</li>
  </ul>
  {b}
</div>'''


def optional(body, title='If you have time', hid=None):
    i = f' id="{hid}"' if hid else ''
    return f'<div class="optional">\n<h2{i}>{title}</h2>\n{body}\n</div>'


# ---------------------------------------------------------------------------------------------------------------------
def ch_week(num):
    body = f'''
{handin_box()}

<h2 id="wk-plan">The week, step by step</h2>
<ol class="plan">
<li><b>Three short exercises</b>, about an hour in all, that give you examples for your essay: a clock made of negative feedback, in <b>Diagrams</b> (chapter 1); where the clock is, and the glands it drives, in <b>Anatomy</b>, the <b>Microscope</b> and <b>Molecules</b> (chapter 2); and your heart’s daily rhythm, in real recordings and <b>R</b> (chapter 3). {goto("s1-clock", "start")}</li>
<li><b>How essays are marked</b>, and <b>plagiarism</b>: read these before you write (chapters 4 and 5, about 25 minutes). {goto("s1-marking", "go there")}</li>
<li><b>Write your essay</b>, and hand it in (chapter 6, about 45 minutes). {goto("s1-write", "go there")}</li>
<li>For more practice, if you would like it: five short-answer questions, and four more essay titles to note for revision (chapter 7). These are optional. {goto("s1-more", "go there")}</li>
</ol>
{activity("Before you start", [
    task("wk-name", 'Add your name: click <b>Your name</b> at the top of the page. It goes at the top of the essay you hand in, and every supervision’s page uses it. (It is kept in this browser only.)', check="named"),
])}

<h2 id="wk-why">Why the clock?</h2>
<p>Your body is not the same at four in the morning as at four in the afternoon. Your core temperature, blood pressure and heart rate, and the levels of cortisol and melatonin in your blood, rise and fall through every day, driven by a master clock in your hypothalamus: the <b>suprachiasmatic nucleus</b> (SCN). The clock is built from negative feedback; it is set each day by light; and it acts through the autonomic nervous system, the pituitary and hormones. So it touches every one of this week’s lectures – and this week we look at them through the clock.</p>

<h2 id="wk-how">How this page works</h2>
<ul>
<li>The instructions are on the left, and the workbench is on the right: each of its tabs is a tool. You can drag the divider between them, and the button at the top left hides the instructions.</li>
<li>The steps of each activity tick themselves when you do them (<span class="auto-tag">✓ spotted</span>), or you can tick them yourself. Buttons such as {bench("exam", "show me")} do things for you: they open a diagram, a slide or a recording, or type a line of R.</li>
<li>Have a go at each question before you look at its <b>model answer</b> (<b>Show answer</b>). Multiple-choice questions tell you straight away whether you are right, and why.</li>
<li>Parts headed <b>If you have time</b> are extras: they don’t count towards finishing the page.</li>
<li>Everything you do is saved in this browser, on this computer. <b>My answers</b>, at the top, downloads your answers; your essay downloads as a Word document.</li>
<li>New to the workbench? The <a href="workbench.html" target="_blank" rel="noopener">workbench guide</a> shows how each of its tabs works.</li>
</ul>
'''
    return chapter("s1-week", num, "This week", "exam", "Supervision 1: feedback, hormones and the hypothalamus", 5,
                   "This week’s lectures – homeostasis and feedback, moving things around, hormones, the hypothalamus and "
                   "pituitary, and the adrenal gland – seen through the body’s daily clock. Here is the essay to hand in, "
                   "and a few short exercises to go with it.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_clock(num):
    body = f'''
<h2 id="ck-thirst">Thirst: a slow loop, and feed-forward</h2>
<p>In the first lecture you met a problem with drinking. When you sweat, the osmolarity of your extracellular fluid (ECF) rises; osmoreceptors in the hypothalamus detect it, and you feel thirsty and drink. But water takes time to be absorbed from the gut – and until it has been, the osmoreceptors go on telling you that you need it.</p>
{activity("Run the thirst loop", [
    task("ck-th-open", f'Open the diagram {flow("example:thirst", "show me")}. The comparator (Σ) compares the osmolarity of the ECF with its set point, 300 mOsm/L, and the difference makes you thirsty.', auto="flow:open example=thirst"),
    task("ck-th-run", f'Press <b>Run</b> {flowrun("show me")}, and watch <i>ECF osmolarity</i> in the graphs under the diagram. You can drag the slider under the graphs to see the diagram at any moment.', auto="flow:run name~thirst blocked>0"),
    task("ck-th-ff", 'The grey arrow labelled <i>feed-forward</i>, from the mouth and stomach receptors, is blocked. Right-click it (or press and hold it), choose <b>Unblock this arrow</b>, and run the diagram again.', auto="flow:run name~thirst blocked=0"),
])}
{q("ck-q-thirst", "With negative feedback alone, what happened to the osmolarity once you started to drink, and why? What did the feed-forward arrow change?",
   "With negative feedback alone, the osmolarity overshot: it fell to about 291 mOsm/L, about as far below the set point as sweating had raised it above it (to about 309), before it came back to 300. The water takes about 15 minutes to be absorbed, and all that time the osmoreceptors still report a high osmolarity, so you go on drinking: by the time the water reaches the blood, you have drunk too much. Negative feedback with a delay overshoots, and can oscillate. With feed-forward, receptors in the mouth and stomach signal that water has been drunk before it has been absorbed, and switch thirst off for a while: you drink less, and the overshoot almost disappears (the lowest point is about 298 mOsm/L). This is what Bellows (1938) found in dogs with oesophageal fistulae, whose water never reached the stomach: they drank about the right amount and then stopped – but only for a while.")}

<h2 id="ck-clock">A clock in every cell</h2>
<p>Almost every cell in your body has a clock, and it is built from a negative feedback loop of genes and proteins (a <em>transcription–translation feedback loop</em>). Two proteins, CLOCK and BMAL1, switch on the <i>Per</i> and <i>Cry</i> genes. Their mRNA is made into the PER and CRY proteins, which – hours later – go back into the nucleus and switch their own genes off. When the proteins have been broken down, the genes come on again, and the cycle starts again.</p>
{callout("concept", "Why a slow loop makes a clock", "<p>Without delays, negative feedback settles to a steady level. But each step of this loop takes hours: transcription, translation, the changes made to the proteins, and their journey back into the nucleus. By the time the proteins switch the genes off there are far too many of them, and by the time they have gone, the genes have been off for too long. So the loop overshoots one way and then the other, for ever: it oscillates, with a period set mainly by its delays – about a day.</p>")}
{activity("Run the clock", [
    task("ck-open", f'Open the clock {flow("example:clock", "show me")}. (If it asks whether to leave the thirst diagram, you needn’t save it.) The arrow from <i>Light</i> is blocked: the clock is in a cave, with no daylight to set it.', auto="flow:open example=clock"),
    task("ck-run", f'Run it {flowrun("show me")}. The message under the diagram gives the period of the oscillation, from one peak to the next.', auto="flow:run name~clock oscillates=true blocked>0"),
])}
{q("ck-q-period", "What is the period of the clock in the cave, in hours?",
   "About 24.6 hours. Without daylight, a clock runs at its own pace, a little different from 24 hours – which is why these rhythms are called <i>circadian</i> (from <i>circa diem</i>, about a day). In 1962 the French caver Michel Siffre lived for 63 days in a cave, with no daylight and no clock. He went on sleeping and waking in a regular cycle, but it was a little longer than 24 hours, so his days slipped later and later: when he came out, he thought he had been underground for much less time than he had.",
   accept="num:24.6±0.4", placeholder="hours")}
{activity("Make some mutants", [
    task("ck-short", 'Click the arrow labelled <i>back into the nucleus</i> and, in the panel on the right, change its <b>Delay</b> from 4 to 2 hours. Run the diagram again, and read the period.', auto="flow:run name~clock period>0 period<22"),
    task("ck-long", 'Now make the delay 6 hours, and run it again.', auto="flow:run name~clock period>27"),
    task("ck-ko", 'Put the delay back to 4 hours. Then right-click <i>PER and CRY proteins</i>, choose <b>Knock it out</b>, and run it.', auto="flow:run name~clock knocked>0 oscillates=false"),
])}
{mcq("ck-q-per", "The first clock gene, <i>period</i>, was found in fruit flies by Ronald Konopka and Seymour Benzer in 1971. One mutant fly had a rhythm of about 19 hours (<i>per</i><sup>S</sup>), another of about 29 hours (<i>per</i><sup>L</sup>), and a third had no rhythm at all (<i>per</i><sup>0</sup>). Which change to the model made a clock like <i>per</i><sup>0</sup>?", [
    ("Shortening the delay of <i>back into the nucleus</i>", False, "No: a shorter delay gave a shorter period (about 20 hours), more like perˢ."),
    ("Knocking out the PER and CRY proteins", True, "Yes. Without the proteins there is no feedback: nothing switches the genes off, so they stay on and nothing oscillates – like the per⁰ flies, which make no working PER protein."),
    ("Lengthening the delay of <i>back into the nucleus</i>", False, "No: a longer delay gave a longer period (about 29 hours), like perᴸ."),
])}
{activity("Out of the cave", [
    task("ck-light", 'Put the proteins back (right-click them: <b>Put it back to normal</b>), and unblock the arrow from <i>Light</i>: the clock is out of the cave. Run it.', auto="flow:run name~clock blocked=0 knocked=0 period>23.5 period<24.5"),
])}
{q("ck-q-light", "Out of the cave, what was the period? What does light do to the clock, and why does the clock need it?",
   "24 hours. Light resets – <em>entrains</em> – the clock each day, so that it keeps to 24 hours and stays in step with the Sun: light is the clock’s main <i>zeitgeber</i> (“time-giver”). A clock with a period of 24.6 hours that was never reset would drift by about 36 minutes a day, and within a few weeks it would be telling you that midnight was noon. In mammals the light reaches the master clock, the SCN, through the eyes (you will follow its path in the next chapter). Many people who are totally blind have clocks that free-run, drifting in and out of step with the day.")}
{callout("info", "A Nobel Prize for the loop", "<p>In 2017 Jeffrey Hall, Michael Rosbash and Michael Young won the Nobel Prize in Physiology or Medicine for discovering how the clock works: the PER protein builds up at night, enters the nucleus and switches off its own gene – the loop you have just run. Clocks are found in animals, plants, fungi and some bacteria: their genes differ, but most are built round a delayed negative feedback loop like this one.</p>")}
{callout("tip", "For your essay", "<p>A clock is negative feedback that is <em>meant</em> to oscillate: a long delay turns a loop that would hold things steady into one that keeps time. Thirst is negative feedback that would overshoot if feed-forward didn’t help it. Both say something about the strengths and the limits of negative feedback.</p>")}
{optional(f"""
{activity("A 24-hour clock in the cave", [
    task("ck-24", 'Block the arrow from <i>Light</i> again. Can you make the clock keep 24 hours in the cave, to within 0.2 hours? Change the delays of <i>made into protein</i> and <i>back into the nucleus</i> (what matters is the total delay round the loop).', auto="flow:run name~clock blocked>0 period>23.8 period<24.2"),
    task("ck-pos", f'For comparison, positive feedback: open the example of blood clotting {flow("example:positive-feedback-clotting", "show me")} and run it.', auto="flow:open example=positive-feedback-clotting"),
])}
{q("ck-q-pos", "Once clotting starts, what happens to it, and why can’t a loop like this hold anything steady?",
   "It runs away: each step makes more of what activates it, so the response grows faster and faster until something outside the loop stops it – in the body, anticoagulants, which keep the clot to the wound. Positive feedback reinforces a change instead of opposing it, so it can’t return a variable to a set point – it is useful where a fast, all-or-nothing change is needed, and it is always brought to an end.")}
""")}
'''
    return chapter("s1-clock", num, "A clock made of feedback", "flow", "A clock made of negative feedback", 15,
                   "Negative feedback holds things steady – unless it is slow. Add a delay and it overshoots; add a long "
                   "one and it never settles. Run two loops from the lectures: thirst, and the clock in your cells.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_where(num):
    body = f'''
<h2 id="wh-brain">The master clock</h2>
<p>The <b>suprachiasmatic nuclei</b> (SCN) are two small clusters of neurons, one on each side of the third ventricle, at the bottom of the hypothalamus. They sit just above the <b>optic chiasm</b>, where the optic nerves meet and cross – hence their name (<i>supra</i>, above). They are too small to be in the model, but you can find exactly where they are.</p>
{activity("Find the clock", [
    task("wh-glands", f'Show the endocrine glands, with their labels {anat("endocrine+labels")}.', auto="anat:system id=endocrine on=true"),
    task("wh-hypo", 'Zoom in on the head. Click on the two parts of the pituitary gland: the <b>adenohypophysis</b> (the anterior pituitary) and the <b>neurohypophysis</b> (the posterior pituitary). Then click on the <b>hypothalamus</b>, just above them.', auto="anat:select id=hypothalamus by=click||anat:select id=hypothalamus by=list"),
    task("wh-pineal", f'{anatfind("pineal-gland", "Find the pineal gland")}, which makes melatonin at night, when the SCN tell it to.', auto="anat:find ok=true target~pineal"),
    task("wh-adrenal", f'{anatfind("suprarenal-gland", "Find a suprarenal gland")} (an adrenal gland), on top of a kidney. The clock reaches it through the pituitary: ACTH, and so cortisol, rise in the early morning, before you wake.', auto="anat:find ok=true target~suprarenal"),
    task("wh-chiasm", f'{anatfind("optic-chiasm", "Find the optic chiasm")}. The brain is shown with it: look at it from below (<b>View</b> ▸ <i>Inferior</i>, or the key <kbd>6</kbd>). The SCN lie just above the chiasm.', auto="anat:find ok=true target~optic-chiasm"),
    task("wh-cut", f'Cut the head in two {anat("brain+endocrine:hypothalamus+section:sagittal@0.5@left")}: in the cut, the hypothalamus, the pituitary on its stalk and the pineal gland all lie close to the midline.', auto="anat:section axis=sagittal"),
])}
{q("wh-q-light", "Light sets the clock. Follow its path: from which cells of the eye, by which route, to where?",
   "Some of the ganglion cells of the retina contain a photopigment of their own, <b>melanopsin</b>, which responds best to blue light. These intrinsically photosensitive retinal ganglion cells (ipRGCs) send their axons along the optic nerve to the optic chiasm, where they leave it in the <b>retinohypothalamic tract</b> for the SCN just above. The SCN’s neurons fire faster by day than at night, and they pass the time of day on to the rest of the body – to the pineal gland, for example, through the paraventricular nucleus, the spinal cord and sympathetic nerves, which is why melatonin is made at night.")}

<h2 id="wh-scope">Under the microscope</h2>
{activity("The pituitary and the adrenal gland", [
    task("wh-pit", f'Open the pituitary gland {scope("pituitary-gland", "show me")}. In this specimen, the anterior pituitary (on the left) and the posterior pituitary (on the right) were cut as two pieces.', auto="scope:open slide=pituitary-gland"),
    task("wh-post", f'{scopefind("pituitary-gland:posterior", "Find the posterior pituitary")}, and compare it with the anterior pituitary at 20×.', auto="scope:find slide=pituitary-gland target=posterior ok=true"),
    task("wh-adr", f'Open the adrenal gland {scope("adrenal-gland", "show me")} and look at it at 1×: a capsule, the cortex in three zones, and the medulla in the middle.', auto="scope:open slide=adrenal-gland"),
    task("wh-zf", f'{scopefind("adrenal-gland:zona-fasciculata", "Find the zona fasciculata")}: the widest zone of the cortex, its cells in long columns.', auto="scope:find slide=adrenal-gland target=zona-fasciculata ok=true"),
    task("wh-med", f'{scopefind("adrenal-gland:medulla", "Find the medulla")}, which makes adrenaline.', auto="scope:find slide=adrenal-gland target=medulla ok=true"),
])}
{q("wh-q-pit", "Why does the posterior pituitary look so different from the anterior pituitary?",
   "The posterior pituitary is nervous tissue, an extension of the hypothalamus: it is made of the axons and nerve terminals of neurons whose cell bodies lie in the supraoptic and paraventricular nuclei, with glial cells (pituicytes) among them – so it looks pale and fibrous, with few nuclei. Its nerve terminals release ADH and oxytocin into the blood. The anterior pituitary is a gland: clusters and cords of endocrine cells, with many nuclei and stained cytoplasm, between wide capillaries (sinusoids) that bring the releasing hormones of the hypothalamus down the portal vessels.")}
{mcq("wh-q-zone", "Cortisol rises in the early morning, before you wake, preparing you for the day. Which part of the adrenal gland makes it?", [
    ("The zona glomerulosa", False, "No: the outermost zone makes aldosterone, under the control of the renin–angiotensin system and the concentration of K+ in the plasma."),
    ("The zona reticularis", False, "No: the innermost zone of the cortex makes mainly androgens, such as DHEA."),
    ("The zona fasciculata", True, "Yes. Its cells make cortisol under the control of ACTH from the anterior pituitary – and cortisol feeds back on the hypothalamus and the pituitary to switch them off: a negative feedback loop, with a daily rhythm on top."),
    ("The medulla", False, "No: the medulla makes adrenaline, when its sympathetic nerves tell it to."),
])}

<h2 id="wh-mol">Two hormones of the day and the night</h2>
{activity("Melatonin and cortisol", [
    task("wh-mel", f'Open melatonin {viewer("clear; molecule melatonin; only ballstick; color cpk", "show me")}, which the pineal gland makes from tryptophan, by way of serotonin. Its level in the blood rises at night, to about 80 pg/mL.', auto="viewer:molecule name=Melatonin"),
    task("wh-cort", f'Now open cortisol {viewer("clear; molecule cortisol; only ballstick; color cpk", "show me")}, a steroid made from cholesterol.', auto="viewer:molecule name=Cortisol"),
])}
{mcq("wh-q-lipid", "Cortisol is a steroid, so it is lipid-soluble. Which of these follows from that?", [
    ("It is stored in vesicles and released by exocytosis", False, "No: that is how water-soluble hormones, such as adrenaline, are released. A lipid-soluble hormone would leak out of a vesicle through its membrane, so steroids are made as they are needed and released straight away."),
    ("It crosses the membranes of its target cells and binds receptors inside them, which change the transcription of genes – so its effects take hours to develop, and last", True, "Yes. Steroid receptors are inside the cell, and once they have bound their hormone they act as transcription factors."),
    ("It is carried freely dissolved in the plasma", False, "No: most of the cortisol in the blood is bound to carrier proteins (corticosteroid-binding globulin and albumin), and only the small free fraction can act."),
], model="Melatonin, an indoleamine, is lipid-soluble too, so it isn’t stored either: it leaves the pineal gland as soon as it is made, and its level in the blood follows how fast it is being made – high at night, low by day. (It acts mainly on receptors in the membranes of its target cells, including those of the SCN: melatonin feeds back on the clock.)")}
{optional(f"""
{activity("Blue light, and the adrenal cortex", [
    task("wh-sim", f'The clock’s photopigment, melanopsin, is most sensitive to blue light, at about 480 nm. Open the Color Vision simulation {sim("color-vision", "show me")} and, on its <b>Single Bulb</b> screen, set the bulb to a single colour of about 480 nm.', auto="sim:open id=color-vision"),
    task("wh-aldo", f'Open aldosterone {viewer("clear; molecule aldosterone; only ballstick; color cpk", "show me")}, made in the zona glomerulosa, and compare it with cortisol: two steroids made from cholesterol, which differ in only a few groups of atoms.', auto="viewer:molecule name=Aldosterone"),
])}
{q("wh-q-screen", "Why might using a bright screen late in the evening make it harder to fall asleep?",
   "Screens give out a lot of blue light, which melanopsin responds to best. Light in the evening reaches the SCN through the retinohypothalamic tract: it suppresses the release of melatonin and shifts the clock later, so you feel sleepy later. Experiments in which people read from a light-emitting screen for a few hours before bed have found just this – less melatonin, and a later clock – though how much a screen matters depends on how bright it is and how long you look at it.")}
{mcq("wh-q-conn", "In Conn’s syndrome, which hormone is made in excess, and where?", [
    ("Cortisol, by the zona fasciculata", False, "No: too much cortisol is Cushing’s syndrome."),
    ("Aldosterone, by the zona glomerulosa", True, "Yes – usually by an adenoma, regardless of the renin–angiotensin system. Too much aldosterone retains Na+ and water and loses K+, so blood pressure rises and the plasma K+ concentration falls."),
    ("Adrenaline, by the medulla", False, "No: a tumour of the medulla that makes too much adrenaline is a phaeochromocytoma."),
])}
""")}
'''
    return chapter("s1-where", num, "Where is the clock?", "anatomy", "Where is the clock?", 20,
                   "Your master clock is a pair of tiny nuclei in the hypothalamus. Find where they are, follow the light "
                   "that sets them, and visit the glands they drive – in 3D, under the microscope and as molecules.", body)


# ---------------------------------------------------------------------------------------------------------------------
# the R typed for the student (kept out of the f-strings, which would have to escape their quotes)
R_READ = 'heart <- read.csv("~/data/heart-rate-24h.csv")'
R_HEAD = 'head(heart)'
R_SUM = 'summary(heart$hr)'
R_ONE = 'one <- subset(heart, subject == 16786)'
R_PLOT1 = 'plot(one$hour, one$hr, type = "b", xlab = "Hour of the day", ylab = "Heart rate (beats/min)")'
R_AGG = 'avg <- aggregate(hr ~ hour, data = heart, FUN = mean)'
R_PLOT2 = 'plot(avg$hour, avg$hr, type = "b", xlab = "Hour of the day", ylab = "Mean heart rate (beats/min)")'
R_MIN = 'avg$hour[which.min(avg$hr)]'
R_DAY = 'day <- mean(heart$hr[heart$hour >= 8 & heart$hour < 20], na.rm = TRUE)'
R_NIGHT = 'night <- mean(heart$hr[heart$hour < 6], na.rm = TRUE)'
R_DIFF = 'day - night'
R_BOX = 'boxplot(hr ~ hour, data = heart, xlab = "Hour of the day", ylab = "Heart rate (beats/min)")'
R_FIT = 'fit <- lm(hr ~ cos(2 * pi * hour / 24) + sin(2 * pi * hour / 24), data = heart)'
R_COEF = 'b <- unname(coef(fit))'
R_COS = 'c(mesor = b[1], amplitude = sqrt(b[2]^2 + b[3]^2), peak = (atan2(b[3], b[2]) * 12 / pi) %% 24)'
R_CURVE = 'curve(b[1] + b[2] * cos(2 * pi * x / 24) + b[3] * sin(2 * pi * x / 24), add = TRUE, col = "red")'


DATA_CREDIT = ('<p>The MIT-BIH Normal Sinus Rhythm Database (version 1.0.0), on PhysioNet, under the Open Data Commons '
               'Attribution License: Goldberger et al. (2000) <i>Circulation</i> 101: e215–e220; '
               '<a href="https://doi.org/10.13026/C2NK5R" target="_blank" rel="noopener">doi:10.13026/C2NK5R</a>. Its 18 '
               'people are 5 men aged 26 to 45 and 13 women aged 20 to 50, whose ECGs showed no significant arrhythmias. How '
               'the hourly heart rates were worked out is described in the repository (<code>starter/data/README.md</code>).</p>')


def ch_heart(num):
    body = f'''
<h2 id="ht-rr">From beats to a heart rate</h2>
<p>The data come from the <b>MIT-BIH Normal Sinus Rhythm Database</b>: long-term ECGs of 18 adults, each recorded for about a day as they went about their lives, with every beat labelled. A heart rate comes from the time between beats, the R–R interval: in beats per minute, it is 60 divided by the R–R interval in seconds. Measure one yourself first.</p>
{activity("Measure an R–R interval", [
    task("ht-open", f'Open an ECG {rec("ecg-normal@2,6", "show me")}: four seconds of a normal heartbeat.', auto="rec:open id=ecg-normal"),
    task("ht-cal", f'Choose the <b>Calipers</b> {rectool("calipers", "show me")} and drag from the peak of one R wave (the tall spike) to the peak of the next. The bar above the trace shows the interval (Δt) and the heart rate it gives.', auto="rec:measure id=ecg-normal dt>0.5 dt<1.2"),
])}
{q("ht-q-rr", "What heart rate does an R–R interval of 0.8 s give, in beats per minute?",
   "75 beats per minute: 60 ÷ 0.8 = 75. In the data set, the heart rate of each hour is 60 ÷ the mean of the R–R intervals in that hour – thousands of them (the column <code>n_beats</code> says how many).",
   accept="num:75±0.5", placeholder="beats per minute")}

<h2 id="ht-r">A day and a night, in R</h2>
{callout("info", "The first time", "<p>The first time you open RStudio, the workbench downloads R itself (about 30 MB), which can take a minute.</p>")}
<p>The file <code>~/data/heart-rate-24h.csv</code>, in your files, holds the heart rate of each of the 18 people for each hour of the day: 432 rows (18 people × 24 hours). Each <b>show me</b> button types a line of R into RStudio’s Console: press <kbd>Enter</kbd> to run it, and look at what it gives.</p>
{activity("Read the data, and plot one person’s day", [
    task("ht-read", f'Read the file into a table called <code>heart</code>: {rcode(R_READ)}', auto="r:input kind=rstudio line~heart-rate-24h.csv"),
    task("ht-head", f'Look at its first rows: {rcode(R_HEAD)}. Each row is one hour of one person: <code>subject</code> (the person), <code>sex</code>, <code>age</code>, <code>hour</code> (0 is midnight to 1 a.m.), <code>time</code>, <code>hr</code> (the heart rate, in beats per minute) and <code>n_beats</code>.', auto="r:input kind=rstudio line~head(heart"),
    task("ht-sum", f'Summarise the heart rates: {rcode(R_SUM)}. <code>heart$hr</code> means “the column <code>hr</code> of the table <code>heart</code>”. Some hours are <code>NA</code>, not available: the recording had ended, or it was too noisy.', auto="r:input kind=rstudio line~summary(heart"),
    task("ht-one", f'Pick out one person, a woman of 32: {rcode(R_ONE)}. Then plot her day: {rcode(R_PLOT1)}', auto="rstudio:plot"),
])}
{q("ht-q-one", "Describe her day. When was her heart rate lowest, and when was it highest?",
   "It was low and steady through the night (61–65 beats per minute, lowest at 05:00), jumped at 08:00 (from 63 to 77) – about when she got up – stayed higher through the day, highest in the afternoon (88 at 15:00), and fell through the evening, to 65 by 23:00. (The hour from 11:00 is missing.)")}
{activity("Everyone’s average day", [
    task("ht-agg", f'Work out the mean of the 18 people for each hour: {rcode(R_AGG)}. Then look at it: {rcode("avg")}. <code>aggregate()</code> splits the heart rates up by hour and takes the mean of each group, leaving out the NAs.', auto="r:input kind=rstudio line~aggregate("),
    task("ht-plot", f'Plot it: {rcode(R_PLOT2)}', auto="r:input kind=rstudio line~plot(avg"),
    task("ht-min", f'Which hour has the lowest mean? {rcode(R_MIN)}', auto="r:input kind=rstudio line~which.min"),
])}
{q("ht-q-low", "Which hour of the day has the lowest mean heart rate (0 to 23)?",
   "5, that is 05:00 to 06:00, at 64.4 beats per minute – although 03:00 and 04:00 are almost as low (64.6): the trough is in the small hours, when most people are asleep. The mean is highest in the late morning and early afternoon, at about 85 beats per minute.",
   accept="num:5", placeholder="the hour")}
{activity("Day against night", [
    task("ht-day", f'The mean heart rate by day, from 08:00 to 20:00: {rcode(R_DAY)}', auto="r:input kind=rstudio line~day <-"),
    task("ht-night", f'… and at night, from midnight to 06:00: {rcode(R_NIGHT)}', auto="r:input kind=rstudio line~night <-"),
    task("ht-diff", f'The difference: {rcode(R_DIFF)}. (<code>na.rm = TRUE</code> tells <code>mean()</code> to leave out the NAs: the mean of anything that includes an NA is NA.)', auto="r:input kind=rstudio line~day - night"),
])}
{q("ht-q-diff", "How much lower is the heart rate at night than by day, in beats per minute?",
   "About 17 beats per minute: 82.5 by day against 65.6 at night, so the heart rate is about a fifth lower at night. Every one of the 18 people was lower at night, by between 7 and 31 beats per minute.",
   accept="num:16.9±0.3", placeholder="beats per minute")}
{mcq("ht-q-mask", "Does this show that the heart rate has a circadian rhythm – one made by the body’s clock?", [
    ("Yes: any rhythm with a period of 24 hours must come from the clock", False, "No: a rhythm driven by the day’s events – sleeping at night, being active by day – also has a period of 24 hours."),
    ("No: a circadian rhythm would have a period of exactly 24 hours", False, "No: on its own, a clock runs with a period of about 24 hours, but in daily life light entrains it to exactly 24 – so the period alone can’t tell you."),
    ("Not by itself: these people slept at night and were active by day, and sleep, posture, meals and exercise change the heart rate directly. To see the clock’s own rhythm, you would have to hold people in constant conditions", True, "Yes. A daily rhythm can be driven by what happens each day as well as by the clock, and the effects of sleep and activity hide (mask) the clock’s own rhythm. Studies that keep people awake, lying still in dim light, with small regular meals (a constant routine) show that the heart rate does have a rhythm of its own – but a smaller one."),
])}
{optional(f"""
{activity("How people differ, and a curve for the rhythm", [
    task("ht-box", f'How much do people differ? {rcode(R_BOX)}: a box for each hour, showing the middle half of the 18 people (the box), the median (the line) and the range (the whiskers).', auto="r:input kind=rstudio line~boxplot("),
    task("ht-cos", f'Circadian biologists describe a rhythm by fitting a cosine curve to it (a <em>cosinor</em>). Fit one: {rcode(R_FIT)}. Keep its coefficients: {rcode(R_COEF)}. Then work out the curve’s mean level (its <em>mesor</em>), its amplitude and the hour of its peak: {rcode(R_COS)}', auto="r:input kind=rstudio line~atan2("),
    task("ht-curve", f'Plot the means again ({rcode(R_PLOT2, "show me")}) and draw the curve over them: {rcode(R_CURVE)}', auto="r:input kind=rstudio line~curve("),
])}
{q("ht-q-cos", "What are the amplitude of the rhythm, and the time of its peak? How well does a cosine curve describe it?",
   "The mesor is 75.3 beats per minute, the amplitude 10.1 beats per minute (the curve swings 10 above and 10 below the mesor), and the peak – the <em>acrophase</em> – is at 14.7 hours, about 14:40. A cosine is only a rough fit: the real rhythm isn’t symmetrical. It jumps up in the morning, when people get up, and falls more slowly through the evening.")}
""")}
{callout("info", "Where the data come from", DATA_CREDIT)}
'''
    return chapter("s1-heart", num, "Your heart’s daily rhythm", "recorder", "Your heart’s daily rhythm", 20,
                   "Your heart beats more slowly at night. With real 24-hour ECGs from 18 people, see the rhythm for "
                   "yourself – in a few lines of R that are typed for you.", body)


# ---------------------------------------------------------------------------------------------------------------------
CRITERIA = [
    ('Addressing the question', 'How relevant the content of the essay is to the question or title set.',
     'It selects relevant material: knowledge, concepts, interpretations, models and others’ views.',
     'It makes clear, throughout, how the material is relevant to the question.'),
    ('Using evidence', 'The use of material from outside sources: research findings, facts, examples, quotations.',
     'It includes information from sources that backs up its points.',
     'It interprets the evidence, and shows explicitly how it supports a more general claim.'),
    ('Developing argument', 'Building a coherent, convincing case for a point of view: an analytical path from a starting point to a conclusion.',
     'It takes a position on the issues the title raises.',
     'It develops its argument throughout, each part building on the last.'),
    ('Critical evaluation', 'Judging the value, significance, strengths and weaknesses of something: a finding, a theory, a method, an interpretation.',
     'It makes evaluative points about the strengths and weaknesses of what it discusses.',
     'It explains and justifies its evaluations, systematically.'),
    ('Structuring', 'The arrangement of the essay into paragraphs.',
     'It has a clear introduction and conclusion, and each paragraph of the main body has one main point.',
     'The order of its paragraphs follows the development of the argument.'),
    ('Use of language', 'Words, grammar and punctuation suited to the purpose.',
     'It is free of errors of spelling, punctuation and grammar.',
     'It uses an academic style, in the register of the subject.'),
]


def criteria_cards():
    cards = ''.join(f'<div class="crit"><h3><span class="cn">{i}</span>{t}</h3><p>{what}</p>'
                    f'<p class="gb"><b>Good:</b> {good}</p><p class="gb"><b>Better:</b> {better}</p></div>'
                    for i, (t, what, good, better) in enumerate(CRITERIA, 1))
    return f'<div class="crit-grid">{cards}</div>'


SAMPLE = [
    'Circadian rhythms are really interesting and are found in loads of animals, as well as in plants and even some bacteria. A circadian rhythm is a rhythm with a period of about 24 hours. In this essay I will talk about circadian rhythms.',
    'Circadian rhythms are made by a feedback loop of genes and proteins. In mammals, CLOCK and BMAL1 switch on the <i>Per</i> and <i>Cry</i> genes, and the PER and CRY proteins go back into the nucleus and switch their own genes off. The master clock is the suprachiasmatic nucleus (SCN) in the hypothalamus, which gets information about light from retinal ganglion cells that contain melanopsin.',
    'Michel Siffre lived in a cave for 63 days in 1962. Shift workers have more health problems than other people. Blood pressure is higher in the morning, and heart attacks are more common then.',
    'Circadian rhythms obviously evolved because they help animals to survive. For example, cortisol goes up in the morning to get us ready to wake up, and melatonin goes up at night.',
    'In conclusion, circadian rhythms are found in lots of animals and there are lots of reasons why they have them, so they are very important.',
]

BETTER = [
    ('Circadian rhythms are rhythms with a period of about 24 hours that persist even when an animal is kept from every cue about the time of day. They are found throughout the animal kingdom, as well as in plants, fungi and some bacteria. This essay argues that animals have them chiefly because they allow the body to anticipate the predictable changes of day and night, rather than respond to each one after it has happened. It shows first that the rhythms are generated within the body, then how they prepare it for the day, and finally weighs the evidence that they help animals to survive.',
     ['Structuring: an introduction that says where the essay is going', 'Developing argument: a position, from the start']),
    ('Because circadian rhythms are generated within the body, they can act ahead of the day. In 1962 Michel Siffre spent 63 days in a cave, without daylight or clocks: he went on sleeping and waking in a regular cycle, but one a little longer than 24 hours, so it cannot have been driven by the day outside. The rhythm is generated by a negative feedback loop of genes and proteins: in mammals, CLOCK and BMAL1 switch on the <i>Per</i> and <i>Cry</i> genes, and the PER and CRY proteins, hours later, return to the nucleus and switch their own genes off, so that each cycle takes about a day. Light reaching the suprachiasmatic nucleus (SCN) of the hypothalamus resets this clock each day, keeping it in step with the Sun.',
     ['Using evidence: Siffre’s cave, used to support a claim', 'Addressing the question: the mechanism, linked to why']),
    ('An internal clock lets the body be ready before it is needed. Plasma cortisol rises in the early morning, before waking, mobilising glucose for the activity of the day, and arterial pressure rises at the same time. A response triggered only by waking would come too late, because hormones take time to be made and to act: the clock works as a form of feed-forward control, preparing the body for a change instead of correcting it afterwards.',
     ['Addressing the question', 'Developing argument: it builds on paragraph 2']),
    ('That this anticipation helps animals to survive is often assumed, and there is some evidence for it. When strains of cyanobacteria with clocks of different periods were grown together, the strain whose period matched the light–dark cycle outgrew the others (Ouyang et al., 1998); and chipmunks returned to the wild after damage to the SCN were killed by predators more often than intact animals (DeCoursey et al., 2000). Such studies are few, however, and they come from only a handful of species: the case for anticipation in general is strong, but weaker for any one rhythm in any one animal.',
     ['Critical evaluation: the evidence weighed', 'Using evidence: sourced and cited']),
    ('Animals therefore have circadian rhythms chiefly because a clock within the body lets them prepare for the predictable events of each day, rather than respond to them late. The rhythms persist without cues, as Siffre’s cave showed; they are kept in time by light; and although the direct evidence that they aid survival comes from only a few species, it points the same way.',
     ['Structuring: a conclusion that draws the points together', 'Use of language: formal and precise throughout']),
]


def sample_essay():
    ps = ''.join(f'<p><span class="pn">{i}</span>{t}</p>' for i, t in enumerate(SAMPLE, 1))
    return f'<div class="sample-essay"><h3>Why do animals have circadian rhythms?</h3>{ps}</div>'


def better_essay():
    ps = ''.join(f'<p><span class="pn">{i}</span>{t}<br>' + ''.join(f'<span class="ctag">{x}</span>' for x in tags) + '</p>'
                 for i, (t, tags) in enumerate(BETTER, 1))
    return (f'<details class="better"><summary>Read a better version, and what each paragraph does</summary>'
            f'<div class="sample-essay"><h3>Why do animals have circadian rhythms?</h3>{ps}</div>'
            f'<p class="credit">About 450 words: a little shorter than most 40-minute essays. Ouyang, Y. et al. (1998) <i>PNAS</i> 95: 8660–8664; DeCoursey, P.J. et al. (2000) <i>Journal of Comparative Physiology A</i> 186: 169–180.</p></details>')


def ch_marking(num):
    body = f'''
<p>When your supervisor gives you feedback on an essay, it is against six <b>core criteria</b>. Each describes a quality of a good essay, and what makes a better one – and they are the qualities examiners look for too.</p>
{criteria_cards()}
<p class="credit">The core criteria and the comments below are from the essay feedback form of <i>Assessment Plus: using assessment criteria to support student learning</i>, a HEFCE-funded consortium project (assessmentplus.net).</p>

<h2 id="mk-example">An example essay</h2>
<p>Here is a short essay on a question from this week’s lectures. Its facts are right – but it has a problem under each of the six criteria. Read it, and then decide which comment from the feedback form fits each part best.</p>
{sample_essay()}

<h2 id="mk-comments">What comments would it get?</h2>
{mcq("mk-q1", "<b>Addressing the question.</b> Paragraph 2 is accurate. Which comment fits it best?", [
    ("The material you use is not relevant to this topic", False, "Not so: the clock’s machinery is certainly part of the topic of circadian rhythms."),
    ("The material you use is relevant to this general topic, but you don’t make clear how it is relevant to this specific question", True, "Yes. The paragraph explains how circadian rhythms are made, but the title asks why animals have them – and it never says what the one has to do with the other. However accurate it is, as it stands it earns little credit."),
    ("Good, you have made it very clear how the material you use is related to the specific issues that are the focus of the essay", False, "Not yet: the paragraph never links the mechanism to why animals have rhythms."),
], model="<b>To put it right</b>, make the mechanism answer the question: <i>“Because the rhythm is generated within the body – by a negative feedback loop of genes and proteins that takes about a day to go round – the body can prepare for dawn before it comes, rather than respond once the light has arrived.”</i>")}
{mcq("mk-q2", "<b>Using evidence.</b> Paragraph 3 mentions Siffre’s cave, shift workers and the morning rise in blood pressure. Which comment fits it best?", [
    ("You don’t provide enough research findings, data, quotations or other sourced material as evidence for your claims", False, "Not quite: there is evidence here. The trouble is that none of it is linked to anything."),
    ("You provide some potential evidence, but the link with your claims could be clearer or developed more", True, "Yes. Siffre’s cave is good evidence – but evidence for what? The paragraph never says. And “shift workers have more health problems” is a claim that needs evidence of its own."),
    ("Good, you use evidence clearly and convincingly to support your claims", False, "Not yet: the facts are listed, but none of them is used to support a point."),
], model="<b>To put it right</b>, say what each piece of evidence shows: <i>“The rhythms are generated within the body: in 1962 Michel Siffre spent 63 days in a cave, without daylight or clocks, and he went on sleeping and waking in a regular cycle – but one a little longer than 24 hours, so it cannot have been driven by the day outside.”</i> Then either support the claim about shift workers, with a source, or leave it out.")}
{mcq("mk-q3", "<b>Developing argument.</b> Read the conclusion, paragraph 5, and think about the essay as a whole. Which comment fits best?", [
    ("Your essay does not contain a point of view or position in relation to the title or question", True, "Yes. The essay never says why animals have circadian rhythms: “there are lots of reasons” is not a position. Without one, the paragraphs can’t build towards anything."),
    ("Your essay contains some expression of a position, which could have been more explicitly developed and justified", False, "Close – but the essay doesn’t really take a position at all: it never says what the reasons are, let alone which matters most."),
    ("Good, you have established a clear position in relation to the question, and developed that position throughout the essay", False, "No: there is no position to develop."),
], model="<b>To put it right</b>, decide on your answer before you write, and state it early: <i>“Animals have circadian rhythms chiefly because they let the body anticipate the predictable changes of each day.”</i> Then make each paragraph a step towards it – the rhythm is made within the body; how it prepares the body; how good the evidence is that this helps – and end with a conclusion that draws those steps together.")}
{mcq("mk-q4", "<b>Critical evaluation.</b> Paragraph 4 says that circadian rhythms “obviously evolved because they help animals to survive”. Which comment fits best?", [
    ("Your essay is too descriptive – there is not enough assessment of the value or significance of what you describe", False, "Partly – but paragraph 4 does make a judgement. The trouble is that it gives no reasons for it."),
    ("Your evaluative points could be more extensive, explicit, systematic, reasoned or justified", True, "Yes. “Obviously” asserts a judgement without justifying it. Whether rhythms help animals survive is a question that biologists have tested, and the evidence can be weighed."),
    ("Good, you have made some systematic, reasoned and justified assessments of value", False, "Not yet: the claim is asserted, not justified."),
], model="<b>To put it right</b>, weigh the evidence: <i>“When strains of cyanobacteria with clocks of different periods were grown together, the strain whose period matched the light–dark cycle outgrew the others (Ouyang et al., 1998); and chipmunks returned to the wild after damage to the SCN were killed by predators more often than intact animals (DeCoursey et al., 2000). Such studies are few, however, and come from only a handful of species.”</i>")}
{mcq("mk-q5", "<b>Structuring.</b> Paragraph 1 is the introduction. Which comment fits it best?", [
    ("Some of your paragraphs do not focus on one main idea each, or are too short", False, "True of paragraph 3, which lists three unconnected facts – but it isn’t the problem with the introduction."),
    ("Your introduction could do more to let the reader know how the essay will deal with the issues", True, "Yes. “In this essay I will talk about circadian rhythms” tells the reader nothing about the answer the essay will give, or how it will get there."),
    ("Your conclusion could do more to give the essay an ending which brings together your various points", False, "That is true of paragraph 5 – but this is the introduction."),
], model="<b>To put it right</b>, define the terms and say where the essay is going: <i>“Circadian rhythms are rhythms with a period of about 24 hours that persist without cues from the environment. This essay argues that animals have them chiefly because they allow the body to anticipate the day: it shows first that the rhythms are generated within the body, then how they prepare it for the day, and finally weighs the evidence that they help animals to survive.”</i>")}
{mcq("mk-q6", "<b>Use of language.</b> Look at the wording of paragraphs 1 and 4: “really interesting”, “loads of”, “get us ready”. Which comment fits best?", [
    ("Your essay has too many spelling, grammar or punctuation errors", False, "No: there are no errors of that kind."),
    ("In some passages your writing makes the meaning unclear or difficult to follow", False, "No: the meaning is perfectly clear."),
    ("Your meaning is clear, but your language is too colloquial", True, "Yes. “Really interesting”, “loads of” and “get us ready” belong in conversation, not in a scientific essay."),
    ("Make sure you stick to the correct citation conventions", False, "Not the main problem here (although Siffre’s study could be cited more carefully)."),
], model="<b>To put it right</b>, use the plain, precise language of science: <i>“Circadian rhythms are found throughout the animal kingdom, as well as in plants, fungi and some bacteria”</i>; <i>“plasma cortisol rises in the early morning, before waking, preparing the body for activity.”</i>")}

<h2 id="mk-better">A better version</h2>
<p>The same essay, rewritten to meet each criterion. It isn’t the only good answer – but notice that it takes a position at the start, that every paragraph is a step towards it, and that its evidence is used, and weighed, rather than listed.</p>
{better_essay()}
{callout("tip", "Use the criteria on your own essay", "<p>In the last few minutes of your 40, read your essay against the six criteria. Does every paragraph answer the question? Is each example linked to the point it supports? Is there a position, built on through the essay? Do you weigh your examples, rather than only describe them? Does each paragraph make one point? Is the language formal and precise?</p>")}
'''
    return chapter("s1-marking", num, "How essays are marked", "exam", "How essays are marked", 15,
                   "Your supervisor gives feedback on essays against six core criteria. See what each one means, and how "
                   "it plays out in an example essay – with the comments it would get, and how to put them right.", body)


# ---------------------------------------------------------------------------------------------------------------------
KOHLER = ('Few laboratory creatures have had such a spectacularly successful and productive history as <i>Drosophila</i>. '
          'It first entered laboratories about 1900, revealed its talent for experimental genetics to Thomas Hunt Morgan and '
          'his students at Columbia University in the early 1910s, and after some ups and downs in status is still going '
          'strong almost a century later.')
KOHLER_REF = 'Kohler, R.E. (1994) <i>Lords of the Fly: Drosophila Genetics and the Experimental Life</i>. The University of Chicago Press.'
VERSIONS = [
    'Despite some ups and downs in status, nearly a century after the fly revealed its talent to Thomas Hunt Morgan and his students, <i>Drosophila</i> genetics research continues its spectacularly successful history (Kohler, 1994).',
    'No model organism has been so amazingly useful and effective as the fruit fly. The fly came on the scene as an experimental tool at the beginning of the 20th century, was adopted by Thomas Hunt Morgan and his Columbia pupils at Columbia University around 1910, and (despite some fluctuations in attention paid to it) is still a widely used experimental system (Kohler 1994).',
    '<i>Drosophila</i> is model organism with a rich and useful legacy. Upon arriving on the scene at the turn of the century, the fruit fly soon became the organism of choice for Thomas Hunt Morgan and his Columbia University pupils. Despite fluctuations in status, fly research is still central to the progress of genetics (Kohler, 1994).',
    'Thomas Hunt Morgan and colleagues at Columbia University were among the first to use the fruit fly <i>Drosophila</i> as a model organism, adopting it as an experimental system around 1910. Since then, the popularity of the fly has waxed and waned somewhat, but the breadth and depth of current research indicates that <i>Drosophila</i> continues its legacy as an incredibly important research tool (Kohler, 1994).',
]
PLAG_OPTS = ['Unacceptable: it copies phrases without quotation marks',
             'Unacceptable: it copies the structure of the original’s sentences',
             'Unacceptable: it copies the structure of the original’s paragraph',
             'Acceptable']
PLAG_WHY = [
    ['Yes. “Some ups and downs in status”, “revealed its talent … to Thomas Hunt Morgan and his students” and “spectacularly successful … history” are Kohler’s own words. Quotation marks would avoid trouble, but it would be much better to write in your own words.',
     'Look at the words themselves first: whole phrases are Kohler’s, word for word.',
     'It does reorder the ideas – but look at the words: whole phrases are Kohler’s, word for word.',
     'No: phrases such as “some ups and downs in status” and “spectacularly successful” are Kohler’s own words, with no quotation marks. A reference doesn’t make copied words your own.'],
    ['Hardly any of the words are Kohler’s: the problem is a subtler one.',
     'Yes. Each sentence follows Kohler’s, part by part, with the words swapped for others: “Few laboratory creatures have had such a … history as Drosophila” becomes “No model organism has been so … as the fruit fly”. (The paragraph follows his as well.)',
     'True, it does – but look inside each sentence: each one copies the shape of Kohler’s, phrase by phrase.',
     'No: the words are new, but each sentence is Kohler’s sentence with its words swapped for others. It is still his writing.'],
    ['No: the words are the writer’s own.',
     'No: its sentences are built differently from Kohler’s.',
     'Yes. The sentences are new, but the paragraph follows Kohler’s idea by idea, in the same order: a remarkable history; arriving about 1900; taken up by Morgan and his students; ups and downs; still going strong. It is his paragraph, rewritten.',
     'No: each sentence is new, but the paragraph takes Kohler’s ideas in exactly his order – his argument, in other words.'],
    ['No: the only words it shares with Kohler are names and plain terms that anyone would use.',
     'No: its sentences are built in their own way.',
     'No: it starts from a different point, puts the ideas in its own order and adds a judgement of its own.',
     'Yes. It starts from a different point (Morgan and his colleagues), puts the ideas in its own order and its own words, and adds its own judgement (the breadth and depth of current research) – and it still credits Kohler, because the ideas are his.'],
]
PLAG_MODEL = [
    'The phrases taken from Kohler: “Despite <mark>some ups and downs in status</mark>, nearly <mark>a century</mark> after the fly <mark>revealed its talent</mark> <mark>to Thomas Hunt Morgan and his students</mark>, <i>Drosophila</i> genetics research continues its <mark>spectacularly successful</mark> <mark>history</mark> (Kohler, 1994).”',
    '<table class="align"><tr><th>Kohler</th><th>Version 2</th></tr>'
    '<tr><td>Few laboratory creatures have had such a spectacularly successful and productive history as <i>Drosophila</i>.</td><td>No model organism has been so amazingly useful and effective as the fruit fly.</td></tr>'
    '<tr><td>It first entered laboratories about 1900,</td><td>The fly came on the scene as an experimental tool at the beginning of the 20th century,</td></tr>'
    '<tr><td>revealed its talent for experimental genetics to Thomas Hunt Morgan and his students at Columbia University in the early 1910s,</td><td>was adopted by Thomas Hunt Morgan and his Columbia pupils at Columbia University around 1910,</td></tr>'
    '<tr><td>and after some ups and downs in status is still going strong almost a century later.</td><td>and (despite some fluctuations in attention paid to it) is still a widely used experimental system.</td></tr></table>',
    'The ideas, in Kohler’s order and in version 3’s: a remarkable history (“a rich and useful legacy”); arriving about 1900 (“at the turn of the century”); taken up by Morgan and his students (“the organism of choice for Thomas Hunt Morgan and his Columbia University pupils”); ups and downs (“despite fluctuations in status”); still going strong (“still central to the progress of genetics”).',
    'Notice that it still gives the reference: an idea taken from a source needs one, even when every word is your own.',
]


def ch_plag(num):
    versions = ''
    for i, v in enumerate(VERSIONS):
        versions += f'<blockquote class="passage"><span class="pv">Version {i + 1}</span>{v}</blockquote>\n'
        opts = [(PLAG_OPTS[k], k == i, PLAG_WHY[i][k]) for k in range(4)]
        versions += mcq(f'pl-q{i + 1}', f'Is version {i + 1} acceptable? If not, what is wrong with it?', opts, model=PLAG_MODEL[i]) + '\n'
    body = f'''
<p>The University counts as plagiarism anything you submit as your own that comes, in part or in whole, from the work of others without due acknowledgement – whether or not you meant to deceive. Copying a sentence is the obvious case. Paraphrasing too closely is the one that catches people out.</p>

<h2 id="pl-orig">The original</h2>
<blockquote class="passage orig"><span class="pv">The original</span>{KOHLER}<span class="src">{KOHLER_REF}</span></blockquote>

<h2 id="pl-versions">Four paraphrases</h2>
<p>Each of these was written by someone who had read the passage, and each gives a reference. Which of them are acceptable, and what is wrong with the others?</p>
{versions}
{mcq("pl-q-quote", "You want to use Kohler’s phrase “a spectacularly successful and productive history”. What should you do?", [
    ("Change a word or two – “a remarkably successful and productive history” – and give the reference", False, "No: that is still Kohler’s phrase, too close to be your own."),
    ("Use it as it is, with the reference at the end of the paragraph", False, "No: a reference credits the idea, but words you have copied also need quotation marks."),
    ("Put it in quotation marks and give the reference: <i>Drosophila</i> has had “a spectacularly successful and productive history” (Kohler, 1994)", True, "Yes: copied words need quotation marks as well as a reference. In science, though, quotations are rare: you would usually put the idea in your own words, and cite the source."),
])}
<p class="credit">The exercise is the University’s (<a href="http://www.biology.cam.ac.uk/exams/plagiarism" target="_blank" rel="noopener">www.biology.cam.ac.uk/exams/plagiarism</a>). Kohler’s book is a history of Thomas Hunt Morgan’s “fly room” – and fifty years after it, <i>Drosophila</i> gave biology its first clock gene, <i>period</i> (chapter 1).</p>

<h2 id="pl-paste">Why Supervision work won’t let you paste</h2>
{callout("warn", "No pasting from anywhere else", f"<p>In the online exam you can’t paste in text copied from outside the exam, and Supervision work is the same: text copied from a website, your notes, an AI tool or these instructions won’t go into your essay. (You can still copy and paste within your own essay, to move a sentence or a paragraph.)</p><p>So every word of the essay you hand in is one you typed – which is the best protection against plagiarising by accident. When you use someone’s finding or idea, put it in your own words and say whose it is: “Konopka and Benzer (1971) found…”. You will see it for yourself when you start your essay. {goto('s1-write', 'go to your essay')}</p>")}
'''
    return chapter("s1-plag", num, "Plagiarism", "exam", "Plagiarism, and why you can’t paste", 10,
                   "Using someone else’s words, ideas or structure without saying so is plagiarism – even when you have "
                   "changed the words. Try the University’s exercise: which of four paraphrases of the same passage is "
                   "acceptable?", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_write(num):
    body = f'''
<p class="essay-title">“{ESSAY}”</p>

<h2 id="es-why">Why write it like this?</h2>
<p>Your exams are written on a computer, in an online exam system: you type your answers in one sitting, against the clock, without notes, and you can’t paste anything in. Supervision work is set up in the same way. Writing your supervision essays like this makes the exam familiar long before the summer: you find out how much you can plan and write in 40 minutes, and what it is like to do it without your notes. And because your supervisor sees the essay you can write in that time, the feedback is about the essay you would actually write in the exam – not one polished over a week. As in the exam, you submit it when you have finished, and it is handed in from the same page: here, you upload it to {SUPERVISOR}’s Dropbox.</p>

<h2 id="es-before">Before you start</h2>
<ul>
<li>Read how essays are marked {goto("s1-marking", "chapter 4")}, and about plagiarism {goto("s1-plag", "chapter 5")}.</li>
<li>Revise the lectures first if you like. Then put your notes away, and find about 45 minutes when you won’t be interrupted.</li>
<li>Have the <b>hand-in password</b> that {SUPERVISOR} gave you ready, for handing it in at the end. It isn’t on this site.</li>
<li>There is no time limit, but give yourself about <b>40 minutes</b>, as in the exam. The clock at the top of the paper counts the time you spend writing, and tells you when you reach 40 minutes. If you haven’t finished by then, write your conclusion – or carry on if you need to: the clock shows how long you took.</li>
<li>Spend the first five minutes planning. What is your answer to the question? Which examples support it, and in what order will you make your points? You can plan on paper, or in the box itself, and delete the plan before you submit.</li>
</ul>
{activity("Write it, and hand it in", [
    task("es-open", f'Open the essay {exam("s1-essay", "show me")} and read its first page.', auto="exam:open paper=s1-essay"),
    task("es-start", 'When you are ready to write, press <b>Start</b>. If you haven’t given your name, it asks for it, for the top of your essay.', auto="exam:start paper=s1-essay", check="paper:s1-essay.started"),
    task("es-paste", 'Before you write, try it: copy a sentence of these instructions (<kbd>Ctrl</kbd>+<kbd>C</kbd>, or <kbd>⌘</kbd>+<kbd>C</kbd> on a Mac) and paste it into the box (<kbd>Ctrl</kbd>+<kbd>V</kbd>). It won’t go in.', auto="exam:paste paper=s1-essay refused=true"),
    task("es-write", 'Plan, then write: an introduction that says what your essay will argue, paragraphs that each make one point, with examples, and a conclusion that draws them together.', auto="exam:words paper=s1-essay words>299"),
    task("es-submit", 'Go to the submission page (the ✓ tile at the bottom right), check your essay, and submit it.', auto="exam:submit paper=s1-essay", check="paper:s1-essay.submitted"),
    task("es-word", 'Hand it in, on the page that follows. First, <b>Download the Word document</b>: it goes to your Downloads folder. (The first page of the paper offers these steps again later.)', auto="exam:download paper=s1-essay format=docx", check="paper:s1-essay.downloaded"),
    task("es-upload", f'Then <b>Open the hand-in page</b>, {SUPERVISOR}’s Dropbox, in a new tab. Enter the password he gave you, press <b>Add files</b> ▸ <b>Files from computer</b> and choose the Word document, type your name and email address, and press <b>Upload</b>.', auto="exam:handin paper=s1-essay step=opened", check="paper:s1-essay.opened"),
    task("es-send", 'When Dropbox says <b>Finished uploading</b>, come back to this tab and press <b>I have handed it in</b>.', auto="exam:handin paper=s1-essay step=confirmed", check="paper:s1-essay.handedIn"),
])}
{callout("info", "The hand-in page", f"<p>It is {SUPERVISOR}’s Dropbox file request for the year’s supervision work, <i>BMS Supervision work 26-27</i>: you don’t need a Dropbox account. It asks first for the password, which {SUPERVISOR} gives you – keep it to yourself – and then for your file, your name and your email address. If it won’t open, or the upload fails, tell {SUPERVISOR}, and send him the Word document another way.</p>")}
{callout("info", "After you have handed it in", "<p><b>Review my answers</b>, on the page that follows the submission, shows the ground a good answer covers. Read it after you have handed your essay in, and note what you would add or change: that is what the supervision is for.</p><p>Your essay is kept in this browser, in Files → <code>essays</code>. On another computer it won’t be there, so download it before you leave.</p>")}
{q("es-q-next", "Once you have read the guidance: what is one thing you would do differently in your next essay?",
   "Your own answer is what matters here: bring it to your supervision. It might be about the content (an example you missed, or one you described without linking it to the question), about the argument (a clearer position from the start), or about the time (more planning, or a shorter introduction).")}
'''
    return chapter("s1-write", num, "Write your essay", "exam", "Write your essay, and hand it in", 45,
                   f"The one piece of work to hand in this week. Write it in Supervision work, as you will write in the "
                   f"online exam; then hand it in from the same page, uploading it to {SUPERVISOR}’s Dropbox.", body)


# ---------------------------------------------------------------------------------------------------------------------
SAQS = [
    'Define ‘feedforward’ and ‘negative feedback’, and explain how these processes relate to thirst.',
    'What are the ways in which solutes can cross cell membranes, and how do they differ?',
    'What are the theoretical problems that you might encounter in designing and interpreting an experiment to investigate the effects of a hormone on the body?',
    'How is the pituitary gland controlled?',
    'What is Addison’s disease? What is Conn’s syndrome?',
]
REVISION = [
    'How does multicellularity affect physiology?',
    'Discuss the relative merits of hormonal versus electrical signals.',
    'Discuss the role of the hypothalamus in homeostasis.',
    'Compare and contrast the roles of adrenaline and cortisol.',
]


def ch_more(num):
    saqs = ''.join(f'<li>{s}</li>' for s in SAQS)
    rev = ''.join(f'<li>{s}</li>' for s in REVISION)
    body = f'''
<h2 id="mo-saq">Short-answer questions</h2>
<p>A short-answer question (SAQ) asks for a focused answer in a few minutes: the definitions, the key points and an example or two, with no introduction or conclusion. These five go with this week’s lectures:</p>
<ol class="titles">{saqs}</ol>
<p>They are a paper of their own in Supervision work {exam("s1-saqs", "open them")}, with no time limit: about 10 minutes for each is a good aim, and you can answer as many as you like. After you submit, <b>Review my answers</b> shows what a good answer covers.</p>

<h2 id="mo-rev">Essay titles for revision</h2>
<p>Note these down: they go with this week’s lectures, and they are the kind of title you could meet in the exam.</p>
<ol class="titles">{rev}</ol>
<p>Planning an answer to each – your argument, your examples and their order – is good revision. Or write one in Supervision work {exam("s1-revision", "open them")}, in 40 minutes, as practice; after you submit, the guidance shows the ground each title covers.</p>
{optional(activity("If you want the practice", [
    task("mo-saq", 'Answer one or more of the short-answer questions, and submit them.', auto="exam:submit paper=s1-saqs"),
    task("mo-plan", 'Plan an answer to one of the revision titles: your position in a sentence, and the three or four points, with examples, that would support it.'),
]), title='Practice')}
'''
    return chapter("s1-more", num, "More practice", "exam", "More practice: short answers and revision", None,
                   "Optional: five short-answer questions on this week’s lectures, and four more essay titles to note for "
                   "revision. Only the essay is to be handed in.", body)


def ALL():
    order = [ch_week, ch_clock, ch_where, ch_heart, ch_marking, ch_plag, ch_write, ch_more]
    return [f(str(i)) for i, f in enumerate(order)]
