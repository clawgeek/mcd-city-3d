#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""在用户个人空间重建源工作台的 4 张数据表，输出 新表ID 映射。"""
import json, subprocess, sys, os

PY = r"C:\Users\10099\.workbuddy\binaries\python\versions\3.13.12\python.exe"
LIB = r"C:\Users\10099\AppData\Local\Programs\WorkBuddy\resources\app.asar.unpacked\resources\plugins\workbuddy-builtin\skills\library"
SPACE = "fwPdZMvtey16eALurOJ7Oj"

TABLES = [
    ("房间定义", "uyXmKHCBZAfyIybyZlwHSh", [
        ("房间id", {"text": {}}), ("标题", {"text": {}}), ("眉题", {"text": {}}),
        ("指标", {"text": {}}), ("摘要", {"text": {}}), ("强调色", {"text": {}}),
        ("段落", {"text": {}}), ("要点", {"text": {}}), ("子弹点", {"text": {}}),
    ]),
    ("角色内容", "YOJ1DUQXLzcV3lpQfoGkTM", [
        ("角色", {"text": {}}), ("房间", {"text": {}}), ("心情", {"text": {}}),
        ("指标", {"text": {}}), ("摘要", {"text": {}}), ("段落", {"text": {}}),
        ("要点", {"text": {}}), ("子弹点", {"text": {}}),
    ]),
    ("创作资产", "ijjLrDVnqb9KMmEMwem76P", [
        ("分类", {"select": {"options": [
            {"text": "封面模板", "style": 26}, {"text": "配乐", "style": 24},
            {"text": "字体", "style": 16}, {"text": "素材", "style": 19}]}}),
        ("名称", {"text": {}}), ("描述", {"text": {}}), ("链接", {"url": {}}),
        ("标签", {"text": {}}), ("更新时间", {"date": {"format": "yyyy-mm-dd"}}),
        ("职业预设", {"select": {"options": [
            {"text": "creator", "style": 6}, {"text": "maker", "style": 8},
            {"text": "designer", "style": 19}, {"text": "student", "style": 24},
            {"text": "life", "style": 0}]}}),
    ]),
    ("用户存档", "GABE4NHgKXQ02a8akQlRj7", [
        ("用户标识", {"text": {}}), ("角色", {"text": {}}), ("角色文本", {"text": {}}),
        ("昵称", {"text": {}}), ("房间状态", {"text": {}}), ("内容进度", {"text": {}}),
        ("更新时间", {"date": {"format": "yyyy-mm-dd"}}),
        ("职业预设", {"select": {"options": [
            {"text": "creator", "style": 13}, {"text": "maker", "style": 23},
            {"text": "designer", "style": 24}, {"text": "student", "style": 23},
            {"text": "life", "style": 15}]}}),
    ]),
]

mapping = {"uyXmKHCBZAfyIybyZlwHSh": "Oh7OgKolSuXfrmwFQluA2b"}  # 房间定义已建
for title, src_id, props in TABLES:
    if src_id in mapping:
        print("SKIP", title, mapping[src_id])
        continue
    schema = {
        "title": title,
        "space_id": SPACE,
        "properties": [{"name": n, "config": c} for n, c in props],
    }
    r = subprocess.run([PY, os.path.join(LIB, "database", "create_database.py"), "--schema", json.dumps(schema, ensure_ascii=False)],
                       capture_output=True, text=True, encoding="utf-8")
    out = r.stdout.strip()
    line = next((l for l in out.splitlines() if l.startswith("{")), "")
    try:
        data = json.loads(line)
    except Exception:
        print("PARSE_FAIL", title, out, r.stderr); sys.exit(1)
    if "error" in data:
        print("ERROR", title, data); sys.exit(1)
    mapping[src_id] = data["database_id"]
    print("CREATED", title, data["database_id"], "props:", data.get("property_count"))

with open("cfg_map.json", "w", encoding="utf-8") as f:
    json.dump(mapping, f, ensure_ascii=False, indent=2)
print("DONE")
