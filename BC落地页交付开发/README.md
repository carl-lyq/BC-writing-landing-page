# BC 写作落地页 · 开发交付包

> **版本**：PRD **v6.5.2** · 2026-05-28  
> **读者**：前端、后端、测试、数据 — **请先读** [`BC落地页-开发交接.md`](./BC落地页-开发交接.md)

## 目录结构

```
BC落地页交付开发/
├── README.md                         ← 本文件（交付包索引）
├── BC落地页PRD_6.5.md                ← 开发验收唯一 PRD
├── BC落地页-开发交接.md              ← 开发立项必读
├── BC落地页ToDo.md                   ← 待办追踪
├── 3Ups_Partner_LandingPage_Tracking_Guide.pdf  ← BC 埋点规范（2026-06 更新版）
├── BC埋点开发说明.md                            ← 埋点开发实现与联调指引
├── BC落地页6.8补充/                             ← 6.8 批次图片素材 + 落位说明
├── BC备考平台logo/                   ← BC 品牌源文件（T-008）
└── UI/                               ← 本地预览（站点根目录）
    ├── index.html                    ← UI/交互主参考（含水滴，生产剔除）
    ├── start.command
    ├── assets/
    └── vendor/
```

## 快速开始

```bash
cd UI && python3 -m http.server 5175
# 打开 http://127.0.0.1:5175/
```

或双击 `UI/start.command`。

**注意**：必须以 `UI/` 为 HTTP 站点根，否则 `./assets/` 与 `./vendor/` 路径会 404。

## 文档引用关系

| 用途 | 文件 |
|------|------|
| **开发验收（唯一）** | `BC落地页PRD_6.5.md` + `UI/index.html` + `UI/assets/` |
| 立项必读 | `BC落地页-开发交接.md` |
| 阻塞项 | `BC落地页ToDo.md` |
| BC 埋点 | `BC埋点开发说明.md` + `3Ups_Partner_LandingPage_Tracking_Guide.pdf` |

交付页水滴链接已指向上述包根文档，**不含**产品工作稿或多版本 PRD。

## 仍待补齐（见 ToDo）

| 项 | ID | 说明 |
|----|-----|------|
| 问卷正式规则 | T-001 | 模式 B 验收 |
| 导航 Logo URL | T-002 | 路径 CTA 已定 |
| Hero 视频地址等 | T-003b | 封面/时长/播放 URL |
| 正式品牌素材 | T-008 | 页面已接 Demo 资产 |
| GrowingIO 凭证 | T-010 | BC 提供 |
| 6 条路径专属媒体图 | T-016 | 16:10 正式图（当前共用占位） |

完整列表见 [`BC落地页ToDo.md`](./BC落地页ToDo.md)。
