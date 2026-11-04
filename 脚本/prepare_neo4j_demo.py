#!/usr/bin/env python3
"""Combine the six development-corpus bundles into Neo4j import CSV files."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from person_biography_config import SUBJECTS


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

    with (OUTPUT / "event_nodes.csv").open(encoding="utf-8-sig", newline="") as handle:
        event_nodes = {row["event_id"]: row for row in csv.DictReader(handle)}
    with (OUTPUT / "event_times.csv").open(encoding="utf-8-sig", newline="") as handle:
        event_times = {row["event_id"]: row for row in csv.DictReader(handle)}

    person_subjects: list[dict[str, str]] = []
    document_persons: list[dict[str, str]] = []
    life_episodes: list[dict[str, str]] = []
    life_episode_sources: list[dict[str, str]] = []
    life_episode_next: list[dict[str, str]] = []
    narrated_contexts: list[dict[str, str]] = []

    for person_id, subject in SUBJECTS.items():
        person_subjects.append({
            "person_entity_id": person_id,
            "person_name": subject["person_name"],
            "biography_status": "WORKFLOW_DEMO",
            "review_status": "CONFIRMED",
        })
        for doc_id in subject["documents"]:
            document_persons.append({
                "doc_id": doc_id,
                "person_entity_id": person_id,
                "relation_type": "INTERVIEW_OF",
                "review_status": "CONFIRMED",
            })

        episode_rows: list[dict[str, str]] = []
        for life_order, (episode_id, event_id, episode_scope) in enumerate(subject["episodes"], start=1):
            if event_id not in event_nodes or event_id not in event_times:
                raise ValueError(f"Biography config references unknown event: {event_id}")
            event = event_nodes[event_id]
            event_time = event_times[event_id]
            episode = {
                "episode_id": episode_id,
                "person_entity_id": person_id,
                "episode_name": event["event_name"],
                "life_order": str(life_order),
                "normalized_start": event_time["normalized_start"],
                "normalized_end": event_time["normalized_end"],
                "precision": event_time["precision"],
                "certainty": event_time["certainty"],
                "episode_scope": episode_scope,
                "confidence": event_time["confidence"],
                "review_status": "CONFIRMED",
            }
            episode_rows.append(episode)
            life_episodes.append(episode)
            life_episode_sources.append({
                "episode_id": episode_id,
                "event_id": event_id,
                "source_role": "PRIMARY_EVIDENCE",
                "review_status": "CONFIRMED",
            })

        for current, following in zip(episode_rows, episode_rows[1:]):
            current_end = current["normalized_end"]
            next_start = following["normalized_start"]
            overlap = "YES" if current_end and next_start and current_end >= next_start else "NO"
            life_episode_next.append({
                "source_episode_id": current["episode_id"],
                "target_episode_id": following["episode_id"],
                "person_entity_id": person_id,
                "basis": "HISTORICAL_TIME_MANUAL_REVIEW",
                "overlap_possible": overlap,
                "confidence": "HIGH",
                "review_status": "CONFIRMED",
            })

        for context_order, event_id in enumerate(subject["narrated_context"], start=1):
            if event_id not in event_nodes:
                raise ValueError(f"Biography config references unknown context event: {event_id}")
            narrated_contexts.append({
                "person_entity_id": person_id,
                "event_id": event_id,
                "context_order": str(context_order),
                "relation_type": "NARRATED_CONTEXT",
                "review_status": "CONFIRMED",
            })

    generated = {
        "person_subjects": person_subjects,
        "document_persons": document_persons,
        "life_episodes": life_episodes,
        "life_episode_sources": life_episode_sources,
        "life_episode_next": life_episode_next,
        "narrated_contexts": narrated_contexts,
    }
    generated_fields = {
        "person_subjects": ["person_entity_id", "person_name", "biography_status", "review_status"],
        "document_persons": ["doc_id", "person_entity_id", "relation_type", "review_status"],
        "life_episodes": ["episode_id", "person_entity_id", "episode_name", "life_order", "normalized_start", "normalized_end", "precision", "certainty", "episode_scope", "confidence", "review_status"],
        "life_episode_sources": ["episode_id", "event_id", "source_role", "review_status"],
        "life_episode_next": ["source_episode_id", "target_episode_id", "person_entity_id", "basis", "overlap_possible", "confidence", "review_status"],
        "narrated_contexts": ["person_entity_id", "event_id", "context_order", "relation_type", "review_status"],
    }
    for table, rows in generated.items():
        with (OUTPUT / f"{table}.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=generated_fields[table])
            writer.writeheader()
            writer.writerows(rows)
        summary[table] = len(rows)

    REPORT.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

