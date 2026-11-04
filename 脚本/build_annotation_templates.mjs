import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const workspace = "/Users/yuqi/Desktop/硕士毕业论文/2609";
const corpusRoot = path.join(workspace, "0920_01/语料");
const outputDir = path.join(workspace, "0920_01/现行标注/00_模板");
const previewDir = path.join(outputDir, "预览");

const tables = {
  documents: ["doc_id", "title", "interviewee", "interview_date", "visit_no", "version", "source_file", "total_characters", "data_role", "include_in_study", "review_status"],
  source_segments: ["segment_id", "doc_id", "segment_order", "source_part", "source_ref_id", "source_block_id", "speaker_id", "speaker_type", "start_timecode", "end_timecode", "start_offset", "end_offset", "segment_type", "verbatim_text", "normalized_text", "transcription_status", "review_status"],
  source_attachments: ["attachment_id", "segment_id", "target_type", "target_id", "function", "quote_start_offset", "quote_end_offset", "confidence", "review_status"],
  event_nodes: ["event_id", "doc_id", "event_name", "narrative_order", "historical_order", "result_state", "factuality", "confidence", "boundary_note", "boundary_confidence", "review_status"],
  event_processes: ["process_id", "event_id", "event_type_id", "process_text", "process_normalized", "evidence_segment_id", "confidence"],
  event_participants: ["event_id", "entity_id", "entity_name", "entity_type", "role", "participation_status", "evidence_segment_id", "confidence"],
  event_circumstances: ["circumstance_id", "event_id", "kind", "value_text", "normalized_value", "entity_id", "evidence_segment_id", "confidence"],
  process_stages: ["stage_id", "event_id", "stage_order", "stage_summary", "process_text", "confidence", "review_status"],
  stage_next: ["source_stage_id", "target_stage_id", "logic", "evidence_segment_id", "confidence", "review_status"],
  event_next: ["source_event_id", "target_event_id", "chain_id", "basis", "confidence", "review_status"],
  entities: ["entity_id", "canonical_name", "entity_type", "entity_subtype", "description", "authority_status", "confidence", "review_status"],
  entity_mentions: ["mention_id", "segment_id", "entity_id", "mention_text", "start_offset", "end_offset", "mention_function", "source_status", "confidence", "review_status"],
  entity_aliases: ["alias_id", "entity_id", "alias_text", "alias_type", "evidence_segment_id", "confidence", "review_status"],
  entity_relations: ["relation_id", "source_entity_id", "relation_type", "target_entity_id", "role_label", "start_date", "end_date", "evidence_segment_id", "source_status", "confidence", "review_status"],
  event_times: ["event_time_id", "event_id", "raw_text", "normalized_start", "normalized_end", "precision", "certainty", "source_status", "evidence_segment_id", "confidence", "review_status"],
  time_expressions: ["time_expression_id", "segment_id", "raw_text", "normalized_start", "normalized_end", "precision", "expression_type", "certainty", "start_offset", "end_offset", "source_status", "confidence", "review_status"],
  document_annotations: ["annotation_id", "doc_id", "annotation_type", "annotation_text", "author_or_editor", "source_status", "target_type", "target_id", "source_segment_id"],
  coverage_audit: ["doc_id", "total_characters", "segmented_characters", "uncovered_characters", "overlap_characters", "total_segments", "attached_segments", "document_only_segments", "coverage_rate", "audit_status"]
};

