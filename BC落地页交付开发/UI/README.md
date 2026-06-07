# 躺着学 BC 落地页本地预览包

本目录为 [`BC落地页交付开发`](../) 交付包内的 **UI 预览子包**。开发验收 PRD 见 [`BC落地页PRD_6.5.md`](../BC落地页PRD_6.5.md)。

## 打开方式

1. 双击 `start.command`，浏览器会自动打开本地预览。
2. 或在此目录运行：

```bash
python3 -m http.server 5174
```

然后打开 `http://localhost:5174/`。

也可以直接双击 `index.html` 查看。推荐使用本地服务方式，资源路径和浏览器行为更接近线上。

## 目录

- `index.html`：落地页交付页（UI/交互参考）
- `assets/`：页面图片与 SVG 资源
- `vendor/`：React、ReactDOM、Babel 本地运行脚本

需求与验收文档在上一级目录：[`BC落地页PRD_6.5.md`](../BC落地页PRD_6.5.md)。
