---
name: update
description: 根据主 HTML 的最新变化和产品决策的最新改动同步主 PRD 文档，并更新主 HTML 中的水滴标注（NoteDrip/TodoDrip/DripAnchor）。Use when the user runs /update, asks to update PRD from recent changes, sync drips with PRD, or refresh prototype annotations after UI/UX edits.
disable-model-invocation: true
---

# Update — 主 PRD 与原型水滴同步

将**主 HTML 交付页**的交互/文案/规则变更写回**主 PRD**，并同步该 HTML 内的**水滴标注**（`NoteDrip` / `TodoDrip` / `DripAnchor`）。  
水滴与调试工具为**交付/交接层**，须在 PRD 中声明「交付保留 · 生产剔除」，**不得**写入正式产品功能列表。

> 水滴组件 API 与集成方式见个人技能 **`proto-drip-annotations`**（`~/.cursor/skills/proto-drip-annotations/`）。

---

## 触发场景

- `/update` 或 `@update`
- 「根据最近改动更新 PRD」
- 交付 HTML 改了 UI/交互/文案，需 PRD 与水滴对齐
- 待办状态变化，需水滴与 TODO 清单同步
- 产品决策定稿后，需回写 PRD + 水滴

---

## Step 0：识别主源（必做 · 多 PRD/HTML 时）

**在改任何文件之前**，先弄清本项目的文档层级。用 `git diff`、`README`、PRD 文首「状态/开发约定」、`.cursor/rules` 或向用户确认。

### 0a. 盘点候选文件

```bash
# 并行：找 PRD / HTML / TODO
find . -maxdepth 4 \( -iname '*PRD*' -o -iname '*prd*' -o -name 'index.html' -o -iname '*todo*' -o -iname '*交接*' \) \
  ! -path '*/node_modules/*' ! -path '*/.git/*' 2>/dev/null | head -40

git diff --stat
git log -5 --oneline
```

### 0b. 判定角色（填表后再动手）

| 角色 | 含义 | 典型特征 |
|------|------|----------|
| **主 PRD** | `/update` **唯一写入**的产品需求来源 | 文首标「正式交付稿/工作稿」；README 指向它；版本号持续递增 |
| **开发冻结 PRD** | 给开发的定稿副本 | 由主 PRD 另存；可能版本号不同（如 v6.5）；**仅当用户明确要求时同步** |
| **归档 PRD** | 历史对照 | 文首标「归档/勿验收/Demo 稿」；**不更新** |
| **主 HTML** | UI/交互/文案/水滴的**唯一基准页** | 含 `DripProvider`、`PAGE_TODOS`；README 或 PRD §0 指向它 |
| **副本 HTML** | 交付包内拷贝或历史 Demo | 与主 HTML 关系须弄清：镜像同步 or 废弃 |
| **TODO 清单** | 与 `PAGE_TODOS` 键名对齐 | 项目根或交付包内 `*ToDo*.md` |

**关系规则**：

1. **只认一个主 PRD + 一个主 HTML**；其余为归档、冻结副本或交付镜像。
2. 若主 PRD 与主 HTML 冲突：**以主 HTML 当前行为为准**回写 PRD（除非用户当场指定以 PRD 为准）。
3. 若有「产品工作稿 PRD」+「开发冻结 PRD」：默认只更新**工作稿**；开发包冻结稿需用户说「同步到冻结稿/6.5」才改。
4. 若有「工作区 HTML」+「交付包 HTML」：默认以**工作区主 HTML** 为源；改完后按需 `cp` 到交付包（或用户指定只改交付包）。
5. 找不到主源时 **先问用户**，勿猜文件名。

将结论写入执行记录（回复用户时说明）：

```
主 PRD:    <path>
主 HTML:   <path>
TODO:      <path>
归档/跳过: <paths>
本次是否同步副本: 是/否
```

项目示例见 [examples/bc-landing-page.md](examples/bc-landing-page.md)。

---

## 工作流

```
Task Progress:
- [ ] 0. 识别主 PRD / 主 HTML / TODO 及副本关系
- [ ] 1. 收集变更（diff / 用户描述 / 读主 HTML）
- [ ] 2. 更新主 PRD
- [ ] 3. 更新主 HTML 水滴（DripAnchor / NoteDrip / TodoDrip / PAGE_TODOS）
- [ ] 4. 必要时同步 TODO 清单（及交付副本）
- [ ] 5. 交叉校验
```

### Step 1：收集变更

```bash
git diff -- <主PRD> <主HTML> <TODO>
```

无 git 时：通读主 HTML 中与 PRD 不一致的区块 + 用户本次描述的产品决策。