const enumerations = {
  data_role: ["WORKFLOW_DEMO", "DEVELOPMENT", "INTERNAL_TEST", "BATCH_APPLICATION", "EXTERNAL_TEST", "UNASSIGNED"],
  include_in_study: ["YES", "NO", "TO_CONFIRM"],
  review_status: ["MODEL_CANDIDATE", "NEEDS_REVIEW", "CONFIRMED"],
  speaker_type: ["INTERVIEWEE", "INTERVIEWER", "EDITOR", "OTHER", "UNKNOWN"],
  segment_type: ["EVENT_EVIDENCE", "BACKGROUND", "INTERVIEWER_PROMPT", "NARRATOR_COMMENT", "DOCUMENT_NOTE", "OFF_TOPIC", "UNCERTAIN"],
  target_type: ["EVENT", "STAGE", "DOCUMENT"],
  annotation_target_type: ["EVENT", "STAGE", "DOCUMENT", "ENTITY", "SOURCE_SEGMENT"],
  source_function: ["EVIDENCE", "BACKGROUND", "COMMENT", "INTERVIEWER_PROMPT", "DOCUMENT_NOTE", "OTHER_RELATED", "DOCUMENT_ONLY"],
  event_type_id: ["MATERIAL_EVENT", "MENTAL_EVENT", "RELATIONAL_EVENT", "VERBAL_EVENT", "BEHAVIOURAL_EVENT", "EXISTENTIAL_EVENT"],
  factuality: ["FACT", "REPORTED", "NEGATED", "INTENDED", "HYPOTHETICAL"],
  confidence: ["HIGH", "MEDIUM", "LOW"],
  circumstance_kind: ["TIME", "LOCATION", "MANNER", "CAUSE", "PURPOSE"],
  stage_logic: ["SEQUENCE", "ENABLES", "CAUSES", "RESULTS_IN", "ELABORATES"],
  next_basis: ["explicit_time", "relative_time", "contextual_inference"],
  entity_type: ["PERSON", "PLACE", "ORGANIZATION", "MILITARY_UNIT", "HISTORICAL_EVENT", "PUBLICATION", "OTHER"],
  entity_subtype: ["INDIVIDUAL", "KINSHIP_PERSON", "ADMINISTRATIVE_PLACE", "SETTLEMENT", "ADDRESS", "LANDMARK", "ROUTE", "PARTY_ORGANIZATION", "SCHOOL", "HOSPITAL", "GOVERNMENT_AGENCY", "PRINTING_HOUSE", "MILITARY_FORMATION", "MASS_ORGANIZATION", "BATTLE", "POLITICAL_EVENT", "WAR", "BOOK", "PERIODICAL", "WEAPON", "INFRASTRUCTURE", "OTHER"],
  entity_authority_status: ["CANONICAL", "LOCAL_CANONICAL", "TRANSCRIPTION_UNCERTAIN", "UNRESOLVED"],
  mention_function: ["PARTICIPANT", "CIRCUMSTANCE", "MENTION_ONLY", "ANNOTATION_SUBJECT", "PROFILE_FACT", "SPEAKER"],
  source_status: ["ORAL_TESTIMONY", "EDITORIAL_PROFILE", "EDITORIAL_NOTE", "INTERVIEWER_QUESTION", "STRUCTURAL_INFERENCE", "MIXED"],
  alias_type: ["ALIAS", "ABBREVIATION", "HISTORICAL_NAME", "TRANSCRIPTION_VARIANT", "DESCRIPTIVE_NAME"],
  entity_relation_type: ["BORN_IN", "WORKED_AT", "STUDIED_AT", "MEMBER_OF", "HELD_POSITION_AT", "PART_OF", "LOCATED_IN", "RELATED_TO", "POSSIBLY_SAME_AS"],
  time_precision: ["DAY", "MONTH", "YEAR", "INTERVAL", "RELATIVE", "UNKNOWN"],
  time_certainty: ["EXACT", "APPROXIMATE", "OPEN_START", "OPEN_END", "UNCERTAIN"],
  time_expression_type: ["DATE", "INTERVAL"],
  role: ["Actor", "Goal", "Client", "Recipient", "Scope", "Senser", "Phenomenon", "Carrier", "Attribute", "Token", "Value", "Sayer", "Target", "Receiver", "Verbiage", "Existent", "Circumstance"]
};

function csvEscape(value) {
  const s = String(value ?? "");
  return /[",\n\r]/.test(s) ? `"${s.replaceAll('"', '""')}"` : s;
}

function csvLine(values) {
  return values.map(csvEscape).join(",");
}

async function walk(dir) {
  const entries = await fs.readdir(dir, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) files.push(...await walk(full));
    else if (entry.isFile() && entry.name.toLowerCase().endsWith(".docx") && !entry.name.startsWith(".~")) files.push(full);
  }
  return files.sort((a, b) => a.localeCompare(b, "zh-CN"));
}

