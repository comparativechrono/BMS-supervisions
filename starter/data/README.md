# The starter data

The files here are copied into each student's home folder on their first visit (`starter/data/x.csv` becomes
`~/data/x.csv`). This file isn't copied.

## heart-rate-24h.csv

The heart rate of 18 people, hour by hour, through a day and a night: from the long-term ECGs of the **MIT-BIH Normal
Sinus Rhythm Database** on PhysioNet (`nsrdb`, version 1.0.0). The database's subjects are 5 men aged 26 to 45 and
13 women aged 20 to 50, who were referred to the Arrhythmia Laboratory of Boston's Beth Israel Hospital and found to
have had no significant arrhythmias. Each recording is about a day long, and every beat in it is labelled. The
recordings were made as people went about their day; nothing is known of when they slept, ate or exercised.

| Column | What it is |
| --- | --- |
| `subject` | The record (one person) |
| `sex`, `age` | As the record's header gives them (F or M; years) |
| `hour` | The clock hour that the row covers, 0 to 23 (13 is 13:00–14:00) |
| `time` | The same, as a time: `"13:00"` |
| `hr` | The heart rate over that hour, in beats per minute (`NA`: too few valid beats) |
| `n_beats` | How many beat-to-beat intervals the heart rate comes from |

432 rows (18 people × 24 hours). 50 hours are `NA`, nearly all in the morning: the beat labels of most records stop
an hour or a few hours before the end of the day (the hours of the next morning, after the time at which the
recording started), and a few hours had too much noise.

**How it was made** – `build/s1/heart_rate.py` (`python3 build/s1/heart_rate.py`, which downloads the records'
headers and beat labels from PhysioNet and checks them against the database's checksums). For each person it takes
the first 24 hours after the recording started (the header gives the clock time) and keeps the normal-to-normal (NN)
intervals: the times between two consecutive beats that were both labelled normal (N), 0.3 to 2 s long, with no
change of signal quality between them, and no more than 30% away from the median of the ten intervals around them
(which leaves out an interval with a missed or an extra beat in it; the database's marks of artefacts, which are not
beats, are passed over). The heart rate for each clock hour is 60 ÷ the mean NN interval of that hour; an hour with
less than 30 minutes of valid intervals is `NA`. In a recording that started at 08:04, the hour 08:00 is made of
08:04–09:00 on the first day and 08:00–08:04 on the second.

**Licence** – the database is published under the **Open Data Commons Attribution License v1.0**
(https://opendatacommons.org/licenses/by/1-0/), and so is this file, which is derived from it. Please cite:

- Goldberger AL, Amaral LAN, Glass L, Hausdorff JM, Ivanov PCh, Mark RG, Mietus JE, Moody GB, Peng C-K, Stanley HE.
  PhysioBank, PhysioToolkit, and PhysioNet: components of a new research resource for complex physiologic signals.
  Circulation 101(23):e215–e220 (2000). https://doi.org/10.1161/01.CIR.101.23.e215
- Pollard T, Moody BE, Lehman L, et al. PhysioNet as a global platform for biomedical research. Nature Health (2026).
  https://doi.org/10.1038/s44360-026-00096-z
- MIT-BIH Normal Sinus Rhythm Database (version 1.0.0). PhysioNet. https://doi.org/10.13026/C2NK5R
