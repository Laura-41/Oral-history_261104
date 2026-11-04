#!/usr/bin/env python3
"""Combine the six development-corpus bundles into Neo4j import CSV files."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CURRENT = ROOT / "现行标注"
SOURCES = [
    CURRENT / "01_陈海峰一访",
    CURRENT / "02_陈锐霆090422",
    CURRENT / "03_陈海峰二访01",
    CURRENT / "04_陈海峰三访01",
    CURRENT / "05_陈锐霆090422_02",
    CURRENT / "06_杨永松100506_01",
]
OUTPUT = CURRENT / "neo4j_demo" / "import"
REPORT = CURRENT / "neo4j_demo" / "reports" / "prepare_summary.json"

TABLES = [
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
]

UNIQUE_KEYS = {
    "documents": ("doc_id",),
    "source_segments": ("segment_id",),
    "source_attachments": ("attachment_id",),
    "event_nodes": ("event_id",),
    "event_processes": ("process_id",),
    "event_participants": ("event_id", "entity_id", "role", "evidence_segment_id"),
    "event_circumstances": ("circumstance_id",),
    "process_stages": ("stage_id",),
    "stage_next": ("source_stage_id", "target_stage_id"),
    "event_next": ("source_event_id", "target_event_id"),
    "entities": ("entity_id",),
    "entity_mentions": ("mention_id",),
    "entity_aliases": ("alias_id",),
    "entity_relations": ("relation_id",),
    "event_times": ("event_time_id",),
    "time_expressions": ("time_expression_id",),
    "document_annotations": ("annotation_id",),
    "coverage_audit": ("doc_id",),
}


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def row_key(row: dict[str, str], columns: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(row.get(column, "") for column in columns)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    summary: dict[str, int] = {}

    for table in TABLES:
        fieldnames: list[str] | None = None
        merged: dict[tuple[str, ...], dict[str, str]] = {}
        for source in SOURCES:
            current_fields, rows = read_rows(source / f"{table}.csv")
            if fieldnames is None:
                fieldnames = current_fields
            elif fieldnames != current_fields:
                raise ValueError(f"Header mismatch in {table}: {source}")
            for row in rows:
                key = row_key(row, UNIQUE_KEYS[table])
                previous = merged.get(key)
                if previous is not None and previous != row:
                    if table == "entities":
                        stable = ("canonical_name", "entity_type", "entity_subtype")
                        if any(previous.get(col) != row.get(col) for col in stable):
                            raise ValueError(f"Conflicting shared entity {key}: {previous} != {row}")
                        # Keep the more cautious review state if either copy needs review.
                        if row.get("review_status") == "NEEDS_REVIEW":
                            previous["review_status"] = "NEEDS_REVIEW"
                        continue
                    raise ValueError(f"Conflicting duplicate in {table} for {key}")
                merged[key] = row

        output = OUTPUT / f"{table}.csv"
        with output.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames or [])
            writer.writeheader()
            writer.writerows(merged.values())
        summary[table] = len(merged)

    REPORT.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

