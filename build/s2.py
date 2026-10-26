"""The chapters of Supervision 2 (supervision-2.html): nerves, synapses and the autonomic nervous system.

There's no essay this week. The work to hand in is one paper in Supervision work (exams/s2-work.json): a practical
question on the thyroid gland, which goes back to Supervision 1's hormones ((a) a labelled photograph of a follicle from
the Microscope, with the area of its lumen worked out in R; (b) how T3 and T4 are made, in no more than 200 words), and
two short-answer questions on this week's lectures. The essay titles for revision are in exams/s2-revision.json.

The chapters: what to do this week; two optional exercises, about half an hour in all (electrochemical gradients,
resting potentials and the action potential, in R, Circuits and PhET's Neuron; the autonomic nervous system on a
guinea-pig ileum in the Organ bath); the practical question, step by step in the Microscope and R; the short-answer
questions and handing in; and the revision titles. ALL() puts them in order.

The lecture notes are Prof. Matthew Mason's (Introduction to Neurobiology): nothing here is copied from them. The
concentrations of frog muscle and the 58 mV form of the Nernst equation at 20 °C are the standard ones that the notes
also use. The values in the model answers were read off the workbench itself (the circuit, the Neuron simulation, the
organ bath's tissues and the thyroid slide)."""
from lib import *

PAPER = 's2-work'
SAQ_EK = 'How can POSITIVELY charged potassium ions generate a NEGATIVE value of <i>E</i><sub>K</sub>?'
SAQ_NAV = ('Briefly describe (a) how a voltage-gated sodium channel is selective for Na<sup>+</sup> ions, and (b) how the '
           'voltage-gating works.')
REVISION = [
    'What is the evidence for the involvement of sodium ions in the nerve action potential?',
    'What is the evidence that transmission between nerve and muscle is chemical in nature?',
    'How can a knowledge of the autonomic nervous system be pharmacologically valuable?',
]

# the follicle that the buttons open (the centre of the view, in mm from the slide's top left, and the objective)
FOLLICLE = 'thyroid-gland@2.05,0.83,20x'

HANDIN_LINE = ('All of it goes in one paper in <b>Supervision work</b>. Once you’ve submitted it, <b>hand it in</b> from the '
               'same page before your supervision. You’ll need the <b>hand-in password</b> I give you, and your work then '
               'goes straight into my Google Drive.')


