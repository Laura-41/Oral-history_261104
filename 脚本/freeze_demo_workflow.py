#!/usr/bin/env python3
"""Freeze the six reviewed documents as a workflow demo, not a gold test set."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CURRENT = ROOT / "现行标注"
FOLDERS = [
    CURRENT / "01_陈海峰一访",
    CURRENT / "02_陈锐霆090422",
    CURRENT / "03_陈海峰二访01",
    CURRENT / "04_陈海峰三访01",
    CURRENT / "05_陈锐霆090422_02",
    CURRENT / "06_杨永松100506_01",
]

# These are the reviewed structural layers.  Fine-grained entity mentions and
# full-text time expressions remain demo annotations rather than gold labels.
CONFIRMED_TABLES = {
    "documents.csv",
    "event_nodes.csv",
    "process_stages.csv",
    "stage_next.csv",
    "event_next.csv",
    "event_times.csv",
    "source_attachments.csv",
}

STATUS_NOTE = (
    "本文件属于六份WORKFLOW_DEMO。研究者已确认事件、阶段、文档内顺序、事件时间和原文挂接结构；"
    "它用于固定工作流和展示，不作为正式内部测试金标准。细粒度实体提及和全文时间表达继续保留其原有核验状态。"
)


def update_csv(path: Path) -> None:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    for row in rows:
        if path.name == "documents.csv":
            row["data_role"] = "WORKFLOW_DEMO"
        if "review_status" in row:
            row["review_status"] = "CONFIRMED"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def update_bundle(folder: Path) -> None:
    path = folder / "annotation_bundle.json"
    bundle = json.loads(path.read_text(encoding="utf-8"))
    bundle["document"]["data_role"] = "WORKFLOW_DEMO"
    bundle["document"]["review_status"] = "CONFIRMED"
    bundle["document"]["total_characters"] = int(bundle["document"]["total_characters"])
    for key in ("events", "stages", "stage_next", "event_next", "event_times", "source_attachments"):
        for row in bundle[key]:
            row["review_status"] = "CONFIRMED"
    for row in bundle["events"]:
        row["narrative_order"] = int(row["narrative_order"])
        row["historical_order"] = int(row["historical_order"])
    for row in bundle["stages"]:
        row["stage_order"] = int(row["stage_order"])
    for row in bundle["source_attachments"]:
        for field in ("quote_start_offset", "quote_end_offset"):
            row[field] = int(row[field]) if row[field] not in ("", None) else None
    bundle["status_note"] = STATUS_NOTE
    path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_review_markdown(folder: Path) -> None:
    path = folder / "事件试标复核稿.md"
    text = path.read_text(encoding="utf-8")
    replacement = (
        "> 状态：`WORKFLOW_DEMO / CONFIRMED`。事件、阶段、文档内顺序、事件时间和原文挂接结构已经研究者确认；"
        "本稿用于固定工作流与Neo4j展示，不作为正式测试金标准。"
    )
    text, count = re.subn(r"^> .*?$", replacement, text, count=1, flags=re.MULTILINE)
    if count != 1:
        raise ValueError(f"未找到复核稿状态说明：{path}")
    path.write_text(text, encoding="utf-8")


def main() -> None:
    for folder in FOLDERS:
        for filename in CONFIRMED_TABLES:
            update_csv(folder / filename)
        update_bundle(folder)
        update_review_markdown(folder)
        print(f"frozen: {folder.name}")


if __name__ == "__main__":
    main()