function corpusRecord(file) {
  const rel = path.relative(corpusRoot, file);
  const name = path.basename(file);
  const no = (name.match(/^(\d+)\./) || [null, ""])[1];
  let interviewee = "";
  let visit = "";
  let prefix = "DOC";
  if (rel.includes("陈海峰")) {
    interviewee = "陈海峰";
    prefix = "CHF";
    visit = rel.includes("1访") ? "1" : rel.includes("2访") ? "2" : rel.includes("3访") ? "3" : "";
  } else if (rel.includes("陈锐霆")) {
    interviewee = "陈锐霆";
    prefix = "CRT";
    visit = name.match(/090422/) ? "090422" : name.match(/090423/) ? "090423" : name.match(/090508/) ? "090508" : name.match(/090509/) ? "090509" : name.match(/090510/) ? "090510" : "";
  } else if (rel.includes("杨永松")) {
    interviewee = "杨永松";
    prefix = "YYS";
    visit = name.match(/100507/) ? "100507" : name.match(/100506/) ? "100506" : "";
  }
  const docId = prefix === "CHF" ? `${prefix}-V${visit}-${no}` : `${prefix}-${no}`;
  const isPilot = name === "01.陈海峰（一访）（二校后 阅读版）.docx" || name === "01.陈锐霆 090422（二校后 阅读版）.docx";
  return [docId, interviewee, visit, no, name, rel, "VALID", isPilot ? "DEVELOPMENT" : "UNASSIGNED", "YES", "", "", isPilot ? "两份人工试标语料" : "正式纳入研究，数据角色待分配"];
}

