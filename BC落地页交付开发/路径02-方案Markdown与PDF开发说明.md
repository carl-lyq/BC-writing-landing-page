# t路径 02 · 学习方案 Markdown 渲染与 PDF 导出 · 开发说明

**读者**：后端 / 前端  
**关联 PRD**：`UI/docs/BC落地页PRD_UI更新.md` §2.2 功能 5.1  
**交付页参考**：`UI/index.html` → `Path02PlanProvider`  
**PDF 样例脚本**：`scripts/generate_plan_pdf.py`  
**方案 Markdown 模版样例**：`雅思写作学习提分方案.md`

---

## 1. 端到端流程

```
学生（已登录）
  → 路径 02 CTA「获取我的专属方案」
  → 上传 1 份 PDF（BC 写作报告，≤5MB）
  → 落地页后端接收文件
  → 后端调用【扣子工作流】（传入 PDF / 解析文本）
  → 扣子返回 Markdown 正文
  → 后端落库 + 返回任务结果给前端
       ├─ markdown：前端弹窗内渲染预览（主展示）
       └─ pdfUrl：后端异步或同步生成 branded PDF，供「下载 PDF」
```

**正式版原则**：


| 环节       | 负责方        | 说明                              |
| -------- | ---------- | ------------------------------- |
| PDF 上传   | 前端 → 后端    | **仅 1 个** PDF；格式校验见 PRD         |
| AI 生成    | **扣子工作流**  | 输出约定为 **Markdown 字符串**（UTF-8）   |
| 在线预览     | **前端**     | 将 Markdown 渲染为 HTML（见 §4）       |
| 下载 PDF   | **后端**（推荐） | 同一份 Markdown 套品牌模版后导出 PDF（见 §5） |
| Demo 交付页 | 前端 mock    | 仍为结构化 `preview` + 假 PDF；正式接入时替换 |


---

## 2. 与扣子的接口约定（建议）

### 2.1 后端 → 扣子


| 项   | 建议                                              |
| --- | ----------------------------------------------- |
| 输入  | 用户 PDF（文件 URL / base64 / 扣子文档节点可接受的格式，按扣子侧文档配置） |
| 输出  | **单一字段** `markdown`（string），或工作流最终节点的文本输出       |
| 模版  | 教研提供章节结构；可参考 `雅思写作学习提分方案.md`                    |
| 超时  | 目标 ≤1 分钟；落地页采用**异步任务**（PRD 已定）                  |


### 2.2 后端 → 前端（任务完成）

```json
{
  "taskId": "…",
  "status": "ready",
  "markdown": "# 雅思写作学习提分方案\n\n…",
  "pdfUrl": "https://…/plans/{id}/download.pdf",
  "generatedAt": "2026-06-09T12:00:00Z"
}
```


| 字段         | 必填  | 说明                                         |
| ---------- | --- | ------------------------------------------ |
| `markdown` | 是   | 扣子返回正文；前端预览唯一数据源                           |
| `pdfUrl`   | 是   | 已生成的 PDF 下载地址（短期 signed URL 或需登录的 API）     |
| `preview`  | 否   | **不要**再维护一套与 Markdown 平行的结构化 JSON（避免双源不一致） |


**生成顺序（推荐）**：

1. 扣子返回 `markdown`
2. 后端持久化 `markdown`
3. 后端调用 PDF 服务（§5）生成文件并存储
4. 将 `markdown` + `pdfUrl` 一并返回前端

若 PDF 生成略慢，可先返回 `markdown` + `pdfStatus: "processing"`，前端轮询 `pdfUrl`；V1 也可同步生成后一次性返回。

---

## 3. 上传规则（产品 · 已定）


| 规则  | 值                          |
| --- | -------------------------- |
| 数量  | **1 份** PDF                |
| 大小  | ≤5MB                       |
| 格式  | `.pdf` / `application/pdf` |
| 登录  | 必须                         |
| 替换  | 删除当前文件后可重新选择               |


交付页 `PlanUploadArea` 已按 **单文件** 交互更新；正式 API 仅接收单文件 `multipart/form-data` 字段名建议：`report` 或 `file`。

---

## 4. 前端：Markdown 预览

### 4.1 依赖建议

- `marked` 或 `markdown-it`（与后端/PDF 管线使用同一解析器更佳）  
- 在结果弹窗 `#plan-result-preview` 容器内 `innerHTML` 或 React 组件渲染

### 4.2 安全

- 扣子输出为受信内容时可用 `marked` 默认解析  
- 若未来允许用户编辑，须 **sanitize**（如 `DOMPurify`）

### 4.3 样式

- 复用落地页 Token：`--ink`、`--accent`、`--paper`  
- 预览区滚动 + 顶底渐变遮罩（交付页 `PlanResultPreview` 已有样式可复用）  
- 标题层级与 PDF 模版保持一致，避免「屏上好看、下载版式不一致」

### 4.4 替换 Demo 逻辑

当前 Demo：

- `buildDemoPlanPreview(fileNames)` → 结构化对象  
- `PlanResultPreview` 渲染 sections  
- `createDemoPdfBlob` 假 PDF

正式版：

```javascript
// 伪代码
const html = marked.parse(plan.markdown);
<PlanResultPreview markdown={plan.markdown} />
// 下载
window.open(plan.pdfUrl, "_blank"); // 或 fetch blob + a[download]
```

---

## 5. 后端：Markdown → 品牌 PDF

### 5.1 参考实现（本仓库）


