"""The chapters of Supervision 5 (supervision-5.html): cardiac output, blood pressure and exercise.

The work to hand in is an essay in Supervision work (exams/s5-essay.json), on the title Dr Fraser suggests in his fifth
handout, which can't be answered well without the equations of the circulation. So the essay's chapter teaches how to
use an equation in an essay (with a worked example, and three questions on the slips essays make), and the guidance
the students read after submitting shows the equations at work. The short-answer questions (s5-saqs.json) and the two
other essay titles (s5-revision.json) are the ones the handouts suggest, and they're optional.

The chapters: what to do this week; two optional exercises, about half an hour in all (the heart rate through ten
minutes of cycling, and the baroreflex as someone stands up, in the Recorder; Dr Fraser's two equations run as Guyton's
model of the circulation in the Circuits tab, examples/circuits/exercise-circulation.circuit.json); writing the essay
and handing it in; and more practice. ALL() puts them in order.

The lecture handouts are Dr James Fraser's (the determinants of cardiac output; the control of arterial blood pressure;
the circulation under stress): nothing here is copied from them. The numbers in the model answers were measured in the
workbench: the exercise ECG's R–R intervals at the buttons' places (0.71 s, 84 a minute, near the start; 0.46 s, 130 a
minute, near the end); a beat of the standing-up recording before he stands (about 97/53 mmHg, mean 65) and at the
lowest pressure after (about 84/38, mean 51), with his heart rate rising from about 77 to about 105 a minute; and the
circuit's meters (rest: 83.3 mL/s, RAP 0, ABP 93 mmHg; the muscles dilated: ABP 18.6; the heart alone at 417 mL/s:
RAP −28; MSFP 17.5: RAP −17.5; the muscle pump as well: RAP 0, ABP 93; a haemorrhage, MSFP 3.5: RAP 0 at 41.7 mL/s,
ABP 46.5)."""
from lib import *

PAPER = 's5-essay'
ESSAY = ('Describe the cardiovascular responses during sustained exercise. What limits maximal exercise performance '
         'under these conditions?')
SAQS = [
    'Explain why increasing heart rate alone does not greatly increase cardiac output.',
    'A healthy person has an arterial blood pressure of 120/80 mmHg. Calculate the pulse pressure and estimate the mean '
    'arterial pressure. Then outline the reflex responses that would follow a sudden fall in arterial pressure.',
    'Explain why breath-hold diving and ascent to altitude produce different cardiovascular responses.',
]
REVISION = [
    '“The heart is necessary for cardiac output, but it does not normally limit it.” Discuss.',
    'Why is arterial blood pressure the principal controlled variable of the circulation? How is it regulated in '
    'exercise?',
]

CYCLE_START = 'exercise@10,16'       # the first seconds of ten minutes of cycling against a high resistance
CYCLE_END = 'exercise@575,581'       # …and the last
STANDING = 'bp-standing@25,75'       # blood pressure (finger) and heart rate as a young man stands up, at 41 s
MODEL = 'example:exercise-circulation'   # Guyton's model: VR = (MSFP − RAP) / RvR, ABP = CO × TPR

HANDIN_LINE = ('Once you’ve submitted it, <b>hand it in</b> from the same page before your supervision. You’ll need the '
               '<b>hand-in password</b> I give you, and your essay then goes straight into my Google Drive.')


def handin_box(buttons=True):
    """the essay to hand in, as the first thing the student sees"""
    b = (f'<p class="hb-acts">{goto("s5-write", "how to write it and hand it in")} {exam(PAPER, "open the essay")}</p>'
         if buttons else '')
    return f'''<div class="handin-box">
  <div class="hb-k">To hand in this week</div>
  <p class="hb-title">“{ESSAY}”</p>
  <ul>
    <li>You write the essay in <b>Supervision work</b>, as you have before and as you will in the online exam: in one sitting, without your notes, and without pasting anything in.</li>
    <li>This title needs <b>equations</b>, used to explain and to argue, not just quoted. Chapter 3 shows you how.</li>
    <li>There’s no time limit, but try to keep to about <b>40 minutes</b>.</li>
    <li>{HANDIN_LINE}</li>
  </ul>
  {b}
</div>'''


def optional(body, title='If you have time', hid=None):
    i = f' id="{hid}"' if hid else ''
    return f'<div class="optional">\n<h2{i}>{title}</h2>\n{body}\n</div>'


