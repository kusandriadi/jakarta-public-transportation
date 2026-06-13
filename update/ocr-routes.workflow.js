export const meta = {
  name: 'tj-route-halte-ocr',
  description: 'Read Transjakarta route-map images and extract per-route halte sequences as markdown',
  phases: [{ title: 'Read routes', detail: 'subagents OCR batches of route images' }],
}

// args = JSON array of absolute image paths (from update/route_files.json).
// Arrives as a string when passed via the Workflow tool — parse defensively.
const paths = typeof args === 'string' ? JSON.parse(args) : args
const B = 7
const batches = []
for (let i = 0; i < paths.length; i += B) batches.push({ idx: batches.length, files: paths.slice(i, i + B) })

log(`Reading ${paths.length} route images in ${batches.length} batches of ${B}`)

const instr = (files) => `You are extracting Transjakarta route data from official route-map images.

Read EACH of these image files with the Read tool (read them one by one):
${files.map((f, i) => `${i + 1}. ${f}`).join('\n')}

Each image is a Transjakarta route map. Top-left is the route NAME (e.g. "TMII - Pancoran"), top-right is the route CODE (e.g. "7D"). Below is a table with operating hours ("Keberangkatan Awal/Akhir") and day badges (WD=weekday, WE=weekend). Then a vertical line with halte names down BOTH sides — the LEFT column is one direction, the RIGHT column is the opposite direction. Small colored circles next to a halte are interchange badges (numbers = connecting corridor/route; rail icons = MRT/LRT/KCI station).

For EACH image, output one markdown block in EXACTLY this format:

### <CODE> — <NAME>
- Jam: <awal>–<akhir> (<days, e.g. Setiap hari / Hari kerja>)
- Arah 1 (<first halte> → <last halte>): halteA · halteB · halteC · ...
- Arah 2 (<first halte> → <last halte>): halteA · halteB · ...
- Transfer: <haltes with interchange badges and what they connect to, e.g. "Cawang (4K,5C,7); Ciliwung (KCI)">

Rules:
- List ALL haltes in order, top to bottom, for each direction. Do not skip any.
- If the route is a one-way loop (single column / circular), output only "Arah 1" and note "(loop)".
- Use the exact halte spelling shown. Separate haltes with " · ".
- If a field is unreadable write "?". If badges are too small, write "ada beberapa transfer" rather than guessing.
- Output ONLY the markdown blocks for all ${files.length} images, in order, separated by a blank line. No preamble.

Your entire final message must be the concatenated markdown blocks — that text IS the return value.`

const results = await parallel(batches.map(b => () =>
  agent(instr(b.files), { label: `routes#${b.idx + 1}`, phase: 'Read routes', agentType: 'general-purpose' })
))

const ok = results.filter(Boolean)
log(`Got ${ok.length}/${batches.length} batches back`)
return ok.join('\n\n')