| 文件                                          | 作用                                               |
| ------------------------------------------- | ------------------------------------------------ |
| `scripts/generate_plan_pdf.py`              | 本地验证管线：MD → HTML（含 Logo 页眉）→ Chrome Headless PDF |
| `scripts/fonts/NotoSansSC-400.woff2`        | 中文正文字体（**必须**嵌入，否则无头浏览器中文空白）                     |
| `scripts/fonts/NotoSansSC-700.woff2`        | 标题粗体                                             |
| `BC落地页交付开发/UI/assets/躺着学LOGO CHILLPREP.png` | 页眉左 Logo                                         |
| `BC落地页交付开发/BC备考平台logo/Property 1=默认.png`    | 页眉右 Logo                                         |


**本地试生成**：

```bash
# 将扣子返回的 markdown 写入 雅思写作学习提分方案.md 后：
python3 scripts/generate_plan_pdf.py
# 输出：./雅思写作学习提分方案.pdf
```

### 5.2 生产部署建议


| 方案                                  | 说明                                                         |
| ----------------------------------- | ---------------------------------------------------------- |
| **A. 移植 Python 脚本**                 | 任务 Worker 内调用；需安装 Chrome/Chromium + `markdown` + woff2 字体  |
| **B. Gotenberg**                    | HTML 模版 + `POST /forms/chromium/convert/html`；与 PRD 部署讨论一致 |
| **C. Node `md-to-pdf` + Puppeteer** | 与主站 Node 栈统一时使用                                            |


**HTML 模版要求**（与 `generate_plan_pdf.py` 内 `build_html` 对齐）：

- A4、`@page` 边距约 18mm / 16mm  
- 页眉双 Logo + 底部分隔线  
- `body` 使用嵌入 `Noto Sans SC`（woff2）  
- Markdown 转出的 HTML 插入 `<main class="doc-body">`

### 5.3 注意

- 勿用 `file://` 在无头环境直接打开未嵌字体的 HTML  
- 勿依赖 `PingFang SC` 等系统字体（Linux 服务器上不存在）  
- PDF 与预览应来自**同一份 `markdown` 源**

---

## 6. API 草案（T-013）

### `POST /api/landing/path02/plan`

- Auth：登录态  
- Body：`multipart/form-data`，单文件 `file`  
- Response：`202` + `{ taskId }`

### `GET /api/landing/path02/plan/tasks/{taskId}`

- Response：`pending` | `ready` | `failed`  
- `ready` 时含 `markdown`、`pdfUrl`  
- `failed` 时前端须调用失败处理（见 §7）

### `GET /api/landing/path02/plan/current`

- 回访「查看我的方案」  
- Response：当前有效方案的 `markdown`、`pdfUrl`

### `POST /api/landing/path02/plan/regenerate`

- 覆盖确认后调用；逻辑同新建

---

## 7. 生成失败（统一前端提示）

**任一环节失败**均走同一套 UI（扣子超时/报错、Markdown 落库失败、PDF 导出失败、网络错误等）：


| 项   | 规范                                       |
| --- | ---------------------------------------- |
| 文案  | **方案生成失败，请重试或联系客服**（固定，不可按错误码分化给用户）      |
| 位置  | 页面**顶部** Toast（Nav 下方，`auth-toast--top`） |
| 时长  | **3 秒**                                  |
| 弹窗  | 关闭「生成中」弹窗                                |
| 状态  | 清除 `generating`；若本次为**覆盖生成**，恢复覆盖前的有效方案  |
| 埋点  | `path02_gen_fail`                        |


**正式接入**：轮询 `taskId` 得到 `status: "failed"`，或扣子/PDF 任一步 catch 后调用：

```javascript
window.bcLandingPath02GenerationFailed?.();
```

交付页已实现 `failGeneration` 并挂到上述全局方法；Demo 仍默认模拟成功，联调时可手动调用以验收 Toast。

---

## 8. 埋点（与 PRD §4.3 对齐）


| btn_id                 | 时机         |
| ---------------------- | ---------- |
| `path02_plan_open`     | 打开上传弹窗     |
| `path02_upload_submit` | 提交 PDF     |
| `path02_wait_close`    | 生成中关闭弹窗    |
| `path02_gen_complete`  | 任务成功       |
| `path02_gen_fail`      | 任务失败（任意环节） |
| `path02_view`          | 查看我的方案     |
| `path02_download`      | 点击下载 PDF   |


---

## 9. 验收清单

- [ ] 仅允许选择 **1** 个 PDF；第二份提示或替换逻辑正确  
- [ ] 扣子返回 Markdown 后，结果弹窗**可见完整中文正文**  
- [ ] 下载 PDF 含双 Logo、中文正常、章节与预览一致  
- [ ] 关闭弹窗后任务继续；会话内完成自动弹结果  
- [ ] 刷新后不自动弹窗，「查看我的方案」可打开  
- [ ] 再次生成走覆盖确认；生成中 CTA 拦截  
- [ ] 模拟 `failed` 或调用 `bcLandingPath02GenerationFailed()` → 页顶 Toast 3 秒、文案正确  

---

## 10. 相关待办


| ID    | 内容                                    |
| ----- | ------------------------------------- |
| T-012 | 扣子工作流 Prompt / 章节模版 / 示例 Markdown     |
| T-013 | 上传、异步任务、扣子调用、Markdown 存储、PDF 导出、3 份历史 |


---

*更新：2026-06-09 · 单 PDF + 扣子 Markdown + 双通道展示 + 统一失败 Toast*