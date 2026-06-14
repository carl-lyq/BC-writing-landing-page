#!/usr/bin/env node
/**
 * Merge proto-drip-export.json into UI/index.html and markdown docs.
 * Usage: node scripts/merge-proto-drip-export.mjs [path/to/proto-drip-export.json]
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");

const exportPath = path.resolve(root, process.argv[2] || "proto-drip-export.json");
const htmlPath = path.join(root, "UI/index.html");
const deliveryHtmlPath = path.join(root, "BC落地页交付开发/UI/index.html");
const notesMdPath = path.join(root, "UI/docs/BC落地页-手写备注.md");
const todosMdPath = path.join(root, "BC落地页ToDo-手写.md");

function fmtTime(iso) {
  if (!iso) return "—";
  const d = new Date(iso);
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")} ${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`;
}

function buildNotesMd(store) {
  let md = "# BC落地页 · 手写备注\n\n";
  md += "> 由原型标注工具导出并合并。系统备注见交付页 `NoteDrip` 与 PRD。\n\n";
  if (!store.notes?.length) {
    md += "_（暂无手写备注）_\n";
    return md;
  }
  for (const n of store.notes) {
    md += `## ${n.id} · ${n.title}\n\n`;
    md += `- 作者：${n.author || "—"}\n`;
    md += `- 更新：${fmtTime(n.updatedAt)}\n`;
    if (n.anchor?.label) md += `- 锚点：${n.anchor.label}\n`;
    if (n.anchor?.selector) md += `- 选择器：\`${n.anchor.selector}\`\n`;
    md += `\n${n.body || ""}\n\n---\n\n`;
  }
  return md;
}

function buildTodosMd(store) {
  let md = "# BC落地页 · 手写待办\n\n";
  md += "> 由原型标注工具导出并合并。系统待办见 [`BC落地页ToDo.md`](./BC落地页ToDo.md)。\n\n";
  if (!store.todos?.length) {
    md += "_（暂无手写待办）_\n";
    return md;
  }
  for (const t of store.todos) {
    md += `## ${t.id} · ${t.title}\n\n`;
    md += `- 作者：${t.author || "—"}\n`;
    md += `- 更新：${fmtTime(t.updatedAt)}\n`;
    md += `- 负责人：${t.owner || "—"}\n`;
    md += `- 状态：${t.status || "待处理"}\n`;
    if (t.blocker) md += `- 阻塞：${t.blocker}\n`;
    if (t.anchor?.label) md += `- 锚点：${t.anchor.label}\n`;
    if (t.anchor?.selector) md += `- 选择器：\`${t.anchor.selector}\`\n`;
    md += `\n${t.detail || ""}\n\n---\n\n`;
  }
  return md;
}

function patchHtml(filePath, store) {
  let html = fs.readFileSync(filePath, "utf8");
  const snippet = `<script type="application/json" id="proto-drip-store">${JSON.stringify({ version: store.version || 1, notes: store.notes || [], todos: store.todos || [] }, null, 2)}</script>`;
  const re = /<script type="application\/json" id="proto-drip-store">[\s\S]*?<\/script>/;
  if (!re.test(html)) {
    throw new Error(`proto-drip-store script not found in ${filePath}`);
  }
  html = html.replace(re, snippet);
  fs.writeFileSync(filePath, html, "utf8");
  console.log(`Updated ${filePath}`);
}

if (!fs.existsSync(exportPath)) {
  console.error(`Export file not found: ${exportPath}`);
  process.exit(1);
}

const raw = JSON.parse(fs.readFileSync(exportPath, "utf8"));
const store = {
  version: raw.version || 1,
  notes: raw.notes || [],
  todos: raw.todos || [],
};

patchHtml(htmlPath, store);
if (fs.existsSync(deliveryHtmlPath)) {
  patchHtml(deliveryHtmlPath, store);
}

fs.writeFileSync(notesMdPath, buildNotesMd(store), "utf8");
fs.writeFileSync(todosMdPath, buildTodosMd(store), "utf8");

console.log(`Wrote ${notesMdPath}`);
console.log(`Wrote ${todosMdPath}`);
console.log(`Merged ${store.notes.length} notes, ${store.todos.length} todos`);