def optional_chapter(body):
    """a whole chapter that's optional: none of its steps or questions count towards finishing the page"""
    return f'<div class="optional whole">\n{body}\n</div>'


# ---------------------------------------------------------------------------------------------------------------------
def ch_week(num):
    body = f'''
{handin_box()}

<h2 id="w5-plan">The week, step by step</h2>
<ol class="plan">
<li>If you’d like to, start with <b>two short exercises</b>. They’re optional and take about half an hour altogether. In chapter 1 you measure, in the <b>Recorder</b>, a heart rate that climbs through ten minutes of cycling, and the baroreflex at work as someone stands up. In chapter 2 you run Dr Fraser’s two equations as a model of the circulation, in the <b>Circuits</b> tab, and find out what has to change for the cardiac output to rise five-fold. Both give you numbers for your essay. {goto("s5-rec", "start")}</li>
<li>Then read how to use equations in an essay, and <b>write your essay</b> and hand it in (chapter 3, about 50 minutes). {goto("s5-write", "go there")}</li>
<li>If you’d like more practice, chapter 4 has three short-answer questions, and two more essay titles to note down for revision. These are optional too. {goto("s5-more", "go there")}</li>
</ol>
{activity("Before you start", [
    task("w5-name", 'Check that your name is at the top of the page. If it says <b>Your name</b>, click it and add yours. It goes at the top of the essay you hand in, and every supervision’s page shares it.', check="named"),
])}

<h2 id="w5-how">How this page works</h2>
<ul>
<li>It works in the same way as the earlier ones. The steps tick themselves off as you do them, the buttons do things for you in the workbench on the right, and every question has a <b>model answer</b> you can look at once you’ve had a go.</li>
<li>Chapters 1, 2 and 4 are optional, so their steps don’t count towards finishing the page. The rest do.</li>
<li>If you haven’t used one of the workbench’s tabs before, the <a href="workbench.html" target="_blank" rel="noopener">workbench guide</a> shows you how it works.</li>
</ul>
'''
    return chapter("s5-week", num, "This week", "exam", "Supervision 5: cardiac output, blood pressure and exercise", 5,
                   "This week’s lectures are about what sets the cardiac output, how the arterial blood pressure is "
                   "controlled, and how the circulation copes with exercise, haemorrhage and hypoxia. They’re built on "
                   "a few equations, and the essay you hand in asks you to use them.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_rec(num):
    body = optional_chapter(f'''
{callout("info", "Optional, about 15 minutes", "<p>This exercise isn’t part of the work to hand in, and its steps don’t count towards finishing the page. It goes with Dr Fraser’s fourth and fifth lectures, and it gives you numbers you could use in your essay.</p>")}

<h2 id="ex-cycle">Ten minutes of cycling</h2>
<p>This recording is an ECG from the chest of a volunteer who cycled against a high resistance for ten minutes. Under the ECG is the volunteer’s heart rate, worked out from the beats.</p>
{activity("The heart rate in sustained exercise", [
    task("ex-open", f'Open the first few seconds of the recording {rec(CYCLE_START)}.', auto="rec:open id=exercise"),
    task("ex-start", f'Choose the <b>Calipers</b> {rectool("calipers", "show me")} and drag from the peak of one R wave to the peak of the next. The bar above the traces shows the interval (Δt) and the heart rate it gives.', auto="rec:measure id=exercise interval=R-R to<60"),
    task("ex-end", f'Now go to the last few seconds of the ten minutes {rec(CYCLE_END)}, and measure an R–R interval there too.', auto="rec:measure id=exercise interval=R-R from>540"),
])}
{q("ex-q-rate", "How much did the heart rate rise? Pacing a resting heart this much faster would hardly change its output. Why does the same rise in rate help in exercise? Use CO = HR × SV and VR = (MSFP − RAP) / RvR.",
   "It rose by about half, from about 84 beats a minute at the start (an R–R interval of about 0.71 s) to about 130 at the end (0.46 s), and it was still rising after ten minutes. CO = HR × SV, so a faster heart raises the output only if each beat still ejects as much blood. Pace a resting heart faster and it doesn’t. Venous return is set by VR = (MSFP − RAP) / RvR, and RAP is already close to zero, so the extra beats can’t draw much more blood back. Each beat fills less, SV falls and CO hardly changes. In exercise, venous return rises at the same time, because sympathetic venoconstriction raises MSFP and the muscle pump lowers RvR. The faster heart, made more forceful by sympathetic stimulation through β<sub>1</sub>-adrenoceptors, pumps that extra blood without letting RAP rise. So SV is kept up, or even rises, as HR rises, and CO rises at least as much as the heart rate, here by half or more, and up to five-fold at maximal effort.")}

<h2 id="ex-stand">Standing up</h2>
<p>When you stand up, about half a litre of blood pools in the veins of your legs. In this recording a healthy young man stood up by himself from lying flat on a tilt table (the table didn’t move), with his blood pressure measured beat by beat at a finger, and an ECG.</p>
{activity("The baroreflex, in the Recorder", [
    task("st-open", f'Open the recording, from 16 s before he stands up to 34 s after {rec(STANDING)}. A flag marks the moment he stands up, and the heart rate is at the bottom. The pressure rises for a beat or two just before the flag, as he braces himself to get up.', auto="rec:open id=bp-standing"),
    task("st-before", 'With the calipers, drag across one beat of the blood pressure from before he stands up, from the lowest point of one pulse to the lowest point of the next. Choose a beat before 37 s, before he starts to move. The bar above the traces now shows the minimum pressure (the diastolic), the maximum (the systolic) and the mean.', auto="rec:measure id=bp-standing signal=bp to<41 dt>0.5 dt<1.3"),
    task("st-low", 'Do the same for a beat at the lowest pressure, a few seconds after he stands up.', auto="rec:measure id=bp-standing signal=bp from>42 to<50 dt>0.4 dt<1.3"),
])}
{q("st-q-map", "Use the minimum and maximum of your beat from before he stood up to estimate his mean arterial pressure, with MAP ≈ D + (S − D) / 3. How close is your estimate to the mean that the Recorder measured? And why is the mean nearer to the diastolic pressure than to the systolic?",
   "For a beat at about 33 s, the pressure was about 97/53 mmHg. The pulse pressure was about 44 mmHg, so MAP ≈ 53 + 44/3 ≈ 68 mmHg. The Recorder measured a mean of about 65 mmHg, so the estimate was within about 3 mmHg (your beat will give slightly different numbers). The mean is nearer to the diastolic pressure because the pressure spends more of each cycle near it. It rises quickly to a brief peak while the ventricle ejects, then falls slowly through diastole, which is the longer part of the cycle at rest. The one-third rule is only an approximation, and how well it works depends on the shape of the pressure wave.")}
{q("st-q-baro", "What made his pressure fall when he stood up, in terms of ABP = CO × TPR? And how did his body bring it back? Use your numbers, and the heart rate.",
   "Within a few seconds his mean pressure fell from about 65 to about 51 mmHg (a beat of about 84/38 mmHg). He stood up by himself, and that lowers both terms. For the first few seconds, the leg muscles that lift him dilate their own arterioles, as at the start of exercise, so TPR falls. Then, as he stays upright, blood pools in the veins of his legs and it’s harder for blood to get back to the heart. Venous return and RAP fall, by Starling’s law each beat ejects less, and CO falls. (On a tilt table that tips you up while your muscles stay relaxed, the fall in CO is the main challenge.) The baroreceptors of the carotid sinus and aortic arch then fire less, so the medulla reduces vagal activity to the heart and raises sympathetic activity. His heart rate rose from about 77 to about 105 a minute within about ten seconds. Sympathetic nerves also constrict the arterioles, which raises TPR, and the veins, which raises MSFP and so venous return. His pressure was back about ten seconds after he stood up. It then overshot, to about 130/70 mmHg, and his heart rate fell back for a few beats as the baroreflex now worked the other way, before both settled, with his heart rate higher than when he was lying down.")}
''')
    return chapter("s5-rec", num, "Exercise and standing", "recorder", "Optional: exercise and standing up", 15,
                   "Measure, in the Recorder, how the heart rate climbs through ten minutes of cycling, and how the "
                   "baroreflex brings the blood pressure back when someone stands up.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_model(num):
    bleed = optional(f'''{activity("A haemorrhage", [
    task("md-bleed", 'Put the model back to rest. Open both switches, and set MSFP to 7 mmHg and the heart to 83.3 mL/s. Now imagine losing a tenth of the blood. Without venoconstriction that roughly halves MSFP, because only about the last fifth of the blood volume stretches the walls of the vessels. So set MSFP to 3.5 mmHg.', auto="circuit:measure kind=voltmeter label~MSFP value>3 value<4"),
])}
{q("md-q-bleed", "With the heart still pumping 83.3 mL/s, what is RAP? Now find the heart’s output that brings RAP back to zero. What is it in litres a minute, and what is ABP then?",
   "With the heart at 83.3 mL/s, RAP falls to −3.5 mmHg, below the point where real veins collapse, so the body couldn’t keep that output up. RAP is back at zero when the heart pumps 41.7 mL/s, which is 2.5 L/min, half its resting output, because VR = MSFP / RvR = 3.5 / 0.084. With nothing to compensate, as in the model, ABP = CO × TPR would then fall to about 46.5 mmHg, half its resting value. So a haemorrhage threatens the blood pressure through MSFP, venous return and CO, not through TPR. In the body the reflexes act on each term as the blood is lost, so a loss this small barely lowers the pressure. Sympathetic venoconstriction raises MSFP again, arteriolar constriction raises TPR, and the heart’s rate and contractility rise.",
   accept="num:2.5±0.15", placeholder="litres a minute")}''')
    body = optional_chapter(f'''
{callout("info", "Optional, about 15 minutes", "<p>This exercise isn’t part of the work to hand in, and its steps don’t count towards finishing the page. It goes with Dr Fraser’s third and fifth lectures, and it gives you numbers you could use in your essay.</p>")}

<p>Dr Fraser’s two equations make a model of the circulation that you can run. In it, the <b>mean systemic filling pressure</b> (MSFP) is a pressure source, which drives venous return to the right atrium through the <b>resistance to venous return</b> (RvR), so that VR = (MSFP − RAP) / RvR. The heart is a flow source, which pumps into the arteries whatever flow you set. From there the blood flows back through the arterioles, the <b>total peripheral resistance</b> (TPR), so that ABP = CO × TPR. The Circuits tab shows pressures in mmHg, flows in mL/s (5 L/min is 83.3 mL/s) and resistances in mmHg·s/mL.</p>
{callout("tip", "A model, not a body", "<p>The veins of this model are rigid, so venous return keeps rising however far the heart pulls RAP down. Real veins collapse once the pressure inside them falls 1 or 2 mmHg below zero, so venous return stops rising there. The model has no compliances (stretchy vessels) either, so it shows only steady states. A real heart also sets its own output. By Starling’s law it pumps what returns to it, which keeps RAP close to zero. Here you set the heart’s output yourself.</p>")}

<h2 id="md-rest">At rest</h2>
{activity("The circulation at rest", [
    task("md-open", f'Open the model {circuit(MODEL, "show me")} and run it {circuitrun("show me")}. The two flowmeters show that venous return and cardiac output are both 83.3 mL/s (5 L/min). In a steady circulation they have to be equal. RAP is close to 0 mmHg, and ABP is 93 mmHg.', auto="circuit:run name~Guyton"),
])}

<h2 id="md-ex">Exercise</h2>
{activity("Five times the cardiac output", [
    task("md-muscle", 'Start exercising. Click the switch <b>Exercising muscles</b> to close it. Closing it connects the working muscles’ dilated arterioles alongside the others, and TPR falls to a fifth of its resting value. Watch ABP.', auto="circuit:switch label~Exercising on=true"),
    task("md-heart", 'Can the heart put this right on its own? Click the <b>Heart</b>, and in the panel on the right, set its flow to 417 mL/s (25 L/min, five times its resting output).', auto="circuit:measure kind=ammeter label~Cardiac value>400"),
])}
{q("md-q-heart", "When the muscles’ arterioles dilated, ABP fell to about 19 mmHg. Why? And with the heart pumping 417 mL/s, ABP is back to 93 mmHg. What has happened to RAP, and why couldn’t a real heart do this?",
   "With CO unchanged, ABP = CO × TPR fell to a fifth, from 93 to about 19 mmHg, because TPR fell to a fifth. Pumping five times as much restores ABP, but RAP falls to about −28 mmHg. With MSFP and RvR unchanged, VR = (MSFP − RAP) / RvR can only rise five-fold if RAP falls far below zero: (7 + 28) / 0.084 = 417 mL/s. Real veins collapse once the pressure in them falls 1 or 2 mmHg below zero, so venous return would stop rising long before that. A heart that pumps harder can only lower RAP, and RAP is already close to zero at rest, so the heart can’t pull more blood out of the veins. That’s why pacing the heart faster doesn’t raise the cardiac output. The heart is needed for cardiac output, but it doesn’t normally limit it.")}
{activity("The veins", [
    task("md-veno", 'Sympathetic venoconstriction raises MSFP two- to three-fold. Click the pressure source <b>Mean systemic filling pressure</b>, and raise it from 7 to 17.5 mmHg (2.5-fold).', auto="circuit:measure kind=voltmeter label~MSFP value>17"),
    task("md-pump", 'The muscle pump about halves RvR. Close the switch <b>Muscle pump</b>, which puts a second path of the same resistance beside RvR.', auto="circuit:switch label~pump on=true"),
])}
{q("md-q-vr", "With MSFP at 17.5 mmHg and RvR halved, what are RAP and ABP now? What does each change do in VR = (MSFP − RAP) / RvR, and what does the heart still have to do?",
   "RAP is back to about 0 mmHg, with 417 mL/s (25 L/min) returning and being pumped, and ABP stays at 93 mmHg. Raising MSFP 2.5-fold raises the pressure that drives venous return, and halving RvR doubles the flow that the same pressure difference can drive, so together they let venous return rise 2.5 × 2 = 5-fold with RAP still close to zero. You fixed the heart’s output here, so the venous changes only brought RAP back up to zero. In the body it’s the other way round. Starling’s law holds RAP close to zero, and the output follows venous return up. The heart’s job is to pump that larger venous return without RAP rising, and less vagal activity and more sympathetic activity raise its rate and its contractility, so it can. In Guyton’s curves, the venous return curve and the cardiac function curve both move up, and they cross at a much higher cardiac output with RAP still close to zero. In the body, ABP rises a little in exercise rather than staying the same, because central command resets the baroreflex to a higher set point.")}
{mcq("md-q-max", "In this model, what sets the highest cardiac output that can be reached with RAP at zero?", [
    ("How hard the heart can pump", False, "No. Pumping harder only lowers RAP. In this model RAP just keeps falling, but in the body the veins would collapse, and venous return would stop rising."),
    ("MSFP and RvR, through venous return", True, "Yes. With RAP at zero, VR = MSFP / RvR, so the highest cardiac output is set on the venous side: how far venoconstriction (and the blood volume) can raise MSFP, and how far the muscle pump can lower RvR."),
    ("TPR", False, "No. TPR sets the arterial pressure that a cardiac output makes (ABP = CO × TPR), but not how much blood returns to the heart. Open and close <b>Exercising muscles</b>, and watch RAP. It doesn’t change."),
    ("ABP", False, "No. ABP is set by CO and TPR. It doesn’t drive venous return."),
])}
{bleed}
''')
    return chapter("s5-model", num, "A model of exercise", "circuit", "Optional: exercise in a model of the circulation",
                   15, "Run Dr Fraser’s two equations as a model of the circulation in the Circuits tab, and find out "
                   "what has to change for the cardiac output to rise five-fold.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_write(num):
    hand_note = callout("info", "Handing in", "<p>Your essay goes straight from this page into my Google Drive, and you don’t need a Google account for that. The hand-in password I give you stops anyone else from handing work in, so please keep it to yourself. Once your essay has arrived, the page tells you so and gives you a receipt. If it can’t be handed in, the page will tell you why. If you try again and it still won’t go, download a copy and send it to me some other way.</p>")
    example = callout("tip", "One equation, quoted and used", (
        "<p><b>Quoted:</b> “Haemorrhage lowers the blood pressure, as ABP = CO × TPR. The baroreceptors detect the fall "
        "and the sympathetic nervous system is activated, which increases heart rate, contractility and TPR, so the "
        "blood pressure returns to normal.”</p>"
        "<p><b>Used:</b> “A haemorrhage threatens the arterial pressure through the cardiac output, not through TPR. "
        "Venous return is VR = (MSFP − RAP) / RvR, and MSFP depends on the stressed volume, only about the last fifth of "
        "the blood volume. So without venoconstriction, losing a tenth of the blood would roughly halve MSFP. RAP is "
        "already close to zero, so if nothing compensated, venous return would fall by about half, and so would the "
        "cardiac output and, by ABP = CO × TPR, the arterial pressure. In fact the reflexes act on each term as the "
        "blood is lost, so a loss this small barely lowers the pressure. Sympathetic venoconstriction raises MSFP "
        "again, arteriolar constriction raises TPR, and a faster, more forceful heart pumps the restored venous return "
        "without RAP rising.”</p>"
        "<p>The first quotes an equation and moves on. The second says which term changes and why, puts a number on "
        "it, and shows how each response acts on a term of the equations. Your essay can do the same for exercise.</p>"))
    body = f'''
<p class="essay-title">“{ESSAY}”</p>

<h2 id="es5-title">Thinking about the title</h2>
<p>The title has two parts. The first asks you to <b>describe</b> the responses, but the best essays also explain what each response does, and why the body needs it. The second asks what <b>limits</b> maximal performance, and that needs an argument. Weigh up the evidence for each possible limit (the lungs, the heart, the muscles and the circulation as a whole), and come to a conclusion. Leave yourself time for it, because it’s where many essays run out of steam.</p>
<p><b>Sustained</b> exercise here means dynamic exercise with large groups of muscles, kept up for minutes at a time, like the cycling in chapter 1. These questions might help you plan.</p>
<ul>
<li><b>In the muscles.</b> How does their blood flow rise so fast at the start, and what keeps it up once exercise is sustained?</li>
<li><b>In the whole circulation.</b> What does that do to TPR, and so to ABP? What must the cardiac output do, and how does venous return rise to match it? Chapter 2 has numbers for this.</li>
<li><b>The control.</b> What drives the changes in sympathetic and vagal activity, and why couldn’t feedback from the baroreceptors do it alone? What happens to ABP?</li>
<li><b>The limits.</b> In a fit person, which limits maximal exercise: the lungs, the heart, the muscles or the circulation? What’s the evidence? Is the answer the same for someone who is unfit, or ill? Dr Fraser’s “O<sub>2</sub> delivery is flow × concentration” can frame this.</li>
</ul>

<h2 id="es5-eq">Using equations in your essay</h2>
<p>This title needs equations, and Dr Fraser’s handout suggests building your answer on two of them: ABP = CO × TPR, and CO = VR = (MSFP − RAP) / RvR. An equation earns its place in an essay when it does some work, organising your answer, making a prediction or putting a number on something. Written once at the start and never used again, it earns nothing. Here’s how to make one work.</p>
<ol class="plan">
<li><b>Write it out, and say what each term is.</b> “Venous return is VR = (MSFP − RAP) / RvR, where MSFP is the mean systemic filling pressure, RAP the right atrial pressure and RvR the resistance to venous return.” Give typical values where you can, such as an MSFP of about 7 mmHg and an RAP close to zero.</li>
<li><b>Say what it means, and what it doesn’t.</b> ABP = CO × TPR is flow = pressure difference / resistance, applied to the whole systemic circulation, with RAP taken as zero. It says how the three are related, not what causes what. CO = HR × SV is always true, because it’s how the cardiac output is defined, but it doesn’t mean that a faster heart pumps more blood. Pace a heart faster and SV falls.</li>
<li><b>Use it as a plan.</b> Take the terms one at a time. For each one, ask what happens to it in exercise, by what mechanism, and by how much. Then the equation tells you what has to happen to the others.</li>
<li><b>Put numbers in.</b> If TPR falls to a fifth of its resting value and ABP is to stay up, the cardiac output has to rise five-fold. If MSFP rises 2.5-fold and RvR halves, venous return can rise 2.5 × 2 = 5-fold, with RAP still close to zero. Say where your numbers come from.</li>
<li><b>Use it to argue.</b> An equation shows what can happen and what can’t. Venous return can’t rise just because the heart pumps harder, because the great veins collapse once RAP falls much below zero. That’s the kind of point the second half of the title asks for.</li>
</ol>
{example}
<p>Here are three sentences of the kind that essays on this topic often contain. Is each one right? If not, what’s wrong with it?</p>
{mcq("es5-q-hr", "“In exercise the cardiac output rises because the heart beats faster (CO = HR × SV).”", [
    ("It’s right. SV stays about the same in exercise, so CO rises in step with HR", False, "Not quite. Paced faster with nothing else changed, the heart pumps hardly any more, because each beat fills less and SV falls. SV holds up in exercise only because venous return rises too."),
    ("It leaves out venous return. A faster heart only helps because venous return rises too", True, "Yes. CO = VR = (MSFP − RAP) / RvR. Venoconstriction raises MSFP and the muscle pump lowers RvR, and the faster, more forceful heart pumps the extra blood without RAP rising. It takes both equations to explain it."),
    ("It’s the wrong way round. In exercise SV rises, and the heart rate hardly changes", False, "No. The heart rate rises a lot (in chapter 1, from about 84 to 130 a minute), but on its own that isn’t enough."),
])}
{mcq("es5-q-veno", "“Sympathetic venoconstriction raises the blood pressure by increasing TPR.”", [
    ("It’s right. Constricting any blood vessel adds to the resistance, so TPR rises", False, "Not quite. TPR is set mainly by the arterioles. Constricting the veins acts on a different term of the equations."),
    ("Arterioles and veins are both constricted, so TPR and MSFP rise by the same amount", False, "No. Sympathetic nerves constrict both, but they act on different terms. Constricting the arterioles raises TPR, and constricting the veins raises MSFP."),
    ("Venoconstriction raises MSFP, not TPR, so venous return rises, and with it CO and ABP", True, "Yes. TPR is set mainly by the arterioles, but they hold less than 1% of the blood. The small veins and venules hold over half of it, so constricting them raises MSFP, and venous return with it, without changing TPR much."),
])}
{mcq("es5-q-pump", "“In exercise the muscle pump raises MSFP.”", [
    ("It lowers RvR instead, helping blood back to the heart without changing MSFP", True, "Yes. The working muscles squeeze the veins inside them, and the veins’ valves send the blood towards the heart. In Guyton’s curves this makes the venous return curve steeper without moving the point where it meets the axis, which is MSFP."),
    ("It’s right. Squeezing the veins of the legs raises the pressure in them, and so MSFP", False, "Not quite. Squeezing a vein raises the pressure in it for a moment, but it doesn’t change the blood volume or the tone of the veins, which set MSFP. What it does is help the blood back to the heart, which lowers RvR."),
    ("It lowers RAP, and that is what raises venous return", False, "No. The heart holds RAP close to zero, at rest and in exercise. The muscle pump acts on RvR, the resistance to venous return."),
])}

<h2 id="es5-before">Before you start</h2>
<ul>
<li>Look back at the feedback on your earlier essays, and pick one thing to do better this time. If you’d like a reminder of the six criteria I mark against, they’re in <a href="supervision-1.html#s1-marking" target="_blank" rel="noopener">Supervision 1, chapter 4</a>.</li>
<li>Revise the lectures first if you like. Then put your notes away and find about 45 minutes when you won’t be interrupted.</li>
<li>Make sure you have the <b>hand-in password</b> I gave you, because you’ll need it at the end. You won’t find it anywhere on this site.</li>
<li>Give yourself about <b>40 minutes</b>, as you would in the exam, and spend the first five of them planning. The clock at the top of the paper tells you when you reach 40 minutes.</li>
<li><b>Writing equations.</b> Type a simple one straight into your text, as you would write it by hand: ABP = CO × TPR (× is among the special characters, under <b>Ω</b>, or just type x). For one with a fraction, use the formula tool, <b>Σ</b>. Type, say, <code>VR = \\frac{{MSFP - RAP}}{{RvR}}</code>, check the preview and press <b>Insert</b>. Either way, say what the equation means straight after it.</li>
<li>A diagram can help too: Guyton’s curves at rest and in exercise, say, or a flow diagram of how the medulla controls the heart and the vessels. Draw it with <b>Insert drawing</b> (the pencil), or draw it on paper and add a photo of it with <b>Insert picture</b>. Type a caption under it, and refer to it in your text.</li>
</ul>
{activity("Write it, and hand it in", [
    task("es5-start", f'Open the essay {exam(PAPER, "show me")}, read its first page, and press <b>Start</b> when you’re ready to write.', auto=f"exam:start paper={PAPER}", check=f"paper:{PAPER}.started"),
    task("es5-write", 'Plan, then write. Aim for an introduction that says what your essay will argue, paragraphs that each make one point and show how it helps to answer the question, and a conclusion that draws them together. Use the equations to carry the argument.', auto=f"exam:words paper={PAPER} words>299"),
    task("es5-submit", 'When you’ve finished, go to the submission page (the ✓ tile at the bottom right), check your essay and submit it.', auto=f"exam:submit paper={PAPER}", check=f"paper:{PAPER}.submitted"),
    task("es5-send", 'Hand it in on the page that comes up next. Type in the hand-in password and press <b>Hand it in</b>. The page shows you a receipt once your essay has arrived.', auto=f"exam:handin paper={PAPER} step=confirmed", check=f"paper:{PAPER}.handedIn"),
    task("es5-word", 'To keep a copy, press <b>Download your copy</b>. Before you hand in, the same button is under the password box, and it’s called <b>Download a copy for yourself</b>. The copy is saved as a Word document, usually in your Downloads folder.', auto=f"exam:download paper={PAPER} format=docx", check=f"paper:{PAPER}.downloaded"),
])}
{hand_note}
{callout("info", "After you’ve handed it in", "<p>Once you’ve submitted, <b>Review my answers</b> shows you the ground a good answer would cover, and how the equations carry it. Read it after you’ve handed your essay in, and make a note of what you’d add or change. That’s what we’ll talk about in the supervision.</p><p>Your essay is kept in this browser, in Files → <code>essays</code>. It won’t be there on another computer, and some shared computers clear it when you log out, so download a copy before you finish.</p>")}
{q("es5-q-next", "Once you’ve read the guidance, where in your essay could an equation have done more work, and what would it have shown?",
   "There’s no single right answer here, so bring yours to the supervision. Many essays on this title quote ABP = CO × TPR at the start, then describe the responses without coming back to it. The equations can carry the whole first half: TPR falls to about a fifth, so the cardiac output has to rise about five-fold, and VR = (MSFP − RAP) / RvR shows how (MSFP up 2.5-fold, RvR halved, RAP held near zero by the heart). In the second half, the same equation shows why the heart alone can’t raise the cardiac output, and O<sub>2</sub> uptake = flow × the O<sub>2</sub> extracted from each litre of blood shows why the one-leg and two-leg experiments point to the circulation as the limit.")}
'''
    return chapter("s5-write", num, "Write your essay", "exam", "Write your essay, and hand it in", 50,
                   "This is the work to hand in this week. As before, you write it in Supervision work, as you will in "
                   "the online exam, and then hand it in from the same page. First, though, a few minutes on how to "
                   "use equations in an essay, because this title needs them.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_more(num):
    saqs = ''.join(f'<li>{s}</li>' for s in SAQS)
    rev = ''.join(f'<li>{s}</li>' for s in REVISION)
    body = f'''
<h2 id="m5-saq">Short-answer questions</h2>
<p>These three go with this week’s lectures, one with each. Each is marked out of five, so answer in bullet points and aim for at least five separate points. Each one can be answered with an equation as its frame.</p>
<ol class="titles">{saqs}</ol>
<p>They have a paper of their own in Supervision work {exam("s5-saqs", "open them")}. There’s no time limit, but about 10 minutes for each is a good aim. After you submit, <b>Review my answers</b> shows you what a good answer covers.</p>

<h2 id="m5-rev">Essay titles for revision</h2>
<p>It’s worth noting these down. They go with Dr Fraser’s third and fourth lectures, and they’re the kind of title you could meet in the exam. Each needs the same equations as this week’s essay.</p>
<ol class="titles">{rev}</ol>
<p>Planning an answer to each one (your argument, your evidence, and the order you’d put them in) is good revision. You could also write one up in Supervision work {exam("s5-revision", "open them")} in 40 minutes, for practice. After you submit, the guidance shows you the ground each title should cover.</p>
{optional(activity("If you want the practice", [
    task("m5-saq", 'Answer one or more of the short-answer questions, and submit them.', auto="exam:submit paper=s5-saqs"),
    task("m5-plan", 'Plan an answer to one of the revision titles. Sum up your position in a sentence, then jot down the three or four points, with the evidence for each, that would support it. Note which equation each point uses.'),
]), title='Practice')}
'''
    return chapter("s5-more", num, "More practice", "exam", "More practice: short answers and revision", None,
                   "This chapter is optional. It has three short-answer questions on this week’s lectures, and two "
                   "more essay titles to note down for revision. Only the essay needs to be handed in.", body)


def ALL():
    order = [ch_week, ch_rec, ch_model, ch_write, ch_more]
    return [f(str(i)) for i, f in enumerate(order)]
