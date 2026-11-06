import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const workspace = "/Users/yuqi/Desktop/硕士毕业论文/2609";
const corpusRoot = path.join(workspace, "0920_01/语料");
const templateDir = path.join(workspace, "0920_01/现行标注/00_模板");
const csvPath = path.join(templateDir, "corpus_inventory.csv");
const workbookPath = path.join(templateDir, "口述史事件标注模板.xlsx");
const previewPath = path.join(templateDir, "预览/语料清单.png");
const inspectionPath = path.join(templateDir, "预览/语料清单_inspection.ndjson");

const headers = [
  "doc_id", "interviewee", "visit_no", "file_no", "filename", "relative_path",
  "source_format", "physical_status", "conversion_status", "data_role",
  "processing_status", "batch_id", "include_in_study", "total_characters",
  "sha256", "version_note", "notes"
];

const workflowDemoPaths = new Set([
  "C 陈海峰_4+8+23/1访/01.陈海峰（一访）（二校后 阅读版）.docx",
  "C 陈海峰_4+8+23/2访/01.陈海峰（二访）（二校后 阅读版）.docx",
  "C 陈海峰_4+8+23/3访/01.陈海峰（三访）20110808（三校后 阅读版）.doc",
  "C 陈锐霆_15/01.陈锐霆 090422（二校后 阅读版）.docx",
  "C 陈锐霆_15/02.陈锐霆 090422（二校后 阅读版）.docx",
  "Y 杨永松_10/01.杨永松100506（二校后 阅读版）.docx"
]);

const batch01Paths = new Set([
  "C 陈海峰_4+8+23/1访/02.陈海峰（一访）（一校后 阅读版）.docx",
  "C 陈锐霆_15/03.陈锐霆 090423（二校后 阅读版）.docx",
  "Y 杨永松_10/02.杨永松100506（二校后 阅读版）.docx"
]);

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
    else if (
      entry.isFile()
      && [".doc", ".docx"].includes(path.extname(entry.name).toLowerCase())
      && !entry.name.startsWith(".~")
    ) files.push(full);
  }
  return files.sort((a, b) => a.localeCompare(b, "zh-CN"));
}

async function makeRecord(file) {
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
  const sourceFormat = path.extname(file).slice(1).toUpperCase();
  const isDemo = workflowDemoPaths.has(rel);
  const isBatch01 = batch01Paths.has(rel);
  const convertedDemoPath = path.join(workspace, "0920_01/现行标注/04_陈海峰三访01/source_converted.docx");
  let conversionStatus = "NOT_REQUIRED";
  let versionNote = "";
  if (sourceFormat === "DOC") {
    if (isDemo && rel.includes("3访/01.")) {
      try {
        await fs.access(convertedDemoPath);
        conversionStatus = "CONVERTED_COPY_AVAILABLE";
        versionNote = "旧版DOC；现行标注已有转换副本";
      } catch {
        conversionStatus = "CONVERSION_REQUIRED";
        versionNote = "旧版DOC；待生成转换副本";
      }
    } else {
      conversionStatus = "CONVERSION_REQUIRED";
      versionNote = "旧版DOC；待生成转换副本";
    }
  }
  const sha256 = crypto.createHash("sha256").update(await fs.readFile(file)).digest("hex");
  const dataRole = isDemo ? "WORKFLOW_DEMO" : "BATCH_APPLICATION";
  const processingStatus = isDemo ? "CONFIRMED" : isBatch01 ? "VALIDATED" : "PENDING";
  const batchId = isDemo ? "DEMO" : isBatch01 ? "BATCH01" : "";
  const notes = isDemo
    ? "六份人工标注工作流Demo"
    : isBatch01
      ? "首批正式语料；窗口抽取与文档级回归已通过"
      : "后续正式批处理；待分批分配";
  return [
    docId, interviewee, visit, no, name, rel, sourceFormat,
    "SOURCE_PRESENT", conversionStatus, dataRole, processingStatus,
    batchId, "YES", "", sha256, versionNote, notes
  ];
}