const schema = {
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.local/oral-history-annotation-bundle.schema.json",
  "title": "口述史事件标注数据包",
  "type": "object",
  "required": ["document", "source_segments", "events", "coverage_audit"],
  "properties": {
    "document": {"type": "object", "required": ["doc_id", "title", "source_file"], "properties": {"doc_id": {"type": "string"}, "title": {"type": "string"}, "interviewee": {"type": "string"}, "source_file": {"type": "string"}, "data_role": {"enum": enumerations.data_role}}},
    "source_segments": {"type": "array", "items": {"type": "object", "required": ["segment_id", "doc_id", "segment_order", "source_part", "source_block_id", "segment_type", "verbatim_text"], "properties": {"segment_id": {"type": "string"}, "doc_id": {"type": "string"}, "segment_order": {"type": "integer", "minimum": 1}, "source_part": {"type": "string"}, "source_ref_id": {"type": ["string", "null"]}, "source_block_id": {"type": "string"}, "speaker_id": {"type": ["string", "null"]}, "speaker_type": {"enum": enumerations.speaker_type}, "start_offset": {"type": ["integer", "null"]}, "end_offset": {"type": ["integer", "null"]}, "segment_type": {"enum": enumerations.segment_type}, "verbatim_text": {"type": "string"}, "normalized_text": {"type": ["string", "null"]}, "review_status": {"enum": enumerations.review_status}}}},
    "events": {"type": "array", "items": {"type": "object", "required": ["event_id", "event_name", "event_type_id", "process", "evidence_segment_ids"], "properties": {"event_id": {"type": "string"}, "event_name": {"type": "string"}, "event_type_id": {"enum": enumerations.event_type_id}, "process": {"type": "string"}, "narrative_order": {"type": ["integer", "null"]}, "historical_order": {"type": ["integer", "null"]}, "result_state": {"type": ["string", "null"]}, "factuality": {"enum": enumerations.factuality}, "confidence": {"enum": enumerations.confidence}, "participants": {"type": "array"}, "circumstances": {"type": "array"}, "stages": {"type": "array"}, "evidence_segment_ids": {"type": "array", "minItems": 1, "items": {"type": "string"}}}}},
    "source_attachments": {"type": "array", "items": {"type": "object", "required": ["segment_id", "target_type", "target_id", "function"], "properties": {"segment_id": {"type": "string"}, "target_type": {"enum": enumerations.target_type}, "target_id": {"type": "string"}, "function": {"enum": enumerations.source_function}}}},
    "event_next": {"type": "array", "items": {"type": "object", "required": ["source_event_id", "target_event_id", "basis"], "properties": {"source_event_id": {"type": "string"}, "target_event_id": {"type": "string"}, "basis": {"enum": enumerations.next_basis}, "confidence": {"enum": enumerations.confidence}}}},
    "entities": {"type": "array", "items": {"type": "object", "required": ["entity_id", "canonical_name", "entity_type"], "properties": {"entity_id": {"type": "string"}, "canonical_name": {"type": "string"}, "entity_type": {"enum": enumerations.entity_type}, "entity_subtype": {"type": ["string", "null"]}, "authority_status": {"enum": enumerations.entity_authority_status}, "confidence": {"enum": enumerations.confidence}, "review_status": {"enum": enumerations.review_status}}}},
    "entity_mentions": {"type": "array", "items": {"type": "object", "required": ["mention_id", "segment_id", "entity_id", "mention_text", "start_offset", "end_offset", "mention_function", "source_status"], "properties": {"mention_id": {"type": "string"}, "segment_id": {"type": "string"}, "entity_id": {"type": "string"}, "mention_text": {"type": "string"}, "start_offset": {"type": "integer", "minimum": 0}, "end_offset": {"type": "integer", "minimum": 1}, "mention_function": {"enum": enumerations.mention_function}, "source_status": {"enum": enumerations.source_status}}}},
    "entity_aliases": {"type": "array", "items": {"type": "object", "required": ["alias_id", "entity_id", "alias_text", "alias_type"], "properties": {"alias_id": {"type": "string"}, "entity_id": {"type": "string"}, "alias_text": {"type": "string"}, "alias_type": {"enum": enumerations.alias_type}}}},
    "entity_relations": {"type": "array", "items": {"type": "object", "required": ["relation_id", "source_entity_id", "relation_type", "target_entity_id", "source_status"], "properties": {"relation_id": {"type": "string"}, "source_entity_id": {"type": "string"}, "relation_type": {"enum": enumerations.entity_relation_type}, "target_entity_id": {"type": "string"}, "source_status": {"enum": enumerations.source_status}}}},
    "event_times": {"type": "array", "items": {"type": "object", "required": ["event_time_id", "event_id", "raw_text", "precision", "certainty", "source_status"], "properties": {"event_time_id": {"type": "string"}, "event_id": {"type": "string"}, "raw_text": {"type": "string"}, "normalized_start": {"type": ["string", "null"]}, "normalized_end": {"type": ["string", "null"]}, "precision": {"enum": enumerations.time_precision}, "certainty": {"enum": enumerations.time_certainty}, "source_status": {"enum": enumerations.source_status}}}},
    "time_expressions": {"type": "array", "items": {"type": "object", "required": ["time_expression_id", "segment_id", "raw_text", "precision", "expression_type", "certainty", "start_offset", "end_offset", "source_status"], "properties": {"time_expression_id": {"type": "string"}, "segment_id": {"type": "string"}, "raw_text": {"type": "string"}, "normalized_start": {"type": ["string", "null"]}, "normalized_end": {"type": ["string", "null"]}, "precision": {"enum": enumerations.time_precision}, "expression_type": {"enum": enumerations.time_expression_type}, "certainty": {"enum": enumerations.time_certainty}, "start_offset": {"type": "integer", "minimum": 0}, "end_offset": {"type": "integer", "minimum": 1}, "source_status": {"enum": enumerations.source_status}}}},
    "coverage_audit": {"type": "object", "required": ["doc_id", "total_characters", "segmented_characters", "uncovered_characters", "coverage_rate"], "properties": {"doc_id": {"type": "string"}, "total_characters": {"type": "integer", "minimum": 0}, "segmented_characters": {"type": "integer", "minimum": 0}, "uncovered_characters": {"type": "integer", "minimum": 0}, "coverage_rate": {"type": "number", "minimum": 0, "maximum": 1}}}
  }
};

function colLetter(n) {
  let s = "";
  while (n > 0) {
    n--;
    s = String.fromCharCode(65 + (n % 26)) + s;
    n = Math.floor(n / 26);
  }
  return s;
}

