# BC 埋点开发说明

**读者**：前端开发、联调测试  
**产品口径**：见 [`BC落地页PRD_6.5.md`](./BC落地页PRD_6.5.md) §4.3.1  
**BC 官方规范**：[`3Ups_Partner_LandingPage_Tracking_Guide.pdf`](./3Ups_Partner_LandingPage_Tracking_Guide.pdf)  
**对接联系人**：杨效鲁 Yang.Xiaolu@britishcouncil.org.cn  
**阻塞待办**：T-010（SDK 凭证）、T-011（btn_id 联调验收）

---

## 1. 概述

本页须接入 **GrowingIO Web JS SDK 4.x**，向 BC 上报流量与转化数据。BC 合作方只关心 **3 项验收指标**；其余 `btn_id` 为产品侧预埋，联调时**不作为 BC 阻塞项**。

| BC 验收指标 | 开发侧实现方式 |
|------------|----------------|
| 网站访问量（PV + UV） | SDK 初始化后 **自动采集**，无需自定义事件 |
| 6 条路径主 CTA 点击 | `tracker_btn_click` + `bc_path_*_cta_click`（6 个语义化 `btn_id`，见 §3.2） |
| 本页注册成功用户数 | `tracker_btn_click` + `register_success` |

---

## 2. SDK 接入

### 2.1 初始化（`<head>` 内尽量靠前）

权威片段见 BC PDF §3.1。交付页实现位于 `UI/index.html` 头部：

```html
<!-- GrowingIO 4.x CDN -->
<script>/* gdp.js loader */</script>
<script>
  window.BC_GIO_CONFIG = window.BC_GIO_CONFIG || {
    accountId: "",      // T-010：BC 提供
    dataSourceId: "",   // T-010：区分生产 / 非生产
  };
  if (cfg.accountId && cfg.dataSourceId) {
    gdp("init", cfg.accountId, cfg.dataSourceId, {});
  }
</script>
```

**上线前**：将 `BC_GIO_CONFIG` 替换为 BC 提供的正式凭证（生产 / 非生产各一套）。

### 2.2 归因参数（URL 不得丢弃）

BC 引流跳转时携带，任何重定向须保留：

| 参数 | 用途 |
|------|------|
| `utm_source` / `utm_medium` / `utm_campaign` / `utm_content` | 渠道归因（SDK 自动采集） |
| `ut` | 用户脱敏唯一 ID，用于 `setUserId` |

### 2.3 访问用户上报（BC 强制 · 每次带 `ut` 的访问）

新版 BC 文档要求使用 `setUserId`，且须紧跟一条自定义事件（否则不会立即上报）：

```javascript
gdp('setUserId', ut);
gdp('track', 'tracker_btn_click', { btn_id: 'set_user_id' });
```

- `setUserId` **全页仅调用一次**，在页面初始化阶段完成  
- 无 `ut` 参数时：不上报用户 ID（具体兜底与 BC 联调确认，T-011）

---

## 3. BC 验收指标（已定口径）

### 3.1 网站访问量 — PV + UV

| 指标 | 口径 | 开发动作 |
|------|------|----------|
| **PV** | 每次打开落地页计 1 次，无需登录 | 确保 SDK `init` 成功即可，**无需**额外埋点 |
| **UV** | 独立访客数 | 同上，BC 在 GrowingIO 后台读取 |

BC 侧自行在 GrowingIO 看板取 PV、UV，前端不提供对应 `btn_id`。

### 3.2 六条路径主 CTA 点击

**只统计**路径卡片上的 **6 个主 CTA 按钮**（`PathCard` 内 `btn--ink` 主按钮）。

| btn_id | 路径 | 说明 |
|--------|------|------|
| `bc_path_course_detail_cta_click` | 01 名师课程 | 含未登录点击（会先弹登录窗） |
| `bc_path_ai_plan_cta_click` | 02 专属方案 | 登录后打开方案弹窗 |
| `bc_path_self_study_course_cta_click` | 03 自学录播 | — |
| `bc_path_camp_cta_click` | 04 训练营 | 打开微信咨询弹窗 |
| `bc_path_ai_calendar_cta_click` | 05 学习日历 | — |
| `bc_path_1v1_review_cta_click` | 06 精批诊断 | — |

**与六项指标分开统计**（独立 `btn_id`，BC 亦建议采集）：

- 导航「登录/注册」→ `bc_nav_login_register_click`
- 各路径「扫码咨询」→ `bc_path_01_wechat_consult_click` … `bc_path_06_wechat_consult_click`
- 顶部路径索引 → `bc_path_index_01_click` … `06`
- Hero 视频切换 → `bc_hero_video_01_select_click` … `06`
- 痛点「查看路径」→ `bc_pain_card_01_view_path_click` … `06`
- 互动诊断提交 → `bc_pain_quiz_submit_click`
- 顶栏 / 左侧流程轴锚点 → `bc_nav_anchor_*` / `bc_flow_axis_*`

