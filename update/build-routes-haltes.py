#!/usr/bin/env python3
"""Build references/routes-haltes.md from the OCR workflow output.

Usage:
    build-routes-haltes.py <input> <output.md> [extra_blocks.md]

<input> may be either:
  - the workflow task .output file (JSON with a "result" string key), or
  - a raw text/markdown file of "### CODE — NAME" blocks.

Groups routes (BRT/feeder, Mikrotrans JAK, Royaltrans/Transjabodetabek, Bus
Wisata), natural-sorts within each group, de-duplicates by code (first wins),
and writes the final reference file. Pass an optional extra_blocks file to merge
hand-transcribed routes the OCR missed.
"""
import json
import re
import sys


def load_body(path):
    raw = open(path, encoding="utf-8").read()
    try:
        data = json.loads(raw)
        if isinstance(data, dict) and "result" in data:
            return data["result"]
        if isinstance(data, str):
            return data
    except json.JSONDecodeError:
        pass
    return raw


def code_of(block):
    m = re.match(r"### (.+?) —", block)
    return m.group(1).strip() if m else "???"


def clean_block(block):
    """Drop leaked OCR/model narration. A valid block only contains the `### `
    header and `- ` data lines (Jam/Arah/Transfer); any other non-blank line is
    prose that leaked from the OCR workflow's reasoning — strip it."""
    kept = []
    for ln in block.splitlines():
        s = ln.strip()
        if not s or s.startswith("###") or s.startswith("-"):
            kept.append(ln)
    return "\n".join(kept).strip()


def norm(code):
    return code.replace(".", "").replace(" ", "").upper()


def group_of(code):
    n = norm(code)
    if n.startswith("JAK"):
        return "MIKRO"
    if n.startswith("BW"):
        return "WISATA"
    if n == "L13E":
        return "BRT"
    if re.match(r"^[A-Z]", n):
        return "REGIONAL"
    return "BRT"


def natkey(code):
    n = norm(code)
    if n.startswith("JAK"):
        n = n[3:]
    m = re.match(r"^([A-Z]*)(\d+)?([A-Z]*)$", n)
    if m:
        return (m.group(1), int(m.group(2)) if m.group(2) else 0, m.group(3))
    return (n, 0, "")


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src, out = sys.argv[1], sys.argv[2]
    body = load_body(src)
    if len(sys.argv) > 3:
        body = body.rstrip() + "\n\n" + open(sys.argv[3], encoding="utf-8").read().strip() + "\n"

    parts = re.split(r"(?m)^(?=### )", body)
    blocks = [clean_block(b) for b in parts if b.strip().startswith("### ")]

    seen, uniq = set(), []
    for b in blocks:
        c = norm(code_of(b))
        if c in seen:
            continue
        seen.add(c)
        uniq.append(b)

    groups = {"BRT": [], "MIKRO": [], "REGIONAL": [], "WISATA": []}
    for b in uniq:
        groups[group_of(code_of(b))].append(b)
    for g in groups:
        groups[g].sort(key=lambda b: natkey(code_of(b)))

    total = sum(len(v) for v in groups.values())
    header = f"""# Transjakarta — Halte per Rute (urutan lengkap dua arah)

Setiap rute dengan urutan halte lengkap kedua arah + jam operasi + titik
transfer. Sumber: peta rute resmi Transjakarta
(`smk.transjakarta.co.id/aset/berkas/rute/`) — **{total} rute**. Rute berubah
berkala; regenerate dengan `update/` (lihat UPDATE.md) atau verifikasi di **Tije**.

Kode: koridor BRT 1–14 & lintas-koridor (mis. 2A, 3F, L13E) + pengumpan (mis. 7D,
8K, 1B) di **BRT/Koridor/Pengumpan**; **JAK** = Mikrotrans; huruf-angka
(B/D/S/T/P/SH) = Royaltrans/Transjabodetabek; **BW** = Bus Wisata.

> Pasangan dengan `transjakarta.md` (ringkasan koridor) & `transjakarta-feeder.md`
> (daftar rute + asal-tujuan). File ini untuk detail halte.

"""
    secs = [
        ("BRT", "## BRT, Koridor & Pengumpan (kode angka)"),
        ("MIKRO", "## Mikrotrans (JAK)"),
        ("REGIONAL", "## Royaltrans & Transjabodetabek (kode huruf)"),
        ("WISATA", "## Bus Wisata (BW)"),
    ]
    chunks = [header]
    for g, title in secs:
        chunks.append(title + "\n")
        chunks.append("\n\n".join(groups[g]))
        chunks.append("")
    open(out, "w", encoding="utf-8").write("\n".join(chunks))
    print(f"Wrote {out}: {total} routes "
          f"(BRT {len(groups['BRT'])}, Mikrotrans {len(groups['MIKRO'])}, "
          f"Regional {len(groups['REGIONAL'])}, Wisata {len(groups['WISATA'])})")


if __name__ == "__main__":
    main()
