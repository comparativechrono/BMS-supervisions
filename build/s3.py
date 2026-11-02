"""The chapters of Supervision 3 (supervision-3.html): muscle and movement.

The work to hand in is an essay in Supervision work (exams/s3-essay.json). The short-answer questions (s3-saqs.json)
and the essay titles for revision (s3-revision.json) are optional.

The chapters: what to do this week; two optional exercises, about half an hour in all (skeletal muscle in the
Microscope, the width of its fibres, and why fibres that wide need T-tubules, worked out in R; a muscle's
force–velocity curve and its power in R, and the arm as a lever in Anatomy); writing the essay and handing it in; and
more practice. ALL() puts them in order.

The lecture handouts are Prof. Ewa Paluch's (Muscle and Movement): nothing here is copied from them. Hill's equation
is used in its normalised form, with a/F0 = 0.25, a typical value. The diffusion coefficient of Ca2+ is its value in
water (about 800 µm²/s), and the lengths of the forearm are round, typical values. The widths of the fibres in the
model answers were measured on the slide itself, at the place the button opens."""
from lib import *

PAPER = 's3-essay'
ESSAY = 'How are movements on the cellular and molecular scale used to produce movement of whole animals?'
SAQS = [
    'If you attach a 50 g mass to a muscle it takes longer to lift a given distance than a 5 g mass. Why does velocity '
    'decrease as force increases? Draw a graph to demonstrate the relationship. How does muscle power vary as a function '
    'of load?',
    'Relate the clinical signs with the physiology of: (a) malignant hyperthermia, (b) Duchenne’s muscular dystrophy, '
    '(c) myasthenia gravis.',
    'Outline similarities and differences between the skeletal and smooth muscle contractile apparatus.',
]
REVISION = [
    'What factors affect the contractile force developed by a skeletal muscle?',
    'Explain how the molecular organisation of the sarcomere enables skeletal muscle contraction and discuss '
    'consequences of defects in structural muscle proteins.',
    'Compare and contrast mechanisms of excitation-contraction coupling in skeletal and smooth muscle.',
]

# where the buttons open the skeletal muscle (the centre of the view, in mm from the slide's top left, and the objective)
LOW = 'skeletal-muscle@1.6,1.6,2x'
ACROSS = 'skeletal-muscle@0.642,3.113,10x'
ALONG = 'skeletal-muscle@1.137,0.494,40x'
SMOOTH = 'smooth-muscle@2.471,2.273,10x'
HEART = 'heart@2.2,1.46,40x'

HANDIN_LINE = ('Once you’ve submitted it, <b>hand it in</b> from the same page before your supervision. You’ll need the '
               '<b>hand-in password</b> I give you, and your essay then goes straight into my Google Drive.')