function styleTable(sheet, headers, dataRowCount = 0) {
  const lastCol = colLetter(headers.length);
  const lastRow = Math.max(2, dataRowCount + 1);
  const used = sheet.getRange(`A1:${lastCol}${lastRow}`);
  used.format.font = { name: "Arial", size: 10, color: "#1F2937" };
  used.format.verticalAlignment = "center";
  const header = sheet.getRange(`A1:${lastCol}1`);
  header.format = {
    fill: "#1F4E78",
    font: { name: "Arial", size: 10, bold: true, color: "#FFFFFF" },
    horizontalAlignment: "center",
    verticalAlignment: "center",
    wrapText: true,
    borders: { preset: "all", style: "thin", color: "#D9D9D9" }
  };
  header.format.rowHeight = 32;
  if (dataRowCount > 0) {
    const body = sheet.getRange(`A2:${lastCol}${dataRowCount + 1}`);
    body.format.borders = { preset: "all", style: "thin", color: "#E5E7EB" };
    body.format.wrapText = false;
  }
  used.format.autofitColumns();
  const longFields = ["verbatim_text", "normalized_text", "annotation_text", "boundary_note", "source_file", "filename", "relative_path", "notes", "description", "role_label"];
  for (let i = 0; i < headers.length; i++) {
    const c = sheet.getRange(`${colLetter(i + 1)}1:${colLetter(i + 1)}${lastRow}`);
    const isLong = longFields.includes(headers[i]);
    const width = isLong ? 34 : 18;
    c.format.columnWidth = width;
    if (isLong && dataRowCount > 0) c.format.wrapText = true;
  }
  if (dataRowCount > 0) sheet.getRange(`A2:${lastCol}${dataRowCount + 1}`).format.autofitRows();
  sheet.freezePanes.freezeRows(1);
  sheet.showGridLines = false;
}

await fs.mkdir(outputDir, { recursive: true });
await fs.mkdir(previewDir, { recursive: true });

for (const [name, headers] of Object.entries(tables)) {
  await fs.writeFile(path.join(outputDir, `${name}.csv`), `\uFEFF${csvLine(headers)}\n`, "utf8");
}
await fs.writeFile(path.join(outputDir, "annotation_bundle.schema.json"), JSON.stringify(schema, null, 2) + "\n", "utf8");
await fs.writeFile(path.join(outputDir, "enumerations.json"), JSON.stringify(enumerations, null, 2) + "\n", "utf8");

const corpusFiles = await walk(corpusRoot);
const inventoryHeaders = ["doc_id", "interviewee", "visit_no", "file_no", "filename", "relative_path", "physical_status", "data_role", "include_in_study", "total_characters", "version_note", "notes"];
const inventoryRows = corpusFiles.map(corpusRecord);
await fs.writeFile(path.join(outputDir, "corpus_inventory.csv"), `\uFEFF${[csvLine(inventoryHeaders), ...inventoryRows.map(csvLine)].join("\n")}\n`, "utf8");

const workbook = Workbook.create();
const guide = workbook.worksheets.add("使用说明");
guide.getRange("A1:H1").merge();
guide.getRange("A1").values = [["口述史事件标注模板"]];
guide.getRange("A1:H1").format = {font: {name: "Arial", size: 15, bold: true, color: "#000000"}, horizontalAlignment: "left", verticalAlignment: "center"};
guide.getRange("A3:B13").values = [
  ["项目", "说明"],
  ["标注顺序", "文档登记 → 原文无损分段 → 片段分类 → 一级事件 → 二级阶段 → 全文实体提及 → 全文时间表达 → 实体消歧 → 事件规范时间 → 原文挂接 → NEXT → 覆盖率审计"],
  ["原文要求", "verbatim_text 必须保存原文，不得被摘要或规范化文本覆盖"],
  ["事件关系", "一级事件之间只使用 NEXT；阶段之间使用 NEXT_STAGE"],
  ["非事件内容", "背景、提问、评价和注释可挂事件或阶段；跑题和寒暄挂文档，标记 DOCUMENT_ONLY"],
  ["实体原则", "所有原文片段均可产生 EntityMention；只有真正承担过程角色者才进入 Participants，地点进入 Circumstances；事件历史时间进入 EventTimes"],
  ["时间原则", "正文、人物小传、脚注和提问中的明确年月日进入 TimeExpressions；录音时间戳不进入；EventTimes 只负责一级事件历史时间"],
  ["跨人物查询", "相同实体使用同一 entity_id；别名进入 EntityAliases；人工已核验但原文仍不确定者使用 review_status=CONFIRMED，并保留 authority_status 的不确定性"],
  ["完整体", "只作疑难边界辅助，不进入正式图谱字段"],
  ["审核状态", "MODEL_CANDIDATE、NEEDS_REVIEW、CONFIRMED"],
  ["完成条件", "coverage_rate=1.0000，且每个片段都有 EVENT、STAGE 或 DOCUMENT 挂接；实体提及和时间表达均可回到原文偏移"]
];
guide.getRange("A3:B3").format = {fill: "#1F4E78", font: {name: "Arial", size: 10, bold: true, color: "#FFFFFF"}, horizontalAlignment: "center", verticalAlignment: "center", borders: {preset: "all", style: "thin", color: "#D9D9D9"}};
guide.getRange("A4:B13").format = {font: {name: "Arial", size: 10, color: "#1F2937"}, verticalAlignment: "top", wrapText: true, borders: {preset: "all", style: "thin", color: "#D9D9D9"}};
guide.getRange("A:A").format.columnWidth = 18;
guide.getRange("B:B").format.columnWidth = 72;
guide.getRange("A1:H13").format.autofitRows();
guide.showGridLines = false;
guide.tabColor = "#1F4E78";

