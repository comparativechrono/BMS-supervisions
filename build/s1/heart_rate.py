#!/usr/bin/env python3
"""Make starter/data/heart-rate-24h.csv: 24 hours of the heart rate of 18 people, hour by hour, from the long-term ECGs
of the MIT-BIH Normal Sinus Rhythm Database (PhysioNet, nsrdb 1.0.0; Open Data Commons Attribution License v1.0).

Each record of the database is about a day of the ECG of one person (5 men aged 26 to 45 and 13 women aged 20 to 50,
"found to have had no significant arrhythmias"), with every beat labelled. Its header gives the clock time at which
the recording started, and the person's age and sex. For each person, this script takes the first 24 hours after the
start, keeps the normal-to-normal (NN) intervals – the times between two consecutive beats that were both labelled
normal (N), 0.3 to 2 s long, with no change of signal quality (a noise mark, ~) between them, and no more than 30 %
away from the median of the ten intervals around them (which leaves out an interval with a missed or an extra beat in
it); the database's artefact marks (|), which are not beats, are passed over – and gives, for each clock hour (0 to
23), the heart rate over the hour: 60 ÷ the mean NN interval, in beats per minute. A clock hour with less than 30
minutes of valid intervals is NA. (In a recording that started at 08:04, the hour 08:00 is made of 08:04–09:00 on
the first day and 08:00–08:04 on the second.)

Columns: subject (the record), sex (F or M), age (years), hour (the clock hour the row covers, 0–23), time ("08:00"),
hr (beats per minute, one decimal place; NA if there were too few valid intervals), n_beats (the NN intervals used).

Run:
    python3 build/s1/heart_rate.py                    # downloads the headers and annotations into the cache first
    python3 build/s1/heart_rate.py --src DIR          # or reads them from DIR (the .hea and .atr files)
Options: --cache DIR (default ~/.cache/bms-workbench/physionet). Needs numpy and wfdb (pip install numpy wfdb)."""
import argparse
import hashlib
import os
import sys
import time
import urllib.request

import numpy as np
import wfdb

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(SITE, 'starter', 'data', 'heart-rate-24h.csv')
DB, VER = 'nsrdb', '1.0.0'
BASE = f'https://physionet.org/files/{DB}/{VER}/'
# the labels of beats (MIT-BIH conventions); every other label (noise ~, artefact |, rhythm +, comment " …) is not a beat
BEATS = set('NLRBAaJSVrFejnE/fQ?')
MIN_RR, MAX_RR = 0.3, 2.0
MIN_VALID_S = 30 * 60


def http_get(url, path, tries=5):
    err = None
    for k in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=120) as r, open(path + '.part', 'wb') as f:
                f.write(r.read())
            os.replace(path + '.part', path)
            return
        except Exception as e:  # noqa: BLE001
            err = e
            time.sleep(3 * (k + 1))
    raise RuntimeError(f'could not download {url}: {err}')


def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def fetch(cache):
    """the database's headers and beat annotations, downloaded into the cache and checked against its SHA256SUMS"""
    d = os.path.join(cache, DB, VER)
    os.makedirs(d, exist_ok=True)
    for f in ('RECORDS', 'SHA256SUMS.txt'):
        if not os.path.exists(os.path.join(d, f)):
            http_get(BASE + f, os.path.join(d, f))
    sums = {}
    for line in open(os.path.join(d, 'SHA256SUMS.txt')):
        p = line.split()
        if len(p) == 2:
            sums[p[1]] = p[0]
    for rec in open(os.path.join(d, 'RECORDS')).read().split():
        for ext in ('.hea', '.atr'):
            p = os.path.join(d, rec + ext)
            if os.path.exists(p) and sha256(p) == sums.get(rec + ext):
                continue
            print('downloading', rec + ext)
            http_get(BASE + rec + ext, p)
            if sums.get(rec + ext) and sha256(p) != sums[rec + ext]:
                os.remove(p)
                raise RuntimeError(f'{rec}{ext} does not match its checksum: try again')
    return d


def hours(src, rec):
    """one person's 24 hours: [(hour, hr or None, n_beats)], and their sex and age"""
    hd = wfdb.rdheader(os.path.join(src, rec))
    fs = hd.fs
    start = hd.base_time  # a datetime.time
    t0 = start.hour * 3600 + start.minute * 60 + start.second
    age, sex = None, None
    for c in hd.comments or []:
        p = c.split()
        if len(p) >= 2 and p[0].isdigit() and p[1] in ('M', 'F'):
            age, sex = int(p[0]), p[1]
    ann = wfdb.rdann(os.path.join(src, rec), 'atr')
    samp = np.asarray(ann.sample, dtype=np.int64)
    sym = list(ann.symbol)
    end = 24 * 3600 * fs  # (the first 24 hours after the start)
    sums = np.zeros(24)  # the time covered by valid intervals in each clock hour (s)
    counts = np.zeros(24, dtype=int)
    # the intervals between consecutive beats: (start sample, end sample, both normal and no noise mark between them)
    iv = []
    prev = None  # the last beat: (sample, symbol), or None after a change of signal quality
    for s, y in zip(samp, sym):
        if y == '~':
            prev = None  # (a change of signal quality between two beats: the interval is not used)
            continue
        if y not in BEATS:
            continue  # (an artefact mark |, a rhythm change + or a comment: not a beat, passed over)
        if prev is not None:
            iv.append((prev[0], s, prev[1] == 'N' and y == 'N'))
        prev = (s, y)
    rrs = np.array([(b - a) / fs for a, b, _ in iv])
    for k, (a, b, nn) in enumerate(iv):
        rr = rrs[k]
        if not nn or not (MIN_RR <= rr <= MAX_RR):
            continue
        # (a missed or an extra beat: more than 30 % from the median of the ten intervals around it)
        near = rrs[max(0, k - 5):k + 6]
        med = float(np.median(near))
        if abs(rr - med) > 0.3 * med:
            continue
        mid = (a + b) / 2
        if mid >= end:
            continue
        h = int(((t0 + mid / fs) // 3600) % 24)
        sums[h] += rr
        counts[h] += 1
    out = []
    for h in range(24):
        if sums[h] >= MIN_VALID_S:
            out.append((h, 60.0 / (sums[h] / counts[h]), int(counts[h])))
        else:
            out.append((h, None, int(counts[h])))
    return sex, age, out, hd


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--src', help='a folder with the records’ .hea and .atr files (else they are downloaded)')
    ap.add_argument('--cache', default=os.path.expanduser('~/.cache/bms-workbench/physionet'))
    a = ap.parse_args()
    src = a.src or fetch(a.cache)
    recs = sorted(f[:-4] for f in os.listdir(src) if f.endswith('.hea'))
    rows = []
    for rec in recs:
        sex, age, hs, hd = hours(src, rec)
        n_na = sum(1 for _, hr, _ in hs if hr is None)
        print(f'{rec}: {sex} {age}, started {hd.base_time}, {hd.sig_len / hd.fs / 3600:.2f} h; {n_na} hours NA')
        for h, hr, n in hs:
            rows.append((rec, sex, age, h, f'{h:02d}:00', 'NA' if hr is None else f'{hr:.1f}', n))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('subject,sex,age,hour,time,hr,n_beats\n')
        for r in rows:
            f.write(','.join(str(x) for x in r) + '\n')
    print(f'wrote {os.path.relpath(OUT, SITE)}: {len(rows)} rows, {os.path.getsize(OUT)} bytes')


if __name__ == '__main__':
    sys.exit(main())