def handin_box(buttons=True):
    """the essay to hand in, as the first thing the student sees"""
    b = (f'<p class="hb-acts">{goto("s3-write", "how to write it and hand it in")} {exam(PAPER, "open the essay")}</p>'
         if buttons else '')
    return f'''<div class="handin-box">
  <div class="hb-k">To hand in this week</div>
  <p class="hb-title">“{ESSAY}”</p>
  <ul>
    <li>You write the essay in <b>Supervision work</b>, as you did in Supervision 1 and as you will in the online exam: in one sitting, without your notes, and without pasting anything in.</li>
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

<h2 id="w3-plan">The week, step by step</h2>
<ol class="plan">
<li>If you’d like to, start with <b>two short exercises</b>. They’re optional and take about half an hour altogether, and they’ll give you numbers and examples to use in your essay. In chapter 1 you look at skeletal muscle in the <b>Microscope</b>, measure its fibres, and use <b>R</b> to work out why they need T-tubules. In chapter 2 you plot a muscle’s force–velocity curve and its power in <b>R</b>, and see how your arm works as a lever in <b>Anatomy</b>. {goto("s3-fibres", "start")}</li>
<li>Then <b>write your essay</b> and hand it in (chapter 3, about 45 minutes). {goto("s3-write", "go there")}</li>
<li>If you’d like more practice, chapter 4 has three short-answer questions, and three more essay titles to note down for revision. These are optional too. {goto("s3-more", "go there")}</li>
</ol>
<p>This week’s lecture on the autonomic nervous system goes with last week’s optional exercise in the <b>Organ bath</b>, so if you didn’t do it then, it’s still there in <a href="supervision-2.html#s2-ans" target="_blank" rel="noopener">Supervision 2, chapter 2</a>.</p>
{activity("Before you start", [
    task("w3-name", 'Check that your name is at the top of the page. If it says <b>Your name</b>, click it and add yours. It goes at the top of the essay you hand in, and every supervision’s page shares it.', check="named"),
])}

<h2 id="w3-how">How this page works</h2>
<ul>
<li>It works in the same way as the last two. The steps tick themselves off as you do them, the buttons do things for you in the workbench on the right, and every question has a <b>model answer</b> you can look at once you’ve had a go.</li>
<li>Chapters 1, 2 and 4 are optional, so their steps don’t count towards finishing the page. The rest do.</li>
<li>If you haven’t used one of the workbench’s tabs before, the <a href="workbench.html" target="_blank" rel="noopener">workbench guide</a> shows you how it works.</li>
</ul>
'''
    return chapter("s3-week", num, "This week", "exam", "Supervision 3: muscle and movement", 5,
                   "This week’s lectures are on muscle: how the proteins of the sarcomere make force, how an action "
                   "potential switches contraction on, and how muscles and the skeleton turn that force into movement. "
                   "The essay you hand in asks you to put all of it together, from molecules to whole animals.", body)


# ---------------------------------------------------------------------------------------------------------------------
R_READ = 'm <- read.csv("~/microscope/measurements.csv")'
R_W = 'w <- subset(m, slide == "skeletal-muscle" & kind == "length")$value'
R_MEAN = 'mean(w)'
R_X = 'x <- mean(w) / 2'
R_T = 'x^2 / (2 * 800)'
R_T1 = '1^2 / (2 * 800)'
R_TS = '2.5^2 / (2 * 800)'


