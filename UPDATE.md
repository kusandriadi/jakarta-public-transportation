# Updating the jakarta-public-transportation skill

**Trigger:** the user says "update skill", "update jakarta-public-transportation", "scan ulang",
"refresh rute", or similar. When that happens, re-scan all sources from scratch
and regenerate the reference files. Tell the user it takes a few minutes (the OCR
workflow is the slow part) and that it spends tokens.

The scrape pipeline is in `update/`. Run it in order.

---

## 1. Fetch + download (deterministic, scripted)

```bash
bash update/fetch-tj-routes.sh
```

This: fetches the 5 Transjakarta listing pages (`brt`, `angkutan-pengumpan`,
`mikrotrans`, `royaltrans`, `wisata`), extracts every route-map image URL,
downloads all images to `/tmp/jakarta-public-transportation-update/tjroutes/`, writes
`/tmp/jakarta-public-transportation-update/route_files.json` (the path list), and refreshes
`assets/krl-map.png`. Note the route count it prints (was 208 on 2026-06-07).

## 2. OCR the route images (workflow — the slow, token-heavy step)

Invoke the saved workflow, passing the path list as `args` (read
`route_files.json` and pass its array value verbatim):

```
Workflow({
  scriptPath: "<skill>/update/ocr-routes.workflow.js",
  args: <the JSON array from /tmp/jakarta-public-transportation-update/route_files.json>
})
```

~30 subagents read ~7 images each and return markdown blocks. It runs in the
background; you're notified on completion. The full result is in the task
`.output` file (a JSON object with a `result` string).

## 3. Build the reference file (deterministic, scripted)

```bash
python3 update/build-routes-haltes.py <task-output.json> references/routes-haltes.md
```

Groups, natural-sorts, and de-duplicates by code. Compare the printed route count
to step 1's download count. If a few clean-coded routes are missing (count <
downloads), read those specific images yourself and pass them as a third arg
(an extra-blocks markdown file) to merge:

```bash
python3 update/build-routes-haltes.py <task-output.json> references/routes-haltes.md /tmp/extra_blocks.md
```

## 4. Refresh the rail + corridor reference docs (model steps)

These aren't fully scripted — re-read the sources and update the prose files:

- **`references/krl.md`** — re-read the refreshed `assets/krl-map.png` (crop &
  zoom regions for small text, e.g. the Merak line) and verify every line +
  station. Sources: the KAI Commuter Jabodetabek & Merak map.
- **`references/mrt-lrt.md`** — MRT Jakarta, LRT Jakarta, LRT Jabodebek lines &
  stations. Official sites are JS-rendered; Wikipedia (`Jakarta_MRT`,
  `LRT_Jakarta`, `Jabodebek_LRT`) is the reliable static source.
- **`references/transjakarta.md`** — BRT corridor halte lists. The official
  `/layanan/brt` page gives corridor + cross-corridor endpoints; per-corridor
  Wikipedia pages (`Koridor_N_Transjakarta`) give full halte lists.
- **`references/transjakarta-feeder.md`** — re-derive feeder / Mikrotrans /
  Royaltrans / Transjabodetabek / Wisata route lists (codes + origin–destination)
  from the listing pages fetched in step 1 and `routes-haltes.md`.

- **`references/fares.md`** — tarif tiap moda + skema tarif integrasi Jak Lingko.
  Tidak ada di OCR scan (hand-maintained). Saat update, verifikasi angka tarif
  resmi terbaru (Transjakarta Rp 3.500 / Mikrotrans gratis / KRL / MRT / LRT /
  KA Bandara) dan cap tarif integrasi. Yang wajib akurat adalah **urutan relatif**
  (termurah → termahal); angka rupiah pasti boleh diberi caveat "cek app resmi".

- **`references/whoosh.md`** — kereta cepat Whoosh (KCIC): 4 stasiun + integrasi,
  jam operasional, headway, 3 kelas/tarif. Hand-maintained (tidak ada di OCR
  scan). Saat update, verifikasi status stasiun (mis. Karawang), tarif kelas,
  jam pertama/terakhir, dan moda integrasi tiap stasiun. Tandai mana yang
  **seamless** vs **co-located**. Sumber: situs/app **KCIC (Whoosh App) /
  Access by KAI**, Wikipedia (`Jakarta–Bandung_high-speed_railway`), berita
  (jam/tarif sering berubah — beri caveat & arahkan ke app).

- **`references/hours.md`** — jam operasional & headway lintas-moda (MRT, LRT
  Jakarta, LRT Jabodebek, Transjakarta, JakLingko, Whoosh, KRL, KA Bandara).
  Hand-maintained. Saat update, verifikasi jam buka-tutup & headway resmi
  terbaru (jam pasti per stasiun/lin tetap arahkan ke app). Sumber: situs/app
  operator (Tije, MRT-J, KRL Access/C-Access, KAI, KCIC) + Wikipedia tiap moda;
  KRL & KA Bandara mengikuti GAPEKA (angka bergeser antar update).

## 5. Finalize

- Update the "captured ≈ <date>" / route-count notes in the touched files to the
  current date.
- Update the memory note (`jakarta-public-transportation-skill.md`) if counts changed
  materially.
- Summarize to the user what changed (new/removed routes, count deltas).

> **Note on source drift:** the KRL map URL and the route-image filename dates
> change over time. If `fetch-tj-routes.sh` downloads 0 images or the KRL map
> fails, the site structure changed — re-inspect `transjakarta.co.id/layanan/*`
> HTML for the new `smk.transjakarta.co.id/.../rute/` pattern and update the grep
> in the script.
