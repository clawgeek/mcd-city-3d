#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为麦当劳经营游戏创建：经营存档表 + 每日经营报表表。"""
import json, subprocess, os, sys

PY = r"C:\Users\10099\.workbuddy\binaries\python\versions\3.13.12\python.exe"
LIB = r"C:\Users\10099\AppData\Local\Programs\WorkBuddy\resources\app.asar.unpacked\resources\plugins\workbuddy-builtin\skills\library"
WS = r"C:\Users\10099\WorkBuddy\2026-10-24-16-20-51"
SPACE = "fwPdZMvtey16eALurOJ7Oj"

TABLES = [
    ("麦当劳经营存档", [
        ("用户标识", {"text": {}}),
        ("存档名", {"text": {}}),
        ("游戏状态", {"text": {}}),
        ("更新时间", {"date": {"format": "yyyy-mm-dd"}}),
    ]),
    ("麦当劳每日经营报表", [
        ("日期", {"text": {}}),
        ("营收", {"number": {}}),
        ("成本", {"number": {}}),
        ("毛利", {"number": {}}),
        ("订单数", {"number": {}}),
        ("堂食单", {"number": {}}),
        ("外送单", {"number": {}}),
        ("客单价", {"number": {}}),
        ("流失率", {"number": {}}),
        ("评分", {"number": {}}),
        ("明细", {"text": {}}),
    ]),
]

def run(args):
    p = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
    line = next((l for l in p.stdout.splitlines() if l.startswith("{")), "")
    try:
        return json.loads(line)
    except Exception:
        print("PARSE_FAIL", p.stdout[:600], p.stderr[:400]); sys.exit(1)

out = {}
for title, props in TABLES:
    schema = {"title": title, "space_id": SPACE,
              "properties": [{"name": n, "config": c} for n, c in props]}
    d = run([PY, os.path.join(LIB, "database", "create_database.py"), "--schema", json.dumps(schema, ensure_ascii=False)])
    if "error" in d:
        print("CREATE_ERROR", title, d); sys.exit(1)
    out[title] = d["database_id"]
    print("CREATED", title, d["database_id"])

with open(os.path.join(WS, "game_map.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print("DONE")
