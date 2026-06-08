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
| 6 条路径主 CTA 点击 | `tracker_btn_click` + `path_cta_01` … `path_cta_06` |
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
| `path_cta_01` | 01 名师课程 | 含未登录点击（会先弹登录窗） |
| `path_cta_02` | 02 专属方案 | 登录后打开方案弹窗 |
| `path_cta_03` | 03 自学录播 | — |
| `path_cta_04` | 04 训练营 | 打开微信咨询弹窗 |
| `path_cta_05` | 05 学习日历 | — |
| `path_cta_06` | 06 精批诊断 | — |

**不计入 BC 六项指标**（产品预埋，可保留代码但联调不验收）：

- 顶部路径索引条 → `path_index_click`
- 各路径「扫码咨询」副按钮 → `path_wechat_consult`

**调用示例**：

```javascript
gdp('track', 'tracker_btn_click', { btn_id: 'path_cta_03' });
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

以下为 T-011 联调时须与 BC 确认的 **完整自定义事件列表**：

| btn_id | 触发时机 | BC 验收 |
|--------|----------|---------|
| `set_user_id` | 页面加载且 URL 含 `ut` | 强制（BC 文档） |
| `path_cta_01` | 路径 01 主 CTA 点击 | ✅ |
| `path_cta_02` | 路径 02 主 CTA 点击 | ✅ |
| `path_cta_03` | 路径 03 主 CTA 点击 | ✅ |
| `path_cta_04` | 路径 04 主 CTA 点击 | ✅ |
| `path_cta_05` | 路径 05 主 CTA 点击 | ✅ |
| `path_cta_06` | 路径 06 主 CTA 点击 | ✅ |
| `register_success` | 本页弹窗内新用户注册成功 | ✅ |

统一事件名：`tracker_btn_click`  
事件级变量：`{ btn_id: '<上表取值>' }`（可按需附加 `video_id`、`path_idx` 等，BC 验收不依赖）

---

## 5. 交付页代码位置

实现文件：**`UI/index.html`**（本交付包内路径：`./UI/index.html`）

| 模块 | 位置 / 符号 | 说明 |
|------|-------------|------|
| SDK 加载与 init | `<head>` 内 GrowingIO 脚本 | §2.1 |
| 工具函数 | `trackBcBtn` / `initBcUserId` / `useBcGrowingIO` | 统一上报入口 |
| 用户 ID | `initBcUserId()` | `App` 挂载时 `useBcGrowingIO()` 触发 |
| 路径 CTA | `trackPathCta(index)` → `PathCard.handlePathCta` | index 0–5 |
| 注册成功 | `bcLandingTrackRegisterSuccess()` | 暴露到 `window`，供主站回调 |
| Demo 模拟注册 | `completeAuth('register')` | 演示环境内触发 `register_success` |

### 5.1 核心 API（交付页已实现）

```javascript
// 通用上报
function trackBcBtn(btnId, extra?) {
  gdp('track', 'tracker_btn_click', { btn_id: btnId, ...extra });
}

// 路径主 CTA（index: 0–5）
function trackPathCta(index) { /* → path_cta_01…06 */ }

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
- [ ] **路径 CTA**：依次点击 6 条路径主按钮，Network 中分别出现 `path_cta_01` … `path_cta_06`  
- [ ] **注册成功**：在本页弹窗点「注册」并完成（Demo 或联调环境），出现 `register_success`  
- [ ] 点「登录」或跳转主站后注册：**不出现** `register_success`  

### 7.3 负向用例

- [ ] 点击路径索引条：若有 `path_index_click`，BC 验收指标**不应**依赖此事件  
- [ ] 点击扫码咨询副按钮：若有 `path_wechat_consult`，同上  
- [ ] 无 `ut` 参数访问：不报错；`set_user_id` 不上报（或按联调约定）  

---

## 8. 产品预埋事件（非 BC 阻塞）

以下事件已在交付页预埋，供躺着学内部分析，**T-011 不必作为 BC 验收阻塞**：

`nav_login_register`、`nav_anchor_*`、`hero_video_play`、`hero_playlist_item_click`、`pain_*`、`path_index_click`、`path02_*`、`path_wechat_consult` 等。

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

*最后更新：2026-06-08 · 口径：PV+UV / 仅 6 路径主 CTA / 本页弹窗内新注册*