const files = await walk(corpusRoot);
const rows = await Promise.all(files.map(makeRecord));
if (rows.length !== 60) throw new Error(`语料文件数应为60，实际为${rows.length}`);
if (new Set(rows.map(row => row[0])).size !== 60) throw new Error("doc_id存在重复");
if (new Set(rows.map(row => row[14])).size !== 60) throw new Error("发现内容哈希重复文件");

const csvText = `\uFEFF${[csvLine(headers), ...rows.map(csvLine)].join("\n")}\n`;
await fs.writeFile(csvPath, csvText, "utf8");

const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(workbookPath));
const sheet = workbook.worksheets.getItem("语料清单");
sheet.getUsedRange().clear({ applyTo: "all" });
sheet.getRange("A1").write([headers, ...rows]);
const lastRow = rows.length + 1;
const used = sheet.getRange(`A1:Q${lastRow}`);
used.format.font = { name: "Arial", size: 10, color: "#1F2937" };
used.format.verticalAlignment = "center";
const header = sheet.getRange("A1:Q1");
header.format = {
  fill: "#1F4E78",
  font: { name: "Arial", size: 10, bold: true, color: "#FFFFFF" },
  horizontalAlignment: "center",
  verticalAlignment: "center",
  wrapText: true,
  borders: { preset: "all", style: "thin", color: "#D9D9D9" }
};
header.format.rowHeight = 32;
const body = sheet.getRange(`A2:Q${lastRow}`);
body.format.borders = { preset: "all", style: "thin", color: "#E5E7EB" };
body.format.wrapText = false;
for (const [column, width] of Object.entries({
  A: 14, B: 10, C: 10, D: 10, E: 42, F: 52, G: 12, H: 16, I: 25,
  J: 18, K: 20, L: 12, M: 14, N: 14, O: 66, P: 25, Q: 38
})) sheet.getRange(`${column}1:${column}${lastRow}`).format.columnWidth = width;
for (const column of ["E", "F", "I", "K", "P", "Q"]) {
  sheet.getRange(`${column}2:${column}${lastRow}`).format.wrapText = true;
}
body.format.autofitRows();
sheet.freezePanes.freezeRows(1);
sheet.showGridLines = false;
sheet.tabColor = "#5B9BD5";
workbook.recalculate();

const inspection = await workbook.inspect({
  kind: "table",
  range: `语料清单!A1:Q${lastRow}`,
  include: "values,formulas",
  tableMaxRows: 65,
  tableMaxCols: 17,
  maxChars: 50000
});
await fs.writeFile(inspectionPath, inspection.ndjson, "utf8");
const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!",
  options: { useRegex: true, maxResults: 300 },
  summary: "语料清单公式错误扫描"
});
if (errors.ndjson.trim()) {
  const parsed = errors.ndjson.trim().split("\n").map(line => JSON.parse(line));
  if (parsed.some(item => (item.matches || []).length > 0)) throw new Error("语料清单存在公式错误");
}
const preview = await workbook.render({ sheetName: "语料清单", range: "A1:Q14", scale: 1.2, format: "png" });
await fs.writeFile(previewPath, new Uint8Array(await preview.arrayBuffer()));
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(workbookPath);

const counts = rows.reduce((acc, row) => {
  acc.roles[row[9]] = (acc.roles[row[9]] || 0) + 1;
  acc.statuses[row[10]] = (acc.statuses[row[10]] || 0) + 1;
  acc.formats[row[6]] = (acc.formats[row[6]] || 0) + 1;
  acc.conversions[row[8]] = (acc.conversions[row[8]] || 0) + 1;
  return acc;
}, { roles: {}, statuses: {}, formats: {}, conversions: {} });
console.log(JSON.stringify({ files: rows.length, ...counts }, null, 2));
