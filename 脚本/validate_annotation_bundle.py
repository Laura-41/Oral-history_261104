#!/usr/bin/env python3
"""Validate referential integrity, sequence chains, and source coverage."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


TABLES = (
    "documents",
    "source_segments",
    "source_attachments",
    "event_nodes",
    "event_processes",
    "event_participants",
    "event_circumstances",
    "process_stages",
    "stage_next",
    "event_next",
    "entities",
    "entity_mentions",
    "entity_aliases",
    "entity_relations",
    "event_times",
    "time_expressions",
    "document_annotations",
    "coverage_audit",
)


def read_csv(folder: Path, name: str) -> list[dict[str, str]]:
    with (folder / f"{name}.csv").open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate(folder: Path) -> dict[str, object]:
    errors: list[str] = []
    rows = {name: read_csv(folder, name) for name in TABLES}

    document_ids = {row["doc_id"] for row in rows["documents"]}
    segment_ids = {row["segment_id"] for row in rows["source_segments"]}
    event_ids = {row["event_id"] for row in rows["event_nodes"]}
    stage_ids = {row["stage_id"] for row in rows["process_stages"]}
    entity_ids = {row["entity_id"] for row in rows["entities"]}
    mention_ids = {row["mention_id"] for row in rows["entity_mentions"]}
    time_expression_ids = {row["time_expression_id"] for row in rows["time_expressions"]}

    require(len(document_ids) == 1, "documents.csv 必须且只能有一个 doc_id", errors)
    require(len(segment_ids) == len(rows["source_segments"]), "segment_id 不唯一", errors)
    require(len(event_ids) == len(rows["event_nodes"]), "event_id 不唯一", errors)
    require(len(stage_ids) == len(rows["process_stages"]), "stage_id 不唯一", errors)
    require(len(entity_ids) == len(rows["entities"]), "entity_id 不唯一", errors)
    require(len(mention_ids) == len(rows["entity_mentions"]), "mention_id 不唯一", errors)
    require(len(time_expression_ids) == len(rows["time_expressions"]), "time_expression_id 不唯一", errors)

    for row in rows["source_segments"]:
        require(row["doc_id"] in document_ids, f"片段 {row['segment_id']} 引用未知文档", errors)
    for row in rows["event_nodes"]:
        require(row["doc_id"] in document_ids, f"事件 {row['event_id']} 引用未知文档", errors)
    for row in rows["event_processes"]:
        require(row["event_id"] in event_ids, f"过程 {row['process_id']} 引用未知事件", errors)
        require(not row["evidence_segment_id"] or row["evidence_segment_id"] in segment_ids,
                f"过程 {row['process_id']} 引用未知证据片段", errors)
    for table in ("event_participants", "event_circumstances"):
        for row in rows[table]:
            require(row["event_id"] in event_ids, f"{table} 引用未知事件 {row['event_id']}", errors)
            require(not row["evidence_segment_id"] or row["evidence_segment_id"] in segment_ids,
                    f"{table} 引用未知证据片段 {row['evidence_segment_id']}", errors)
            if row.get("entity_id"):
                require(row["entity_id"] in entity_ids, f"{table} 引用未知实体 {row['entity_id']}", errors)
    for row in rows["process_stages"]:
        require(row["event_id"] in event_ids, f"阶段 {row['stage_id']} 引用未知事件", errors)
    stage_to_event = {row["stage_id"]: row["event_id"] for row in rows["process_stages"]}
    for index, row in enumerate(rows["stage_next"], start=1):
        source_id = row["source_stage_id"]
        target_id = row["target_stage_id"]
        require(source_id in stage_ids and target_id in stage_ids,
                f"第 {index} 条阶段关系引用未知阶段", errors)
        if source_id in stage_to_event and target_id in stage_to_event:
            require(stage_to_event[source_id] == stage_to_event[target_id],
                    f"第 {index} 条阶段关系跨越了不同一级事件", errors)
    for row in rows["event_next"]:
        require(row["source_event_id"] in event_ids and row["target_event_id"] in event_ids,
                f"事件关系 {row['source_event_id']}→{row['target_event_id']} 引用未知事件", errors)

    segment_text = {row["segment_id"]: row["verbatim_text"] for row in rows["source_segments"]}
    for row in rows["entity_mentions"]:
        require(row["segment_id"] in segment_ids, f"实体提及 {row['mention_id']} 引用未知片段", errors)
        require(row["entity_id"] in entity_ids, f"实体提及 {row['mention_id']} 引用未知实体", errors)
        if row["segment_id"] in segment_text:
            start, end = int(row["start_offset"]), int(row["end_offset"])
            require(segment_text[row["segment_id"]][start:end] == row["mention_text"],
                    f"实体提及 {row['mention_id']} 的偏移与原文不一致", errors)
    for row in rows["entity_aliases"]:
        require(row["entity_id"] in entity_ids, f"实体别名 {row['alias_id']} 引用未知实体", errors)
        require(not row["evidence_segment_id"] or row["evidence_segment_id"] in segment_ids,
                f"实体别名 {row['alias_id']} 引用未知证据片段", errors)
    for row in rows["entity_relations"]:
        require(row["source_entity_id"] in entity_ids and row["target_entity_id"] in entity_ids,
                f"实体关系 {row['relation_id']} 引用未知实体", errors)
        require(not row["evidence_segment_id"] or row["evidence_segment_id"] in segment_ids,
                f"实体关系 {row['relation_id']} 引用未知证据片段", errors)
    for row in rows["event_times"]:
        require(row["event_id"] in event_ids, f"事件时间 {row['event_time_id']} 引用未知事件", errors)
        require(not row["evidence_segment_id"] or row["evidence_segment_id"] in segment_ids,
                f"事件时间 {row['event_time_id']} 引用未知证据片段", errors)
    require({row["event_id"] for row in rows["event_times"]} == event_ids,
            "并非每个事件都恰有规范时间记录", errors)
    for row in rows["time_expressions"]:
        require(row["segment_id"] in segment_ids,
                f"时间表达 {row['time_expression_id']} 引用未知原文片段", errors)
        if row["segment_id"] in segment_text:
            start, end = int(row["start_offset"]), int(row["end_offset"])
            require(segment_text[row["segment_id"]][start:end] == row["raw_text"],
                    f"时间表达 {row['time_expression_id']} 的偏移与原文不一致", errors)

    for row in rows["document_annotations"]:
        target_ok = (
            row["target_type"] == "DOCUMENT" and row["target_id"] in document_ids
            or row["target_type"] == "EVENT" and row["target_id"] in event_ids
            or row["target_type"] == "STAGE" and row["target_id"] in stage_ids
            or row["target_type"] == "ENTITY" and row["target_id"] in entity_ids
            or row["target_type"] == "SOURCE_SEGMENT" and row["target_id"] in segment_ids
        )
        require(target_ok, f"文档注释 {row['annotation_id']} 的目标不存在", errors)
        require(row["source_segment_id"] in segment_ids,
                f"文档注释 {row['annotation_id']} 引用未知原文片段", errors)

    attached_segments: set[str] = set()
    for row in rows["source_attachments"]:
        require(row["segment_id"] in segment_ids, f"挂接 {row['attachment_id']} 引用未知片段", errors)
        target_ok = (
            row["target_type"] == "DOCUMENT" and row["target_id"] in document_ids
            or row["target_type"] == "EVENT" and row["target_id"] in event_ids
            or row["target_type"] == "STAGE" and row["target_id"] in stage_ids
        )
        require(target_ok, f"挂接 {row['attachment_id']} 的目标不存在", errors)
        if row["segment_id"] in segment_ids:
            attached_segments.add(row["segment_id"])

    missing_segments = sorted(segment_ids - attached_segments)
    require(not missing_segments, f"有 {len(missing_segments)} 个原文片段未挂接", errors)

    sorted_events = sorted(rows["event_nodes"], key=lambda row: int(row["historical_order"]))
    expected_next = list(zip(
        [row["event_id"] for row in sorted_events[:-1]],
        [row["event_id"] for row in sorted_events[1:]],
    ))
    actual_next = [(row["source_event_id"], row["target_event_id"]) for row in rows["event_next"]]
    require(actual_next == expected_next, "event_next 不是完整的历史顺承链", errors)

    audit = rows["coverage_audit"]
    require(len(audit) == 1, "coverage_audit.csv 必须有一条记录", errors)
    if audit:
        require(audit[0]["coverage_rate"] == "1.0000", "原文覆盖率不是 1.0000", errors)
        require(int(audit[0]["total_segments"]) == len(segment_ids), "覆盖审计片段总数不一致", errors)
        require(int(audit[0]["attached_segments"]) == len(attached_segments), "覆盖审计挂接数不一致", errors)

    with (folder / "annotation_bundle.json").open(encoding="utf-8") as handle:
        bundle = json.load(handle)
    bundle_keys = {
        "documents": "document",
        "source_segments": "source_segments",
        "source_attachments": "source_attachments",
        "event_nodes": "events",
        "event_processes": "processes",
        "event_participants": "participants",
        "event_circumstances": "circumstances",
        "process_stages": "stages",
        "stage_next": "stage_next",
        "event_next": "event_next",
        "entities": "entities",
        "entity_mentions": "entity_mentions",
        "entity_aliases": "entity_aliases",
        "entity_relations": "entity_relations",
        "event_times": "event_times",
        "time_expressions": "time_expressions",
        "document_annotations": "document_annotations",
        "coverage_audit": "coverage_audit",
    }
    for table_name, bundle_key in bundle_keys.items():
        value = bundle.get(bundle_key)
        json_count = 1 if isinstance(value, dict) else len(value or [])
        require(json_count == len(rows[table_name]), f"JSON 与 {table_name}.csv 行数不一致", errors)

    return {
        "folder": str(folder),
        "documents": len(document_ids),
        "segments": len(segment_ids),
        "attached_segments": len(attached_segments),
        "events": len(event_ids),
        "stages": len(stage_ids),
        "entities": len(entity_ids),
        "entity_mentions": len(mention_ids),
        "time_expressions": len(time_expression_ids),
        "event_next": len(actual_next),
        "coverage_rate": audit[0]["coverage_rate"] if audit else None,
        "errors": errors,
        "valid": not errors,
    }


if __name__ == "__main__":
    folders = [Path(value) for value in sys.argv[1:]]
    if not folders:
        raise SystemExit("请提供一个或多个试标目录")
    results = [validate(folder) for folder in folders]
    print(json.dumps(results, ensure_ascii=False, indent=2))
    raise SystemExit(0 if all(result["valid"] for result in results) else 1)
