"""The chapters of Supervision 4 (supervision-4.html): the heart and the circulation.

The work to hand in is an essay in Supervision work (exams/s4-essay.json), on the title Prof. Giussani suggests in his
handout. The short-answer questions (s4-saqs.json) and the two other essay titles (s4-revision.json) are the ones the
handouts suggest, and they're optional.

The chapters: what to do this week; two optional exercises, about half an hour in all (cardiac muscle in the
Microscope, and the parts of a heartbeat measured in the ECG and the heart sounds in the Recorder; Furchgott's
experiment on rings of rat aorta in the Organ bath); writing the essay and handing it in; and more practice. ALL() puts
them in order.

The lecture handouts are Prof. Dino Giussani's (the heart and cardiac muscle) and Dr James Fraser's (capillary exchange;
arterioles): nothing here is copied from them. The numbers in the model answers were measured in the workbench: the
heart sounds' marked S1 and S2 (systole 0.26 s and diastole 0.53 s on average, at 75 beats a minute), the PR (0.18 s)
and QT (0.36 s) intervals of the beat the button opens in lead II of the 12-lead ECG, and the organ bath's ring of aorta
from seed 1 (acetylcholine 10⁻⁶ M relaxes 83% of phenylephrine's tone with the endothelium and 2% without it;
nitroprusside relaxes all of it; acetylcholine 10⁻⁴ M contracts the rubbed ring by about 0.55 g)."""
from lib import *

PAPER = 's4-essay'
ESSAY = ('Explain how the structural and electrical properties of cardiac muscle enable coordinated, rhythmic pumping '
         'of blood while allowing relaxation between beats.')
SAQS = [
    'A left ventricle has an EDV of 120 mL and an ESV of 50 mL. Sketch and label its pressure–volume loop. Identify the '
    'four valve events and the phases during which both valves are closed. Calculate stroke volume and indicate when '
    'S1 and S2 occur.',
    'What factors influence water movement between plasma and interstitial fluid?',
    'Explain how the endothelium can cause vasodilatation of arterioles.',
]
REVISION = [
    'Discuss the factors that govern the exchange of solutes and water across the capillary wall, and explain how '
    'disturbances of these factors can lead to oedema.',
    'Arteriolar resistance must meet the needs of individual tissues while also maintaining arterial blood pressure. '
    'Discuss how these demands may conflict and how they are reconciled.',
]

HEART = 'heart@1.779,2.273,20x'          # cardiac muscle cut lengthways, with intercalated discs
SOUNDS = 'heart-sounds@0.4,2.4'          # the heart sounds (S1 and S2 marked) with an ECG
TWELVE = 'ecg-12lead@1.1,2.1:II'         # one beat of lead II: P, QRS and T
BLOCK = 'ecg-block@8,20'                 # second-degree (2:1) heart block
RING = 'aorta?seed=1'                    # a ring of rat aorta with its endothelium (the same for everyone)
RUBBED = 'aorta?endothelium=off&seed=1'  # …and one from the same aorta with its endothelium rubbed off

HANDIN_LINE = ('Once you’ve submitted it, <b>hand it in</b> from the same page before your supervision. You’ll need the '
               '<b>hand-in password</b> I give you, and your essay then goes straight into my Google Drive.')