**调用示例**：

```javascript
gdp('track', 'tracker_btn_click', { btn_id: 'bc_path_self_study_course_cta_click' });
```

交付页封装：`trackPathCta(pathIndex)`，`pathIndex` 为 0–5。

### 3.3 本页注册成功用户数

| btn_id | 触发条件 |
|--------|----------|
| `register_success` | 用户经本页 **任意入口**，在 **本页嵌入的登录/注册弹窗内** 完成 **新用户注册** 且服务端返回成功 |

**须同时满足**：

1. 来源标识为本 BC 落地页（与主站注册来源字段约定一致）  
2. 注册动作在 **本页弹窗内** 完成  
3. 为 **新注册**，非老用户登录  

**不得触发** `register_success` 的情形：

- 用户点击「登录」完成老账号登录  
- 用户经路径 CTA 登录/注册后 **跳转主站**，在主站或其他页面完成注册  

**正式环境接入**：主站注册组件在弹窗内鉴权成功后，调用：

```javascript
window.bcLandingTrackRegisterSuccess();
```

**禁止**在 `navigatePathCta()` 或任何主站外链跳转逻辑中调用此函数。

---

## 4. 联调事件清单（发给 BC）

**上报规范**：`tracker_btn_click` **仅传** `{ btn_id: '...' }`；**不传** `cta_label`、`path_idx`、`video_id` 等。行为区分靠不同 `btn_id`。

### 4.1 BC 验收必报

| btn_id | 触发时机 |
|--------|----------|
| `set_user_id` | 页面加载且 URL 含 `ut` |
| `bc_path_course_detail_cta_click` | 路径 01 主 CTA |
| `bc_path_ai_plan_cta_click` | 路径 02 主 CTA |
| `bc_path_self_study_course_cta_click` | 路径 03 主 CTA |
| `bc_path_camp_cta_click` | 路径 04 主 CTA |
| `bc_path_ai_calendar_cta_click` | 路径 05 主 CTA |
| `bc_path_1v1_review_cta_click` | 路径 06 主 CTA |
| `register_success` | 本页弹窗内新用户注册成功 |

### 4.2 建议一并联调（BC 反馈补充）

| 分组 | btn_id 模式 |
|------|-------------|
| 登录注册 | `bc_nav_login_register_click` |
| 扫码咨询 | `bc_path_01_wechat_consult_click` … `bc_path_06_wechat_consult_click` |
| 视频播放 | `bc_hero_video_01_play_click` … `06`（**每次点击计 1 次，不做用户去重**） |
| 视频切换 | `bc_hero_video_01_select_click` … `bc_hero_video_06_select_click` |
| 痛点模式切换 | `bc_pain_switch_to_card_click` / `bc_pain_switch_to_quiz_click` |
| 痛点选卡 | `bc_pain_card_select_click` |
| 痛点查看路径 | `bc_pain_card_01_view_path_click` … `bc_pain_card_06_view_path_click` |
| 问卷提交 | `bc_pain_quiz_submit_click` |
| 路径索引 | `bc_path_index_01_click` … `bc_path_index_06_click` |
| 顶栏锚点 | `bc_nav_anchor_hero_click` / `_pain_` / `_paths_` / `_proof_` |
| 左侧流程轴 | `bc_flow_axis_hero_click` … + `bc_flow_axis_path_01_click` … `06` |
| 路径 02 方案链路 | `bc_path02_plan_open_click` / `upload_submit` / `wait_close` / `gen_complete` / `gen_fail` / `view` / `download` / `overwrite_confirm` |

完整表见主 PRD §4.3.1。

---

## 5. 交付页代码位置

实现文件：**`UI/index.html`**（本交付包内路径：`./UI/index.html`）

| 模块 | 位置 / 符号 | 说明 |
|------|-------------|------|
| SDK 加载与 init | `<head>` 内 GrowingIO 脚本 | §2.1 |
| 工具函数 | `trackBcBtn` / `initBcUserId` / `useBcGrowingIO` | 统一上报入口 |
| 用户 ID | `initBcUserId()` | `App` 挂载时 `useBcGrowingIO()` 触发 |
| 路径 CTA | `trackPathCta(index)` → `BC_PATH_CTA_BTN_IDS` | index 0–5 |
| 扫码咨询 | `trackPathWechatConsult(pathIndex)` | 按路径 01–06 |
| 路径索引 | `trackPathIndexClick(i)` | |
| 导航锚点 | `trackNavAnchor(sectionId)` | |
| 流程轴 | `trackFlowAxisSection` / `trackFlowAxisPath` | |
| 注册成功 | `bcLandingTrackRegisterSuccess()` | 暴露到 `window`，供主站回调 |
| Demo 模拟注册 | `completeAuth('register')` | 演示环境内触发 `register_success` |

