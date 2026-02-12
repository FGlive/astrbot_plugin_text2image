"""集成测试：实际渲染测试"""
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    print("Starting integration test...")

    # 测试文本
    test_text = """# 测试文档

| 姓名 | 年龄 | 描述 |
|------|------|------|
| 张三 | 25 | 开发者 |
| 李四 | 30 | 设计师 |

这是普通文本。

## 表格测试

| 字段1 | 字段2 |
|-------|-------|
| 值A | 值B |

表格后面还有内容。

## 代码和Emoji测试

行内代码: `print("hello")`

代码中的Emoji应该正常显示: 测试😀🎉

代码块:
```python
# 注释
print("Hello 🌍")
```

纯Emoji测试: 👍💯✨
"""

    try:
        from astrbot_plugin_text2image.core.renderer import TextRenderer
        from pathlib import Path

        # 配置
        config = {
            "image_width": 500,
            "image_scale": 2,
            "padding": 24,
            "font_size": 24,
            "line_height": 1.6,
            "bg_color": "#ffffff",
            "text_color": "#333333",
        }

        font_dir = Path(__file__).parent / "astrbot_plugin_text2image" / "ziti"
        renderer = TextRenderer(config, font_dir)

        # 渲染
        output_path = renderer.render(test_text)
        print(f"SUCCESS: Image saved to: {output_path}")
        return 0

    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
