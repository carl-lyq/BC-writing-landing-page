# 水滴标注参考（UI 交付页）

> **`UI/index.html` 交付页保留**；**生产构建须剔除**（见 PRD §2.3）。

## 架构

```
DripProvider（根包裹）
├── DripAnchor + NoteDrip / TodoDrip（元素级锚定）
├── DripModal（点击水滴弹出）
└── proto-toolbar（左侧控制条，默认收起）
```

## DOC_LINKS 键

| 键 | 文件 |
|----|------|
| `prd` | `./docs/BC落地页PRD_UI更新.md` |
| `todo` | `../BC落地页ToDo.md` |
| `tracking` | `./docs/Partner_LandingPage_Tracking_Guide.pdf` |
| `html` | `./index.html` |

## DripAnchor

```jsx
<DripAnchor side="end" row block drip={...}>
  {/* 目标控件 */}
</DripAnchor>
```

| Prop | 说明 |
|------|------|
| `side` | `end`（右）\| `start` \| `top` \| `bottom` |
| `row` | 多水滴横向排列 |
| `block` | 块级容器（section 标题等） |

## NoteDrip props

| Prop | 类型 | 说明 |
|------|------|------|
| `inline` | bool | **必加**（元素级锚定时） |
| `title` | string | 弹层标题 |
| `body` | string | 说明正文，支持 `\n` |
| `prd` | string[] | PRD 章节标签，如 `"§2.2 功能 1"` |
| `docs` | string[] | DOC_LINKS 键 |
| `links` | `{label,href}[]` | 可选外链 |
| `pos` / `style` | — | **已废弃**于交付页；勿用 section 四角定位 |

## TodoDrip props

| Prop | 类型 | 说明 |
|------|------|------|
| `inline` | bool | **必加**（元素级锚定时） |
| `todoId` | string | 对应 `PAGE_TODOS` 键，如 `"T-001"` |

## 当前区块分布（维护时对照）

| 区块 | 锚定元素 | NoteDrip | TodoDrip |
|------|----------|----------|----------|
| Hero | 标语文案 | Banner 规格 | — |
| Hero | 播放按钮 | 播放量规则 | — |
| Hero | 播放列表标题 | 无眉标 + 总时长；6 集 Icey Zhang | T-003b |
| 需求匹配 | 「自主选择」Tab | 模式 A | — |
| 需求匹配 | 「互动诊断」Tab | 模式 B | T-001 |
| 需求匹配 | 选中卡「查看路径」 | 跳转逻辑 | — |
| 需求匹配 | 问卷「查看专属路径」 | 跳转逻辑 | — |
| 学习路径 | 「学习路径」标题 | 六大路径结构 | — |
| 学习路径 | 索引条 01–06 | BC 埋点 | T-010, T-011 |
| 学习路径 | 各路径媒体图 | 16:10；6 张正式图待 T-016 | T-016 |
| 学习路径 | 各路径主 CTA | 01/03/05/06 deep link；04 微信弹窗；02 方案流程 | 02：T-012–013 |
| 学习路径 | 「回到路径选择」 | 滚动回 #pain | — |
| 学习路径 | 微信咨询卡 | 点击打开联名弹窗；正式 QR | T-016 |
| 学员故事 | 区块标题 | 居中标题 + 案例卡 + 路径按钮 | — |
| 页脚 | 品牌名 | 主站对齐 | T-008 |
| 导航 | 左侧躺着学 Logo | — | T-008 |
| 导航 | 右侧登录 + BC Logo | 登录在 BC 左；BC 高与躺着学一致 34/28 | T-006 / T-008 |
| 导航 | 「学员故事」链接 | IA | — |
| 导航 | 登录按钮 | 登录拦截；04 例外；学生来源 | T-006 |
| Tweaks | ⚙ 按钮 | 调试说明 | — |

新增区块时按上表模式补 `DripAnchor`；移除区块时删除对应水滴。

## PAGE_TODOS 维护规则

1. 键名 = `BC落地页ToDo.md` 表格 ID（如 `T-003b`）
2. `detail` 一句话说明 + 与 PRD 不矛盾
3. `prd` 数组指向相关 PRD 节，便于弹层跳转
4. 已完成：更新 `status: "已定稿"`，或移除 TodoDrip

## 多水滴同一控件

在 `DripAnchor` 的 `drip` 内用 Fragment 并列：

```jsx
<DripAnchor side="end" drip={
  <>
    <NoteDrip inline title="…" body="…" prd={["§2.2 功能 5"]} />
    <TodoDrip inline todoId="T-002" />
  </>
}>
  <button>主 CTA</button>
</DripAnchor>
```

## PRD 必写声明（§2.3 模板要点）

- 蓝色备注水滴 = PRD/逻辑说明
- 橙色待办水滴 = 待办项
- 左侧 `proto-toolbar`：独立开关备注/待办，默认收起
- **生产环境：不得包含水滴、弹层、控制条、Tweaks**
