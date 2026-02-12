"""完整测试：表格、行内代码、emoji"""
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from astrbot_plugin_text2image.core.markdown import parse_markdown, LineContext

def test_all():
    print("=== 测试 1: 表格转列表 ===")
    lines = [
        "| 字段1 | 字段2 |",
        "|-------|-------|",
        "| 值A | 值B |",
        ""
    ]
    ctx = LineContext()
    for line in lines:
        parse_markdown(line, ctx)
    print(f"表格解析完成，table_rows={len(ctx.table_rows)}")

    print("\n=== 测试 2: 行内代码 ===")
    ctx2 = LineContext()
    result = parse_markdown("这是`代码`测试", ctx2)
    print(f"片段数: {len(result)}")
    for seg in result:
        print(f"  text='{seg.text}', code={seg.code}")

    print("\n=== 测试 3: 行内代码+emoji ===")
    ctx3 = LineContext()
    result3 = parse_markdown("这是`代码😀`测试", ctx3)
    print(f"片段数: {len(result3)}")
    for seg in result3:
        print(f"  text='{seg.text}', code={seg.code}, is_emoji={seg.is_emoji}")

    print("\n=== 测试 4: 纯emoji ===")
    ctx4 = LineContext()
    result4 = parse_markdown("测试😀🎉", ctx4)
    print(f"片段数: {len(result4)}")
    for seg in result4:
        print(f"  text='{seg.text}', code={seg.code}, is_emoji={seg.is_emoji}")

if __name__ == "__main__":
    test_all()
