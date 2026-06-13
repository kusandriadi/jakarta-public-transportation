# jakarta-public-transportation

An [Agent Skill](https://docs.claude.com/en/docs/claude-code/skills) for routing
across **Jakarta / Jabodetabek public transport** — Transjakarta, MRT, LRT, KRL,
KA Bandara, and Whoosh high-speed rail. It answers "naik apa dari A ke B" from
captured data rather than guesses, optimizing for both fastest and cheapest.

## Contents

- `SKILL.md` — routing rules + interchange-hub map (the entry point)
- `references/` — the data: corridors, per-halte stop sequences (208 routes),
  MRT/LRT/KRL lines, Whoosh, fares, operating hours
- `assets/krl-map.png` — KRL Jabodetabek & Merak route map
- `UPDATE.md` + `update/` — pipeline to re-scan and regenerate the data

## Install

Drop this folder into your agent's skills directory (Claude Code:
`~/.claude/skills/jakarta-public-transportation/` or a project
`.claude/skills/`). The agent discovers it via the `SKILL.md` frontmatter.

## Note

Transit data was captured around 2026 and drifts over time — for live fares and
schedules use the official apps (Tije, MRT-J, KRL Access, Whoosh App). See
`UPDATE.md` to refresh.

## License

[MIT](LICENSE).
