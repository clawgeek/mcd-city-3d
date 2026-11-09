#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把源表 CSV 数据灌入用户个人空间的新表。"""
import json, subprocess, os, csv, io, sys

PY = r"C:\Users\10099\.workbuddy\binaries\python\versions\3.13.12\python.exe"
LIB = r"C:\Users\10099\AppData\Local\Programs\WorkBuddy\resources\app.asar.unpacked\resources\plugins\workbuddy-builtin\skills\library"
WS = r"C:\Users\10099\WorkBuddy\2026-10-24-16-20-51"

mapping = json.load(open(os.path.join(WS, "cfg_map.json"), encoding="utf-8"))

# 源表字段类型 -> 新表写入方式
def make_value(field, raw, schema_fields):
    if raw is None:
        raw = ""
    raw = raw.strip()
    ftype = schema_fields.get(field, "text")
    if ftype == "select":
        return {"select": raw} if raw else {}
    if ftype == "url":
        return {"url": {"text": raw, "link": raw}} if raw else {}
    if ftype == "date":
        return {"date": raw} if raw else {}
    return {"text": raw}

def load_csv(path):
    raw = json.load(open(path, encoding="utf-8"))["content"]
    return list(csv.DictReader(io.StringIO(raw)))

TABLES = [
    ("房间定义", "uyXmKHCBZAfyIybyZlwHSh",
     {"房间id":"text","标题":"text","眉题":"text","指标":"text","摘要":"text","强调色":"text","段落":"text","要点":"text","子弹点":"text"}),
    ("角色内容", "YOJ1DUQXLzcV3lpQfoGkTM",
     {"角色":"text","房间":"text","心情":"text","指标":"text","摘要":"text","段落":"text","要点":"text","子弹点":"text"}),
    ("创作资产", "ijjLrDVnqb9KMmEMwem76P",
     {"分类":"select","名称":"text","描述":"text","链接":"url","标签":"text","更新时间":"date","职业预设":"select"}),
    ("用户存档", "GABE4NHgKXQ02a8akQlRj7",
     {"用户标识":"text","角色":"text","角色文本":"text","昵称":"text","房间状态":"text","内容进度":"text","更新时间":"date","职业预设":"select"}),
]

total = 0
for title, src_id, fields in TABLES:
    rows = load_csv(os.path.join(WS, f"src_{src_id}.csv"))
    db_id = mapping[src_id]
    recs = []
    for r in rows:
        props = {}
        for f in fields:
            v = make_value(f, r.get(f), fields)
            if v:
                props[f] = v
        if props:
            recs.append(props)
    ok = 0
    for i in range(0, len(recs), 100):
        chunk = recs[i:i+100]
        p = subprocess.run([PY, os.path.join(LIB, "database", "batch_add_database_records.py"),
                            "--database-id", db_id, "--records", json.dumps(chunk, ensure_ascii=False)],
                           capture_output=True, text=True, encoding="utf-8")
        line = next((l for l in p.stdout.splitlines() if l.startswith("{")), "")
        try:
            d = json.loads(line)
        except Exception:
            print("FAIL", title, p.stdout[:500]); sys.exit(1)
        if "error" in d:
            print("ERROR", title, d); sys.exit(1)
        ok += len(chunk)
    print(f"IMPORTED {title} -> {db_id} : {ok}/{len(rows)}")
    total += ok
print("TOTAL", total)
