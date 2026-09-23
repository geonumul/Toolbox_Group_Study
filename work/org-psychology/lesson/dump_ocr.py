# -*- coding: utf-8 -*-
"""작성용: 글자 층에 없는 그림 속 글(OCR 줄)의 좌표 보기. python dump_ocr.py O2 5,6,7
recall/_ocr/<덱>.json (tools/recall_build.py 가 만든 OCR 캐시) 을 읽는다."""
import json, os, sys
from build_common import lines, W_DIR

sys.stdout.reconfigure(encoding="utf-8")
deck = sys.argv[1]
ocr = json.load(open(os.path.join(W_DIR, "recall", "_ocr", f"{deck}.json"), encoding="utf-8"))
for p in [int(x) for x in sys.argv[2].split(",")]:
    pg = ocr[p - 1]
    W, H = pg["w"], pg["h"]
    pdf = lines(deck, p)
    print(f"== {deck} p.{p} (OCR, 글자 층 밖)")
    for ws in pg["lines"]:
        if not ws:
            continue
        x0 = min(w[1] for w in ws) / W; y0 = min(w[2] for w in ws) / H
        x1 = max(w[1] + w[3] for w in ws) / W; y1 = max(w[2] + w[4] for w in ws) / H
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        if any(l[0] - 0.01 <= cx <= l[2] + 0.01 and l[1] - 0.01 <= cy <= l[3] + 0.01 for l in pdf):
            continue
        if cy < 0.09 and cx > 0.62:
            continue
        print(f"  x{x0:.3f}-{x1:.3f} y{y0:.3f}-{y1:.3f} {' '.join(w[0] for w in ws)[:70]}")