def handin_box(buttons=True):
    """the work to hand in, as the first thing the student sees"""
    b = (f'<p class="hb-acts">{goto("s2-thyroid", "start the practical question")} {exam(PAPER, "open the paper")}</p>'
         if buttons else '')
    return f'''<div class="handin-box">
  <div class="hb-k">To hand in this week</div>
  <p class="hb-title">A practical question on the thyroid gland, and two short-answer questions</p>
  <ul>
    <li>The <b>practical question</b> goes back to last week’s hormones. You photograph a thyroid follicle in the <b>Microscope</b>, label it, measure the area of its lumen and work it out in <b>R</b>. Then you describe how T3 and T4 are made, in no more than 200 words.</li>
    <li>The two <b>short-answer questions</b> are on this week’s lectures: how <i>E</i><sub>K</sub> can be negative, and how the voltage-gated sodium channel works. Each is marked out of five, so answer in bullet points and make at least five.</li>
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

<h2 id="w2-plan">The week, step by step</h2>
<ol class="plan">
<li>If you’d like to, start with <b>two short exercises</b>. They’re optional and take about half an hour altogether. In chapter 1 you work out equilibrium potentials and a resting potential in <b>R</b>, model the membrane as a circuit in <b>Circuits</b>, and set off an action potential in the <b>Neuron</b> simulation, which is good preparation for the short-answer questions. In chapter 2 you find out where nicotine acts on a piece of gut in the <b>Organ bath</b>. {goto("s2-ions", "start")}</li>
<li>Then do the <b>practical question</b> in chapter 3, which takes about 40 minutes. You look at the thyroid in the <b>Microscope</b> and <b>R</b>, and then answer the question’s two parts. {goto("s2-thyroid", "go there")}</li>
<li>Answer the <b>two short-answer questions</b>, then submit the paper and hand it in (chapter 4, about 20 minutes). {goto("s2-saq", "go there")}</li>
<li>If you’d like more practice, chapter 5 has three essay titles to note down for revision. These are optional too. {goto("s2-more", "go there")}</li>
</ol>
{activity("Before you start", [
    task("w2-name", 'Check that your name is at the top of the page. If it says <b>Your name</b>, click it and add yours. It goes at the top of the work you hand in, and every supervision’s page shares it.', check="named"),
])}

<h2 id="w2-how">How this page works</h2>
<ul>
<li>It works in the same way as last week’s. The steps tick themselves off as you do them, the buttons do things for you in the workbench on the right, and every question has a <b>model answer</b> you can look at once you’ve had a go.</li>
<li>Chapters 1, 2 and 5 are optional, so their steps don’t count towards finishing the page. Everything in chapters 3 and 4 does.</li>
<li>If you haven’t used one of the workbench’s tabs before, the <a href="workbench.html" target="_blank" rel="noopener">workbench guide</a> shows you how it works.</li>
</ul>
'''
    return chapter("s2-week", num, "This week", "exam", "Supervision 2: nerves, synapses and the autonomic nervous system", 5,
                   "This week’s lectures introduce neurobiology: electrochemical gradients, action potentials, synapses and "
                   "the autonomic nervous system. There’s no essay this week. Instead you hand in a practical question on "
                   "the thyroid gland, which goes back to last week’s hormones, and two short-answer questions on this "
                   "week’s lectures.", body)


# ---------------------------------------------------------------------------------------------------------------------
R_EK = '58 * log10(2.25 / 140)'
R_ENA = '58 * log10(120 / 10)'
R_GHK = 'ghk <- function(r) 58 * log10((2.25 + r * 120) / (140 + r * 10))'
R_TRY = 'ghk(c(0.001, 0.01, 0.05, 0.1))'


