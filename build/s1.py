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


HANDIN_LINE = f'Once you’ve submitted it, <b>hand it in</b> from the same page before your supervision. You’ll need the hand-in password that <b>{SUPERVISOR}</b> gives you, and your essay then goes straight to his Google Drive.'


def handin_box(buttons=True):
    """the essay to hand in, as the first thing the student sees"""
    b = (f'<p class="hb-acts">{goto("s1-write", "how to write it and hand it in")} {exam("s1-essay", "open the essay")}</p>'
         if buttons else '')
    return f'''<div class="handin-box">
  <div class="hb-k">To hand in this week</div>
  <p class="hb-title">“{ESSAY}”</p>
  <ul>
    <li>You write the essay in <b>Supervision work</b>, the first tab of the workbench, in the same way you’ll write essays in the online exam. That means typing it in one sitting, without your notes, and without pasting anything in.</li>
    <li>There’s no time limit, but try to keep to about <b>40 minutes</b>.</li>
    <li>{HANDIN_LINE}</li>
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
<li>Start with <b>three short exercises</b>. They take about an hour altogether, and they’ll give you examples to use in your essay. In chapter 1 you build a clock out of negative feedback in <b>Diagrams</b>. In chapter 2 you find the clock, and the glands it controls, in <b>Anatomy</b>, the <b>Microscope</b> and <b>Molecules</b>. In chapter 3 you look at your heart’s daily rhythm, using real recordings and <b>R</b>. {goto("s1-clock", "start")}</li>
<li>Before you write, read chapters 4 and 5, on <b>how essays are marked</b> and on <b>plagiarism</b>. Together they take about 25 minutes. {goto("s1-marking", "go there")}</li>
<li>Then <b>write your essay</b> and hand it in (chapter 6, about 45 minutes). {goto("s1-write", "go there")}</li>
<li>If you’d like more practice, chapter 7 has five short-answer questions and four more essay titles to note down for revision. These are optional. {goto("s1-more", "go there")}</li>
</ol>
{activity("Before you start", [
    task("wk-name", 'Add your name by clicking <b>Your name</b> at the top of the page. It goes at the top of the essay you hand in, and every supervision’s page uses it. It’s only kept in this browser.', check="named"),
])}

<h2 id="wk-why">Why the clock?</h2>
<p>Your body isn’t the same at four in the morning as it is at four in the afternoon. Your core temperature, blood pressure and heart rate rise and fall over the course of every day, and so do the levels of cortisol and melatonin in your blood. All of this is driven by a master clock in your hypothalamus, the <b>suprachiasmatic nucleus</b> (SCN). The clock itself is built from negative feedback. It’s reset every day by light, and it works through the autonomic nervous system, the pituitary and hormones. That means it touches every one of this week’s lectures, which is why we’re using it to tie them together.</p>

<h2 id="wk-how">How this page works</h2>
<ul>
<li>The instructions are on the left and the workbench is on the right, with a different tool in each of its tabs. You can drag the divider between them to change their widths, and the button at the top left hides the instructions.</li>
<li>The steps in each activity tick themselves off as you do them (<span class="auto-tag">✓ spotted</span>), and you can also tick them yourself. Buttons like {bench("exam", "show me")} do something for you, such as opening a diagram, a slide or a recording, or typing a line of R.</li>
<li>Have a go at each question before you look at its <b>model answer</b> (<b>Show answer</b>). The multiple-choice questions tell you straight away whether you’re right, and why.</li>
<li>Sections headed <b>If you have time</b> are extras, and they don’t count towards finishing the page.</li>
<li>Everything you do is saved in this browser, on this computer. You can download your answers with <b>My answers</b> at the top of the page, and your essay downloads as a Word document.</li>
<li>If you haven’t used the workbench before, the <a href="workbench.html" target="_blank" rel="noopener">workbench guide</a> shows you how each of its tabs works.</li>
</ul>
'''
    return chapter("s1-week", num, "This week", "exam", "Supervision 1: feedback, hormones and the hypothalamus", 5,
                   "This week’s lectures cover homeostasis and feedback, moving things around, hormones, the hypothalamus "
                   "and pituitary, and the adrenal gland. We’ll come at all of them through one example, the body’s daily "
                   "clock. Below you’ll find the essay to hand in, and a few short exercises to go with it.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_clock(num):
    body = f'''
<h2 id="ck-thirst">Thirst: a slow loop, and feed-forward</h2>
<p>In the first lecture you met a problem with drinking. When you sweat, the osmolarity of your extracellular fluid (ECF) rises. Osmoreceptors in the hypothalamus detect the change, so you feel thirsty and drink. But water takes time to be absorbed from the gut, and until it has been, the osmoreceptors keep telling you that you need more.</p>
{activity("Run the thirst loop", [
    task("ck-th-open", f'Open the diagram {flow("example:thirst", "show me")}. The comparator (Σ) compares the osmolarity of the ECF with its set point of 300 mOsm/L, and the difference between them is what makes you thirsty.', auto="flow:open example=thirst"),
    task("ck-th-run", f'Press <b>Run</b> {flowrun("show me")} and watch <i>ECF osmolarity</i> in the graphs below the diagram. Dragging the slider under the graphs shows you the diagram at any moment of the run.', auto="flow:run name~thirst blocked>0"),
    task("ck-th-ff", 'The grey arrow labelled <i>feed-forward</i>, which comes from receptors in the mouth and stomach, is blocked at the moment. Right-click it (or press and hold it), choose <b>Unblock this arrow</b>, and run the diagram again.', auto="flow:run name~thirst blocked=0"),
])}
{q("ck-q-thirst", "With negative feedback alone, what happened to the osmolarity once you started to drink, and why? What did the feed-forward arrow change?",
   "With negative feedback alone, the osmolarity overshot. Sweating had raised it to about 309 mOsm/L. Once you started drinking, it fell to about 291, roughly as far below the set point as it had been above it, before settling back at 300. The water takes about 15 minutes to be absorbed, and all that time the osmoreceptors are still reporting a high osmolarity, so you keep drinking. By the time the water reaches your blood, you’ve drunk too much. That’s typical of negative feedback with a delay: it overshoots, and it can oscillate. With feed-forward, receptors in the mouth and stomach signal that you’ve drunk water before it has been absorbed, and they switch thirst off for a while. You drink less, and the overshoot almost disappears (the lowest point is about 298 mOsm/L). Bellows (1938) saw exactly this in dogs with oesophageal fistulae, whose water never reached the stomach. They drank about the right amount and then stopped, but only for a while.")}

<h2 id="ck-clock">A clock in every cell</h2>
<p>Almost every cell in your body has a clock of its own, built from a negative feedback loop of genes and proteins (a <em>transcription–translation feedback loop</em>). Two proteins, CLOCK and BMAL1, switch on the <i>Per</i> and <i>Cry</i> genes. Their mRNA is translated into the PER and CRY proteins, which go back into the nucleus hours later and switch their own genes off. Once those proteins have been broken down, the genes come back on and the cycle begins again.</p>
{callout("concept", "Why a slow loop makes a clock", "<p>Without delays, negative feedback settles at a steady level. Every step of this loop takes hours, though: transcription, translation, the changes made to the proteins, and their journey back into the nucleus. By the time the proteins switch their genes off, far too many of them have been made. And by the time they’ve gone, the genes have been off for too long. So the loop keeps overshooting, first one way and then the other. In other words, it oscillates, with a period of about a day that’s set mainly by its delays.</p>")}
{activity("Run the clock", [
    task("ck-open", f'Open the clock {flow("example:clock", "show me")}. If it asks whether you want to leave the thirst diagram, there’s no need to save it. The arrow from <i>Light</i> is blocked, so the clock is in a cave, with no daylight to set it.', auto="flow:open example=clock"),
    task("ck-run", f'Run it {flowrun("show me")}. The message under the diagram tells you the period of the oscillation, measured from one peak to the next.', auto="flow:run name~clock oscillates=true blocked>0"),
])}
{q("ck-q-period", "What is the period of the clock in the cave, in hours?",
   "About 24.6 hours. Without daylight, a clock runs at its own pace, which is a little different from 24 hours. That’s why these rhythms are called <i>circadian</i>, from <i>circa diem</i>, “about a day”. In 1962 the French caver Michel Siffre spent 63 days in a cave with no daylight and no clock. He kept sleeping and waking in a regular cycle, but it was a little longer than 24 hours, so his days slipped later and later. When he came out, he thought he’d been underground for far less time than he had.",
   accept="num:24.6±0.4", placeholder="hours")}
{activity("Make some mutants", [
    task("ck-short", 'Click the arrow labelled <i>back into the nucleus</i>, and in the panel on the right change its <b>Delay</b> from 4 hours to 2. Run the diagram again and read off the period.', auto="flow:run name~clock period>0 period<22"),
    task("ck-long", 'Now make the delay 6 hours and run it again.', auto="flow:run name~clock period>27"),
    task("ck-ko", 'Put the delay back to 4 hours. Then right-click <i>PER and CRY proteins</i>, choose <b>Knock it out</b>, and run it again.', auto="flow:run name~clock knocked>0 oscillates=false"),
])}
{mcq("ck-q-per", "The first clock gene, <i>period</i>, was found in fruit flies by Ronald Konopka and Seymour Benzer in 1971. One mutant fly had a rhythm of about 19 hours (<i>per</i><sup>S</sup>), another of about 29 hours (<i>per</i><sup>L</sup>), and a third had no rhythm at all (<i>per</i><sup>0</sup>). Which change to the model made a clock like <i>per</i><sup>0</sup>?", [
    ("Shortening the delay of <i>back into the nucleus</i>", False, "No. A shorter delay gave a shorter period, about 20 hours, which is more like perˢ."),
    ("Knocking out the PER and CRY proteins", True, "That’s right. Without the proteins there’s no feedback. Nothing switches the genes off, so they stay on and nothing oscillates, just like the per⁰ flies, which make no working PER protein."),
    ("Lengthening the delay of <i>back into the nucleus</i>", False, "No. A longer delay gave a longer period, about 29 hours, like perᴸ."),
])}
{activity("Out of the cave", [
    task("ck-light", 'Put the proteins back (right-click them and choose <b>Put it back to normal</b>), then unblock the arrow from <i>Light</i>. Now the clock is out of the cave. Run it.', auto="flow:run name~clock blocked=0 knocked=0 period>23.5 period<24.5"),
])}
{q("ck-q-light", "Out of the cave, what was the period? What does light do to the clock, and why does the clock need it?",
   "24 hours. Light resets, or <em>entrains</em>, the clock every day, so it keeps to 24 hours and stays in step with the Sun. That makes light the clock’s main <i>zeitgeber</i> (“time-giver”). A clock with a period of 24.6 hours that was never reset would drift by about 36 minutes a day, and within a few weeks it would be telling you that midnight was noon. In mammals, light reaches the master clock in the SCN through the eyes, and you’ll follow its path in the next chapter. Many people who are totally blind have clocks that free-run, drifting in and out of step with the day.")}
{callout("info", "A Nobel Prize for the loop", "<p>In 2017 Jeffrey Hall, Michael Rosbash and Michael Young won the Nobel Prize in Physiology or Medicine for working out how the clock works. They showed that the PER protein builds up at night, enters the nucleus and switches off its own gene, which is the loop you’ve just run. Clocks have been found in animals, plants, fungi and some bacteria. Their genes differ, but most are built around a delayed negative feedback loop like this one.</p>")}
{callout("tip", "For your essay", "<p>A clock is negative feedback that’s <em>meant</em> to oscillate, because a long delay turns a loop that would hold things steady into one that keeps time. Thirst is negative feedback that would overshoot if feed-forward didn’t help it out. Both examples tell you something about what negative feedback does well, and where it falls short.</p>")}
{optional(f"""
{activity("A 24-hour clock in the cave", [
    task("ck-24", 'Block the arrow from <i>Light</i> again. Can you make the clock keep 24 hours in the cave, to within 0.2 hours? Try changing the delays on <i>made into protein</i> and <i>back into the nucleus</i>. What matters is the total delay around the loop.', auto="flow:run name~clock blocked>0 period>23.8 period<24.2"),
    task("ck-pos", f'For comparison, here’s positive feedback. Open the blood clotting example {flow("example:positive-feedback-clotting", "show me")} and run it.', auto="flow:open example=positive-feedback-clotting"),
])}
{q("ck-q-pos", "Once clotting starts, what happens to it, and why can’t a loop like this hold anything steady?",
   "It runs away. Each step makes more of whatever activates it, so the response grows faster and faster until something outside the loop stops it. In the body, that’s the job of anticoagulants, which keep the clot to the wound. Positive feedback reinforces a change instead of opposing it, so it can’t bring a variable back to a set point. It’s useful when you need a fast, all-or-nothing change, and something always has to bring it to an end.")}
""")}
'''
    return chapter("s1-clock", num, "A clock made of feedback", "flow", "A clock made of negative feedback", 15,
                   "Negative feedback keeps things steady, as long as it’s quick. Add a delay and it overshoots, and with a "
                   "long enough delay it never settles at all. In this chapter you’ll run two loops from the lectures: "
                   "thirst, and the clock inside your cells.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_where(num):
    body = f'''
<h2 id="wh-brain">The master clock</h2>
<p>The <b>suprachiasmatic nuclei</b> (SCN) are two small clusters of neurons at the bottom of the hypothalamus, one on each side of the third ventricle. They sit just above the <b>optic chiasm</b>, where the optic nerves meet and cross, which is where their name comes from (<i>supra</i> means “above”). They’re too small to appear in the model, but you can still find exactly where they are.</p>
{activity("Find the clock", [
    task("wh-glands", f'Show the endocrine glands with their labels {anat("endocrine+labels")}.', auto="anat:system id=endocrine on=true"),
    task("wh-hypo", 'Zoom in on the head and click on the two parts of the pituitary gland, the <b>adenohypophysis</b> (the anterior pituitary) and the <b>neurohypophysis</b> (the posterior pituitary). Then click on the <b>hypothalamus</b>, just above them.', auto="anat:select id=hypothalamus by=click||anat:select id=hypothalamus by=list"),
    task("wh-pineal", f'{anatfind("pineal-gland", "Find the pineal gland")}, which makes melatonin at night when the SCN tell it to.', auto="anat:find ok=true target~pineal"),
    task("wh-adrenal", f'{anatfind("suprarenal-gland", "Find a suprarenal gland")} (an adrenal gland), which sits on top of a kidney. The clock reaches it through the pituitary, so ACTH, and with it cortisol, rise in the early morning before you wake.', auto="anat:find ok=true target~suprarenal"),
    task("wh-chiasm", f'{anatfind("optic-chiasm", "Find the optic chiasm")}. The brain is shown with it, so look at it from below (<b>View</b> ▸ <i>Inferior</i>, or press <kbd>6</kbd>). The SCN lie just above the chiasm.', auto="anat:find ok=true target~optic-chiasm"),
    task("wh-cut", f'Cut the head in two {anat("brain+endocrine:hypothalamus+section:sagittal@0.5@left")}. You’ll see that the hypothalamus, the pituitary on its stalk and the pineal gland all lie close to the midline.', auto="anat:section axis=sagittal"),
])}
{q("wh-q-light", "Light sets the clock. Can you trace its path? Which cells in the eye pick it up, which route does the signal take, and where does it end up?",
   "Some of the ganglion cells in the retina have a photopigment of their own, <b>melanopsin</b>, which responds best to blue light. These intrinsically photosensitive retinal ganglion cells (ipRGCs) send their axons along the optic nerve to the optic chiasm. There they leave it in the <b>retinohypothalamic tract</b> and go to the SCN just above. The SCN’s neurons fire faster by day than at night, and they pass the time of day on to the rest of the body. The pineal gland, for example, gets the message through the paraventricular nucleus, the spinal cord and sympathetic nerves, which is why melatonin is made at night.")}

<h2 id="wh-scope">Under the microscope</h2>
{activity("The pituitary and the adrenal gland", [
    task("wh-pit", f'Open the pituitary gland {scope("pituitary-gland", "show me")}. In this specimen the anterior pituitary (on the left) and the posterior pituitary (on the right) were cut as two separate pieces.', auto="scope:open slide=pituitary-gland"),
    task("wh-post", f'{scopefind("pituitary-gland:posterior", "Find the posterior pituitary")} and compare it with the anterior pituitary at 20×.', auto="scope:find slide=pituitary-gland target=posterior ok=true"),
    task("wh-adr", f'Open the adrenal gland {scope("adrenal-gland", "show me")} and look at it at 1×. You should be able to see a capsule, the cortex with its three zones, and the medulla in the middle.', auto="scope:open slide=adrenal-gland"),
    task("wh-zf", f'{scopefind("adrenal-gland:zona-fasciculata", "Find the zona fasciculata")}. It’s the widest zone of the cortex, with its cells arranged in long columns.', auto="scope:find slide=adrenal-gland target=zona-fasciculata ok=true"),
    task("wh-med", f'{scopefind("adrenal-gland:medulla", "Find the medulla")}, which makes adrenaline.', auto="scope:find slide=adrenal-gland target=medulla ok=true"),
])}
{q("wh-q-pit", "Why does the posterior pituitary look so different from the anterior pituitary?",
   "The posterior pituitary is nervous tissue, an extension of the hypothalamus. It’s made of the axons and nerve terminals of neurons whose cell bodies lie in the supraoptic and paraventricular nuclei, with glial cells (pituicytes) among them, so it looks pale and fibrous, with few nuclei. Its nerve terminals release ADH and oxytocin into the blood. The anterior pituitary, on the other hand, is a gland. It’s made of clusters and cords of endocrine cells, with many nuclei and stained cytoplasm, lying between wide capillaries (sinusoids). These bring the releasing hormones of the hypothalamus down the portal vessels.")}
{mcq("wh-q-zone", "Cortisol rises in the early morning, before you wake, preparing you for the day. Which part of the adrenal gland makes it?", [
    ("The zona glomerulosa", False, "No. The outermost zone makes aldosterone, under the control of the renin–angiotensin system and the plasma K+ concentration."),
    ("The zona reticularis", False, "No. The innermost zone of the cortex mostly makes androgens, such as DHEA."),
    ("The zona fasciculata", True, "Yes. Its cells make cortisol under the control of ACTH from the anterior pituitary, and cortisol feeds back on the hypothalamus and the pituitary to switch them off. It’s a negative feedback loop with a daily rhythm on top."),
    ("The medulla", False, "No. The medulla makes adrenaline, when its sympathetic nerves tell it to."),
])}

<h2 id="wh-mol">Two hormones of the day and the night</h2>
{activity("Melatonin and cortisol", [
    task("wh-mel", f'Open melatonin {viewer("clear; molecule melatonin; only ballstick; color cpk", "show me")}. The pineal gland makes it from tryptophan, by way of serotonin, and its level in the blood rises to about 80 pg/mL at night.', auto="viewer:molecule name=Melatonin"),
    task("wh-cort", f'Now open cortisol {viewer("clear; molecule cortisol; only ballstick; color cpk", "show me")}, a steroid made from cholesterol.', auto="viewer:molecule name=Cortisol"),
])}
{mcq("wh-q-lipid", "Cortisol is a steroid, which makes it lipid-soluble. Which of these follows from that?", [
    ("It is stored in vesicles and released by exocytosis", False, "No. That’s how water-soluble hormones such as adrenaline are released. A lipid-soluble hormone would leak out of a vesicle through its membrane, so steroids are made as they’re needed and released straight away."),
    ("It crosses the membranes of its target cells and binds to receptors inside them, which change gene transcription. Its effects therefore take hours to develop, and they last", True, "Yes. Steroid receptors are inside the cell, and once they’ve bound their hormone they act as transcription factors."),
    ("It is carried freely dissolved in the plasma", False, "No. Most of the cortisol in the blood is bound to carrier proteins (corticosteroid-binding globulin and albumin), and only the small free fraction can act."),
], model="Melatonin, an indoleamine, is lipid-soluble too, so it isn’t stored either. It leaves the pineal gland as soon as it’s made, which means its level in the blood follows how fast it’s being made: high at night and low by day. It acts mainly on receptors in the membranes of its target cells, including cells in the SCN, so melatonin feeds back on the clock as well.")}
{optional(f"""
{activity("Blue light, and the adrenal cortex", [
    task("wh-sim", f'The clock’s photopigment, melanopsin, is most sensitive to blue light at about 480 nm. Open the Color Vision simulation {sim("color-vision", "show me")}, go to its <b>Single Bulb</b> screen, and set the bulb to a single colour of about 480 nm.', auto="sim:open id=color-vision"),
    task("wh-aldo", f'Open aldosterone {viewer("clear; molecule aldosterone; only ballstick; color cpk", "show me")}, which is made in the zona glomerulosa, and compare it with cortisol. Both are steroids made from cholesterol, and they differ in only a few groups of atoms.', auto="viewer:molecule name=Aldosterone"),
])}
{q("wh-q-screen", "Why might using a bright screen late in the evening make it harder to fall asleep?",
   "Screens give out a lot of blue light, the colour melanopsin responds to best. Light in the evening reaches the SCN through the retinohypothalamic tract, where it suppresses the release of melatonin and shifts the clock later, so you feel sleepy later. Experiments where people read from a light-emitting screen for a few hours before bed have found exactly this: less melatonin, and a later clock. How much a screen matters depends on how bright it is and how long you look at it, though.")}
{mcq("wh-q-conn", "In Conn’s syndrome, which hormone is made in excess, and where?", [
    ("Cortisol, by the zona fasciculata", False, "No. Too much cortisol causes Cushing’s syndrome."),
    ("Aldosterone, by the zona glomerulosa", True, "Yes. It’s usually made by an adenoma, regardless of the renin–angiotensin system. Too much aldosterone makes the body hold on to Na+ and water and lose K+, so blood pressure rises and the plasma K+ concentration falls."),
    ("Adrenaline, by the medulla", False, "No. A tumour of the medulla that makes too much adrenaline is a phaeochromocytoma."),
])}
""")}
'''
    return chapter("s1-where", num, "Where is the clock?", "anatomy", "Where is the clock?", 20,
                   "Your master clock is a pair of tiny nuclei in the hypothalamus. In this chapter you’ll find where they "
                   "are, follow the light that sets them, and look at the glands they control, in 3D, under the microscope "
                   "and as molecules.", body)


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


DATA_CREDIT = ('<p>The data are from the MIT-BIH Normal Sinus Rhythm Database (version 1.0.0) on PhysioNet, used under the '
               'Open Data Commons Attribution License: Goldberger et al. (2000) <i>Circulation</i> 101: e215–e220; '
               '<a href="https://doi.org/10.13026/C2NK5R" target="_blank" rel="noopener">doi:10.13026/C2NK5R</a>. The 18 '
               'people were 5 men aged 26 to 45 and 13 women aged 20 to 50, and none of their ECGs showed any significant '
               'arrhythmias. The repository explains how the hourly heart rates were worked out '
               '(<code>starter/data/README.md</code>).</p>')


def ch_heart(num):
    body = f'''
<h2 id="ht-rr">From beats to a heart rate</h2>
<p>The data come from the <b>MIT-BIH Normal Sinus Rhythm Database</b>, a set of long-term ECGs from 18 adults. Each one was recorded over about a day while the person went about their life, and every beat has been labelled. A heart rate comes from the time between beats, the R–R interval. In beats per minute, it’s 60 divided by the R–R interval in seconds. Start by measuring one yourself.</p>
{activity("Measure an R–R interval", [
    task("ht-open", f'Open an ECG {rec("ecg-normal@2,6", "show me")}. It shows four seconds of a normal heartbeat.', auto="rec:open id=ecg-normal"),
    task("ht-cal", f'Choose the <b>Calipers</b> {rectool("calipers", "show me")} and drag from the peak of one R wave (the tall spike) to the peak of the next. The bar above the trace shows the interval (Δt) and the heart rate that goes with it.', auto="rec:measure id=ecg-normal dt>0.5 dt<1.2"),
])}
{q("ht-q-rr", "What heart rate does an R–R interval of 0.8 s give, in beats per minute?",
   "75 beats per minute, because 60 ÷ 0.8 = 75. In the data set, the heart rate for each hour is 60 divided by the mean of all the R–R intervals in that hour. That’s thousands of them, and the <code>n_beats</code> column tells you exactly how many.",
   accept="num:75±0.5", placeholder="beats per minute")}

<h2 id="ht-r">A day and a night, in R</h2>
{callout("info", "The first time", "<p>The first time you open RStudio, the workbench has to download R itself (about 30 MB), so it can take a minute.</p>")}
<p>The file <code>~/data/heart-rate-24h.csv</code>, which is already in your files, holds the heart rate of each of the 18 people for each hour of the day. That makes 432 rows (18 people × 24 hours). Each <b>show me</b> button types a line of R into RStudio’s Console for you. Press <kbd>Enter</kbd> to run it, and look at what comes back.</p>
{activity("Read the data, and plot one person’s day", [
    task("ht-read", f'Read the file into a table called <code>heart</code>: {rcode(R_READ)}', auto="r:input kind=rstudio line~heart-rate-24h.csv"),
    task("ht-head", f'Look at its first few rows: {rcode(R_HEAD)}. Each row is one hour for one person. The columns are <code>subject</code> (the person), <code>sex</code>, <code>age</code>, <code>hour</code> (0 means midnight to 1 a.m.), <code>time</code>, <code>hr</code> (the heart rate in beats per minute) and <code>n_beats</code>.', auto="r:input kind=rstudio line~head(heart"),
    task("ht-sum", f'Summarise the heart rates: {rcode(R_SUM)}. Here <code>heart$hr</code> means “the <code>hr</code> column of the table <code>heart</code>”. Some hours are <code>NA</code> (not available), either because the recording had ended or because it was too noisy.', auto="r:input kind=rstudio line~summary(heart"),
    task("ht-one", f'Pick out one person, a woman of 32: {rcode(R_ONE)}. Then plot her day: {rcode(R_PLOT1)}', auto="rstudio:plot"),
])}
{q("ht-q-one", "Describe her day. When was her heart rate lowest, and when was it highest?",
   "Her heart rate was low and steady through the night, at 61–65 beats per minute, and lowest at 05:00. It jumped from 63 to 77 at 08:00, around the time she got up, and stayed higher through the day, peaking in the afternoon at 88 (at 15:00). Then it fell through the evening, down to 65 by 23:00. The hour from 11:00 is missing.")}
{activity("Everyone’s average day", [
    task("ht-agg", f'Work out the mean of the 18 people for each hour: {rcode(R_AGG)}. Then have a look at it: {rcode("avg")}. The <code>aggregate()</code> function splits the heart rates up by hour and takes the mean of each group, leaving out the NAs.', auto="r:input kind=rstudio line~aggregate("),
    task("ht-plot", f'Plot it: {rcode(R_PLOT2)}', auto="r:input kind=rstudio line~plot(avg"),
    task("ht-min", f'Which hour has the lowest mean? {rcode(R_MIN)}', auto="r:input kind=rstudio line~which.min"),
])}
{q("ht-q-low", "Which hour of the day has the lowest mean heart rate (0 to 23)?",
   "Hour 5, that is from 05:00 to 06:00, at 64.4 beats per minute. The hours starting at 03:00 and 04:00 are almost as low (64.6), so the trough comes in the small hours, when most people are asleep. The mean is highest in the late morning and early afternoon, at about 85 beats per minute.",
   accept="num:5", placeholder="the hour")}
{activity("Day against night", [
    task("ht-day", f'Work out the mean heart rate by day, from 08:00 to 20:00: {rcode(R_DAY)}', auto="r:input kind=rstudio line~day <-"),
    task("ht-night", f'Then the mean at night, from midnight to 06:00: {rcode(R_NIGHT)}', auto="r:input kind=rstudio line~night <-"),
    task("ht-diff", f'And the difference between them: {rcode(R_DIFF)}. (<code>na.rm = TRUE</code> tells <code>mean()</code> to leave out the NAs, because the mean of anything that includes an NA is NA.)', auto="r:input kind=rstudio line~day - night"),
])}
{q("ht-q-diff", "How much lower is the heart rate at night than by day, in beats per minute?",
   "About 17 beats per minute (82.5 by day against 65.6 at night), so the heart rate is about a fifth lower at night. Every one of the 18 people had a lower heart rate at night, by between 7 and 31 beats per minute.",
   accept="num:16.9±0.3", placeholder="beats per minute")}
{mcq("ht-q-mask", "Does this show that the heart rate has a circadian rhythm, one that’s generated by the body’s clock?", [
    ("Yes, because any rhythm with a period of 24 hours must come from the clock", False, "No. A rhythm driven by the events of the day, like sleeping at night and being active by day, also has a period of 24 hours."),
    ("No, because a circadian rhythm would have a period of exactly 24 hours", False, "No. Left to itself, a clock runs with a period of about 24 hours, but in everyday life light entrains it to exactly 24, so the period alone can’t tell you."),
    ("Not by itself. These people slept at night and were active by day, and sleep, posture, meals and exercise all change the heart rate directly. To see the clock’s own rhythm, you’d have to keep people in constant conditions", True, "Yes. A daily rhythm can be driven by what happens each day as well as by the clock, and the effects of sleep and activity hide, or mask, the clock’s own rhythm. Studies that keep people awake and lying still in dim light, with small regular meals (a “constant routine”), show that the heart rate does have a rhythm of its own, but a smaller one."),
])}
{optional(f"""
{activity("How people differ, and a curve for the rhythm", [
    task("ht-box", f'How much do people differ? Try {rcode(R_BOX)}. You get a box for each hour: the box covers the middle half of the 18 people, the line inside it is the median, and the whiskers show the range.', auto="r:input kind=rstudio line~boxplot("),
    task("ht-cos", f'Circadian biologists often describe a rhythm by fitting a cosine curve to it, which they call a <em>cosinor</em>. Fit one: {rcode(R_FIT)}. Keep its coefficients: {rcode(R_COEF)}. Then work out the curve’s mean level (its <em>mesor</em>), its amplitude, and the hour of its peak: {rcode(R_COS)}', auto="r:input kind=rstudio line~atan2("),
    task("ht-curve", f'Plot the means again ({rcode(R_PLOT2, "show me")}) and draw the curve over them: {rcode(R_CURVE)}', auto="r:input kind=rstudio line~curve("),
])}
{q("ht-q-cos", "What’s the amplitude of the rhythm, and when does it peak? How well does a cosine curve describe it?",
   "The mesor is 75.3 beats per minute and the amplitude is 10.1 beats per minute, so the curve swings about 10 above and 10 below the mesor. The peak, called the <em>acrophase</em>, is at 14.7 hours, which is about 14:40. A cosine is only a rough fit, because the real rhythm isn’t symmetrical. It jumps up in the morning when people get up, then falls more slowly through the evening.")}
""")}
{callout("info", "Where the data come from", DATA_CREDIT)}
'''
    return chapter("s1-heart", num, "Your heart’s daily rhythm", "recorder", "Your heart’s daily rhythm", 20,
                   "Your heart beats more slowly at night. Using real 24-hour ECGs from 18 people, you’ll see this rhythm "
                   "for yourself in a few lines of R, which the page types for you.", body)


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
            f'<p class="credit">It’s about 450 words, a little shorter than most 40-minute essays. Ouyang, Y. et al. (1998) <i>PNAS</i> 95: 8660–8664; DeCoursey, P.J. et al. (2000) <i>Journal of Comparative Physiology A</i> 186: 169–180.</p></details>')


def ch_marking(num):
    body = f'''
<p>When your supervisor gives you feedback on an essay, it’s against six <b>core criteria</b>. Each one describes a quality of a good essay and what would make it better, and examiners look for the same qualities.</p>
{criteria_cards()}
<p class="credit">The core criteria, and the comments below, come from the essay feedback form of <i>Assessment Plus: using assessment criteria to support student learning</i>, a HEFCE-funded consortium project (assessmentplus.net).</p>

<h2 id="mk-example">An example essay</h2>
<p>Below is a short essay on a question from this week’s lectures. Its facts are all correct, but it has a problem under each of the six criteria. Read it through, then decide which comment from the feedback form fits each part best.</p>
{sample_essay()}

<h2 id="mk-comments">What comments would it get?</h2>
{mcq("mk-q1", "<b>Addressing the question.</b> Paragraph 2 is accurate, but which comment fits it best?", [
    ("The material you use is not relevant to this topic", False, "No. The clock’s machinery is certainly part of the topic of circadian rhythms."),
    ("The material you use is relevant to this general topic, but you don’t make clear how it is relevant to this specific question", True, "Yes. The paragraph explains how circadian rhythms are made, but the title asks why animals have them, and it never connects the two. However accurate it is, as it stands it earns little credit."),
    ("Good, you have made it very clear how the material you use is related to the specific issues that are the focus of the essay", False, "Not yet. The paragraph never links the mechanism to why animals have rhythms."),
], model="<b>To put it right</b>, use the mechanism to answer the question, perhaps like this: <i>“Because the rhythm is generated within the body – by a negative feedback loop of genes and proteins that takes about a day to go round – the body can prepare for dawn before it comes, rather than respond once the light has arrived.”</i>")}
{mcq("mk-q2", "<b>Using evidence.</b> Paragraph 3 mentions Siffre’s cave, shift workers and the morning rise in blood pressure. Which comment fits it best?", [
    ("You don’t provide enough research findings, data, quotations or other sourced material as evidence for your claims", False, "Not quite. There is evidence here, but none of it is linked to anything."),
    ("You provide some potential evidence, but the link with your claims could be clearer or developed more", True, "Yes. Siffre’s cave is good evidence, but evidence for what? The paragraph never says. And “shift workers have more health problems” is a claim that needs evidence of its own."),
    ("Good, you use evidence clearly and convincingly to support your claims", False, "Not yet. The facts are listed, but none of them is used to support a point."),
], model="<b>To put it right</b>, say what each piece of evidence shows. For example: <i>“The rhythms are generated within the body: in 1962 Michel Siffre spent 63 days in a cave, without daylight or clocks, and he went on sleeping and waking in a regular cycle – but one a little longer than 24 hours, so it cannot have been driven by the day outside.”</i> Then either back up the claim about shift workers with a source, or leave it out.")}
{mcq("mk-q3", "<b>Developing argument.</b> Read the conclusion (paragraph 5) and think about the essay as a whole. Which comment fits best?", [
    ("Your essay does not contain a point of view or position in relation to the title or question", True, "Yes. The essay never says why animals have circadian rhythms, and “there are lots of reasons” isn’t a position. Without one, the paragraphs can’t build towards anything."),
    ("Your essay contains some expression of a position, which could have been more explicitly developed and justified", False, "Close, but the essay doesn’t really take a position at all. It never says what the reasons are, let alone which one matters most."),
    ("Good, you have established a clear position in relation to the question, and developed that position throughout the essay", False, "No. There’s no position here to develop."),
], model="<b>To put it right</b>, decide on your answer before you start writing, and say what it is early on. You might write: <i>“Animals have circadian rhythms chiefly because they let the body anticipate the predictable changes of each day.”</i> Then make each paragraph a step towards that answer. One could show that the rhythm is made within the body, the next how it prepares the body for the day, and another how good the evidence is that this helps. Finish with a conclusion that draws those steps together.")}
{mcq("mk-q4", "<b>Critical evaluation.</b> Paragraph 4 says that circadian rhythms “obviously evolved because they help animals to survive”. Which comment fits best?", [
    ("Your essay is too descriptive – there is not enough assessment of the value or significance of what you describe", False, "Partly, but paragraph 4 does make a judgement. The trouble is that it gives no reasons for it."),
    ("Your evaluative points could be more extensive, explicit, systematic, reasoned or justified", True, "Yes. “Obviously” asserts a judgement without justifying it. Whether rhythms help animals survive is a question that biologists have tested, and the evidence can be weighed."),
    ("Good, you have made some systematic, reasoned and justified assessments of value", False, "Not yet. The claim is asserted, but it isn’t justified."),
], model="<b>To put it right</b>, weigh up the evidence, as in this passage: <i>“When strains of cyanobacteria with clocks of different periods were grown together, the strain whose period matched the light–dark cycle outgrew the others (Ouyang et al., 1998); and chipmunks returned to the wild after damage to the SCN were killed by predators more often than intact animals (DeCoursey et al., 2000). Such studies are few, however, and come from only a handful of species.”</i>")}
{mcq("mk-q5", "<b>Structuring.</b> Paragraph 1 is the introduction. Which comment fits it best?", [
    ("Some of your paragraphs do not focus on one main idea each, or are too short", False, "That’s true of paragraph 3, which lists three unconnected facts, but it isn’t the problem with the introduction."),
    ("Your introduction could do more to let the reader know how the essay will deal with the issues", True, "Yes. “In this essay I will talk about circadian rhythms” tells the reader nothing about the answer the essay will give, or how it will get there."),
    ("Your conclusion could do more to give the essay an ending which brings together your various points", False, "That’s true of paragraph 5, but this is the introduction."),
], model="<b>To put it right</b>, define the terms and say where the essay is going. For example: <i>“Circadian rhythms are rhythms with a period of about 24 hours that persist without cues from the environment. This essay argues that animals have them chiefly because they allow the body to anticipate the day: it shows first that the rhythms are generated within the body, then how they prepare it for the day, and finally weighs the evidence that they help animals to survive.”</i>")}
{mcq("mk-q6", "<b>Use of language.</b> Look at the wording of paragraphs 1 and 4: “really interesting”, “loads of”, “get us ready”. Which comment fits best?", [
    ("Your essay has too many spelling, grammar or punctuation errors", False, "No. There aren’t any errors of that kind."),
    ("In some passages your writing makes the meaning unclear or difficult to follow", False, "No. The meaning is perfectly clear."),
    ("Your meaning is clear, but your language is too colloquial", True, "Yes. “Really interesting”, “loads of” and “get us ready” belong in conversation, not in a scientific essay."),
    ("Make sure you stick to the correct citation conventions", False, "Not the main problem here (although Siffre’s study could be cited more carefully)."),
], model="<b>To put it right</b>, use the plain, precise language of science, such as <i>“Circadian rhythms are found throughout the animal kingdom, as well as in plants, fungi and some bacteria”</i> and <i>“plasma cortisol rises in the early morning, before waking, preparing the body for activity.”</i>")}

<h2 id="mk-better">A better version</h2>
<p>Here’s the same essay, rewritten to meet each criterion. It isn’t the only good answer, but look at how it takes a position at the start, how every paragraph is a step towards that position, and how it uses and weighs its evidence instead of just listing it.</p>
{better_essay()}
{callout("tip", "Use the criteria on your own essay", "<p>In the last few minutes of your 40, read your essay through against the six criteria. Does every paragraph help to answer the question? Is each example linked to the point it supports? Do you take a position and build on it as the essay goes on? Do you weigh up your examples, rather than just describing them? Does each paragraph make one main point? And is the language formal and precise?</p>")}
'''
    return chapter("s1-marking", num, "How essays are marked", "exam", "How essays are marked", 15,
                   "Your supervisor gives feedback on essays against six core criteria. Here you’ll see what each one "
                   "means, and how it applies to an example essay: the comments the essay would get, and how to put each "
                   "problem right.", body)


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
    ['Yes. “Some ups and downs in status”, “revealed its talent … to Thomas Hunt Morgan and his students” and “spectacularly successful … history” are all Kohler’s own words. Quotation marks would keep you out of trouble, but it would be much better to put it in your own words.',
     'Look at the words themselves first. Whole phrases are Kohler’s, word for word.',
     'It does reorder the ideas, but look at the words. Whole phrases are Kohler’s, word for word.',
     'No. Phrases such as “some ups and downs in status” and “spectacularly successful” are Kohler’s own words, used without quotation marks. A reference doesn’t make copied words your own.'],
    ['Hardly any of the words are Kohler’s. The problem here is a subtler one.',
     'Yes. Each sentence follows Kohler’s part by part, with the words swapped for others, so “Few laboratory creatures have had such a … history as Drosophila” becomes “No model organism has been so … as the fruit fly”. The paragraph follows his as well.',
     'It does, but look inside each sentence too. Each one copies the shape of Kohler’s, phrase by phrase.',
     'No. The words are new, but each sentence is Kohler’s sentence with its words swapped for others, so it’s still his writing.'],
    ['No. The words are the writer’s own.',
     'No. Its sentences are built differently from Kohler’s.',
     'Yes. The sentences are new, but the paragraph follows Kohler’s idea by idea, in the same order: a remarkable history, arriving around 1900, being taken up by Morgan and his students, ups and downs, and still going strong. It’s his paragraph, rewritten.',
     'No. Each sentence is new, but the paragraph takes Kohler’s ideas in exactly his order. In other words, it’s his argument.'],
    ['No. The only words it shares with Kohler are names, and plain terms that anyone would use.',
     'No. Its sentences are built in their own way.',
     'No. It starts from a different point, puts the ideas in its own order and adds a judgement of its own.',
     'Yes. It starts from a different point (Morgan and his colleagues), puts the ideas in its own order and its own words, and adds a judgement of its own (the breadth and depth of current research). It still credits Kohler, too, because the ideas are his.'],
]
PLAG_MODEL = [
    'Here are the phrases taken from Kohler: “Despite <mark>some ups and downs in status</mark>, nearly <mark>a century</mark> after the fly <mark>revealed its talent</mark> <mark>to Thomas Hunt Morgan and his students</mark>, <i>Drosophila</i> genetics research continues its <mark>spectacularly successful</mark> <mark>history</mark> (Kohler, 1994).”',
    '<table class="align"><tr><th>Kohler</th><th>Version 2</th></tr>'
    '<tr><td>Few laboratory creatures have had such a spectacularly successful and productive history as <i>Drosophila</i>.</td><td>No model organism has been so amazingly useful and effective as the fruit fly.</td></tr>'
    '<tr><td>It first entered laboratories about 1900,</td><td>The fly came on the scene as an experimental tool at the beginning of the 20th century,</td></tr>'
    '<tr><td>revealed its talent for experimental genetics to Thomas Hunt Morgan and his students at Columbia University in the early 1910s,</td><td>was adopted by Thomas Hunt Morgan and his Columbia pupils at Columbia University around 1910,</td></tr>'
    '<tr><td>and after some ups and downs in status is still going strong almost a century later.</td><td>and (despite some fluctuations in attention paid to it) is still a widely used experimental system.</td></tr></table>',
    'Here are Kohler’s ideas in his order, each with version 3’s wording for it: a remarkable history (“a rich and useful legacy”), arriving around 1900 (“at the turn of the century”), being taken up by Morgan and his students (“the organism of choice for Thomas Hunt Morgan and his Columbia University pupils”), ups and downs (“despite fluctuations in status”), and still going strong (“still central to the progress of genetics”).',
    'It still gives the reference, though. An idea taken from a source needs one, even when every word is your own.',
]


