# 文字转图片

AstrBot 插件，将 Bot 文字回复渲染为图片。

## 功能

- 自适应高度
- 手机宽度 (375px @2x 高清)
- 支持 emoji（Twemoji 彩色图标）
- 支持自动撤回

## 配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| enable_render | 启用渲染 | true |
| render_scope | llm_only / all_text | llm_only |
| render_char_threshold | 字符阈值，0=不限 | 0 |
| image_width | 逻辑宽度 | 375 |
| image_scale | 渲染倍数 | 2 |
| font_size | 字体大小 | 24 |
| line_height | 行高倍数 | 1.6 |
| bg_color | 背景色 | #ffffff |
| text_color | 文字色 | #333333 |
| recall_enabled | 启用自动撤回 | false |
| recall_time | 撤回时间（秒） | 30 |

## 致谢

- [小钊 / astrbot_plugin_recall_xz](https://github.com/zxqtd/astrbot_plugin_recall_xz) - 自动撤回功能参考
- [传话筒·立绘对话框](https://github.com/bvzrays/astrbot_plugin_chuanhuatong) - 原始项目