def ch_fibres(num):
    smooth = optional(f'''{activity("Smooth and cardiac muscle", [
    task("fb-smooth", f'Open the smooth muscle of the oesophagus at 10× {scope(SMOOTH, "show me")}, the same magnification as the skeletal muscle. Its cells are long, thin spindles, each with one nucleus in the middle, packed together in bundles. There are no striations, even at higher power.', auto="scope:open slide=smooth-muscle"),
    task("fb-smooth-t", f'A smooth muscle cell is only about 5 µm across at its widest. How long would Ca²⁺ take to reach its middle from the membrane? {rcode(R_TS)}', auto="r:input kind=rstudio line~2.5^2"),
    task("fb-heart", f'Now open the heart, at 40× {scope(HEART, "show me")}. Cardiac muscle is striated, like skeletal muscle, but its cells are much smaller, with one or two nuclei in the middle. They branch, and they’re joined end to end by intercalated discs, the dark lines across the fibres.', auto="scope:open slide=heart"),
])}
{q("fb-q-smooth", "Smooth muscle has actin and myosin too. Why does it have no striations, and why doesn’t it need T-tubules?",
   "Its actin and myosin aren’t lined up in sarcomeres. Bundles of filaments run at an angle across the cell, anchored to dense bodies in the cytoplasm, which do the job of Z discs and are linked to each other by intermediate filaments, and to adhesion plaques on the membrane. With nothing in register, there’s nothing to make stripes, and when the cell contracts it gets shorter and fatter rather than pulling along a single line. It’s so thin that Ca²⁺ coming in through its membrane has at most 2.5 µm to go, which takes about 4 ms (2.5² / 1600 = 0.0039 s), so it doesn’t need T-tubules. It has small pits in its membrane, caveolae, instead, and it contracts far more slowly than skeletal muscle anyway.")}''')
    body = optional_chapter(f'''
{callout("info", "Optional, about 15 minutes", "<p>This exercise isn’t part of the work to hand in, and its steps don’t count towards finishing the page. It goes with the first two lectures, and it gives you some numbers you could use in your essay.</p>")}

<h2 id="fb-levels">A muscle, level by level</h2>
<p>A skeletal muscle is built in levels. The whole muscle is made of bundles of fibres, the <b>fascicles</b>. Each <b>fibre</b> is a single cell, very long and with many nuclei, packed with <b>myofibrils</b>. Each myofibril is a chain of <b>sarcomeres</b>, and each sarcomere is an array of actin and myosin filaments. The Microscope shows you the first few levels.</p>
{activity("Skeletal muscle", [
    task("fb-open", f'Open a section of human skeletal muscle at low power {scope(LOW, "show me")}. Some of its fibres were cut lengthways and some across. You can see how they’re grouped into fascicles, with pale connective tissue between them.', auto="scope:open slide=skeletal-muscle"),
    task("fb-peri", f'Choose the <b>Label</b> tool {scopetool("label", "show me")} and click on the connective tissue between two fascicles. Call the label <i>Perimysium</i>. It carries blood vessels and nerves into the muscle. Like the endomysium round each fibre and the epimysium round the whole muscle, it runs into the tendon, so it helps to pass the pull of the fibres on to the bone.', auto="scope:label slide=skeletal-muscle text~perimys"),
    task("fb-across", f'Now go to some fibres cut across, at 10× {scope(ACROSS, "show me")}. Each of these shapes is one fibre, and so one cell.', auto="scope:mag slide=skeletal-muscle mag>9||scope:view slide=skeletal-muscle mag>9"),
    task("fb-nuc", 'With the <b>Label</b> tool, label one of the nuclei at the edge of a fibre, and call it <i>Nucleus</i>. Look at how many nuclei each fibre has, and where they are.', auto="scope:label slide=skeletal-muscle text~nucle"),
    task("fb-width", f'Measure three fibres. Choose the <b>Measure</b> tool {scopetool("measure:fibre width", "show me")} and drag across a fibre at its narrowest, from one edge to the other. Then do the same for two more fibres.', auto="scope:measure slide=skeletal-muscle kind=length n>2"),
])}
{callout("tip", "Why the narrowest width?", "<p>A fibre that was cut at a slant looks longer than it should in one direction, but its narrowest width hardly changes. That’s why pathologists who measure the fibres in a muscle biopsy use the narrowest width too. They call it the lesser diameter.</p>")}
{q("fb-q-nuclei", "Why does a skeletal muscle fibre need so many nuclei? And why might they sit at its edge?",
   "A fibre is a huge cell. These are 60 to 80 µm across, and a fibre can be many centimetres long, sometimes running the whole length of its muscle. One nucleus couldn’t make enough mRNA for the proteins of so much cytoplasm, so each nucleus looks after the stretch of fibre around it. The nuclei come from the many myoblasts that fused to make the fibre as it developed. Satellite cells, which lie just outside the fibre under its basement membrane, can fuse with it to add more nuclei when it grows or is repaired. Keeping the nuclei at the edge leaves the middle of the fibre to the myofibrils. A row of nuclei down the middle of a fibre is a sign that it has regenerated after damage, as happens again and again in Duchenne muscular dystrophy.")}

<h2 id="fb-sarc">Smaller than the scan can show</h2>
<p>A sarcomere is only about 2.5 µm long, and each pixel of this scan is half a micrometre across, so the cross-striations that the sarcomeres make are too fine for it. Look at some fibres cut lengthways at 40× {scope(ALONG, "show me")}, though, and you may just make out fine lines running along them. Those are the myofibrils, each about a micrometre across.</p>
{mcq("fb-q-band", "As a sarcomere shortens, which of these stays the same length?", [
    ("The I band", False, "No. The I band is the part of each thin filament that the thick filaments don’t overlap, so it gets narrower as the filaments slide past each other."),
    ("The A band", True, "Yes. The A band is the length of the thick filaments, so it stays the same however much the sarcomere shortens, while the I band and the H zone get narrower. That was the key observation of the two papers of 1954 that proposed the sliding filament theory: the filaments slide past each other, and neither kind changes its length."),
    ("The H zone", False, "No. The H zone is the middle of the A band, where the thin filaments don’t reach. It narrows as they slide in, and it can disappear."),
    ("The distance from one Z disc to the next", False, "No. That’s the length of the sarcomere itself, which is what shortens."),
])}

<h2 id="fb-tt">Why T-tubules?</h2>
<p>In the second lecture you saw that the action potential spreads from the surface of a fibre into its middle along the <b>T-tubules</b>, so that the sarcoplasmic reticulum releases its Ca²⁺ right next to every myofibril. Why not just let Ca²⁺ in through the surface membrane? Your measurements can tell you. The time a molecule takes to diffuse a distance <i>x</i> is roughly <i>t</i> = <i>x</i>² / 2<i>D</i>, where <i>D</i> is its diffusion coefficient. For Ca²⁺ in water, <i>D</i> is about 800 µm² per second. Each <b>show me</b> button types a line into RStudio’s Console for you. Press <kbd>Enter</kbd> to run it.</p>
{activity("In R", [
    task("fb-read", f'Read your measurements into R: {rcode(R_READ)}', auto="r:input kind=rstudio line~measurements.csv"),
    task("fb-w", f'Pick out the widths of your fibres, in µm: {rcode(R_W)}. Then work out their mean: {rcode(R_MEAN)}', auto="r:input kind=rstudio line~mean(w)"),
    task("fb-t", f'Halve it, to get the distance from the edge of a fibre to its middle: {rcode(R_X)}. Then work out how long Ca²⁺ would take to diffuse that far, in seconds: {rcode(R_T)}', auto="r:input kind=rstudio line~x^2 / (2 * 800)"),
    task("fb-t1", f'Inside the fibre, Ca²⁺ released from the sarcoplasmic reticulum has only about 1 µm to go to reach the filaments. Work that out too: {rcode(R_T1)}', auto="r:input kind=rstudio line~1^2 / (2 * 800)"),
])}
{q("fb-q-tt", "How long would Ca²⁺ take to diffuse from the surface of one of your fibres to its middle, and how long from the sarcoplasmic reticulum to the filaments? What does that tell you?",
   "For these fibres, 60 to 80 µm across, the distance from the surface to the middle is about 33 µm, and 33² / 1600 gives about 0.7 s. From the sarcoplasmic reticulum to the filaments, 1 µm, it’s about 0.6 ms. That’s a thousand times quicker for a distance only 33 times shorter, because the time goes with the square of the distance. A twitch develops its force within a few tens of milliseconds of the action potential, so Ca²⁺ coming in through the surface would be far too slow. The edge of the fibre would contract long before the middle, and much of the Ca²⁺ would be pumped away before it got there. In real cytoplasm it would be slower still, because proteins bind Ca²⁺ as it goes. The T-tubules solve the problem by carrying the action potential into the middle of the fibre within about a millisecond, so that the sarcoplasmic reticulum releases its Ca²⁺ right next to every myofibril, and the whole width of the fibre contracts at once.")}
{smooth}
''')
    return chapter("s3-fibres", num, "Muscle fibres", "scope", "Optional: from the whole muscle to the fibre", 15,
                   "An optional exercise. Look at skeletal muscle in the Microscope, measure the width of its fibres, and "
                   "use R to work out why fibres that wide need T-tubules.", body)


