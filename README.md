# jakarta-public-transportation

An [Agent Skill](https://docs.claude.com/en/docs/claude-code/skills) for **routing
across Jakarta / Jabodetabek public transport**. It answers "naik apa dari A ke B"
from **captured real-world data** rather than guesses, and optimizes every trip for
both the **fastest** and the **cheapest** option.

It covers all the BRT + rail systems in one place and knows where they physically
connect, so it can chain a multi-system journey (e.g. KRL → MRT → Transjakarta) end
to end instead of answering one mode at a time.

## What it covers

| System | Scope |
|---|---|
| **Transjakarta** | World's longest BRT — **14 BRT corridors** + feeder (Angkutan Pengumpan), **Mikrotrans** (Jak Lingko), Royaltrans, Transjabodetabek, Bus Wisata. Full per-halte stop sequences for **208 routes**, both directions, with transfer points. |
| **MRT Jakarta** | North–South line (Lebak Bulus ↔ Bundaran HI, operating) + East–West line (under construction). |
| **LRT Jakarta** (city) | Pegangsaan Dua ↔ Velodrome. |
| **LRT Jabodebek** (regional) | Cibubur & Bekasi lines via the Dukuh Atas–Cawang trunk. |
| **KRL Commuter** | All 5 lines — Bogor (Red), Cikarang (Blue), Rangkasbitung (Green), Tangerang (Brown), Tanjung Priok (Pink) — every station. |
| **KA Bandara & Skytrain** | Airport train Manggarai ↔ Soekarno-Hatta + Kalayang skytrain. |
| **KA Lokal Merak** | Rangkasbitung ↔ Merak (LM1–LM11). |
| **Whoosh** (KCIC HSR) | Jakarta–Bandung high-speed rail — 4 stations (Halim · Karawang · Padalarang · Tegalluar), all-stop, no express. |
| **Fares & hours** | Per-mode fares (cheapest-option logic + Jak Lingko integration cap) and operating hours / headway across modes. |

## Contents

```
jakarta-public-transportation/
├── SKILL.md                    # routing rules + interchange-hub map (entry point)
├── references/                 # the data — read these before answering
│   ├── transjakarta.md         #   14 BRT corridor summaries
│   ├── transjakarta-feeder.md  #   feeder / Mikrotrans / Royaltrans route list
│   ├── routes-haltes.md        #   per-halte detail, 208 routes, both directions
│   ├── mrt-lrt.md              #   MRT + LRT Jakarta + LRT Jabodebek
│   ├── krl.md                  #   KRL Commuter + KA Bandara + KA Lokal Merak
│   ├── whoosh.md               #   Whoosh HSR Jakarta–Bandung
│   ├── fares.md                #   per-mode fares + cheapest-option logic
│   └── hours.md                #   operating hours & headway per mode
├── assets/krl-map.png          # KRL Jabodetabek & Merak route map
└── UPDATE.md + update/         # pipeline to re-scan & regenerate the data
```

## How it answers

1. **Reads the relevant `references/` doc(s) first** — it never improvises a route
   from generic web knowledge.
2. **Prefers a single mode** when one covers the trip; otherwise chains via an
   **interchange hub** (Dukuh Atas/Sudirman, CSW/ASEAN, Manggarai, Jakarta Kota,
   Cawang, …) and minimizes unnecessary transfers.
3. Returns a **concrete, ordered answer** — where to board, where to transfer,
   where to alight — with fare and rough timing, giving both the fastest and the
   cheapest variant when they differ.

## Example questions it handles

- "Dari Ciledug ke Bundaran HI naik apa?" → Transjakarta Koridor 13 → CSW → MRT
  ASEAN (skybridge) → MRT to Bundaran HI.
- "KRL dari Bogor ke Bandara?" → Lin Bogor to Manggarai → KA Bandara to Soekarno-Hatta.
- "Cara paling murah Bekasi → Sudirman?" — weighs KRL vs LRT Jabodebek vs Transjakarta.
- "Jakarta ke Bandung pakai Whoosh, turun di mana?" — Halim → Padalarang/Tegalluar
  with onward connections.

## Install

Drop this folder into your agent's skills directory — Claude Code:
`~/.claude/skills/jakarta-public-transportation/`, or a project `.claude/skills/`.
The agent discovers it automatically via the `SKILL.md` frontmatter.

## Data freshness

Transit data was captured **around 2026** from official sources (Transjakarta /
Tije, MRT Jakarta, KAI Commuter, KCIC). Networks change — endpoints shift during
MRT/LRT construction, and fares and hours are adjusted periodically. The data here
is for choosing routes and estimating cost/time, **not** a live timetable. For live
fares, departures, and service alerts, use the official apps: **Tije**, **MRT-J**,
**KRL Access / C-Access**, **Whoosh App / Access by KAI**. Re-scan and regenerate
the data via the pipeline documented in `UPDATE.md`.

## License

[MIT](LICENSE).
