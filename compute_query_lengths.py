#!/usr/bin/env python3
"""
Auto-download and compute query-length statistics (mean, std, etc.)
for 5 text-to-video retrieval benchmarks:
    MSR-VTT, LSMDC, DiDeMo, ActivityNet Captions, VATEX

Simply run:
    python compute_query_lengths.py

Data is cached under ./benchmark_data/ so subsequent runs are fast.
LSMDC requires manual registration -- the script will skip it gracefully.

Download sources (all public, no auth needed):
  MSR-VTT:   GitHub release from ArrowLuo/CLIP4Clip
  DiDeMo:    GitHub raw from LisaAnne/LocalizingMoments
  ANet Cap:  GitHub raw from JaywongWang/DenseVideoCaptioning
  VATEX:     Official website eric-xw.github.io
  LSMDC:     Manual (MPII registration required)
"""

import csv
import json
import os
import subprocess
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

import numpy as np

CACHE_DIR = Path("./benchmark_data")
CACHE_DIR.mkdir(exist_ok=True)


def word_count(text: str) -> int:
    return len(text.strip().split())


def download(url: str, dest: Path, desc: str = "") -> bool:
    if dest.exists() and dest.stat().st_size > 100:
        print(f"  [cached] {dest}")
        return True
    print(f"  Downloading {desc}...")
    print(f"    URL: {url}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    ret = subprocess.run(
        ["wget", "-q", "--show-progress", "-L", "--no-check-certificate",
         url, "-O", str(dest)],
        timeout=600,
    )
    if ret.returncode != 0 or not dest.exists() or dest.stat().st_size < 100:
        print(f"  [FAIL] wget exit code {ret.returncode}")
        if dest.exists():
            dest.unlink()
        return False
    print(f"  [OK] {dest.stat().st_size / 1024:.0f} KB")
    return True


def try_download(urls: list, dest: Path, desc: str = "") -> bool:
    for url in urls:
        if download(url, dest, desc):
            return True
    return False


def report(lengths: list, name: str) -> dict:
    a = np.array(lengths, dtype=float)
    print(f"\n{'=' * 70}")
    print(f"  {name}")
    print(f"{'=' * 70}")
    print(f"  Total queries : {len(a):,}")
    print(f"  Mean  (words) : {a.mean():.2f}")
    print(f"  Std   (words) : {a.std():.2f}")
    print(f"  Median        : {np.median(a):.1f}")
    print(f"  Min / Max     : {int(a.min())} / {int(a.max())}")
    print(f"  25th / 75th   : {np.percentile(a, 25):.1f} / {np.percentile(a, 75):.1f}")
    return dict(name=name, n=len(a), mean=a.mean(), std=a.std(),
                median=np.median(a), mn=int(a.min()), mx=int(a.max()))


# ====================================================================
# 1. MSR-VTT
# ====================================================================
def process_msrvtt() -> list:
    print("\n>>> [1/5] MSR-VTT")
    outdir = CACHE_DIR / "msrvtt"; outdir.mkdir(exist_ok=True)
    zip_path = outdir / "msrvtt_data.zip"
    json_path = outdir / "MSRVTT_data.json"

    if not json_path.exists():
        ok = try_download([
            "https://github.com/ArrowLuo/CLIP4Clip/releases/download/v0.0/msrvtt_data.zip",
        ], zip_path, "MSR-VTT zip")
        if ok:
            with zipfile.ZipFile(zip_path) as zf:
                zf.extractall(outdir)
            # find the json wherever it was extracted
            for root, _, files in os.walk(outdir):
                for f in files:
                    if f == "MSRVTT_data.json":
                        src = Path(root) / f
                        if src != json_path:
                            import shutil; shutil.move(str(src), str(json_path))
                        break

    if not json_path.exists():
        print("  [SKIP] Could not get MSRVTT_data.json"); return []

    with open(json_path) as f:
        data = json.load(f)

    results = []
    all_lens = [word_count(s["caption"]) for s in data["sentences"]]
    results.append(report(all_lens, "MSR-VTT — all 200K captions"))

    vid2split = {v["video_id"]: v.get("split","") for v in data.get("videos",[])}
    for split in ("train", "validate", "test"):
        ids = {k for k,v in vid2split.items() if v == split}
        if ids:
            lens = [word_count(s["caption"]) for s in data["sentences"] if s["video_id"] in ids]
            results.append(report(lens, f"MSR-VTT — {split} split"))
    return results


# ====================================================================
# 2. LSMDC (manual)
# ====================================================================
def process_lsmdc() -> list:
    print("\n>>> [2/5] LSMDC")
    ldir = CACHE_DIR / "lsmdc"; ldir.mkdir(exist_ok=True)
    search_train = [
        ldir / "LSMDC16_annos_training_someone.csv",
        ldir / "LSMDC16_annos_training.csv",
        Path("LSMDC16_annos_training_someone.csv"),
    ]
    search_test = [
        ldir / "LSMDC16_challenge_1000_publictect.csv",
        Path("LSMDC16_challenge_1000_publictect.csv"),
    ]
    train_csv = next((p for p in search_train if p.exists()), None)
    test_csv  = next((p for p in search_test  if p.exists()), None)

    if not train_csv and not test_csv:
        print("  [SKIP] LSMDC requires manual download (registration).")
        print(f"    Place CSVs in: {ldir.resolve()}/")
        return []

    results = []
    for tag, fp in [("train ~101K", train_csv), ("test 1K", test_csv)]:
        if not fp: continue
        lens = []
        with open(fp, encoding="utf-8", errors="replace") as f:
            for row in csv.reader(f, delimiter="\t"):
                if len(row) >= 2:
                    c = row[-1].strip()
                    if c: lens.append(word_count(c))
        if lens: results.append(report(lens, f"LSMDC — {tag}"))
    return results