# ---------------------------------------------------------------------------------------------------------------------
R_HILL = 'hill <- function(f) 0.25 * (1 - f) / (f + 0.25)'
R_F = 'f <- seq(0, 1, by = 0.01)'
R_V = 'v <- hill(f)'
R_PLOTV = 'plot(f, v, type = "l", xlab = "Force (fraction of the isometric force)", ylab = "Velocity (fraction of the maximum)")'
R_P = 'p <- f * v'
R_PLOTP = 'plot(f, p, type = "l", xlab = "Force (fraction of the isometric force)", ylab = "Power")'
R_MAX = 'f[which.max(p)]'
R_RATIO = 'hill(0.05) / hill(0.5)'
R_GAIN = '35 / 4'
R_FORCE = '5 * 9.81 * 35 / 4'


def ch_move(num):
    types = optional(f'''{activity("Fast and slow muscles", [
    task("mo-soleus", f'Two muscles of the calf share the calcaneal (Achilles) tendon, which pulls up the heel. {anatfind("soleus-muscle", "Find the soleus")}, the deeper of the two.', auto="anat:find ok=true target~soleus"),
    task("mo-gastro", f'{anatfind("medial-head-of-gastrocnemius|lateral-head-of-gastrocnemius", "Find the gastrocnemius")}, which lies over it and crosses the knee as well as the ankle.', auto="anat:find ok=true target~gastrocnemius"),
    task("mo-mb", f'Slow, oxidative fibres are red because they’re full of myoglobin, which stores O<sub>2</sub> for them. Open it {pdb("1MBN", "show me")}. This myoglobin is the sperm whale’s, whose muscles hold so much of it that they’re almost black.', auto="viewer:loaded id~1mbn"),
])}
{q("mo-q-types", "In most people the soleus has more type I fibres than the gastrocnemius. How does that fit what each muscle does?",
   "The soleus is a postural muscle. It works almost all the time you’re standing, to stop you falling forwards over your ankles, so it needs fibres that hold a force economically and don’t tire. Those are type I fibres: slow and oxidative, with plenty of mitochondria, capillaries and myoglobin. Most of the soleus’s fibres are type I, often 70 to 90 per cent. The gastrocnemius is used for quick, powerful movements, such as jumping, sprinting and pushing off, and about half its fibres are fast, type II fibres, which contract quickly but tire sooner, especially the glycolytic type IIb (called IIx in people). The nervous system recruits the small, slow motor units first, for standing and walking, and adds the large, fast ones only when more force is needed. That’s the size principle.")}''')
    body = optional_chapter(f'''
{callout("info", "Optional, about 15 minutes", "<p>This exercise isn’t part of the work to hand in, and its steps don’t count towards finishing the page. It goes with the third lecture, and with the first short-answer question in chapter 4.</p>")}

<h2 id="mo-fv">Force, velocity and power</h2>
<p>The heavier the load, the more slowly a muscle can lift it. A. V. Hill described the relationship in 1938 with the equation (<i>F</i> + <i>a</i>)(<i>v</i> + <i>b</i>) = (<i>F</i><sub>0</sub> + <i>a</i>)<i>b</i>, where <i>F</i><sub>0</sub> is the isometric force, the largest force the muscle can exert, and <i>a</i> and <i>b</i> are constants. If you measure the force as a fraction of <i>F</i><sub>0</sub> and the velocity as a fraction of the maximum, <i>v</i><sub>max</sub>, and take <i>a</i> to be a quarter of <i>F</i><sub>0</sub>, which is typical, it becomes <i>v</i> = 0.25(1 − <i>F</i>) / (<i>F</i> + 0.25). Each <b>show me</b> button types a line into RStudio’s Console for you. Press <kbd>Enter</kbd> to run it.</p>
{activity("In R", [
    task("mo-hill", f'Make Hill’s equation into a function: {rcode(R_HILL)}. Then make a series of forces from 0 to 1, and work out the velocity at each: {rcode(R_F)} and {rcode(R_V)}', auto="r:input kind=rstudio line~hill(f)"),
    task("mo-plotv", f'Plot the force–velocity curve: {rcode(R_PLOTV)}', auto="r:input kind=rstudio line~plot(f, v"),
    task("mo-plotp", f'Power is force × velocity. Work it out, and plot it: {rcode(R_P)} and {rcode(R_PLOTP)}', auto="r:input kind=rstudio line~plot(f, p"),
    task("mo-max", f'Find the force at which the power is greatest: {rcode(R_MAX)}', auto="r:input kind=rstudio line~which.max(p"),
    task("mo-ratio", f'Compare a light load with a heavy one, 0.05 of <i>F</i><sub>0</sub> and 0.5 of it: {rcode(R_RATIO)}', auto="r:input kind=rstudio line~hill(0.05)"),
])}
{q("mo-q-why", "Why does a muscle shorten more slowly as the load gets heavier?",
   "Because the load is carried by the cross-bridges that are attached at that moment. With no load, the filaments slide as fast as the cross-bridges can cycle, which sets <i>v</i><sub>max</sub>. That depends on how fast the muscle’s myosin uses ATP, and it’s higher in fast fibres. The heavier the load, the more cross-bridges have to be attached at any one time to bear it, so each spends more of its time attached and pulling, and less of it detaching and moving on, and the filaments slide more slowly. At the isometric force, <i>F</i><sub>0</sub>, all the attached cross-bridges are needed just to hold the load, and the muscle doesn’t shorten at all.")}
{q("mo-q-max", "At what force is the power greatest, as a fraction of the isometric force?",
   "At 0.31 of <i>F</i><sub>0</sub>, where the velocity is also 0.31 of <i>v</i><sub>max</sub>, so the power there is only about a tenth of <i>F</i><sub>0</sub> × <i>v</i><sub>max</sub>. Power is zero at both ends of the curve. With no load the muscle shortens fastest but exerts no force, and at <i>F</i><sub>0</sub> it exerts its greatest force but doesn’t move. A muscle gives its most power at intermediate loads and speeds, about a third of its maximum force and velocity.",
   accept="num:0.31±0.02", placeholder="fraction of F0")}
{q("mo-q-50g", "Say a muscle can just hold 100 g, so that 5 g is 0.05 of its isometric force and 50 g is 0.5 of it. How many times longer does it take to lift the 50 g mass the same distance?",
   "About 4.75 times: <code>hill(0.05) / hill(0.5)</code> is 0.792 / 0.167. The time it takes to lift a mass through a given distance is the distance divided by the velocity (leaving out the moment it takes to get going), so ten times the load takes almost five times as long. That’s the first part of the first short-answer question in chapter 4.",
   accept="num:4.75±0.05", placeholder="times longer")}

<h2 id="mo-lever">Your arm is a lever</h2>
<p>A muscle can only pull, and it can only shorten by a fraction of its length. The skeleton turns that pull into movement. Bones act as levers, the joints are their pivots, and where a muscle’s tendon is attached decides what it trades for what.</p>
{activity("The biceps, in Anatomy and R", [
    task("mo-bic", f'{anatfind("long-head-of-biceps-brachii", "Find the long head of the biceps")} (biceps brachii, in the front of the upper arm).', auto="anat:find ok=true target~biceps-brachii"),
    task("mo-fade", 'Once you’ve found it, the panel on the right tells you about it. Press <b>Fade the others</b> there, then <b>Frame it</b>, and follow the biceps down past the elbow. Its tendon attaches to the radius, just below the elbow.', auto="anat:fade on=true base~biceps"),
    task("mo-arm", f'The tendon pulls on the radius about 4 cm from the elbow, and your hand is about 35 cm from it. Work out how many times as far, and as fast, the hand moves as the biceps shortens: {rcode(R_GAIN)}. Then work out the force, in newtons, that the biceps needs to hold 5 kg in your hand with your forearm horizontal: {rcode(R_FORCE)}', auto="r:input kind=rstudio line~9.81 * 35"),
])}
{q("mo-q-lever", "What does your arm gain from having the biceps attached so close to the elbow, and what does it lose?",
   "It gains speed and range. Every centimetre the biceps shortens moves the hand 8.75 cm in the same time, so the hand moves 8.75 times as far and as fast as the muscle shortens. It loses force. To hold 5 kg (49 N) in the hand with the forearm horizontal, the biceps has to pull with 8.75 times as much, about 430 N, and more once you add the weight of the forearm itself. Most of the levers of the limbs work like this, trading force for the speed and range of movement that limbs need. Different jobs are geared differently, though. Digging animals such as armadillos have a long olecranon, the lever the triceps pulls on, which gives their forelimbs force, while running animals such as horses have muscles that pull close to the joints, at the top of long, light legs, which gives them speed.")}
{q("mo-q-gears", "How do a bicycle’s gears let you cycle at close to your maximum power, whatever the slope of the road?",
   "Your leg muscles give their most power at one particular combination of force and speed, about a third of their maximum of each, which for cycling means a particular rate of pedalling. The gears change how fast your legs have to turn for a given speed of the bicycle, and so how much force they have to exert. Uphill, a low gear lets your legs keep turning quickly against a force they can manage, though the bicycle moves slowly. On the flat, or downhill, a high gear stops your legs having to spin faster than they can usefully go. Either way the muscles stay near the load and speed at which they give their most power. The levers of the skeleton are gears too, but fixed ones, which is one reason why muscles that do different jobs have different fibre types and shapes.")}
{types}
''')
    return chapter("s3-move", num, "From muscle to movement", "rstudio", "Optional: from muscle to movement", 15,
                   "An optional exercise. Plot a muscle’s force–velocity curve and its power in R, and see how your arm "
                   "works as a lever, in Anatomy.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_write(num):
    hand_note = callout("info", "Handing in", "<p>Your essay goes straight from this page into my Google Drive, and you don’t need a Google account for that. The hand-in password I give you stops anyone else from handing work in, so please keep it to yourself. Once your essay has arrived, the page tells you so and gives you a receipt. If it can’t be handed in, the page will tell you why. If you try again and it still won’t go, download a copy and send it to me some other way.</p>")
    body = f'''
<p class="essay-title">“{ESSAY}”</p>

<h2 id="es3-title">Thinking about the title</h2>
<p>The title covers an enormous range of scales. In one cross-bridge cycle a myosin head moves an actin filament about 10 nm, and a running animal covers metres in a second. The question is how you get from one to the other, so a good essay is about the steps in between: how the tiny movements of molecules are added up, switched on together, controlled, and passed on to the skeleton. These questions might help you plan.</p>
<ul>
<li><b>The motor.</b> What does one myosin head do in one cross-bridge cycle, and where does the energy come from?</li>
<li><b>Adding up.</b> What happens to the shortening when thousands of sarcomeres are joined end to end, and to the force when myofibrils and fibres lie side by side?</li>
<li><b>Switching on.</b> How does an action potential at the surface of a fibre make every sarcomere in it contract at once? Chapter 1 has some numbers for this.</li>
<li><b>Control.</b> How does the nervous system grade the force of a whole muscle?</li>
<li><b>From muscle to limb.</b> How do tendons and the levers of the skeleton turn the shortening of a muscle into the movement of a limb, and what do they trade? Chapter 2 has some numbers for this too.</li>
<li><b>Whole animals.</b> Which examples will you use? And do all animals move in the same way?</li>
</ul>
<p>Don’t try to write down everything you know about each step. Choose the points that show how one scale produces the next, and say how as you go.</p>

<h2 id="es3-before">Before you start</h2>
<ul>
<li>Look back at the feedback on your first essay, and pick one thing to do better this time. If you’d like a reminder of the six criteria I mark against, they’re in <a href="supervision-1.html#s1-marking" target="_blank" rel="noopener">Supervision 1, chapter 4</a>.</li>
<li>Revise the lectures first if you like. Then put your notes away and find about 45 minutes when you won’t be interrupted.</li>
<li>Make sure you have the <b>hand-in password</b> I gave you, because you’ll need it at the end. You won’t find it anywhere on this site.</li>
<li>Give yourself about <b>40 minutes</b>, as you would in the exam, and spend the first five of them planning. The clock at the top of the paper tells you when you reach 40 minutes.</li>
<li>A diagram can save you a lot of words in this essay: a labelled sarcomere, say, or the cross-bridge cycle, or the forearm as a lever. Draw it with <b>Insert drawing</b> (the pencil), or draw it on paper and add a photo of it with <b>Insert picture</b>. Type a caption under it, and refer to it in your text.</li>
</ul>
{activity("Write it, and hand it in", [
    task("es3-start", f'Open the essay {exam(PAPER, "show me")}, read its first page, and press <b>Start</b> when you’re ready to write.', auto=f"exam:start paper={PAPER}", check=f"paper:{PAPER}.started"),
    task("es3-write", 'Plan, then write. Aim for an introduction that says what your essay will argue, paragraphs that each make one point and show how it helps to answer the question, and a conclusion that draws them together.', auto=f"exam:words paper={PAPER} words>299"),
    task("es3-submit", 'When you’ve finished, go to the submission page (the ✓ tile at the bottom right), check your essay and submit it.', auto=f"exam:submit paper={PAPER}", check=f"paper:{PAPER}.submitted"),
    task("es3-send", 'Hand it in on the page that comes up next. Type in the hand-in password and press <b>Hand it in</b>. The page shows you a receipt once your essay has arrived.', auto=f"exam:handin paper={PAPER} step=confirmed", check=f"paper:{PAPER}.handedIn"),
    task("es3-word", 'To keep a copy, press <b>Download a copy for yourself</b>, under the password box (once you’ve handed in, the button says <b>Download your copy</b>). The copy is saved as a Word document in your Downloads folder.', auto=f"exam:download paper={PAPER} format=docx", check=f"paper:{PAPER}.downloaded"),
])}
{hand_note}
{callout("info", "After you’ve handed it in", "<p>Once you’ve submitted, <b>Review my answers</b> shows you the ground a good answer would cover. Read it after you’ve handed your essay in, and make a note of what you’d add or change. That’s what we’ll talk about in the supervision.</p><p>Your essay is kept in this browser, in Files → <code>essays</code>. It won’t be there on another computer, so download it before you leave.</p>")}
{q("es3-q-next", "Once you’ve read the guidance, which step from molecules to whole animals did your essay cover least well, and what would you add?",
   "There’s no single right answer here, so bring yours to the supervision. Many essays on this title spend most of their words on the cross-bridge cycle and excitation–contraction coupling, and then rush the end: how the force of many fibres is graded and passed through tendons and levers to move a limb, and what that means for a whole animal as it walks, runs, swims or flies. Others describe each scale well but never say how one produces the next, which is what the title asks.")}
'''
    return chapter("s3-write", num, "Write your essay", "exam", "Write your essay, and hand it in", 45,
                   "This is the work to hand in this week. As before, you write it in Supervision work, as you will in "
                   "the online exam, and then hand it in from the same page. It goes straight into my Google Drive.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_more(num):
    saqs = ''.join(f'<li>{s}</li>' for s in SAQS)
    rev = ''.join(f'<li>{s}</li>' for s in REVISION)
    body = f'''
<h2 id="m3-saq">Short-answer questions</h2>
<p>These three go with this week’s lectures. Each is marked out of five, so answer in bullet points and make at least five.</p>
<ol class="titles">{saqs}</ol>
<p>They have a paper of their own in Supervision work {exam("s3-saqs", "open them")}. There’s no time limit, but about 10 minutes for each is a good aim. Sketch the graph for the first one with <b>Insert drawing</b> (the pencil). After you submit, <b>Review my answers</b> shows you what a good answer covers.</p>

<h2 id="m3-rev">Essay titles for revision</h2>
<p>It’s worth noting these down. They go with this week’s lectures, and they’re the kind of title you could meet in the exam.</p>
<ol class="titles">{rev}</ol>
<p>Planning an answer to each one (your argument, your evidence, and the order you’d put them in) is good revision. You could also write one up in Supervision work {exam("s3-revision", "open them")} in 40 minutes, for practice. After you submit, the guidance shows you the ground each title should cover.</p>
{optional(activity("If you want the practice", [
    task("m3-saq", 'Answer one or more of the short-answer questions, and submit them.', auto="exam:submit paper=s3-saqs"),
    task("m3-plan", 'Plan an answer to one of the revision titles. Sum up your position in a sentence, then jot down the three or four points, with the evidence for each, that would support it.'),
]), title='Practice')}
'''
    return chapter("s3-more", num, "More practice", "exam", "More practice: short answers and revision", None,
                   "This chapter is optional. It has three short-answer questions on this week’s lectures, and three "
                   "more essay titles to note down for revision. Only the essay needs to be handed in.", body)


def ALL():
    order = [ch_week, ch_fibres, ch_move, ch_write, ch_more]
    return [f(str(i)) for i, f in enumerate(order)]
