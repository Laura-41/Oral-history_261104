from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path

from lxml import etree

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


def qn(tag: str) -> str:
    return f"{{{W}}}{tag}"


def paragraph_text(p: etree._Element) -> str:
    pieces: list[str] = []
    for node in p.iter():
        if node.tag == qn("t"):
            pieces.append(node.text or "")
        elif node.tag == qn("tab"):
            pieces.append("\t")
        elif node.tag in {qn("br"), qn("cr")}:
            pieces.append("\n")
        elif node.tag == qn("noBreakHyphen"):
            pieces.append("-")
        elif node.tag == qn("softHyphen"):
            pieces.append("\u00ad")
    return "".join(pieces)


def paragraph_style(p: etree._Element) -> str:
    style = p.find("./w:pPr/w:pStyle", NS)
    return style.get(qn("val"), "") if style is not None else ""


def extract_part(xml_bytes: bytes, part_name: str) -> list[dict]:
    root = etree.fromstring(xml_bytes)
    if part_name == "document":
        container = root.find(".//w:body", NS)
        children = list(container) if container is not None else []
    elif part_name in {"footnotes", "endnotes", "comments"}:
        blocks: list[dict] = []
        order = 0
        item_tag = {"footnotes": "footnote", "endnotes": "endnote", "comments": "comment"}[part_name]
        for item in root.findall(f"./w:{item_tag}", NS):
            item_id = item.get(qn("id"), "")
            paras = [paragraph_text(p) for p in item.findall(".//w:p", NS)]
            text = "\n".join(p for p in paras if p)
            if not text:
                continue
            order += 1
            blocks.append({
                "order": order,
                "block_type": item_tag,
                "style": "",
                "text": text,
                "part": part_name,
                "item_id": item_id,
            })
        return blocks
    else:
        children = list(root)

    blocks: list[dict] = []
    order = 0
    for child in children:
        if child.tag == qn("p"):
            text = paragraph_text(child)
            if text or part_name != "document":
                order += 1
                blocks.append({
                    "order": order,
                    "block_type": "paragraph",
                    "style": paragraph_style(child),
                    "text": text,
                    "part": part_name,
                })
        elif child.tag == qn("tbl"):
            rows: list[str] = []
            for tr in child.findall("./w:tr", NS):
                cells: list[str] = []
                for tc in tr.findall("./w:tc", NS):
                    paras = [paragraph_text(p) for p in tc.findall(".//w:p", NS)]
                    cells.append("\n".join(paras))
                rows.append("\t".join(cells))
            text = "\n".join(rows)
            order += 1
            blocks.append({
                "order": order,
                "block_type": "table",
                "style": "",
                "text": text,
                "part": part_name,
            })
    return blocks


def count_tags(xml_bytes: bytes) -> dict:
    root = etree.fromstring(xml_bytes)
    return {
        "paragraphs": len(root.findall(".//w:p", NS)),
        "tables": len(root.findall(".//w:tbl", NS)),
        "text_nodes": len(root.findall(".//w:t", NS)),
        "insertions": len(root.findall(".//w:ins", NS)),
        "deletions": len(root.findall(".//w:del", NS)),
        "comment_refs": len(root.findall(".//w:commentReference", NS)),
        "footnote_refs": len(root.findall(".//w:footnoteReference", NS)),
        "endnote_refs": len(root.findall(".//w:endnoteReference", NS)),
        "textboxes": len(root.findall(".//w:txbxContent", NS)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_docx")
    parser.add_argument("output_dir")
    parser.add_argument("--doc-id", required=True)
    args = parser.parse_args()

    input_path = Path(args.input_docx).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(input_path) as zf:
        names = set(zf.namelist())
        document_xml = zf.read("word/document.xml")
        body_blocks = extract_part(document_xml, "document")
        parts: dict[str, list[dict]] = {"document": body_blocks}
        for filename, part_name in [
            ("word/footnotes.xml", "footnotes"),
            ("word/endnotes.xml", "endnotes"),
            ("word/comments.xml", "comments"),
        ]:
            if filename in names:
                parts[part_name] = extract_part(zf.read(filename), part_name)

        headers = sorted(n for n in names if re.fullmatch(r"word/header\d+\.xml", n))
        footers = sorted(n for n in names if re.fullmatch(r"word/footer\d+\.xml", n))
        for filename in headers + footers:
            part_name = Path(filename).stem
            parts[part_name] = extract_part(zf.read(filename), part_name)

        stats = count_tags(document_xml)
        stats["has_comments_part"] = "word/comments.xml" in names
        stats["has_footnotes_part"] = "word/footnotes.xml" in names
        stats["has_endnotes_part"] = "word/endnotes.xml" in names

    blocks: list[dict] = []
    char_offset = 0
    for idx, block in enumerate(body_blocks, start=1):
        text = block["text"]
        item = {
            "block_id": f"{args.doc_id}-B{idx:04d}",
            "doc_id": args.doc_id,
            **block,
            "start_offset": char_offset,
            "end_offset": char_offset + len(text),
        }
        blocks.append(item)
        char_offset += len(text) + 1

    raw_text = "\n".join(b["text"] for b in body_blocks)
    payload = {
        "doc_id": args.doc_id,
        "source_file": str(input_path),
        "body_character_count": len(raw_text),
        "body_block_count": len(blocks),
        "xml_stats": stats,
        "blocks": blocks,
        "additional_parts": {k: v for k, v in parts.items() if k != "document"},
    }

    (output_dir / "extracted_blocks.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output_dir / "extracted_body.txt").write_text(raw_text, encoding="utf-8")
    with (output_dir / "extracted_blocks_readable.txt").open("w", encoding="utf-8") as f:
        for b in blocks:
            f.write(f"[{b['block_id']}][{b['block_type']}][{b['style']}]\n{b['text']}\n\n")
    (output_dir / "extraction_summary.json").write_text(json.dumps({
        "doc_id": args.doc_id,
        "source_file": str(input_path),
        "body_character_count": len(raw_text),
        "body_block_count": len(blocks),
        "xml_stats": stats,
        "additional_parts": {k: len(v) for k, v in parts.items() if k != "document"},
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "doc_id": args.doc_id,
        "body_character_count": len(raw_text),
        "body_block_count": len(blocks),
        "xml_stats": stats,
        "output_dir": str(output_dir),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