def ch_plag(num):
    versions = ''
    for i, v in enumerate(VERSIONS):
        versions += f'<blockquote class="passage"><span class="pv">Version {i + 1}</span>{v}</blockquote>\n'
        opts = [(PLAG_OPTS[k], k == i, PLAG_WHY[i][k]) for k in range(4)]
        versions += mcq(f'pl-q{i + 1}', f'Is version {i + 1} acceptable? If not, what’s wrong with it?', opts, model=PLAG_MODEL[i]) + '\n'
    body = f'''
<p>The University counts as plagiarism anything you submit as your own that comes, in whole or in part, from other people’s work without due acknowledgement, whether or not you meant to deceive anyone. Copying a sentence is the obvious case. Paraphrasing too closely is the one that tends to catch people out.</p>

<h2 id="pl-orig">The original</h2>
<blockquote class="passage orig"><span class="pv">The original</span>{KOHLER}<span class="src">{KOHLER_REF}</span></blockquote>

<h2 id="pl-versions">Four paraphrases</h2>
<p>Each of these was written by someone who had read the passage, and each one gives a reference. Which of them are acceptable, and what’s wrong with the others?</p>
{versions}
{mcq("pl-q-quote", "You want to use Kohler’s phrase “a spectacularly successful and productive history”. What should you do?", [
    ("Change a word or two – “a remarkably successful and productive history” – and give the reference", False, "No. That’s still Kohler’s phrase, and too close to be your own."),
    ("Use it as it is, with the reference at the end of the paragraph", False, "No. A reference credits the idea, but words you’ve copied need quotation marks as well."),
    ("Put it in quotation marks and give the reference: <i>Drosophila</i> has had “a spectacularly successful and productive history” (Kohler, 1994)", True, "Yes. Copied words need quotation marks as well as a reference. Quotations are rare in science, though. Usually you’d put the idea in your own words and cite the source."),
])}
<p class="credit">This exercise is the University’s own (<a href="http://www.biology.cam.ac.uk/exams/plagiarism" target="_blank" rel="noopener">www.biology.cam.ac.uk/exams/plagiarism</a>). Kohler’s book is a history of Thomas Hunt Morgan’s “fly room”. Decades later, <i>Drosophila</i> gave biology its first clock gene, <i>period</i> (see chapter 1).</p>

<h2 id="pl-paste">Why Supervision work won’t let you paste</h2>
{callout("warn", "No pasting from anywhere else", f"<p>In the online exam you can’t paste in text that you copied from outside the exam, and Supervision work is just the same. Text copied from a website, your notes, an AI tool or these instructions won’t go into your essay. You can still copy and paste within your own essay, to move a sentence or a paragraph around.</p><p>That way every word of the essay you hand in is one you typed yourself, which is the best protection against plagiarising by accident. When you use someone’s finding or idea, put it in your own words and say whose it is, as in “Konopka and Benzer (1971) found…”. You’ll see this for yourself when you start your essay. {goto('s1-write', 'go to your essay')}</p>")}
'''
    return chapter("s1-plag", num, "Plagiarism", "exam", "Plagiarism, and why you can’t paste", 10,
                   "Using someone else’s words, ideas or structure without saying so is plagiarism, even if you’ve "
                   "changed the words. Try the University’s exercise, and decide which of four paraphrases of the same "
                   "passage is acceptable.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_write(num):
    hand_steps = [
        task("es-send", f'Hand it in on the page that comes up next. Type the hand-in password that {SUPERVISOR} gave you and press <b>Hand it in</b>. Your essay goes straight to his Google Drive, and the page shows you a receipt once it has arrived.', auto="exam:handin paper=s1-essay step=confirmed", check="paper:s1-essay.handedIn"),
        task("es-word", 'Keep a copy for yourself with <b>Download a copy for yourself</b>, under the password box (or <b>Download your copy</b> once it’s been handed in). It’s saved as a Word document in your Downloads folder.', auto="exam:download paper=s1-essay format=docx", check="paper:s1-essay.downloaded"),
    ]
    hand_note = callout("info", "Handing in", f"<p>Your essay goes straight from this page to {SUPERVISOR}’s Google Drive, and you don’t need a Google account for that. The hand-in password, which {SUPERVISOR} gives you, stops anyone else from handing work in, so please keep it to yourself. Once your essay has arrived, the page tells you so and gives you a receipt. If it can’t be handed in, the page will tell you why. If it still won’t go, download a copy and send it to {SUPERVISOR} some other way.</p>")
    body = f'''
<p class="essay-title">“{ESSAY}”</p>

<h2 id="es-why">Why write it like this?</h2>
<p>Your exams are taken on a computer, in an online exam system. You type your answers in one sitting, against the clock, without notes, and you can’t paste anything in. Supervision work is set up the same way. Writing your supervision essays like this means the exam will feel familiar long before the summer. You’ll find out how much you can plan and write in 40 minutes, and what it’s like to do it without your notes. And because your supervisor sees the essay you can actually write in that time, the feedback is about the essay you’d write in the exam, not one you’ve polished over a week. Just as in the exam, you submit it when you’ve finished and hand it in from the same page. From there it goes straight to {SUPERVISOR}’s Google Drive.</p>

<h2 id="es-before">Before you start</h2>
<ul>
<li>Read about how essays are marked {goto("s1-marking", "chapter 4")} and about plagiarism {goto("s1-plag", "chapter 5")}.</li>
<li>Revise the lectures first if you like. Then put your notes away and find about 45 minutes when you won’t be interrupted.</li>
<li>Have the <b>hand-in password</b> that {SUPERVISOR} gave you to hand, because you’ll need it at the end. It isn’t anywhere on this site.</li>
<li>There’s no time limit, but give yourself about <b>40 minutes</b>, as you would in the exam. The clock at the top of the paper counts the time you spend writing and tells you when you reach 40 minutes. If you haven’t finished by then, write your conclusion. You can carry on if you need to, and the clock will show how long you took.</li>
<li>Spend the first five minutes planning. What’s your answer to the question? Which examples support it, and in what order will you make your points? You can plan on paper, or in the answer box itself as long as you delete the plan before you submit.</li>
<li>A diagram can help an essay, and you can add one here just as you can in the exam. Either draw it with <b>Insert drawing</b> (the pencil), or draw it on paper, take a photo, and add the photo with <b>Insert picture</b>. You can also drag a picture file into your essay. Type a caption underneath, and say in your text what the diagram shows. Your pictures go into the Word document along with your essay.</li>
</ul>
{activity("Write it, and hand it in", [
    task("es-open", f'Open the essay {exam("s1-essay", "show me")} and read its first page.', auto="exam:open paper=s1-essay"),
    task("es-start", 'When you’re ready to write, press <b>Start</b>. If you haven’t added your name yet, it will ask for it so that it can go at the top of your essay.', auto="exam:start paper=s1-essay", check="paper:s1-essay.started"),
    task("es-paste", 'Before you start writing, try this. Copy a sentence from these instructions (<kbd>Ctrl</kbd>+<kbd>C</kbd>, or <kbd>⌘</kbd>+<kbd>C</kbd> on a Mac) and paste it into the box (<kbd>Ctrl</kbd>+<kbd>V</kbd>). It won’t go in.', auto="exam:paste paper=s1-essay refused=true"),
    task("es-write", 'Plan, then write. Aim for an introduction that says what your essay will argue, paragraphs that each make one point with examples, and a conclusion that draws them together.', auto="exam:words paper=s1-essay words>299"),
    task("es-submit", 'When you’ve finished, go to the submission page (the ✓ tile at the bottom right), check your essay and submit it.', auto="exam:submit paper=s1-essay", check="paper:s1-essay.submitted"),
] + hand_steps)}
{hand_note}
{callout("info", "After you’ve handed it in", "<p>Once you’ve submitted, <b>Review my answers</b> shows you the ground a good answer would cover. Read it after you’ve handed your essay in, and make a note of what you’d add or change. That’s what we’ll talk about in the supervision.</p><p>Your essay is kept in this browser, in Files → <code>essays</code>. It won’t be there on another computer, so download it before you leave.</p>")}
{q("es-q-next", "Once you’ve read the guidance, what’s one thing you would do differently in your next essay?",
   "There’s no single right answer here. What matters is your own answer, so bring it to your supervision. It might be about the content (an example you missed, or one you described without linking it to the question), about the argument (taking a clearer position from the start), or about your timing (more planning, or a shorter introduction).")}
'''
    return chapter("s1-write", num, "Write your essay", "exam", "Write your essay, and hand it in", 45,
                   f"This is the one piece of work to hand in this week. You write it in Supervision work, just as you’ll "
                   f"write in the online exam, and then hand it in from the same page. It goes straight to {SUPERVISOR}’s "
                   f"Google Drive.", body)


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
<p>A short-answer question (SAQ) asks for a focused answer that takes a few minutes to write. You give the definitions, the key points and an example or two, without an introduction or a conclusion. These five go with this week’s lectures:</p>
<ol class="titles">{saqs}</ol>
<p>They have a paper of their own in Supervision work {exam("s1-saqs", "open them")}. There’s no time limit, but about 10 minutes for each is a good aim, and you can answer as many as you like. After you submit, <b>Review my answers</b> shows you what a good answer covers.</p>

<h2 id="mo-rev">Essay titles for revision</h2>
<p>It’s worth noting these down. They go with this week’s lectures, and they’re the kind of title you could meet in the exam.</p>
<ol class="titles">{rev}</ol>
<p>Planning an answer to each one (your argument, your examples, and the order you’d put them in) is good revision. You could also write one up in Supervision work {exam("s1-revision", "open them")} in 40 minutes, for practice. After you submit, the guidance shows you the ground each title should cover.</p>
{optional(activity("If you want the practice", [
    task("mo-saq", 'Answer one or more of the short-answer questions, and submit them.', auto="exam:submit paper=s1-saqs"),
    task("mo-plan", 'Plan an answer to one of the revision titles. Sum up your position in a sentence, then jot down the three or four points, with examples, that would support it.'),
]), title='Practice')}
'''
    return chapter("s1-more", num, "More practice", "exam", "More practice: short answers and revision", None,
                   "This chapter is optional. It has five short-answer questions on this week’s lectures, and four more "
                   "essay titles to note down for revision. Only the essay needs to be handed in.", body)


def ALL():
    order = [ch_week, ch_clock, ch_where, ch_heart, ch_marking, ch_plag, ch_write, ch_more]
    return [f(str(i)) for i, f in enumerate(order)]
