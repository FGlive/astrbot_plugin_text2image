#!/usr/bin/env python3
"""测试渲染修复效果 - 验证字符裁切和 emoji 行显示问题"""

from pathlib import Path
from astrbot_plugin_text2image.core.renderer import TextRenderer

def test_character_clipping():
    """测试英文字符右侧裁切问题"""
    print("测试 1: 英文字符右侧裁切（MoviePilot）")
    print("=" * 50)

    config = {
        "image_width": 375,
        "image_scale": 2,
        "padding": 24,
        "font_size": 24,
        "line_height": 1.6,
        "bg_color": "#ffffff",
        "text_color": "#333333",
    }

    font_dir = Path(__file__).parent / "astrbot_plugin_text2image" / "ziti"
    renderer = TextRenderer(config, font_dir)

    test_text = """
**项目名称**：MoviePilot
**版本**：v2.9.11
**状态**：运行中
"""

    print(f"输入文本:\n{test_text}")
    result = renderer.render(test_text)
    if result:
        print(f"✅ 渲染成功: {result}")
        print("请检查生成的图片，确认 'MoviePilot' 右侧字符不再被裁切")
    else:
        print("❌ 渲染失败")

    return result is not None

def test_emoji_line_visibility():
    """测试 Emoji 行显示问题"""
    print("\n测试 2: Emoji 行显示（🚀 最近更新）")
    print("=" * 50)

    config = {
        "image_width": 375,
        "image_scale": 2,
        "padding": 24,
        "font_size": 24,
        "line_height": 1.6,
        "bg_color": "#ffffff",
        "text_color": "#333333",
    }

    font_dir = Path(__file__).parent / "astrbot_plugin_text2image" / "ziti"
    renderer = TextRenderer(config, font_dir)

    test_text = """
🚀 最近更新（v2.9.11）
- 新增功能 A
- 修复问题 B
- 性能优化 C
"""

    print(f"输入文本:\n{test_text}")
    result = renderer.render(test_text)
    if result:
        print(f"✅ 渲染成功: {result}")
        print("请检查生成的图片，确认 '🚀 最近更新（v2.9.11）' 行完整显示且未被裁切")
    else:
        print("❌ 渲染失败")

    return result is not None

def test_bold_and_list():
    """测试粗体和列表的宽度计算"""
    print("\n测试 3: 粗体文本和列表符号宽度")
    print("=" * 50)

    config = {
        "image_width": 375,
        "image_scale": 2,
        "padding": 24,
        "font_size": 24,
        "line_height": 1.6,
        "bg_color": "#ffffff",
        "text_color": "#333333",
    }

    font_dir = Path(__file__).parent / "astrbot_plugin_text2image" / "ziti"
    renderer = TextRenderer(config, font_dir)

    test_text = """
**这是粗体文本**，测试字符宽度计算是否正确。

- 列表项 1：MoviePilot
- 列表项 2：一些很长的文本需要自动换行显示
- 列表项 3：`code` 内联代码和**粗体**混合
"""

    print(f"输入文本:\n{test_text}")
    result = renderer.render(test_text)
    if result:
        print(f"✅ 渲染成功: {result}")
        print("请检查生成的图片，确认粗体文本和列表项右侧不再溢出或被裁切")
    else:
        print("❌ 渲染失败")

    return result is not None

def main():
    print("文本渲染修复测试")
    print("=" * 50)

    results = []
    results.append(("英文字符裁切", test_character_clipping()))
    results.append(("Emoji 行显示", test_emoji_line_visibility()))
    results.append(("粗体和列表", test_bold_and_list()))

    print("\n" + "=" * 50)
    print("测试总结:")
    print("=" * 50)
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{name}: {status}")

    all_passed = all(r[1] for r in results)
    print(f"\n总体结果: {'✅ 全部通过' if all_passed else '❌ 存在失败'}")

if __name__ == "__main__":
    main()
