---
name: update
description: 根据 UI/index.html 或产品决策的最新改动同步 UI/docs/BC落地页PRD_UI更新.md，并更新交付页中的原型水滴标注（NoteDrip/TodoDrip/DripAnchor）。Use when the user runs /update, asks to update PRD from recent changes, sync drips with PRD, or refresh prototype annotations after UI/UX edits.
---

# Update — PRD 与原型水滴同步

将 **`UI/index.html`** 的交互/文案变更写回 **`UI/docs/BC落地页PRD_UI更新.md`**，并同步交付页内的 **水滴标注**。生产环境不含水滴，但 PRD 须持续声明这一点（§2.3）。

## 触发场景

- 用户运行 `/update` 或 `@update`
- 「根据最近改动更新 PRD」
- 交付 HTML 改了 UI/交互/文案，需要 PRD 与水滴对齐
- 待办状态变化，需要水滴与 `BC落地页ToDo.md` 同步

## 核心文件

| 文件 | 角色 |
|------|------|
| **`UI/docs/BC落地页PRD_UI更新.md`** | 产品需求**唯一来源**（正式交付稿 v1.0.x） |
| **`UI/index.html`** | UI 交付页 + 水滴标注（**交付保留，生产剔除**） |
| **`BC落地页ToDo.md`** | 待办清单；与 `PAGE_TODOS` 对齐 |
| `BC落地页PRD.md` | **仅归档**（v0.21 Demo 稿），**勿再更新** |
| `BC落地页Demo.html` | 历史原型，**非验收基准** |

## 工作流

```
Task Progress:
- [ ] 1. 收集变更（diff / 用户描述 / 读 UI/index.html）
- [ ] 2. 更新 UI/docs/BC落地页PRD_UI更新.md
- [ ] 3. 更新水滴（DripAnchor / NoteDrip / TodoDrip / PAGE_TODOS）
- [ ] 4. 必要时同步 BC落地页ToDo.md
- [ ] 5. 交叉校验文档一致
```

### Step 1：收集变更

并行执行：

```bash
git diff -- UI/docs/BC落地页PRD_UI更新.md BC落地页ToDo.md UI/index.html
git log -5 --oneline
```

若无 git 历史，直接读 `UI/index.html` 中与 PRD 不一致的区块（Hero 标语/视频、问题匹配、路径、学员故事、页脚、Tweaks）。

**变更分类**：

| 类型 | 写 PRD | 写水滴 |
|------|--------|--------|
| 产品/UI 交互定稿 | ✅ 功能描述、验收标准 | ✅ NoteDrip body |
| 业务规则定稿 | ✅ 业务规则、数据规则 | ✅ NoteDrip body |
| 待办新增/完成 | ✅ §9.2 / 变更记录 | ✅ TodoDrip + PAGE_TODOS |
| 原型调试工具 | ✅ §2.3 声明生产剔除 | ❌ 不当作正式功能 |
| 纯样式微调 | 仅影响可读性时写 §2.4 / §2.5 | 可选 |

### Step 2：更新 PRD

目标文件：**`UI/docs/BC落地页PRD_UI更新.md`**

1. **版本号**：小改动 `v1.0.x → v1.0.x+1`；定稿决议改 §9.9
2. **定位章节**（按变更类型）：

| UI 区块 | PRD 章节 |
|---------|----------|
| 导航 / 联名 | §2.1 |
| Hero 标语 + 公开课 | §2.2 功能 1（含 1.1 标语、1.2 视频） |
| 痛点卡 A | §2.2 功能 2 |
| 问卷 B | §2.2 功能 3 |
| A/B 切换 | §2.2 功能 4 |
| 6 条路径 + 路径02 | §2.2 功能 5 / 5.1 |
| 学员故事 | §2.2 功能 6 |
| 页脚 | §2.2 功能 7 |
| 水滴 / Tweaks / proto-toolbar | §2.3（**交付保留，生产剔除**） |
| 字号 / 视觉 / Token | §2.4 / §2.5 |
| 响应式 | §3.2 |
| 埋点 | §4.3.1 |
| MVP 边界 | §7–§8 |

3. **必改项**（有实质变更时）：
   - 对应功能的「交互规则 / 业务规则 / 验收标准」
   - §9.5–§9.9 交付差异与产品决议（如有）
   - 文末变更记录（日期、版本、摘要）

4. **PRD 写作约束**：
   - 产品视角，不写 React/CSS 实现细节（Token 速查 §9.8 除外）
   - 已定稿用「已定」；待定保留待办引用（如 T-001）
   - **水滴永远写在 §2.3**，标注「交付页保留 · 生产构建剔除」

### Step 3：更新水滴