def handin_box(buttons=True):
    """the essay to hand in, as the first thing the student sees"""
    b = (f'<p class="hb-acts">{goto("s4-write", "how to write it and hand it in")} {exam(PAPER, "open the essay")}</p>'
         if buttons else '')
    return f'''<div class="handin-box">
  <div class="hb-k">To hand in this week</div>
  <p class="hb-title">“{ESSAY}”</p>
  <ul>
    <li>You write the essay in <b>Supervision work</b>, as you have before and as you will in the online exam: in one sitting, without your notes, and without pasting anything in.</li>
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

<h2 id="w4-plan">The week, step by step</h2>
<ol class="plan">
<li>If you’d like to, start with <b>two short exercises</b>. They’re optional and take about half an hour altogether. In chapter 1 you look at cardiac muscle in the <b>Microscope</b>, then measure the parts of a heartbeat in the ECG and the heart sounds, in the <b>Recorder</b>. That one goes with your essay. In chapter 2 you repeat Furchgott’s experiment on rings of aorta in the <b>Organ bath</b>, the experiment that showed how the endothelium makes arteries relax. {goto("s4-beat", "start")}</li>
<li>Then <b>write your essay</b> and hand it in (chapter 3, about 45 minutes). {goto("s4-write", "go there")}</li>
<li>If you’d like more practice, chapter 4 has three short-answer questions, and two more essay titles to note down for revision. These are optional too. {goto("s4-more", "go there")}</li>
</ol>
{activity("Before you start", [
    task("w4-name", 'Check that your name is at the top of the page. If it says <b>Your name</b>, click it and add yours. It goes at the top of the essay you hand in, and every supervision’s page shares it.', check="named"),
])}

<h2 id="w4-how">How this page works</h2>
<ul>
<li>It works in the same way as the earlier ones. The steps tick themselves off as you do them, the buttons do things for you in the workbench on the right, and every question has a <b>model answer</b> you can look at once you’ve had a go.</li>
<li>Chapters 1, 2 and 4 are optional, so their steps don’t count towards finishing the page. The rest do.</li>
<li>If you haven’t used one of the workbench’s tabs before, the <a href="workbench.html" target="_blank" rel="noopener">workbench guide</a> shows you how it works.</li>
</ul>
'''
    return chapter("s4-week", num, "This week", "exam", "Supervision 4: the heart and the circulation", 5,
                   "This week’s lectures start on the cardiovascular system: the heart as a pump and the muscle it’s "
                   "made of, the exchange of solutes and water across the walls of the capillaries, and how the "
                   "arterioles control the flow of blood through each tissue. The essay you hand in is about the heart.",
                   body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_beat(num):
    block = optional(f'''{activity("When the atria and ventricles part company", [
    task("hb-block", f'Open a recording of second-degree heart block {rec(BLOCK, "show me")}. Some of the P waves, marked <i>blocked P</i>, aren’t followed by a QRS at all.', auto="rec:open id=ecg-block"),
])}
{q("hb-q-block", "In the stretch where only every other P wave is followed by a QRS, the ventricles beat at half the rate of the atria. What does that tell you about the atrioventricular node?",
   "That it’s the only route by which excitation reaches the ventricles. The P waves keep their regular rhythm, because the sinoatrial node goes on setting the rate of the atria. But each time the AV node fails to conduct, no QRS follows, and the ventricles miss a beat. In a 2:1 block only every other P wave gets through. If conduction through the node failed completely (third-degree block), the ventricles would be left to a slower pacemaker of their own, at perhaps 30 to 40 beats a minute, which is too slow for most people to manage on, and why they’re given artificial pacemakers.")}''')
    body = optional_chapter(f'''
{callout("info", "Optional, about 15 minutes", "<p>This exercise isn’t part of the work to hand in, and its steps don’t count towards finishing the page. It goes with Professor Giussani’s lecture, and it gives you evidence and numbers you could use in your essay.</p>")}

<h2 id="hb-cells">Cardiac muscle</h2>
<p>Last week you looked at skeletal muscle. Cardiac muscle is striated too, but its cells are built and joined to each other differently, and those differences are much of what makes the heart work as a pump.</p>
{activity("Cardiac muscle, in the Microscope", [
    task("hb-open", f'Open a section of the wall of the left ventricle, at 20× {scope(HEART, "show me")}. These cells were cut lengthways. Each usually has one nucleus, in the middle of the cell, and the cells branch and join their neighbours.', auto="scope:open slide=heart"),
    task("hb-disc", f'Look for short, dark lines that cross the cells, often in steps. These are the <b>intercalated discs</b>, where one cell meets the next. Choose the <b>Label</b> tool {scopetool("label", "show me")} and label one of them <i>Intercalated disc</i>. Zoom in if that helps.', auto="scope:label slide=heart text~intercal"),
    task("hb-nuc", 'Label a nucleus too, and call it <i>Nucleus</i>. The brown granules beside some of the nuclei are lipofuscin, a pigment that builds up in heart cells with age.', auto="scope:label slide=heart text~nucle"),
])}
{q("hb-q-discs", "How are cardiac muscle cells joined to each other, and why does that matter for the heart as a pump? Compare them with skeletal muscle fibres.",
   "At the intercalated discs, the cells are joined by two kinds of junction. Desmosomes hold the cells together and pass the force of each cell on to the next, so that the pull of the whole wall adds up. Gap junctions connect the cytoplasm of neighbouring cells, so that current flows from one to the next, and an action potential that starts in one cell spreads to all of them. So the heart works as a functional syncytium. Once the pacemaker fires, the whole of the atria, and then the whole of the ventricles, are excited and contract together, which is what a pump needs. Skeletal muscle fibres have no intercalated discs. Each is electrically separate and is excited by its own motor neuron at a neuromuscular junction, so the nervous system can grade the force of a muscle by recruiting more or fewer motor units. The heart can’t do that, because every cell contracts in every beat. Its force is graded instead by how much Ca²⁺ each cell releases, and by how far the cells are stretched before they contract.")}

<h2 id="hb-sounds">The heart sounds and the ECG</h2>
<p>The ECG records the heart’s electrical activity from the surface of the body. The <b>P wave</b> comes as the atria depolarise, the <b>QRS complex</b> as the ventricles depolarise, and the <b>T wave</b> as the ventricles repolarise. The heart sounds come from the valves closing. Recording the two together shows how the electrical events lead to the mechanical ones.</p>
{activity("The heart sounds, in the Recorder", [
    task("hb-snd", f'Open a recording of the heart sounds, made with an electronic stethoscope, with an ECG recorded at the same time {rec(SOUNDS, "show me")}. The start of the first sound of each beat is marked S1, and the start of the second S2.', auto="rec:open id=heart-sounds"),
    task("hb-listen", f'If you can, listen to it. Switch the sound on {rectool("listen", "show me")} and press Play {rectool("play", "show me")}. Headphones help.', auto="rec:play id=heart-sounds on=true"),
    task("hb-sys", f'Choose the <b>Calipers</b> {rectool("calipers", "show me")} and, on the heart sounds, drag from the start of an S1 to the start of the S2 that follows it. That’s <b>systole</b>, while the ventricles contract and eject blood.', auto="rec:measure id=heart-sounds signal=pcg dt>0.15 dt<0.4"),
    task("hb-dia", 'Now drag from the start of that S2 to the start of the next S1. That’s <b>diastole</b>, while the ventricles relax and fill.', auto="rec:measure id=heart-sounds signal=pcg dt>0.4 dt<0.75"),
])}
{q("hb-q-sounds", "Why does S1 come just after the QRS, and S2 near the end of the T wave? And which lasts longer at rest, systole or diastole?",
   "S1 is heard as the atrioventricular (mitral and tricuspid) valves close at the start of ventricular systole. The QRS is the ventricles depolarising, and their contraction follows that electrical activation. As soon as the pressure in the ventricles rises above the pressure in the atria, the AV valves are pushed shut. S2 is heard as the aortic and pulmonary valves close at the end of systole. The T wave is the ventricles repolarising, and as they relax, the pressure in them falls below the pressure in the arteries, so the semilunar valves close. In this recording systole lasts about 0.26 s and diastole about 0.53 s, at about 75 beats a minute, so diastole is about twice as long. As the heart rate rises, diastole shortens much more than systole. That leaves less time for the ventricles to fill, and for blood to flow through the coronary arteries of the left ventricle, which happens mostly in diastole.")}
<p>Now look at the intervals of the ECG itself, in one beat of a resting 12-lead ECG.</p>
{activity("The ECG’s intervals", [
    task("hb-12", f'Open lead II of a resting 12-lead ECG, a second of it at a time {rec(TWELVE, "show me")}. You can see a whole beat: the P wave, the QRS complex and the T wave.', auto="rec:open id=ecg-12lead"),
    task("hb-pr", 'With the calipers, measure the <b>PR interval</b>. Drag from the start of the P wave to the start of the QRS. The menu beside the <b>Data pad</b> button shows what the Recorder thinks you’ve measured, and it should say PR.', auto="rec:measure id=ecg-12lead interval=PR || rec:datapad id=ecg-12lead n_pr>0"),
    task("hb-qt", 'Then measure the <b>QT interval</b>, from the start of the QRS to the end of the T wave.', auto="rec:measure id=ecg-12lead interval=QT || rec:datapad id=ecg-12lead n_qt>0"),
])}
{q("hb-q-pr", "The PR interval is mostly the delay at the atrioventricular node. How long was it, and what is the delay for?",
   "About 0.18 s (anything from 0.12 to 0.20 s is normal). The fibrous skeleton of the heart insulates the atria from the ventricles, so the only way for excitation to cross is through the AV node and the bundle of His. The AV node conducts slowly, which gives the atria time to contract and top up the ventricles before the ventricles are excited. Then the fast His–Purkinje system spreads the excitation through the ventricles in less than a tenth of a second (the width of the QRS). Its branches run down the septum to the apex before they turn up the walls, so the ventricles contract from the apex upwards and squeeze blood towards the outflow valves.")}
{q("hb-q-qt", "The QT interval is about as long as a ventricular action potential. How does that compare with an action potential in skeletal muscle, and what does a long action potential do for the heart?",
   "It was about 0.36 s here, roughly a hundred times as long as a skeletal muscle action potential, which lasts only a few milliseconds. During the plateau, Ca²⁺ coming in through L-type channels roughly balances K⁺ going out, which keeps the cell depolarised, and the Ca²⁺ that comes in triggers the release of much more from the sarcoplasmic reticulum (calcium-induced calcium release). While the cell stays depolarised its Na⁺ channels stay inactivated, so the refractory period lasts nearly as long as the contraction. Another action potential can’t start until the muscle has begun to relax, so the heart can’t be tetanised: it has to relax, and fill, between beats. Skeletal muscle, with its short action potentials and refractory periods, can add twitches together into a tetanus.")}
{block}
''')
    return chapter("s4-beat", num, "The heartbeat", "scope", "Optional: cardiac muscle and the heartbeat", 15,
                   "Look at cardiac muscle in the Microscope, then measure the parts of a heartbeat in the ECG and the "
                   "heart sounds, in the Recorder.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_endo(num):
    more = optional(f'''{activity("Acetylcholine on its own", [
    task("fu-high", f'Once the rubbed ring has settled after the wash {bathdo("plateau", "show me")}, add acetylcholine to it on its own, at a high concentration, 10<sup>−4</sup> M {bathdo("add acetylcholine 1e-4", "show me")}, and take it to its plateau. Watch the chart rather than the Results, which measure acetylcholine’s responses as relaxations.', auto="bath:add drug=acetylcholine conc>5e-5"),
])}
{q("fu-q-high", "Furchgott saw this too: at high concentrations, acetylcholine made the rubbed rings contract. What does that suggest about where its receptors are?",
   "That the smooth muscle has muscarinic receptors of its own, and that they make it contract, as muscarinic receptors on smooth muscle do elsewhere (in the ileum in Supervision 2, for example). Here the ring contracted by about half a gram. In a ring with its endothelium, the relaxation that the endothelium’s receptors cause, through NO, is far more powerful and hides this. So the same transmitter can relax a blood vessel or contract it, depending on which of its cells have the receptors.")}
{q("fu-q-r4", "Flow through a vessel goes with the fourth power of its radius (Poiseuille’s law). If an arteriole constricts so that its radius falls by 16%, what fraction of the flow is left? Work out 0.84⁴, on a calculator or in R.",
   "About half: 0.84⁴ = 0.50. The other way round, doubling the radius would increase the flow 16 times (2⁴), and the fourfold range of diameters that arterioles can span changes the flow about 250 times (4⁴ = 256). That’s why the arterioles control the flow through each tissue, and why the balance between dilators such as NO and constrictors such as noradrenaline matters so much.",
   accept="num:0.5±0.02", placeholder="fraction of the flow")}''')
    body = optional_chapter(f'''
{callout("info", "Optional, about 15 minutes", "<p>This exercise isn’t part of the work to hand in, and its steps don’t count towards finishing the page. It goes with Dr Fraser’s second lecture, on the arterioles, and with the third short-answer question in chapter 4.</p>")}

<p>In 1980 Robert Furchgott found that acetylcholine relaxed strips of rabbit aorta only if their <b>endothelium</b>, the single layer of cells lining the inside of the vessel, was intact. If the endothelium had been rubbed off, acetylcholine no longer relaxed them, though noradrenaline still made them contract. The endothelium was releasing a relaxing factor, later shown to be nitric oxide (NO), and the discovery won Furchgott, Ignarro and Murad the Nobel Prize in 1998. In the <b>Organ bath</b> you can repeat the experiment on rings of rat aorta. Phenylephrine, an α<sub>1</sub>-adrenoceptor agonist like noradrenaline, contracts them first, so that you can see whether anything relaxes them.</p>

<h2 id="fu-with">A ring with its endothelium</h2>
{activity("Acetylcholine, with the endothelium", [
    task("fu-ring", f'Set up a ring of rat aorta {bath(RING, "show me")}. Its clock already runs 20 times faster than real time, because the aorta responds slowly. This button gives everyone the same ring, so your numbers should be close to the ones in the model answers.', auto="bath:setup tissue=aorta endothelium=true"),
    task("fu-pe", f'Contract it with phenylephrine, to give 10<sup>−6</sup> M in the bath {bathdo("add phenylephrine 1e-6", "show me")}, and let the contraction reach its plateau {bathdo("plateau", "show me")}.', auto="bath:add drug=phenylephrine"),
    task("fu-ach", f'Now add acetylcholine to give 10<sup>−6</sup> M {bathdo("add acetylcholine 1e-6", "show me")} and take it to its plateau. Then wash the bath out {bathdo("wash", "show me")}. The Organ bath reads each response when you wash, or when you add the next drug, and puts it in the <b>Results</b> under the chart.', auto="bath:response drug=acetylcholine pct>50"),
])}

<h2 id="fu-without">A ring without it</h2>
{activity("Acetylcholine and nitroprusside, without the endothelium", [
    task("fu-rub", f'Set up a second ring from the same aorta, but with its endothelium rubbed off {bath(RUBBED, "show me")}.', auto="bath:setup tissue=aorta endothelium=false"),
    task("fu-snp", f'As before, contract it with phenylephrine {bathdo("add phenylephrine 1e-6", "show me")} and add acetylcholine {bathdo("add acetylcholine 1e-6", "show me")}, taking each to its plateau. Then, without washing, add sodium nitroprusside, which releases NO itself, to give 10<sup>−6</sup> M {bathdo("add nitroprusside 1e-6", "show me")}, and take that to its plateau too.', auto="bath:add drug=nitroprusside"),
    task("fu-wash", f'Wash the bath out {bathdo("wash", "show me")}, and compare the three relaxations in the <b>Results</b>.', auto="bath:response drug=nitroprusside pct>80"),
])}
{q("fu-q-endo", "What do the two rings tell you about how acetylcholine relaxes the aorta?",
   "With its endothelium, this ring relaxed by about 83% of the tone that phenylephrine gave it. Without its endothelium, it hardly relaxed at all (about 2%). So acetylcholine doesn’t relax the smooth muscle directly. It acts on muscarinic receptors on the endothelial cells, which then make nitric oxide from L-arginine, using nitric oxide synthase. NO is small and lipophilic, so it diffuses straight into the smooth muscle. There it stimulates a soluble guanylyl cyclase, and the cGMP that makes activates a protein kinase that relaxes the muscle, by lowering its [Ca²⁺]<sub>i</sub> and the sensitivity of its contractile machinery to Ca²⁺. Sodium nitroprusside relaxed the rubbed ring completely, because it releases NO itself. The muscle could still respond to NO, so what the ring had lost was the ability to make it.")}
{mcq("fu-q-sild", "Sildenafil (Viagra) makes the NO pathway more effective. How?", [
    ("It releases NO, as glyceryl trinitrate does", False, "No. Glyceryl trinitrate and nitroprusside release NO, but sildenafil doesn’t. It acts further along the pathway."),
    ("It activates nitric oxide synthase in the endothelium", False, "No. It doesn’t make more NO. It makes the NO that’s there more effective."),
    ("It inhibits the phosphodiesterase (PDE5) that breaks down cGMP", True, "Yes. With PDE5 blocked, the cGMP made in response to NO lasts longer, so the same amount of NO relaxes the smooth muscle more. Sildenafil was first developed as a possible treatment for angina."),
    ("It blocks α<sub>1</sub>-adrenoceptors on the smooth muscle", False, "No. That’s how prazosin relaxes blood vessels, by blocking the noradrenaline released by sympathetic nerves. Sildenafil acts on the NO pathway."),
])}
{more}
''')
    return chapter("s4-endo", num, "Furchgott’s experiment", "bath", "Optional: Furchgott’s experiment", 15,
                   "Repeat, in the Organ bath, the experiment that showed that acetylcholine relaxes arteries only if "
                   "their endothelium is there.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_write(num):
    hand_note = callout("info", "Handing in", "<p>Your essay goes straight from this page into my Google Drive, and you don’t need a Google account for that. The hand-in password I give you stops anyone else from handing work in, so please keep it to yourself. Once your essay has arrived, the page tells you so and gives you a receipt. If it can’t be handed in, the page will tell you why. If you try again and it still won’t go, download a copy and send it to me some other way.</p>")
    body = f'''
<p class="essay-title">“{ESSAY}”</p>

<h2 id="es4-title">Thinking about the title</h2>
<p>The title asks how the properties of cardiac muscle make three things possible. The pumping has to be <b>coordinated</b>, with every cell contracting together and in the right order. It has to be <b>rhythmic</b>, with a beat that starts itself, at a rate that can change. And the heart has to <b>relax between beats</b>, so that it can fill. A good essay is organised around those demands, and shows which structural and electrical properties meet each one, rather than describing the heart from top to bottom. These questions might help you plan.</p>
<ul>
<li><b>Coordinated.</b> How do the junctions between the cells, and the conduction system, make the atria and then the ventricles contract as units, and in the right order? Chapter 1 has some numbers for this.</li>
<li><b>Rhythmic.</b> Where does each beat start, what makes the pacemaker cells fire on their own, and how do the autonomic nerves change the rate?</li>
<li><b>Pumping.</b> How does an action potential become a contraction in a cardiac muscle cell, and how is the force of a beat graded, when every cell contracts every time?</li>
<li><b>Relaxation.</b> What stops the heart from being tetanised, and what has to happen for it to relax and fill? Why does relaxing need energy?</li>
<li><b>The whole cycle.</b> How do the valves, which open and close passively, turn these contractions into one-way flow?</li>
</ul>
<p>Comparing cardiac muscle with skeletal muscle, which you wrote about last week, can help, but only where the comparison explains something about the heart.</p>

<h2 id="es4-before">Before you start</h2>
<ul>
<li>Look back at the feedback on your earlier essays, and pick one thing to do better this time. If you’d like a reminder of the six criteria I mark against, they’re in <a href="supervision-1.html#s1-marking" target="_blank" rel="noopener">Supervision 1, chapter 4</a>.</li>
<li>Revise the lectures first if you like. Then put your notes away and find about 45 minutes when you won’t be interrupted.</li>
<li>Make sure you have the <b>hand-in password</b> I gave you, because you’ll need it at the end. You won’t find it anywhere on this site.</li>
<li>Give yourself about <b>40 minutes</b>, as you would in the exam, and spend the first five of them planning. The clock at the top of the paper tells you when you reach 40 minutes.</li>
<li>A diagram can save you a lot of words in this essay: the conduction system of the heart, say, or a ventricular action potential with its phases, or the events of the cardiac cycle. Draw it with <b>Insert drawing</b> (the pencil), or draw it on paper and add a photo of it with <b>Insert picture</b>. Type a caption under it, and refer to it in your text.</li>
</ul>
{activity("Write it, and hand it in", [
    task("es4-start", f'Open the essay {exam(PAPER, "show me")}, read its first page, and press <b>Start</b> when you’re ready to write.', auto=f"exam:start paper={PAPER}", check=f"paper:{PAPER}.started"),
    task("es4-write", 'Plan, then write. Aim for an introduction that says what your essay will argue, paragraphs that each make one point and show how it helps to answer the question, and a conclusion that draws them together.', auto=f"exam:words paper={PAPER} words>299"),
    task("es4-submit", 'When you’ve finished, go to the submission page (the ✓ tile at the bottom right), check your essay and submit it.', auto=f"exam:submit paper={PAPER}", check=f"paper:{PAPER}.submitted"),
    task("es4-send", 'Hand it in on the page that comes up next. Type in the hand-in password and press <b>Hand it in</b>. The page shows you a receipt once your essay has arrived.', auto=f"exam:handin paper={PAPER} step=confirmed", check=f"paper:{PAPER}.handedIn"),
    task("es4-word", 'To keep a copy, press <b>Download your copy</b> (before you hand in, it’s called <b>Download a copy for yourself</b>, under the password box). The copy is saved as a Word document in your Downloads folder.', auto=f"exam:download paper={PAPER} format=docx", check=f"paper:{PAPER}.downloaded"),
])}
{hand_note}
{callout("info", "After you’ve handed it in", "<p>Once you’ve submitted, <b>Review my answers</b> shows you the ground a good answer would cover. Read it after you’ve handed your essay in, and make a note of what you’d add or change. That’s what we’ll talk about in the supervision.</p><p>Your essay is kept in this browser, in Files → <code>essays</code>. It won’t be there on another computer, and some shared computers clear it when you log out, so download a copy before you finish.</p>")}
{q("es4-q-next", "Once you’ve read the guidance, which of the three demands, coordination, rhythm or relaxation, did your essay deal with least well, and what would you add?",
   "There’s no single right answer here, so bring yours to the supervision. Many essays on this title describe the action potential and excitation–contraction coupling in detail, but say little about relaxation, which the title asks for in so many words: the long refractory period that prevents tetanus, the removal of Ca²⁺ by SERCA and the Na⁺/Ca²⁺ exchanger, and why that needs energy. Others list the properties of cardiac muscle without saying what each one does for the heart as a pump, which is what the title asks.")}
'''
    return chapter("s4-write", num, "Write your essay", "exam", "Write your essay, and hand it in", 45,
                   "This is the work to hand in this week. As before, you write it in Supervision work, as you will in "
                   "the online exam, and then hand it in from the same page. It goes straight into my Google Drive.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_more(num):
    saqs = ''.join(f'<li>{s}</li>' for s in SAQS)
    rev = ''.join(f'<li>{s}</li>' for s in REVISION)
    body = f'''
<h2 id="m4-saq">Short-answer questions</h2>
<p>These three go with this week’s lectures, one with each. Each is marked out of five, so answer in bullet points and aim for at least five separate points.</p>
<ol class="titles">{saqs}</ol>
<p>They have a paper of their own in Supervision work {exam("s4-saqs", "open them")}. There’s no time limit, but about 10 minutes for each is a good aim. Sketch the loop for the first one with <b>Insert drawing</b> (the pencil), or draw it on paper and add a photo of it with <b>Insert picture</b>. After you submit, <b>Review my answers</b> shows you what a good answer covers.</p>

<h2 id="m4-rev">Essay titles for revision</h2>
<p>It’s worth noting these down. They go with Dr Fraser’s two lectures, and they’re the kind of title you could meet in the exam.</p>
<ol class="titles">{rev}</ol>
<p>Planning an answer to each one (your argument, your evidence, and the order you’d put them in) is good revision. You could also write one up in Supervision work {exam("s4-revision", "open them")} in 40 minutes, for practice. After you submit, the guidance shows you the ground each title should cover.</p>
{optional(activity("If you want the practice", [
    task("m4-saq", 'Answer one or more of the short-answer questions, and submit them.', auto="exam:submit paper=s4-saqs"),
    task("m4-plan", 'Plan an answer to one of the revision titles. Sum up your position in a sentence, then jot down the three or four points, with the evidence for each, that would support it.'),
]), title='Practice')}
'''
    return chapter("s4-more", num, "More practice", "exam", "More practice: short answers and revision", None,
                   "This chapter is optional. It has three short-answer questions on this week’s lectures, and two "
                   "more essay titles to note down for revision. Only the essay needs to be handed in.", body)


def ALL():
    order = [ch_week, ch_beat, ch_endo, ch_write, ch_more]
    return [f(str(i)) for i, f in enumerate(order)]
