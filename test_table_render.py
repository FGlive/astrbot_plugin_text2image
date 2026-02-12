"""测试表格渲染修改"""
import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from astrbot_plugin_text2image.core.markdown import parse_markdown, LineContext
from astrbot_plugin_text2image.core.renderer import TextRenderer
from astrbot_plugin_text2image.core.styles import TextSegment

def test_table_to_list():
    """测试表格转换为列表"""
    test_text = """| 姓名 | 年龄 | 城市 |
|------|------|------|
| 张三 | 25 | 北京 |
| 李四 | 30 | 上海 |"""

    ctx = LineContext()
    segments = []

    for line in test_text.split('\n'):
        result = parse_markdown(line, ctx)
        segments.extend(result)

    print("=== 表格转换为列表测试 ===")
    print(f"生成的片段数: {len(segments)}")

    for i, seg in enumerate(segments):
        print(f"片段 {i+1}: text='{seg.text[:20]}...', list_item={seg.list_item}, "
              f"code={seg.code}, emoji={seg.is_emoji}, no_wrap={seg.no_wrap}")

    # 验证预期行为
    assert all(seg.list_item for seg in segments), "所有片段应该是列表项"
    assert not any(seg.no_wrap for seg in segments), "不应该有 no_wrap 标记"
    print("✅ 表格转列表测试通过")


def test_inline_code_emoji():
    """测试行内代码中的 emoji"""
    test_text = "这是`代码😀`中的表情"

    ctx = LineContext()
    segments = parse_markdown(test_text, ctx)

    print("\n=== 行内代码 Emoji 测试 ===")
    print(f"生成的片段数: {len(segments)}")

    for i, seg in enumerate(segments):
        print(f"片段 {i+1}: text='{seg.text}', code={seg.code}, emoji={seg.is_emoji}")

    # 查找 emoji 片段
    emoji_segs = [seg for seg in segments if seg.is_emoji]
    print(f"找到 {len(emoji_segs)} 个 emoji 片段")

    if emoji_segs:
        print("✅ Emoji 片段识别成功")
    else:
        print("⚠️ Emoji 片段未识别，可能需要检查 split_text 逻辑")


def test_code_block_emoji():
    """测试代码块中的 emoji"""
    test_text = """```python
# 这是注释 😀
print("Hello 🌍")
```"""

    ctx = LineContext()
    segments = []

    for line in test_text.split('\n'):
        result = parse_markdown(line, ctx)
        segments.extend(result)

    print("\n=== 代码块 Emoji 测试 ===")
    print(f"生成的片段数: {len(segments)}")

    for i, seg in enumerate(segments):
        print(f"片段 {i+1}: text='{seg.text[:30]}...', code_block={seg.code_block}, "
              f"emoji={seg.is_emoji}, no_wrap={seg.no_wrap}")

    # 查找 emoji 片段（不应该有 code_block=True 的 emoji）
    emoji_in_code = [seg for seg in segments if seg.is_emoji and seg.code_block]
    print(f"错误标记为 code_block 的 emoji 数: {len(emoji_in_code)}")

    if not emoji_in_code:
        print("✅ 代码块 Emoji 处理正确")
    else:
        print("⚠️ 存在错误标记的 emoji 片段")


if __name__ == "__main__":
    test_table_to_list()
    test_inline_code_emoji()
    test_code_block_emoji()
    print("\n所有测试完成！")
