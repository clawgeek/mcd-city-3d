#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""复刻源页面的 6 张「一屋一表」业务表到用户个人空间。"""
import json, subprocess, os, csv, io, sys

PY = r"C:\Users\10099\.workbuddy\binaries\python\versions\3.13.12\python.exe"
LIB = r"C:\Users\10099\AppData\Local\Programs\WorkBuddy\resources\app.asar.unpacked\resources\plugins\workbuddy-builtin\skills\library"
WS = r"C:\Users\10099\WorkBuddy\2026-10-24-16-20-51"
SPACE = "fwPdZMvtey16eALurOJ7Oj"

PRESET_OPTS = [
    {"text": "creator", "style": 9}, {"text": "maker", "style": 26},
    {"text": "designer", "style": 1}, {"text": "student", "style": 17},
    {"text": "life", "style": 6},
]

# (源表id, 表名, [(字段, 类型, options?)], 是否含职业预设)
TABLES = [
    ("NhqVuqPR9wynDGqURc8MeR", "今日计划", [
        ("事项", "text"), ("计划时间", "date"), ("优先级", "select",
         [{"text": "高", "style": 22}, {"text": "中", "style": 25}, {"text": "低", "style": 24}]),
        ("状态", "select", [{"text": "未开始", "style": 12}, {"text": "进行中", "style": 9}, {"text": "已完成", "style": 25}]),
        ("备注", "text"), ("职业预设", "select", PRESET_OPTS)]),
    ("A3XPdUQH6qYxdpc9R72YMQ", "灵感池", [
        ("灵感", "text"), ("来源", "text"), ("分类", "select",
         [{"text": "选题", "style": 15}, {"text": "观察", "style": 15}, {"text": "问题", "style": 13}, {"text": "收藏", "style": 0}]),
        ("热度", "number"), ("状态", "select",
         [{"text": "待整理", "style": 6}, {"text": "已采用", "style": 24}, {"text": "暂存", "style": 23}]),
        ("记录日期", "date"), ("职业预设", "select", PRESET_OPTS)]),
    ("BNp5tjWzvW1lUplOmtw2eN", "内容项目", [
        ("内容标题", "text"), ("发布平台", "select",
         [{"text": "小红书", "style": 23}, {"text": "视频号", "style": 18}, {"text": "公众号", "style": 7}, {"text": "其他", "style": 7}]),
        ("阶段", "select", [{"text": "选题", "style": 13}, {"text": "脚本", "style": 17}, {"text": "制作", "style": 24},
                            {"text": "待发布", "style": 11}, {"text": "已发布", "style": 1}]),
        ("截止日期", "date"), ("发布链接", "url"), ("备注", "text"), ("职业预设", "select", PRESET_OPTS)]),
    ("2j8UqsJq67rmglW9cyI1as", "训练记录", [
        ("训练项目", "text"), ("类型", "select",
         [{"text": "力量", "style": 15}, {"text": "有氧", "style": 10}, {"text": "拉伸", "style": 12}, {"text": "恢复", "style": 9}]),
        ("计划日期", "date"), ("时长（分钟）", "number"), ("完成", "checkbox"),
        ("备注", "text"), ("职业预设", "select", PRESET_OPTS)]),
    ("9c9BoPd4Xkb4C1j455aX0c", "复盘实验", [
        ("复盘主题", "text"), ("周期", "select",
         [{"text": "日", "style": 1}, {"text": "周", "style": 7}, {"text": "月", "style": 12}, {"text": "项目", "style": 26}]),
        ("关键指标", "text"), ("结论", "text"), ("下次实验", "text"),
        ("已行动", "checkbox"), ("职业预设", "select", PRESET_OPTS)]),
    ("u2ARSjTzMLfCgYlwa770Kh", "旅行计划", [
        ("目的地", "text"), ("状态", "select",
         [{"text": "想去", "style": 2}, {"text": "计划中", "style": 23}, {"text": "已出发", "style": 15}, {"text": "已到访", "style": 23}]),
        ("出发日期", "date"), ("预算（元）", "number"), ("行程清单", "text"),
        ("职业预设", "select", PRESET_OPTS)]),
]

def run(args):
    p = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
    line = next((l for l in p.stdout.splitlines() if l.startswith("{")), "")
    try:
        return json.loads(line)
    except Exception:
        print("PARSE_FAIL", p.stdout[:600], p.stderr[:400]); sys.exit(1)

mapping = json.load(open(os.path.join(WS, "cfg_map.json"), encoding="utf-8"))

for src_id, title, fields in TABLES:
    # 1. 建表
    props = []
    for f in fields:
        name, ftype = f[0], f[1]
        if ftype == "select":
            cfg = {"select": {"options": f[2]}}
        elif ftype == "date":
            cfg = {"date": {"format": "yyyy-mm-dd"}}
        elif ftype == "number":
            cfg = {"number": {}}
        elif ftype == "checkbox":
            cfg = {"checkbox": {}}
        elif ftype == "url":
            cfg = {"url": {}}
        else:
            cfg = {"text": {}}
        props.append({"name": name, "config": cfg})
    schema = {"title": title, "space_id": SPACE, "properties": props}
    d = run([PY, os.path.join(LIB, "database", "create_database.py"), "--schema", json.dumps(schema, ensure_ascii=False)])
    if "error" in d:
        print("CREATE_ERROR", title, d); sys.exit(1)
    db_id = d["database_id"]
    mapping[src_id] = db_id
    print("CREATED", title, db_id)

    # 2. 导数据
    src_csv = os.path.join(WS, f"src_{src_id}.csv")
    rows = []
    if os.path.exists(src_csv):
        raw = json.load(open(src_csv, encoding="utf-8"))["content"]
        rows = list(csv.DictReader(io.StringIO(raw)))
    if not rows:
        print("  (源表无数据或不可读，跳过)")
        continue
    ftypes = {f[0]: f[1] for f in fields}
    recs = []
    for r in rows:
        pr = {}
        for fname, ftype in ftypes.items():
            v = (r.get(fname) or "").strip()
            if not v:
                continue
            if ftype == "select":
                pr[fname] = {"select": v}
            elif ftype == "url":
                pr[fname] = {"url": {"text": v, "link": v}}
            elif ftype == "date":
                pr[fname] = {"date": v}
            elif ftype == "number":
                try:
                    pr[fname] = {"number": float(v) if "." in v else int(v)}
                except ValueError:
                    continue
            elif ftype == "checkbox":
                pr[fname] = {"checkbox": v.lower() in ("true", "1", "是", "yes")}
            else:
                pr[fname] = {"text": v}
        if pr:
            recs.append(pr)
    ok = 0
    for i in range(0, len(recs), 100):
        chunk = recs[i:i+100]
        rr = run([PY, os.path.join(LIB, "database", "batch_add_database_records.py"),
                  "--database-id", db_id, "--records", json.dumps(chunk, ensure_ascii=False)])
        if "error" in rr:
            print("  IMPORT_ERROR", title, rr); sys.exit(1)
        ok += len(chunk)
    print("  IMPORTED", title, ok, "/", len(rows))

with open(os.path.join(WS, "cfg_map.json"), "w", encoding="utf-8") as f:
    json.dump(mapping, f, ensure_ascii=False, indent=2)
print("DONE", len(mapping))