| 类型 | 写主 PRD | 写水滴 |
|------|----------|--------|
| 产品/UI 交互定稿 | ✅ 功能描述、验收标准 | ✅ NoteDrip body |
| 业务规则定稿 | ✅ 业务规则、数据规则 | ✅ NoteDrip body |
| 待办新增/完成 | ✅ 变更记录 / 待定节 | ✅ TodoDrip + PAGE_TODOS |
| 原型调试工具 | ✅ 声明生产剔除 | ❌ 不作正式功能 |
| 纯样式微调 | 仅影响可读性时写视觉节 | 可选 |

### Step 2：更新主 PRD

1. **版本号**：小改动 patch +1；产品决议改确认/决议节 + 变更记录。
2. **定位章节**：按 UI 区块映射到 PRD 功能节（见 [reference.md](reference.md) 映射模板）。
3. **必改**（有实质变更时）：交互/业务规则、验收标准（Given/When/Then）、变更记录。
4. **写作约束**：产品视角；已定用「已定」；待定引用 TODO ID；水滴只在「非生产/原型工具」节声明。

### Step 3：更新主 HTML 水滴

水滴是**开发交接工具**，比 PRD 更短，须与 PRD 一致。

#### 元素级锚定（DripAnchor）

贴在**具体控件旁**，不用 section 四角绝对定位：

```jsx
<DripAnchor side="end" drip={<NoteDrip inline title="…" body="…" prd={["§2.2 …"]} />}>
  <button>目标按钮</button>
</DripAnchor>
```

- `side`：`end` | `start` | `top` | `bottom`；多水滴用 `row`；块级用 `block`
- `NoteDrip` / `TodoDrip` 元素级锚定须加 **`inline`**

#### PAGE_TODOS（TODO 有变时）

```javascript
"T-00x": {
  title, detail, owner, status, blocker,
  prd: ["§…"],   // 须在主 PRD 中存在
  docs: ["prd"],  // 映射 DOC_LINKS 键
}
```

- `status` / `blocker` 与 TODO 表格一致
- 已定稿：移除 `TodoDrip` 或更新 status
- 新待办：TODO 加行 + `PAGE_TODOS` 加键 + 控件旁 `TodoDrip`

#### 不改动的部分

- `DripProvider` / `DripModal` / `proto-toolbar` 基础设施
- `.proto-drip` / `.proto-anchor` CSS（除非用户要求）
- **不要把水滴写进 PRD 正式功能列表**

### Step 4：同步 TODO 与副本

- 新待定 → TODO 加行 + `PAGE_TODOS` + `TodoDrip`
- 定稿 → TODO 标完成 + `PAGE_TODOS.status` + PRD 去「待补充」
- 若项目有交付包副本（冻结 PRD / 镜像 HTML）：**仅当用户要求或项目惯例**时同步

### Step 5：交叉校验

| 检查项 | 通过标准 |
|--------|----------|
| 主源明确 | 本次只改了认定的主 PRD + 主 HTML |
| 非生产声明 | PRD 写明水滴/Tweaks **交付保留、生产剔除** |
| `NoteDrip.prd` | 每条引用在主 PRD 中存在 |
| `PAGE_TODOS` | 键名与 TODO 表 ID 一一对应 |
| 文案一致 | 主 HTML 文案与 PRD 相同 |
| 变更记录 | 主 PRD 文末已追加版本行 |
| 水滴位置 | 锚定在控件旁，非 section 四角 |
| HTML 可写 | 若只读，`chmod u+w "<主HTML>"` |

---

## 输出格式

完成后汇报：

1. **主源路径**（主 PRD / 主 HTML）
2. **PRD 版本**与改了哪些节
3. **水滴**：新增/修改/移除的 DripAnchor、NoteDrip、TodoDrip
4. **TODO** 是否同步；交付副本是否同步
5. **未决项**：仍依赖 T-00x 的内容

---

## 反模式

- ❌ 未识别主源就改「第一个找到的 PRD/HTML」
- ❌ 更新归档 PRD 或历史 Demo HTML
- ❌ 把水滴当作正式功能写入产品功能节
- ❌ NoteDrip body 复制整段 PRD
- ❌ 只改 PRD 不更新对应 NoteDrip
- ❌ 水滴挂在 section 四角（`pos="tr"`）而非 `DripAnchor`
- ❌ `prd` 引用不存在的章节号
- ❌ 忘记 PRD 变更记录

---

## 附加资源

- 通用映射与检查清单：[reference.md](reference.md)
- BC 落地页项目示例：[examples/bc-landing-page.md](examples/bc-landing-page.md)
- 水滴组件集成：`~/.cursor/skills/proto-drip-annotations/`