const inventory = workbook.worksheets.add("语料清单");
inventory.getRange("A1").write([inventoryHeaders, ...inventoryRows]);
styleTable(inventory, inventoryHeaders, inventoryRows.length);
inventory.tabColor = "#5B9BD5";

const sheetMap = {
  documents: "Documents",
  source_segments: "SourceSegments",
  source_attachments: "SourceAttachments",
  event_nodes: "Events",
  event_processes: "Processes",
  event_participants: "Participants",
  event_circumstances: "Circumstances",
  process_stages: "Stages",
  stage_next: "StageNext",
  event_next: "EventNext",
  entities: "Entities",
  entity_mentions: "EntityMentions",
  entity_aliases: "EntityAliases",
  entity_relations: "EntityRelations",
  event_times: "EventTimes",
  time_expressions: "TimeExpressions",
  document_annotations: "Annotations",
  coverage_audit: "CoverageAudit"
};

for (const [name, headers] of Object.entries(tables)) {
  const sheet = workbook.worksheets.add(sheetMap[name]);
  sheet.getRange("A1").write([headers]);
  styleTable(sheet, headers, 0);
}

const enums = workbook.worksheets.add("枚举值");
const enumNames = Object.keys(enumerations);
const maxLen = Math.max(...Object.values(enumerations).map(v => v.length));
const enumMatrix = [enumNames];
for (let i = 0; i < maxLen; i++) enumMatrix.push(enumNames.map(k => enumerations[k][i] ?? ""));
enums.getRange("A1").write(enumMatrix);
styleTable(enums, enumNames, maxLen);
enums.tabColor = "#A5A5A5";

workbook.recalculate();
const guideInspection = await workbook.inspect({
  kind: "table",
  range: "使用说明!A1:B13",
  include: "values,formulas",
  tableMaxRows: 20,
  tableMaxCols: 4,
  maxChars: 12000
});
await fs.writeFile(path.join(previewDir, "guide_inspection.ndjson"), guideInspection.ndjson, "utf8");

const formulaErrors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: {useRegex: true, maxResults: 300},
  summary: "final formula error scan"
});
await fs.writeFile(path.join(previewDir, "formula_errors.ndjson"), formulaErrors.ndjson, "utf8");

for (const sheetName of ["使用说明", "语料清单", ...Object.values(sheetMap), "枚举值"]) {
  const preview = await workbook.render({sheetName, autoCrop: "all", scale: 1, format: "png"});
  await fs.writeFile(path.join(previewDir, `${sheetName}.png`), new Uint8Array(await preview.arrayBuffer()));
}
const xlsx = await SpreadsheetFile.exportXlsx(workbook);
await xlsx.save(path.join(outputDir, "口述史事件标注模板.xlsx"));

const inspection = await workbook.inspect({kind: "sheet", include: "id,name", maxChars: 8000});
await fs.writeFile(path.join(previewDir, "workbook_sheets.ndjson"), inspection.ndjson, "utf8");

console.log(JSON.stringify({outputDir, workbook: "口述史事件标注模板.xlsx", csvTemplates: Object.keys(tables).length, corpusFiles: corpusFiles.length, sheets: 3 + Object.keys(tables).length}, null, 2));