水滴是 **开发交接工具**，内容须与 PRD 一致、比 PRD 更短。位于 **`UI/index.html`**。

#### 3a. 元素级锚定（DripAnchor）

水滴须贴在**具体控件旁**，不用板块四角绝对定位：

```jsx
<DripAnchor side="end" drip={<NoteDrip inline title="…" body="…" prd={["§2.2 …"]} />}>
  <button>目标按钮</button>
</DripAnchor>
```

- `side`：`end`（右侧）| `start` | `top` | `bottom`
- `row`：多个水滴横向排列（如路径 CTA 行）
- `block`：块级容器（如 section 标题）
- NoteDrip / TodoDrip 须加 **`inline`**（除非用 `style` 精确定位）

#### 3b. 更新 `PAGE_TODOS`（`BC落地页ToDo.md` 有变时）

位于 `UI/index.html` 内 `const PAGE_TODOS = { ... }`。每个条目字段：

```javascript
"T-00x": {
  title, detail, owner, status, blocker,
  prd: ["§2.2 功能 N", ...],  // 须能在 PRD 中找到
  docs: ["tracking"],           // 可选，映射 DOC_LINKS
}
```

- `status` / `blocker` 与 `BC落地页ToDo.md` 表格一致
- 已完成项：从区块移除 `TodoDrip`，或保留但更新 status 为「已定稿」
- 新待办：在 `BC落地页ToDo.md` 加行 + `PAGE_TODOS` 加键 + 对应控件加 `<TodoDrip inline todoId="T-00x" />`

#### 3c. 更新 `NoteDrip`

```jsx
<DripAnchor side="end" drip={
  <NoteDrip
    inline
    title="简短标题"
    body={"多行说明\n· 要点"}
    prd={["§2.2 功能 4"]}
    docs={["prd", "todo", "tracking"]}
    links={[{ label, href }]}
  />
}>
  {/* 锚定目标元素 */}
</DripAnchor>
```

**何时改 NoteDrip**：
- PRD 改了交互/规则 → 更新 `body` 与 `prd` 章节列表
- 新增区块 → 在对应控件旁补 DripAnchor + NoteDrip
- 文案/UI 定稿 → 去掉 body 里已过时的描述

#### 3d. 更新 `TodoDrip`

```jsx
<DripAnchor side="end" drip={<TodoDrip inline todoId="T-001" />}>
  <button>互动诊断</button>
</DripAnchor>
```

同一控件多个待办：在 `drip` 内用 Fragment 并列多个 `TodoDrip inline`。

#### 3e. 不改动的部分

- `DripProvider` / `DripModal` / `proto-toolbar` 基础设施
- `.proto-drip` / `.proto-anchor` CSS（除非用户明确要求改样式）
- **不要**把水滴写进 PRD 正式功能列表

组件 API 详见 [drip-reference.md](drip-reference.md)。

### Step 4：同步 BC落地页ToDo.md

PRD 变更涉及待办时：
- 新待定项 → `BC落地页ToDo.md` 加行 + HTML `PAGE_TODOS` + `TodoDrip`
- 定稿项 → `BC落地页ToDo.md` 标完成 + 更新 `PAGE_TODOS.status` + PRD 去掉「待补充」措辞

### Step 5：交叉校验

| 检查项 | 通过标准 |
|--------|----------|
| PRD §2.3 | 明确水滴/Tweaks **交付保留、生产剔除** |
| NoteDrip.prd | 每条引用在 PRD 中存在 |
| PAGE_TODOS | 键名与 BC落地页ToDo.md ID 一一对应 |
| 文案一致 | 交付页文案与 PRD 相同 |
| 变更记录 | PRD 文末已追加本次版本行 |
| 水滴位置 | 锚定在具体控件旁，非 section 四角 |
| HTML 可写 | 若只读，`chmod u+w "UI/index.html"` |

## 输出格式

完成后向用户汇报：

1. **PRD 版本**与改了哪些 §
2. **水滴**：新增/修改/移除的 DripAnchor、NoteDrip、TodoDrip
3. **待办**是否同步
4. **未决项**：仍依赖 T-00x 的内容

## 反模式

- ❌ 更新归档的 `BC落地页PRD.md` 而非 `UI/docs/BC落地页PRD_UI更新.md`
- ❌ 把水滴当作正式版功能写入 §2.2
- ❌ NoteDrip body 复制整段 PRD（应提炼要点）
- ❌ 只改 PRD 不更新对应 NoteDrip
- ❌ 水滴挂在 section 四角（`pos="tr"`）而非 `DripAnchor` 元素旁
- ❌ `prd` 引用不存在的章节号
- ❌ 忘记 PRD 变更记录

## 附加资源

- 水滴组件与分布清单：[drip-reference.md](drip-reference.md)