def ch_ions(num):
    body = optional_chapter(f'''
{callout("info", "Optional, about 15 minutes", "<p>This exercise isn’t part of the work to hand in, and its steps don’t count towards finishing the page. It’s good preparation for the short-answer questions, though, and you’ll need R for the practical question anyway.</p>")}

<h2 id="io-nernst">Equilibrium potentials, in R</h2>
<p>In a frog muscle fibre, the K<sup>+</sup> concentration is about 140 mM inside and 2.25 mM outside, and the Na<sup>+</sup> concentration about 10 mM inside and 120 mM outside. At 20 °C the Nernst equation becomes <i>E</i> = (58 / <i>z</i>) log<sub>10</sub>([ion]<sub>out</sub> / [ion]<sub>in</sub>), in mV, and for K<sup>+</sup> and Na<sup>+</sup> <i>z</i> is +1. Each <b>show me</b> button types a line into RStudio’s Console for you. Press <kbd>Enter</kbd> to run it.</p>
{activity("Work them out", [
    task("io-ek", f'Work out <i>E</i><sub>K</sub>: {rcode(R_EK)}', auto="r:input kind=rstudio line~log10(2.25"),
    task("io-ena", f'And <i>E</i><sub>Na</sub>: {rcode(R_ENA)}', auto="r:input kind=rstudio line~log10(120"),
    task("io-ghk", f'The resting membrane is permeable to both ions, though much more to K<sup>+</sup>. The Goldman–Hodgkin–Katz (GHK) equation weights each one by its permeability, so make it a function of the ratio <i>P</i><sub>Na</sub> / <i>P</i><sub>K</sub>: {rcode(R_GHK)}. Then try a few ratios: {rcode(R_TRY)}', auto="r:input kind=rstudio line~ghk(c("),
])}
{q("io-q-e", "What did you get for <i>E</i><sub>K</sub> and <i>E</i><sub>Na</sub>, and what happens to the resting potential as the ratio <i>P</i><sub>Na</sub> / <i>P</i><sub>K</sub> goes up?",
   "<i>E</i><sub>K</sub> is about −104 mV and <i>E</i><sub>Na</sub> about +63 mV. With a ratio of 0.001 the GHK equation gives −102.7 mV, close to <i>E</i><sub>K</sub>, and as the ratio goes up the potential moves towards <i>E</i><sub>Na</sub>: −93.3 mV at 0.01, −71.4 mV at 0.05 and −57.7 mV at 0.1. The resting potential lies between the two equilibrium potentials, and nearer the one for the ion the membrane is more permeable to.")}
{mcq("io-q-ratio", "A frog muscle fibre rests at about −90 mV. Roughly what is the ratio of <i>P</i><sub>K</sub> to <i>P</i><sub>Na</sub>?", [
    ("About 1 to 1", False, "No. With equal permeabilities the potential would sit about halfway between the equilibrium potentials, not near −90 mV."),
    ("About 10 to 1", False, "Not quite. A ratio <i>P</i><sub>Na</sub> / <i>P</i><sub>K</sub> of 0.1 gives about −58 mV, which is far too positive."),
    ("About 70 to 1", True, "Yes. A ratio <i>P</i><sub>Na</sub> / <i>P</i><sub>K</sub> of 0.014 gives −90 mV (0.01 gives −93 mV), so <i>P</i><sub>K</sub> is roughly 70 times <i>P</i><sub>Na</sub>. A mammalian neuron, resting at about −70 mV, has a much smaller ratio, nearer 25 to 1."),
    ("About 1000 to 1", False, "No. With a ratio <i>P</i><sub>Na</sub> / <i>P</i><sub>K</sub> of 0.001 the potential would be about −103 mV, almost at <i>E</i><sub>K</sub>."),
])}

<h2 id="io-circuit">The membrane as a circuit</h2>
<p>In the parallel-conductance model of a membrane, each kind of ion channel is a conductance (drawn as a resistor, since conductance is 1 / resistance) in series with a battery at that ion’s equilibrium potential. The membrane potential settles where the currents through them cancel out, at the average of the equilibrium potentials weighted by their conductances.</p>
{activity("Run the model", [
    task("io-open", f'Open the model {circuit("example:resting-potential", "show me")} and run it {circuitrun("show me")}. The voltmeter reads the membrane potential. It settles at about −70 mV, between E(K<sup>+</sup>) at −90 mV and E(Na<sup>+</sup>) at +60 mV, but much nearer E(K<sup>+</sup>), because the K<sup>+</sup> conductance is far larger.', auto="circuit:run name~resting"),
    task("io-switch", 'Click the switch labelled <b>Na<sup>+</sup> switch</b> to close it. Many more Na<sup>+</sup> channels open, and the membrane potential swings towards E(Na<sup>+</sup>). Read it off, then click the switch again to open it.', auto="circuit:switch id=S1 on=true"),
])}
{q("io-q-switch", "With the switch closed, the membrane potential rises to about +47 mV, but not all the way to E(Na<sup>+</sup>) at +60 mV. Why not?",
   "Because the K<sup>+</sup> channels are still open. The membrane potential is the average of the two equilibrium potentials weighted by their conductances, and with the switch closed that’s (10 × −90 + 101.5 × 60) / 111.5 ≈ +46.5 mV, with the conductances in nanosiemens. It would only reach E(Na<sup>+</sup>) if Na<sup>+</sup> were the only ion the membrane let through. The same is true at the peak of a real action potential.")}

<h2 id="io-ap">An action potential</h2>
{activity("Stimulate a neuron", [
    task("io-sim", f'Open the Neuron simulation {sim("neuron", "show me")} and press <b>Stimulate Neuron</b>. Watch the channels open and close, and the ions move through them, as the action potential passes.', auto="sim:action id=neuron action=stimulate"),
    task("io-chart", 'Tick <b>Potential Chart</b> under <b>Show</b>, and stimulate the neuron again to see the action potential on the chart. As soon as it has fired, try to stimulate it once more. For a while, the <b>Stimulate Neuron</b> button won’t work.', auto="sim:action id=neuron action=chart"),
])}
{q("io-q-peak", "In the simulation the neuron rests at about −65 mV, and it uses Hodgkin and Huxley’s values for the squid axon: E(Na<sup>+</sup>) about +50 mV and E(K<sup>+</sup>) about −77 mV. Does the membrane potential reach either of them during the action potential? Why not?",
   "No. It peaks at roughly +30 to +40 mV, below E(Na<sup>+</sup>), and after the spike it dips to about −73 mV, close to E(K<sup>+</sup>) but not quite there. By the peak, the Na<sup>+</sup> channels are already inactivating and the voltage-gated K<sup>+</sup> channels are opening, so the membrane is never permeable to Na<sup>+</sup> alone. During the after-hyperpolarization the K<sup>+</sup> permeability is higher than at rest, which pulls the potential towards E(K<sup>+</sup>), but some permeability to other ions remains, so it doesn’t quite get there. It’s the same reason the circuit didn’t reach E(Na<sup>+</sup>).")}
{mcq("io-q-lock", "Why won’t the simulation let you stimulate the neuron again straight away?", [
    ("The axon has run out of sodium ions", False, "No. An action potential moves only a tiny fraction of the ions across the membrane, far too few to change the concentrations on either side."),
    ("Its sodium channels are inactivated, and they can’t open again until the membrane has repolarized: the refractory period", True, "Yes. For the absolute refractory period no stimulus, however large, can fire another action potential, and in the relative refractory period that follows only a larger one can. This is what sets the upper limit on how often a neuron can fire."),
    ("The sodium pump has to restore the concentration gradients first", False, "No. The pump plays no direct part in the action potential, and one action potential changes the gradients far too little to matter."),
])}
''')
    return chapter("s2-ions", num, "Membrane potentials", "circuit", "Optional: gradients, resting potentials and the action potential", 15,
                   "An optional exercise. Work out equilibrium potentials and a resting potential in R, model the "
                   "membrane as a circuit, and set off an action potential in a simulated neuron.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_ans(num):
    atropine = optional(f'<p>Wash the hexamethonium out {bathdo("antagonist none", "show me")} and let the tissue recover for 10 minutes {bathdo("wait 600", "show me")}. Then put <b>atropine</b> (10<sup>−8</sup> M) in the washing solution {bathdo("antagonist atropine 1e-8", "show me")}, wait another 10 minutes, and try acetylcholine and nicotine again.</p>\n' +
                        q("an-q-atr", "Atropine blocks the responses to both acetylcholine and nicotine. Why both?", "Because both end in the same place. Acetylcholine acts on the muscle’s muscarinic receptors directly, and nicotine acts through the ganglia, whose neurons release acetylcholine onto those same muscarinic receptors. Atropine is a competitive antagonist at muscarinic receptors, so it blocks the last step of both. (In this tissue, atropine at 10<sup>−8</sup> M cut both responses to about 13% of the maximum.) Atropine comes from deadly nightshade, <i>Atropa belladonna</i>. It dilates the pupils, which is how belladonna got its name."))
    body = optional_chapter(f'''
{callout("info", "Optional, about 15 minutes", "<p>This exercise isn’t part of the work to hand in, and its steps don’t count towards finishing the page. It goes with the last two lectures, on synapses and the autonomic nervous system.</p>")}

<p>The guinea-pig ileum is a short length of small intestine. Its smooth muscle has plexuses of nerve cells in its wall, the <b>enteric ganglia</b>, and parasympathetic nerves act on it through them. Postganglionic neurons release acetylcholine onto <b>muscarinic</b> receptors on the muscle, which make it contract. The ganglia themselves are cholinergic too, but their receptors are <b>nicotinic</b>, and a different type from those at the neuromuscular junction. Drugs that act at different points along that path let you work out where something acts. In the <b>Organ bath</b>, a piece of ileum hangs in warm salt solution, and its contractions are drawn on a chart.</p>

<h2 id="an-two">Acetylcholine and nicotine</h2>
{activity("Two agonists", [
    task("an-setup", f'Set up a fresh piece of ileum {bath("ileum?seed=3", "show me")}, and make the clock run 20 times faster {bathdo("speed 20", "show me")}. This button gives everyone the same piece of ileum, so your numbers should be close to the ones in the model answers.', auto="bath:setup tissue=ileum"),
    task("an-ach", f'Add acetylcholine to give 10<sup>−7</sup> M in the bath {bathdo("add acetylcholine 1e-7", "show me")}. Once the contraction has reached its plateau {bathdo("plateau", "show me")}, wash it out {bathdo("wash", "show me")}. The response goes into the <b>Results</b> under the chart.', auto="bath:response drug=acetylcholine condition=control"),
    task("an-nic", f'Now add nicotine to give 10<sup>−5</sup> M {bathdo("add nicotine 1e-5", "show me")}. Again, take it to its plateau and wash it out.', auto="bath:response drug=nicotine condition=control"),
])}
{mcq("an-q-nic", "Nicotine makes the ileum contract too. Which receptors do you think it acts on?", [
    ("Muscarinic receptors on the smooth muscle, the same as acetylcholine", False, "Probably not. Nicotine is a very weak agonist at muscarinic receptors, and the next steps will show you where it really acts."),
    ("Nicotinic receptors on the neurons of the enteric ganglia, which then release acetylcholine onto the muscle", True, "Yes, and the next steps test it. If nicotine acts on the ganglia, a drug that blocks ganglionic nicotinic receptors should stop it working, while acetylcholine, which acts on the muscle directly, should still work."),
    ("Nicotinic receptors on the smooth muscle, like those at the neuromuscular junction", False, "No. The nicotinic receptors at the neuromuscular junction are on skeletal muscle. Smooth muscle doesn’t contract through nicotinic receptors."),
])}

<h2 id="an-hex">Blocking the ganglia</h2>
{activity("Add hexamethonium", [
    task("an-hexa", f'Put hexamethonium (10<sup>−4</sup> M) in the solution used for washing, and wash the bath with it {bathdo("antagonist hexamethonium 1e-4", "show me")}. Let it equilibrate for 10 minutes {bathdo("wait 600", "show me")}. That also gives the nicotinic receptors time to recover, as nicotine desensitizes them.', auto="bath:equilibrated drug=hexamethonium"),
    task("an-nic2", 'Add nicotine (10<sup>−5</sup> M) again, take it to its plateau, and wash it out.', auto="bath:response drug=nicotine condition~hexamethonium"),
    task("an-ach2", 'Then add acetylcholine (10<sup>−7</sup> M) again, take it to its plateau, and wash it out.', auto="bath:response drug=acetylcholine condition~hexamethonium"),
])}
{q("an-q-hex", "Compare the responses in hexamethonium with the ones before. (In the Results table, each response is also given as a percentage of the largest contraction so far.) What do they tell you?",
   "In this tissue, hexamethonium cut the response to nicotine from about 97% to about 11% of the largest contraction, but left the response to acetylcholine unchanged, at about 100%. So nicotine acts at the ganglia. It excites the enteric neurons through their nicotinic receptors, and they release acetylcholine onto the muscle. Acetylcholine added to the bath acts on the muscle’s muscarinic receptors directly, so blocking the ganglia doesn’t affect it. Hexamethonium blocks the nicotinic receptors of autonomic ganglia but hardly touches those of the neuromuscular junction, which is one sign that the two are different types.")}
{atropine}
''')
    return chapter("s2-ans", num, "The autonomic nervous system", "bath", "Optional: where does nicotine act?", 15,
                   "An optional exercise. Use acetylcholine, nicotine and a ganglion blocker on a piece of guinea-pig "
                   "ileum in the Organ bath to work out where nicotine acts.", body)


# ---------------------------------------------------------------------------------------------------------------------
R_READ = 'm <- read.csv("~/microscope/measurements.csv")'
R_SUB = 'lumen <- subset(m, slide == "thyroid-gland" & kind == "area")'
R_SHOW = 'lumen[, c("label", "value", "unit", "objective")]'
R_LAST = 'area <- tail(lumen$value, 1)'
R_MM = 'area / 1e6'
R_DIAM = '2 * sqrt(area / pi)'

PRACTICAL_A = ('Use the digital microscope to examine a histological section of the thyroid gland. Choose an appropriate '
               'magnification, and use the labelling tool to label a <b>thyroid follicle</b>, its <b>lumen</b> and a '
               '<b>thyroid follicular cell</b>, and take a photograph that shows your labels. Measure the area of the '
               'lumen of your follicle, and use R to report it.')
PRACTICAL_B = ('In your own words, and using your labelled photograph to support your narrative account, describe the steps '
               'involved in the synthesis of the T3 and T4 hormones. Write no more than 200 words.')


def ch_thyroid(num):
    body = f'''
<div class="handin-box">
  <div class="hb-k">The practical question</div>
  <p><b>(a)</b> {PRACTICAL_A}</p>
  <p><b>(b)</b> {PRACTICAL_B}</p>
</div>
<p>You’ll come back to T3 and T4 later in the course, in more detail, so this is good revision. You may need to look up the structure of the thyroid gland to answer (a), and you can, but write your answers in your own words.</p>

<h2 id="th-look">What you’re looking for</h2>
<p>The thyroid gland is made of <b>follicles</b>. Each is a hollow ball, lined by a single layer of <b>follicular cells</b>, and its <b>lumen</b> is filled with <b>colloid</b>, which is mostly stored thyroglobulin and stains pink. Between the follicles there are capillaries and thin strands of connective tissue. You’ll see follicles of many different sizes, cut at different levels, so choose one that has been cut through near its middle.</p>

<h2 id="th-photo">Photograph a follicle</h2>
{activity("In the Microscope", [
    task("th-open", f'Open the thyroid gland {scope("thyroid-gland@1.8,1.6,2x", "show me")} and look at it at low power first. Almost all of it is follicles, each a ring of cells around pink colloid.', auto="scope:open slide=thyroid-gland"),
    task("th-find", f'Find a follicle you can see the whole of, with an unbroken ring of cells round it. This one works well {scope(FOLLICLE, "show me one")}. At <b>20×</b> the whole follicle fits in the view, and you can still pick out the single follicular cells and their nuclei. For a bigger follicle, 10× may be better.', auto="scope:mag slide=thyroid-gland mag>9||scope:view slide=thyroid-gland mag>9"),
    task("th-lab-f", f'Choose the <b>Label</b> tool {scopetool("label", "show me")} and click on the edge of your follicle. Call the label <i>Thyroid follicle</i>.', auto="scope:label slide=thyroid-gland text~follicle"),
    task("th-lab-l", 'Add a second label in the middle of the colloid, and call it <i>Lumen</i>.', auto="scope:label slide=thyroid-gland text~lumen||scope:label slide=thyroid-gland text~colloid"),
    task("th-lab-c", 'Add a third on one of the cells in the wall of the follicle, on its nucleus, and call it <i>Follicular cell</i>.', auto="scope:label slide=thyroid-gland text~cell"),
    task("th-area", f'Now measure the lumen. Choose the <b>Area</b> tool {scopetool("area:lumen", "show me")}, click your way round the inner edge of the follicular cells, and click the first point again to finish. In many follicles the colloid has shrunk away from the cells and left a pale gap. That happened when the tissue was processed, so measure to the cells, not to the edge of the colloid.', auto="scope:measure slide=thyroid-gland kind=area"),
    task("th-photo", f'Take a photograph with the camera {scopetool("capture", "show me")}. Take it last, so that it shows your three labels, the outline you measured and the scale bar. It’s saved in your files, in <code>~/microscope/pictures</code>.', auto="scope:capture slide=thyroid-gland"),
])}
{callout("tip", "Putting things right", "<p>To move or rename a label, click on it again with the <b>Label</b> tool, where you can change its text or delete it. A measurement you don’t want can be deleted in the <b>Measurements</b> panel. If you take the photograph again, the new one is saved alongside the old one.</p>")}

<h2 id="th-r">The area of the lumen, in R</h2>
<p>Every measurement you make in the Microscope goes into the file <code>~/microscope/measurements.csv</code>, one row each, and R can read it. Use R to pick out your lumen and report its area.</p>
{activity("In R", [
    task("th-read", f'Read the file into a table called <code>m</code>: {rcode(R_READ)}', auto="r:input kind=rstudio line~measurements.csv"),
    task("th-sub", f'Pick out the areas you measured on the thyroid slide: {rcode(R_SUB)}. Then look at them: {rcode(R_SHOW)}', auto="r:input kind=rstudio line~subset(m"),
    task("th-last", f'Keep the last one, which is your lumen, in µm²: {rcode(R_LAST)}. Then work it out in mm², and as the diameter of a circle with the same area, in µm: {rcode(R_MM)} and {rcode(R_DIAM)}', auto="r:input kind=rstudio line~sqrt(area"),
])}
{q("th-q-area", "What is the area of your follicle’s lumen, in µm² and in mm²?",
   "It depends on the follicle you chose. The one that <b>show me one</b> opens has a lumen of about 13,000 µm² (0.013 mm²), the same area as a circle about 130 µm across. The follicles on this slide range from about 50 µm to over 300 µm across, so anything from a few thousand µm² to well over 50,000 µm² is reasonable, as long as it matches your photograph.")}

<h2 id="th-write">Answer the question</h2>
{activity("In Supervision work", [
    task("th-paper", f'Open the paper {exam(PAPER, "show me")}, read its first page, and press <b>Start</b>.', auto=f"exam:start paper={PAPER}", check=f"paper:{PAPER}.started"),
    task("th-pic", 'Part (a) is the first question. Press <b>Insert picture</b> in the toolbar and choose your photograph from your files (it’s the newest one). Under it, give the area of the lumen, and the magnification you chose, with a sentence on why you chose it.', auto=f"exam:picture paper={PAPER} q=thyroid-a"),
    task("th-b", 'Then write part (b), on how T3 and T4 are made, in no more than 200 words. Use your photograph as you go, to show where each step happens: in the follicular cells, or in the colloid of the lumen.', auto=f"exam:words paper={PAPER} q=thyroid-b words>99"),
])}
{callout("tip", "Writing part (b)", "<p>A narrative account tells the story in order, from start to finish, so make sure each step leads on to the next. The word count under the box turns red if you go over 200 words. Nothing stops you typing, so you can write a draft first and then cut it down.</p>")}
'''
    return chapter("s2-thyroid", num, "The practical question", "scope", "The practical question: the thyroid gland", 40,
                   "Back to last week’s hormones. You’ll photograph and label a thyroid follicle in the Microscope, measure "
                   "the area of its lumen and work it out in R, and then describe how T3 and T4 are made.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_saq(num):
    hand_note = callout("info", "Handing in", "<p>Your work goes straight from this page into my Google Drive, and you don’t need a Google account for that. The hand-in password I give you stops anyone else from handing work in, so please keep it to yourself. Once your work has arrived, the page tells you so and gives you a receipt. If it can’t be handed in, the page will tell you why. If you try again and it still won’t go, download a copy and send it to me some other way.</p>")
    body = f'''
<h2 id="sq-mark">How short answers are marked</h2>
<p>Each of these questions is marked out of five, with roughly a mark for each correct, relevant point. So answer in <b>bullet points</b>, and make <b>at least five</b>, each a separate point. You don’t need an introduction or a conclusion. A point earns its mark when it’s specific: it names the thing, says what it does, and gives a number or an example where one helps.</p>
{callout("concept", "A vague point, and a better one", "<p>Say the question were <i>What does the sodium pump do?</i></p><ul><li><b>Too vague:</b> “It keeps the gradients going.”</li><li><b>Worth a mark:</b> “It pumps three Na<sup>+</sup> ions out of the cell and two K<sup>+</sup> ions in for each ATP it uses, against their electrochemical gradients.”</li></ul>")}

<h2 id="sq-q">The two questions</h2>
<ol class="titles"><li>{SAQ_EK}</li><li>{SAQ_NAV}</li></ol>
<p>They’re the last two questions of the paper, after the practical question. Try them as you would in the exam, without your notes, and give each about 10 minutes. To start a bulleted list, press the bulleted list button in the toolbar, and then <kbd>Enter</kbd> for each new point.</p>
{activity("Answer them, and hand in", [
    task("sq-ek", f'Answer the first question, on <i>E</i><sub>K</sub>, in bullet points {exam(PAPER, "open the paper")}.', auto=f"exam:words paper={PAPER} q=saq-ek words>29"),
    task("sq-nav", 'Answer the second, on the voltage-gated sodium channel. Parts (a) and (b) can each have their own bullet points.', auto=f"exam:words paper={PAPER} q=saq-nav words>29"),
    task("sq-submit", 'When you’ve answered all four parts of the paper, go to the submission page (the ✓ tile at the bottom right), check your answers and submit them.', auto=f"exam:submit paper={PAPER}", check=f"paper:{PAPER}.submitted"),
    task("sq-send", 'Hand it in on the page that comes up next. Type in the hand-in password and press <b>Hand it in</b>. The page shows you a receipt once your work has arrived.', auto=f"exam:handin paper={PAPER} step=confirmed", check=f"paper:{PAPER}.handedIn"),
    task("sq-word", 'To keep a copy, press <b>Download a copy for yourself</b>, under the password box (once you’ve handed in, the button says <b>Download your copy</b>). The copy is saved as a Word document in your Downloads folder.', auto=f"exam:download paper={PAPER} format=docx", check=f"paper:{PAPER}.downloaded"),
])}
{hand_note}
{callout("info", "After you’ve handed it in", "<p>Once you’ve submitted, <b>Review my answers</b> shows you the points a good answer covers, for all four parts. Read it after you’ve handed your work in, and make a note of anything you’d add or change. That’s what we’ll talk about in the supervision.</p><p>Your answers are kept in this browser, in Files → <code>essays</code>. They won’t be there on another computer, so download a copy before you leave.</p>")}
'''
    return chapter("s2-saq", num, "Short answers", "exam", "Short-answer questions, and handing in", 20,
                   "Two short-answer questions on this week’s lectures, in the same paper as the practical question. Then "
                   "you submit the paper and hand it in.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_more(num):
    rev = ''.join(f'<li>{s}</li>' for s in REVISION)
    body = f'''
<h2 id="m2-rev">Essay titles for revision</h2>
<p>It’s worth noting these down. They go with this week’s lectures, and they’re the kind of title you could meet in the exam.</p>
<ol class="titles">{rev}</ol>
<p>Planning an answer to each one (your argument, your evidence, and the order you’d put them in) is good revision. You could also write one up in Supervision work {exam("s2-revision", "open them")} in 40 minutes, for practice. After you submit, the guidance shows you the ground each title should cover.</p>
{optional(activity("If you want the practice", [
    task("m2-plan", 'Plan an answer to one of the titles. Sum up your position in a sentence, then jot down the three or four points, with the evidence for each, that would support it.'),
    task("m2-write", 'Or write one of them up in Supervision work, and submit it.', auto="exam:submit paper=s2-revision"),
]), title='Practice')}
'''
    return chapter("s2-more", num, "More practice", "exam", "More practice: essay titles for revision", None,
                   "This chapter is optional. It has three essay titles from this week’s lectures to note down for "
                   "revision. Only the practical question and the two short-answer questions need to be handed in.", body)


def ALL():
    order = [ch_week, ch_ions, ch_ans, ch_thyroid, ch_saq, ch_more]
    return [f(str(i)) for i, f in enumerate(order)]
