#!/usr/bin/env bash
# Refresh Transjakarta route-map images + KRL map from official sources.
# Deterministic part of the skill update. After running this, run the OCR
# workflow (update/ocr-routes.workflow.js) then update/build-routes-haltes.py.
# See UPDATE.md for the full procedure.
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK="${1:-/tmp/jakarta-public-transportation-update}"
ROUTES="$WORK/tjroutes"
mkdir -p "$ROUTES"
cd "$WORK"

echo "==> Work dir: $WORK"
echo "==> Skill dir: $SKILL_DIR"

# 1. Fetch the 5 Transjakarta service listing pages
PAGES=(brt angkutan-pengumpan mikrotrans royaltrans wisata)
for p in "${PAGES[@]}"; do
  curl -sL "https://transjakarta.co.id/layanan/$p" -o "tj_$p.html"
  n=$(grep -oE 'https://smk.transjakarta.co.id/aset/berkas/rute/[^"]+\.(jpg|jpeg|png)' "tj_$p.html" | sort -u | wc -l)
  printf "    %-20s %s route images\n" "$p" "$n"
done

# 2. Collect unique route-image URLs
cat tj_*.html \
  | grep -oE 'https://smk.transjakarta.co.id/aset/berkas/rute/[^"]+\.(jpg|jpeg|png)' \
  | sort -u > all_route_images.txt
echo "==> $(wc -l < all_route_images.txt) unique route images"

# 3. Download all images in parallel
echo "==> Downloading images to $ROUTES ..."
( cd "$ROUTES" && xargs -P 16 -I{} sh -c 'curl -sL "{}" -o "$(basename "{}")"' < ../all_route_images.txt )
echo "==> Downloaded $(ls -1 "$ROUTES" | wc -l) files ($(du -sh "$ROUTES" | cut -f1))"

# 4. Verify all are images
bad=0
for f in "$ROUTES"/*; do
  file -b "$f" | grep -qiE 'image|JPEG|PNG' || { echo "    BAD: $f"; bad=$((bad+1)); }
done
[ "$bad" -eq 0 ] && echo "==> All images valid" || echo "==> WARNING: $bad non-image files"

# 5. Build JSON array of absolute paths (input for the OCR workflow's `args`)
ls -1 "$ROUTES" | sort | sed "s#^#$ROUTES/#" \
  | python3 -c "import sys,json; print(json.dumps([l.strip() for l in sys.stdin]))" \
  > route_files.json
echo "==> Wrote route_files.json ($(python3 -c "import json;print(len(json.load(open('route_files.json'))))") paths)"

# 6. Refresh the KRL Jabodetabek & Merak map into the skill assets
curl -sL "https://banner-access.krl.co.id/banner-access/assets/maps/4c468c4dde4663d22270f3ce25ac32d2.png" \
  -o "$SKILL_DIR/assets/krl-map.png" \
  && echo "==> Refreshed assets/krl-map.png" || echo "==> WARN: KRL map download failed (URL may have changed)"

cat <<EOF

==> NEXT STEPS (see UPDATE.md):
    1. Run OCR workflow over the images:
         Workflow({ scriptPath: "$SKILL_DIR/update/ocr-routes.workflow.js",
                    args: <contents of $WORK/route_files.json> })
    2. When it completes, build the reference file:
         python3 "$SKILL_DIR/update/build-routes-haltes.py" \\
                 <workflow-output.json> "$SKILL_DIR/references/routes-haltes.md"
    3. Re-read assets/krl-map.png and refresh references/krl.md, mrt-lrt.md,
       transjakarta.md, transjakarta-feeder.md per their sources.
EOF