# ====================================================================
# 3. DiDeMo
#    Source: LisaAnne/LocalizingMoments on GitHub (original author)
# ====================================================================
def process_didemo() -> list:
    print("\n>>> [3/5] DiDeMo")
    ddir = CACHE_DIR / "didemo"; ddir.mkdir(exist_ok=True)

    # Original data from the paper author's GitHub repo
    gh_raw = "https://raw.githubusercontent.com/LisaAnne/LocalizingMoments/master/data"

    results = []
    for split in ("train", "val", "test"):
        fname = f"{split}_data.json"
        fpath = ddir / fname
        try_download([f"{gh_raw}/{fname}"], fpath, f"DiDeMo {split}")
        if not fpath.exists(): continue

        with open(fpath) as f:
            items = json.load(f)

        vid_sents = defaultdict(list)
        indiv = []
        for item in items:
            vid = item.get("video", item.get("video_id", ""))
            cap = item.get("caption", item.get("sentence",
                  item.get("description", "")))
            if cap:
                indiv.append(word_count(cap))
                vid_sents[vid].append(cap)
        para = [word_count(" ".join(ss)) for ss in vid_sents.values()]

        if indiv:
            results.append(report(indiv, f"DiDeMo {split} — individual sentences"))
        if para:
            results.append(report(para, f"DiDeMo {split} — concat. paragraphs (retrieval query)"))
    return results


# ====================================================================
# 4. ActivityNet Captions
#    Source: JaywongWang/DenseVideoCaptioning on GitHub (has the JSONs)
#    Backup: 26hzhang/VSLNet
# ====================================================================
def process_anet() -> list:
    print("\n>>> [4/5] ActivityNet Captions")
    adir = CACHE_DIR / "activitynet"; adir.mkdir(exist_ok=True)

    # These repos host the original ActivityNet Captions JSONs
    gh1 = "https://raw.githubusercontent.com/JaywongWang/DenseVideoCaptioning/master/dataset/ActivityNet_Captions"
    gh2 = "https://raw.githubusercontent.com/26hzhang/VSLNet/master/data/dataset/activitynet"

    results = []
    for tag, fname in [("train", "train.json"), ("val1", "val_1.json")]:
        fpath = adir / fname
        try_download([
            f"{gh1}/{fname}",
            f"{gh2}/{fname}",
        ], fpath, f"ActivityNet Captions {tag}")
        if not fpath.exists(): continue

        with open(fpath) as f:
            data = json.load(f)

        indiv, para = [], []
        for vid, info in data.items():
            sents = info.get("sentences", [])
            for s in sents:
                indiv.append(word_count(s))
            if sents:
                para.append(word_count(" ".join(sents)))

        if indiv:
            results.append(report(indiv, f"ActivityNet Captions {tag} — individual sentences"))
        if para:
            results.append(report(para, f"ActivityNet Captions {tag} — concat. paragraphs (retrieval query)"))
    return results


# ====================================================================
# 5. VATEX
#    Source: Official website
# ====================================================================
def process_vatex() -> list:
    print("\n>>> [5/5] VATEX")
    vdir = CACHE_DIR / "vatex"; vdir.mkdir(exist_ok=True)

    urls = {
        "train": ("https://eric-xw.github.io/vatex-website/data/vatex_training_v1.0.json",
                   vdir / "vatex_training_v1.0.json"),
        "val":   ("https://eric-xw.github.io/vatex-website/data/vatex_validation_v1.0.json",
                   vdir / "vatex_validation_v1.0.json"),
    }

    results = []
    for tag, (url, fpath) in urls.items():
        try_download([url], fpath, f"VATEX {tag}")
        if not fpath.exists(): continue

        with open(fpath) as f:
            data = json.load(f)

        en_lens, zh_lens = [], []
        for item in data:
            for c in item.get("enCap", []):
                en_lens.append(word_count(c))
            for c in item.get("chCap", []):
                zh_lens.append(len(c.replace(" ", "")))

        if en_lens:
            results.append(report(en_lens, f"VATEX {tag} — English (word count)"))
        if zh_lens:
            results.append(report(zh_lens, f"VATEX {tag} — Chinese (char count)"))
    return results


# ====================================================================
def main():
    print("=" * 70)
    print("  Text-to-Video Retrieval: Query Length Statistics")
    print(f"  Cache: {CACHE_DIR.resolve()}")
    print("=" * 70)

    all_results = []
    all_results += process_msrvtt()
    all_results += process_lsmdc()
    all_results += process_didemo()
    all_results += process_anet()
    all_results += process_vatex()

    print("\n\n")
    print("=" * 85)
    print("  FINAL SUMMARY")
    print("=" * 85)
    print(f"  {'Dataset':<60} {'N':>8} {'Mean':>7} {'Std':>7}")
    print("-" * 85)
    for r in all_results:
        print(f"  {r['name']:<60} {r['n']:>8,} {r['mean']:>7.2f} {r['std']:>7.2f}")

    if not all_results:
        print("\n  Nothing processed.")
        print("  If downloads fail, manually place files in ./benchmark_data/")
        print("  Subfolder structure: msrvtt/, didemo/, activitynet/, vatex/, lsmdc/")

if __name__ == "__main__":
    main()