### 5.1 核心 API（交付页已实现）

```javascript
// 通用上报（仅 btn_id）
function trackBcBtn(btnId) {
  gdp('track', 'tracker_btn_click', { btn_id: btnId });
}

// 路径主 CTA（index: 0–5）→ bc_path_*_cta_click
function trackPathCta(index) { /* … */ }

// 注册成功（仅本页弹窗内新注册）
function bcLandingTrackRegisterSuccess() { trackBcBtn('register_success'); }
window.bcLandingTrackRegisterSuccess = bcLandingTrackRegisterSuccess;
```

---

## 6. 正式环境待接事项

| 项 | 负责 | 说明 |
|----|------|------|
| T-010 凭证 | BC / 对接 | 填入 `BC_GIO_CONFIG.accountId` / `dataSourceId` |
| 主站注册回调 | 前端 + 主站 | 弹窗内注册成功 → 调用 `bcLandingTrackRegisterSuccess()` |
| 注册来源字段 | 前端 + 后端 | 打开登录/注册时携带来源 = BC落地页，与 SVIP 赠礼规则一致 |
| T-011 联调 | 前端 / BC | 提供测试链接 + 上表 btn_id 清单 + 测试时间 |

---

## 7. 自测清单

### 7.1 Network 基础

- [ ] 页面加载 `gdp.js`，Status 200  
- [ ] `BC_GIO_CONFIG` 已配置时，`gdp('init', …)` 已执行  
- [ ] 带 `?ut=xxx&utm_source=bc` 访问：出现 `setUserId` 相关上报 + `btn_id: set_user_id`  
- [ ] GrowingIO 域名 `*.growingio.com` 有上报，Status 200 / 204  

### 7.2 BC 三项指标

- [ ] **PV / UV**：刷新页面、换浏览器 / 隐身窗口，BC 后台可看到 PV、UV 变化（无需自定义事件）  
- [ ] **路径 CTA**：依次点击 6 条路径主按钮，Network 中分别出现 `bc_path_course_detail_cta_click` … `bc_path_1v1_review_cta_click`  
- [ ] **注册成功**：在本页弹窗点「注册」并完成（Demo 或联调环境），出现 `register_success`  
- [ ] 点「登录」或跳转主站后注册：**不出现** `register_success`  

### 7.3 补充点击（BC 建议联调）

- [ ] 导航「登录/注册」→ `bc_nav_login_register_click`  
- [ ] 6 个「扫码咨询」→ `bc_path_0N_wechat_consult_click`  
- [ ] 播放列表切换 → `bc_hero_video_0N_select_click`  
- [ ] 主播放器点击播放 → `bc_hero_video_0N_play_click`（同一用户重复播放仍每次上报）  
- [ ] 痛点模式切换 / 选卡 → `bc_pain_switch_to_*` / `bc_pain_card_select_click`  
- [ ] 痛点「查看路径」→ `bc_pain_card_0N_view_path_click`  
- [ ] 互动诊断提交 → `bc_pain_quiz_submit_click`  
- [ ] 路径索引 6 标签 → `bc_path_index_0N_click`  
- [ ] 顶栏 / 左侧流程轴锚点 → `bc_nav_anchor_*` / `bc_flow_axis_*`  

### 7.4 负向用例

- [ ] 点击路径索引条：出现 `bc_path_index_0N_click`，**不计入** BC 六项主 CTA 指标  
- [ ] 点击扫码咨询副按钮：出现 `bc_path_0N_wechat_consult_click`，**不计入** BC 六项主 CTA 指标  
- [ ] 无 `ut` 参数访问：不报错；`set_user_id` 不上报（或按联调约定）  

---

## 8. 产品预埋事件（非 BC 阻塞）

以下事件已在交付页预埋，**BC 联调建议一并验收**（见 §4.2），但不计入 BC 三项核心指标：

`bc_nav_login_register_click`、`bc_nav_anchor_*`、`bc_flow_axis_*`、`bc_hero_video_*`、`bc_pain_*`、`bc_path_index_*`、`bc_path_*_wechat_consult_click`、`bc_path02_*_click` 等。

完整列表见 PRD §4.3.1「完整清单」表。

---

## 9. 文档关系

```
3Ups_Partner_LandingPage_Tracking_Guide.pdf   ← BC 官方 SDK 规范
BC落地页PRD_6.5.md §4.3.1                     ← 产品口径与验收标准
BC埋点开发说明.md（本文）                      ← 开发实现与联调指引
UI/index.html                                 ← 交付页实现
```

---

*最后更新：2026-06-09 · 口径：语义化 `btn_id`、仅传 `btn_id`、视频播放每次点击计次、PV+UV / 6 路径主 CTA / 本页弹窗内新注册*
