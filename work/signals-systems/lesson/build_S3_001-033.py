# -*- coding: utf-8 -*-
# 3주차(S3) 회독 레슨 1~33쪽 생성기. 사용: python build_S3_001-033.py
# 도우미 S3_001-033_lib.py, 그림 S3_001-033_figs.py, 쪽 S3_001-033_pA~pD.py 를 차례로 읽는다.
import os, cmath, math

HERE = os.path.dirname(os.path.abspath(__file__))
G = {"__name__": "s3_001_033", "math": math, "cmath": cmath, "__file__": os.path.join(HERE, "S3_001-033_lib.py")}


def _run(name):
    path = os.path.join(HERE, name)
    with open(path, encoding="utf-8") as f:
        exec(compile(f.read(), path, "exec"), G)


_run("S3_001-033_lib.py")
G["cmath_exp_j"] = lambda th: cmath.exp(1j * th)
G["S"] = []
_run("S3_001-033_figs.py")
for part in ("pA", "pB", "pC", "pD"):
    if os.path.exists(os.path.join(HERE, f"S3_001-033_{part}.py")):
        _run(f"S3_001-033_{part}.py")

G["build"](os.path.join(HERE, "S3_001-033.json"), "S3", 1, 33, G["S"])
